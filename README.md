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

Under `authorize {}` make sure both `sql` and `eap {..}` are uncommented.

Under `authenticate {}` make sure `eap` is uncommented.

Under `session {}` make sure `sql` is uncommented.

Under `post-auth {}` make sure `sql` is uncommented as well as in the `Post-Auth-Type REJECT {}` subsection.

### Modify /etc/freeradius/3.0/mods-available/sql

This is the configuration file for the SQL module.
```
sql {
        # The sub-module to use to execute queries. This should match
        # the database you're attempting to connect to.
        #
        #    * rlm_sql_mysql
        #    * rlm_sql_mssql
        #    * rlm_sql_oracle
        #    * rlm_sql_postgresql
        #    * rlm_sql_sqlite
        #    * rlm_sql_null (log queries to disk)
        #
        #driver = "rlm_sql_null"
        driver = "rlm_sql_mysql"
#
#       Several drivers accept specific options, to set them, a
#       config section with the the name as the driver should be added
#       to the sql instance.
#
#       Driver specific options are:
#
#       sqlite {
#               # Path to the sqlite database
#               filename = "/tmp/freeradius.db"
#
#               # How long to wait for write locks on the database to be
#               # released (in ms) before giving up.
#               busy_timeout = 200
#
#               # If the file above does not exist and bootstrap is set
#               # a new database file will be created, and the SQL statements
#               # contained within the bootstrap file will be executed.
#               bootstrap = "${modconfdir}/${..:name}/main/sqlite/schema.sql"
#       }
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
#
#       postgresql {
#
#               # unlike MySQL, which has a tls{} connection configuration, postgresql
#               # uses its connection parameters - see the radius_db option below in
#               # this file
#
#               # Send application_name to the postgres server
#               # Only supported in PG 9.0 and greater. Defaults to no.
#               send_application_name = yes
#       }
#

        # The dialect of SQL you want to use, this should usually match
        # the driver you selected above.
        #
        # If you're using rlm_sql_null, then it should be the type of
        # database the logged queries are going to be executed against.
        dialect = "mysql" #"sqlite"

        # Connection info:
        #
        server = "localhost"
        port = 3306
        login = "radius"
        password = "StrongPasswordHere" #"radpass"

        # Database table configuration for everything except Oracle
        radius_db = "radius"

        # If you are using Oracle then use this instead
#       radius_db = "(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=localhost)(PORT=1521))(CONNECT_DATA=(SID=your_sid)))"

        # If you're using postgresql this can also be used instead of the connection info parameters
#       radius_db = "dbname=radius host=localhost user=radius password=raddpass"

        # Postgreql doesn't take tls{} options in its module config like mysql does - if you want to
        # use SSL connections then use this form of connection info parameter
#       radius_db = "host=localhost port=5432 dbname=radius user=radius password=raddpass sslmode=verify-full sslcert=/etc/ssl/client.crt sslkey=/etc/ssl/client.key sslrootcert=/etc/ssl/ca.crt" 

        # If you want both stop and start records logged to the
        # same SQL table, leave this as is.  If you want them in
        # different tables, put the start table in acct_table1
        # and stop table in acct_table2
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

        # Table to keep group info
        usergroup_table = "radusergroup"

        # If set to 'yes' (default) we read the group tables unless Fall-Through = no in the reply table.
        # If set to 'no' we do not read the group tables unless Fall-Through = yes in the reply table.
#       read_groups = yes

        # If set to 'yes' (default) we read profiles unless Fall-Through = no in the groupreply table.
        # If set to 'no' we do not read profiles unless Fall-Through = yes in the groupreply table.
#       read_profiles = yes

        # Remove stale session if checkrad does not see a double login
        delete_stale_sessions = yes

        # Write SQL queries to a logfile. This is potentially useful for tracing
        # issues with authorization queries.  See also "logfile" directives in
        # mods-config/sql/main/*/queries.conf.  You can enable per-section logging
        # by enabling "logfile" there, or global logging by enabling "logfile" here.
        #
        # Per-section logging can be disabled by setting "logfile = ''"
#       logfile = ${logdir}/sqllog.sql

        #  Set the maximum query duration and connection timeout
        #  for rlm_sql_mysql.
#       query_timeout = 5

        #  As of version 3.0, the "pool" section has replaced the
        #  following configuration items:
        #
        #  num_sql_socks
        #  connect_failure_retry_delay
        #  lifetime
        #  max_queries

        #
        #  The connection pool is new for 3.0, and will be used in many
        #  modules, for all kinds of connection-related activity.
        #
        # When the server is not threaded, the connection pool
        # limits are ignored, and only one connection is used.
        #
        # If you want to have multiple SQL modules re-use the same
        # connection pool, use "pool = name" instead of a "pool"
        # section.  e.g.
        #
        #       sql1 {
        #           ...
        #           pool {
        #                ...
        #           }
        #       }
        #
        #       # sql2 will use the connection pool from sql1
        #       sql2 {
        #            ...
        #            pool = sql1
        #       }
        #
        pool {
                #  Connections to create during module instantiation.
                #  If the server cannot create specified number of
                #  connections during instantiation it will exit.
                #  Set to 0 to allow the server to start without the
                #  database being available.
                start = ${thread[pool].start_servers}

                #  Minimum number of connections to keep open
                min = ${thread[pool].min_spare_servers}

                #  Maximum number of connections
                #
                #  If these connections are all in use and a new one
                #  is requested, the request will NOT get a connection.
                #
                #  Setting 'max' to LESS than the number of threads means
                #  that some threads may starve, and you will see errors
                #  like 'No connections available and at max connection limit'
                #
                #  Setting 'max' to MORE than the number of threads means
                #  that there are more connections than necessary.
                max = ${thread[pool].max_servers}

                #  Spare connections to be left idle
                #
                #  NOTE: Idle connections WILL be closed if "idle_timeout"
                #  is set.  This should be less than or equal to "max" above.
                spare = ${thread[pool].max_spare_servers}

                #  Number of uses before the connection is closed
                #
                #  0 means "infinite"
                uses = 0

                #  The number of seconds to wait after the server tries
                #  to open a connection, and fails.  During this time,
                #  no new connections will be opened.
                retry_delay = 30

                # The lifetime (in seconds) of the connection
                lifetime = 0

                #  idle timeout (in seconds).  A connection which is
                #  unused for this length of time will be closed.
                idle_timeout = 60

                #  NOTE: All configuration settings are enforced.  If a
                #  connection is closed because of "idle_timeout",
                #  "uses", or "lifetime", then the total number of
                #  connections MAY fall below "min".  When that
                #  happens, it will open a new connection.  It will
                #  also log a WARNING message.
                #
                #  The solution is to either lower the "min" connections,
                #  or increase lifetime/idle_timeout.
        }

        # Set to 'yes' to read radius clients from the database ('nas' table)
        # Clients will ONLY be read on server startup.
        read_clients = yes

        # Table to keep radius client info
        client_table = "nas"

        #
        # The group attribute specific to this instance of rlm_sql
        #

        # This entry should be used for additional instances (sql foo {})
        # of the SQL module.
#       group_attribute = "${.:instance}-SQL-Group"

        # This entry should be used for the default instance (sql {})
        # of the SQL module.
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
