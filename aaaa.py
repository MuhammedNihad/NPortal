import cv2

cap=cv2.VedioCapture(0)
while(True)

    ret,frame=cap.read()
    print("hiiii")
cap.release()
cv2.destroyAllWindows()