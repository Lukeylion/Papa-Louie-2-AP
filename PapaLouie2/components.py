from worlds.LauncherComponents import Component, components, Type, launch_subprocess


def launch_client() -> None:
    from .client import launch
    launch_subprocess(launch, name="PapaLouie2Client")


components.append(Component(
    "PapaLouie2 Client",
    func=launch_client,
    component_type=Type.CLIENT,
))