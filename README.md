# blog-django
Simple Django blogging app

 ![blog](https://github.com/ncunx/blog-django/blob/master/pics/main.png)

For more pictures, see `pics` directory. See also `https://ncunx.pythonanywhere.com/` for the deployed version.

Features
--------

1. User authorisation and registration
2. Basic user permissions: admin, editor, normal.

	[//]: # "- Normal users can view posts and comment (after logging in)."
	- Editors can add posts, update/delete the existing ones for which they have suitable
	  permissions/ownership.
	- admin is superuser as usual.
3. Facebook comments
4. Tags
5. Search, year/month archives, sort by post author, category, tags.
6. Basic REST API provided by Django REST framework (available at `localhost:8000/api/`) 

Main requirements
------------

1. `python` 3.5, 3.6, 3.7
2. `Django` 2.1.3

This project also uses a few external packages (see `requirements.txt` file for details). 
For instance, tags support is provided by [django-taggit](https://github.com/alex/django-taggit).


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

5. For testing purposes several accounts are created. Credentials: `(admin, passwordadmin), (userN, passworduserN)`, where `N=1,2,3,4`.