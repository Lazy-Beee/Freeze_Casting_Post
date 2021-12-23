import cv2
import os.path
path = os.getcwd()

frames = [str(200*i).zfill(4) for i in range(1, 13)]
file_path = 'images/12-04-2021'
img_array = []
for frame in frames:
    img = cv2.imread(os.path.dirname(path) + f'/{file_path}/{frame}.png')

    font = cv2.FONT_HERSHEY_SIMPLEX
    bottomLeftCornerOfText = (300, 50)
    fontScale = 1
    fontColor = (255, 255, 255)
    thickness = 2
    lineType = 2

    cv2.putText(img, f'Time = {frame}s',
                bottomLeftCornerOfText,
                font,
                fontScale,
                fontColor,
                thickness,
                lineType)

    height, width, layers = img.shape
    size = (width, height)
    img_array.append(img)

out = cv2.VideoWriter(os.path.dirname(path) + f'/{file_path}/video.avi',
                      cv2.VideoWriter_fourcc(*'DIVX'), 1.2, size)

for i in range(len(img_array)):
    out.write(img_array[i])
out.release()