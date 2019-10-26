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

Files to modify

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

### Modify /etc/freeradius/3.0/clients.conf

Add the following lines before `#IPv6 Client`

```
client tplink {
        ipaddr = 192.168.0.1
        secret = testing123
}

```

### Modify /etc/freeradius/3.0/sites-available/default

Under the `authorize {}` section:

Uncomment these lines
```
eap {
               ok = return
               updated = return
    }
```
and
```
sql
```
Add `noresetcounter` after `sql`
```
sql
noresetcounter
```

Under `authenticate {}` section make sure to uncomment:
```
eap
```
Under the `accounting {}` section uncomment the sql line:
```
sql
```
Under the `session {}` uncomment the `sql` line.

Under the `post-auth {}` section uncomment the `sql` line.

Under the `post-auth {}` section, under the `Post-Auth-Type REJECT {}` uncomment the `sql` line.


### Modify /etc/freeradius/3.0/sites-available/inner-tunnel

This is a virtual server that handles only inner tunnel requests for EAP-TTLS and PEAP types.

Under `authorize {}` make sure both `sql` and `eap {..}` are uncommented. Add `noresetcounter` after `sql`
```
sql
noresetcounter
```

Under `authenticate {}` make sure `eap` is uncommented.

Under `session {}` make sure `sql` is uncommented.

Under `post-auth {}` make sure `sql` is uncommented as well as in the `Post-Auth-Type REJECT {}` subsection.

### Modify /etc/freeradius/3.0/mods-available/sql

This is the configuration file for the SQL module.
```
sql {

        driver = "rlm_sql_mysql"

#
        mysql {
#               # If any of the files below are set, TLS encryption is enabled
#               tls {
#                       ca_file = "/etc/ssl/certs/my_ca.crt"
#                       ca_path = "/etc/ssl/certs/"
#                       certificate_file = "/etc/ssl/certs/private/client.crt"
#                       private_key_file = "/etc/ssl/certs/private/client.key"
#                       cipher = "DHE-RSA-AES256-SHA:AES128-SHA"
#               }
#
#               # If yes, (or auto and libmysqlclient reports warnings are
#               # available), will retrieve and log additional warnings from
#               # the server if an error has occured. Defaults to 'auto'
               warnings = yes  #auto
        }

        dialect = "mysql" #"sqlite"

        # Connection info:
        #
        server = "localhost"
        port = 3306
        login = "radius"
        password = "StrongPasswordHere" #"radpass"

        # Database table configuration for everything except Oracle
        radius_db = "radius"

        acct_table1 = "radacct"
        acct_table2 = "radacct"

        # Allow for storing data after authentication
        postauth_table = "radpostauth"

        # Tables containing 'check' items
        authcheck_table = "radcheck"
        groupcheck_table = "radgroupcheck"

        # Tables containing 'reply' items
        authreply_table = "radreply"
        groupreply_table = "radgroupreply"
        group_attribute = "SQL-Group"

        # Read database-specific queries
        $INCLUDE ${modconfdir}/${.:name}/main/${dialect}/queries.conf
}
```

To enable the SQL module make sure /etc/freeradius/3.0/mods-enabled/sql is existing, otherwise:
```
$ ln -s /etc/freeradius/3.0/mods-available/sql /etc/freeradius/3.0/mods-enabled/sql
```

### Modify /etc/freeradius/3.0/mods-available/eap

Among the other options, the ones that need to be changed are:
```
eap {
    ...

    default_eap_type = ttls

    ...

    tls-config tls-common {
        private_key_file = /etc/ssl/private/ssl-cert-snakeoil.key
        certificate_file = /etc/ssl/certs/ssl-cert-snakeoil.pem
        ca_file = /etc/ssl/certs/ca-certificates.crt
        dh_file = /etc/raddb/dh.pem
        random_file = /dev/urandom
        cipher_list = "HIGH"
        cipher_server_preference = yes
        tls_min_version = "1.2"
    }

    ...

    ttls {
        # make sure these lines are the same

        tls = tls-common

        virtual_server = "inner-tunnel"

    }

}
```

To enable the SQL module make sure /etc/freeradius/3.0/mods-enabled/sql is existing, otherwise:
```
$ ln -s /etc/freeradius/3.0/mods-available/eap /etc/freeradius/3.0/mods-enabled/eap
```

### Modify /etc/freeradius/3.0/mods-config/sql/counter/mysql/noresetcounter.conf
This is the configuration file:
```
query = "\
        SELECT IFNULL( MAX(TIME_TO_SEC(TIMEDIFF(NOW(), authdate))),0) \
        FROM radpostauth \
        WHERE username='%{${key}}' AND reply = 'Access-Accept' \
        ORDER BY authdate desc \
        LIMIT 1;"
```

### Modify /etc/freeradius/3.0/mods-available/

Under section `noresetcounter` set `mysql` as dialect.
```
sqlcounter noresetcounter {
        dialect = mysql
}
```
Under section `expire_on_login` set `mysql` as dialect.
```
sqlcounter expire_on_login {
        dialect = mysql
}
```

### Modify /etc/freeradius/3.0/mods-config/sql/main/mysql/queries.conf

Modify the Simultaneous Use Checking Query
```
#######################################################################
# Simultaneous Use Checking Queries
#######################################################################

simul_count_query = "\
        SELECT COUNT(*) \
        FROM ${postauth_table} \
        WHERE   username = '%{SQL-User-Name}' \
                AND reply = 'Access-Accept'  \
        "
```

Under `post-auth` section modify the `query` subsection
```
post-auth {
        query = "\
                INSERT INTO ${..postauth_table} \
                        (username, pass, reply, authdate, nasipaddress, macaddress) \
                VALUES ( \
                        '%{SQL-User-Name}', \
                        '%{%{User-Password}:-%{Chap-Password}}', \
                        '%{reply:Packet-Type}', \
                        '%S', \
                        '%{NAS-IP-Address}', \
                        '%{NAS-Ip-Address}')"
}
```

### Modify /etc/freeradius/3.0/dictionary

Add `Max-All-Sesion` attribute
```
ATTRIBUTE       Max-All-Session         3003    integer
```
