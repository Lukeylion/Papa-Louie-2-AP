# Papa-Louie-2-AP
An Archipelago Mod For Papa Louie 2

AI DISCLAIMER: THE ACTUAL MOD WAS MADE WITH THE HELP OF AI HOWEVER THE APWORLD OUTSIDE OF THE CLIENT IS ALL HUMAN


DISCLAIMER 2: DUE TO COPYRIGHT I CANNOT DISTRIBUTE THE MODDED FILES SO THERE ARE A LOT OF STEPS TO SET THIS UP SORRY IN ADVANCE IT SHOULDN'T BE THAT HARD THOUGH 
Guide:
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
11. Then copy the code from the file in this repository named ApClient (Not in releases)
12. Click the new ApClient file you just made and press edit actionscript underneath the code window and paste the copied code
13. Press save down the bottom and find a folder called package_4 in that theres a file named class_5 open it
14. Now where it says <img width="352" height="38" alt="image" src="https://github.com/user-attachments/assets/70aef82b-a10f-4f62-bee5-44ec783c3eb8" /> under that { paste public var apClient:ApClient;
15. Now scroll down past the final public var which is public var var_239:Boolean = false; right under that add
      public function class_5()
      {
         this.apClient = new ApClient(this.var_106,this.var_112,this.var_113,this);
         super();
      }
16. Scroll down to public function method_196() : void and under __loc1__.var_109.prepareLevelData(false); add this.apClient = new ApClient(this.var_106,this.var_112,this.var_113,this);
17. Now scroll down to public function finishLevel() : void and under completedLevel = _loc1_.var_109.currentLevel; add _loc1_.apClient.sendCheck(completedLevel,0);
18. Scroll down to public function method_132() : void and under _loc1_ = this; add _loc1_.apClient.sendDeath()

