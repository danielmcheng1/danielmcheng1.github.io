
/************************************************/
//map from source characters strings to constructor function for that actor 
var actorChars = {
	"1": Player,
	"2": Computer,
	"p": Checkpoint,
	"o": Coin,
	"=": Lava, "|": Lava, "v": Lava,
	"B": Bomb, "b": BombSpray,
	"w": Water,
	"+": Ice, "-": Ice,
	"C": CartesianBomb, "c": CartesianBombSpray,
	"@": WaterPowerup, "#": CartesianBombPowerup
};
var staticObstacles = {	"!": "lava", "x": "wall", "y": "wall", "z": "wall"};
var hiddenActors = {"y": "p", "z": "="}
var killingActors = ["lava", "bombSpray", "cartesianBombSpray", "computer"];
var playerPowerups = ["waterPowerup", "cartesianBombPowerup"];
var moveOnTopOfActors = ["ice"];


/*constructor that builds a level,
given the imput array of strings defining a level
*/
function Level(plan, speedMultipliers, levelId, livesRemaining, checkpoint) {
	this.width = plan[0].length;
	this.height = plan.length;
	this.grid = [];
	this.actors = [];
	this.gridHiddenActors = [];
	
	this.speedMultipliers = speedMultipliers;
	this.levelId = levelId; //0 based indexing
	this.levelNum = this.levelId; //in case we want to increment 1 above 0 based indexing
	
	this.coinsTotal = 0;
	this.coinsRemaining = 0;
	
	this.livesRemaining = livesRemaining;
	if (checkpoint) {			
		this.saveState(); //again, deep copy the state because the checkpoint actors are now the current actors;
		this.restoreState(checkpoint);
	}
	else {
		for(var y = 0; y < this.height; y++) {
			var line = plan[y];
			var gridLine = [];
			var gridLineHiddenActors = [];
			for(var x = 0; x < this.width; x++) {
				var ch = line[x];
				var fieldType, hiddenActor;
				var Actor = actorChars[ch];
				if (Actor) {	
					fieldType = null;
					hiddenActor = null;
					var speedMultiplier = speedMultipliers[ch];
					var actorObj = new Actor(new Vector(x, y), {"subtype": ch, "speedMultiplier": speedMultiplier, "origPos": new Vector(x, y)});
					this.actors.push(actorObj);
				}
				else {
					fieldType = staticObstacles[ch];
					hiddenActor = hiddenActors[ch];
				}
				gridLine.push(fieldType);
				gridLineHiddenActors.push(hiddenActor);
			}
			this.grid.push(gridLine);
			this.gridHiddenActors.push(gridLineHiddenActors);
		}
	};
	
	//find the player object and save as a property of this level
	this.player = this.findPlayer();
	
	this.coinsTotal = this.actors.filter(function(actor) {
		return actor.type == "coin";
	}).length;
	this.coinsRemaining = this.coinsTotal;
	
	//track the status of the game
	//finishDelay to allow lag before resetting level 
	this.status = this.finishDelay = null;
};

//check whether to reset the level 
Level.prototype.isFinished = function() {
	return this.status != null && this.finishDelay < 0;
};

//update statistics
Level.prototype.updateStatus = function() {
	var livesStatusNode = document.getElementById("liveStatus");
	livesStatusNode.innerText = this.livesRemaining + " lives";
	
	var levelStatus = document.getElementById("levelStatus");
	levelStatus.innerText = this.levelNum;
	
	var coinStatus = document.getElementById("coinStatus");
	coinStatus.innerText = this.coinsRemaining + " out of " + this.coinsTotal + " coins";
};

//other level utility functions
Level.prototype.removeActor = function(actor) {
	this.actors = this.actors.filter(function(other) {
		return other != actor;
	});
};
Level.prototype.findPlayer = function() {
	//abstract this out so that we can find player from a snapshot, which only contanis the actor object and not the level object 
	return findPlayerFromActors(this.actors);
};
function findPlayerFromActors(actors) {
	var players = actors.filter(function (actor) {
		return actor.type == "player";
	});
	if (players.length == 1) return players[0];
	else throw "Did not find exactly one player: " + players;
};

Level.prototype.revealHiddenActor = function(x, y) {
	 this.grid[y][x] = null;
	 var ch = this.gridHiddenActors[y][x];
	 var Actor = actorChars[ch];
	 var speedMultiplier = this.speedMultipliers[ch];
	 if (Actor) {
		 var actorObj = new Actor(new Vector(x, y), {"subtype": ch, "speedMultiplier": speedMultiplier, "origPos": new Vector(x, y)});
		 this.actors.push(actorObj);
	 };
 };
 
/************************************************/
//primitive motion functions
//first detect whether an object overlaps with any nonempty space 
Level.prototype.staticObstaclesAndCoordinatesAt = function(pos, size) {
	//round so that we get full range of background squares touched by the box 
	var padding = 0.3;
	var xStartPadding = Math.floor(pos.x + padding);
	var xEndPadding = Math.ceil(pos.x + size.x - padding);
	
	var xStart = Math.floor(pos.x);
	var xEnd = Math.ceil(pos.x + size.x);
	
	var yStart = Math.floor(pos.y);
	var yEnd = Math.ceil(pos.y + size.y);
	
	var returnObj = {obstacles: [], x: [], y: []};
	//TBD need to fix this
	//should hit wall if the player goes too far to the side
	if (xStart < 0 || xEnd > this.width || yStart < 0) {
		returnObj["obstacles"].push("wall");
		returnObj["x"].push(-1);
		returnObj["y"].push(-1);
	}
	//should die if player goes below the bottom 
	else if (yEnd > this.height)	{
		returnObj["obstacles"].push("lava");
		returnObj["x"].push(-1);
		returnObj["y"].push(-1);
	}
	//otherwise see what object we're next to 
	else {
		for(var y = yStart; y < yEnd; y++) {
			for(var x = xStart; x < xEnd; x++) {
				var fieldType = this.grid[y][x];
				if (fieldType) {
					//padding for lava
					if (fieldType == "lava" && (x < xStartPadding || x > xEndPadding)) continue;
					returnObj["obstacles"].push(fieldType);
					returnObj["x"].push(x);
					returnObj["y"].push(y);
				};
			};
		};
	};
	return returnObj;
};
Level.prototype.staticObstacleAt = function(pos, size) {
	var obstaclesAndCoordinates = this.staticObstaclesAndCoordinatesAt(pos, size);
	var obstacles = obstaclesAndCoordinates["obstacles"].sort();
	if (obstacles != []) return obstacles[0];
	else return null;
};

