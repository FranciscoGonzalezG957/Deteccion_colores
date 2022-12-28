from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import shutil
import numpy as np
from Tkinter import *
# inicializar la camara
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))
# precalentamiento de la camara
time.sleep(0.1)
# captura de video
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
#crear captura cruda
    image = frame.array
# imagen umbralizada
blue,g,r = cv2.split(image)
ret, im_floodfill=cv2.threshold(blue,80,255,cv2.THRESH_BINARY)
key = cv2.waitKey(1) & 0xFF
# mascara usada para el flood filling.
h, w = image.shape[:2]
mask = np.zeros((h+2, w+2), np.uint8)
# Floodfill
filling=cv2.floodFill(im_floodfill, mask, (0,0), 255);
#cv2.imshow("flood filling", im_floodfill)
#solo cate
maskinv=cv2.bitwise_not(im_floodfill)
maskinv2=maskinv/255
BinImage = cv2.merge((maskinv2,maskinv2,maskinv2))
solo=image*BinImage
#cv2.imshow("solo cate", solo)
#BGR promedio
b,g,r = cv2.split(solo)
num = np.sum(maskinv2)
b=np.sum(b)
g=np.sum(g)
r=np.sum(r)
b=b/num
g=g/num
r=r/num
#concatenar imagenes
flood = cv2.merge((maskinv,maskinv,maskinv))
contorno = cv2.merge((blue,blue,blue))
cate2=np.concatenate((image,contorno),axis=1)
cate3=np.concatenate((flood,solo),axis=1)
cate4=np.concatenate((cate2,cate3),axis=0)
cate5 = cv2.resize(cate4,(960,720))
cate6 = cv2.putText(cate5,"px="+str(num),(480,380),cv2.FONT_HERSHEY_SIMPLEX, 0.5
,(10,16,202), 2 , cv2.LINE_AA)
cate7 = cv2.putText(cate6,"b="+str(b),(480,400),cv2.FONT_HERSHEY_SIMPLEX, 0.5
,(10,16,202), 2 , cv2.LINE_AA)
cate8 = cv2.putText(cate7,"g="+str(g),(480,420),cv2.FONT_HERSHEY_SIMPLEX, 0.5
,(10,16,202), 2 , cv2.LINE_AA)
cate9 = cv2.putText(cate8,"r="+str(r),(480,440),cv2.FONT_HERSHEY_SIMPLEX, 0.5
,(10,16,202), 2 , cv2.LINE_AA)
cv2.imshow("Camara", cate9)
# limpiar la pantalla antes de mostrar una nueva imagen
rawCapture.truncate(0)
if key == ord("q"):
    camera.capture(rawCapture, format="bgr")
img = rawCapture.array
#leer registro
f = open ('registro.txt','r')
reg = f.read()
reg = int(reg)
reg=reg+1
f.close()
#escribir registro
f = open ('registro.txt','w')
f.write(str(reg))
f.close()
f = open('train.txt','a')
f.write('\n' + '[' + str(b) + ',' + str(g) + ',' + str(r) + ',' + str(num) + ']' )
f.close()
#guardar imagen y mostrar
cv2.destroyWindow("Frame")
cv2.imshow("Image", img)
cv2.waitKey(0)
cv2.destroyWindow("Image")
cv2.imwrite("foto-"+str(reg)+".png", img)
shutil.move("foto-"+str(reg)+".png", "/home/pi/Desktop/base/dia2")
time.sleep(0.1)
rawCapture.truncate(0)
if key == ord("x"):
    quit()
cv2.destroyAllWindow