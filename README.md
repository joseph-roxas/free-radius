# Free Radius
Free Radius Installation Guide in Ubuntu 18.04

## Step 1. Install MySQL server and run security setting.

```
$ sudo su
# apt-get update
# apt-get install mysql-server
# mysql_secure_installation
```

## Step 2. Install freeradius

```
$ sudo su
# apt-get install freeradius openssl freeradius-common freeradius-mysql freeradius-utils
```

## Step 3. Configure MySQL

Create "radius" database

Open up MySQL shell

```
$ mysql -u root -p
```
Enter root password

```
mysql> CREATE DATABASE radius;
```
Exit MySQL shell

```
msql> quit; 
```
Navigate to MySQL config files and run radius database schema

```
$ sudo su
# cd /etc/freeradius/3.0/mods-config/sql/main/mysql/
# mysql -u root -p radius < schema.sql
```

Create default administrator for radius database

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
## Step 4. Edit Free Radius Files

list files to modify

```
/etc/freeradius/3.0/clients.conf
/etc/freeradius/3.0/sites-available/default
/etc/freeradius/3.0/sites-available/inner-tunnel
/etc/freeradius/3.0/mods-available/sql
/etc/freeradius/3.0/mods-available/eap
/etc/freeradius/3.0/mods-config/sql/counter/mysql/noresetcounter.conf
/etc/freeradius/3.0/dictionary
/etc/freeradius/3.0/mods-available/sqlcounter
/etc/freeradius/3.0/mods-config/sql/main/mysql/queries.conf
```