//look for actors that overlap the input actor arg
//TBD could cause issues that we're returning only the first actor
Level.prototype.actorAt = function(actor, options) {
	for (var i = 0; i < this.actors.length; i++) {
		var other = this.actors[i];
		if (options == "on top") {
			if (other != actor &&
				actor.pos.x + actor.size.x > other.pos.x + other.size.x * 0.25 &&
				actor.pos.x < other.pos.x + other.size.x * 0.75 &&
				(actor.pos.y + actor.size.y) - other.pos.y > -0.15 &&
				(actor.pos.y + actor.size.y) - other.pos.y < 0.15)
				return other;
		}
		else {
			//if right side of input actor beyond left side of the other actor--
			//and vice versa for the other side--
			//then they must overlap 
			if (other != actor &&
				actor.pos.x + actor.size.x > other.pos.x &&
				actor.pos.x < other.pos.x + other.size.x &&
				actor.pos.y + actor.size.y > other.pos.y &&
				actor.pos.y < other.pos.y + other.size.y)
				return other;
		};
	};
};


/************************************************/
//POSITION FUNCTIONS
function Vector(x, y) {
	this.x = x;
	this.y = y;
};
//add two vectors -- e.g. two positions
Vector.prototype.plus = function(other) {
	return new Vector(this.x + other.x, this.y + other.y)
};
//scale vector by a factor -- e.g. speed times time = distance
Vector.prototype.times = function(factor) {
	return new Vector(this.x * factor, this.y * factor);
};
//subtract two vectors 
Vector.prototype.minus = function(other) {
	return new Vector(this.x - other.x, this.y - other.y);
};



/************************************************/
//ACTORS
//position = starting pos of the top-left corner
function Player(pos, options) {
	//since player is 1.5 squares high, subtract 0.5 from vertical start position
	this.pos = pos.plus(new Vector(0, -0.5)); 
	//save the inputs so we can copy/snapshot these actors 
	this.options = options || {};
	
	this.size = new Vector(0.8, 1.5);
	this.regularSize = this.size;
	this.smallSize = new Vector(0.8, 0.5);
	this.direction = new Vector(1, 0); //start off facing to the right
	this.speed = new Vector(0, 0);
	
	//keep track of last time the player employed weapons;
	this.waterShootingLatency = 0;
	this.cartesianBombShootingLatency = 0;
	
	this.onMovingActor = this.options["onMovingActor"] || null;
	this.weapons = this.options["weapons"] || [];
	this.currentWeaponIndex = this.options["currentWeaponIndex"] || NaN;
	this.allowWeaponSwitch = this.options["allowWeaponSwitch"] || true;	
	//TBD update options obj with the most recent values for these so that they are passed through in the saveState function 
	//["onMovingActor", "weapons", "currentWeaponIndex", "allowWeaponSwitch"].forEach(function (property) {
	//	this.options[property] = this[property];//[property];
	//}, this); //Learning: this context must be specific for forEach prototype
};
Player.prototype.type = "player";

function Computer(pos, options) {
	this.pos = pos.plus(new Vector(0.05, 0)); //center the computer with 0.1 padding on either side so that it doesn't run into obstacles as easily
	this.options = options || {};
	
	this.size = new Vector(0.9, 0.5);
	this.speedMultiplier = options["speedMultiplier"] || 1;
	this.speed = new Vector(3, 3).times(this.speedMultiplier);
	
};
Computer.prototype.type = "computer";
	
function Coin(pos, options) {
	this.pos = pos.plus(new Vector(0.2, 0.1));
	this.options = options || {};

	this.origPos = this.options["origPos"];
	this.size = new Vector(0.6, 0.6);
	//start coins at random position to prevent syncing
	this.wobble = Math.random() * Math.PI * 2;
};
Coin.prototype.type = "coin";

function Lava(pos, options) {
	this.pos = pos;
	this.options = options || {};
	
	this.subtype = options["subtype"];
	this.speedMultiplier = options["speedMultiplier"] || 1;
	
	this.size = new Vector(1, 1);
	if (this.subtype == "=") {
		this.speed = new Vector(2, 0).times(this.speedMultiplier);
	} else if (this.subtype == "|") {
		this.speed = new Vector(0, 2).times(this.speedMultiplier);
	} else if (this.subtype == "v") {
		this.speed = new Vector(0, 3).times(this.speedMultiplier);
		this.origPos = options["origPos"];
	}
};
Lava.prototype.type = "lava";

function Ice(pos, options) {
	this.pos = pos;
	this.options = options || {};
	this.subtype = options["subtype"];
	this.speedMultiplier = options["speedMultiplier"] || 1;
	
	this.size = new Vector(1, 1);
	if (this.subtype == "-") {
		this.speed = new Vector(2, 0).times(this.speedMultiplier);
	} else if (this.subtype == "+") {
		this.speed = new Vector(0, 2).times(this.speedMultiplier);
	};
};
Ice.prototype.type = "ice";

function Bomb(pos, options) {
	this.pos = pos;
	this.options = options || {};
	this.spraySpeedMultiplier = options["spraySpeedMultiplier"] || 1;
	
	this.size = new Vector(1, 1);
	this.timeElapsed = 0;
	this.aboutToExplode = false;
	this.hasExploded = false;
};
Bomb.prototype.type = "bomb";

function BombSpray(pos, options) {
	this.pos = pos;
	this.options = options || {};
	this.speed = options["speed"];
	
	this.size = new Vector(1, 1);
};
BombSpray.prototype.type = "bombSpray";



function CartesianBomb(pos, options) {
	this.pos = pos;
	this.options = options || {};
	
	this.size = new Vector(1, 1);
	this.timeElapsed = 0;
	this.hasExploded = false;
	this.aboutToExplode = false;
};
CartesianBomb.prototype.type = "cartesianBomb";

function CartesianBombSpray(pos, options) {
	this.pos = pos;
	this.options = options || {};
	this.speed = options["speed"];
	
	this.size = new Vector(1, 1);
	this.timeElapsed = 0;
};
CartesianBombSpray.prototype.type = "cartesianBombSpray";



function Water(pos, options) {
	this.pos = pos;
	this.options = options || {};
	this.speed = options["speed"];
	
	this.size = new Vector(1, 0.5);
};
Water.prototype.type = "water";


