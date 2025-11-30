from PIL import Image
import os

if not os.path.exists('media'):
    os.makedirs('media')

img = Image.new('RGB', (300, 300), color = (73, 109, 137))
img.save('media/default.jpg')
print('Created media/default.jpg')
