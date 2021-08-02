import os
from threading import Thread
from PyQt5.QtCore import pyqtSignal, QObject
from os.path import exists

from ui_tools.img_utils import video_to_img, get_person_from_img, images_dir_reduce


class FileProcessor(Thread, QObject):
    finishedOneFileProcess = pyqtSignal()
    finished = pyqtSignal()

    def __init__(self, video_paths, output_dirs, person_dirs, txt_files, select_person_dirs):
        Thread.__init__(self)
        QObject.__init__(self)
        self.videoPaths = video_paths
        self.outputDirs = output_dirs
        self.personDirs = person_dirs
        self.txtFiles = txt_files
        self.selectPersonDirs = select_person_dirs

    def run(self) -> None:

        for i in range(len(self.videoPaths)):

            video_to_img(self.videoPaths[i], self.outputDirs[i])

            if not exists(self.txtFiles[i]):
                print(self.txtFiles[i]+'不存在')
                break

            # print(self.outputDirs[i], self.personDirs[i], self.txtFiles[i])

            get_person_from_img(self.outputDirs[i], self.personDirs[i], self.txtFiles[i])

            images_dir_reduce(self.personDirs[i], self.selectPersonDirs[i])

            save_to_query(self.selectPersonDirs[i])

            self.finishedOneFileProcess.emit()

        self.finished.emit()


def save_to_query(source_dir: str):
    from shutil import copytree, rmtree
    query_dir = '/'.join(source_dir.split('/')[:-2]) + '/query/'
    if os.path.exists(query_dir):
        rmtree(query_dir)
    copytree(source_dir, query_dir)
