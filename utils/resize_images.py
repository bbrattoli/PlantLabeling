from joblib import Parallel, delayed
from PIL import Image
import time
import os

def img_resize(name,source,dest):
    image = Image.open(source+name)
    w,h = image.size
    image = image.resize((int(w*0.15),int(h*0.15)))
    image.save(dest+name)


path = "./images/"
dest = "./small_images/"
imgs = os.listdir(path)
#imgs = imgs[:10]
with Parallel(n_jobs=24) as parallel:
    parallel(delayed(img_resize)(name,path,dest) for name in imgs)
