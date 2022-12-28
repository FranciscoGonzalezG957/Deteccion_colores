import numpy as np
import cv2

def nada(x):
    pass

cv2.namedWindow('Parametros')
cv2.createTrackbar('Tonalidad Minima','Parametros',0,179,nada)
cv2.createTrackbar('Tonalidad Maxima','Parametros',0,179,nada)  #Parametro H - Color
cv2.createTrackbar('Pureza Minima','Parametros',0,255,nada)
cv2.createTrackbar('Pureza Maxima','Parametros',0,255,nada) #Parametro S - Saturacion
cv2.createTrackbar('Luminosidad Minima','Parametros',0,255,nada)
cv2.createTrackbar('Luminosidad Maxima','Parametros',0,255,nada)    #Parametro V - Luminosidad
cv2.createTrackbar('Kernel X','Parametros',1,30,nada)
cv2.createTrackbar('Kernel Y','Parametros',1,30,nada)   #Filtro Kernel: Suaviza los pixeles

#Iniciamos la captura de video
cap = cv2.VideoCapture(0)

while(1):
    ret, frame = cap.read()
    if ret:
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        Tmin = cv2.getTrackbarPos('Tonalidad Minima','Parametros')
        Tmax = cv2.getTrackbarPos('Tonalidad Maxima','Parametros')
        Pmin = cv2.getTrackbarPos('Pureza Minima','Parametros')
        Pmax = cv2.getTrackbarPos('Pureza Maxima','Parametros')
        Lmin = cv2.getTrackbarPos('Luminosidad Minima','Parametros')
        Lmax = cv2.getTrackbarPos('Luminosidad Maxima','Parametros')

        color_oscuro = np.array([Tmin,Pmin,Lmin])
        color_brillante = np.array([Tmax,Pmax,Lmax])

        mascara = cv2.inRange(hsv, color_oscuro, color_brillante)

        kernelx = cv2.getTrackbarPos('Kernel X','Parametros')
        kernely = cv2.getTrackbarPos('Kernel Y','Parametros')

        kernel = np.ones((kernelx,kernely),np.uint8)

        mascara = cv2.morphologyEx(mascara,cv2.MORPH_CLOSE,kernel)
        mascara = cv2.morphologyEx(mascara,cv2.MORPH_OPEN,kernel)

        contornos, _ = cv2.findContours(mascara, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(frame,contornos, -1, (0,0,0),2)

        cv2.imshow("Camara",frame)
        cv2.imshow("Mascara",mascara)

        k = cv2.waitKey(5)
        if k == 27:
            cv2.destroyAllWindows()
    
cap.release()

