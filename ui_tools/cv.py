from cv2 import VideoWriter, VideoWriter_fourcc, imread, resize, imdecode, destroyAllWindows
from os import listdir
from PIL import Image
from numpy import fromfile, uint8


def pic_to_video(imgPath: str, videoPath: str):
    images = listdir(imgPath)
    fps = 25  # 每秒25帧数

    # VideoWriter_fourcc为视频编解码器 ('I', '4', '2', '0') —>(.avi) 、('P', 'I', 'M', 'I')—>(.avi)、('X', 'V', 'I', 'D')—>(.avi)、('T', 'H', 'E', 'O')—>.ogv、('F', 'L', 'V', '1')—>.flv、('m', 'p', '4', 'v')—>.mp4
    fourcc = VideoWriter_fourcc('m', 'p', '4', 'v')

    image = Image.open(imgPath + images[0])
    videoWriter = VideoWriter(videoPath, fourcc, fps, image.size)
    for im_name in range(len(images)):
        frame = imdecode(fromfile((imgPath + images[im_name]), dtype=uint8), 1)  # 此句话的路径可以为中文路径
        print(im_name)
        videoWriter.write(frame)
    print("图片转视频结束！")
    videoWriter.release()
    destroyAllWindows()


if __name__ == '__main__':
    pic_to_video('/home/hao/Code/PaddleDetection/videos/1/', '/home/hao/Code/PaddleDetection/videos/1.mp4')
