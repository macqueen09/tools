# -*- coding: utf-8 -*-

import cv2
import numpy as np
import sys
import time
import random

sys.path.append('/home/makaili/openposeori/build/python/openpose')
import pyopenpose as op

class item():
    def _init_(self):
        self.data = np.array([])
        self.num_fream = 0

def head_size(keypoints):
    head = 5
    if (keypoints[18][0] >1) and (keypoints[17][0] > 1):
        temp_head = 1.5 * abs(keypoints[18][0]-keypoints[17][0])
        head = max(temp_head,head)
    elif (keypoints[15][0] >1) and (keypoints[16][0] > 1):
        temp_head = 2 * abs(keypoints[15][0]-keypoints[16][0])
        head = max(temp_head,head)
    elif (keypoints[5][0] >1) and (keypoints[2][0]>1):
        temp_head = 0.9 * abs(keypoints[5][0] -keypoints[2][0])
        head = max(temp_head,head)
    else:
        print("-head was hard to detect")
        head = 8
    print(int(head)," head ")
    return int(head)

def bresize((x1,y1) , (x2,y2) , keypoints):
    head = head_size(keypoints)
    x1 = max(0,x1-head)
    y1 = max(0,y1-1.5*head)
    x2 = x2 + head
    y2 = y2 + head
    return (int(x1),int(y1)) , (int(x2),int(y2)) , head

def bbound(keypoints):  #shape = 25,3
    x = keypoints[: , 0]
    y = keypoints[: , 1]
    rex = [tx for tx in x if tx>0.05]
    rey = [ty for ty in y if ty>0.05]

    x1 = min(rex)
    y1 = min(rey)
    x2 = max(rex)
    y2 = max(rey)

    (x1,y1),(x2,y2),_ = bresize((x1,y1) , (x2,y2) , keypoints)
    return (x1,y1),(x2,y2)

def f2p_list(afream,datum):
    datum.cvInputData = afream
    opWrapper.emplaceAndPop([datum])
    person_list = datum.poseKeypoints
    return person_list

def v2list(cap,datum):
    allpeople = []
    ifr = 0
    while (cap.isOpened()):
        ret,fream = cap.read()
        if not ret:
            break
        if(ifr%sample==0):
            person_list = f2p_list(fream, datum)
            tempone = item()
            tempone.num_fream = ifr
            tempone.data = person_list
            allpeople.append(tempone)
        ifr += 1
    return allpeople, ifr


# input 3 dims data , compute distance of 2 dims of two numbers
# part1 dim is: 1*3 like [15,17,0.5] 
def part_distance(part1,part2): 
    part1 = part1[:2]
    part2 = part2[:2]
    res_distance = np.sqrt(np.sum(np.square(part1-part2)))
    return res_distance

def crop_one_person(fileread,one_person_in_fream,num_fream,outputdir,bigarea=0):
    #one_person_in_fream is one person's keypoints
    ## num_fream is begin fream of crop
    cape = cv2.VideoCapture(fileread)
    fsize_c = (int(cape.get(cv2.CAP_PROP_FRAME_WIDTH)),
        int(cape.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    fps = cape.get(cv2.CAP_PROP_FPS)

    (x1,y1),(x2,y2) = bbound(one_person_in_fream)
    senterx = x1 + (x2-x1)/2
    sentery = y1 + (y2-y1)/2
    w = x2-x1
    h = y2-y1

    X = 200
    realW = max(w,200)
    realH = max(h,200)
    ran_name = outputdir+"/out_"+str(random.randint(1,10000))+".avi"

    if bigarea>10:
        X = bigarea
    fileout_lips = cv2.VideoWriter(ran_name, \
        cv2.VideoWriter_fourcc('M','J','P','G'),10,(X,X))

    while(cape.isOpened()):
        cret,cfreame = cape.read()
        if(cape.get(cv2.CAP_PROP_POS_FRAMES)<num_fream):
            continue
        if (not cret) or (cape.get(cv2.CAP_PROP_POS_FRAMES)+65>TotalFreamNum) \
          or(cape.get(cv2.CAP_PROP_POS_FRAMES) - num_fream)>64:
            break
        # resize senterx,sentery   to forbiden out of range
        
        if(senterx + X/2 > fsize_c[0]):
            senterx = fsize_c[0] - X/2 
        if(senterx - X/2 < 0):
            senterx = X/2 
        if(sentery + X/2 > fsize_c[1]):
            sentery = fsize_c[1] - X/2 
        if(sentery - X/2 < 0):
            sentery = X/2 

        a1=int(senterx) -X/2
        a2=int(senterx) +X/2
        b1=int(sentery) -X/2
        b2=int(sentery) +X/2
        freamout = cfreame[b1:b2 , a1:a2]

        fileout_lips.write(freamout)
    cape.release()
    fileout_lips.release()


def eat_crop(fileread,video_p_l,outputdir):
    print(len(video_p_l),"---0-00-0-0")
    for allpeople_a_fream in video_p_l:
    #allpeople_a_fream is: all person keypoint in a fream
        print(type(allpeople_a_fream),'-------------')
        for one_person_in_fream in allpeople_a_fream.data:
            # recognize every person in this fream
            # head-hand distance less a length of head
            if(min(part_distance(one_person_in_fream[4],one_person_in_fream[0]),  \
                   part_distance(one_person_in_fream[7],one_person_in_fream[0])  )\
                   < 2.2*head_size(one_person_in_fream) ):

                crop_one_person(fileread,one_person_in_fream,allpeople_a_fream.num_fream,outputdir)

def all_people_crop_big_area(fileread,video_p_l,outputdir):
    for allpeople_a_fream in video_p_l:
        for one_person_in_fream in allpeople_a_fream.data:
            crop_one_person(fileread,one_person_in_fream,allpeople_a_fream.num_fream,outputdir,500)


fileread = r'1eat.mp4'
cap = cv2.VideoCapture(fileread)
params = dict()
params["model_folder"] = "/home/makaili/openposeori/models/"
params["num_gpu"] = 1
params["write_images"] = "/home/makaili/openposeori/out2/"


opWrapper = op.WrapperPython() # repare the  model
opWrapper.configure(params)
opWrapper.start()

datum = op.Datum()
tic = time.clock()
sample = 20 # a imort args, whis stand: after sample fream has a pose detect
# video 2 keypoint list ,out is people list in every some fream in video
video_p_l,TotalFreamNum = v2list(cap,datum)
cap.release()

outputdir = 'out2/eat'
print("video_p_l length",len(video_p_l))
eat_crop(fileread,video_p_l,outputdir)
print("successful end in %.2f seconds"%(time.clock()-tic))