function WaterPowerup(pos, options) {
	this.pos = pos;
	this.options = options || {};
	this.size = new Vector(1, 1);
};
WaterPowerup.prototype.type = "waterPowerup";
function CartesianBombPowerup(pos, options) {
	this.pos = pos;
	this.options = options || {};
	this.size = new Vector(1, 1);
};
CartesianBombPowerup.prototype.type = "cartesianBombPowerup";

function Checkpoint(pos, options) {
	this.pos = pos;
	this.options = options || {};
	this.size = new Vector(1, 1);
};
Checkpoint.prototype.type = "checkpoint";

/************************************************/
//ENCAPSULATED DRAWING/DISPLAY METHODS 
//TBD helper function to create an element and give it a class 
function elt(name, className) {
	var elt = document.createElement(name);
	if (className) elt.className = className;
	return elt;
};

//display level by giving:
	//a parent element--to append to
	//a level object--to append
//TBD how is this actually working? 
function DOMDisplay(parent, level) {
	//appendChild returns the appended element 
	this.wrap = parent.appendChild(elt("div", "game"));
	this.level = level;
	
	this.wrap.appendChild(this.drawBackground());
	//only drawing the static background once at the start 
	this.actorLayer = null;
	this.drawFrame();
};

//draw each row of the game grid as a table row 
//class names for each <td> table cell element maps to the CSS display for that element
var scale = 20;
DOMDisplay.prototype.drawBackground = function() {
	var table = elt("table", "background");
	table.style.width = this.level.width * scale + "px";
	this.level.grid.forEach(function(row) {
		var rowElt = table.appendChild(elt("tr"));
		rowElt.style.height = scale + "px";
		row.forEach(function(type) {
			rowElt.appendChild(elt("td", type));
		});
	});
	return table;
};

DOMDisplay.prototype.drawActors = function() {
	var wrap = elt("div");
	this.level.actors.forEach(function(actor) {
		//give the element more than one class 
		//actor class ==> absolute position 
		//type gives them color, etc. 
		var rect = wrap.appendChild(elt("div", "actor " + actor.type));
		if (actor.type == "player") {
			rect.style.width = (actor.size.x * scale) + "px";
			rect.style.left = (actor.pos.x * scale)  + "px";
			rect.style.height = actor.size.y * scale + "px";
		    rect.style.top = actor.pos.y * scale + "px";
		}
		else {
			rect.style.width = actor.size.x * scale + "px";
			rect.style.left = actor.pos.x * scale + "px";
			rect.style.height = actor.size.y * scale + "px";
		    rect.style.top = actor.pos.y * scale + "px";
		};
	});
	return wrap;
};

/*redrawing actors 
	few actors-->easier to just remove all actors and redraw 
	otherwise we would have to associate actors with each DOM and dynamically remove DOM elements as actors vanish
*/
DOMDisplay.prototype.drawFrame = function() {
	//TBD what is THIS here? 
	if (this.actorLayer) {
		this.wrap.removeChild(this.actorLayer);
	}
	this.actorLayer = this.wrap.appendChild(this.drawActors());
	//style player different colors based on current game status
	//status = {won, lost, neither} -- only change color class for 1st two
	this.wrap.className = "game " + (this.level.status || "");
	this.scrollPlayerIntoView();
};
DOMDisplay.prototype.scrollPlayerIntoView = function() {
	//use margin to determine when to scroll player into view 
	//this way we only scroll over once in awhile to prevent "jarring" from constantly centering
	var width = this.wrap.clientWidth;
	var height = this.wrap.clientHeight;
	var margin = width / 3;
	
	//the current viewport 
	var left = this.wrap.scrollLeft, right = left + width;
	var top = this.wrap.scrollTop, bottom = top + height; 
	
	//player's coordinates that we want to approximately center to 
	var player = this.level.player;
	//player's center is pos (top left corner) + 1/2 its height, multiplied by the game scale 
	var center = player.pos.plus(player.size.times(0.5)).times(scale);
	//TBD have to console.log this 
	if (center.x < left + margin)
		this.wrap.scrollLeft = center.x - margin;
	else if (center.x > right - margin)
		this.wrap.scrollLeft = center.x + margin - width;
	if (center.y < top + margin)
		this.wrap.scrollTop = center.y - margin;
	else if (center.y > bottom - margin)
		this.wrap.scrollTop = center.y + margin - height;
};

//need to clear level whenever we reset 
DOMDisplay.prototype.clear = function() {
	//TBD may have already been cleared from navigation 
	this.wrap.parentNode.removeChild(this.wrap);
};



/************************************************/
//MASTER ANIMATION FUNCTIONS 
//break down all movements into small enough chunks 

//TBD bombs depend on this--should use real time
var defaultMaxStep = 0.05; 
var maxStep = defaultMaxStep;
//step is the time interval
//keys is the object containing the player's input
Level.prototype.animate = function(step, keys) {
	//decrement delay time for special case where player has won or lost 
	if (this.status != null)
		this.finishDelay -= step;
	//animate each of the actors 
	while (step > 0) {
		var thisStep = Math.min(step, maxStep);
		this.actors.forEach(function(actor) {
			actor.act(thisStep, this, keys); //this = level object
		}, this);
		step -= thisStep;
	};
};

function runAnimation(frameFunc) {
	var lastTime = null;
	function frame(time) {
		var stop = false;
		if (lastTime != null) {
			//timestep in seconds
			var timeStep = Math.min(time - lastTime, 100) / 1000;
			stop = frameFunc(timeStep) === false;
		};
		lastTime = time;
		if (!stop)
			requestAnimationFrame(frame);
	};
	requestAnimationFrame(frame);
};

//Display object passed in -- e.g. DOMDisplay -- an encapsulated display/draw object
function runLevel(level, Display, andThen) {
	var display = new Display(document.body, level);
	document.body.onkeyup = function (e) {
		if (e.keyCode == 13) { //space bar
			runAnimation(function(step) {
				level.animate(step, arrows);
				display.drawFrame(step);
				level.updateStatus();
				if (level.isFinished()) {
					display.clear();
					if (andThen)
						andThen(level.status);
					return false;
				}
			});
		};
	};
};

