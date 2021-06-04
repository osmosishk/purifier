#!/usr/bin/env python

from pyzbar import pyzbar
import argparse
import cv2
import numpy as np
import pytesseract
from pytesseract import Output
import re
import os
from datetime import datetime
import random
import shutil
import glob


temp ='output001.jpg'
path = 'sample8_006.jpg'
global outputfile


def readqrcode(filename):
    image = cv2.imread(filename)

    barcodes = pyzbar.decode(image)

    for barcode in barcodes:
        barcodeData = barcode.data.decode("utf-8")
        barcodeType = barcode.type

        text = "{} ({})".format(barcodeData, barcodeType)

        print("[INFO] Found {} barcode: {}".format(barcodeType, barcodeData))
    return barcodeData


def ResizeWithAspectRatio(image, width=None, height=None, inter=cv2.INTER_AREA):
    dim = None
    (h, w) = image.shape[:2]

    if width is None and height is None:
        return image
    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)
    else:
        r = width / float(w)
        dim = (width, int(h * r))

    return cv2.resize(image, dim, interpolation=inter)

def orientpage(filename):
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

    f = open(filename, 'rb')
    img_bytes = f.read()
    f.close()

    image = cv2.imdecode(np.frombuffer(img_bytes, dtype='uint8'), cv2.IMREAD_COLOR)  # Initially decode as color


    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.bitwise_not(gray)

    rot_data = pytesseract.image_to_osd(image);
    ##print("[OSD] " + rot_data)
    rot = re.search('(?<=Rotate: )\d+', rot_data).group(0)

    angle = float(rot)
    if angle > 0:
        angle = 360 - angle
    ##print("[ANGLE] " + str(angle))

    # rotate the image to deskew it
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 0.7)
    rotated = cv2.warpAffine(image, M, (w, h),flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

    #  TODO: Rotated image can be saved here
    ##print(pytesseract.image_to_osd(rotated));

    cv2.imwrite(temp, rotated)


def cropwhitespace(filename,qrcode):
    global outputfile

    img = cv2.imread(filename)  # Read in the image and convert to grayscale

    img = img[:-20, :-20]  # Perform pre-cropping
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = 255 * (gray < 128).astype(np.uint8)  # To invert the text to white
    gray = cv2.morphologyEx(gray, cv2.MORPH_OPEN, np.ones((2, 2), dtype=np.uint8))# Perform noise filtering
    coords = cv2.findNonZero(gray)  # Find all non-zero points (text)
    x, y, w, h = cv2.boundingRect(coords)  # Find minimum spanning bounding box
    rect = img[y:y + h, x:x + w]
    rect = ResizeWithAspectRatio(rect, width=1280)
    now = datetime.now()

    outputfile = qrcode+"_"+now.strftime("%Y%m%d%H%M%S")+str(random.randint(1111, 9999))+".jpg"
    print(outputfile)
    cv2.imwrite(outputfile, rect)
    folderchange(outputfile,qrcode)


    ##cv2.imshow('image', rect)
    ##cv2.waitKey(0)
    ##cv2.destroyAllWindows()


def readtxt(filename):
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
    readimg = cv2.imread(filename)
    h, w, _ = readimg.shape
    gray = cv2.cvtColor(readimg, cv2.COLOR_BGR2GRAY)
    boxes = pytesseract.image_to_boxes(gray)
    for b in boxes.splitlines():
        b = b.split(' ')
        img = cv2.rectangle(readimg, (int(b[1]), h - int(b[2])), (int(b[3]), h - int(b[4])), (0, 255, 0), 2)
    custom_config = r'--oem 1 --psm 12'
    details = pytesseract.image_to_string(gray, output_type=Output.DICT, config=custom_config, lang='eng')
    print(details)
    ##n_boxes = len(details['level'])
    ##for i in range(n_boxes):
    ##    (x, y, w, h) = (details['left'][i],  details['top'][i],  details['width'][i],  details['height'][i])
    ##    cv2.rectangle(gray, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.imshow('img', readimg)
    cv2.waitKey(0)
    ##print(details.keys())



def folderchange(filename,customercode):

    path = customercode+"/"

    if not os.path.isdir(customercode):
        try:
            os.makedirs(path)
        except OSError:
            print("Creation of the directory %s failed" % path)
        else:
            print("Successfully created the directory %s" % path)

    shutil.move(filename, customercode + "/" + filename)




txtfiles = []
for file in glob.glob("*.jpg"):
    txtfiles.append(file)


print(len(txtfiles))

for item in txtfiles:
    qrcodedoc = readqrcode(item)
    orientpage(item)
    cropwhitespace(temp,qrcodedoc)







##readtxt(outputfile)