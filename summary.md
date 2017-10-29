## Daniel M. Cheng
### Completed Projects 
1. [Automated Drone Photo Service](#automated-drone-photo-service)
2. [Scrabble AI (Greedy Search Algorithm)](#scrabble-ai)
3. [Obstruct.io: A Javascript Game](#obstructio-a-javascript-game)
4. [ETL Utility Library Suite](#library-of-sas-utilities-for-etls-and-qc)

### In Progress 
* [Abstract Syntax Tree](#abstract-syntax-tree)
* [Virtual AI Therapist](#virtual-ai-therapist)

## Automated Drone Photo Service 
[Numerate.io](https://goo.gl/3yVGLa) is a completely automated drone photo service to count cars (to save time circling parking lots) and people (to save time waiting in line).
Users of this service can request photos in two ways:
1. Send a text message to trigger the drone to start its mission 
2. Schedule the drone to fly every 10 minutes over the same area each day 

_Click below to view the drone service in action_ 

<a href="https://goo.gl/4taYny">
<img src="static/img/play_button2.jpg" width = 40% alt="Drone Overview Video"/>     
</a>

This service has two parts: 
1. Custom Android app that automates mission control via DJI's SDK, before compressing and pushing the photos to the backend
2. AWS-hosted backend that stitches and cleans photos using OpenCV before displaying on the Flask website in realtime

**[Click here to visit numerate.io](https://goo.gl/3yVGLa)** to see photos collected by previous drone missions.

### Technical Challenges: Multithreading and Synchronization 
A significant challenge was in troubleshooting why realtime downloads of images would get corrupted after about 5 photos. After digging deep into the code, I found that triggering a download immediately after photo capture quickly saturated the limited radio bandwidth and caused dropped packets that corrupted the jepgs.

The naive solution here is to add photos to a queue and download them in sequence. However, because the download method is asynchronous, it instantly returns; hence sequentially processing the queue leads to the same bandwidth saturating behavior as before.

To solve this, I first maintained a queue of photos. I then implemented a lock to prevent a second download from running as long as one photo is downloading. While this slowed down the download process, this solution guaranteed reliability, a far more valuable feature for this drone service. 

**[Read through my drone writeup](https://goo.gl/rLVcGm)** to learn more about these technical challenges, how I defined the MVP, broke down the tasks, estimated the time required for each, and adapted as that plan changed greatly during the course of this project.

### Architecture for Drone Service
<img src="static/img/architecture_drone.png" width="80%" alt="Diagram of drone architecture"/>

[Click here to view the code base.](https://github.com/danielmcheng1/drone)

## Scrabble AI
I built a complete Scrabble application where players can play against the computer. The two main features are:
1. AI running greedy backtracking algorithm to search for the optimal tile placement 
2. Complete game logic for validating and scoring human moves

The entire move algorithm was built from scratch based on the data structures explained in Appel & Jacobson's research paper. I optimized the search for valid Scrabble placements through three techniques:
1. __Space-Efficient Data Structure__: Load the lexicon into a DAWG (directed acyclic word graph), essentially a trie with all common suffixes merged
2. __Precompute Constraints__: Precompute all hook spots and crossword letters to reduce branching factor 
3. __Backtracking__: Prune search by terminating as early in the prefix as possible 

I further sped up search performance by converting Appel & Jacobson's DAWG structure into the GADDAG proposed by Steven A. Gordon. Since placed tiles must "hook" onto existing tiles, the GADDAG stores every reversed prefix of every word, so that the recursive search algorithm can build deterministically from each hook spot. Hence using a GADDAG applies the classic tradeoff of space for time: the GADDAG is nearly five times larger than the DAWG, but generates moves twice as fast.

[Play my Scrabble game here on Chrome.](https://goo.gl/Y2wisi)
 
<a href="https://goo.gl/Y2wisi">
<img src="static/img/sample_scrabble.gif" alt="Scrabble gif"/>     
</a>

### Architecture for Scrabble
<img src="static/img/architecture_scrabble.png" alt="Diagram of Scrabble architecture"/>

[Click here to view the code base.](https://github.com/danielmcheng1/scrabble)

## Obstruct.io: A Javascript Game 
Obstruct.io is a full-fledged game complete with user editable levels. This project allowed me to gain experience in building a fully functional product from start to finish.

I started off with a simple prototype where the objective was to jump over obstacles and avoid lava. I then added advanced features like shooting water to destroy lava blocks, destroying obstacles using bombs, and jumping on floating ice blocks to pass over lava. I also built simple killer bots that honed in to attack wherever the player was.

<a href="https://danielmcheng1.github.io/obstructio/obstructio.html">
<img src="static/img/sample_obstructio2.gif" alt="obstructio gif 2"/>
</a>


I strove towards clean code by:
1. __Scoping__: I scoped down variables to maintain readable code and to prevent unintended side effects. This was particularly important in transmitting information between levels--a key requirement of this game.
2. __Serialization__: I converted an object state into byte stream for transmission. This allows restarting at the last checkpoint.
3. __Asynchronous Callbacks__: Callbacks enable interactivity in the game e.g. "When I click on this button, run this animation" 

[Click here to see if you can beat all 16 levels in this very fun game.](https://danielmcheng1.github.io/obstructio/obstructio.html) Be sure to use your headphones!

[You can also view the code base here.](https://github.com/danielmcheng1/danielmcheng1.github.io/tree/master/obstructio)

## Library of SAS utilities for ETLs and QC
I wrote a [library of SAS utilities](https://github.com/danielmcheng1/sas-utility-library) to:
* __Calculate Transformation Sequence__: How do two datasets differ? What sequence of update, delete, and insert commands will transform one dataset into the other? 
* __Perform Validation__: Validate standard checks such as uniqueness check and null check 
* __Perform Type Conversion__: Convert correctly and quickly between different data types to allow proper joins and comparisons 
* __Optimize ETL Performance__: Speed up daily loads by selecting the optimal algorithm for the given datasets (e.g. hash lookup vs. binary search)

Building this library required me to carefully think from the client's perspective to properly define an API. This produced a robust API where the calling client didn't need to know any details within my code base, but could still expect intuitive behavior. Hence to do this, I had to fulfill the API contract for a wide variety of input parameters.

Furthermore, any production code must also be properly documented and thoroughly tested. My [repository](https://github.com/danielmcheng1/sas-utility-library) provides thorough documentation as well as unit tests for each utility. 

## Abstract Syntax Tree
I built an initial prototype (using regex) to parse the SAS programming language. Aside from being a theoretical curiosity and software exercise, this parser also enabled automatic identification of dataset dependencies within SAS codes executed in daily ETLs. 

This allows clients to quickly identify which input data sets affect which output data sets across a series of SAS codes. So for instance, if you discover an error in one input data set and need to update this input, you would be able to quickly tell what output datasets would be affected.

I am currently working to rebuild this using ANTLR. After defining a grammar, I will use ANTLR to create a lexer and parser, ultimately generating an abstract syntax tree. After that, it would be a straightforward exercise to use a listener or visitor to walk down the abstract syntax tree and identify datasets and dependencies. This would then be transformed into a front-end interface for users to quickly drilldown into their code structure. 

<img src="static/img/sample_parser.gif"  alt="SAS parser gif"/>

[Click here to view the current code base.](https://github.com/danielmcheng1/ast-parser)

## Virtual AI Therapist
I built a Facebook Messenger-like Javascript widget for users to speak to multiple virtual AI therapists. The backend is in Python. It uses the Python Natural Languate Tool Kit (NLTK) chat modules, then calls Indico's emotion recognition API to tag emotions in the user's message. This allows the AI therapist to be more empathic in the response it generates.

<a href="http://danielmcheng1-therapist.herokuapp.com/">
<img src="static/img/sample_therapist.gif"  alt="AI therapist gif"/>
</a>

Training a bot to recognize emotions is of particular interest to me, particularly with this latest "Emotional Chatting Machine" blurring the boundary between human and robot (see [_The Guardian_ news briefing](https://www.theguardian.com/technology/2017/may/05/human-robot-interactions-take-step-forward-with-emotional-chatting-machine-chatbot)). I'd like to improve this bot to blend more sophisticated emotion APIs, and ultimately apply this towards enhancing psychotherapy. Several companies have already started doing this. 

**[You can chat with the AI therapist here on Chrome](http://danielmcheng1-therapist.herokuapp.com/)**. I included two additional bots (Olga and Ana) purely as entertainment to contrast their personalities with the actual AI therapist (Eliana).

This bot is hosted on Heroku, using Flask-SocketIO to transmit messages between user and AI therapist. [Click here to view the code base.](https://github.com/danielmcheng1/therapist)