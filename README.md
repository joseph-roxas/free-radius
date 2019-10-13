# Free Radius
Free Radius Installation Guide in Ubuntu 18.04

Step 1. Install MySQL server and run security setting.

```
$ sudo su
# apt-get update
# apt-get install mysql-server
# mysql_secure_installation
```

Step 2. Install freeradius

```
$ sudo su
# apt-get install freeradius openssl freeradius-common freeradius-mysql freeradius-utils
```

Step 3. Configure MySQL

Create "radius" database

```
$ sudo su
# cd /etc/freeradius/3.0/mods-config/sql/main/mysql/
# mysql -u root -p radius < schema.sql
```

Create "radius" user

Open up the MySQL shell

```
$ mysql -u root -p
```

From there, create a new user "radius" and give it a strong password:

```
mysql> CREATE USER 'radius'@'localhost' IDENTIFIED BY 'strongpassword';
```

Allow the server to read any table in SQL

```
GRANT SELECT ON radius.* TO 'radius'@'localhost';
```
Allow the server to write to the accounting and post-auth logging table.

```
GRANT ALL on radius.radacct TO 'radius'@'localhost';
GRANT ALL on radius.radpostauth TO 'radius'@'localhost';
```

