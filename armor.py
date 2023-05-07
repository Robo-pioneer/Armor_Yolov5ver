# -*- coding: UTF-8 -*-
'''
@Gavin向
识别装甲板算法部分代码
Date:2022.9.17
'''

import cv2
import torch
import time,math,serial
import numpy as np
import traceback
import art 
from art import *
import torch.nn.functional as F
from utils.dataloaders import IMG_FORMATS, VID_FORMATS, LoadImages, LoadScreenshots, LoadStreams
#计算帧率的变量
fps_time_past = 0
fps_time_now = 0
input_pin = 15
armor_contours=[]#装甲板轮廓列表
armor_area_list = []#装甲板面积列表

k = np.ones((6,6),np.uint8)#创建6*6的数组作为核
erode = np.ones((1,1),np.uint8)#创建1*1的数组作为核

serial_port = 115200#设置串口波特率(9600或者115200)
com = serial.Serial("/dev/ttyUSB0",serial_port)#设置串口设备

device = torch.device("cuda")# [只有N卡才可以使用cuda加速]
#device = torch.device("cpu")#cpu推理模式

torch_model = torch.hub.load('./', 'custom',
                             './models/armor/weights/best.pt',source='local', force_reload=True)  #加载本地yolov5模型(需要修改路径和文件)
def send_message(bool,x_position,y_position):
    if bool == True:#如果bool为真才会发送信息
        print("send",x_position,y_position)
        send_string = "x "+str(x_position - 400)+' y '+str(y_position - 300)+"\n"#将坐标信息整合到send_string中
        com.write(send_string.encode('utf-8'))#将send_string发送给EP(EP和开发板的串口波特率需要保持一致)
    else:
        pass


def check_armor(roi_frame):
    armor_contours = []  # 清空列表

    fontStyle = cv2.FONT_HERSHEY_TRIPLEX  # 设置字体样式

    hsv = cv2.cvtColor(roi_frame, cv2.COLOR_BGR2HSV)  # HSV颜色设置
    mask = cv2.inRange(hsv, Color_lower, Color_upper)  # 提取在HSV范围内的图像
    res = cv2.morphologyEx(mask,cv2.MORPH_GRADIENT,np.ones((6,6),np.uint8))
    res = cv2.Canny(res, 100, 1050)  # Canny边缘检测

    contours, hierarchy = cv2.findContours(res, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)  # 寻找轮廓(只识别外围轮廓)
    contours_amount = len(contours)#统计轮廓的数量
    print("未筛选前的轮廓数量：",contours_amount)
    armor_contours_amount = 0#计算轮廓数量
    for count in range(contours_amount):#遍历所有的轮廓(用于筛选出装甲板)
        x, y, w, h = cv2.boundingRect(contours[count])#获取坐标，宽高
        if w>=1 and h>=1:#增加判断装甲板条件
            armor_contours.append(contours[count])
            armor_contours_amount = armor_contours_amount + 1
        else:
            pass#如果不符合判断条件，就跳过该轮廓
    print("经过筛选后的轮廓数量：",armor_contours_amount)

    try:
        armor_area_list = []#重置列表，用于筛选出最大面积装甲板
        for i in range(armor_contours_amount):
            x, y, w, h = cv2.boundingRect(armor_contours[i])
            armor_area = w*h
            armor_area_list.append(armor_area)
        max_area = armor_area_list[0]
        for k in range(1,len(armor_area_list)):
            if max_area <= armor_area_list[k]:
                max_area = armor_area_list[k]

        max_area_index = armor_area_list.index(max_area)
        finally_armor_information = armor_contours[max_area_index]
        x, y, w, h = cv2.boundingRect(finally_armor_information);position_string = "X:"+str(x)+"  Y:"+str(y)
        #roi_frame = cv2.rectangle(roi_frame, (x, y), (x + w, y + h), (0, 255, 255), 5)  # 在原画面上绘制出方框
        #roi_frame = cv2.putText(roi_frame, position_string, (x, y - 25), fontStyle, 1, (0, 255, 255))  # 在识别的装甲板上显示装甲板坐标
        print("成功匹配图像","x:",x,"y：",y, "\n图像宽度:", w, "图像高度:", h)  # 打印测试（可注释该行代码）

        return (True,roi_frame)#验证成功
    except:
        return (False,roi_frame)#验证失败


