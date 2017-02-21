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
  * in the grader config file, set ```grader ALL=(ALL) ALL```

2. Enable key-based authentication
  * generate key on local machine ```ssh-keygen```
  * copy key content from local machine ```cat ~/.ssh/udacitygrader.rsa```
  * paste content to authorized_keys on server ```sudo vi ~/.ssh/authorized_keys```

3. Update all installed packages
  * ```sudo apt-get update```
  * ```sudo apt-get upgrade```

4. Disable remote login for root user
  * ```sudo vi /etc/ssh/sshd_config```
  * ```PermitRootLogin no```
  * ```sudo service ssh restart```

5. Change SSH port from 22 to 2200
  * ```sudo vi /etc/ssh/sshd_config```
  * change ```Port 22``` to ```Port 2200```
  * sudo service ssh restart
  
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
  * select ```UTC``` from the menu

8. Install and configure Apache to serve a Python mod_wsgi application.
  * ```sudo apt-get install apache2```
  * create application directories
    * ```sudo mkdir /var/www/myapps```
    * ```sudo mkdir /var/www/myapps/item_catalog```
  * create WSGI file
    * ```sudo vi /var/www/myapps.wsgi```
  
9. Set password for default 'postgres' user

10. Disable remote connections to database

11. Create 'catalog' user with limited permissions to 'catalogdb' database

12. Clone and configure Item Catalog app
  * create app directory
    * ```sudo mkdir /var/www/myapps```
  * clone Item Catalog app
    * ```cd /var/www/myapps```
    * ```git clone....```
  * create virtual environment and install required software
    * ```virtualenv...```
    * ```sudo apt-get install flask```
    * ```sudo apt-get install sqlalchemy```
  * enable site
    * ```a2enmod item_catalog```

## Resources
- [How do I disable SSH remote login as root](http://askubuntu.com/questions/27559/how-do-i-disable-remote-ssh-login-as-root-from-a-server)
- [UFW](https://help.ubuntu.com/community/UFW)
- [PostgreSQL](https://help.ubuntu.com/community/PostgreSQL)
- [How to install and use PostgreSQL](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-14-04)
- [How to secure PostgreSQL on an Ubuntu VPS](https://www.digitalocean.com/community/tutorials/how-to-secure-postgresql-on-an-ubuntu-vps)

## Known Issues
Intermittent 'Internal Server Error' accessing website on Amazon Web Services. Refreshing the page clears the error and renders the appropriate webpage. Apache error log reports the following:

> InvalidRequestError: This Session's transaction has been rolled back due to a previous exception during flush. To begin a new transaction with this Session, first issue Session.rollback(). Original exception was: (psycopg2.IntegrityError) duplicate key value violates unique constraint "user_pkey"

Intermittent SSH disconnection to server on Amazon Web Services. Occurs occassionally when reviewing log files or reading ('cat') files. Error reported in terminal:

> packet_write_wait: Connection to 35.164.200.0 port 2200: Broken pipe
