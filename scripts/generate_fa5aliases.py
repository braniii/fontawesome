def to_camel_case(s):
    parts = s.split('-')
    return ''.join(p.capitalize() for p in parts)

# # Write .def file (for faIcon aliases)
# with open('assets/icon_renaming.txt') as f, open('fontawesome6/tex/fontawesome6-fa5alias.def', 'w') as out:
#     for line in f:
#         if not line.strip() or line.startswith('//'):
#             continue
#         fa5, fa6 = [x.strip() for x in line.split('\t') if x.strip()]
#         out.write(f'\\cs_new_protected:cpn {{fa__{fa5}:}} {{\\faIcon{{{fa6}}}}}\n')

# Write .sty file (for NewDocumentCommand macros)
with open('assets/icon_renaming.txt') as f, open('fontawesome6/tex/fontawesome6-fa5alias-cmds.sty', 'w') as out:
    out.write(r"""% Copyright 2025 Daniel Nagel
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

\@ifpackageloaded{fontawesome6}{}{\PackageError{fontawesome6-generic-helper}{This package should not be loaded individually. Load fontawesome6 instead.}{}}


\ProvidesExplPackage{fontawesome6-fa5alias-cmds}{2025/04/20}{6.7.2}{Alias definitions for FA5 for fontawesome6}
""")
    # out.write('\\ProvidesPackage{fontawesome6-fa5alias-cmds}[FA5 macro aliases]\n')
    # out.write('\\RequirePackage{xparse}\n')
    for line in f:
        if not line.strip() or line.startswith('//'):
            continue
        fa5, fa6 = [x.strip() for x in line.split('\t') if x.strip()]
        if not any(char.isdigit() for char in fa5):
            camel_cmd = 'fa' + to_camel_case(fa5)
            out.write(
                f'\\NewDocumentCommand\\{camel_cmd}'
                '{O{\\str_use:N\\l_fontawesome_style_str}}'
                f'{{\\faIcon[#1]{{{fa6}}}}}\n'
            )

# Write documentation table (for inclusion in the document body)
with open('assets/icon_renaming.txt') as f, open('fontawesome6/doc/fa6_fa5alias.tex', 'w') as out:
    out.write('% Auto-generated FA5 alias table\n')
    out.write('\newgeometry{textwidth=18cm}\n')
    out.write('\\subsection*{Full~icon~list~for~FontAwesome~5~Aliases}\n')
    out.write('\\begin{longtable}{cll}\n')
    for line in f:
        if not line.strip() or line.startswith('//'):
            continue
        fa5, fa6 = [x.strip() for x in line.split('\t') if x.strip()]
        fa5_cmd = 'fa' + to_camel_case(fa5)
        if (
            fa5_cmd == 'faHourglassHalf' or
            fa5_cmd == 'faPeopleArrows'
        ):
            continue
        out.write(
            f'\\{fa5_cmd} & '
            f'\\texttt{{\\textbackslash {fa5_cmd}}} & '
            f'\\texttt{{\\textbackslash faIcon{{{fa6}}}}} \\\\\n'
        )
    out.write('\\end{longtable}\n')
    out.write('\\restoregeometry\n')