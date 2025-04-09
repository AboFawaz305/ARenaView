> [!NOTE]  
> This repository was made to show our progress for the AILeague contest.

# Project status
- [x] Code to gather data from devices and send it to the server
- [x] Main endpoints for the server
- [ ] An example View to test viewing from the server
- [x] Code to use the model
- [x] the main.py of the server
- [ ] Code to manage the frames coming from the multiple devices camera
- [ ] Code to process and enhance the frames before using the model
- [ ] Build the model to calculate players speed
- [ ] Build the model to add visual effects to frames
- [ ] Adding test cases
- [ ] Buld the goal detection model

# How the code works

The program is divided into 3 subparts the device part in the folder "device" contain the code that should run on devices to send their camera output to the other part the server. the server - contained in the "server" directory job is to receive frames from the devices and organize it to be processed by the model to choose the frame that gives the best view and add some enhancements and effects to make the enhance the fans experience, after that the last part the view code which is inside the "view" directory is concerned with the code that should run on the viewing devices to take the frames from the server and show to the user you can say it is the frontend.

# LICENCE
This code is licenced under the MIT licence for more details you can refer to the LICENCE file inside this repository.

