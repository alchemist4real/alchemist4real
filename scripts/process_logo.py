import cv2
import numpy as np
from PIL import Image
import os

src_path = r'C:\Users\Thosiba\.gemini\antigravity\brain\edc77f85-0b6d-421b-bf5e-63f9cf72f391\.user_uploaded\media_1786437768875.jpg'
assets_dir = r'd:\DOWNLOAD\alchemist4real\assets'
os.makedirs(assets_dir, exist_ok=True)

# Save copy of original input
with open(src_path, 'rb') as f_in, open(os.path.join(assets_dir, 'logo-original.jpg'), 'wb') as f_out:
    f_out.write(f_in.read())

# Read image
img = cv2.imread(src_path, cv2.IMREAD_COLOR)
h, w, _ = img.shape
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Flood fill outer white background from outer edges
mask = np.zeros((h + 2, w + 2), np.uint8)

# Flood fill from all border pixels
border_pts = []
for x in range(w):
    border_pts.append((x, 0))
    border_pts.append((x, h-1))
for y in range(h):
    border_pts.append((0, y))
    border_pts.append((w-1, y))

for x, y in border_pts:
    if gray[y, x] > 200:
        cv2.floodFill(gray, mask, (x, y), 255, loDiff=25, upDiff=25, flags=4 | (255 << 8) | cv2.FLOODFILL_MASK_ONLY)

outer_bg = mask[1:h+1, 1:w+1]

# Create Alpha channel:
# Inner region: 255 (opaque white details + black artwork)
# Outer region: 0 for transparent background, smooth alpha transition near dark artwork edge
rgba = np.zeros((h, w, 4), dtype=np.uint8)
rgba[:, :, 0:3] = img

alpha = np.full((h, w), 255, dtype=np.uint8)

# Calculate clean alpha for outer flood-filled region
outer_gray = gray.astype(float)
# Outer background pixels:
# If pixel intensity > 235, alpha is 0.
# If pixel intensity is lower (dark line edges), alpha transitions smoothly:
alpha_outer = np.clip((240.0 - outer_gray) * 3.0, 0, 255).astype(np.uint8)
alpha[outer_bg > 0] = alpha_outer[outer_bg > 0]

# Clean up near-zero noise
alpha[alpha < 12] = 0

rgba[:, :, 3] = alpha

# Convert BGR to RGB for PIL
rgba_rgb = cv2.cvtColor(rgba, cv2.COLOR_BGRA2RGBA)
pil_logo = Image.fromarray(rgba_rgb)

# 1. Save main high-res transparent logo (1024x1024)
pil_logo.save(os.path.join(assets_dir, 'logo.png'), 'PNG')
print("Saved assets/logo.png")

# 2. Pure monochrome black logo on transparent background
mono_rgba = np.zeros((h, w, 4), dtype=np.uint8)
# Luminance alpha: black lines are opaque
lum_alpha = np.clip((245.0 - gray.astype(float)) * 2.0, 0, 255).astype(np.uint8)
lum_alpha[alpha == 0] = 0
mono_rgba[:, :, 3] = lum_alpha
pil_mono_logo = Image.fromarray(mono_rgba)
pil_mono_logo.save(os.path.join(assets_dir, 'logo-monochrome.png'), 'PNG')

# 3. White monochrome logo for dark mode
white_rgba = np.full((h, w, 4), 255, dtype=np.uint8)
white_rgba[:, :, 3] = lum_alpha
pil_white_logo = Image.fromarray(white_rgba)
pil_white_logo.save(os.path.join(assets_dir, 'logo-white.png'), 'PNG')

# 4. Square Logo Icon (Cropped tight around emblem with padding)
# Find bounding box of non-transparent pixels in pil_logo
bbox = pil_logo.getbbox()
if bbox:
    cropped = pil_logo.crop(bbox)
else:
    cropped = pil_logo

cw, ch = cropped.size
padding = int(max(cw, ch) * 0.05) # 5% padding
max_dim = max(cw, ch) + 2 * padding

icon_canvas = Image.new('RGBA', (max_dim, max_dim), (0, 0, 0, 0))
icon_canvas.paste(cropped, ((max_dim - cw) // 2, (max_dim - ch) // 2))

# Save logo-icon.png (512x512)
logo_icon = icon_canvas.resize((512, 512), Image.Resampling.LANCZOS)
logo_icon.save(os.path.join(assets_dir, 'logo-icon.png'), 'PNG')
print("Saved assets/logo-icon.png (512x512)")

# 5. Apple Touch Icon (180x180)
# Create apple touch icon (can be transparent or on sleek dark/light background)
apple_icon = icon_canvas.resize((180, 180), Image.Resampling.LANCZOS)
apple_icon.save(os.path.join(assets_dir, 'apple-touch-icon.png'), 'PNG')

# 6. Favicon 32x32 & 16x16
fav32 = icon_canvas.resize((32, 32), Image.Resampling.LANCZOS)
fav32.save(os.path.join(assets_dir, 'favicon-32x32.png'), 'PNG')

fav16 = icon_canvas.resize((16, 16), Image.Resampling.LANCZOS)
fav16.save(os.path.join(assets_dir, 'favicon-16x16.png'), 'PNG')

# 7. ICO file
icon_canvas.save(
    os.path.join(assets_dir, 'favicon.ico'),
    format='ICO',
    sizes=[(16, 16), (32, 32), (48, 48), (64, 64)]
)

# 8. Generate SVG Wrapper / Favicon SVG
svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {max_dim} {max_dim}">
  <image href="logo-icon.png" width="{max_dim}" height="{max_dim}" />
</svg>'''
with open(os.path.join(assets_dir, 'favicon.svg'), 'w', encoding='utf-8') as f:
    f.write(svg_content)

print("Generated all logo & favicon assets successfully!")