//TBD how is status reset each time?--don't quite get these final steps
var startingLives = 3;
var startingCheckpoint = null;
var currentCheckpoint = null;
function runGame(plans, names, speedMultipliers, Display) {
	/*
	Learning: As James said, the DOM does not support removing an object directly. You have to go to its parent and remove it from there. 
	Javascript won't let an element commit suicide, but it does permit infanticide...
	*/
	function clearExistingGames() {
		//Display.clearDisplay();
		var existingGames = document.getElementsByClassName("game");
		for (var i = 0; i < existingGames.length; i++) {
			existingGames[i].remove();
		};
	};
	
	/*running a level*/
	function startLevel(n, numLivesLeft, checkpoint) {
		//Display.clear();
		clearExistingGames();
		var currentLevel = new Level(plans[n], speedMultipliers[n], n, numLivesLeft, checkpoint);
		if (n == 13 || n == 14) maxStep = 0.005; //TBD for more accurate movement on ice blocks
		runLevel(currentLevel, Display, function(status) {
			/*if (numLivesLeft == 0) startLevel(0, startingLives);*/
			if (status == "lost")
				startLevel(n, numLivesLeft - 1, currentCheckpoint);
			else if (n < plans.length - 1) {
				startLevel(n + 1, startingLives, startingCheckpoint);
			}
			else {
				playMusic("sound/applause.wav");
				window.alert("You have mastered all levels!");
			};
		});
	};
	
	/*let user select which level to jump to*/
	function createLevelListener(v, levelElt) {
		return function() {
			startLevel(v, startingLives, startingCheckpoint);
			
			var musicNode = document.getElementById("music");
			musicNode.volume = 0.6;
			musicNode.src = "sound/aladdin.mp3";
			musicNode.play();
			musicNode.addEventListener('ended', function() {
				var rand = Math.random();
				if (rand < 0.3) {
					musicNode.src = "sound/trump.mp3";
				} else if (rand < 0.6) {
					musicNode.src = "sound/mulan.mp3";
				} else {
					musicNode.src = "sound/chestnuts.mp3";
				};
				musicNode.play();
			});
		};
	};
	for(var i = 0; i < plans.length; i++) {
		var dropdownElt = document.getElementById("dropdown-menu");
		var levelElt = elt("a", "Level");
		dropdownElt.appendChild(levelElt);
		levelElt.addEventListener("click", createLevelListener(i, levelElt));
		levelElt.innerText = "Level " + i + ": " + names[i];
	};
};

	
/*
Learning: closure / callbacks for createLevelListener function
Source: https://stackoverflow.com/questions/750486/javascript-closure-inside-loops-simple-practical-example
var funcs = [];
function createfunc(i) {
    return function() { console.log("My value: " + i); };
}
for (var i = 0; i < 3; i++) {
    funcs[i] = createfunc(i);
}
for (var j = 0; j < 3; j++) {
    funcs[j]();                        // and now let's run each one to see
}
*/
/************************************************/
//KEY TRACKING 
var arrowCodes = {32: "space", 37: "left", 38: "up", 39: "right", 40: "down", 66: "bkey", 68: "dkey", 69: "ekey", 83: "skey", 87: "wkey"};
var arrows = trackKeys(arrowCodes);
function trackKeys(codes) {
	var pressed = Object.create(null);
	function handler(event) {
		//event.keyCode lets you know the code of the key that was pressed 
		//then see if this key code is in the arrowCodes that we're tracking 
		//and log it as true/false in our own "arrows" object which tracks what is being pressed 
		if (codes.hasOwnProperty(event.keyCode)) {
			//boolean if the key is being held down 
			var keyPressedDown = event.type == "keydown";
			var keyCodeName = codes[event.keyCode];
			pressed[keyCodeName] = keyPressedDown;
			
			if (keyPressedDown) {
				if (pressed[keyCodeName + " timedelta"]) {
					//time in milliseconds
					pressed[keyCodeName + " timedelta"] = NaN; //event.timeStamp - pressed[keyCodeName + " timedelta"];
				} else {
					pressed[keyCodeName + " timedelta"] = 1;
				};
			} 
			else {
				pressed[keyCodeName + " timedelta"] = NaN;
			};
			//prevent normal actions 
			event.preventDefault();
			
		}
		/*
		else {
			for (var keyCodeName in pressed) {
				if (keyCodeName.endsWith("first")) pressed[keyCodeName] = false;
			}
		};*/
	};
	addEventListener("keydown", handler);
	addEventListener("keyup", handler);
	return pressed;
};

//INDIVIDUAL ACTOR ANIMATION FUNCTIONS

Lava.prototype.act = function(step, level) {
	var newPos = this.pos.plus(this.speed.times(step));
	//check if new position will overlap an obstacle 
	if (!level.staticObstacleAt(newPos, this.size))
		//okay to move the actor 
		this.pos = newPos;
	else if (this.origPos)
		//jump back to the top for lava that falls from the ceiling 
		this.pos = this.origPos;
	else 
		//reverse direction from the obstacle 
		this.speed = this.speed.times(-1);
};

//coins wobble about axis
var wobbleSpeed = 8, wobbleDist = 0.07;
Coin.prototype.act = function(step) {
	this.wobble += step * wobbleSpeed;
	var wobblePos = Math.sin(this.wobble) * wobbleDist;
	this.pos = this.origPos.plus(new Vector(0, wobblePos));
};

WaterPowerup.prototype.act = function(step) {
};
CartesianBombPowerup.prototype.act = function(step) {
};
Checkpoint.prototype.act = function(step) {
};

Computer.prototype.act = function(step, level) {
	var player = level.findPlayer();
	var targetPos = new Vector(player.pos.x, player.pos.y);
	var xDist = targetPos.x - this.pos.x;
	var yDist = targetPos.y - this.pos.y;
	//flip direction based on where the player is
	if (Math.sign(this.speed.x) != Math.sign(xDist)) this.speed.x *= -1;
	if (Math.sign(this.speed.y) != Math.sign(yDist)) this.speed.y *= -1;
	
	var origNewPos = this.pos.plus(this.speed.times(step));
	var testNewPos = new Vector(origNewPos.x, origNewPos.y);
	
	//only move either horizontally or vertically so that the computer "zig zags" towards the player
	//try moving to the new position in either direction, recursing until we get stacuk 
	//TBD could make this a recursive call instead of convoluted if-else logic 
	//TBD could improve this with an AI that finds the shortest path given obstacles 
	if (Math.abs(xDist) >= Math.abs(yDist)) {
		testNewPos.y = this.pos.y;
	}
	else {
		testNewPos.x = this.pos.x;
	};	
	var obstacle = level.staticObstacleAt(new Vector(testNewPos.x, testNewPos.y), this.size); 
	if (obstacle) {
		testNewPos = new Vector(origNewPos.x, origNewPos.y);
		if (Math.abs(xDist) < Math.abs(yDist)) {
			 testNewPos.y = this.pos.y;
		}
		else {
			testNewPos.x = this.pos.x;
		};	
		obstacle = level.staticObstacleAt(new Vector(testNewPos.x, testNewPos.y), this.size); 
		if (obstacle) {
			testNewPos = this.pos;
		};
	};
	this.pos = testNewPos;
};

