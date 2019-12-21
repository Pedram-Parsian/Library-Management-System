# Library Management System
[![Open Source Love](https://badges.frapsoft.com/os/v1/open-source.svg?v=103)](https://github.com/ellerbrock/open-source-badges/)
[![GPL Licence](https://badges.frapsoft.com/os/gpl/gpl.svg?v=103)](https://opensource.org/licenses/GPL-3.0/)

This program has been started on 20 Sep 2019, from an 15-hour code challenge!

We will choose a name for it later!

## Installation Guide
##### Step 1:
Create a virtual environment, activate it and install the project requirements from the `requirements.txt` file:
```python
pip3 install -r requirements.txt  # or pip install ...
```
##### Step 2:
Login into your PostgreSQL environment and create a database called `lms` (or change database name in settings), alongside with a user that has full privileges on the database.
##### Step 3:
Change production email back-end as you wish in `lms/settings/production.py`; the password (or app password) must be set in `lms/settings/secrets.py` module.
##### Step 4:
Inside the `lms/settings/` directory, create a module called `secrets.py` containing:
```python
_SECRET_KEY = 'Some long-enough random string'

_DB_PASSWORD = 'Your PostgreSQL password here'

_RECAPTCHA_PUBLIC_KEY = 'Your Google public API key here'

_RECAPTCHA_PRIVATE_KEY = 'Your Google Private API key here'

_EMAIL_HOST_PASSWORD = 'Password (or app password) of your production email'
``` 
##### Step 5:
adjust the timezone in `lms/settings/base.py` based on your location.


## Deployment Tips
- Currently, only _books_ are supported and handled by the application, not **digital items** (such as e-books, DVD, etc.)


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[GNU GPLv3](https://opensource.org/licenses/GPL-3.0)