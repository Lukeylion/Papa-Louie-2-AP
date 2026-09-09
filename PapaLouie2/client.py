"""
PapaLouie2 Archipelago client.

Drop this file in your apworld folder as client.py (alongside __init__.py,
items.py, locations.py, etc). It plays the same role the Node.js bridge did,
but as a real Archipelago client built on CommonClient — meaning the AP
protocol handshake, reconnect logic, and DataPackage handling all come for
free from Archipelago's own code instead of being reimplemented by hand.

WHAT IT DOES:
  - Connects to your Archipelago server as a normal client (same as any
    other game's client.py).
  - Opens a small local TCP server that your patched SWF (running in Flash
    Player Projector) connects to via flash.net.XMLSocket, using the exact
    same message format the Node.js bridge used:
        SWF -> client:  {"type":"check","world":0,"challenge":1}\0
        client -> SWF:  {"type":"item","id":26,"name":"Warp Key"}\0
        client -> SWF:  {"type":"connected","slot":1,"team":0}\0
      (each message is one line of JSON terminated with a null byte,
       matching what AS3's XMLSocket expects)
  - Also answers XMLSocket's automatic policy-file request, since Flash
    always sends one before it'll allow the connection through.

CAVEAT: this is written against Archipelago's public CommonClient.py source
as of writing, but has not been run against a live Archipelago install from
here — expect to need small fixes once you actually try it (import paths,
minor API differences between AP versions, etc). Send me any tracebacks
and I'll help sort them out.
"""

from __future__ import annotations

import asyncio
import json
import time
import typing

import Utils
from CommonClient import CommonContext, ClientCommandProcessor, server_loop, gui_enabled, get_base_parser, logger
from NetUtils import ClientStatus

if typing.TYPE_CHECKING:
    from NetUtils import NetworkItem

# ---------------------------------------------------------------
# (whichWorld, whichChallenge) -> apworld location name.
# Same table as the Node.js bridge — built from ChallengeManager's
# decompiled challenge list, cross-referenced against locations.py.
# World 8 / challenge 1 ("Papa Louie Rescued") is an EVENT location
# (address=None) and is intentionally not sent as a location check.
# ---------------------------------------------------------------
WORLD_CHALLENGE_TO_LOCATION: dict[int, dict[int, str]] = {
    0: {0: "Level1 Complete", 1: "Prudence Rescued", 2: "Taylor Rescued", 3: "Clover Rescued", 4: "Level1 Find 5 Red Coins", 5: "Level1 Defeat 3 Burgerzillas", 6: "Level1 Find 100 Coins"},
    1: {0: "Level2 Complete", 1: "Big Pauly Rescued", 2: "Mindy Rescued", 3: "Akari Rescued", 4: "Level2 Find 5 Flowers", 5: "Level2 Defeat 11 Burgerzillas", 6: "Level2 Find 100 Coins"},
    2: {0: "Level3 Complete", 1: "Boomer Rescued", 2: "Kahuna Rescued", 3: "Prof. Fitz Rescued", 4: "Level3 Find 5 Gold Helmets", 5: "Level3 Defeat 11 Burgerzillas", 6: "Level3 Find 100 Coins"},
    3: {0: "Level4 Complete", 1: "Georgito Rescued", 2: "Foodini Rescued", 3: "Yippy Rescued", 4: "Level4 Find 5 Purple Coins", 5: "Level4 Defeat 6 Burgerzillas", 6: "Level4 Find 100 Coins"},
    4: {0: "Level5 Complete", 1: "Scooter Rescued", 2: "Kingsley Rescued", 3: "Connor Rescued", 4: "Level5 Find 5 Gummie Worms", 5: "Level5 Defeat 8 Burgerzillas", 6: "Level5 Find 100 Coins"},
    5: {0: "Level6 Complete", 1: "James Rescued", 2: "Greg Rescued", 3: "Captain Cori Rescued", 4: "Level6 Find 5 Gold Ballons", 5: "Level6 Defeat 10 Burgerzillas", 6: "Level6 Find 100 Coins"},
    6: {0: "Level7 Complete", 1: "Ninjoy Rescued", 2: "Peggy Rescued", 3: "Penny Rescued", 4: "Level7 Find 5 Sodas", 5: "Level7 Defeat 13 Burgerzillas", 6: "Level7 Find 100 Coins"},
    7: {0: "Level8 Complete", 1: "Sarge Fan Rescued", 2: "Rico Rescued", 3: "Zoe Rescued", 4: "Level8 Find 5 Raddish Coins", 5: "Level8 Defeat 12 Burgerzillas", 6: "Level8 Find 100 Coins"},
    8: {0: "Level9 Complete", 1: "Papa Louie Rescued"},  # challenge 1 here is the EVENT location — never sent as a check
}

