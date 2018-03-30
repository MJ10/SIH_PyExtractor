from __future__ import print_function
import tensorflow as tf
import numpy as np
import os, sys, cv2, shutil
import glob
import shutil
import pytesseract
import subprocess
from server.preprocess import Preprocessing
from PIL import Image
sys.path.append(os.path.join(os.getcwd(), 'server', 'seg_model'))
from lib.networks.factory import get_network
from lib.fast_rcnn.config import cfg,cfg_from_file
from lib.fast_rcnn.test import test_ctpn
from lib.utils.timer import Timer
from lib.text_connector.detectors import TextDetector
from lib.text_connector.text_connect_cfg import Config as TextLineCfg


cfg_from_file('server/seg_model/ctpn/text.yml')

# init session
config = tf.ConfigProto(allow_soft_placement=True)
sess = tf.Session(config=config)
# load network
net = get_network("VGGnet_test")
# load model
print(('Loading network {:s}... '.format("VGGnet_test")), end=' ')
saver = tf.train.Saver()
pr = Preprocessing()
l = []
global curr_s
try:
    ckpt = tf.train.get_checkpoint_state(cfg.TEST.checkpoints_path)
    # print('Restoring from {}...'.format(ckpt.model_checkpoint_path), end=' ')
    saver.restore(sess, ckpt.model_checkpoint_path)
    # print('done')
except:
    raise 'Check your pretrained {:s}'.format(ckpt.model_checkpoint_path)

def resize_im(im, scale, max_scale=None):
    f=float(scale)/min(im.shape[0], im.shape[1])
    if max_scale!=None and f*max(im.shape[0], im.shape[1])>max_scale:
        f=float(max_scale)/max(im.shape[0], im.shape[1])
    return cv2.resize(im, None,None, fx=f, fy=f,interpolation=cv2.INTER_LINEAR), f

def draw_boxes(img,image_name,boxes,scale):
    global curr_s
    count = 0
    for box in boxes:
        if box[8]>=0.9:
            color = (0,255,0)
        elif box[8]>=0.8:
            color = (255,0,0)
        # cv2.line(img, (int(box[0]), int(box[1])), (int(box[2]), int(box[3])), color, 2)
        # cv2.line(img, (int(box[0]), int(box[1])), (int(box[4]), int(box[5])), color, 2)
        # cv2.line(img, (int(box[6]), int(box[7])), (int(box[2]), int(box[3])), color, 2)
        # cv2.line(img, (int(box[4]), int(box[5])), (int(box[6]), int(box[7])), color, 2)
        count = count+1

        mask = np.zeros(img.shape, dtype=np.uint8)
        roi_corners = np.array([[(int(box[0]),int(box[1])),(int(box[2]),int(box[3])),(int(box[6]),int(box[7])),(int(box[4]),int(box[5]))]], dtype=np.int32)
        channel_count = img.shape[2]
        ignore_mask_color = (255,)*channel_count
        cv2.fillPoly(mask, roi_corners, ignore_mask_color)
        masked_image = cv2.bitwise_and(img.copy(), mask)
        cv2.imwrite('server/res/result' + str(count) + '.png', masked_image)
        im = Image.open('server/res/result' + str(count) + '.png')
        crop_rectangle = (min([int(box[0]),int(box[4])]), min([int(box[1]),int(box[3])]),
                            max([int(box[2]),int(box[6])]), max([int(box[5]),int(box[7])]))
        cropped_im = im.crop(crop_rectangle)
        # cropped_im = cv2.cvtColor(cropped_im, cv2.COLOR_BGR2GRAY)
        cropped_im.save('server/res/result' + str(count) + '.png', dpi=(600,600))
        image = cv2.imread('server/res/result' + str(count) + '.png')
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        cv2.imwrite('server/res/result' + str(count) + '.png', gray_image)
        # subprocess.run(['python', 'server/process.py', 'server/res/result' + str(count) + '.png',
        #                 'server/res/result' + str(count) + '.png'])
        subprocess.run(['server/scripts/textcleaner', 'server/res/result' + str(count) + '.png', 
                        'server/res/result' + str(count) + '.png'])
        pr.preprocess('server/res/result' + str(count) + '.png', 'server/res/result' + str(count) + '.png')
        # a = cv2.imread('res/result' + str(count) + '.png')
        # preprocess.img_x = len(a)
        # preprocess.img_y = len(a[0])
        # preprocess.preprocess('res/result' + str(count) + '.png', 'res/result' + str(count) + '.png')
        s = extract_text('server/res/result' + str(count) + '.png')
        print(s)
        l.append(s)
        folder = 'server/res/'
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(e)

# def draw_boxes(img,image_name,boxes,scale):
#     for box in boxes:
#         if box[8]>=0.9:
#             color = (0,255,0)
#         elif box[8]>=0.8:
#             color = (255,0,0)
#         cv2.line(img, (int(box[0]), int(box[1])), (int(box[2]), int(box[3])), color, 2)
#         cv2.line(img, (int(box[0]), int(box[1])), (int(box[4]), int(box[5])), color, 2)
#         cv2.line(img, (int(box[6]), int(box[7])), (int(box[2]), int(box[3])), color, 2)
#         cv2.line(img, (int(box[4]), int(box[5])), (int(box[6]), int(box[7])), color, 2)

#     base_name = image_name.split('/')[-1]
#     img=cv2.resize(img, None, None, fx=1.0/scale, fy=1.0/scale, interpolation=cv2.INTER_LINEAR)
#     cv2.imwrite(os.path.join("data/results", base_name), img)

def ctpn(sess, net, image_name):
    img = cv2.imread(image_name)
    img, scale = resize_im(img, scale=TextLineCfg.SCALE, max_scale=TextLineCfg.MAX_SCALE)
    scores, boxes = test_ctpn(sess, net, img)

    textdetector = TextDetector()
    boxes = textdetector.detect(boxes, scores[:, np.newaxis], img.shape[:2])
    # print(boxes)
    draw_boxes(img, image_name, boxes, scale)

def extract_text(input_file):
    return pytesseract.image_to_string(Image.open(input_file), lang='hin+tam+tel')

def segment_images(image_folder):
    global curr_s
    im_names = glob.glob(os.path.join(image_folder, '*.png')) + \
        glob.glob(os.path.join(image_folder, '*.jpg')) + \
        glob.glob(os.path.join(image_folder, '*.jpeg'))
        

    for im_name in im_names:
        curr_s = ''
        ctpn(sess, net, im_name)
        print(curr_s)
        l.append(curr_s)
    return l
