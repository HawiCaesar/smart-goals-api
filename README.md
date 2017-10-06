[![Build Status](https://travis-ci.org/HawiCaesar/smart-goals-api.svg?branch=develop)](https://travis-ci.org/HawiCaesar/smart-goals-api)
[![Coverage Status](https://coveralls.io/repos/github/HawiCaesar/smart-goals-api/badge.svg?branch=develop)](https://coveralls.io/github/HawiCaesar/smart-goals-api?branch=develop)
[![Code Climate](https://codeclimate.com/github/HawiCaesar/smart-goals-api/badges/gpa.svg)](https://codeclimate.com/github/HawiCaesar/smart-goals-api)
[![Issue Count](https://codeclimate.com/github/HawiCaesar/smart-goals-api/badges/issue_count.svg)](https://codeclimate.com/github/HawiCaesar/smart-goals-api)
# Smart Goals API

What would you like to do in the next few years? Climbs a mountain? Learn to
ride a bike? It's important to keep track of what you have already done and
what you are yet to achieve.
Smart Goals allows you to register and achieve all these feats and also
allows you to tick off what you have done.

## Based on
This app is built on [Smart Goals](https://github.com/HawiCaesar/smart-goals)
It is a continuation only this will use a RESTFUL API and database as opposed to python data structures like lists and dictionaries as data stores

## RESTFUL API features
Create Read Update Delete bucketlist & Items

## Installation
After cloning the repo into your local machine

#### Create a Virtual Environment and Wrapper
```
$ export WORKON_HOME=~/Environs
$ export VIRTUALENVWRAPPER_PYTHON=/usr/local/bin/python3

$ cd smart-goals-api
$ virtualenv sm-goal-api

```

### API Dependencies
Install all package requirements in your python virtual environment.
```
pip install -r requirements.txt
```

## Tests
To run tests

```
nosetests tests/
```
Coverage Tests
```
coverage run -m unittest discover && coverage report
```
## Documentation
Follow this [link](http://docs.smartgoalsapi.apiary.io/#) to check out the documentation

## Routes
Endpoint | Description
------------ | -------------
POST /auth/register | Register user. Request should have name and password in form data.
POST /auth/login | Login user. Session token is valid for 30 minutes.
POST /auth/logout | Logout user.
POST /bucketlists/ | Create a new bucket list. Request should have desc in form data.
GET /bucketlists/ | List all the created bucket lists.
GET /bucketlists/<id> | Get single bucket list.
PUT /bucketlists/<id>| Update single bucket list. Request should have desc in form data.
DELETE /bucketlists/<id> | Delete single bucket list.
POST /bucketlists/<id>/items | Add a new item to this bucket list. Request should have goal in form data.
PUT /bucketlists/<id>/items/<item_id> | Update the bucket list completion status to true.
DELETE /bucketlists/<id>/items/<item_id> | Delete this single bucket list item.
GET /bucketlists?limit=5 | Get 5 bucket list records belonging to user.
GET /bucketlists?q=draw	| Search for bucket lists with phrase or words draw

## Hosted on Heroku
https://demo-smart-goals-api.herokuapp.com/

## Authors

* **Brian Hawi Odhiambo**

## Acknowledgements

* Python 3.6 Documentation
* Flask 0.12.2 Documentation
* Flask-Restful 0.3.6 Documentation
* PostgresSQL 9.5.7
* Various Internet resources and
Friends, [James Kinyua](https://github.com/JayKay24/), 
         [Herman Sifuna](https://github.com/mkiterian),
         [Josiah Nyarega](https://github.com/jmnyarega)
