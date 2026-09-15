import os
import zlib
import struct

def create_png_icon(width, height, is_maskable, filename):
    # Colors: deep indigo gradient feel: #4f46e5 (79, 70, 229) and white #ffffff
    r_bg, g_bg, b_bg = 79, 70, 229
    r_fg, g_fg, b_fg = 255, 255, 255
    r_dark, g_dark, b_dark = 67, 56, 202
    
    center_x, center_y = width / 2.0, height / 2.0
    safe_radius = width * (0.38 if is_maskable else 0.44)
    inner_radius = width * (0.24 if is_maskable else 0.28)
    
    raw = bytearray()
    for y in range(height):
        raw.append(0)  # Filter None
        # subtle vertical gradient
        grad_factor = y / float(height)
        cur_bg_r = int(r_bg * (1 - grad_factor * 0.2) + r_dark * (grad_factor * 0.2))
        cur_bg_g = int(g_bg * (1 - grad_factor * 0.2) + g_dark * (grad_factor * 0.2))
        cur_bg_b = int(b_bg * (1 - grad_factor * 0.2) + b_dark * (grad_factor * 0.2))

        for x in range(width):
            dist = ((x - center_x)**2 + (y - center_y)**2)**0.5
            
            if not is_maskable and dist > (width * 0.48):
                # transparent corner for non-maskable rounded icon
                raw.extend((0, 0, 0, 0))
            elif dist <= inner_radius:
                # Center logo badge
                raw.extend((r_fg, g_fg, b_fg, 255))
            elif dist <= inner_radius + (width * 0.04):
                # Accent ring
                raw.extend((224, 231, 255, 255))
            else:
                # Brand background
                raw.extend((cur_bg_r, cur_bg_g, cur_bg_b, 255))

    compressor = zlib.compressobj()
    compressed = compressor.compress(bytes(raw)) + compressor.flush()
    
    def chunk(chunk_type, data):
        c = chunk_type + data
        crc = struct.pack('>I', zlib.crc32(c) & 0xffffffff)
        return struct.pack('>I', len(data)) + c + crc
        
    png = b'\x89PNG\r\n\x1a\n'
    png += chunk(b'IHDR', struct.pack('>IIBBBBB', width, height, 8, 6, 0, 0, 0))
    png += chunk(b'IDAT', compressed)
    png += chunk(b'IEND', b'')
    
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'wb') as f:
        f.write(png)
    print(f"Generated {filename}")

# Generate PNGs
create_png_icon(192, 192, False, 'public/pwa-192x192.png')
create_png_icon(512, 512, False, 'public/pwa-512x512.png')
create_png_icon(512, 512, True, 'public/pwa-maskable-512x512.png')
create_png_icon(180, 180, False, 'public/apple-touch-icon.png')

# Generate SVG
svg_content = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512">
  <defs>
    <linearGradient id="pwaGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#6366f1"/>
      <stop offset="100%" stop-color="#4338ca"/>
    </linearGradient>
  </defs>
  <rect width="512" height="512" rx="128" fill="url(#pwaGrad)"/>
  <circle cx="256" cy="256" r="140" fill="#ffffff" opacity="0.15"/>
  <circle cx="256" cy="256" r="110" fill="#ffffff"/>
  <!-- SP Brand monogram / Academic emblem -->
  <path d="M210 210 Q256 185 302 210 L302 295 Q256 270 210 295 Z" fill="#4f46e5" stroke="#4f46e5" stroke-width="8" stroke-linejoin="round"/>
  <path d="M256 200 L256 275" stroke="#ffffff" stroke-width="5" stroke-linecap="round"/>
  <path d="M220 330 L292 330" stroke="#4f46e5" stroke-width="8" stroke-linecap="round"/>
</svg>'''

with open('public/icon.svg', 'w') as f:
    f.write(svg_content)
print("Generated public/icon.svg")
