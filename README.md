# Papa-Louie-2-AP
An Archipelago Mod For Papa Louie 2

AI DISCLAIMER: THE ACTUAL MOD WAS MADE WITH THE HELP OF AI HOWEVER THE APWORLD OUTSIDE OF THE CLIENT IS ALL HUMAN


DISCLAIMER 2: DUE TO COPYRIGHT I CANNOT DISTRIBUTE THE MODDED FILES SO THERE ARE A LOT OF STEPS TO SET THIS UP SORRY IN ADVANCE IT SHOULDN'T BE THAT HARD THOUGH 
Guide:
MOD SETUP START
1. Download the latest version of JPEX from https://github.com/jindrapetrik/jpexs-decompiler/releases/tag/version26.2.1
2. Download the latest version of Adobe Flash Player Projector from https://github.com/Grubsic/Adobe-Flash-Player-Debug-Downloads-Archive (Note for Linux Users download the .exe and run it through proton 9.0-4 on steam trust me the Linux version of flash player is awful)
3. Go to https://www.coolmathgames.com/0-papa-louie-2-when-burgers-attack wait for the game to fully load then right click outside the game window and click inspect elements
4. Go to network it may ask you to reload press reload if it does
5. Up the top theres a search bar <img width="657" height="38" alt="image" src="https://github.com/user-attachments/assets/5834dd5a-17d4-409e-8634-d1ed7c22990e" /> type .swf into it and double click on papalouie2_sdk_coolmath.swf don't worry about the fonts.swf
6. Open up JPEX the executable is called ffdec yes its weird
7. Once it opens press Open in the top left and open the papalouie2_sdk_coolmath.swf file that you just installed
8. Now on the left there will be a bunch of folders just scroll down until you find papaGame.data
9. Right click on papaGame.data and press add class
10. Name it ApClient it needs to be exactly like that
11. When it asks select docb tag change it to frame2
12. Then copy the code from the file in this repository named ApClient (Not in releases)
13. Click the new ApClient file you just made and press edit actionscript underneath the code window and paste the copied code
14. Press save down the bottom and find a folder called package_4 in that theres a file named class_5 open it
15. Now where it says <img width="352" height="38" alt="image" src="https://github.com/user-attachments/assets/70aef82b-a10f-4f62-bee5-44ec783c3eb8" /> under that { paste public var apClient:ApClient;
16. Now scroll down past the final public var which is public var var_239:Boolean = false; right under that replace the punlic function class_5() with
      public function class_5()
      {
         this.apClient = new ApClient(this.var_106,this.var_112,this.var_113,this);
         super();
      }
17. Scroll down to public function method_196() : void and under \_loc1_.var_109.prepareLevelData(false); add this.apClient = new ApClient(this.var_106,this.var_112,this.var_113,this);
18. Now scroll down to public function finishLevel() : void and under var \_loc1_:class5; add var completedLevel:Number;
19. Now under \_loc_1 = this add completedLevel = \_loc1_.var_109.currentLevel;
20. Now under that add \_loc1_.apClient.sendCheck(completedLevel,0);
21. Scroll down to public function method_132() : void and under \_loc1_ = this; add \_loc1_.apClient.sendDeath()
23. Now press save at the bottom and go to papaGame.models.objects GameObject19
24. Find \_loc1_.gameObj.var_106.unlockCustomer(_loc1_.customerActualIndex); and infront of it add //
25. Press save down the bottom and go to papaGame.data UserData
26. Find public function completeChallenge(param1:Number, param2:Number) : void and above if(param1 !=9) add /* and under the third } under catch(err:Error) add */
27. Now press save at the bottom and go to papaGame.managers Challenge Manager
28. Under the } under \_loc5_.updateDisplay(); add _loc2_.gameObj.apClient.sendCheck(_loc7_.whichWorld,_loc7_.whichChallenge); to public function recordBurgerzilla(param1:Number = 1) : void, public function recordCoin(param1:Number = 1) : void, public function recordSpecialItem(param1:Number = 1) : void and public function recordCustomerCage(param1:Number) : void
29. Save that and if you havent already press the save at the top or save as if you want to save it as a different name
30. Test if everything still works by opening the adobe flash player pressing open -> browse and find the .swf file
MOD SETUP END

AP SETUP START
I assume you know how to make the archipelago server so I won't go over that here
1. Download PapaLouie2.apworld from the latest releases
2. Add it to the archipelago launcher
3. Open the archipelago launcher and search for papalouie2client **IMPORTANT DO NOT CONNECT TO THE SERVER YET**
4. Open the .swf file in adobe flash player and after the loading press continue
5. The client should say a 3 \[Conn#NUMBER] SWF Connected and one \[Conn#NUMBER] Disconnected
6. Create a new profile the second \[Conn#NUMBER] may disconnect thats fine as long as the third is still connected
7. Now once you've loading into the game you can connect to the server by typing in the port at the top and slot name and password if needed at the bottom
NOTE: TO ENABLE DEATHLINK TYPE /deathlink INTO THE COMMAND BAR AT THE BOTTOM OF THE CLIENT
AP SETUP END
