# User manual
Welcome to Emotion Capture, a tool that automates the process of finding keypoints and extracting facial features from mice. A process that usually is extensive and time consuming is now automated by using our application. Assuming you provide our model with correct training data our product should be able to help you avoid long labeling sessions.

## Installation
To be able to run the application you need to download the correct packages and extensions. All of the requirements to install and how you should create the enviroment is provided in install.md. There you can see the expected file structure and how to clone the repository. 

## Getting started
Upon launching Emotion Capture, you will be greeted with a start up screen. From here, you can create a new project or open an existing one, these options can be found under the menu option "file". When creating a new project, you need to provide a name for the project. 
After a project is created or opened you can choose to add more mice or new data to a project, these options are also available unde the menu option "file". For a new project you must add a new mouse. When adding a new mouse you should add mouse name, mouse gender, mouse genotype, mouse weight and mouse age. All the fields needs to be filled in! Then when a mouse is created it will not show up in the file selecter before you have added data to that mouse. Select a video or some images by clicking "Browse" in the smaller pop-up window that appears when clicking the button "New data". After a video or some images that you want to ectract data from is selected and you click the button "switch" a smaller window appear that says Processing data. This window will show the progression of the video/image processing. Do not click the window during processing, it might crash the application. Wait until the processing window says "Done" before closing it. Image format should be either JPG, PNG or JPEG. Video format should be MP4.

## Validation
When the interesting frames are extracted, you will have to validate the data and assign a phase label to the frame. Go through all of the frames in the filelist, watch so that the keypoints are correctly placed. If a framed is bad, select it and remove it by clicking the trash can below the image displayer. If the points are slightly wrong, they can be modified by clicking the paint brush below the image diplayer. A pop-up window will appear where you can drag points and then save the new position by the check-symbol. If an image has a low profile confidence, keypoint confidence or if the feature is outside of a specific interval a small yellow warning triangle is shown in the top left corner of the image in the file selecter. This indicates that you should be even more vigilant that the result might be bad. To assign a phase to the frames, select all frame you want to assign (left-click first frame and then shift + left-click last to select all in between), then right-click, assign label and choose either baseline, experiment or recovery. 

## Visualisation
By clicking the "Visualisation" in the menu bar you get the option to choose either K-means clustering or HDBSCAN clustering. If you want to return to the validation window, you can do so by clicking the "main" option. In the visualisation window both the radarplot, lineplot and the text box updates when clicking a frame or a point in the clustering graph. Clicking a specific measurement in the radarplot will either remove it or add it to the lineplot depending on if is shown at the time. There is aslo an option in the menu bar to refresh the visualisation, this is done by clicking "reload the visualisation".

## Exporting the result
To export the data to a csv-file you need to right-click the video folder and click export. Then you can save the csv as usual by assigning a name to the csv and then where to save it.   

We recommend watching the video of how to use the application. 
