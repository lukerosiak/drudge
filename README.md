DRUDGE REPORT TRACKER by Luke Rosiak @lukerosiak www.lukerosiak.info


Hit drudgereport.com every 5 minutes and parse its articles into a PostgreSQL database.


It also bakes an HTML file showing analysis of top news outlets, etc. to S3, so you'll need to put in your AWS credentials in credentials.py or just have it store a file locally.


Live version is at www.lukerosiak.info/drudge.html


Uses Django for a tiny amount of convenience, but probably winds up only making it more complicated than it needs to be. You have to use PostgreSQL as the backend because of some hard-coded SQL.

Rename settings_example.py and credentials_example.py to settings.py and credentials.py and set your settings, "pip install -r requirements.txt", create a psql db called drudge with "createdb drudge" and run python manage.py syncdb


Then set it up to to run every 5 minutes thusly (on Linux):

crontab -e

/5 * * * * python /[path]/manage.py scraper


LICENSE: CC-0 -- do whatever you want with it.
