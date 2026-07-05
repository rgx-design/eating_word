from PIL import Image
import os

PNG_DIR = 'png'

for filename in os.listdir(PNG_DIR):
    if not filename.endswith('.png'):
        continue
    
    filepath = os.path.join(PNG_DIR, filename)
    print(f'Processing: {filename}...')
    
    try:
        img = Image.open(filepath).convert('RGBA')
        datas = img.getdata()
        
        new_data = []
        for item in datas:
            r, g, b, a = item
            if r > 240 and g > 240 and b > 240:
                new_data.append((r, g, b, 0))
            else:
                new_data.append(item)
        
        img.putdata(new_data)
        img.save(filepath)
        print(f'  Done: {filename}')
        
    except Exception as e:
        print(f'  Failed: {filename} - {e}')

print('All images processed!')
