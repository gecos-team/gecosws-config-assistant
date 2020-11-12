#!/usr/bin/expect -f

lassign $argv arg1 arg2 

spawn /usr/bin/gem source -a "$arg1" --config-file "$arg2"

expect "\[yn\]"

send  "y\r"
expect eof
