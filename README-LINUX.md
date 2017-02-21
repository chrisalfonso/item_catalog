# Linux Server Configuration
This configures an Amazon Web Services (AWS) virtual server to host the Item Catalog application.

## Access
- 35.164.200.0
- [ec2-35-164-200-0.us-west-2.compute.amazonaws.com](http://ec2-35-164-200-0.us-west-2.compute.amazonaws.com)

## Software
- [Apache HTTP Server](http://httpd.apache.org/docs/2.2/) (serves item catalog as a WSGI application)
- [Flask](http://flask.pocoo.org/)
- [Git](https://help.ubuntu.com/lts/serverguide/git.html)
- [OAuth2](https://developers.google.com/identity/protocols/OAuth2) (provides authentication via Google API)
- [PostgreSQL 9.3](https://www.postgresql.org/docs/9.3/static/index.html)
- [SQLAlchemy](http://www.sqlalchemy.org/) (Python ORM)
- [virtualenv](http://flask.pocoo.org/docs/0.12/installation/)

## Configuration
1. Create ```grader``` user with sudo access
  * ```sudo adduser grader```
  * ```vi /etc/sudoers.d/grader```
  * In the grader config file, set ```grader ALL=(ALL) ALL```

2. Enable key-based authentication
  * Generate key on local machine ```ssh-keygen```
  * Copy key content from local machine ```cat ~/.ssh/udacitygrader.rsa```
  * Paste content to authorized_keys on server ```sudo vi ~/.ssh/authorized_keys```

3. Update all installed packages
  * ```sudo apt-get update```
  * ```sudo apt-get upgrade```

4. Disable remote login for root user
  * ```sudo vi /etc/ssh/sshd_config```
  * ```PermitRootLogin no```
  * ```sudo service ssh restart```

5. Change SSH port from 22 to 2200
  * ```sudo vi /etc/ssh/sshd_config```
  * Change ```Port 22``` to ```Port 2200```
  * Restart SSH ```sudo service ssh restart```
  
6. Allow incoming connections only to ports 2200, 80, and 123
  * ```sudo ufw default allow outgoing```
  * ```sudo ufw default deny incoming```
  * ```sudo ufw allow 2200```
  * ```sudo ufw allow 80```
  * ```sudo ufw allow 123```
  * ```sudo ufw enable```
  * ```sudo ufw status```
  
7. Configure local timezone to UTC
  * ```sudo dpkg-reconfigure tzdata```
  * Select ```UTC``` from the menu

8. Install and configure Apache to serve a Python mod_wsgi application.
  * ```sudo apt-get install apache2```
  * ```sudo apt-get install libapache2-mod-wsgi```
  * Enable mod_wsgi
    * ```sudo a2enmod wsgi ```
  * Create application directory
    * ```sudo mkdir /var/www/myapps```
  * Create WSGI file
    * ```sudo vi /var/www/myapps/myapps.wsgi```
  * Create configuration file
    * ```sudo vi /etc/apache2/sites-available/myapps.conf```
  
9. Install and configure PostgreSQL
  * ```sudo apt-get install postgresql```
  * Set password for default 'postgres' user
    * ```sudo -u postgres psql postgres```
    * ```\password mypassword```
  * Disable remote connections
    * ```sudo vi /etc/postgresql/9.1/main/pg_hba.conf```
    * Below "Database administrative login by Unix domain socket", ensure line is uncommented and refers to "local"
  * Create 'catalog' user with limited permissions to database
    * ```sudo -u postgres createuser -D -A -P catalog```
    * ```sudo -u postgres createdb -O catalog catalogdb```
    * Login as postgres user to catalogdb database ```sudo -u postgres psql catalogdb```
    * ```GRANT UPDATE ON category TO catalog;```
    * ```GRANT UPDATE ON item TO catalog;```
    * ```GRANT UPDATE ON items TO catalog;```
    * ```GRANT UPDATE ON user TO catalog;```

12. Clone and configure Item Catalog app
  * Clone Item Catalog app
    * ```cd /var/www/myapps```
    * ```git clone https://github.com/chrisalfonso/item_catalog.git```
  * Create virtual environment and install required software
    * ```sudo virtualenv venv```
    * ```source venv/bin/activate```
    * ```sudo pip install flask```
    * ```sudo pip install sqlalchemy```
  * Update configuration file
  
  * Rename application.py to __init__.py
  
  * Edit __init__.py
    * Update client secrets path to ```/var/www/myapps/item_catalog/client_secrets.json```
    * Update database connection to ```postgresql://catalog:udacitygrader@localhost/catalogdb```
    
  * Edit database_setup.py
    * Update database connection to ```postgresql://catalog:udacitygrader@localhost/catalogdb```
    
  * Enable site
    * ```sudo a2ensite item_catalog```
    
  * Restart Apache
    * ```sudo service apache2 restart```

## Resources
- [How do I disable SSH remote login as root](http://askubuntu.com/questions/27559/how-do-i-disable-remote-ssh-login-as-root-from-a-server)
- [UFW](https://help.ubuntu.com/community/UFW)
- [mod_wsgi (Apache)](http://flask.pocoo.org/docs/0.12/deploying/mod_wsgi/)
- [How To Deploy a Flask Application on an Ubuntu VPS](https://www.digitalocean.com/community/tutorials/how-to-deploy-a-flask-application-on-an-ubuntu-vps)
- [Cloning a Repository](https://help.github.com/articles/cloning-a-repository/)
- [PostgreSQL](https://help.ubuntu.com/community/PostgreSQL)
- [How to install and use PostgreSQL](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-14-04)
- [How to secure PostgreSQL on an Ubuntu VPS](https://www.digitalocean.com/community/tutorials/how-to-secure-postgresql-on-an-ubuntu-vps)
- [How To Use Roles and Manage Grant Permissions in PostgreSQL on a VPS](https://www.digitalocean.com/community/tutorials/how-to-use-roles-and-manage-grant-permissions-in-postgresql-on-a-vps--2)

## Known Issues
Intermittent 'Internal Server Error' accessing website on Amazon Web Services. Refreshing the page eventually clears the error. Apache error log reports the following:

> InvalidRequestError: This Session's transaction has been rolled back due to a previous exception during flush. To begin a new transaction with this Session, first issue Session.rollback(). Original exception was: (psycopg2.IntegrityError) duplicate key value violates unique constraint "user_pkey"

Intermittent SSH disconnection to server on Amazon Web Services. Occurs occassionally when reviewing log files (using ```tail```) or reading files (using ```cat```). Error reported in terminal:

> packet_write_wait: Connection to 35.164.200.0 port 2200: Broken pipe
