import cv2
from PIL import Image

pts = []
imgs = []

def click(event, x, y, flags, param):
    global firstFrame
    if event == 1:
        pts.append([x, y])
        cv2.circle(firstFrame, (x, y), 5, (0, 0, 255), -1)

video = cv2.VideoCapture(r"C:\Users\v\Documents\Rick Astley - Never Gonna Give You Up (Official Video) (4K Remaster).mp4")
_, firstFrame = video.read()

cv2.imshow("", firstFrame)
cv2.setMouseCallback("", click)

while len(pts) < 4:
    cv2.imshow("", firstFrame)
    cv2.waitKey(1)

x1 = min(p[0] for p in pts)
y1 = min(p[1] for p in pts)
x2 = max(p[0] for p in pts)
y2 = max(p[1] for p in pts)

while True:
    _, frame = video.read()
    if frame is None:
        break

    slide = frame[y1:y2, x1:x2]
    cv2.imshow("", slide)
    k = cv2.waitKey(30)

    if k == ord("s"):
        imgs.append(Image.fromarray(cv2.cvtColor(slide, cv2.COLOR_BGR2RGB)))
    if k == ord("q"):
        break

cv2.destroyAllWindows()
video.release()

imgs[0].save("pres.pdf", save_all=True, append_images=imgs[1:])
print(len(imgs))