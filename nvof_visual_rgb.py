import sys
import numpy as np 
import cv2 as cv
from sys import platform

def main(vid_path, grid_size=5):
    cap = cv.VideoCapture(vid_path)
    i = 0
    frames = []
    flow = []
    size = None
    while(cap.isOpened()):
        success, frame = cap.read()
        height, width, layers = frame.shape
        size = (width,height)
        if success:
            frames.append(frame)
            if i == 0:
                i += 1
                continue
            else:
                print(frames[i-1].shape, frames[i].shape)
                nvof = cv.cuda_NvidiaOpticalFlow_1_0.create(frame.shape[1], frame.shape[0], grid_size, False, False, False, 0)
                flow = nvof.calc(frames[i-1], frames[i], None)
                flowUpSampled = nvof.upSampler(flow[0], frame.shape[1], frame.shape[0], nvof.getGridSize(), None)
                flow.append(flowUpSampled)
                i += 1
                nvof.collectGarbage()
    cap.release()
    if platform == "win32":
        nlst = fn.split('.')
        filename = nlst[0].split('\\')[-1] if len(nlst) == 2 else nlst[1].split('\\')[-1]
    else:
        nlst = fn.split('.')
        filename = nlst[0].split('/')[-1] if len(nlst) == 2 else nlst[1].split('/')[-1]
    fname = f"output/{filename}.avi"
    out = cv.VideoWriter(fname,cv.VideoWriter_fourcc(*'DIVX'), i, size)
    for i in range(len(flow)):
        out.write(flow[i])
    out.release()
    print(f"Video output: {fname}")

if __name__=='__main__':
    try:
        fn = sys.argv[1]
    except:
        print('No video input!')
    if len(sys.argv) >= 3:
        gs = sys.argv[2]
        main(fn, grid_size=gs)
    else:
        main(fn)