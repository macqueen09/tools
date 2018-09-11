#!/usr/bin/python
# -*- coding: UTF-8 -*-
# in pic
# out bin
from scipy.io import loadmat
import argparse
import os
import sys
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mping
import math,Image
from Queue import Queue
from threading import Thread,current_thread
import struct
from scipy.misc import imsave
from PIL import Image

def dataset(data_dir, name, num_sample_size = 10000):
    #
    #
    filename = os.path.join(data_dir, name+ '_32x32.mat')
    if not os.path.join(filename):
        raise ValueError('Please supply a the file')
    datadict = loadmat(filename)    
    train_x = datadict['X']
    train_x = train_x.transpose((3,0,1,2))
    train_y = datadict['y'].flatten()

    train_y[train_y==10] = 0
    train_x = train_x[:num_sample_size]
    train_y = train_y[:num_sample_size]

    return train_x, train_y


def split_dataset(train_x, train_y, validation_size):
    return (train_x[:-validation_size],
            train_y[:-validation_size],
            train_x[-validation_size:],
            train_y[-validation_size:])

def convert2bin(images,labels,fileName):
    binaryValue = []
    file = open(fileName,"wb")
    try:
        print (images.shape,labels[0])
        print(labels[0:10])

        width = images[0].shape[0]

        # for index in range(images.shape[0]): # number of example
        #     parsedata = struct.pack("?",np.array(labels[index]))
        #     # print ('label is : ',struct.unpack("b",parsedata)),
        #     file.write(parsedata)
        #     for rgb in range(3):
        #         for j in range(width):
        #             for i in range(width):
        #                 temp = struct.pack("i",np.array(images[index][i][j][rgb]))
        #                 file.write(temp)

    finally:
        file.close()
        print("write file success",fileName)

def view(filename):
    num = 2
    bytestream = open(filename, "rb")
    buf = bytestream.read(num * (1 + 32 * 32 * 3))

    bytestream.close()
     
    data = np.frombuffer(buf, dtype=np.uint8)
    data = data.reshape(num, 1 + 32*32*3)
    labels_images = np.hsplit(data, [1])

    labels = labels_images[0].reshape(num)
    images = labels_images[1].reshape(num, 32, 32, 3)
     
    img = np.reshape(images[1], (3, 32, 32)) 
    print("one ori label is :",labels[1])

    img = img.transpose( 1, 2 , 0)#102
    print("after img size is : ",img.shape)
    
    imsave("cifar.jpg", img)
    plt.imshow(img)
    # plt.show()
    # return buf,data
    
def pic2bin():
    filename = "data_batch_1.bin"
    filetest = "test_batch.bin"
    classes = ['4','5']
    bytestream = open(filename,"wb")
    # bytestream.write(buf)
    imgspath = os.path.join(os.getcwd(),"pic2tfrecord")
    # print('****',imgspath)
    # lena = mping.imread(img)
    # lena1 = lena[:,:,:]
    # plt.imshow(lena1)
    # plt.show()
    # lena1 = np.uint8(lena1)
    # lena1 = str(lena)
    # bytestream.write(lena1)

    for index,name in enumerate(classes):
        class_path = imgspath + "/" + name + "/"
        i=1
        for img_name in os.listdir(class_path):
            img_path = class_path + img_name
            aimg = mping.imread(img_path)
            # label = np.uint(name) #- np.uint(47)
            label = int(name) 
            # print(str(label)), # here is 0 and 1
            aimg0 = aimg[:,:,0]
            aimg1 = aimg[:,:,1]
            aimg2 = aimg[:,:,2]
            aimg = [aimg0,aimg1,aimg2]
            # for x in range(5):
            bytestream.write(struct.pack('B',(label)))
            bytestream.write(np.array(aimg))
            i=i+1
    # print("****my img size ",type(np.array(aimg)))
    bytestream.close()

def main(unused_argv):
    # train_x, train_y = dataset(FLAGS.directory, 'train')
    # test_x, test_y = dataset(FLAGS.directory, 'test')
    
    # train_x, train_y, valid_x, valid_y = split_dataset(
    #     train_x, train_y, FLAGS.validation_size)

    # trainFileName = os.path.join(FLAGS.directory, 'train.bin')
    # validationFileName = os.path.join(FLAGS.directory, 'validation.bin')
    # testFileName = os.path.join(FLAGS.directory, 'test.bin')

    # convert2bin(train_x, train_y, trainFileName)

    # temp1 = os.path.join(FLAGS.directory, 'ori_1.bin')
    # view(temp1)

    pic2bin()

    # view(os.path.join(FLAGS.directory, 'data_batch_1.bin'))


    print('success end')

# if __name__ ='__main__':
    
parser = argparse.ArgumentParser()
parser.add_argument(
    '--directory',
    type = str,
    default = '/home/mkl/Documents/tensorflow_model/models/tutorials/image/cifar10/temp/svhn',
    help = 'Directory to download data files and write the converted result'
    )
parser.add_argument(
    '--validation_size',
    type = int,
    default = 5000,
    help = """\
    Number of example to separate from the training data for the validation
    """)

FLAGS, unparsed = parser.parse_known_args()
print('FLAG: ',FLAGS,'  unparsed  ',unparsed)
tf.app.run(main=main, argv=[sys.argv[0]] + unparsed)