Ice.prototype.act = function(step, level) {
	var newPos = this.pos.plus(this.speed.times(step));
	//check if new position will overlap an obstacle 
	if (!level.staticObstacleAt(newPos, this.size))
		//okay to move the actor 
		this.pos = newPos;
	else if (this.origPos)
		//jump back to the top for lava that falls from the ceiling 
		this.pos = this.origPos;
	else 
		//reverse direction from the obstacle 
		this.speed = this.speed.times(-1);
};



var bombSprayThreshold = 25;
var avgBombSpraySpeed = 2;
Bomb.prototype.act = function(step, level) {
	if (!this.hasExploded) {
		var rand = Math.random();
		//try exploding 
		if (rand < 0.1) {
			var currentBombSprayActors = level.actors.filter(function(other) {
				return other.type == "bombSpray";
			});
			//explode preferentially if little bomb spray is on the board right now
			if (currentBombSprayActors.length < bombSprayThreshold) {
				playMusic("sound/bomb.mp3", 0.05);
				
				//generate bomb spray expanding out in a circle 
				var Actor = actorChars["b"];
				//some randomnness in speed around the average expected value 
				thisBombSpraySpeed = (Math.random() - 0.5) + avgBombSpraySpeed;
				//scale based on difficulty 
				thisBombSpraySpeed = thisBombSpraySpeed * this.spraySpeedMultiplier;
				for(var i = 0; i <= 2 * Math.PI; i+= Math.PI / 6) {
					level.actors.push(new Actor(this.pos, {"subtype": "b", "speed": new Vector(Math.cos(i) * thisBombSpraySpeed, Math.sin(i) * thisBombSpraySpeed)}));
				};
				this.hasExploded = true;
				//remove the starting bomb
				level.removeActor(this);
			};
		}
		//otherwise animate a ticking bomb 
		else {
			var timeElapsedMod = this.timeElapsed % 75;
			if (timeElapsedMod > 55)
				this.aboutToExplode = true;
			else
				this.aboutToExplode = false;
		};
	};
	this.timeElapsed++;
};


BombSpray.prototype.act = function(step, level) {
	var newPos = this.pos.plus(this.speed.times(step));
	//check if new position will overlap an obstacle 
	if (!level.staticObstacleAt(newPos, this.size)) {
		//move the bomb but slow down the next step 
		this.pos = newPos;
		if (this.speed.x != 0)
			this.speed.x = this.speed.x * 0.999999;
		if (this.speed.y != 0)
			this.speed.y = this.speed.y * 0.999999;
	}
	else {
		//remove this bomb spray 
		level.removeActor(this);
	};
};

CartesianBomb.prototype.act = function(step, level) {
	if (this.timeElapsed > 100) {	
		playMusic("sound/bomb.mp3", 0.05);
		
		//generate bomb spray expanding out in a circle 
		var Actor = actorChars["c"];
		thisBombSpraySpeed = 2;
		for(var i = 0; i <= Math.PI; i+= Math.PI) {
			level.actors.push(new Actor(this.pos, {"subtype": "c", "speed": new Vector(Math.cos(i) * thisBombSpraySpeed, Math.sin(i) * thisBombSpraySpeed)}));
		};
		this.hasExploded = true;
		//remove the starting bomb
		level.removeActor(this);
	}
	else if (this.timeElapsed > 50) {
		this.aboutToExplode = true;
	};
	this.timeElapsed++;
};

CartesianBombSpray.prototype.act = function(step, level) {
	var newPos = this.pos.plus(this.speed.times(step));	
	var obstaclesAndCoordinates = level.staticObstaclesAndCoordinatesAt(newPos, this.size);
	var obstacles = obstaclesAndCoordinates["obstacles"];
	if (obstacles.indexOf("wall") >= 0) {
		for (var i = 0; i < obstacles.length; i++) {
			//check if new position will overlap an obstacle 
			if (obstacles[i] == "wall") {
				var obstacleX = obstaclesAndCoordinates["x"][i];
				var obstacleY = obstaclesAndCoordinates["y"][i];
				if (obstacleX == Math.round(this.pos.x) && obstacleY == Math.round(this.pos.y)) {
					//TBD basically need to pass in padding for everyone 
					//TBD need to abstract this out into general actors fight function
					if (obstacleX != -1 && obstacleY != -1) {
						level.revealHiddenActor(obstacleX, obstacleY);
						level.removeActor(this);
						return;
					};
				}
			};
		};
	}
	//move the bomb but slow down the next step 
	this.pos = newPos;
	if (this.speed.x != 0)
		this.speed.x = this.speed.x * 0.999999; //TBD slowdown depends on powerups
	if (this.speed.y != 0)
		this.speed.y = this.speed.y * 0.999999;
	
	if (this.timeElapsed > 50)
		level.removeActor(this);
	else 
		this.timeElapsed++;
};

Water.prototype.act = function(step, level) {
	var newPos = this.pos.plus(this.speed.times(step));
	if (level.staticObstacleAt(newPos, this.size)) {
		//get rid of the water if we hit a wall or static lava 
		level.removeActor(this);
	}
	else {
		var otherActor = level.actorAt(this);
		if (otherActor)
			level.actorsFight(this, otherActor);
		//TBD if water hasn't been removed 
		if(this)
			this.pos = newPos;
	};
};

