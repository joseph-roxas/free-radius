#!/bin/sh

mysql -uradius -pStrongPassword radius < ../Sql/add_user_12_Hrs.sql 2>/dev/null
