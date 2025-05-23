-- Copyright 2025 Daniel Nagel
--
-- This work may be distributed and/or modified under the
-- conditions of the LaTeX Project Public License, either version 1.3c
-- of this license or (at your option) any later version.
-- The latest version of this license is in
--   http://www.latex-project.org/lppl.txt
-- and version 1.3 or later is part of all distributions of LaTeX
-- version 2005/12/01 or later.
--
-- This work has the LPPL maintenance status `maintained'.
-- 
-- The Current Maintainer of this work is Daniel Nagel
--

function fontawesome6_analyze_current_font(fontid)
  for name, value in pairs(font.getfont(fontid).resources.unicodes) do
    tex.sprint(
      luatexbase.catcodetables.expl,
      "\\exp_args:NNc\\tex_global:D\\tex_chardef:D{c__fontawesome_slot_" .. name .. '_char}' .. value .. '\\scan_stop:')
    tex.sprint(
      luatexbase.registernumber("CatcodeTableExpl"),
      "\\cs_gset_protected:Npn"
        .. string.gsub('\\fa-' .. name, '-(%w)', string.upper)
        .. "{\\faPreselectedIcon{" .. name .. "}}")
  end
end
