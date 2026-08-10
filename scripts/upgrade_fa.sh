#!/usr/bin/env bash
# Upgrade the fontawesome7 package to the latest Font Awesome release.
#
# Checks the FortAwesome/Font-Awesome releases, and if a newer 7.x version
# than the one in fontawesome7.sty is available: downloads the desktop
# fonts, regenerates all binding artifacts, bumps the package version,
# rebuilds the documentation and cheatsheets, and runs a full icon
# compile test on pdfLaTeX, XeLaTeX and LuaLaTeX.
#
# Requirements: curl, unzip, jq, python3 + fontTools, TeX Live
# (pdflatex, xelatex, lualatex, otftotfm).
#
# Environment overrides (mainly for testing):
#   FA_VERSION=7.3.1   use this version instead of querying GitHub
#   FORCE=1            run even if the version matches the current one
set -euo pipefail

cd "$(dirname "$0")/.."
ROOT=$(pwd)
FA7="$ROOT/fontawesome7"
WORK=$(mktemp -d)
trap 'rm -rf "$WORK"' EXIT

# --- 1. Determine current and latest version ---------------------------------
CURRENT=$(grep -oE '\{7\.[0-9]+\.[0-9]+-[0-9]+\}' "$FA7/tex/fontawesome7.sty" | tr -d '{}' | cut -d- -f1)
if [ -n "${FA_VERSION:-}" ]; then
    LATEST="$FA_VERSION"
else
    LATEST=$(curl -fsSL https://api.github.com/repos/FortAwesome/Font-Awesome/releases/latest | jq -r .tag_name)
fi
echo "Current FA version: $CURRENT — latest: $LATEST"

case "$LATEST" in
    7.*) ;;
    *) echo "Latest release $LATEST is not a 7.x version, manual intervention needed."; exit 1 ;;
esac
if [ "$CURRENT" = "$LATEST" ] && [ -z "${FORCE:-}" ]; then
    echo "Already up to date."
    exit 0
fi

# --- 2. Download the desktop release and copy fonts + metadata ---------------
echo "Downloading fontawesome-free-$LATEST-desktop.zip ..."
curl -fsSL -o "$WORK/fa.zip" \
    "https://github.com/FortAwesome/Font-Awesome/releases/download/$LATEST/fontawesome-free-$LATEST-desktop.zip"
unzip -q "$WORK/fa.zip" -d "$WORK"
REL="$WORK/fontawesome-free-$LATEST-desktop"

cp "$REL/otfs/Font Awesome 7 Brands-Regular-400.otf" "$FA7/opentype/FontAwesome7Brands-Regular-400.otf"
cp "$REL/otfs/Font Awesome 7 Free-Regular-400.otf"   "$FA7/opentype/FontAwesome7Free-Regular-400.otf"
cp "$REL/otfs/Font Awesome 7 Free-Solid-900.otf"     "$FA7/opentype/FontAwesome7Free-Solid-900.otf"
cp "$REL/metadata/icons.json" "$ROOT/assets/icons.json"

# --- 3. Regenerate binding artifacts -----------------------------------------
if python3 -c "import fontTools" 2>/dev/null; then
    PYRUN="python3"
elif command -v uv >/dev/null; then
    PYRUN="uv run --with fonttools python3"
else
    echo "fontTools not available (pip install fonttools)"; exit 1
fi
$PYRUN scripts/generate_binding.py > "$WORK/generate.log" || { cat "$WORK/generate.log"; exit 1; }
tail -3 "$WORK/generate.log"

# --- 4. Bump package version --------------------------------------------------
NEWVER="$LATEST-1"
TODAY=$(date +%Y/%m/%d)
for f in fontawesome7.sty fontawesome7-utex-helper.sty fontawesome7-generic-helper.sty; do
    sed -E -i.bak "s|(\\\\ProvidesExplPackage\{fontawesome7[a-z-]*\})\{[0-9/]+\}\{[0-9.-]+\}|\1{$TODAY}{$NEWVER}|" "$FA7/tex/$f"
