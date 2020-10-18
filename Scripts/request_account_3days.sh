#!/bin/sh

mysql -uradius -pStrongPassword radius < ../Sql/add_user_3_Days.sql 2>/dev/null
