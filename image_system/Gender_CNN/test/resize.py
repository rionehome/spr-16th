from PIL import Image
import glob


man_path = './original_data/man/*'
woman_path = './original_data/woman/*'


for f in glob.glob(man_path):
    img = Image.open(f).resize((128, 128))
    img.save(f.replace('original', 'teacher'))

for f in glob.glob(woman_path):
    img = Image.open(f).resize((128, 128))
    img.save(f.replace('original', 'teacher'))