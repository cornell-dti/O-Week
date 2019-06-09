O-Week Backend
======
#### Contents
  - [About](#about)
  - [Getting Started](#getting-started)
  - [Documentation](#documentation)
  - [Contributors](#contributors)
  
## About
The backend for the O-week app, to help incoming freshmen during their first week as a Cornell student. The database should be online [here](https://oweekapp.herokuapp.com); edit configurations with the [Heroku dashboard](https://dashboard.heroku.com/apps/oweekapp).
- [Android](https://github.com/cornell-dti/o-week-android)
- [iOS](https://github.com/cornell-dti/events-manager-ios)


## Getting Started
You will need **Python 3.6** to run the latest version of this app, which uses Django. Django can be installed using python's inbuilt _pip_ function. 

You might want IntelliJ IDEA as your source code editor.

Note: If `python` is Python 2 by default on your computer instead of Python 3, substitute `pip` and `python` with `pip3` and `python3`.

#### Install requirements
`pip install -r requirements.txt`

#### Create environment variables
Create a file named `.env` in the main directory. Fill it with variables with secret parameters copied from Heroku Config, such as `SECRET_KEY` or `BUCKETEER_AWS_ACCESS_KEY_ID`. **Never** commit this file and push to GitHub; if you do, contact the developer leads to figure out how to revert the changes and change the exposed secret values.

#### Database update
If the database has been updated (changes were made to `models.py`), then we need to reflect those changes in MySQL. Run the following commands:
```console
python manage.py makemigrations --run-syncdb
python manage.py migrate
```

#### Start the local server
`python manage.py runserver`

The website will be located at `127.0.0.1:8000`.

## Documentation
All editing requires logging into the [admin page](https://oweekapp.herokuapp.com/admin/). Credentials are provided by the DTI LastPass on a need-to-know basis; ask the developer leads for access.

Editing resources, dates, and categories can be directly done through the admin panel. Editing events and images can be done in bulk through [bulk add_events](https://oweekapp.herokuapp.com/flow/bulk_add_event/) and [bulk_image](https://oweekapp.herokuapp.com/flow/bulk_image/). _TODO further document format of .csv uploads_

The most important app APIs are:

### Version
[https://oweekapp.herokuapp.com/flow/version/<local_version>](https://oweekapp.herokuapp.com/flow/version/0)

Provides the updated/deleted events and categories.

#### Parameters
Replace <local_version> with the version number last seen. If this is the first time the app has called this URL, use 0 as the version number.

#### Format
The response has 3 main keys: **version**, **events**, **categories**. 

**version** is the database's version. Store on the device after this version has been processed. 

**events** is further divided into two key-value pairs: **changed** and **deleted**.

**changed** is a list of the events that have been added or modified. This is not a 
list of pks but instead a list of event objects in jSON form.

**deleted** is a list of pks of the event deleted between local_version and the newest version. Note: an event object in this list many not be in the app's database at all.

**categories** is similar to events but for category objects.


### Event
Event object returned by the [Version API](#version).

#### Format
`{"pk": 117, "name": "Transfer and Exchange Students Orientation Leader Meeting #1", "description": "Welcome transfer students! Welcome exchange students!", "additional": "## Meet your OL at one of the following locations ## ____ Architecture, Art, and Planning # Lobby, Goldwin Smith Hall ____ Arts and Sciences # 165 McGraw Hall", "location": "Locations In Additional Information", "place_ID": "ChIJndqRYRqC0IkR9J8bgk3mDvU", "category": 14, "start_date": "2018-08-17", "end_date": "2018-08-17", "start_time": "20:00:00", "end_time": "21:30:00", "required": false, "category_required": true}`

**pk**: The private key, a unique identifier of the event.
**category**: The pk of the category this event belongs to.
**date**: The date in which this event BEGINS. If this event crosses over midnight, the date is that of the 1st day.
**categoryRequired**: True if this event is required by its category. For example, the event above is not required for all, but for transfer students, and the event is in the transfer students category.
**additional**: Additional information to display in a special format. Formatted like so: `## HEADER ## ____BULLET # INFO ____BULLET # INFO`. The chunks are `## HEADER ##`, `____BULLET`, and `# INFO`.


### Category
Category object returned by the [Version API](#version).

#### Format
`{"pk": 1, "category": "The Greeks", "description": "Test"}`
**pk**: The private key, a unique identifier of the category.


### Images
[https://oweekapp.herokuapp.com/flow/event/<event_pk>/image](https://oweekapp.herokuapp.com/flow/event/117/image)

The image of an event.

#### Parameters
Replace <event_pk> with the **pk** of the event. The above link may be broken if the event no longer exists or the image has been deleted.


## Contributors
##### 2019
**David Chu** - Developer Lead
##### 2018
**Arnav Ghosh** - Back-End Developer
##### 2017
**Arnav Ghosh** - Back-End Developer
##### 2016
**Arnav Ghosh** - Back-End Developer

We are a part of the O-Week/Events team within **Cornell Design & Tech Initiative**. For more information, see our website [here](https://cornelldti.org/).
<img src="https://raw.githubusercontent.com/cornell-dti/design/master/Branding/Wordmark/Dark%20Text/Transparent/Wordmark-Dark%20Text-Transparent%403x.png">

_Last updated **6/9/2019**_.