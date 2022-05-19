# Project Cloudware #
## Description ##
This is the final project from the DAW Course imparted in [Esteve Terradas i L'Illa school](https://www.iesesteveterradas.cat).\
The project is about building a web application that allows users to upload resources into the application and share those resources.
## Made By ##
This project has been developed by:
* [Guillem Albo](https://github.com/g-alpi)
* [Carlos Valenzuela](https://github.com/carlosvalgar)
## Tecnologies Used ##
* :page_facing_up: HTML :page_facing_up:
* :art: CSS :art:
* :tv: JavaScript :tv:
* :snake: Python :snake:
### Frameworks Used ###
* :snake: Developed in Django 4.0 :snake:
* :art: Layout made with Bootstrap 5.0 :art:
## How we managed the project ##
We used the Scrum methodology to organize our project.

![image](https://user-images.githubusercontent.com/73992493/169298161-7a2f4c66-84e3-46a6-ac75-bfe234bd9a03.png)

We used the project and issues feature in Github to manage all our tasks or bugs that we found:

![image](https://user-images.githubusercontent.com/73992493/169298274-1925d927-96ed-4470-b32d-28b9908a55b9.png)

For every week we started a new project emulating a sprint:

![image](https://user-images.githubusercontent.com/73992493/169298016-c5c67e54-5c16-489e-aedd-5255c51d02cf.png)

## Wireframes ##
We used [Figma](https://www.figma.com/) to develop a wireframe that we could follow:

![image](https://user-images.githubusercontent.com/73992493/169297721-658ce371-f100-42df-8150-3b606456f313.png)

## Database Design ##

![image](https://user-images.githubusercontent.com/73992493/169298528-9b72f26f-ec5c-4f9c-9982-ad20eaf1aa43.png)

## Web Page ##
### Landing Page ###
In the landing page we though of made the typical web that tells about the product we're offering:
### Register and Login Pages ##
In those pages we have a form with validations that guides our users to use the application:
### Profile Page ###
In this page the user can change many options of their profile, or even delete their account:
### Application Page ###
This is the most important page of our project, here we have a screen with all the documents that the user uploaded an can download: \
The Shared Files, and the options to upload, share or delete resources: \
The user can click with the right click to open a contextual menu to make all operations that are in the buttons, so he can select the way he wants to use our application: \
For everly option will open a modal box to manage the appropiate operation: \
And will guide the user like the register and login pages: \
The Share Files Page we can see all the files that have been shared with us with a similar use of the Cloudware application page:
## How to Install ##
:snake: Install python3:
```
sudo apt install python3
```
:snake: Install the virtualenv from python:
```
pip install virtualenv
```
:hammer: Open a terminal inside the downloaded project (Cloudware Folder) and create the environment:
```
python3 -m venv [path-to-new-virtual-environment]
```
:confetti_ball: Activate the environment
```
source [path-to-new-virtual-environment]/bin/activate
```
:pray: Install the requirements into the environment:
```
pip install -r requirements.txt
```
:running: Run the application:
```
./manage.py runserver
```
