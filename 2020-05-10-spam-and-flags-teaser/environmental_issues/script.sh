#!/usr/bin/env bash

####################################
# THE ENVIRONMENTAL ISSUE DATABASE #
####################################

set -x

if ! test -z "$USE_SED"
then
    line="$(sed -n "/${1:?Missing arg1: name}/p" issues.txt)"
else
    line="$(grep "${1:?Missing arg1: name}" < issues.txt)"
fi
echo "$line"

silent() { "$@" &>/dev/null; return "$?"; }

quiet() { bash -c 'for fd in /proc/$$/fd/*
                   do eval "exec ${fd##*/}>&-"
                   done; "$@" &> /dev/null' bash "$@"; }

if ! silent hash imaginary
then
    silent imaginary
    quiet cat flag
fi

