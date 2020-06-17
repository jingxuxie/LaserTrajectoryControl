# -*- coding: utf-8 -*-
"""
Created on Fri Sep 20 16:09:05 2019

@author: Jingxu Xie

v1.0 跟随鼠标路径画直线，0关闭激光，显示绿色，安全，1打开激光，红色危险，按q退出，按x清除并重新画线
v1.1 输出结果为始末点坐标，而非线上每个点的坐标，且加入可以实时输出线段长度
v1.2 更改了消除之前画线的方式，记录画过的线，直接用原图覆盖，再重新画，取消算法
v1.3 加入按指定长度画线，由方向键控制，上下加减1，左右加减0.1，按5恢复自由画线，优化了部分语法和结构
    增加了键盘输入的实时响应，以及长度控制锁
"""

import numpy as np
import cv2

def find_position_given_distance(x1,y1,x2,y2,length):
    if x1 == x2 and y1 == y2:
        return x2,y2
    if x1 == x2:
        return x2,int(y1+length*abs(y2-y1)/(y2-y1))
    if y1 == y2:
        return int(x1+length*abs(x2-x1)/(x2-x1)),y2
    dx=x2-x1
    dy=y2-y1
    cos_angle=dx/(np.sqrt(dx**2+dy**2))
    sin_angle=dy/(np.sqrt(dx**2+dy**2))
    x=int(x1+round(length*cos_angle))
    y=int(y1+round(length*sin_angle))
    return x,y


def text_position(x1,y1,x2,y2):#计算文本坐标
    d=np.sqrt((x2-x1)**2+(y2-y1)**2)+0.0001
    x=int(round((x1+x2)/2-60*(y2-y1)/d))
    if x > (x1+x2)/2:
        x=int(round((x1+x2)/2-15*(y2-y1)/d))
    y=int(round((y1+y2)/2+30*(x2-x1)/d))
    if y < (y1+y2)/2:
        y=int(round((y1+y2)/2+20*(x2-x1)/d))
    return x,y


def draw_grid():
    for i in range(8):
        cv2.line(img_copy,(i*100,0),(i*100,700),[255,255,255])
        cv2.line(img_copy,(0,i*100),(700,i*100),[255,255,255])
    cv2.line(img_copy,(100,100),(100,600),[0,255,255],3)
    cv2.line(img_copy,(100,100),(600,100),[0,255,255],3)
    cv2.line(img_copy,(600,100),(600,599),[0,255,255],3)
    cv2.line(img_copy,(600,599),(100,600),[0,255,255],3)

def redraw():#清除并重画
    global posx,posy,poswitch,textposx,textposy,d,img_copy
    img_copy=img0.copy()
    draw_grid()
    for i in range(len(posx)-1):#绘制之前的线
        cv2.line(img_copy,(posx[i],posy[i]),(posx[i+1],posy[i+1]),color[poswitch[i+1]],3)
        text=str(round(d[i+1]/50,1))
        cv2.putText(img_copy,text,(textposx[i+1],textposy[i+1]),cv2.FONT_HERSHEY_PLAIN,1.2,color[poswitch[i+1]],1)
        
        
def update_drawing():#根据键盘输入更新情况
    global x_old,y_old,x_new,y_new,LengthD,LengthLock
    redraw()
    if LengthLock==0:
        cv2.line(img_copy,(x_old,y_old),(x_new,y_new),color[switch],3)
        d_temp=np.sqrt((x_new-x_old)**2+(y_new-y_old)**2)+0.0001
        LengthD=d_temp
        textposx_temp,textposy_temp=text_position(x_old,y_old,x_new,y_new)
        text=str(round(d_temp/50,1))
        cv2.putText(img_copy,text,(textposx_temp,textposy_temp),cv2.FONT_HERSHEY_PLAIN,1.2,color[switch],1)
    if LengthLock==1:
        x_new,y_new=find_position_given_distance(x_old,y_old,x_new,y_new,LengthD)
        cv2.line(img_copy,(x_old,y_old),(x_new,y_new),color[switch],3)
        d_temp=np.sqrt((x_new-x_old)**2+(y_new-y_old)**2)+0.0001
        textposx_temp,textposy_temp=text_position(x_old,y_old,x_new,y_new)
        text=str(round(d_temp/50,1))
        cv2.putText(img_copy,text,(textposx_temp,textposy_temp),cv2.FONT_HERSHEY_PLAIN,1.2,color[switch],1)

    