Player.prototype.act = function(step, level, keys) {
	var onTopOfActor = level.actorAt(this, "on top");
	if (onTopOfActor && moveOnTopOfActors.indexOf(onTopOfActor.type) >= 0) {
		this.onMovingActor = onTopOfActor;
	}
	else {
		this.onMovingActor = null;
	};
	
	//move left, right, and up 
	this.moveY(step, level, keys);
	this.moveX(step, level, keys);
		
	//use weapons
	this.useWeapons(step, level, keys);

	//check for overlapping actors after moving 
	var otherActor = level.actorAt(this);
	if (otherActor)
		level.actorsFight(this, otherActor);
	
	//if player lost, animate accordingly 
	//won status animation is in the playerTouched function 
	if (level.status == "lost") {
		//player shrinks in size 
		this.pos.y += step;
		this.size.y -= step;
	};
};
//split player into two axes to simulate hitting a wall vs. gravity
var playerXSpeed = 7, gravity = 30, largeJumpSpeed = 17, smallJumpSpeed = 5;
Player.prototype.moveX = function(step, level, keys) {
	//update speed based on what user pressed 
	this.speed.x = 0;
	if (keys.left) this.speed.x -= playerXSpeed;
	if (keys.right) this.speed.x += playerXSpeed;
	
	if (this.onMovingActor) this.speed.x += this.onMovingActor.speed.x;
	
	//check if new pos will overlap with obstacle 
	var motion = new Vector(this.speed.x * step, 0);
	var newPos = this.pos.plus(motion);
	var obstacle = level.staticObstacleAt(newPos, this.size);
	if (obstacle) 
		level.actorsFight(this, obstacle);
	else 
		this.pos = newPos;
};
/*
always accelerate player down due to gravity
if already stationary, then player stays as is as speed = 0 
	but if they pressed up, then jump (this.speed.y = -jumpSpeed)
	and if they're falling and hit an obstacle, then bounce (this.speed.y = -jumpSpeed)
*/

Player.prototype.moveY = function(step, level, keys) {
	if (this.onMovingActor) {
		this.speed.y = this.onMovingActor.speed.y;
		if (keys.up) {
			this.speed.y = this.speed.y - largeJumpSpeed;
		}
		var motion = new Vector(0, this.speed.y * step);
		var newPos = this.pos.plus(motion);
	}
	else {
		this.speed.y += step * gravity;
		var motion = new Vector(0, this.speed.y * step);
		var newPos = this.pos.plus(motion);
	};
	var staticObstacle = level.staticObstacleAt(newPos, this.size);
	//movement 
	if (staticObstacle) {
		level.actorsFight(this, staticObstacle);
		//jumping -- default is to make the largest possible jump
		//only accelerate upwards if 
		if (keys.up && this.speed.y > 0) {
			this.speed.y = -largeJumpSpeed;
		}
		//hit an obstacle 
		else {
			this.speed.y = 0;
		};
	}
	else {
		//if player releases the up key and the player is going faster than the smaller jump speed, cancel the jump down to the smaller jump 
		if (!keys.up && this.speed.y < (-smallJumpSpeed)) {
			//this.speed.y = -smallJumpSpeed;
			this.speed.y += 1.5;
		}
		this.pos = newPos;
	};
	
	//ducking
	if (keys.dkey && this.size != this.smallSize) {
	//if (keys.dkey) {
		//this.smallSize = true;
		this.size = this.smallSize;
	};
	if (keys.ekey && this.size != this.regularSize) {
	//if (keys.ekey) {
		//this.smallSize = false;
		var diff = this.smallSize.minus(this.regularSize);
		this.pos = this.pos.plus(diff);
		this.size = this.regularSize;
	};
};

Player.prototype.useWeapons = function(step, level, keys) {
	if (this.weapons.length > 0) {
		//TBD trying to track only the first keypress down 
		if(keys.skey) {
			if (this.allowWeaponSwitch) {
				if (this.currentWeaponIndex >= this.weapons.length - 1) 
					this.currentWeaponIndex = 0;
				else 
					this.currentWeaponIndex++;
				this.allowWeaponSwitch = false;
			};
		}
		else {
			this.allowWeaponSwitch = true;
		};
		
		//now use the weapon
		var currentWeapon = this.weapons[this.currentWeaponIndex];
		if (currentWeapon == "waterPowerup") 
			this.shootWater(step, level, keys);
		else if (currentWeapon == "cartesianBombPowerup")
			this.placeCartesianBomb(step, level, keys);
	};
};

Player.prototype.placeCartesianBomb = function(step, level, keys) {
	if (keys.space && this.cartesianBombShootingLatency == 0) {
		var Actor = actorChars["C"];
		var bottomOfActor = new Vector(this.pos.x, this.pos.y + this.size.y - 1);
		level.actors.push(new Actor(bottomOfActor, {"subtype": "C"}));
		this.cartesianBombShootingLatency = 25;
	}
	else {
		this.cartesianBombShootingLatency = Math.max(--this.cartesianBombShootingLatency, 0);
	};
};
Player.prototype.shootWater = function(step, level, keys) {
	if (keys.space && this.waterShootingLatency == 0) {
		playMusic("sound/waterballoon.wav", 0.4);
		var waterSpeed, waterPos;
		var defaultWaterSpeedX = 5;
		if (this.speed.x < 0) {
			waterSpeed = new Vector(this.speed.x - defaultWaterSpeedX, 0);
			waterPos = this.pos;
		}
		else if (this.speed.x > 0) {
			waterSpeed = new Vector(this.speed.x + defaultWaterSpeedX, 0);
			waterPos = this.pos;
		}
		else {
			if (this.direction.x > 0) waterSpeed = new Vector(defaultWaterSpeedX, 0);
			else waterSpeed = new Vector(-defaultWaterSpeedX, 0);
			//waterSpeed = new Vector(0, Math.min(this.speed.y, -5));
			waterPos = this.pos;
		};
		var Actor = actorChars["w"];
		level.actors.push(new Actor(waterPos, {"speed": waterSpeed, "subtype": "w"}));
		this.waterShootingLatency = 25;
	}
	else {
		this.waterShootingLatency = Math.max(--this.waterShootingLatency, 0);
	};
};


Level.prototype.actorsFight = function(attacker, defender) {
	//TBD FIX THIS OVERRIDE 
	var defenderType, defenderObj;
	if (defender.type == null) {
		defenderType = defender;
		defenderObj = null;
	}
	else {
		defenderType = defender.type;
		defenderObj = defender;
	};
	
	if (attacker.type == "player") {
		if (killingActors.indexOf(defenderType) >= 0 && this.status == null) {
			this.status = "lost";
			this.finishDelay = 2;
			playMusic("sound/burning.mp3", 0.2);
		}
		else if (defenderType == "coin") {
			//remove this coin from the list of actors 
			playMusic("sound/smb_coin.wav", 0.2);
			this.removeActor(defenderObj);
			this.coinsRemaining--;
			
			//see if any coins are remaining
			if (this.coinsRemaining == 0) {
				this.status = "won";
				this.finishDelay = 1;
			};
		}
		else if (playerPowerups.indexOf(defenderType) >= 0) {
			playMusic("sound/smb_1up.wav", 0.45);
			this.removeActor(defenderObj);
			attacker.weapons.push(defenderType);
			attacker.currentWeaponIndex = attacker.weapons.length - 1;
		}
		else if (defenderType == "checkpoint") {
			this.removeActor(defender);
			this.saveState();
		};
	}
	else if (attacker.type == "water") {
		if (defenderType == "lava" && defenderObj) {
			this.removeActor(defenderObj);
			this.removeActor(attacker);
		};
	};
};


