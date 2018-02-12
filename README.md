# django-podcast-host
A simple Django project for hosting podcasts using Django REST framework

## What it does

This project provides an API for creating podcasts, as well as the ability to consume the podcasts via an RSS feed or a (super-basic) web front-end. The aim of this project was to create a demo of a minimal useful API using Django REST framework, but it posed some interesting challenges:

- using slugs instead of primary keys in URIs
- authenticating users and controlling access
- foreign key relationships
- handling file uploads from users

## How to install locally

Assuming you already have Python3 and the ability to create virtual environments installed, first clone this repository from github and `cd` into it:

    git clone https://github.com/esonderegger/django-podcast-host.git
    cd django-podcast-host

Then create a virtual environment for this project (I use the following commands, but there are several ways to get the desired result):

    python3 -m venv ~/.virtualenvs/podcasthost
    source ~/.virtualenvs/podcasthost/bin/activate

Next, install this project's dependencies

    pip install -r requirements.txt

Then, make and run the required database migrations

    python manage.py makemigrations
    python manage.py migrate

Finally, run the development web server:

    python manage.py runserver

## How to use

If the local installation was successful, you should be able to go to `http://localhost:8000/` and see a minimal web page. Click the "Sign up" link, and you will see a basic form. Enter a username and password according the instructions provided, and it should log you in and redirect you to `http://localhost:8000/api/`

Next, use the form fields (or `curl` or a REST client like Postman if you prefer) to enter data for a sample podcast and Click `POST`. You should see the JSON representation of the podcast you just created. Take note of the `slug` field. This is how you will access this podcast in future requests.

Next, go to `http://localhost:8000/api/<podcast_slug>`. You should see all of the form fields from the previous page, but with a `PUT` button for you to edit any of the fields in this entity and a `DELETE` button if you would like to delete this podcast.

Next, go to `http://localhost:8000/api/<podcast_slug>/items`. You should see an empty list and a set of form fields for creating a new episode for this podcast. Fill in the fields (note: enclosure is required) and click `POST`. Take note of the `slug` field returned in this response.

Next, go to go to `http://localhost:8000/api/<podcast_slug>/<episode_slug>`. You should see all of the form fields from the previous page, but with a `PUT` button for you to edit any of the fields in this entity and a `DELETE` button if you would like to delete this episode.

Finally, go to `http://localhost:8000/api/<podcast_slug>/categories` to edit the categories for this podcast. They should come from [this list](https://help.apple.com/itc/podcasts_connect/#/itc9267a2f12) although this project does not enforce this presently. For example, to list the podcast as being in the "Government & Organizations -> Non-Profit" category, enter "Non-Profit" for `name` and "Government & Organizations" for `parent_name`. and click Post.

Now, you should be able to go to `http://localhost:8000/` and see your new podcast listed. Click on its link and you should be taken to `http://localhost:8000/<podcast_slug>`. If you view the source code for the page, you should see something like `<link rel="alternate" type="application/rss+xml" title="<Podcast title>" href="http://localhost:8000/<podcast_slug>/feed.xml">` in the head tag. If you download the feed from `http://localhost:8000/<podcast_slug>/feed.xml` and open it in an xml/rss reader, you should see the RSS representation of your podcast.

## TODOs

- Limit categories to only the ones allowed by iTunes. Ideally this category list would live in a database that is only editable by an admin user. This could require getting a many to many relationship to work. It might also be possible to do this with a `MultipleChoiceField`.
- use ffprobe to get duration and type information from uploaded enclosures
- use ffmpeg to re-encode uploaded media according to recommended specifications. Both this and using ffprobe would require having non-python dependencies and would also need to work asynchronously after the uploaded file has been saved.
- make better front-ends for everything
- improve the sign-up/login flow
- improve error handling for unauthenticated podcast creation
- use Django forms to create front-end for creating/editing podcasts
- write tests
