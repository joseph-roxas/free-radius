#! /bin/bash

xrandr --newmode $(cvt 1920 1080 60 | grep Mode | sed -e 's/.*"/1920x1080/')

xrandr --addmode VGA-0 1920x1080