LOCAL_HOST = "127.0.0.1"
LOCAL_PORT = 8082

POLICY_REQUEST = b"<policy-file-request/>\x00"
POLICY_RESPONSE = (
    '<?xml version="1.0"?>'
    '<!DOCTYPE cross-domain-policy SYSTEM "http://www.adobe.com/xml/dtds/cross-domain-policy.dtd">'
    '<cross-domain-policy><allow-access-from domain="*" to-ports="*" /></cross-domain-policy>\x00'
).encode("utf-8")


class PapaLouie2ClientCommandProcessor(ClientCommandProcessor):
    def _cmd_papa(self) -> None:
        """Show whether the patched SWF is currently connected to this client."""
        ctx = typing.cast("PapaLouie2Context", self.ctx)
        connected = ctx.swf_writer is not None
        self.output(f"SWF connected: {connected}")

    def _cmd_deathlink(self) -> None:
        """Toggle DeathLink on/off."""
        ctx = typing.cast("PapaLouie2Context", self.ctx)
        ctx.death_link_enabled = not ctx.death_link_enabled
        if ctx.death_link_enabled:
            ctx.tags = ctx.tags | {"DeathLink"}
        else:
            ctx.tags = ctx.tags - {"DeathLink"}
        Utils.async_start(ctx.send_msgs([{
            "cmd": "ConnectUpdate",
            "tags": list(ctx.tags),
            "items_handling": ctx.items_handling,
        }]))
        self.output(f"DeathLink: {'enabled' if ctx.death_link_enabled else 'disabled'}")


