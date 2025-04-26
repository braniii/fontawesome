import json
import math
import re
import os

from fontTools.ttLib import TTFont

# Hardcoded font file names and output enc names
fonts = [
    ("FontAwesome6Brands-Regular-400.otf", "fa6brands"),
    ("FontAwesome6Free-Regular-400.otf", "fa6free"),
    ("FontAwesome6Free-Solid-900.otf", "fa6free"),
]
fonts_enc = [
    ("FontAwesome6Brands-Regular-400.otf", "fa6brands"),
    ("FontAwesome6Free-Solid-900.otf", "fa6free"),
]

root_dir = "fontawesome6"
opentype_dir = "opentype"
enc_dir = "enc"
map_dir = "map"
tfm_dir = "tfm"
type1_dir = "type1"
tex_dir = "tex"
GLYPHS_PER_ENC = 256

# Paths
ICON_JSON = os.path.join('assets', 'icons.json')
OUTPUT_DEF = os.path.join(root_dir, 'tex', 'fontawesome6-mapping.def')

ALLOWED_PATTERN = re.compile("[A-Za-z]+")
SKIP_ICONS = set(str(i) for i in range(10))
HEADING_MAPPING = """% Copyright 2025 Daniel Nagel
%
% This work may be distributed and/or modified under the
% conditions of the LaTeX Project Public License, either version 1.3c
% of this license or (at your option) any later version.
% The latest version of this license is in
%   http://www.latex-project.org/lppl.txt
% and version 1.3 or later is part of all distributions of LaTeX
% version 2005/12/01 or later.
%
% This work has the LPPL maintenance status `maintained'.
% 
% The Current Maintainer of this work is Daniel Nagel
%
"""

FD_FREE = """\\DeclareFontFamily{{U}}{{fontawesome6{enc}}}{{}}
\\DeclareFontShape{{U}}{{fontawesome6{enc}}}{{solid}}{{n}}
    {{<-> fa6{enc}solid}}{{}}
\\DeclareFontShape{{U}}{{fontawesome6{enc}}}{{regular}}{{n}}
    {{<-> fa6{enc}regular}}{{}}

\\DeclareFontShape{{U}}{{fontawesome6{enc}}}{{m}}{{n}}
    {{<->ssub * fontawesome6{enc}/regular/n}}{{}}
\\DeclareFontShape{{U}}{{fontawesome6{enc}}}{{b}}{{n}}
    {{<->ssub * fontawesome6{enc}/solid/n}}{{}}
\\DeclareFontShape{{U}}{{fontawesome6{enc}}}{{bx}}{{n}}
    {{<->ssub * fontawesome6{enc}/solid/n}}{{}}
"""

FD_BRANDS = """\\DeclareFontFamily{{U}}{{fontawesome6{enc}}}{{}}
\\DeclareFontShape{{U}}{{fontawesome6{enc}}}{{regular}}{{n}}
    {{<-> fa6{enc}}}{{}}
\\DeclareFontShape{{U}}{{fontawesome6{enc}}}{{solid}}{{n}}
    {{<->ssub * fontawesome6{enc}/regular/n}}{{}}
\\DeclareFontShape{{U}}{{fontawesome6{enc}}}{{light}}{{n}}
    {{<->ssub * fontawesome6{enc}/regular/n}}{{}}

\\DeclareFontShape{{U}}{{fontawesome6{enc}}}{{l}}{{n}}
    {{<->ssub * fontawesome6{enc}/regular/n}}{{}}
\\DeclareFontShape{{U}}{{fontawesome6{enc}}}{{m}}{{n}}
    {{<->ssub * fontawesome6{enc}/regular/n}}{{}}
\\DeclareFontShape{{U}}{{fontawesome6{enc}}}{{b}}{{n}}
    {{<->ssub * fontawesome6{enc}/regular/n}}{{}}
\\DeclareFontShape{{U}}{{fontawesome6{enc}}}{{bx}}{{n}}
    {{<->ssub * fontawesome6{enc}/regular/n}}{{}}
"""



def generate_enc(otf_path, enc_base, enc_dir):
    font = TTFont(otf_path)
    glyph_order = font.getGlyphOrder()
    glyph_order = [g for g in glyph_order if not g.startswith('.')]
    glyph_order = [g for g in glyph_order if g not in SKIP_ICONS]
    glyph_order.sort()
    n_glyphs = len(glyph_order)

    glyph_assignments = {}

    # get number of subfiles
    n_parts = math.ceil(len(glyph_order) / GLYPHS_PER_ENC)
    for part in range(n_parts):
        enc_name = f"{enc_base}{part}"
        enc_path = os.path.join(root_dir, enc_dir, f"{enc_name}.enc")
        with open(enc_path, "w", encoding="utf-8") as f:
            f.write(f"/{enc_name} [\n")
            for idx in range(part * GLYPHS_PER_ENC, (part + 1) * GLYPHS_PER_ENC):
                if idx < n_glyphs:
                    f.write(f"/{glyph_order[idx]}\n")
                    slot = idx % GLYPHS_PER_ENC
                    glyph_assignments[glyph_order[idx]] = (enc_name[3:], slot)
                else:
                    f.write("/.notdef\n")
            f.write("] def\n")
        print(f"... generated {enc_path}")
    
    return glyph_assignments