/*************************/
//Saving and restoring snapshots
Level.prototype.saveState = function () {
	currentCheckpoint = {};
	
	currentCheckpoint["grid"] = [];
	currentCheckpoint["gridHiddenActors"] = []
	for(var y = 0; y < this.height; y++) {
		var line = this.grid[y];
		var gridLine = [];
		var gridLineHiddenActors = []
		for(var x = 0; x < this.width; x++) {
			gridLine.push(this.grid[y][x]);
			gridLineHiddenActors.push(this.gridHiddenActors[y][x]);
		};
		currentCheckpoint["grid"].push(gridLine);
		currentCheckpoint["gridHiddenActors"].push(gridLineHiddenActors);
	};
	
	currentCheckpoint["actors"] = [];
	this.actors.forEach(function (actor) {
		var Actor = actorChars[actor.options["subtype"]];			
		var actorObj = new Actor(new Vector(actor.pos.x, actor.pos.y), actor.options);
		currentCheckpoint["actors"].push(actorObj);
	}, this); //Learning: Pass in the this object for forEach because this references the array otherwise
	
	var checkpointPlayer = findPlayerFromActors(currentCheckpoint["actors"]);
	var levelPlayer = this.findPlayer(); //explicitly search the actors in case the level attribute ".player" has not be initialized yet
	checkpointPlayer.size = new Vector(levelPlayer.size.x, levelPlayer.size.y);
};

Level.prototype.restoreState = function(savedState) {
	this.grid = savedState["grid"];
	this.gridHiddenActors = savedState["gridHiddenActors"];
	this.actors = savedState["actors"];
	
	var checkpointPlayer = findPlayerFromActors(savedState["actors"]);
	var levelPlayer = this.findPlayer();
	//TBD how to deal with size
	levelPlayer.size = new Vector(checkpointPlayer.size.x, checkpointPlayer.size.y);
}



/**********************************/
//CANVAS DISPLAY
/********************/
var bombAboutToExplodeSprite = document.createElement("img");
var bombSpraySprite = document.createElement("img");
var bombSprite = document.createElement("img");

var cartesianBombAboutToExplodeSprite = document.createElement("img");
var cartesianBombPowerupSprite = document.createElement("img");
var cartesianBombSpraySprite = document.createElement("img");
var cartesianBombSprite = document.createElement("img");

var checkpointSprite = document.createElement("img");
var coinSprite = document.createElement("img");
var computerSprite = document.createElement("img");

var iceSprite = document.createElement("img");
var lavaSprite = document.createElement("img");

var playerCartesianBombPowerupSprite = document.createElement("img");
var playerLostSprite = document.createElement("img");
var playerSprite0 = document.createElement("img");
var playerWaterPowerupSprite = document.createElement("img");
var playerWonSprite = document.createElement("img");

var wallSprite = document.createElement("img");
var waterPowerupSprite = document.createElement("img");
var waterSprite = document.createElement("img");
var playerXOverlap = 0; //adjustment because our images are > 20 pixels

/********************/
bombAboutToExplodeSprite.src = "img/bombAboutToExplode.png";
bombSpraySprite.src = "img/bombSpray.png";
bombSprite.src = "img/bomb.png";

cartesianBombAboutToExplodeSprite.src = "img/cartesianBombAboutToExplode.png";
cartesianBombPowerupSprite.src = "img/cartesianBombPowerup.png";
cartesianBombSpraySprite.src = "img/cartesianBombSpray.png";
cartesianBombSprite.src = "img/cartesianBomb.png";

checkpointSprite.src = "img/checkpoint.png";
coinSprite.src = "img/coin.png";
computerSprite.src = "img/computer.png";

iceSprite.src = "img/ice.png";
lavaSprite.src = "img/lava.png";

playerCartesianBombPowerupSprite.src = "img/playerCartesianBombPowerup.png";
playerLostSprite.src = "img/playerLost.png";
playerSprite0.src = "img/player0.png";
playerWaterPowerupSprite.src = "img/playerWaterPowerup.png";
playerWonSprite.src = "img/playerWon.png";

wallSprite.src = "img/wall.png";
waterPowerupSprite.src = "img/waterPowerup.png";
waterSprite.src = "img/water.png";

/***************************/
var sprites = {
		"player": [playerSprite0],
		"playerwon": playerWonSprite,
		"playerlost": playerLostSprite, 
		"playercartesianBombPowerup": playerCartesianBombPowerupSprite,
		"playerwaterPowerup": playerWaterPowerupSprite,
		"computer": computerSprite, 
		
		"wall": wallSprite, 
		"lava": lavaSprite, 
		"coin": coinSprite,
		"water": waterSprite,
		"ice": iceSprite,
		
		"bomb": bombSprite,
		"bombAboutToExplode": bombAboutToExplodeSprite,
		"bombSpray": bombSpraySprite,
		"cartesianBomb": cartesianBombSprite,
		"cartesianBombSpray": cartesianBombSpraySprite,
		"cartesianBombAboutToExplode": cartesianBombAboutToExplodeSprite,
		
		"checkpoint": checkpointSprite,
		"cartesianBombPowerup": cartesianBombPowerupSprite,
		"waterPowerup": waterPowerupSprite
		}

function CanvasDisplay(parent, level) {
	this.canvas = document.createElement("canvas");
	this.canvas.width = Math.min(600, level.width * scale);
	this.canvas.height = Math.min(450, level.height * scale);
	parent.appendChild(this.canvas);
	this.cx = this.canvas.getContext("2d");
	
	this.level = level;
	this.animationTime = 0;
	this.flipPlayer = false;
	
	this.viewport = {
		left: 0,
		top: 0,
		width: this.canvas.width / scale,
		height: this.canvas.height / scale
	};
	
	this.drawFrame(0);
};

//redrawing requires clearing everything each time
CanvasDisplay.prototype.clear = function() {
	this.canvas.parentNode.removeChild(this.canvas);
};

