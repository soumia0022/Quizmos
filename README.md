# Quizmos
Polling website for the SEG Major Group Project.

## Team members

The members of the team are:

- Amina Ali
- Rashida Begum
- Soumia Bekhli
- Alishba Faisal
- Leyli Jalilova
- Eeshal Malik
- Marium Rukiya

## Project structure

The project is called `Quizmos`. Our system has the following apps:

- user_management
- poll_management
- question_management
- response_management
- analytics
- ui_components

## Deployed version of the application

The deployed version of the application can be found at http://ec2-13-48-203-183.eu-north-1.compute.amazonaws.com/

## Installation instructions

Our application has been developed using the latest versions of Python and Django.

To begin, set up and activate a local (virtual) development environment. From the root of the project:

```
$ python3.10 -m venv venv
$ source venv/bin/activate
```

Install all required packages:

```
$ pip3 install -r requirements.txt
```

Then, migrate the database:

```
$ python3 manage.py migrate
```

Seed the development database with:

```
$ python3 manage.py seed
```

Run all tests with:

```
$ python3 manage.py test
```

All tests should pass. Check the coverage with:

```
$ coverage run manage.py test
$ coverage html
```
You can open this file in your web browser.


Run the server with:
```
$ python3 manage.py runserver
```

To use the real-time functionality, you will need to run redis.
