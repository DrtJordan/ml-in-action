import numpy as np
import cv2

camera = cv2.VideoCapture(0)
# 第一帧用不了
_, frame = camera.read()

track_window = None

while True:
    ret, frame = camera.read()

    if track_window == None:
        r, h, c, w = 450, 250, 450, 250
        track_window = (c, r, w, h)

        roi = frame[r:r + h, c:c + w]
        cv2.imshow('roi', roi)
        cv2.waitKey(0)

        hsv_roi = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv_roi, np.array((100., 30., 32.)), np.array((180., 120., 255.)))

        roi_hist = cv2.calcHist([hsv_roi], [0], mask, [180], [0, 180])
        cv2.normalize(roi_hist, roi_hist, 0, 255, cv2.NORM_MINMAX)

        term_crit = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)

    if ret:
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        dst = cv2.calcBackProject([hsv], [0], roi_hist, [0, 180], 1)

        ret, track_window = cv2.CamShift(dst, track_window, term_crit)
        pts = cv2.boxPoints(ret)
        pts = np.int0(pts)

        img2 = cv2.polylines(frame, [pts], True, 255, 2)
        cv2.imshow('img2', frame)
        if cv2.waitKey(1) == ord("q"):
            break
    else:
        break
cv2.destroyAllWindows()
camera.release()