def draw_line(event,x,y,flags,param):
    global drawing,x_old,y_old,x_new,y_new,switch,poswitch,count,LengthD,color,textposx,textposy,d,LengthLock
    global img_copy
    
    if event == cv2.EVENT_LBUTTONDOWN: 
        LengthLock=0#关闭长度锁
        drawing = True
        textposx.append(text_position(x_old,y_old,x_new,y_new)[0])#更新文本和其坐标
        textposy.append(text_position(x_old,y_old,x_new,y_new)[1])
        d.append(np.sqrt((x_new-x_old)**2+(y_new-y_old)**2))
        if x_new==0 and y_new==0:#这个if用来判断是否为起始点
            x_old,y_old = x,y
        else:
            x_old,y_old = x_new,y_new             
        posx.append(x_old)#更新点坐标和开关
        posy.append(y_old)
        poswitch.append(switch)
        switch=0#恢复关闭状态，保证安全
        count+=1

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing == True and LengthLock==0:
            redraw()
            x_new,y_new=x,y
            update_drawing()
        if drawing == True and LengthLock!=0:
            redraw()
            x_new,y_new=find_position_given_distance(x_old,y_old,x,y,LengthD)
            update_drawing()

    elif event == cv2.EVENT_RBUTTONDOWN:
        redraw()
        drawing = False



def main():
    global drawing,x_old,y_old,x_new,y_new,switch,poswitch,count,img0,img_copy,posx,posy,LengthD,color,textposx,textposy,d,LengthLock
    LengthD=0 #增加线的长度
    LengthLock=0 #长度控制锁，0为关，1为开
    drawing = False # true if mouse is pressed
    color=[[0,255,0],[0,0,255]]
    x_old,y_old,x_new,y_new=0,0,0,0
    switch=0#开关
    count=0#计数
    posx = []#记录位置
    posy = []
    poswitch = []
    textposx=[]
    textposy=[]
    d=[]

        
    img0 = np.zeros((700,700,3), np.uint8)#+255
    #img0=cv2.imread('test.png')
    img_copy=img0.copy()
    cv2.namedWindow('Laser trajectory')
    cv2.moveWindow('Laser trajectory',300,100)
    cv2.setMouseCallback('Laser trajectory',draw_line)
    draw_grid()


    while(1):    
        cv2.imshow('Laser trajectory',img_copy)  
        k = cv2.waitKeyEx(20)
        '''
        if k!=-1:
            ans=k
            print(ans)
            '''
        if k==ord('z') and len(posx)>0:#撤销
            
            posx.pop()
            posy.pop()
            poswitch.pop()
            textposx.pop()
            textposy.pop()
            d.pop()
            redraw()
            if len(posx)>0:
                x_old,y_old=posx[-1],posy[-1]
            else:
                x_old,y_old=0,0#全部归零
                drawing = False # true if mouse is pressed
                x_old,y_old,x_new,y_new=0,0,0,0
                switch=0#开关
                count=0#计数
                posx = []#记录位置
                posy = []
                poswitch = []
                textposx=[]
                textposy=[]
                d=[]
                redraw()

        if k == 2490368:#上
            LengthD+=50
            LengthLock=1
            redraw()
            update_drawing()
        if k == 2621440:#下
            LengthD-=50
            LengthLock=1
            redraw()
            update_drawing()
        if k == 2424832:#左
            LengthD-=5
            LengthLock=1
            redraw()
            update_drawing()
        if k == 2555904:#右
            LengthD+=5
            LengthLock=1
            redraw()
            update_drawing()
        if k == ord('5'):#恢复自由
            LengthLock=0
            
        if k == ord('0'):#设置关
            switch=0
            redraw()#实时更新
            update_drawing()
        if k == ord ('1'):#开
            switch=1
            redraw()
            update_drawing()
        if k == ord ('x'):#清除重画
            drawing=False
            x_old,y_old,x_new,y_new=0,0,0,0#初始位置置零
            switch=0#开关置零
            count=0#计数清零
            posx = []#记录位置
            posy = []
            poswitch = []
            textposx=[]
            textposy=[]
            d=[]
            img_copy=img0.copy()
            draw_grid()
        if k == ord('q'):#退出
            break

    poswitch[:len(poswitch)-1]=poswitch[1:len(poswitch)]
    if len(poswitch)>0:
        poswitch[-1]=0

    
    outposx=np.array(posx)
    outposy=np.array(posy)
    outposwitch=np.array(poswitch)

    OutPut=np.vstack((outposx,outposy))
    OutPut=np.vstack((OutPut,outposwitch))
    OutPut=np.transpose(OutPut)
    #print(OutPut)
    cv2.destroyAllWindows()
    out=OutPut.copy()#通过copy来消除strided arrays
    out=out.astype(np.double)
    out[:,0:2]=(out[:,0:2]-100)/50
    out=np.vstack((np.array([[0,0,0]]),out))
    out=np.vstack((out,np.array([[0,0,0]])))
    return out
#np.array([[1000,1000,1000],[1000,10000,10000],[20000,2000,20000]])

    
a=main()
np.savetxt('laser_trajectory.txt',a,delimiter=' ')
    
#x,y=find_position_given_distance(100,200,98,200,5)