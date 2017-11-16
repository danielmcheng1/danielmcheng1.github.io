## Obstruct.io: A JavaScript Game 
Obstruct.io is a full-fledged JavaScript game complete with user editable levels. 

[Click here to play the game](https://dmcheng2010.github.io/obstructio.html).

Let me know if you beat all 16 levels! (Trust me...you'll hate me by the 16th level) For an immersive experience, be sure to use headphones, particularly on the later levels...

## Building Your Own Levels
You can easily modify Obstructio.io to build your own custom levels:
1. Clone this repository to your local machine 
2. In js/level_config.js, add a new variable with an ASCII-array of characters
3. Update the MASTER_DICT variable which configures the names and background music for each level 
4. Add the name of your level to the ALL_NAMES variable

Now, simply drag obstructio.html into a Chrome browser and begin playing!  

Detailed examples for each step below:
```javascript 
// Step 2: The one absolutely required character is the block character! (ASCII = 1)
var myNewLevel = [
	  "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!",
	  "!                         o    o         !         o           ",
	  "!            o      o     o    o     o  o  o  o                ",
	  "!   1        !      !     !    !     x  xxxxxxxx        !  oooo",
	  "!!!xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
];
```

```javascript
// Here is the mapping for each character:
var actorChars = {
	"1": Player,
	"2": Computer,
	"3": Computer,
	"p": Checkpoint,
	"o": Coin,
	"=": Lava, "|": Lava, "v": Lava,
	"B": Bomb, "b": BombSpray,
	"w": Water,
	"+": Ice, "-": Ice,
	"C": CartesianBomb, "c": CartesianBombSpray,
	"@": WaterPowerup, "#": CartesianBombPowerup
};
```

```javascript 
// Step 3: Update the config for your new level, 
// which maps from level name to [level variable, speed options, background music]
// you can load your own background mp3's to sound/background_music 
var MASTER_DICT = {
    "Easy": [easy, {}, "bach_gigue_english.mp3"],
    "Simple Abyss": [simpleAbyss, {}, "bach_gigue_english.mp3"],
	[...]
	"Insert Interesting Name": [myNewLevel, {}, "stravinsky_riteofspring.mp3"]
};
```
```javascript 
// Step 4: Add your level name to the end of this array 
// so that the engine knows to display your latest and greatest level 
var ALL_NAMES = [ 
        "Easy", "Simple Abyss", "Bungee Jump", 
        "Lava World", "Abyss Revisited", "Chase", "Gauntlet",
        "Bomb Away",  "To the Sky", "Weeping Angel",
        "Ice World", "Elevator", 
        "Bunny World", "Fool's Gold", "Into the Mines",
        "Hell", 
		"Insert Interesting Name"];
```
