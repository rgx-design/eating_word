from PIL import Image
import os

PNG_DIR = 'png'

def isLightCyan(r, g, b):
    brightness = (r + g + b) / 3
    if brightness < 180:
        return False
    green_blue_diff = abs(g - b)
    r_ratio = r / max(brightness, 1)
    return green_blue_diff < 40 and r_ratio < 0.95 and g > 180 and b > 180

for filename in os.listdir(PNG_DIR):
    if not filename.endswith('.png'):
        continue
    
    filepath = os.path.join(PNG_DIR, filename)
    print(f'Processing: {filename}...')
    
    try:
        img = Image.open(filepath).convert('RGBA')
        datas = img.getdata()
        
        new_data = []
        removed = 0
        for item in datas:
            r, g, b, a = item
            if (r > 240 and g > 240 and b > 240) or isLightCyan(r, g, b):
                new_data.append((r, g, b, 0))
                removed += 1
            else:
                new_data.append(item)
        
        img.putdata(new_data)
        img.save(filepath)
        print(f'  Done: {filename} (removed {removed} pixels)')
        
    except Exception as e:
        print(f'  Failed: {filename} - {e}')

print('All images processed!')
