# Goals

- Take your first steps in backend development with Python
- Create, from scratch, your first web application
- Learn to structure a project within this framework
- Get to know Django and place it in the Python ecosystem

## Starting
Install Django\
`pip install django` \
Start proyect\
`django-admin startproject premios` 

## Crear un entorno virtual

```zsh
python3 -m venv venv
source ./venv/bin/activate
```
## Files

- `manage.py`: Shows the different commands available to make the project work.

- `_init_.py` : Indicates that the folder is a package containing the web application files.

- `asgi.py` / `wsgi.py`: Used to deploy the application.

- `settings.py`: Contains all the project configuration information such as language, time zone, databases, etc.

- `urls.py`: Where the addresses with which we can move through the project are worked, such as the admin or user route.

# Premios Platzi App

Create a app called "polls"
```zsh
python3 manage.py startapp polls
```

Inside main folder: "premios", there are two folder "premios" y "polls"
The main project is a container for different applications, so each application has its `urls.py` file.
The file that is contained in the main project folder has to include the files of the other applications

**File *urls.py* proyect folder:**
```py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("polls/" ,include("polls.urls"))
]
```

The new app *polls* must be added to the project configuration file:

**File *settings.py* proyect folder:**
```py
INSTALLED_APPS = [
    "polls.apps.PollsConfig",
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
```
## Models
**File *models.py* folder polls:**

```py
- Create your models here.

- name´s models always singular

class Question(models.Model):

    # id - Automatically by Django 
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")

class Choice(models.Model):

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
```
### Every time you make a change you must do migration

In the console (we have to have the virtual environment active and be located in the parent folder)
```zsh
python3 manage.py makemigrations polls
python3 manage.py migrate
```
The concept *migration* corresponds to changing information or software from one system to another. In this case we transform those written in python into a relational database.

A file *0001_initial.py* is created in which django describes the entire creation of the tables in the database, this is where the ORM concept is used.

Django takes the programming we did in the *models.py* file and converts it to tables in the database we are using (in this case sqlite3)

When methods are added to classes it is not necessary to make migrations.

### ORM - Object Relational Mapping

 It is the way to replicate the structure of a relational database with object-oriented programming.

>> Using an ORM we can operate on the database taking advantage of the characteristics of object orientation, such as inheritance and polymorphism.

The databases are made up of tables and each table obtains the data related to each entity. It is possible to convert these databases into a python file that contains the object-oriented programming representation.

The tables correspond to models (which are expressed as classes), the columns will correspond to attributes of those classes and the data types of each column will correspond to classes linked to the attributes of the objects.

## Views
>DRY: Don´t Repeat Yourself

A model is always created that is displayed in a template that in turn appears in a view (in this project we have the Question and Choice models) 

- Index view: Show all questions
- Detail view: Show the question with the answers
- Vote view: Count the vouts
- results view: Show the vote for each options

### Administrator

To start using the administrator you must create a username and password:
`python3 manage.py createsuperuser`
Great care must be taken with the security of this data, since if it is exposed it can compromise the entire application.

Now, the created models must be made available to the administrator:
*In the *admin.py* file in the polls folder:*
```py
from .models import Question

admin.site.register(Question)
```

Using the address http://127.0.0.1:8000/admin/ You can enter the administration panel.


  
### Formularios

`{% csrf_token %}`: This tag adds a security token to prevent form hacking attacks
