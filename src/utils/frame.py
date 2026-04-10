from PIL import Image
import numpy as np

def upload_to_frame(upload):
    img = Image.open(upload)
    img = img.convert("RGB")  
    frame = np.array(img)      
    return frame
