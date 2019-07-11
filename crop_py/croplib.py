# -*- coding: utf-8 -*-


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
    x1 = max(0,x1-1.5*head)
    y1 = max(0,y1-2.5*head)
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