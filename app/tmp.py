"""
Helper Functions for Result generator
"""
import cv2 as cv

video = cv.VideoCapture('../data/in/videos/tracking1.mp4')
fps = video.get(cv.CAP_PROP_FPS)
ok, img = video.read()

frame_size = img.shape[:2]
size = (frame_size[1], frame_size[0])
fourcc = cv.VideoWriter_fourcc(*'XVID')
out = cv.VideoWriter('../data/out/test1.avi',fourcc, fps, size)

while ok:
    ok, img = video.read()
    out.write(img)

video.release()
out.release()