//now we redraw the background each time instead of drawing it once and scrolling the DOM to "move" the background
CanvasDisplay.prototype.drawFrame = function(step) {
	this.animationTime += step;
	this.updateViewport();
	this.clearDisplay();
	this.drawBackground();
	this.drawActors();
};

//center to where the player is
CanvasDisplay.prototype.updateViewport = function() {
	var view = this.viewport;
	var margin = view.width / 3;
	var player = this.level.player;
	var center = player.pos.plus(player.size.times(0.5));
	
	if (center.x < view.left + margin) {
		//reposition so that the left side is now (margin) away from the center of the player 
		view.left = Math.max(center.x - margin, 0);
	}
	else if (center.x > view.left + view.width - margin) {
		view.left = Math.min(center.x + margin - view.width, this.level.width - view.width);
	};
	
	if (center.y < view.top + margin) {
		view.top = Math.max(center.y - margin, 0);
	}
	else if (center.y > view.top + view.height - margin) {
		view.top = Math.min(center.y + margin - view.height, this.level.height - view.height);
	};
};

//TBD what does this refer to here?
CanvasDisplay.prototype.clearDisplay = function() {
	if (this.level.status == "won") {
		//this.cx.fillStyle = "rgb(68, 1919, 255)";
	}
	else if (this.level.status == "lost") {
		//this.cx.fillStyle = "rgb(44, 136, 214)";
	}
	else {
		//this.cx.fillStyle = "rgb(52, 166, 251)";
		this.cx.fillStyle = "#add8e6";
	};
	this.cx.fillRect(0, 0, this.canvas.width, this.canvas.height);
};

CanvasDisplay.prototype.drawBackground = function() {
	var view = this.viewport;
	var xStart = Math.floor(view.left);
	var xEnd = Math.ceil(view.left + view.width);
	var yStart = Math.floor(view.top);
	var yEnd = Math.ceil(view.top + view.height);
	
	for (var y = yStart; y < yEnd; y++) {
		for (var x = xStart; x < xEnd; x++) {
			var tile = this.level.grid[y][x];
			//only draw non empty tiles 
			if (tile == null) continue;
			var screenX = (x - view.left) * scale;
			var screenY = (y - view.top) * scale;
			//other sprites contans wall:lava:coin
			//so wall is at pixel 0, lava is offset at pixel 20 = scale 
			//var tileX = tile == "lava" ? scale : 0;
			
			//2nd to 5th arguments are the dimensions of the fragment to include 
			//6th to 9th arguments give the rectangle on the canvas to copy this fragment onto 
			var factor;
			factor = 1;
			this.cx.drawImage(sprites[tile], 
							0, 0, scale, scale,
							screenX, screenY, factor * scale, factor * scale);
		};
	};
};

CanvasDisplay.prototype.drawActors = function() {
	this.level.actors.forEach(function(actor) {
		var width = actor.size.x * scale;
		var height = actor.size.y * scale;
		//(0, 0) on canvas = top left of the viewport -- not of the level itself 
		//could also have used translate instead 
		var x = (actor.pos.x - this.viewport.left)  * scale;
		var y = (actor.pos.y - this.viewport.top) * scale;
		if (actor.type == "player") {
			this.drawPlayer(x, y, width, height);
		}
		else {
			//var tileX = (actor.type == "coin" ? 2 : 1) * scale;
			//TBD scale this and the powerups resizing 
			if (actor.type) {
				if (actor.type == "bombSpray" || actor.type == "cartesianBombSpray") 
					factor = 0.5;
				else if (actor.type == "bombSprayPowerup" || actor.type == "cartesianBombSprayPowerup") 
					factor = 0.5;
				else
					factor = 1;
				if ((actor.type == "cartesianBomb" || actor.type == "bomb") && actor.aboutToExplode)
					actor.type = actor.type + "AboutToExplode";
				this.cx.drawImage(sprites[actor.type],
								0, 0, width, height,
								x, y, width * factor, height * factor);
			}
		};
	}, this);
};


CanvasDisplay.prototype.drawPlayer = function(x, y, width, height) {
	var player = this.level.player;
	width += playerXOverlap;
	if (player.speed.x != 0)
		this.flipPlayer = player.speed.x < 0;
	
	//set default sprite
	var whichSprite = sprites["player"][0];
	var numSprites = sprites["player"].length;
	//now calculate sprite based on current game conditions
	if (this.level.status == "won" || this.level.status == "lost") {
		whichSprite = sprites["player" + this.level.status];
	}
	else if (player.weapons.length != 0) {
		var currentWeapon = player.weapons[player.currentWeaponIndex];
		whichSprite = sprites["player" + currentWeapon];
	}		
	else {
		if (player.speed.y != 0)
			//sprite = 9; //jumping sprite 
			whichSprite = sprites["player"][0];
		else if (player.speed.x != 0)
			//animation time is in seconds 
			//switch / show frames 12 times per second 
			//mod 8 to pick one of the first 8 walking images 
			//sprite = Math.floor(this.animationTime * 12) % 8;
			whichSprite = sprites["player"][Math.floor(this.animationTime * 12) % numSprites];
	};
	this.cx.save();
	
	if (this.flipPlayer) {
		flipHorizontally(this.cx, x + width / 2);
		//only flip the player's internal direction if we have changed direction -- 
		//because flip horizontally is called every tiem to flip just the player relative to the rest of the game 
		player.direction = new Vector(-1, 0);
		//	player.direction = player.direction.times(-1);	
	}
	else {
		player.direction = new Vector(1, 0);
	};
	
	/*
	if (player.smallSize) {
		this.cx.drawImage(whichSprite, 
						0, 0, width, height,
						x, y + 2/3 * height, width, 1/3 * height);
	}	*/
	this.cx.drawImage(whichSprite, 
						0, 0, width, height,
						x, y, width, height);
	this.cx.restore();

};

function flipHorizontally(context, around) {
	context.translate(around, 0);
	context.scale(-1, 1);
	context.translate(-around, 0);
};


/************************************************/
//AUDIO 

//TBD organize sounds
function playMusic(path, volume, seconds) {
	var audio = document.createElement("audio");
	audio.src = path;
	if (volume) audio.volume = Math.min(volume, 1);
	audio.play();
	if (seconds) {
		audio.addEventListener("canplaythrough", function() {
			setTimeout(function(){
				audio.pause();
				//alert("Audio Stop Successfully");
			},
			seconds * 1000);
		}, false); 
	};
	return audio;
};