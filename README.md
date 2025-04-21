# FontAwesome6 LaTeX Package

[![CTAN](https://img.shields.io/ctan/v/fontawesome6.svg)](https://ctan.org/pkg/fontawesome6)

FontAwesome6 is a LaTeX package that provides access to the [Font Awesome 6](https://fontawesome.com/) icon set. It enables you to easily include high-quality icons in your LaTeX documents, presentations, and posters.

## Features

- Access to hundreds of Font Awesome 6 icons
- Supports both regular and solid styles
- Easy-to-use commands for inserting icons
- Works with PDFLaTeX, XeLaTeX, and LuaLaTeX
- Compatible with all styles of Pro version (requires a paid license)

## Installation

The package is available on [CTAN](https://ctan.org/pkg/fontawesome6). You can install it using your TeX distribution:

- **TeX Live:**  
    ```
    tlmgr install fontawesome6
    ```
- **MiKTeX:**  
    ```
    mpm --install fontawesome6
    ```

Alternatively, copy the package files to your local texmf tree.

## Usage

Add the following to your document preamble:

```latex
\usepackage{fontawesome6}
% or directly setting the global style
\usepackage[style=solid|regular]{fontawesome6}
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
\usepackage[pro, style=solid|regular|light|thin|duotone-solid|duotone-regular|duotone-light|duotone-thin|sharp-solid|sharp-regular|sharp-light|sharp-thin|sharp-duotone-solid|sharp-duotone-regular|sharp-duotone-light|sharp-duotone-thin]{fontawesome6}
```

Then, use the same commands as above to insert icons. For duotone icons, you can set the secondary color:

```latex
  % Remember to load xcolor
  % Set secondary color to green
  \faDuotoneSetSecondary{\color{green}}
```

## Icon List

For a full list of available icons and their names, see the [package documentation](doc/fontawesome6.pdf) or the [Font Awesome icon gallery](https://fontawesome.com/icons).

## Example

```latex
\documentclass{article}
\usepackage{fontawesome6}
\begin{document}

\faGithub \quad
\fauser \quad
\faAddressBook

\end{document}
```

## Acknowledgments

Special thanks to Marcel Krüger for creating the original [fontawesome5](https://ctan.org/pkg/fontawesome5) package, which served as the foundation for this package.

## Documentation

Comprehensive documentation is available in [`doc/fontawesome6.pdf`](doc/fontawesome6.pdf).

## License

This package is distributed under the [LaTeX Project Public License (LPPL)](https://www.latex-project.org/lppl/).

---

*FontAwesome6 is not affiliated with or endorsed by Fonticons, Inc.*
