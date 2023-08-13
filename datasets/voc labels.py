import xml.etree.ElementTree as ET
import pickle
import os
from os import listdir, getcwd
from os.path import join
sets = ['train', 'test', 'val']
classes = ['YJV_0.6_1kV_4x35', 'YJV_0.6_1kV_4x120', 'YJV_0.6_1kV_4x185', 'YJV_0.6_1kV_4x240',
           'YJV_8.7_10kV_3x70', 'YJV_26_35kV_1x630', 'ZA_YJV_8.7_10kV_3x120',
           'ZA_YJV_8.7_10kV_3x240', 'ZA_YJV_8.7_10kV_3x400', 'ZA_YJV_26_35kV_3x400']

def convert(size, box):
    dw = 1. / size[0]
    dh = 1. / size[1]
    x = (box[0] + box[1]) / 2.0
    y = (box[2] + box[3]) / 2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return (x, y, w, h)

def convert_annotation(image_id):
    in_file = open('voc/Annotations/%s.xml' % (image_id))
    out_file = open('voc/labels/%s.txt' % (image_id), 'w')
    tree = ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)
    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in classes or int(difficult) == 1:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text),
             float(xmlbox.find('xmax').text),
             float(xmlbox.find('ymin').text),
             float(xmlbox.find('ymax').text))
        bb = convert((w, h), b)
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')

wd = getcwd()
print(wd)
for image_set in sets:
    if not os.path.exists('voc/labels/'):
        os.makedirs('voc/labels/')
    image_ids = open('voc/ImageSets/%s.txt' % (image_set)).read().strip().split()
    list_file = open('voc/%s.txt' % (image_set), 'w')
    for image_id in image_ids:
        list_file.write('datasets/voc/images/%s.jpg\n' % (image_id))
        convert_annotation(image_id)
    list_file.close()