done
sed -E -i.bak "s|version [0-9.-]+, dated [0-9/]+|version $NEWVER, dated $TODAY|" "$FA7/doc/fontawesome7.tex"
sed -E -i.bak "s|corresponds to Font Awesome [0-9.]+\.|corresponds to Font Awesome $LATEST.|" "$FA7/doc/fontawesome7.tex"
rm -f "$FA7"/tex/*.bak "$FA7"/doc/*.bak

# --- 5. Compile test: every icon on all three engines ------------------------
# The test document redefines the mapping macro to typeset every icon via
# \faIcon, so a glyph missing from the fonts aborts the compilation.
TEST="$WORK/build"
mkdir -p "$TEST"
cp "$FA7"/opentype/*.otf "$TEST/"  # cwd copies so luaotfload picks the new fonts
cat > "$TEST/testicons.tex" <<'EOF'
\documentclass{article}
\usepackage{fontawesome7}
\begin{document}
\ExplSyntaxOn
\cs_set:Nn\__fontawesome_def_icon:nnnnn{\faIcon{#2}~}
\file_input:n{fontawesome7-mapping.def}
\ExplSyntaxOff
\end{document}
EOF

export TEXINPUTS="$TEST:$FA7/tex:"
export LUAINPUTS="$FA7/tex:"
export OPENTYPEFONTS="$FA7/opentype:"
export TFMFONTS="$FA7/tfm:"
export T1FONTS="$FA7/type1:"
export ENCFONTS="$FA7/enc:"
export TEXFONTMAPS="$FA7/map:"

for eng in pdflatex xelatex lualatex; do
    echo "Testing all icons with $eng ..."
    ( cd "$TEST" && $eng -interaction=nonstopmode -halt-on-error testicons.tex > "$eng.log" 2>&1 ) \
        || { echo "FAILED: $eng"; tail -30 "$TEST/$eng.log"; exit 1; }
done

# --- 6. Rebuild documentation and cheatsheets --------------------------------
build_pdf() {
    local dir="$1" texfile="$2" jobname="$3"
    for _ in 1 2 3; do
        ( cd "$dir" && TEXINPUTS=".:$FA7/tex:" pdflatex -interaction=nonstopmode -halt-on-error \
            -jobname="$jobname" "$texfile" > "$WORK/$jobname.build.log" 2>&1 ) \
            || { echo "FAILED building $jobname"; tail -30 "$WORK/$jobname.build.log"; exit 1; }
        grep -q "Rerun" "$dir/$jobname.log" || break
    done
    if grep -q "No shorthand defined" "$dir/$jobname.log"; then
        echo "FAILED: new icons need special handling in fa7_fulllist.tex:"
        grep -A2 "No shorthand defined" "$dir/$jobname.log"
        exit 1
    fi
    rm -f "$dir/$jobname".{aux,log,toc,out}
}

echo "Building documentation ..."
build_pdf "$FA7/doc" fontawesome7.tex fontawesome7

echo "Building cheatsheets ..."
build_pdf "$ROOT/cheatsheet" fa7_cheatsheet.tex fa7_cheatsheet
sed -i.bak 's|^%\\input{fa7_icon}|\\input{fa7_icon}|; s|^\\input{fa7_cmd}|%\\input{fa7_cmd}|' "$ROOT/cheatsheet/fa7_cheatsheet.tex"
build_pdf "$ROOT/cheatsheet" fa7_cheatsheet.tex fa7_cheatsheet_faicon
sed -i.bak 's|^\\input{fa7_icon}|%\\input{fa7_icon}|; s|^%\\input{fa7_cmd}|\\input{fa7_cmd}|' "$ROOT/cheatsheet/fa7_cheatsheet.tex"
rm -f "$ROOT/cheatsheet/fa7_cheatsheet.tex.bak"

# --- 7. Summary ---------------------------------------------------------------
ADDED=$(git diff --no-color -- fontawesome7/tex/fontawesome7-mapping.def | grep -c '^+\\' || true)
REMOVED=$(git diff --no-color -- fontawesome7/tex/fontawesome7-mapping.def | grep -c '^-\\' || true)
echo "Upgrade to FA $LATEST complete (mapping diff: +$ADDED/-$REMOVED lines)."
if [ -n "${GITHUB_OUTPUT:-}" ]; then
    {
        echo "version=$LATEST"
        echo "package_version=$NEWVER"
    } >> "$GITHUB_OUTPUT"
fi
