import cv2
import numpy

def img_to_buffer(img: numpy.ndarray):
    success, img_buffer = cv2.imencode('.png',img)
    return img_buffer

def buffer_to_img(buffer):
    nparr = numpy.frombuffer(buffer, numpy.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img