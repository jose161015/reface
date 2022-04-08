import cv2
#cap = cv2.VideoCapture(0)
#cap = cv2.VideoCapture('http://1jfiegbrfzrea:joselainez982000@192.168.1.20:80/tmpfs/auto.jpg')#camara kamtron


cap = cv2.VideoCapture('rtsp://1jfiegbrfzrea:joselainez982000@192.168.1.18:554/Streaming/Channels/1')

while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imshow('img.png', frame)
    k=cv2.waitKey(0) & 0xFF
    if k==27:
        
        break
cap.release()
cv2.destroyAllWindows()