# blog-django
Simple Django blogging app

 ![blog](https://github.com/ncunx/blog-django/blob/master/pics/main.png)

For more pictures, see `pics` directory.

Features
--------

1. User authorisation and registration; custom profiles.
2. Basic user permissions: admin, editor, normal.
	- Normal users can view posts and comment (after logging in).
	- Editors have Normal users permissions but also can add posts, update/delete the existing ones for which they have suitable permissions.
	- admin is superuser as usual.
3. Facebook comments
4. Tags
5. Search, year/month archives, sort by post author, category, tags.
6. Basic REST API provided by Django REST framework (available at `localhost:8000/api/`) 

Main requirements
------------

1. `python` 3.5+
2. `Django` 2.0.7

This project also uses a few external packages (see `requirements.txt` file for details). 
For instance, processing images is done via [Pillow](https://github.com/python-pillow/Pillow) and tags via [django-taggit](https://github.com/alex/django-taggit).


Usage
-----

1. Create a new directory and change to it:

`mkdir blog-django && cd blog-django`

2. Clone the repository:

`git clone https://github.com/ncunx/blog-django.git .`

3. Set up a virtual environment and activate it:

`python3 -m venv <preferred_name> && source <preferred_name>/bin/activate`

4. Install required packages:

`pip3 install -r requirements.txt`

The project is all set up. Run a local server with

`python3 manage.py runserver`

The blog should be available at `localhost:8000`.
