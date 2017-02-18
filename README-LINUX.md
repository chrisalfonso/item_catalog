# Linux Server Configuration

## Access
- 35.164.200.0
- [ec2-35-164-200-0.us-west-2.compute.amazonaws.com](http://ec2-35-164-200-0.us-west-2.compute.amazonaws.com)

## Installed Software
- Apache
- Git
- PostgreSQL

## Configurations
1. Create grader user with permission to sudo
  * ```sudo adduser grader```
  * ```usermod -aG sudo grader```

2. Enable key-based authentication
  * on local machine ```ssh-keygen```

3. Update all installed packages
  * ```sudo apt-get update```
  * ```sudo apt-get upgrade```

4. Change SSH port from 22 to 2200
5. Allow incoming connections only to the following ports 2200, 80, and 123
6. Configure local timezone to UTC
7. Serve WSGI application
8. Set password for default 'postgres' user
9. Disable remote connections to database
10. Create 'catalog' user with limited permissions to 'catalogdb' database
11. Clone and configure Item Catalog app

## Known Issues
Intermittent 'Internal Server Error' accessing website on Amazon Web Services. Refreshing the page clears the error and renders the appropriate webpage. Apache error log reports the following:

> InvalidRequestError: This Session's transaction has been rolled back due to a previous exception during flush. To begin a new transaction with this Session, first issue Session.rollback(). Original exception was: (psycopg2.IntegrityError) duplicate key value violates unique constraint "user_pkey"

Intermittent SSH disconnection to server on Amazon Web Services. Occurs occassionally when reviewing log files or reading ('cat') files. Error reported in terminal:

> packet_write_wait: Connection to 35.164.200.0 port 2200: Broken pipe
