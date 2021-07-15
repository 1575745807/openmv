# 2021.06.15 智能分拣系统 天眼计划
#  x=320 y=240
import sensor, image, time, math, json, pyb,lcd
from pyb import LED
from pyb import UART
from pyb import Pin
from pyb import Timer
#LED(1).on()
#LED(2).on()
#LED(3).on()
pin0 = Pin('P1', Pin.IN, Pin.PULL_UP)
#pin1 = Pin('P1', Pin.OUT_PP, Pin.PULL_NONE)

blue_L_min=1
blue_L_max=1
blue_A_min=1
blue_A_max=1
blue_B_min=1
blue_B_max=1

# 颜色跟踪阈值(L Min, L Max, A Min, A Max, B Min, B Max)
thresholds1 =[
#(0, 26, -128, 126, -128, -18),#13；40
#(0, 100, -128, 127, -128, -26),  #17:17
#(0, 27, -128, 125, -128, -13)
(blue_L_min,blue_L_max,blue_A_min,blue_A_max,blue_B_min,blue_B_max)
] #16:30  #蓝色车尾
              # generic_blue_thresholds
thresholds2 =[(0, 58, -128, -20, -128, 127),#19;22反光
(0, 26, -128, -13, -128, 127),#12:43
(20, 43, -128, -16, -128, 127) #16:30  #绿色车头
]
#thresholds3 =[
#(0, 18, -128, 10, -128, 6),#18;15
#(0, 14, -128, 6, -128, 127)  #14:10  #测试黑色
#]
#thresholds4 =[(0, 100, 26, 127, -128, 127),#16：10 #修正
#(33, 100, 26, 127, 25, 127),  #15:15 #修正
#(57, 100, 8, 127, 19, 127),#21：00半黄
#(0, 99, 26, 124, -128, 127)]  #16:30  #测试橘黄

sensor.reset()
#初始化摄像头，reset()是sensor模块里面的函数
sensor.set_pixformat(sensor.RGB565)
#设置图像色彩格式，有RGB565色彩图和GRAYSCALE灰度图两种
sensor.set_framesize(sensor.QVGA)
lcd.init() # 初始化lcd屏幕。
#设置图像像素大小
sensor.skip_frames(time = 2000)
#sensor.set_vflip(True)
#sensor.set_hmirror(True)
sensor.set_contrast(0)
sensor.set_auto_gain(False) # 颜色跟踪必须关闭自动增益
sensor.set_auto_whitebal(False) # 颜色跟踪必须关闭白平衡
clock = time.clock()
uart = UART(3, 115200)
left_roi = [22,20,284,186]  ##感性区域，设计颜色识别的有效区域
left_roi1 = [0,120,160,120]

ROI=(140,100,20,20)
# 只有比“pixel_threshold”多的像素和多于“area_threshold”的区域才被
# 下面的“find_blobs”返回。 如果更改相机分辨率，
# 请更改“pixels_threshold”和“area_threshold”。 “merge = True”合并图像中所有重叠的色块。
def find_max(blobs):
    max_size=0
    for blob in blobs:
        if blob.pixels() > max_size:
            max_blob = blob
            max_size = blob.pixels()
    return max_blob

def tick(timer):      #这里开启了一个定时器
    log3y=1

tim = Timer(2, freq=1)      # create a timer object using timer 2 - trigger at 1Hz
tim.callback(tick)          # set the callback to our tick function

temp =20
xiu =0
log1x=0
log1y=0
log2x=0
log2y=0
log3x=0
log3y=0
a1=0
a2=0
a3=0
a4=0
a5=0
a6=0
a7=0
a8=0
a9=0
a10=0
string=''
string3=''
string6=''
string9=''
string12=''
key0 = 2
key1 = 2

Lmin = 1
Lmax = 1
Amin = 1
Amax = 1
Bmin = 1
Bmax = 1

#pin0.value([0])
while(True):
    clock.tick()
    img = sensor.snapshot()

    statistics=img.get_statistics(roi=ROI)
    color_l=statistics.l_mode()
    color_a=statistics.a_mode()
    color_b=statistics.b_mode()
    print(color_l,color_a,color_b)
    img.draw_rectangle(ROI)
    Lmin = color_l - 10
    Lmax = color_l + 10
    Amin = color_a - 10
    Amax = color_a + 10
    Bmin = color_b - 10
    Bmax = color_b + 10

    key0 = pin0.value()
    print(key0,key0)
    if key0 == 0:
        LED(3).on()
        LED(1).off()
        blue_L_min = Lmin
        blue_L_max = Lmax
        blue_A_min = Amin
        blue_A_max = Amax
        blue_B_min = Bmin
        blue_B_max = Bmax
        print(blue_L_min,blue_L_max,blue_A_min,blue_A_max,blue_B_min,blue_B_max)
        thresholds1 =  [(blue_L_min,blue_L_max,blue_A_min,blue_A_max,blue_B_min,blue_B_max)]
    if key0 == 1:
        LED(1).on()
        LED(3).on()
        print(blue_L_min,blue_L_max,blue_A_min,blue_A_max,blue_B_min,blue_B_max)

###蓝色最大目标作为车尾
    blobs = img.find_blobs(thresholds1,roi=left_roi,pixels_threshold=50, area_threshold=50,merge = True)
    if blobs:  #a5,a6,string6,string7,string8
        a5=1
        max_blob1 = find_max(blobs)
        img.draw_edges(max_blob1.min_corners(), color=(0,0,255))
        img.draw_cross(max_blob1[5], max_blob1[6],color=(0,0,255))
        output_str="(%3d%3d)" % (max_blob1[5],max_blob1[6]) #方式1
        print(max_blob1[9])
        string6 =str(max_blob1[5])+','+str(max_blob1[6])+','
        log1x = max_blob1[5]
        log1y = max_blob1[6]
        #print(max_blob[2],max_blob[3])
##禄色最大目标作为车头
    blobs1 = img.find_blobs(thresholds2,roi=left_roi,pixels_threshold=50, area_threshold=50,merge = True)
    if blobs1:   #a7,a8,string9,string10,string11
        a7=1
        max_blob = find_max(blobs1)
        img.draw_edges(max_blob.min_corners() ,color=(0,255,0))
        img.draw_cross(max_blob[5], max_blob[6], color=(0,255,0))
        output_str="(%3d%3d)" % (max_blob[5],max_blob[6]) #方式1
      #  a8 = string9
        string9 =str(max_blob[5])+','+str(max_blob[6])+','
        log2x = max_blob[5]
        log2y = max_blob[6]
    if a7 != 0:
        if a5 != 0:
            string9 = str(string9)+str(string6)
            string10 = list(string9) #先转换成列表
            string10.pop()   #删除列表的最后一位
            string11 =''.join(string10)  #再重新转换成字符串
            string9 ='>'+str(string11)+'<'
            print(string9)
            uart.write(string9)
            a7=0
            string9=''
            a5=0
            string6=''
    lcd.display(img) # 拍照并显示图像。


