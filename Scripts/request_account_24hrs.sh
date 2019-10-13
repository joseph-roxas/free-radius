#!/bin/sh

mysql -uradius -pStrongPassword radius < ../Sql/add_user_24_Hrs.sql 2>/dev/null
