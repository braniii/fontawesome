from fontTools.ttLib import TTFont
import os

# Hardcoded font file names and output enc names
fonts = [
    ("FontAwesome6Brands-Regular-400.otf", "fontawesome6brands-regular-400.enc"),
    ("FontAwesome6Free-Regular-400.otf", "fontawesome6free-regular-400.enc"),
    ("FontAwesome6Free-Solid-900.otf", "fontawesome6free-solid-900.enc"),
]

opentype_dir = "opentype"
enc_dir = "enc"

def generate_enc(otf_path, enc_path, enc_name):
    font = TTFont(otf_path)
    glyph_order = font.getGlyphOrder()
    # Remove .notdef and .null if present
    glyph_order = [g for g in glyph_order if not g.startswith('.')]
    with open(enc_path, "w", encoding="utf-8") as f:
        f.write(f"/{enc_name} [\n")
        for glyph in glyph_order:
            f.write(f"/{glyph}\n")
        f.write("] def\n")

if __name__ == "__main__":
    for otf_file, enc_file in fonts:
        otf_path = os.path.join(opentype_dir, otf_file)
        enc_path = os.path.join(enc_dir, enc_file)
        enc_name = enc_file.replace(".enc", "")
        print(f"Generating {enc_path} from {otf_path} ...")
        generate_enc(otf_path, enc_path, enc_name)
    print("Done.")
