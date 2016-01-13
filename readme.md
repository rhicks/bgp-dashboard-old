BGP Dashboard
=============

A "realtime" web view of your BGP network

- Who do I peer with?
- How many routes do I receive from my peers?
- Who do I use for tranist?
- What AS path does a prefix take out of my network?
- How many routes and autonomous systems do I see?


How it works
---------
> Work in progress and many things are broken or changing. This is alpha code.

###### Read data from the output of Cisco 'show ip bgp' and 'show ipv6 unicast' commands
- Currently a manual process running outside of the bgp-dashboard application.  
- Setup a rancid/clogin, or similar cli automation tool, reoccurring cron job to grab the data and save locally as text.

###### Store the data into a SQLite database
- After the 'show ip bgp' data is saved locally, run bgp2sql.py from the scripts folder to build/update the SQLite database.
- Again, best to automate this via a cron job at regular intervals.

###### Start the Flask application and view the data
- [Flask](http://flask.pocoo.org/), [SQLAlchemy](http://flask-sqlalchemy.pocoo.org/), [Bootstrap](http://getbootstrap.com/), and various JavaScript libraries are used to present the data via the web


Screenshots
---------
(TODO) - Add screenshots



Requirements
---------
```
Python 3.4+
dnspython3
docopt
Flask
Flask-SQLAlchemy
```

Install
---------
```
$ git clone https://github.com/rhicks/bgp-dashboard.git
$ cd bgp-dashboard
$ pip3 install -r requirements.txt
...(TODO) - Create the database
...(TODO) - Setup cron jobs
$ python3 web/hello.py (TODO) - Change the name of the app
```

Development Workflow
---------
```
$ git clone https://github.com/rhicks/bgp-dashboard.git
$ cd bgp-dashboard
$ [sudo] pip install virtualenv
$ [sudo] pip install virtualenvwrapper # Read virtualenvwrapper install instructions for shell integration
$ mkvirtualenv --python=`which python3` bgp-dashboard
$ workon bgp-dashboard
$ pip install -r requirements.txt
```

Todo
---------
- Use [netmiko](https://github.com/ktbyers/netmiko) to automate the download of BGP data from routers
- Investigate the use of BMP to trigger updates
- Add ability to search for ASN/IP and find the next hop and full AS path
- Add support for other router vendors
- Add ability to monitor ASN or Prefix changes (next hop IP, next hop ASN, AS path, etc...)
- Add alerting for monitored ASN/Prefixes (email, pager, etc...)
