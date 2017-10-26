## Automated Drone Photo Service 
[link](http://ec2-52-11-200-166.us-west-2.compute.amazonaws.com:5000/photos)
    
This is a complete automated drone photo service to count cars and people. Users of this service can request photos in two ways:
1. Send a text message to trigger the drone to start its mission 
2. Schedule the drone to fly every 10 minutes over the same area each day 
[VIDEO]
In terms of architecture, I built a custom Android app to automate mission control of the drone (via [DJI's mobile SDK](https://developer.dji.com/mobile-sdk/). This then compresses and pushes the photos to the hosting AWS EC2. Python then stitches and cleans the photos using [Hugin](https://wiki.panotools.org/Hugin_executor) and [OpenCV](https://opencv.org/), before posting to the [Flask-hosted website](http://ec2-52-11-200-166.us-west-2.compute.amazonaws.com:5000/photos). I completed the entire build in 2 weeks. 

One significant technical challenge was in troubleshooting multithreading issues with limited download bandwidth. To automatically transfer photos from the drone to AWS, I had initially allowed the DJI SDK to continually download as many photos in parallel as possible. However, after 5 or more photos, the SDK quickly ran out of bandwidth and failed to download any remaining photos. To solve this, I first maintained a queue of photos to order downloads one by one. Secondly, I implemented a mutex to prevent multiple callbacks from executing in parallel. While this slowed down the download process, this solution guaranteed reliability, a far more valuable feature for this drone service. 

You can review the [drone writeup](https://github.com/danielmcheng1/drone/blob/master/writeup.md) to learn more about these technical challenges, softer project skills (defining user requirements and completing an MVP), and the overall software architecture. 

##Scrabble AI
[link](http://ec2-52-11-200-166.us-west-2.compute.amazonaws.com:8000/login)
This is a complete Scrabble application with:
1. AI running greedy backtracking algorithm to play optimal move each turn 
2. Validation and scoring for all human moves
Click [here]((http://ec2-52-11-200-166.us-west-2.compute.amazonaws.com:8000/login)) to test your own lexical skills against the Scrabble AI.

The entire move algorithm was built from scratch based on the algorithms

    <h2>Play the Classic Word Game against the Scrabble AI</h2>
        <img src="/static/img/scrabble.png"></img>
    </a>
Building a Scrabble validator and AI is a more complex exercise than at first glance.

Details on GADDAG: https://en.wikipedia.org/wiki/GADDAG 
3 constraints

<!doctype html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Daniel M Cheng</title>
    <link rel=stylesheet href="static/css/index.css">
</head>
<body>
    
    
    
    <a href="obstructio/obstructio.html" style="color:black">
    <h2>Obstructio: The Block Game to Break Your Will</h2>
        <img src="/static/img/obstructio.png"></img>
    </a>
    
    
    <a href="http://danielmcheng1-therapist.herokuapp.com" style="color:black">
    <h2>Speak to Your Virtual AI Therapist</h2>
        <img src="/static/img/therapist.png"></img>
    </a>
    
    SAS module /API
</body>

<!--html lang="en-US">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="refresh" content="1; url=https://danielmcheng1.github.io/obstructio/obstructio.html?">
        <script type="text/javascript">
            window.location.href = "https://danielmcheng1.github.io/obstructio/obstructio.html?"
        </script>
        <title>Page Redirection</title>
    </head>
    <body>
        If you are not redirected automatically, follow this <a href='http://danielmcheng1.githubio.com/obstructio'>link to example</a>.
    </body>
</html-->