import json
import math
import re
import os

from fontTools.ttLib import TTFont

# Hardcoded font file names and output enc names
fonts = [
    ("FontAwesome6Brands-Regular-400.otf", "fa6brands", "regular"),
    ("FontAwesome6Free-Regular-400.otf", "fa6free", "regular"),
    ("FontAwesome6Free-Solid-900.otf", "fa6free", "solid"),
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
HEADING_MAPPING = """% Copyright 2025-2026 Daniel Nagel
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



def _glyphs_from_otf(otf_path):
    font = TTFont(otf_path)
    glyph_order = font.getGlyphOrder()
    glyph_order = [g for g in glyph_order if not g.startswith('.')]
    glyph_order = [g for g in glyph_order if g not in SKIP_ICONS]
    glyph_order.sort()
    return glyph_order


def generate_enc_pair(solid_otf_path, regular_otf_path, enc_base, enc_dir):
    solid_glyphs = _glyphs_from_otf(solid_otf_path)
    regular_glyphs = set(_glyphs_from_otf(regular_otf_path))

    glyph_assignments = {}

    n_parts = math.ceil(len(solid_glyphs) / GLYPHS_PER_ENC)
    for part in range(n_parts):
        base_name = f"{enc_base}{part}"
        # Solid enc file
        enc_path_solid = os.path.join(root_dir, enc_dir, f"{base_name}_solid.enc")
        with open(enc_path_solid, "w", encoding="utf-8") as f:
            f.write(f"/{base_name}solid [\n")
            for idx in range(part * GLYPHS_PER_ENC, (part + 1) * GLYPHS_PER_ENC):
                if idx < len(solid_glyphs):
                    name = solid_glyphs[idx]
                    f.write(f"/{name}\n")
                    slot = idx % GLYPHS_PER_ENC
                    glyph_assignments[name] = (base_name[3:], slot)
                else:
                    f.write("/.notdef\n")
            f.write("] def\n")
        print(f"... generated {enc_path_solid}")

        # Regular enc file (holes for missing glyphs)
        enc_path_regular = os.path.join(root_dir, enc_dir, f"{base_name}_regular.enc")
        with open(enc_path_regular, "w", encoding="utf-8") as f:
            f.write(f"/{base_name}regular [\n")
            for idx in range(part * GLYPHS_PER_ENC, (part + 1) * GLYPHS_PER_ENC):
                if idx < len(solid_glyphs):
                    name = solid_glyphs[idx]
                    if name in regular_glyphs:
                        f.write(f"/{name}\n")
                    else:
                        f.write("/.notdef\n")
                else:
                    f.write("/.notdef\n")
            f.write("] def\n")
        print(f"... generated {enc_path_regular}")

    return glyph_assignments


def generate_enc_simple(otf_path, enc_base, enc_dir):
    """Generate a single enc set (no style suffix). Used for brands."""
    glyph_order = _glyphs_from_otf(otf_path)
    glyph_assignments = {}
    n_parts = math.ceil(len(glyph_order) / GLYPHS_PER_ENC)
    for part in range(n_parts):
        enc_name = f"{enc_base}{part}"
        enc_path = os.path.join(root_dir, enc_dir, f"{enc_name}.enc")
        with open(enc_path, "w", encoding="utf-8") as f:
            f.write(f"/{enc_name} [\n")
            for idx in range(part * GLYPHS_PER_ENC, (part + 1) * GLYPHS_PER_ENC):
                if idx < len(glyph_order):
                    name = glyph_order[idx]
                    f.write(f"/{name}\n")
                    slot = idx % GLYPHS_PER_ENC
                    glyph_assignments[name] = (enc_name[3:], slot)
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
    for tfm_file in sorted([f for f in os.listdir(tfm_path) if f.endswith(".tfm")]):
        tfm_name = tfm_file[:-4]
        for base in font_psnames.keys():
            if base in tfm_name:
                ps_name, pfb_file = font_psnames[base]
                break

        # Extract encoding root (e.g., fa6free0) and style
        if tfm_name.endswith("solid"):
            style = "solid"
        elif tfm_name.endswith("regular"):
            style = "regular"
        else:
            style = "regular"  # brands fallback
        enc_root = tfm_name.replace("solid", "").replace("regular", "")

        # Brands use single enc, named exactly like file
        if enc_root.startswith("fa6brands"):
            enc_file = f"{enc_root}.enc"
            enc_name = enc_root
        else:
            # Free: style-specific enc file with shared root
            enc_file = f"{enc_root}_{style}.enc"
            enc_name = f"{enc_root}{style}"

        map_line = f"{tfm_name} {ps_name} \"{enc_name} ReEncodeFont\" <[{enc_file} <{pfb_file}"
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
    # Brands: single regular-only enc set
    brands_otf = os.path.join(root_dir, opentype_dir, "FontAwesome6Brands-Regular-400.otf")
    glyph_assignments |= generate_enc_simple(
        otf_path=brands_otf,
        enc_base="fa6brands",
        enc_dir=enc_dir,
    )
    # Free: generate parallel encs from Solid and Regular OTFs
    free_solid_otf = os.path.join(root_dir, opentype_dir, "FontAwesome6Free-Solid-900.otf")
    free_regular_otf = os.path.join(root_dir, opentype_dir, "FontAwesome6Free-Regular-400.otf")
    glyph_assignments |= generate_enc_pair(
        solid_otf_path=free_solid_otf,
        regular_otf_path=free_regular_otf,
        enc_base="fa6free",
        enc_dir=enc_dir,
    )

    print("Generating mapping file...")
    generate_mapping(glyph_assignments)

    print("Generating type1 files...")
    enc_files = [f for f in os.listdir(os.path.join(root_dir, enc_dir)) if f.endswith(".enc")]
    enc_files.sort()
    for otf_file, enc_base, style in fonts:
        otf_path = os.path.join(root_dir, opentype_dir, otf_file)
        # loop over all enc files
        for enc_file in enc_files:
            if enc_file.startswith(enc_base):
                enc_path = os.path.join(root_dir, enc_dir, enc_file)
                tfm_path = os.path.join(root_dir, tfm_dir)
                type1_path = os.path.join(root_dir, type1_dir)
                # For free fonts, only use enc files matching their style suffix
                if enc_base == "fa6free":
                    if not enc_file.endswith(f"_{style}.enc"):
                        continue
                # For brands, single enc set is fine

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

                if enc_base.endswith("brands"):
                    new_tfm_file = os.path.join(tfm_path, f"{enc_file[:-4]}.tfm")
                else:
                    enc_root = enc_file[:-4]  # e.g., fa6free0_solid
                    enc_part_root = enc_root.replace("_solid", "").replace("_regular", "")
                    style_tag = "solid" if style == "solid" else "regular"
                    new_tfm_file = os.path.join(tfm_path, f"{enc_part_root}{style_tag}.tfm")

                os.rename(tfm_file, new_tfm_file)
                print(f"... generated {new_tfm_file}")

    # Generate the map file
    print("Generating map file...")
    generate_map()

    print("Generating fd files...")
    generate_fd_files(glyph_assignments)

    print("Done.")
    
