import json
import os

# Paths
ICON_JSON = os.path.join('scripts', 'icons.json')
OUTPUT_DEF = os.path.join('fontawesome6', 'tex', 'fontawesome6-mapping.def')

HEADING = """% Copyright 2025 Daniel Nagel
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
% Auto-generated from icons.json
"""

# Map FA6 style to LaTeX font family
STYLE_MAP = {
    "brands": "brands0",
    "solid": "free0",
    "regular": "free1",
    "light": "free2",
    "thin": "free3",
    "duotone": "free4",
}

def main():
    with open(ICON_JSON, encoding="utf-8") as f:
        icons = json.load(f)

    lines = []
    idx = {k: 0 for k in STYLE_MAP.values()}

    for name, icon in icons.items():
        unicode_val = icon.get("unicode")
        styles = icon.get("styles", [])
        label = icon.get("label", name)
        for style in styles:
            if style not in STYLE_MAP:
                continue
            fam = STYLE_MAP[style]
            macro = f"\\fa{''.join([w.capitalize() for w in name.split('-')])}"
            # Compose line
            lines.append(
                f'\\__fontawesome_def_icon:nnnnn{{{macro}}}{{{name}}}{{{fam}}}{{{idx[fam]}}}{{"{unicode_val.upper()}}}'
            )
            idx[fam] += 1

    # Write header and lines
    with open(OUTPUT_DEF, "w", encoding="utf-8") as out:
        out.write(HEADING)
        for line in lines:
            out.write(line + "\n")

if __name__ == "__main__":
    main()
