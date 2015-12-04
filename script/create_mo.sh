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

cp $pofile /tmp/tmp.po
tail -n+20 $gladepofile >> /tmp/tmp.po

msgfmt /tmp/tmp.po --output-file $mofile
