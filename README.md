# FontAwesome7 LaTeX Package

> For using FontAwesome6, please see the `fa6` branch

[![CTAN](https://img.shields.io/ctan/v/fontawesome7.svg)](https://ctan.org/pkg/fontawesome7)

FontAwesome7 is a LaTeX package that provides access to the [Font Awesome 7](https://fontawesome.com/) icon set. It enables you to easily include high-quality icons in your LaTeX documents, presentations, and posters.

## Features

> Looking for free duotone icon sets? Have a look at the amazing [Phosphoricons](https://github.com/braniii/phosphoricons)

- Access to hundreds of Font Awesome 7 icons
- Supports both regular and solid styles
- Easy-to-use commands for inserting icons
- Works with PDFLaTeX, XeLaTeX, and LuaLaTeX
- Compatible with all styles of Pro version (requires a paid license)

## Installation

The package is available on [CTAN](https://ctan.org/pkg/fontawesome7). You can install it using your TeX distribution:

- **TeX Live:**  
    ```
    tlmgr install fontawesome7
    ```
- **MiKTeX:**  
    ```
    mpm --install fontawesome7
    ```

Alternatively, copy the package files to your local texmf tree like this. It should be noted, **that this script should only be used if you know what you are doing!**
```bash
bash ./local_install.sh
```

## Usage

Add the following to your document preamble:

```latex
\usepackage{fontawesome7}
% or directly setting the global style
\usepackage[style=solid|regular]{fontawesome7}
% or with
\faStyle{solid|regular}
```

Then, you can use the following commands to insert icons:

```latex
\faIcon{github}
% or
\faGithub
```

You can also specify styles:

```latex
\faIcon[regular]{address-book}
\faCamera[solid]
```

## Usage with Pro Version
To use the Pro version, ensure you have the Font Awesome Pro fonts installed and use XeLaTeX or LuaLaTeX. The commands remain the same, but you can access additional icons.

```latex
\usepackage[pro, style=solid|regular|light|thin|duotone-solid|duotone-regular|duotone-light|duotone-thin|sharp-solid|sharp-regular|sharp-light|sharp-thin|sharp-duotone-solid|sharp-duotone-regular|sharp-duotone-light|sharp-duotone-thin]{fontawesome7}
```

Then, use the same commands as above to insert icons. For duotone icons, you can set the secondary color:

```latex
  % Remember to load xcolor
  % Set secondary color to green
  \faDuotoneSetSecondary{\color{green}}
```

## Icon List

For a full list of available icons and their names, see the [package documentation](fontawesome7/doc/fontawesome7.pdf) or the [Font Awesome icon gallery](https://fontawesome.com/icons).
A cheatsheet for the `\faIcon` syntax can be found [here](cheatsheet/fa7_cheatsheet_faicon.pdf) and for the command syntax, e.g. `faGithub` [here](cheatsheet/fa7_cheatsheet.pdf).

## Example

```latex
\documentclass{article}
\usepackage{fontawesome7}
\begin{document}

\faGithub \quad
\fauser \quad
\faAddressBook

\end{document}
```

## Acknowledgments

Special thanks to Marcel Krüger for creating the original [fontawesome5](https://ctan.org/pkg/fontawesome5) package, which served as the foundation for this package.

## Documentation

Comprehensive documentation is available in [`doc/fontawesome7.pdf`](fontawesome7/doc/fontawesome7.pdf).

## License

This package is distributed under the [LaTeX Project Public License (LPPL)](https://www.latex-project.org/lppl/).

---

*FontAwesome7 is not affiliated with or endorsed by Fonticons, Inc.*