class PapaLouie2Context(CommonContext):
    game = "PapaLouie2"
    items_handling = 0b111  # all items, including our own and starting inventory
    command_processor = PapaLouie2ClientCommandProcessor

    def __init__(self, server_address: str | None, password: str | None) -> None:
        super().__init__(server_address, password)
        self.swf_reader: asyncio.StreamReader | None = None
        self.swf_writer: asyncio.StreamWriter | None = None
        self.swf_server: asyncio.base_events.Server | None = None
        self.swf_items_forwarded: int = 0  # count of items_received already forwarded to the SWF
        self.goal_completed: bool = False
        self.death_link_enabled: bool = False  # off by default — toggle with the !deathlink command
        self.expecting_local_death_from_link: bool = False  # suppress echo: don't rebroadcast a death we just forced
        if self.death_link_enabled:
            self.tags = self.tags | {"DeathLink"}

    # -----------------------------------------------------------
    # CommonClient overrides
    # -----------------------------------------------------------
    async def server_auth(self, password_requested: bool = False) -> None:
        if password_requested and not self.password:
            await super().server_auth(password_requested)
        await self.get_username()
        await self.send_connect()

    def on_package(self, cmd: str, args: dict) -> None:
        if cmd == "Connected":
            Utils.async_start(self.send_to_swf({
                "type": "connected",
                "slot": self.slot,
                "team": self.team,
            }))
            Utils.async_start(self._forward_pending_items())

        elif cmd == "ReceivedItems":
            Utils.async_start(self._forward_pending_items())

        elif cmd == "Bounced":
            tags = args.get("tags", [])
            if "DeathLink" in tags:
                Utils.async_start(self._handle_incoming_death_link(args.get("data", {})))

    async def _handle_incoming_death_link(self, data: dict) -> None:
        if not self.death_link_enabled:
            return
        source = data.get("source")
        if source == self.player_names.get(self.slot):
            return  # our own death bouncing back to us — ignore
        cause = data.get("cause", "")
        logger.info(f"DeathLink received from {source}: {cause}")
        self.expecting_local_death_from_link = True
        await self.send_to_swf({"type": "kill"})

    async def _forward_pending_items(self) -> None:
        # Forward items strictly by position in items_received, not by item
        # ID — several items in this game (Warp Key x23, +100 Points) share
        # the same ID across multiple copies, so ID-based dedup would
        # silently drop every copy after the first. Tracking how many we've
        # forwarded so far handles duplicates correctly and is also safe
        # across SWF reconnects within the same client process.
        while self.swf_items_forwarded < len(self.items_received):
            item = self.items_received[self.swf_items_forwarded]
            name = self.item_names.lookup_in_game(item.item)
            await self.send_to_swf({"type": "item", "id": item.item, "name": name})
            self.swf_items_forwarded += 1

    # -----------------------------------------------------------
    # SWF-facing TCP server (XMLSocket-compatible framing)
    # -----------------------------------------------------------
    async def start_swf_server(self) -> None:
        self.swf_server = await asyncio.start_server(self._handle_swf_connection, LOCAL_HOST, LOCAL_PORT)
        logger.info(f"Listening for the patched SWF on {LOCAL_HOST}:{LOCAL_PORT}")

    async def _handle_swf_connection(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
        self._conn_counter = getattr(self, "_conn_counter", 0) + 1
        conn_id = self._conn_counter
        peer = writer.get_extra_info("peername")
        logger.info(f"[conn#{conn_id}] SWF connected from {peer}")
        self.swf_reader, self.swf_writer = reader, writer
        try:
            buffer = b""
            while True:
                chunk = await reader.read(4096)
                if not chunk:
                    break
                buffer += chunk

                if buffer.startswith(b"<policy-file-request/>"):
                    writer.write(POLICY_RESPONSE)
                    await writer.drain()
                    buffer = buffer[len(POLICY_REQUEST):]
                    continue

                while b"\x00" in buffer:
                    raw, buffer = buffer.split(b"\x00", 1)
                    if raw:
                        await self._handle_swf_message(raw.decode("utf-8"))
        except (ConnectionResetError, asyncio.IncompleteReadError):
            pass
        finally:
            logger.info(f"[conn#{conn_id}] SWF disconnected")
            if self.swf_writer is writer:
                self.swf_reader = None
                self.swf_writer = None

    async def send_to_swf(self, obj: dict) -> None:
        if self.swf_writer is None:
            logger.info(f"No SWF connected, dropping message: {obj}")
            return
        # separators=(",", ":") produces compact JSON with no spaces —
        # required because the AS3 side no longer uses a real JSON parser
        # (see AS3_PATCH_NOTES.txt) and instead does simple substring
        # extraction that assumes no whitespace around ":" or ",".
        self.swf_writer.write((json.dumps(obj, separators=(",", ":")) + "\x00").encode("utf-8"))
        await self.swf_writer.drain()

    async def _handle_swf_message(self, raw: str) -> None:
        try:
            msg = json.loads(raw)
        except json.JSONDecodeError:
            logger.info(f"Failed to parse SWF message: {raw!r}")
            return

        if msg.get("type") == "check":
            world, challenge = msg.get("world"), msg.get("challenge")
            name = WORLD_CHALLENGE_TO_LOCATION.get(world, {}).get(challenge)
            if name is None:
                logger.info(f"Unknown world/challenge from SWF: {world}/{challenge}")
                return
            if name == "Papa Louie Rescued":
                # Event location — has no real network ID, so there's
                # nothing to send via LocationChecks. But reaching it IS
                # this slot's goal (world.set_completion_rule(Has("Victory"))
                # in world.py), and since event items are never sent over
                # the network either, the server has no other way to learn
                # the goal was met — we have to tell it explicitly.
                logger.info("Reached victory event (Papa Louie Rescued) — sending goal completion to server.")
                if not self.goal_completed:
                    self.goal_completed = True
                    await self.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
                return
            location_id = _reverse_lookup(self, name)
            if location_id is None:
                logger.info(f'Location "{name}" not found in DataPackage — is game/apworld name set correctly?')
                return
            await self.check_locations([location_id])
        elif msg.get("type") == "death":
            if not self.death_link_enabled:
                return
            if self.expecting_local_death_from_link:
                # This death was caused by us forcing a kill from an
                # incoming DeathLink — don't rebroadcast it, or every
                # DeathLink would echo back and forth between players.
                self.expecting_local_death_from_link = False
                return
            logger.info("Sending DeathLink (local death)")
            await self.send_msgs([{
                "cmd": "Bounce",
                "tags": ["DeathLink"],
                "data": {
                    "time": time.time(),
                    "source": self.player_names.get(self.slot, self.auth),
                    "cause": f"{self.player_names.get(self.slot, self.auth)} Got Louied By The Papa",
                },
            }])
        else:
            logger.info(f"Unknown message type from SWF: {msg}")


def _reverse_lookup(ctx: PapaLouie2Context, location_name: str) -> int | None:
    """Find a location's numeric id by name using the context's loaded data package."""
    if not ctx.game:
        return None
    for loc_id, name in ctx.location_names[ctx.game].items():
        if name == location_name:
            return loc_id
    return None


def launch() -> None:
    async def main(args) -> None:
        ctx = PapaLouie2Context(args.connect, args.password)
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="server loop")

        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()

        await ctx.start_swf_server()

        await ctx.exit_event.wait()
        await ctx.shutdown()

    import colorama

    parser = get_base_parser()
    args = parser.parse_args()

    colorama.init()
    asyncio.run(main(args))
    colorama.deinit()


if __name__ == "__main__":
    launch()