def recognize_armor(frame,color):
    global torch_model
    global device
    armor_bool = [0, 0]
    armor_list = []
    fontStyle = cv2.FONT_HERSHEY_TRIPLEX  # 设置显示字体样式
    if armor_color == "red":
        detect_armor_class = 16
    elif armor_color == "blue":
        detect_armor_class = 15
    torch_model = torch_model.to(device)
    results = torch_model(frame)
    #print("Pytorch_result:")
    #results.print()
    print("modle complete:" + str((time.time() - fps_time_past)))
    try:
        xyxy = results.pandas().xyxy[0].values
        xmins, ymins, xmaxs, ymaxs, class_list, confidences = xyxy[:, 0], xyxy[:, 1], xyxy[:, 2], xyxy[:, 3], xyxy[:, 5], xyxy[:, 4]
       
        print("result decode complete:" + str((time.time() - fps_time_past)))
        count = 0#记数
        for xmin, ymin, xmax, ymax,class_l,conf in zip(xmins, ymins, xmaxs, ymaxs,class_list,confidences):#for循环遍历
            print("detect_armor_class:", detect_armor_class)
            if class_l == detect_armor_class and conf>=0.25:#如果置信度大于0.25且
                count = count + 1
                armor_list.append([int(xmin), int(ymin), int(xmax), int(ymax),conf,count])#将识别物体信息加入armor_list列表

                print("torch_position:", int(xmin), int(ymin), int(xmax), int(ymax))
                
            print("count",count)#装甲板数量
            if len(armor_list) > 0:
                print("ARMOR:",armor_list)#[xmin,ymin,xmax,ymax,conf,index]
                armor_position_list = []#清空列表
                armor_distance_list = []
                k = 0
                for i in armor_list:
                    k = k + 1
                    if detect_armor_class == 1:
                        confidence_string = "RED " + str(round(i[4] , 2)) + "%"#设置显示置信度的字符串
                    else:
                        confidence_string = "BLUE " + str(round(i[4], 2)) + "%"  # 设置显示置信度的字符串

                    frame = cv2.rectangle(frame, (int(i[0]), int(i[1])), (int(i[2]), int(i[3])), (0, 255, 0), 2) # 在原图像中画出方框框记识别目标
                    frame = cv2.putText(frame, confidence_string, (int(i[0]), int(i[1]) - 20), fontStyle, 1, (0, 255, 0))  # 在识别的装甲板上标注识别置信度

                    #print(i[2],i[0])
                    armor_x_position = int(i[2] - (i[2]-i[0]) / 2)#计算识别目标的X坐标
                    #print(i[3],i[1])
                    armor_y_position = int(i[3] - (i[3]-i[1]) / 2)#计算识别目标的Y坐标
                    
                    #print("armor_x_position",armor_x_position)
                    #print("armor_y_position", armor_y_position)

                    distance = math.sqrt(armor_x_position*armor_x_position + armor_y_position*armor_y_position)#运用勾股定理计算出每个目标坐标到中心点的距离
                    armor_distance_list.append(distance)#把距离distance加入列表armor_distance_list
                    armor_position_list.append([armor_x_position,armor_y_position])#将装甲板坐标加入armor_position_list
                print("detect complete:" + str((time.time() - fps_time_past)))
                print(armor_distance_list)
                min_armor_distance = min(armor_distance_list)
                finally_armor_information = armor_list[armor_distance_list.index(min_armor_distance)]
                x_position = finally_armor_information[2] - (
                        finally_armor_information[2] - finally_armor_information[0]) / 2
                y_position = finally_armor_information[3] - (
                        finally_armor_information[3] - finally_armor_information[1]) / 2
                send_message(True,x_position,y_position)#将坐标通过Uart通信发送给EP机器人
        
        #if armor_bool[0] == True:#二次验证成功
        #    #计算装甲板中心点坐标
        #    
        #    print("good")
        #elif armor_bool[0] == False:#二次验证失败
        #    print("error")
        #    send_message(False,0,0)#不发送

    except:#若出现错误：
        armor_bool[1] = 0
        traceback.print_exc()#打印报错信息
    else:
        print("Loop complete in :" + str((time.time() - fps_time_past)))
        print("FPS:" + str( 1 / (time.time() - fps_time_past)))
        print("--------------程序进程正常--------------")#方便Debug
    return (frame,armor_bool[1])#frame---第一次识别结果  armor_bool[1]---第二次识别结果


def camera_set(bool):#摄像头基础参数设置函数
    if bool == True:
        cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)
        cap.set(cv2.CAP_PROP_BRIGHTNESS, 100)
        cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)
        cap.set(cv2.CAP_PROP_EXPOSURE, 20)#设置曝光
        #cap.set(CV_CAP_PROP_FPS, 30)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)
        cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
    elif bool == False:
        print("Video test-----")
    else:
        print("bool error-----")

if __name__ == "__main__":#main
    cap = 0
    cap = cv2.VideoCapture(cap)
    camera_set(True)#摄像头设置
    armor_color = "blue"#设置识别装甲板的颜色
    
    print(text2art("Detect: "+armor_color))
    if armor_color == "blue":
        # 蓝色armor
        Color_lower = np.array([100, 123, 120])
        Color_upper = np.array([160, 255, 230])
    elif armor_color == "red":
        # 蓝色armor
        Color_lower = np.array([160, 255, 230])
        Color_upper = np.array([180, 255, 250])

    while True:#循环
        fps_time_past = time.time()#记录开始时间
        ret, frame = cap.read()
        print("Get img from cam in :" + str((time.time() - fps_time_past)))
        frame = recognize_armor(frame,armor_color)
        cv2.imshow("frame",frame[0])
        if cv2.waitKey(1) & 0xFF == 27:# 按ESC退出
            print("程序结束")
            break # 退出

