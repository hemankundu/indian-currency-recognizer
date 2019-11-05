import cv2
from os.path import basename
from os import listdir
#import numpy as np
#from glob import glob

def get_contours(img):
    imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(imgray, 150, 255, 0)
    contours, hierarchy = cv2.findContours(thresh, 1, 2)
    size = get_size(img)
    contours = [cc for cc in contours if contourOK(cc, size)]
    return contours

def get_size(img):
    ih, iw = img.shape[:2]
    return iw * ih

def contourOK(cc, size=1000000):
    x, y, w, h = cv2.boundingRect(cc)
    if w < 50 or h < 50: return False # too narrow or wide is bad
    area = cv2.contourArea(cc)
    rt = area < (size * 0.8) and area > 200
    if not rt:
      print("ignoring..")
    else:
      print("ok")
    return rt

def find_boundaries(img, contours):
    # margin is the minimum distance from the edges of the image, as a fraction
    ih, iw = img.shape[:2]
    minx = iw
    miny = ih
    maxx = 0
    maxy = 0

    for cc in contours:
        x, y, w, h = cv2.boundingRect(cc)
        if x < minx: minx = x
        if y < miny: miny = y
        if x + w > maxx: maxx = x + w
        if y + h > maxy: maxy = y + h

    return (minx, miny, maxx, maxy)

def crop(img, boundaries):
    minx, miny, maxx, maxy = boundaries
    return img[miny:maxy, minx:maxx]

def process_image(src_path, dst_path,fname):
    img = cv2.imread(src_path + fname)
    img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
    # alpha = 1.2
    # beta = 0
    # for y in range(img.shape[0]):
    #     for x in range(img.shape[1]):
    #         for c in range(img.shape[2]):
    #             img[y,x,c] = np.clip(alpha*img[y,x,c] + beta, 0, 255)
    contours = get_contours(img)
    #cv2.drawContours(img, contours, -1, (0,255,0)) # draws contours, good for debugging
    bounds = find_boundaries(img, contours)
    cropped = crop(img, bounds)
    
    if cropped.shape[0] > 250 and cropped.shape[1] > 250:
        cv2.imwrite(dst_path + fname, cropped)

def preprocess_captured():
    for f in listdir('captured/'):
        process_image("captured/", "preprocessed/", f)

# def is_object_present(img_path):
#     img = cv2.imread(img_path)
#     shape = img.shape
#     print("Shapes of preprocessed image is:", shape)
#     return not (shape[0]<250 and shape[1]<250)

if __name__ == "__main__":
    preprocess_captured()