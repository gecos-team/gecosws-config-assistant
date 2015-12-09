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

gladepotfilesin="${podir}/POTFILES-glade.in"
gladepotfile="${podir}/${appname}-glade.pot"
gladepofile="${podir}/${lang}.po.glade"


find .. -type f -name "*.py" > $potfilesin

xgettext --language=Python --keyword=_ --output=$potfile -f $potfilesin
xgettext --sort-output --keyword=translatable --output=$gladepotfile -f $gladepotfilesin

# Python PO file
if [ ! -f $pofile ]; then

    msginit --input=$potfile --locale=es_ES --output-file $pofile

else

    msgmerge $pofile $potfile > $pofilemerged
    mv $pofilemerged $pofile

fi

# Glade PO file
if [ ! -f $gladepofile ]; then

    msginit --input=$gladepotfile --locale=es_ES --output-file $gladepofile

else

    msgmerge $gladepofile $gladepotfile > $pofilemerged
    mv $pofilemerged $gladepofile

fi

# Merge both
msgcat $gladepofile $pofile > $pofilemerged
mv $pofilemerged $pofile


sed -i s@^../@@g $potfilesin