def generate_mapping(enc_assignments):
    with open(ICON_JSON, encoding="utf-8") as f:
        icons = json.load(f)

    lines = []
    for name, icon in icons.items():
        unicode_val = icon.get("unicode")
        if name not in enc_assignments:
            continue
        fam, slot = enc_assignments.get(name)
        macro = f"\\fa{''.join([w.capitalize() for w in name.split('-')])}"
        # if digit in macro delete macro
        if not ALLOWED_PATTERN.fullmatch(macro[2:]):
            macro = ""
        # Compose line
        lines.append(
            f'\\__fontawesome_def_icon:nnnnn{{{macro}}}{{{name}}}{{{fam}}}{{{slot}}}{{"{unicode_val.upper()}}}'
        )

    # Write header and lines
    with open(OUTPUT_DEF, "w", encoding="utf-8") as out:
        out.write(HEADING_MAPPING)
        for line in lines:
            out.write(line + "\n")
    
    print(f"... generated {OUTPUT_DEF}")


def generate_map():
    map_lines = []

    # Map font base to PostScript name and .pfb file
    font_psnames = {
        "brands": ("FontAwesome6Brands-Regular", "FontAwesome6Brands-Regular.pfb"),
        "regular": ("FontAwesome6Free-Regular", "FontAwesome6Free-Regular.pfb"),
        "solid": ("FontAwesome6Free-Solid", "FontAwesome6Free-Solid.pfb"),
    }

    tfm_path = os.path.join(root_dir, tfm_dir)
    for tfm_file in sorted(
        [f for f in os.listdir(tfm_path) if f.endswith(".tfm")]
    ):
        tfm_name = tfm_file[:-4]
        for base in font_psnames.keys():
            if base in tfm_name:
                ps_name, pfb_file = font_psnames[base]
                break

        # Extract encoding part (e.g., fa6free0, fa6free1, ...)
        enc_part = tfm_name.replace("solid", "").replace("regular", "")
        enc_file = f"{enc_part}.enc"
        enc_name = enc_part

        map_line = (
            f"{tfm_name} {ps_name} \"{enc_name} ReEncodeFont\" <[{enc_file} <{pfb_file}"
        )
        map_lines.append(map_line)

    map_path = os.path.join(root_dir, map_dir, "fontawesome6.map")
    with open(map_path, "w", encoding="utf-8") as f:
        for line in map_lines:
            f.write(line + "\n")
    print(f"... generated {map_path}")


def generate_fd_files(enc_assignments):
    fd_dir = os.path.join(root_dir, tex_dir)
    enc_files = set(enc for enc, _ in enc_assignments.values())

    for enc in enc_files:
        # Generate fd files for free fonts
        fd_path = os.path.join(fd_dir, f"ufontawesome6{enc}.fd")
        with open(fd_path, "w", encoding="utf-8") as f:
            f.write(HEADING_MAPPING)
            if enc.startswith("free"):
                f.write(FD_FREE.format(enc=enc))
            else:
                f.write(FD_BRANDS.format(enc=enc))
        print(f"... generated {fd_path}")


if __name__ == "__main__":
    glyph_assignments = {}
    print("Generating enc files...")
    for otf_file, enc_base in fonts_enc:
        otf_path = os.path.join(root_dir, opentype_dir, otf_file)
        glyph_assignments |= generate_enc(otf_path, enc_base, enc_dir)
    
    print("Generating mapping file...")
    generate_mapping(glyph_assignments)

    print("Generating type1 files...")
    enc_files = [f for f in os.listdir(os.path.join(root_dir, enc_dir)) if f.endswith(".enc")]
    enc_files.sort()
    for otf_file, enc_base in fonts:
        otf_path = os.path.join(root_dir, opentype_dir, otf_file)
        # loop over all enc files
        for enc_file in enc_files:
            if enc_file.startswith(enc_base):
                enc_path = os.path.join(root_dir, enc_dir, enc_file)
                tfm_path = os.path.join(root_dir, tfm_dir)
                type1_path = os.path.join(root_dir, type1_dir)
                # Generate type1 files
                os.system(
                    "otftotfm --no-encoding --force "
                    f"--tfm-directory {tfm_path} "
                    f"--type1-directory {type1_path} "
                    f"-e {enc_path} {otf_path}"
                )

                # rename tfm files
                tfm_file = os.path.join(
                    tfm_path, f"{otf_file[:-8]}--{enc_file[:-4]}.tfm",
                )

                new_tfm_file = os.path.join(
                    tfm_path, f"{enc_file[:-4]}.tfm",
                ) if enc_base.endswith("brands") else os.path.join(
                    tfm_path, f"{enc_file[:-4]}{'solid' if 'Solid' in otf_file else 'regular'}.tfm",
                )

                os.rename(tfm_file, new_tfm_file)
                print(f"... generated {new_tfm_file}")

    # Generate the map file
    print("Generating map file...")
    generate_map()

    print("Generating fd files...")
    generate_fd_files(glyph_assignments)

    print("Done.")
    