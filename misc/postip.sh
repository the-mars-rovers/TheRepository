#!/usr/bin/env bash

(
    timedatectl;
    echo '----------';
    date;
    echo '----------';
    ifconfig;
    echo '----------';
    iwconfig
) | ix -i 1BB7
