# Drone Software Project
_Author: Daniel Cheng_<br>
_Date: 9/2/17 to 9/17/17_

This writeup documents the software development process for [numerate.io](http://ec2-52-11-200-166.us-west-2.compute.amazonaws.com:5000/photos), an automated drone photo service. I completed this prototype over the course of two weeks. The below analysis showcases three topics: 
* __Project Planning__: Defining user requirements, adjusting timeline as challenges arise, completing MVP
* __Technical Challenges__: Evaluating data structures, learning new tools, solving fundamental CS issues (e.g. multithreading)
* __Software Architecture__: Interfacing with existing APIs, coordinating software components to meet user requirements

[//]: # (include embedded page/screenshot) 

## Document Outline
1. [Project Planning](#1-Project-Planning)
2. [Evaluation of Existing Tools](#2-Evaluation-of-Existing-Tools)
3. [Android App Development](#3-Android-App-Development)
4. [Flask Web Service](#4-Flask-Web-Service)
5. [Conclusions](#5-COnclusions)

## Overview of Software Components 
![Diagram of project architecture](writeup_images/drawio_architecture.JPG)


## 1. Project Planning 
### Raison D'Etre
Drone adoption has rapidly grown over the last few years, from search-and-rescue missions and aerial surveyance prior to excavation, to automated package delivery and photo shoots for personal enjoyment. 

This project prototypes a new application of drones as photo subscription service. The offered service falls into two categories of high-level user stories. 

__Request a photo now__<br> 
* As a city worker, I want to know how many street parking spots areo open so that I can park in the closest spot to my office
* As a commuter, I want to now how long the line is at my local carpooling stop so that I can decide whether to leave now 
* As a young working professional, I want to know how long the line is at my favorite restaurant so that I can avoid standing in a long line 

__Analyzing historical images__<br>
* As a city engineer, I want to know the daily usage of parking spots so that I can analyze the effect of increasing or decreasing free parking spots 
* As a marketer, I want to understand the demographic distribution of shoppers at IKEA so that I can design more targeted advertisements
[//]: # ( * As a real estate investor, I want to survey properties so that I can evaluate the value of my potential investment)

Hence, this drone service automates photo capture so that subscribers can easily count cars and people in real-time for any location of interest. The above stories were merely a sampling of possible applications--you can easily envision many other situations that would benefit from this drone service.

### Requirements
The above user stories can broken down into the following criteria for a minimum viable product.  

As a user of this drone service, I want to have the ability to:
1. Request a photo capture right now
2. Browse current AND historical images for my location of interest 

### Initial Timeline
To further breakdown the complexity of this project, I defined the following timeline for completing each project component over the next 16 days.

![Project Timeline](writeup_images/timeline1.png)

_Note:_ All of this was planned as a prototype for purely recreational purposes. Further development into a commercial product would require consideration of FAA regulations around drone flight.

### Anticipated Roadblocks 
Having done initial research into consumer drone capabilities, I knew that it was possible to automate taking photos and flying predetermined flight routes. In my searches, I had found numerous drone apps that appeared to have these capabilities (discussed in further detail in the next section). Thus the work for days 1 through 4 seemed to merely be a matter of execution.

However, I had found no examples of consumers apps allowing for scheduled or triggered missions. I suspected there were potential safety concerns--as well as less demand for this in the hobbyist market (i.e. unless you are flying drones commercially, it seems unlikely that you would need to have fully automated scheduled drone flights). 

If by Day 5 in my timeline, I indeed could not find an existing product for scheduling drone flight, I had two alternate plans:
1. Build a customized app using [DJI's mobile SDK](https://developer.dji.com/mobile-sdk/)
2. Plan for having a manual release of the drone by a human worker. No matter how automated, this drone service would likely need some human intervention to maintain

## 2. Evaluation of Existing Tools 
### Hardware Justification
For this project, I chose to use a DJI drone for two reasons. First, DJI is the clear leader in the consumer drone space, owning perhaps [50% of the North American market](https://www.recode.net/2017/4/14/14690576/drone-market-share-growth-charts-dji-forecast). My project was focused on software rather than hardware--so I wanted to pick the most reliable hardware available, thus avoiding having to troubleshoot flight control or camera issues.

Secondly, DJI offer [programmatic control](https://developer.dji.com/mobile-sdk/documentation/introduction/mobile_sdk_introduction.html) of its drones, opening up the possibility of advanced customized control over the drone's flight. 

Among the DJI drones, I selected the Mavic Pro because of its popularity in taking high-quality aerial photography. As a middle-tier drone, the Mavic Pro also automates many parts of drone piloting, from takeoff and landing to obstacle avoidance and intelligent flight modes. Again, the focus of this project was on software and not on hardware--hence I wanted to select a drone that would automate as much of the piloting experience as possible. 

<img src="writeup_images/mavicpro1.png" width="50%" alt="Mavic Pro"/>
<img src="writeup_images/mavicprocontroller.png" width="40%" alt="Mavic Pro Remote Controller"/>
<br>

_Note_: For those unfamiliar with drones, you control the drone aircraft (left image) using a remote controller (right image), which transmits commands at 2.4 to 2.483 GHz. You then connect your phone to the remote controller, allowing you to not only issue commands directly from an app, but to also view a live camera feed of the drone's point of view.

### Downloading Photos
For the first two days, I experimented with the basics of flying a drone and taking photos. I first confirmed that the image quality was more than sufficient for my photo service (the photos came out as 12000 MP, a resolution far higher than most web browsers need for rendering). Secondly, I tested flying simple automated flights ("missions").

During this phase, I ran into a roadblock with displaying the drone image in real-time on a website. When a photo is captured, the drone only stores the images on the SD card loaded on the physicial aircraft. However, I needed to download those photos from the aircraft to my mobile device--so that I could then immediately push those photos to my web server. Otherwise, the images would remain stuck on the aircraft until it landed. Furthermore, this image download had to occur programmatically, so that scheduled and triggered flights could push images automatically without any human intervention.

Hence, to deliver on this feature, I sought out a DJI mobile app that could reliably download all images captured during a flight to local phone storage. Photos could then be pushed (using an app like [BotSync] (https://play.google.com/store/apps/details?id=com.botsync)) to the EC2 hosting my web server. 

Should this prove impossible, I had a backup plan to install an Eyefi card on the aircraft--so that at the very least, images could automatically transmit once the drone landed in the wifi area. This would incur a slight delay in streaming to the website, but this would still allow for fully automated upload of images without human intervention.
 
### Comparison of Drone Apps 
Given my first two days of drone exploration, I now focused my efforts on finding an existing mobile app providing functionality to:
1. Take photos while automatically flying a preset flight path (mission)
2. Download photos to phone
3. Schedule and/or trigger missions 

You may ask why I did not immediately attempt to write my own mobile app to accomplish all of my required features. In software development, it is better practice to first use existing libraries and packages instead of writing your own custom solution. First, this can save significant time if you can simply plug in an existing app into your own custom architecture. Secondly, prebuilt libraries are usually better tested, having gone through multiple iterations before being shared for general use. 

Hence, I wanted to exhaust existing solutions that could achieve the above three criteria, before considering alternate solutions (such as writing my own mobile application). 

[//]: # (check spelling, cost, system availability)

#### Native DJI GO App
<img src="writeup_images/djigoapp1.png" width="65%" alt="DJI Go App"/>

DJI provides its own [DJI GO App](https://www.dji.com/goapp) when flying its drones. This app runs comprehensive startup validation (e.g. compass calibrated, GPS connected), then offers a full suite of in-flight controls, including:
* Single shot, timed shot, and video capture 
* Camera tuning (adjusting focus, exposure, and orientation) 
* Photo caching (download photos to phone storage) 
* Waypoint missions (automatically flying the drone along a predetermined set of GPS coordinates)

Thus the DJI GO App fulfills criteria #2 (download photos), but only partially achieves criteria #1 (automated mission). Although the app could automatically fly the drone along previously visited waypoints, it could not automate photo capture throughout the mission. 

As it turns out, the majority of other consumer apps allow for more advanced control over waypoint missions (criteria #2), but fail to allow for photo downloading (criteria #1). The next section evaluates these feature tradeoffs amongst the most popular DJI drone apps. 

#### Category 1: Hobbyist Apps for Recreational Photography
This first set of apps targets the drone enthusiast market who fly drones solely for personal recreation. In increasing order of price:
1. Airnest 
2. DJI Ultimate Flight
3. Litchi
4. Autopilot

<br>__Airnest__<br>
The [Airnest app](http://www.airnest.com/) is marketed as simply and easy to use with a "Photostop style" interface. For example, for waypoint missions, the app allows users to simply "paint a line" on a map, and the app converts that into mission instructions for the drone.

<img src="writeup_images/airnest.png" width="60%" alt="Airnest App"/><br>

In my user tests, the app unfortunately failed to live up to its promise of being extraordinarily simple and easy to use. Missions could indeed be drawn with the flick of a finger, but editing those missions proved nearly impossible. For example, when I attempted adjust the auto-generated waypoint, I could find only one exact pixel spot where the app would respond to my touch.

Airnest does offer other features for more serious drone enthusiasts, such as flight logging, playback, and health metrics. As a free app, Airnest provides perhaps the best value for a drone hobbyist wishing for customization beyond the native DJI Go App. 

<br>__DJI Ultimate Flight and Litchi__<br>
These next two apps offer very similar features, with [DJI Ultimate Flight](http://djiultimateflight.com/) coming in at $20, and [Litchi](https://flylitchi.com/) at $23-25 depending on the system. These two are the most popular DJI drone apps mentioned in drone enthusiast forums and sites.

The app layout mimics the DJI Go4 App, with a first-person video stream in front, camera options on the side, and toggle menus for capture settings, waypoint behavior, etc.

<img src="writeup_images/djiultimateflight.png" width="60%" alt="DJI Ultimate Flight App"/>

Users can create far more customized and automated missions than would be possible in the native DJI app. This includes:
* Taking pictures (single shot and timed shot) at a waypoint
* Recording video at a waypoint
* Rotating the camera to focus on a point of interest 
* Pausing and hovering at a waypoint

Users simply tap on the map to create a waypoint, then add any of the above actions to that waypoint. A series of such waypoints are then uploaded as a mission to the drone. All that's left is to hit "Run Mission" and the app will fly the drone from start to finish!

<img src="writeup_images/litchi_missionscreen.JPG" width="60%" alt="Litchi Mission"/>

Hence, DJI Ultimate Flight and Litchi fulfill criteria #2 (automated mission with photos). However, these apps fail to meet criteria #1 (download pictures automatically). Litchi does offer photo caching on iOS, but this feature is not avialable during waypoint missions.

For example, for the waypoint missions, these apps allow you to mark destinations on a map, then convert these into a drone mission--unlike the DJI Go4 App which requires you to fly the drone through all these destinations before rerunning.

<br>__Autopilot__<br>
[Autopilot](https://autoflight.hangar.com/) is by far the most advanced hobbyist app on the market. Users can precisely control every aspect of automated drone flight, from the exact camera angle and focus to the curvature and descent of flight between waypoints. Autopilot also offers tracking of other drones within the area, on top of flight recording and logging.

<img src="writeup_images/autopilot.png" width="65%" alt="Autopilot"/>

The priciest of all these apps ($29.99), Autopilot is ideally suited for those who need advanced automated flight control beyond what Litchi and DJI Ultimate Flight can offer. The learning curve is steeper due to the increased complexity offered for mission planning.

Despite its advanced features, Autopilot does not offer automatic photo download either during waypoint missions, hence failing criteria #2.

#### Category 2: Commercial Apps for Surveying and Mapping
This second set of apps targets professional or enterprise customers who fly drones to survey and map landscapes. These apps enable users to automate flight paths for large areas of land: Mark a rectangular grid on the map, and the app will automatically calculate the path, speed, and frequency of photo capture.

Thus, instead of allowing users to customize every point along the mission, these apps determine the optimal path so that the resulting photos can be used to generate high-resolution stitched images and 3D models of the landscape. In increasing order of cost:
1. PrecisionFlight
2. Pix4Dcapture
3. DroneDeploy

<br>__PrecisionFlight__<br>
Deployed by PrecisionHawk, this free [PrecisionFlight app](http://www.precisionhawk.com/precisionflight) is straightforward to use: Simply touch and drag to mark the survey area on the map, then the app will automatically generate a waypoint mission to fly. There are no additional capabilities for customizing camera focus or gimbal rotation--the app simply flies the drone over the desired area and captures the images required to generate a high-resolution image of the area.
<img src="writeup_images/precisionflight.png" width="65%" alt="PrecisionFlight"/>

<br>__Pix4Dcapture__<br>
Another free app, [Pix4Dcapture](https://pix4d.com/product/pix4dcapture/), offers more control over missions than FlyingPrecision does. Upon opening the app, users select from various mission layouts to suit their surveying needs.
<img src="writeup_images/pix4dcapture.png" width="65%" alt="Pix4Dcapture"/>

As evident in the above screenshot, everything in the app is geared towards the post-processing stage, in which photos are transformed into 2D maps and 3D models. In the words of one of the supported reps that I contacted regarding this app:
> Pix4Dcapture is a great flight planning app we provide free [but] you are free to use other applications if they better suit your needs. It is our Pix4Dmapper software that is the premier solution for photogrammetry, and as long as you are able to capture your images with the correct overlap and quality, you can process with Pix4Dmapper. 

Among the apps I surveyed, Pix4D was the only one that offered complete functional photo caching on both Android and iOS. Upon mission completion, all photos are streamed to the corresponding mission folder on internal storage, before being uploaded to Pix4D cloud for 3D modeling.

<br>__DroneDeploy__<br>
The [DroneDeploy](https://www.dronedeploy.com/app.html) app lands users on a demo mission showcasing the app's ability to map a large Midwest farm. Offering a free Explorer tier followed by a $99 per month Pro tier, DroneDeploy offers the most advanced mapping features of all apps considered. This includes automatic area and volume measurements, NDVI calculations, and 3D exports. 

<img src="writeup_images/dronedeploy.png" width="65%" alt="DroneDeploy"/>

Although DroneDeploy offered perhaps the best mapping features on the app market, I ran into similar issues with photo caching, in which the app automatically generated hundreds for photos for a mission, but required manual extraction of images from the SD card in order to process. 

### Conclusion of Drone App Evaluation 
After thoroughly testing all of these drone apps, I concluded that no existing app could fulfill the minimum criteria necessary for my drone service.

Litchi came closest with its mission planning interface and automated flights, but failed to offer photo downloading during missions--essential for immediate streaming to my website. 

Pix4D was a close second since it automatically downloaded images to the phone upon completion of the mission, but its mission planning was not flexible enough for my needs. Because the app was meant for surveying a region, the quality and rate of image capture was locked away in a black box--hence I had no ability to customize taking pictures at different angles and speeds. 

Finally, none of the apps offered a way to schedule or trigger a mission (through a medium like SMS). Ultimately, you would still have to manually press a button to start the mission.

__***Hence, I now had to rapidly pivot from my original development plan and build my own Android app to fulfill the project requirements.***__ 

## 3. Android App Development
### Minimum Requirements for App
Given the limited timeframe, I needed to carefully identify the exact requirements for my custom app. I was _not_ designing a user-facing app like Litchi, with a complete UI, product validation, forms for custom missions, and so on. Rather, I only had to build the following list of features: 

_Rebuilding Features Available in Existing Apps_<br>
* __Mission Automation__: Take off from ground, fly preset route while taking photos, then return home and land 
* __Photo Download__: Photos should automatically download to the phone's internal storage 
* __Image Quality__: Camera should auto focus throughout to ensure quality photos

_Adding New Features_<br> 
* __Scheduled Missions__: Schedule a mission to run every 5/10/15 minutes
* __Triggered Missions__: Use SMS to trigger the mission
* __Photo Transfer__: Push downloaded photos to EC2 server
* __Photo Compression__: Reduce photo size from 5 MB to 0.5 MB to speed up transfer


### Problem Search: Evaluating the Mobile SDK
Before jumping into coding all of these functions, I first identified how each requirement mapped to an existing class or method in the [DJI mobile SDK](https://developer.dji.com/mobile-sdk/documentation/introduction/index.html). For any software engineering project, it is a best practice to evaluate the feasibility of each component beforehand--instead of discovering halfway through the project that the most crucial part is not possible. 

Feature | DJI SDK Class | DJI SDK Method
------- | --------- | ----------
Mission Automation | MissionBuilder | addWaypoint, addAction, loadMission, startMission 
Photo Download | MediaManager | onNewFile, fetchFileData
Image Quality | Camera | setFocusmode

Feature | Android Package
------- | ---------------
Scheduled Missions | Timer
Triggered Missions | BroadcastReceiver / SMS Manager
Photo Compression | ImageUtil
Photo Transfer| JSch

During this phase, I also reviewed the sample [DJI tutorials}(https://developer.dji.com/mobile-sdk/documentation/introduction/index.html), and identified troubleshooting resources, such as the [DJI developer forum] (http://forum.dev.dji.com) and [DJI posts on Stack Overflow] (https://stackoverflow.com/questions/tagged/dji-sdk). I additionally contacted DJI support to validate the most essential feature for my app (i.e. that photos could be automatically downloaded during mission execution).

### Revised Timeline 
Once I determined that the DJI mobile SDK could implement all of my required features, I adjusted my initial timeline to account for the effort required to write an Android application. 

At this point, six days had elapsed already. Given that I had not worked with Android before, an initial prototype would take, at minimum, three days--and a would likely take closer to five or six days to iron out any bugs. Hence, to accommodate app development, I had to eliminate several features in my initial timeline, including:
* Automated MMS photo sharing 
* Setting up subscription service 
* Prototyping system for multiple drones 

These were nice-to-have features in a beta version of the app--but were not necessary for the alpha version. Recall the requirements for this drone service:
> 1. Request a photo capture right now
> 2. Browse current AND historical images for my location of interest 

Hence I chose to divert the majority of my remaining time into this custom Android app, to ensure I could achieve the above two criteria. 

Finally, I also deprioritized writing code to automatically parse and count cars in these drone images. This was again a nice-to-have feature, but not strictly necessary. For example, users of this service could easily take a look at a photo of street parking and tell if any parking spots were open. Automatic object recognition was not strictly necessary for the success of this project prototype.  

Thus my revised timeline was as follows: 

![Project Timeline](writeup_images/timeline2.png)

### Software Build 
I chose Android as the development platform for two reasons:
1. __Existing Hardware__: I had an Android phone readily available for installing and debugging 
2. __Developer Control__: I valued Android having more flexibility than iOS (e.g. having more control to save photos in any folder of the file system, having the ability to publish app directly to the Marketplace)

As I had no direct Android app development experience--and given the limited timeframe for project completion--I copied the existing codebase from DJI's [QuickStart Guide](https://developer.dji.com/mobile-sdk/documentation/quick-start/index.html) and basic [mission and camera tutorials](https://developer.dji.com/mobile-sdk/documentation/android-tutorials/index.html). Rather than spending my limited time setting up product registration, drone connectivity, and live-camera streaming, I simply enhanced the existing tutorial to address my needs.

Below is a breakdown of which app features were successfully completed by project day:<br>
__Day 7__:
<br>[x] Compile and run tutorials 
<br>[x] Set up live video stream 
<br>[x] Create button to take a photo during drone flight
<br>[x] Troubleshoot Android permissions (requested at runtime instead of on install for >= Marshmallow)

[ ] Test

__Day 8__:  
<br>[x] Programmatically set autofocus 
<br>[x] Automatically take off
<br>[x] Automatically land 
<br>[x] Download photos to internal storage 

__Day 9__:
<br>[x] Add waypoints based on GPS coordinates
<br>[x] Add custom actions at each waypoint (start timed shot, rotate gimbal, etc.) 
<br>[x] Upload multiple waypoints as one mission to the flight controller 

__Day 10__:
<br>[x] Test complete execution of mission with automatic timed shots 
<br>[x] Create button to trigger mission every 5/10/15 minutes 
<br>[x] Resize images from 5 MB to 0.2 MB 
<br>[x] Post resized images to EC2 server backend 

__Day 11__:
<br>[x] Create button to listen for SMS trigger for kicking off mission 
<br>[x] Automatically save photos in timestamped mission folder (locally and on server)
<br>[x] Test complete execution of mission with automatic resize and upload to server 
 
__Days 12 - 14__: 
<br>[x] Troubleshoot multithreading / download bandwidth issues with downloading photos 

As evident in the above timeline, I completed the app prototype within the expected timeframe of six days, but I ran into a major roadblock with downloading photos that consumed nearly three full days. 


### Technical Challenges: Synchronization and Multithreading for Photo Downloads
_Debugging / Problem Scope_ 
During my first code iteration, I automatically triggered file download to local phone storage. That is, whenever the DJI camera app generated a new file, it would automatically start downloading the file data:
```java 
camera.setMediaFileCallback(new MediaFile.Callback() {
    @Override
    public void onNewFile(MediaFile mediaFile) {
        mediaFile.fetchFileData(new File(mDownloadPath + "/" + subfolder), filenameNoExtension, new DownloadListener<String>() {
            @Override
            public void onStart() {
            }
            public void onSuccess(String s) {
            }
            public void onFailure(String s) {
            }
            
        }
    }
}
```
This feature appeared to work perfectly when testing indoors in the DJI simulator (a virtual flight software allowing execution of missions on the computer). 10-20 photos would be captured and downloaded automatically throughout mission flight.

However, upon running the exact same missions outside, only the first 5 or 6 images would download. The rest would raise a timeout error and block all subsequent downloads. I had two hypotheses for debugging this failure to download photos:
* __Transmission Distance__: Failure due to increased radio distance transmission when flying outdoors
* __Limited Bandwidth__: Failure due to limited CPU or bandwidth for downloading media files
 To test these hypotheses, I first ran a more extensive stress by trying to download all the photos at the end of the mission, when the drone was within a few feet of me. Despite this adjustment, I still ran into similar download issues. 

Moving onto the second hypothesis, I found supporting documentation in a DJI developer thread regarding timeout due to limited bandwidth. By downloading the data as soon as a new file was generated, I had consumed all the bandwidth by the time the mission had taken its 10th or 11th automatic photo. Furthermore, I did not consistently observe this error during simulator testing because the overall system load was lower; that is, when flying outside, the drone system had to allocate additional resources towards flight control, as opposed to merely simulating flight indoors. 

In typical software development. one needs to execute three types of tests:
1. __Fault Testing__: The program should correctly executes its intended function 
2. __Stability Testing__: The program should reliably execute its function as frequently as possible (even if one or two cases fail)
3. __Stress Testing__: The program should execute properly when scaled up to production level

Hence my automatic photo download failed stress testing because the simulator environment did not fully capture the load during production (i.e. when flying outside). 

_Solution_<br>
To workaround the limited bandwidth for downloading media files using the DJI SDK, I applied two software techniques:
1. Maintain a queue of downloads 
2. Apply a mutex to prevent multithreaded callbacks  

Implementing the queue was as simple as adding new files into an array list:
```java 
camera.setMediaFileCallback(new MediaFile.Callback() {
    @Override
    public void onNewFile(MediaFile mediaFile) {
        addNewMediaFileToQueue(mediaFile);
    }
}
```

However, simply dequeueing element by element and calling the download method failed due to multithreading.
```java
while(!mMediaFilesToDownload.isEmpty()) {
    MediaFile mediaFile = mMediaFilesToDownload.remove(mMediaFilesToDownload.size());
    downloadOneMediaFile(mediaFile, label);
}
``` 
Because array lists are not synchronized structures, multiple threads were popping off and attempting to download, which not only cause concurrent write conflicts, but also led to multiple downloads executing in parallel (which ultimately consumed all available download bandwidth).

This was easily remedied by either (1) making the method synchronized, or (2) iterating without removing. 
```java
while(!mMediaFilesToDownload.isEmpty()) {
    MediaFile mediaFile = mMediaFilesToDownload.remove(mMediaFilesToDownload.size());
    // avoid repeated download if method is called again 
    if (!mMediaFileNamesDownloaded.contains(mediaFile.getFileName())) {
        downloadOneMediaFile(mediaFile, label);
    }
}
```

However, this dequeueing approach still failed to prevent overloaded download bandwith because the SDK download call was executed as a callback. Thus, even though files were dequeued sequentially, one at a time, the callbacks could end up executing simultaneously on the background thread.

Hence, to solve this, I implemented a mutex so that only one file could be downloading at any given time. This guaranteed that even if multiple callbacks were triggered, only one file could download at once--hence ensuring sufficient download bandwidth.

Note that although this solution executed more slowly than download multiple files in parallel, this solution was far more reliable--a more valuable feature in this case to ensure that all images would be loaded to the server.

```java   
mediaFile.fetchFileData(new File(mDownloadPath + "/" + subfolder), filenameNoExtension, new DownloadListener<String>() {
    @Override
    public void onStart() {
        mMediaDownloadOneFileLock.lock();
    }
    public void onSuccess(String s) {
        try {
            // resize image 
            // SCP to EC2 server 
        } catch (IOException e) {
            e.printStackTrace();
        } finally {
            mMediaDownloadOneFileLock.unlock();
        }
    }
    public void onFailure(String s) {
        mMediaDownloadOneFileLock.unlock();
    }
}
```
   
### Other Technical Learnings 
* Android Studio/Gradle
* DJI Assistant/Simulator
* ADB Logging Tools
* Java Concepts
   * Enums
   * Builders 
   * Callbacks
   * Implementing and extending 
   * Synchronizing / multithreading 
* Android Concepts
   * Android Life Cycle (onPause, onResume, onDestroy, etc.)
   * Multithreading (UI thread, main thread, etc.)
   * Broadcast receiver and intent filters
   * Permissions 
   
### Final Architecture of Android App
//replace with zoomed in view of diagram 
* Image Resize
* ScpTo
* SMS Processor
* Custom exceptions
* Waypoint mission flying
* Live video feed

// TBD: insert screenshot of app here 

## 4. Flask Web Service
After troubleshooting the photo downloading issue described above, I had 1.5 days remaining to build the front-end web service in Flask. Given the tight timeline, I again winnowed down to the following  minimum criteria for completion. Note that this lists excludes automatic parsing / counting of cars within the images--as discussed before, this was a useful but not necessary feature of my envisioned service, and hence I chose to drop this so that I could deliver on the below essential features. 
* Automatic refresh of latest images from drone 
* Fast historical image browsing 
* Playback of historical images 
* Responsive on mobile 

### Architecture
[//]: # diagram 
[left to right] 
SCP sharing folder
Images with final stitched/cleaned photos
Merge to find differences 
-->hugin executor 
-->CV2 image reiszing/rotation 
-->Flask server / Jinja generates  template -->hosting on EC2 

front end client views this 
-->Javascript front end for animation, browsing, and refreshing 
loops back to front 

### Find the Latest Images  
[//]: # (tree snapshot)
During mission execution, images are automatically saved into timestamped folders by mission ID. These raw images are pushed from Android local storage to the SCP share location.

The final processed images for displaying on the web are placed in an identical folder structure. Hence to determine new mission executions since the last refrehs, I simply compare the two folder structures and process any folder names that are in the SCP share location but not in the static/images location. 

### Image Processing 
For certain missions, the drone takes a series of timed shots--hence these photos need to be stitched together to construct the final blended photo. 

I selected Hugin, an open source photo processing package, because it fulfilled the two minimum requirements for stitching:
1. Any number of images could be correctly blended into one final image 
2. The stitching process could be automated as a script

Hugin offers Hugin Executor, a command line utility for stitching, aligning, and processing photos. Stitching is achieved by calling various other photo processing packages, such as nona, enblend, and cpfind. These implement algorithms like Dijkstra's two point alignment and [...].

The one unforeseen problem with Hugin Executor was its requirements for high CPU usage, which exceeded the capacity of the EC2 I used for hosting. One solution was to simply upgrade the EC2, but I chose instead to write a simple script to cap CPU usage by Hugin and all its derivative processors. Even a larger box, I would need some way to guarantee that Hugin did not consume too much compute power; hence limiting CPU was the simplest and fastest solution towards a viable product.

```bash
nohup cpulimit --exe=/usr/bin/hugin_executor --limit=75 &
disown

nohup cpulimit --exe=/usr/bin/nona --limit=75 &
disown
[...]
```

Finally, I utilized the Python CV2 library for final image clean-up, including compressing and converting Hugin output tif to jpeg images.

### Flask Hosting
Because I architected my SCP sharing site and image hosting folder with a mission ID-date-timestamp hierarchy, it was simple to iterate over each processed mission folder and generate an HTML template where users could:
1. Scroll down the page and views pictures grouped by day 
2. Browse within a day and views pictures sorted by timestamp 

Using the Jinja engine, I dynamically generated the HTML template for displaying all images. 

### Front End 
To display the mission images in a clean user-friendly front-end interface, I utilized bootstrap for basic styling. This also ensured responsiveness across devices. 

I then coded Javascript functions so that users could:
1. Click and zoom in on images (pinch and zoom on mobile) 
2. Click to browse pictures sorted by timestamp within a given day 
3. Click to animate the photos (essentially showing a gif for a given day) 

Finally, because Flask does not enable auto refreshing of a page from the back-end server, I implemented a Javascript callback to trigger a refresh every 60 seconds. While not ideal, this solution sufficed for this prototype. Future iterations can implement a method to refresh immediately when a new image is found.

## 5. Conclusion
### Future Work 
My next iteration of this drone service would add the following features: 
* Automatically parse and count cars in the drone images 
* Send MMS of images from the latest executed mission 
* Set up subscription service for requesting drone to fly mission right now 

Should this prove successful, I would then scale this up: 
* Prototype software to coordinate and schedule  multiple drones flying throughout the day 
* Minimize downtime for battery recharging

This is currently the difficulty with almost all consumer drones: A single battery can last for approximately 25 minutes of flight. Hence to fly missions over the span of several hours requires human intervention to swap and recharge batteries. 

Several commercial products have been developed to address this need:
* __Skysense__: Wireless charging (drone charges upon landing on pad--no manual battery swap needed) 
* __Dronebox__: Solar-powered autonomous charging stations
* __Airobotics__: Robotic arm automatically swaps batteries and payloads in and out

I would explore these products in more depth to determine compatibilitiy with current drone setup (as they may not work with DJi drones), and to evaluate cost tradeoffs (e.g. robotic battery swapping machine may cost far more than simply having a worker manually swap batteries for my service). 

### Final Takeaways
SEE NOTES 
BREAKDOWN PROBLEM—e.g. API make it as explicit as possible and small as possible so that you make the MVP
Make sure you scope as much of the problem so you know if feasible before investing more time
You always try to find a prebuilt solution—like all these apps—instead of building your own. Much faster and smarter and safer
Agile Development:  Planning a project of unknown complexity, adjusting as unexpected obstacles come  up
Minimum Viable Product: Quickly picking up and learning whatever techniques are necessary for MVP 
Production Systems: Having your component communicate with each API/service--and making it work with your product so YOUR integration is reliable and failsafe despite any issues with the other APIs/systems

