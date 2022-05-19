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

![image](https://user-images.githubusercontent.com/73992493/169299574-6ca70eaf-6d08-4416-9f30-19ac707c9474.png)

### Register and Login Pages ##
In those pages we have a form with validations that guides our users to use the application:

![image](https://user-images.githubusercontent.com/73992493/169299820-82d32430-d989-4752-b7c4-fef328c33284.png)

![image](https://user-images.githubusercontent.com/73992493/169299997-38985e8a-a07d-4e58-b6c8-65992387b12c.png)

![image](https://user-images.githubusercontent.com/73992493/169300066-d4063af3-5546-4f7d-a42f-a99126d2373b.png)

### Profile Page ###
In this page the user can change many options of their profile, or even delete their account:

![image](https://user-images.githubusercontent.com/73992493/169300331-4918aae0-1b60-4fb2-a60c-6d644aa2b445.png)

![image](https://user-images.githubusercontent.com/73992493/169300384-ca4542f9-ce79-442c-b38e-5092d32062f7.png)

### Application Page ###
This is the most important page of our project, here we have a screen with all the documents that the user uploaded an can download:

![image](https://user-images.githubusercontent.com/73992493/169300561-67754fdc-afde-4e81-997b-a4b80738a0fa.png)

![image](https://user-images.githubusercontent.com/73992493/169300619-878d63c0-d094-4cc5-9a93-2bf6231276e4.png)

The Shared Files, and the options to upload, share or delete resources:

![image](https://user-images.githubusercontent.com/73992493/169300878-a1cbb7a2-0aff-42e5-ab29-6400aaf69b73.png)

The user can click with the right click to open a contextual menu to make all operations that are in the buttons, so he can select the way he wants to use our application:

![image](https://user-images.githubusercontent.com/73992493/169300744-30e9de67-49c1-4a33-ace4-1cf0a005cb21.png)

![image](https://user-images.githubusercontent.com/73992493/169301056-cb3cbb1c-fea7-4de7-b5c3-46b031eb2717.png)

For everly option will open a modal box to manage the appropiate operation:

![image](https://user-images.githubusercontent.com/73992493/169300947-79452474-2bef-4772-8052-9131a21c1aef.png)

And will guide the user like the register and login pages:

![image](https://user-images.githubusercontent.com/73992493/169301157-9fd309b1-6737-4913-8c94-f73d75c6fccd.png)

The Share Files Page we can see all the files that have been shared with us with a similar use of the Cloudware application page:

![image](https://user-images.githubusercontent.com/73992493/169301860-90919145-a2db-4dda-beaa-0fa5c0568bd9.png)

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
