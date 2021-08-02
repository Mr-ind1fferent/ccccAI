def get_person_from_img(root_dir: str, save_dir: str, txt_file: str):
    """

    Args:
        root_dir: 视频源图片存放地址
        save_dir: 保存地址
        txt_file: 检测文件地址


    """

    from os.path import join, exists
    from os import makedirs
    from PIL import Image
    import glob

    # for imgs_dir in glob.glob(root_path + '/*'):
    video_name = root_dir.split('/')[-3]
    # print(txt_file)
    if not exists(save_dir):
        # print(save_dir)
        makedirs(save_dir)

    with open(txt_file, 'r') as f:
        frame = 1
        frame_name = 3
        flag = False
        for img in glob.glob(root_dir + '/*'):
            im = Image.open(img)
            # print(frame, frame_name)
            while frame_name != '' and frame == int(frame_name):
                # print(1)
                if frame_name != '':
                    if not flag:

                        data = f.readline()
                        data = data.split(',')
                        # print('data:', data)
                        frame_name = data[0]
                        # print('frame_name:', frame_name)

                        if frame_name!='' and frame == int(frame_name):
                            id_name = data[1]
                            bbox = data[2:6]
                            # print('id_name:', id_name)
                            # print('bbox:', (int(float(bbox[0])),
                            #                    int(float(bbox[1])),
                            #                    int(float(bbox[2]) + float(bbox[0])),
                            #                    int(float(bbox[3]) + float(bbox[1]))))
                            cropped = im.crop((int(float(bbox[0])),
                                               int(float(bbox[1])),
                                               int(float(bbox[2]) + float(bbox[0])),
                                               int(float(bbox[3]) + float(bbox[1]))))
                            file = join(save_dir + '/',
                                        video_name + '_'
                                        + '%03d' % int(id_name) + '_'
                                        + '%05d' % int(frame_name) + '.jpg')
                            cropped.save(file)
                        else:
                            flag = True

                    elif frame == int(frame_name):
                        # print(2)
                        flag = False
                        id_name = data[1]
                        bbox = data[2:6]
                        cropped = im.crop((int(float(bbox[0])),
                                           int(float(bbox[1])),
                                           int(float(bbox[2]) + float(bbox[0])),
                                           int(float(bbox[3]) + float(bbox[1]))))
                        file = join(save_dir + '/',
                                    video_name + '_'
                                    + '%03d' % int(id_name) + '_'
                                    + '%05d' % int(frame_name) + '.jpg')
                        cropped.save(file)

            frame = frame + 1
            # print(3)


def video_to_img(video_file: str, output_dir: str):
    """

    Args:
        video_file: 视频地址
        output_dir: 输出文件夹

    """

    import cv2
    from os import makedirs
    from os.path import exists
    num = 1

    if not exists(output_dir):
        makedirs(output_dir)

    vid = cv2.VideoCapture(video_file)
    while vid.isOpened():
        is_read, frame = vid.read()
        if is_read:
            # if num % interval == 1:
            file_name = '%05d' % num
            cv2.imwrite(output_dir + str(file_name) + '.jpg', frame)
            # 00000111.jpg 代表第111帧
            cv2.waitKey(1)
            # print(frame)
            num += 1

        else:
            break


def images_dir_reduce(source_dir: str, result_dir: str, ):
    from os import mkdir, listdir
    from os.path import exists
    from shutil import copyfile

    # isSaveOnePiece = False
    isSaveOnePiece = True


    # source_dir = '/home/hao/Code/PaddleDetection/videos/1_person/'
    # copy_to = 'copy/'

    if not exists(source_dir):
        print('文件夹不存在:'+source_dir)
        return
    files = listdir(source_dir)
    files.sort()

    datas = [[]]

    for file in files:
        data = file.split('.')[0].split('_')  # video id frame
        # print(data)
        datas.append(data)

    start = end = 0
    i = 2
    length = len(datas)

    while True:

        if i > length:
            break

        start = datas[i-1][2]

        while i < length and int(datas[i][2]) == int(datas[i-1][2]) + 1 and datas[i][1] == datas[i-1][1] and datas[i][0] == datas[i-1][0]:
            i += 1

        end = datas[i-1][2]

        center = int((int(end) + int(start)) / 2)

        if isSaveOnePiece:
            while i < length and int(datas[i][1]) == int(datas[i-1][1]) and datas[i][0] == datas[i-1][0]:
                i += 1

        # print('video:{} id:{} start:{} end:{} save:{}'.format(datas[i-1][0], datas[i-1][1], start, end, center))

        fileName = '{}_{}_{}.jpg'.format(datas[i - 1][0], datas[i - 1][1], '%05d' % center)
        source = source_dir + fileName
        # result_dir = '/'.join(source_dir.split('/')[:-2]) +'/' + result_dir
        if not exists(result_dir):
            mkdir(result_dir)
        target = result_dir + fileName
        if exists(source):
            copyfile(source, target)
            # print('file coped:' + target)
        else:
            print('file not exist:' + source)

        i += 1


if __name__ == '__main__':
    # video_to_img(video_file=r"/home/hao/Code/PaddleDetection/videos/1.mp4",
    #              output_dir=r"/home/hao/Code/PaddleDetection/videos/1/")

    get_person_from_img(root_dir='/home/hao/Code/PaddleDetection/output/frames/1',
                        save_dir='/home/hao/Code/PaddleDetection/output/frames/1_person/',
                        txt_file='/home/hao/Code/PaddleDetection/output/track/1/1.txt')

    images_dir_reduce(source_dir='/home/hao/Code/PaddleDetection/output/frames/1/person/',
                      result_dir='/home/hao/Code/PaddleDetection/output/frames/1/select_person/')

