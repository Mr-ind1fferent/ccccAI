from os import mkdir, listdir
from os.path import exists
from shutil import copyfile

# isSaveOnePiece = False
isSaveOnePiece = True


path = '/home/hao/Code/PaddleDetection/videos/1_person/'
copyTo = 'copy/'

files = listdir(path)
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

    print('video:{} id:{} start:{} end:{} save:{}'.format(datas[i-1][0], datas[i-1][1], start, end, center))

    fileName = '{}_{}_{}.jpg'.format(datas[i - 1][0], datas[i - 1][1], '%05d' % center)
    source = path + fileName
    targetDir = '/'.join(path.split('/')[:-2])+'/' + copyTo
    if not exists(targetDir):
        mkdir(targetDir)
    target = targetDir + fileName
    if exists(source):
        copyfile(source, target)
        print('file coped:' + target)
    else:
        print('file not exist:' + source)

    i += 1

