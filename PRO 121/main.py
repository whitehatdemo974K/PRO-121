import cv2
import time
import numpy as np
fourcc = cv2.VideoWriter_fourcc(*'XVID')
output=cv2.VideoWriter('output.avi', fourcc, 20.0, (640,480))
cap= cv2.VideoCapture(0)
time.sleep(2)
bg=0
for i in range(60):
    ret, bg=cap.read()
bg=np.flip(bg, axis=1)
while (cap.isOpened()):
    ret, img=cap.read()
    if not ret:
        break
    img=np.flip(img, axis=1)
    hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    lower_red=np.array([0,120,50])
    upper_red=np.array([10,255,255])
    mask1=cv2.inRange(hsv,lower_red,upper_red)
    
    lower_red=np.array([170,120,70])
    upper_red=np.array([180,255,255])
    mask2=cv2.inRange(hsv,lower_red,upper_red)
    mask1 = mask1+mask2
    mask1 = cv2.morphologyEx(mask1, cv2.MORPH_OPEN,np.ones((3,3),np.uint8))
    mask1 = cv2.morphologyEx(mask1, cv2.MORPH_DILATE,np.ones((3,3),np.uint8))
    mask2 = cv2.bitwise_not(mask1)
    result1=cv2.bitwise_and(img, img,mask=mask2)
    result2=cv2.bitwise_and(bg, bg,mask=mask1)
    final_op=cv2.addWeighted(result1,1,result2,1,0)
    output.write(final_op)
    cv2.imshow("invisible",final_op)
    cv2.waitKey(1)
cap.release()
cv2.destroyAllWindows()