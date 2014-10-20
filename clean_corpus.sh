CORPUS=$1
iconv -c -f utf-8 -t ascii $CORPUS | tr '[A-Z]' '[a-z]' | sed "s/[^a-z0-9]*[ \t\n\r][^a-z0-9]*/ /g" | sed "s/[^a-z0-9]*$/ /g" | sed "s/  */ /g" > $CORPUS.filtered