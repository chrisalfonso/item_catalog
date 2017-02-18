# Linux Server Configuration

### Access
- 35.164.200.0
- ec2-35-164-200-0.us-west-2.compute.amazonaws.com

### Installed Software
- Apache
- Git
- PostgreSQL

### Configurations
1. Create grader user with permission to sudo
2. Enable key-based authentication
3. Update all installed packages
4. Change SSH port from 22 to 2200
5. Allow incoming connections only to the following ports 2200, 80, and 123
6. Configure local timezone to UTC
7. Serve WSGI application
8. Set password for default 'postgres' user
9. Disable remote connections to database
10. Create 'catalog' user with limited permissions to 'catalogdb' database
11. Clone and configure Item Catalog app