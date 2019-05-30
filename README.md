# blog-django
Simple Django blogging app

 ![blog](https://github.com/kkosiba/blog-django/blob/master/pics/main.png)

For more pictures, see `pics` directory. See also `https://django-blog-1k4z.herokuapp.com/` for the deployed version. With sample content. For testing purposes several accounts are created. Credentials: `(X, Xpassword)`, where `X=anna, bob, chris`.

Features
--------
1. User authorisation and registration
2. Basic user permissions: admin, editor, normal.
	- Editors can add posts, update/delete the existing ones for which they have suitable
	  permissions/ownership.
	- admin is superuser as usual.
3. Facebook comments
4. Tags
5. Search, year/month archives, sort by post author, category, tags.
6. Basic REST API provided by Django REST framework (available at `/api`)

Main requirements
------------

1. `python` 3.5, 3.6, 3.7
2. `Django` 2.1.8
3. `PostreSQL` 11.1

This project also uses a few external packages (see `requirements.txt` file for details).
For instance, tags support is provided by [django-taggit](https://github.com/alex/django-taggit).


## How to set up

### Setup using Docker

The easiest way to get this project up and running is via [Docker](https://www.docker.com/). See [docs](https://docs.docker.com/get-started/) to get started. Once set up run the following command:

`docker-compose up`

It may take a while for the process to complete, as Docker needs to pull required dependencies. Once it is done, the application should be accessible at `0.0.0.0:8000`. 

### Manual setup

Firstly, create a new directory and change to it:

`mkdir blog-django && cd blog-django`

Then, clone this repository to the current directory:

`git clone https://github.com/kkosiba/blog-django.git .`


Next, one needs to setup database like SQLite or PostgreSQL on a local machine. This project uses PostgreSQL by default (see [Django documentation](https://docs.djangoproject.com/en/2.1/ref/settings/#databases) for different setup). This process may vary from one OS to another, eg. on Arch Linux one can follow a straightforward guide [here](https://wiki.archlinux.org/index.php/PostgreSQL).

The database settings are specified in `website/settings/local.py`. In particular the default database name is `BlogDjango`, which can be created from the PostgreSQL shell by running `createdb BlogDjango`.


Next, set up a virtual environment and activate it:

`python3 -m venv env && source env/bin/activate`

Install required packages:

`pip3 install -r requirements.txt`

Next, perform migration:

`python3 manage.py migrate --settings=website.settings.local`

The setup is complete. Run a local server with

`python3 manage.py runserver --settings=website.settings.local`

The blog should be available at `localhost:8000`.

## What's next?

At this point, one may want to create a superuser account, create the Editors group and add a few users to this group.