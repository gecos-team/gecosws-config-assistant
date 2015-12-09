#!/bin/bash

lang=$1
appname="firstboot"

if [ "" == "$lang" ]; then
    lang="es"
fi

podir="../po"
pofile="${podir}/${lang}.po"
mofile="${podir}/${appname}.mo"

cp $pofile /tmp/tmp.po

msgfmt /tmp/tmp.po --output-file $mofile
