import numpy as np
import imutils
import cv2
import sys
from sys import platform
import copy

def draw_flow(img, flow, step=10, thickness=1, line_color=(255, 100, 0)):
    h, w = img.shape[:2]
    y, x = np.mgrid[step/2:h:step, step/2:w:step].reshape(2, -1).astype(int)
    fx, fy = flow[y, x].T
    lines = np.vstack([x, y, x + fx, y + fy]).T.reshape(-1, 2, 2)
    lines = np.int32(lines + 0.5)
    vis = copy.copy(img)
    cv2.polylines(vis, lines, 0, line_color, thickness)
    return vis

def main(fn, WIDTH=700, step=5, thickness=1, scale=1, line_color=(255, 100, 0)):
    if fn == 0:
        filename = 'cam'
    elif platform == "win32":
        nlst = fn.split('.')
        filename = nlst[0].split('\\')[-1] if len(nlst) == 2 else nlst[1].split('\\')[-1]
    else:
        print(f"{fn} on {platform}")
        nlst = fn.split('.')
        filename = nlst[0].split('/')[-1] if len(nlst) == 2 else nlst[1].split('/')[-1]
    
    cap = cv2.VideoCapture(fn)
    ret, prev = cap.read()
    prev = imutils.resize(prev, width=WIDTH)
    frame1 = cv2.cvtColor(prev, cv2.COLOR_BGR2GRAY)

    (major_ver, _, _) = (cv2.__version__).split('.')
    if int(major_ver)  < 3 :
        fps = cap.get(cv2.cv.CV_CAP_PROP_FPS)
    else :
        fps = cap.get(cv2.CAP_PROP_FPS)

    fname = f"{filename}_processed_grid_{step}.avi"
    height, width = frame1.shape
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(fname, fourcc, fps, (width, height))

    try:
        nvof = cv2.cuda_NvidiaOpticalFlow_1_0.create(frame1.shape[1], frame1.shape[0], 5, False, False, False, 0)
        has_cuda_nvof = False
    except AttributeError:
        has_cuda_nvof = False

    while cap.isOpened():
        print('.', end='')
        ret, img = cap.read()
        if not ret:
            break
        img = imutils.resize(img, width=WIDTH)
        frame2 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        if has_cuda_nvof:
            nvof = cv2.cuda_NvidiaOpticalFlow_1_0.create(frame1.shape[1], frame1.shape[0], 5, False, False, False, 0)
            flow = nvof.calc(frame1, frame2, None)
            flow = nvof.upSampler(flow[0], frame1.shape[1], frame1.shape[0], nvof.getGridSize(), None)
            nvof.collectGarbage()
        else:
            flow = cv2.calcOpticalFlowFarneback(frame1, frame2, None, 0.5, 3, 15, 3, 5, 1.2, 0)
            flow = draw_flow(prev, flow*scale, step=step, thickness=thickness, line_color=line_color)
        
        frame1 = frame2
        prev = img
        out.write(flow)

    cap.release()
    out.release()
    cv2.destroyAllWindows()
    return None

if __name__ == '__main__':
    try:
        fn = sys.argv[1]
        step = int(sys.argv[2]) if sys.argv[2] else 5
        thickness = int(sys.argv[3]) if sys.argv[3] else 1
        scale = int(sys.argv[4]) if sys.argv[4] else 1
        print("Processing...")
        main(fn, step=step, thickness=thickness, scale=scale)
        print("Done!")
    except IndexError:
        print('No video file provided! Video file required!')
