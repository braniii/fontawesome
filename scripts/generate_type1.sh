ARGS="--no-encoding --tfm-directory tfm --type1-directory type1"

otftotfm $ARGS -e enc/fontawesome6free-regular-400.enc opentype/FontAwesome6Free-Regular-400.otf
otftotfm $ARGS -e enc/fontawesome6brands-regular-400.enc opentype/FontAwesome6Brands-Regular-400.otf
otftotfm $ARGS -e enc/fontawesome6free-solid-900.enc opentype/FontAwesome6Free-Solid-900.otf

# rename tfm files to match map
cd tfm
for f in *--*
    do mv "$f" "${f#*--}"
done
cd ..
