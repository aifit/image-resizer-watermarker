{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  name = "image-resizer-watermarker-env";

  buildInputs = with pkgs; [
    # Python 3.8+ with Pillow
    (python3.withPackages (ps: with ps; [
      pillow
    ]))
  ];

  shellHook = ''
    echo "🖼️  Image Resizer & Watermarker Environment"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "Python version: $(python --version)"
    echo "Pillow installed: $(python -c 'import PIL; print(PIL.__version__)')"
    echo ""
    echo "📂 Required folder structure:"
    echo "   • input-images/     → Place original images here"
    echo "   • output/           → Processed images saved here"
    echo "   • landscape-watermark.png"
    echo "   • portrait-watermark.png"
    echo ""
    echo "▶️  Run: python script.py"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  '';
}
