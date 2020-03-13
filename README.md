# pluto
an app that enables developers keep track of their side projects and ideas

To run this app, you will need the postgresql admin for viewing tables and other database related information. Get that at <a href='https://postgresql.org' target='blank'>postgresql.org</a>.
You also need python installed globally, get that at <a href='https://python.org'>python.org</a>.
Get mailgun credentials for the emails functionalities at <a href='https://mailgun.org' target='blank'>mailgun.org</a>

Clone this repo by running <b>git clone https://github.com/olamileke/pluto.git</b> in a directory of your choice on your system. Follow the instructions found <a href="https://flask.palletsprojects.com/en/1.1.x/installation/">here</a> to install the virtual environment in which app dependencies will be installed.

Still in your directory, run <b>venv\scripts\activate</b> to activate the virtual environment. Then, run <b>pip install requirements.txt</b> to install all the app dependencies. 

In the postgresql admin, create a database for the application (preferably named pluto). Then, fill in the relevant credentials in the config.py file.

Next, run the following commands
<b>python manage.py db init</b> to create the migrations subfolder
<b>python manage.py db migrate</b> to create the migration based on the models.py file in the /Pluto subdirectory
<b>python manage.py db upgrade</b> to run the migration and create the database schema for the application

Finally, execute <b>python -m flask run</b> to run the application. Access it at localhost:5000 in your browser.
To stop app execution, run Ctrl + C in the terminal.
Run deactivate to close the virtual machine.
