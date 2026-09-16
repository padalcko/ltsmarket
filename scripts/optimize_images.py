"""Generate WebP display variants; retain all original images. Requires Pillow."""
from pathlib import Path
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]
for source in (ROOT / 'assets/img').rglob('*'):
    if not source.is_file() or source.suffix.lower() not in ('.webp', '.png') or 'optimized' in source.parts:
        continue
    with Image.open(source) as original:
        original = ImageOps.exif_transpose(original)
        for size in (320, 480, 960, 1440):
            target = ROOT / 'assets/img/optimized' / source.relative_to(ROOT / 'assets/img').with_suffix('')
            target = target.with_name(target.name + f'-{size}.webp')
            target.parent.mkdir(parents=True, exist_ok=True)
            copy = original.copy()
            width = min(size, original.width)
            copy = original.resize((width, round(original.height * width / original.width)), Image.Resampling.LANCZOS)
            copy.save(target, 'WEBP', quality=82, method=4)
