#!/bin/bash

lang=$1
appname="firstboot"

if [ "" == "$lang" ]; then
    lang="es"
fi

podir="../po"
pofile="${podir}/${lang}.po"
gladepofile="${podir}/${lang}_glade.po"
mofile="${podir}/${appname}.mo"

msgfmt $pofile $gladepofile --output-file $mofile
