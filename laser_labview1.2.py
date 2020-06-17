# -*- coding: utf-8 -*-
"""
Created on Fri Sep 20 15:05:33 2019

@author: Jingxu Xie

v1.0 跟随鼠标路径画直线，0关闭激光，显示绿色，安全，1打开激光，红色危险，按q退出，按x清除并重新画线
v1.1 输出结果为始末点坐标，而非线上每个点的坐标，且加入可以实时输出线段长度
v1.2 更改了消除之前画线的方式，记录画过的线，直接用原图覆盖，再重新画，取消算法
"""

import numpy as np
import cv2

def text_position(x1,y1,x2,y2):
    d=np.sqrt((x2-x1)**2+(y2-y1)**2)+0.0001
    x=int(round((x1+x2)/2-60*(y2-y1)/d))
    if x > (x1+x2)/2:
        x=int(round((x1+x2)/2-15*(y2-y1)/d))
    y=int(round((y1+y2)/2+30*(x2-x1)/d))
    if y < (y1+y2)/2:
        y=int(round((y1+y2)/2+20*(x2-x1)/d))
    return x,y

def redraw():#清除并重画
    global posx,posy,poswitch,textposx,textposy,d,img_copy
    img_copy=img0.copy()
    for i in range(len(posx)-1):#绘制之前的线
        if poswitch[i+1]==0:
            cv2.line(img_copy,(posx[i],posy[i]),(posx[i+1],posy[i+1]),(0,255,0),2)
            text=str(round(d[i+1],1))
            cv2.putText(img_copy,text,(textposx[i+1],textposy[i+1]),cv2.FONT_HERSHEY_PLAIN,1.0,[0,255,0],1)
        if poswitch[i+1]==1:
            cv2.line(img_copy,(posx[i],posy[i]),(posx[i+1],posy[i+1]),(0,0,255),2)
            text=str(round(d[i+1],1))
            cv2.putText(img_copy,text,(textposx[i+1],textposy[i+1]),cv2.FONT_HERSHEY_PLAIN,1.0,[0,0,255],1)

def draw_line(event,x,y,flags,param):

    global drawing,a,b,switch,poswitch,count,LengthD,textposx,textposy,d
    global img_copy

    if event == cv2.EVENT_LBUTTONDOWN:      
        drawing = True
        textposx.append(text_position(a,b,x,y)[0])
        textposy.append(text_position(a,b,x,y)[1])
        d.append(np.sqrt((x-a)**2+(y-b)**2))
        a,b= x,y
        posx.append(x)
        posy.append(y)
        if switch==0:
            poswitch.append(0)
        if switch==1:
            poswitch.append(1)
        count+=1

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing == True and LengthD==0:
            redraw()
            if switch==0:
                cv2.line(img_copy,(a,b),(x,y),(0,255,0),2)#关闭，绿色，安全
            if switch==1:
                cv2.line(img_copy,(a,b),(x,y),(0,0,255),2)#打开，红色，危险
            d_temp=np.sqrt((x-a)**2+(y-b)**2)+0.0001
            textposx_temp,textposy_temp=text_position(a,b,x,y)
            text=str(round(d_temp,1))

            if switch==0:
                cv2.putText(img_copy,text,(textposx_temp,textposy_temp),cv2.FONT_HERSHEY_PLAIN,1.0,[0,255,0],1)
            if switch==1:
                cv2.putText(img_copy,text,(textposx_temp,textposy_temp),cv2.FONT_HERSHEY_PLAIN,1.0,[0,0,255],1)
            

    elif event == cv2.EVENT_RBUTTONDOWN:
        redraw()
        drawing = False
        #a,b=x,y


def main():
    global drawing,a,b,switch,poswitch,count,img0,img_copy,posx,posy,LengthD,textposx,textposy,d
    LengthD=0 #给定线的长度
    drawing = False # true if mouse is pressed
    a,b,=0,0
    switch=0#开关
    count=0#计数
    posx = []#记录位置
    posy = []
    poswitch = []
    textposx=[]
    textposy=[]
    d=[]

        
    img0 = np.zeros((800,800,3), np.uint8)
    #img0=cv2.imread('test.png')
    img_copy=img0.copy()
    cv2.namedWindow('image')
    cv2.moveWindow('image',300,100)
    cv2.setMouseCallback('image',draw_line)


    while(1):    
        cv2.imshow('image',img_copy)  
        k = cv2.waitKeyEx(1)
        '''
        if k!=-1:
            ans=k
            print(ans)
            '''
        if k == 2490368:#上
            LengthD+=1
        if k == 2621440:#下
            LengthD-=1
        if k == 2424832:#左
            LengthD-=0.1
        if k == 2555904:#右
            LengthD+=0.1
        if k == ord('5'):#恢复自由
            LengthD=0
            
        if k == ord('0'):#设置关
            switch=0
        if k == ord ('1'):#开
            switch=1
        if k == ord ('x'):#清除重画
            drawing=False
            count=0#计数清零
            posx = []#记录位置
            posy = []
            poswitch = []
            textposx=[]
            textposy=[]
            d=[]
            img_copy=img0.copy()
        if k == ord('q'):#退出
            break
    
    outposx=np.array(posx)
    outposy=np.array(posy)
    outposwitch=np.array(poswitch)

    OutPut=np.vstack((outposx,outposy))
    OutPut=np.vstack((OutPut,outposwitch))
    OutPut=np.transpose(OutPut)
    #print(OutPut)
    cv2.destroyAllWindows()
    out=OutPut.copy()#通过copy来消除strided arrays
    return out
#np.array([[1000,1000,1000],[1000,10000,10000],[20000,2000,20000]])

    
a=main()

