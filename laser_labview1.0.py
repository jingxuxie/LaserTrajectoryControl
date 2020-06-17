# -*- coding: utf-8 -*-
"""
Created on Tue Sep 17 21:51:31 2019

@author: Jingxu Xie email:jingxuxie@berkeley.edu

v1.0 跟随鼠标路径画直线，0关闭激光，显示绿色，安全，1打开激光，红色危险，按q退出，按x清除并重新画线
"""

import numpy as np
import cv2

def Bresenham_Algorithm(x0,y0,x1,y1):#返回值为list
    xindex=[]
    yindex=[]    
    xindex.append(x0)#记录初始位置，最终数组中两条线的交点始末点会重复一次
    yindex.append(y0)
    dx=abs(x1-x0)
    dy=abs(y1-y0)
    InclineRate=0#斜率小于45度
    if dx<dy:
        InclineRate=1#斜率大于45度
        x0,y0=y0,x0
        x1,y1=y1,x1
        dx,dy=dy,dx
    dx=abs(x1-x0)
    dy=abs(y1-y0)
    x=x0
    y=y0
    d=dy*2-dx
    
    if (x1-x0)>0:
        ix=1
    else:
        ix=-1
    if (y1-y0)>0:
        iy=1
    else:
        iy=-1
    if InclineRate==0:
        while (x!=x1):
            if d<0:
                d+=dy*2
            else:
                d+=(dy-dx)*2
                y+=iy
            #cv2.circle(img,(x,y),1,(0,0,255))
            x+=ix
            xindex.append(x)
            yindex.append(y)
    if InclineRate==1:  
        while (x!=x1):
            if d<0:
                d+=dy*2
            else:
                d+=(dy-dx)*2
                y+=iy
            #cv2.circle(img,(y,x),1,(0,0,255))
            x+=ix
            xindex.append(y)
            yindex.append(x)
            
    return xindex, yindex #返回的是list

def draw_line(event,x,y,flags,param):
    
    global drawing,a,b,e,f,switch,oldpx,oldpy,poswitch,count

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        a,b= x,y
        if count>0:
            posx[count-1].append(oldpx)
            posy[count-1].append(oldpy)
            if switch==0:
                poswitch[count-1].append(np.zeros(len(posx[count-1][0]),dtype=int).tolist())
            if switch==1:
                poswitch[count-1].append((np.zeros(len(posx[count-1][0]),dtype=int)+1).tolist())
        count+=1

    elif event == cv2.EVENT_MOUSEMOVE:

        if drawing == True:
            oldpx,oldpy=Bresenham_Algorithm(b,a,f,e)
            img_copy[oldpx,oldpy,:]=img1[oldpx,oldpy,:].copy()
            oldpx,oldpy=Bresenham_Algorithm(f,e,b,a)#用于二次消除干净，并不清楚bug来源
            #img_copy[oldpx,oldpy,:]=img1[oldpx,oldpy,:].copy()
            if switch==0:
                cv2.line(img_copy,(a,b),(x,y),(0,255,0),1)#关闭，绿色，安全
            if switch==1:
                cv2.line(img_copy,(a,b),(x,y),(0,0,255),1)#打开，红色，危险
            e,f=x,y
            oldpx,oldpy=Bresenham_Algorithm(b,a,f,e)#计算新的线的坐标
            #a,b=x,y
            #print(x,y)
            

    elif event == cv2.EVENT_RBUTTONDOWN:
        oldpx,oldpy=Bresenham_Algorithm(b,a,f,e)
        img_copy[oldpx,oldpy,:]=img0[oldpx,oldpy,:]
        drawing = False
        #a,b=x,y


def main():
    global drawing,a,b,e,f,switch,oldpx,oldpy,poswitch,count,img0,img_copy,posx,posy,img1
    drawing = False # true if mouse is pressed
    a,b,e,f=0,0,0,0
    switch=0#开关
    count=0#计数
    linemax=20#可画的最多线条数
    posx = [list() for i in range(linemax)]#记录位置,创建二维空list
    posy = [list() for i in range(linemax)]
    poswitch = [list() for i in range(linemax)]
    oldpx=[]#记录旧的直线坐标
    oldpy=[]
        
    img0 = np.zeros((800,800,3), np.uint8)
    img1 = np.zeros((800,800,3), np.uint8)+100
    #img0=cv2.imread('test.png')
    img_copy=img0.copy()
    cv2.namedWindow('image')
    cv2.moveWindow('image',300,100)
    cv2.setMouseCallback('image',draw_line)


    while(1):    
        cv2.imshow('image',img_copy)  
        k = cv2.waitKey(1)
        if k == ord('0'):
            switch=0
        if k == ord ('1'):
            switch=1
        if k == ord ('x'):
            count=0#计数清零
            posx = [list() for i in range(linemax)]#位置清零
            posy = [list() for i in range(linemax)]
            poswitch = [list() for i in range(linemax)]
            img_copy=img0.copy()
        if k == ord('q'):
            break
    
    outposx=np.array(posx[0])
    outposy=np.array(posy[0])
    outposwitch=np.array(poswitch[0])
    for i in range(1,count-1):
        outposx=np.hstack((outposx,posx[i]))
        outposy=np.hstack((outposy,posy[i]))
        outposwitch=np.hstack((outposwitch,poswitch[i]))
    OutPut=np.vstack((outposx,outposy))
    OutPut=np.vstack((OutPut,outposwitch))
    OutPut=np.transpose(OutPut)
    #print(OutPut)
    cv2.destroyAllWindows()
    out=OutPut.copy()#通过copy来消除strided arrays
    return out
#np.array([[1000,1000,1000],[1000,10000,10000],[20000,2000,20000]])

    
a=main()
