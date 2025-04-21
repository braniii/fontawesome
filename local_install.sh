mkdir -p ~/texmf/tex/latex/fontawesome6
mkdir -p ~/texmf/fonts/opentype/fontawesome6
mkdir -p ~/texmf/fonts/type1/fontawesome6
mkdir -p ~/texmf/fonts/tfm/fontawesome6
mkdir -p ~/texmf/fonts/map/dvips/fontawesome6
mkdir -p ~/texmf/fonts/enc/dvips/fontawesome6

cd fontawesome6

# copy files
# Copy LaTeX package and helper files
cp tex/*.sty ~/texmf/tex/latex/fontawesome6/
cp tex/*.fd ~/texmf/tex/latex/fontawesome6/
cp tex/*.lua ~/texmf/tex/latex/fontawesome6/
cp tex/*.def ~/texmf/tex/latex/fontawesome6/

# Copy OpenType fonts
cp opentype/*.otf ~/texmf/fonts/opentype/fontawesome6/

# Copy Type1 fonts
cp type1/*.pfb ~/texmf/fonts/type1/fontawesome6/

# Copy TFM files
cp tfm/*.tfm ~/texmf/fonts/tfm/fontawesome6/

# Copy map files
cp map/*.map ~/texmf/fonts/map/dvips/fontawesome6/

# Copy encoding files
cp enc/*.enc ~/texmf/fonts/enc/dvips/fontawesome6/

mktexlsr ~/texmf
updmap-user --enable Map=fontawesome6.map

updmap-user --syncwithtrees
kpsewhich pdftex.map
updmap-user
