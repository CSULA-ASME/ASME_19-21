import cv2
import numpy as np 
import laneFunctions as lf

curveList = []
avgVal = 10

def getLaneCurve(img, display=2):
    imgCopy = np.copy(img)
    imgRes = np.copy(img)
    # STEP 1
    imgThres = lf.thresholding(img)
    # STEP 2
    hT, wT, c = img.shape
    points = lf.valTrackbars()
    imgWarp = lf.warpImg(imgThres, points, wT, hT)
    imgWarpPoints = lf.drawPoints(imgCopy, points)
    # STEP 3
    midPoint,imgHist = lf.getHistogram(imgWarp,display=True,minPer=0.5, region=4)
    curveAvgPoint,imgHist = lf.getHistogram(imgWarp,display=True,minPer=0.9)
    curveRaw = curveAvgPoint-midPoint

    # STEP 4
    curveList.append(curveRaw)
    if len(curveList)> avgVal:
        curveList.pop(0)

    curve = int(sum(curveList) / len(curveList))

    # STEP 5 
    if display != 0:
        imgInvWarp = lf.warpImg(imgWarp, points, wT, hT, inv=True)
        imgInvWarp = cv2.cvtColor(imgInvWarp, cv2.COLOR_GRAY2BGR)
        imgInvWarp[0:hT // 3, 0:wT] = 0,0,0
        imgLaneColor = np.zeros_like(img)
        imgLaneColor[:] = 0,255,0
        imgLaneColor = cv2.bitwise_and(imgInvWarp, imgLaneColor)
        imgRes = cv2.addWeighted(imgRes, 1 , imgLaneColor, 1, 0)
        midY = 450
        cv2.putText(imgRes, str(curve), (wT // 2 - 80, 85), cv2.FONT_HERSHEY_COMPLEX, 2, (255,0,0), 3)
        cv2.line(imgRes, (wT // 2, midY), (wT // 2 + (curve * 3), midY), (255,0,255), 5)
        cv2.line(imgRes, ((wT // 2 + (curve * 3)), midY-25), (wT // 2 + (curve * 3), midY), (255,0,255), 5)

        for x in range(-30, 30):
            w = wT // 20
            cv2.line(imgRes, (w * x + int(curve // 50), midY - 10), (w * x + int(curve // 50), midY + 10), (0,0,255), 2)

    if display == 2:
        imgStacked = lf.stackImages(0.7, ([img, imgWarpPoints, imgWarp],[imgHist, imgLaneColor, imgRes]))
        cv2.imshow('IMAGESTACK', imgStacked)

    elif display == 1:
        cv2.imshow('RESULT', imgRes)

    curve = curve / 100
    if curve>1: curve == 1
    if curve<-1: curve == -1

    return curve

if __name__ == '__main__':
    cap = cv2.VideoCapture('vid1.mp4')
    intialTrackBarVals = [102, 80, 20, 214 ]
    lf.initTrackbars(intialTrackBarVals)
    frameCounter = 0
    while True:
        frameCounter += 1
        if cap.get(cv2.CAP_PROP_FRAME_COUNT) == frameCounter:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            frameCounter = 0
 
        success, img = cap.read()
        img = cv2.resize(img,(480,240))
        curve = getLaneCurve(img,display=2)
        print('Curve Value:' + str(curve))
        #cv2.imshow('Vid',img)
        cv2.waitKey(1)