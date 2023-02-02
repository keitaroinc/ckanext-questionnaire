[![Tests](https://github.com/blagojabozinovski/ckanext-questionnaire/workflows/Tests/badge.svg?branch=main)](https://github.com/blagojabozinovski/ckanext-questionnaire/actions)

# ckanext-questionnaire

With this extension CKAN sysadmin can set up a survey for the all the users. The Questions in the survey can be added or deleted by the sysadmin and the answers can be set up to be as text, choose one or choose multiple options. The Questions are the same for all the users. 

## Requirements

Compatibility with core CKAN versions:

| CKAN version    | Compatible?   |
| --------------- | ------------- |
| 2.6 and earlier | not tested    |
| 2.7             | not tested    |
| 2.8             | not tested    |
| 2.9             | Yes           |


## Installation

To install ckanext-questionnaire:

1. Activate your CKAN virtual environment, for example:

     . /usr/lib/ckan/default/bin/activate

2. Clone the source and install it on the virtualenv

    git clone https://github.com/keitaroinc/ckanext-questionnaire.git
    cd ckanext-questionnaire
    pip install -e .
	pip install -r requirements.txt

3. Add `questionnaire` to the `ckan.plugins` setting in your CKAN
   config file (by default the config file is located at
   `/etc/ckan/default/ckan.ini`).

4. Create the database tables running:

ON CKAN >= 2.9:

    ckan -c /path/to/ini/file questionnaire init-db

ON CKAN <= 2.8:

    paster questionnaire init-db -c ../path/to/ini/file


5. Restart CKAN. For example if you've deployed CKAN with Apache on Ubuntu:

     sudo service apache2 reload


## Config settings

When logging in the user is redirected to the Questions page available on the User Dashboard page.
You need to add the following setting in your ckan.ini file:

	route_after_login = "user.me"


## Developer installation

To install ckanext-questionnaire for development, activate your CKAN virtualenv and
do:

    git clone https://github.com/keitaroinc/ckanext-questionnaire.git
    cd ckanext-questionnaire
    python setup.py develop
    pip install -r dev-requirements.txt


## Tests

To run the tests, do:

    pytest --ckan-ini=test.ini


## License

[AGPL](https://www.gnu.org/licenses/agpl-3.0.en.html)
