PICHR
BMI 210 2014' - '15
Final Project 
### Team
Emily Ye
Vincent D’Andrea
Kapil Kanagal
Leslie Kurt
Richard Tang

## Getting Started

### Dependencies

For best results, make sure you have at least:

* Python 2.7
* Django 1.5


### Installing the Application

    cd pichr/                                     # changes directory to project after initial git clone
    python manage.py syncdb                       # sets up django database
    python manage.py migrate pichr                # migrates any south migrations
    python manage.py loaddata SCTInfo.json
    python manage.py loaddata instances.json

Application will be running at [http://localhost:8000](http://localhost:8000) after running one of the two commands:

    python manage.py runserver                                        # Normal way
