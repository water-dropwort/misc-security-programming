# 顔検出の動作確認用スクリプト
import cv2
import sys

def face_detect(imfile_path):
    img     = cv2.imread(imfile_path)
    cascade = cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")
    rects   = cascade.detectMultiScale(img, 1.3, 4, cv2.CASCADE_SCALE_IMAGE, (20,20))

    if len(rects) == 0:
        return

    rects[:, 2:] += rects[:, :2]

    # 画像中のすべての顔をハイライト
    for x1,y1,x2,y2 in rects:
        cv2.rectangle(img, (x1,y1), (x2,y2), (127,255,0), 2)

    cv2.imshow("detected",img)
    cv2.waitKey(5000)
    
face_detect(sys.argv[1])
