#!/usr/bin/env bash

export IP=$(hostname -I | cut -f1 -d' ')

dyndns rospi ${IP}

(
    echo ${IP}
    echo '----------';
    timedatectl;
    echo '----------';
    date;
    echo '----------';
    ifconfig;
    echo '----------';
    iwconfig
) | ix -i 1BB7
