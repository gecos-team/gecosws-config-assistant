#!/bin/bash

lang=$1
appname="gecosws-config-assistant"

if [ "" == "$lang" ] 
then
    lang="es"
fi

podir="../po"
potfilesin="${podir}/POTFILES.in"
potfile="${podir}/${appname}.pot"
pofile="${podir}/${lang}.po"
pofilemerged="${podir}/${lang}.merged.po"
mofile="${podir}/${appname}.mo"

gladepotfilesin="${podir}/POTFILES_glade.in"
gladepotfile="${podir}/${appname}_glade.pot"
gladepofile="${podir}/glade_${lang}.po"


find .. -type f -name "*.py" > $potfilesin

xgettext --language=Python --keyword=_ --output=$potfile -f $potfilesin
xgettext --sort-output --keyword=translatable --output=$gladepotfile -f $gladepotfilesin

if [ ! -f $pofile ]; then

    msginit --input=$potfile --locale=es_ES --output-file $pofile

else

    msgmerge $pofile $potfile > $pofilemerged
    mv $pofilemerged $pofile

fi


if [ ! -f $gladepofile ]; then

    msginit --input=$gladepotfile --locale=es_ES --output-file $gladepofile

else

    msgmerge $gladepofile $gladepotfile > $pofilemerged
    mv $pofilemerged $gladepofile

fi


sed -i s@^../@@g $potfilesin
