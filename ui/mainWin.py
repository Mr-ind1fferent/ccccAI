import os
import platform
import threading

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMessageBox, QDesktopWidget
from ui.mainWindow import Ui_MainWindow
from ui.videoFrame import FileException
from ui.videoFrame import VideoFrame
from ui_tools.detectCmdExecutor import DetectCmdExecutor
from ui_tools.trackCmdExecutor import TrackCmdExecutor
from ui.targetWin import TargetWin
from ui_tools.fileProcessor import FileProcessor
from ui.targetResultWin import TargetResultWin


class MainWin(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.result_win = TargetResultWin()
        self.thread_lock = threading.Lock()
        self.setupUi(self)
        self.init_connect()
        self.isWindows = platform.uname().system == 'Windows'
        self.isSave = False
        self.isUseGPU = False
        self.isParallel = True
        self.isProcessing = False
        self.isPreviewDetect = True
        self.isPreviewTrack = True
        self.isFileProcessed = False
        self.savePath = ''
        self.doubleSpinBox.setValue(0.80)
        self.refresh_slider()
        self.row = 0
        self.col = 0
        self.vfs = []
        self.model_path = self.output_path = self.infer = self.model_dir = self.use_gpu = self.thread_hold = ''
        self.infer_mot = self.config = self.video_file = self.save_videos = ''
        self.processedCount = 0
        self.executors = []
        self.totalFrame = 0
        self.processedFrame = 0
        self.threadNum = 1
        self.modelPath = [
            'models/model1',
            'models/model2'
        ]
        self.pythonPath = 'python'
        self.select_win = None

        if self.isWindows:
            self.btn_stop.close()
        else:
            self.scrollArea.setFrameShape(QtWidgets.QFrame.StyledPanel)
            self.frame_detect.setFrameShape(QtWidgets.QFrame.StyledPanel)
            self.frame_track.setFrameShape(QtWidgets.QFrame.StyledPanel)
            self.frame_select.setFrameShape(QtWidgets.QFrame.StyledPanel)
            # self.frame_save.setFrameShape(QtWidgets.QFrame.StyledPanel)
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2,
                  (screen.height() - size.height()) / 2)

    def init_connect(self):
        self.action_add_video.triggered.connect(self.add_video)
        self.btn_add_video.clicked.connect(self.add_video)
        self.slider_confidence.valueChanged.connect(self.refresh_spinbox)
        self.doubleSpinBox.valueChanged.connect(self.refresh_slider)
        self.btn_process_detect.clicked.connect(self.start_detect)
        self.btn_process_track.clicked.connect(self.start_track)
        # self.btn_change_path.clicked.connect(self.change_path)
        self.radioButton_use_gpu.clicked.connect(self.switch_gpu_parallel)
        self.radioButton_parallel.clicked.connect(self.switch_gpu_parallel)
        # self.checkBox_save.clicked.connect(self.switch_save)
        self.btn_stop.clicked.connect(self.on_btn_stop_clicked)
        self.btn_select_win.clicked.connect(self.file_process)

    def add_video(self):
        vf = VideoFrame(self)
        self.vfs.append(vf)
        frame = vf.get_frame()
        try:
            vf.load()
            self.gridLayout_2.addWidget(frame, self.row, self.col, 1, 1)
            self.col = (self.col + 1) % 2
            self.row = self.row + (1 if self.col == 0 else 0)
            self.gridLayout_2.removeWidget(self.btn_add_video)
            self.gridLayout_2.addWidget(self.btn_add_video, self.row, self.col, 1, 1)
        except FileException:
            self.vfs.pop()

    def refresh_spinbox(self):
        self.doubleSpinBox.setValue(self.slider_confidence.value() / 100)

    def refresh_slider(self):
        self.slider_confidence.setValue(self.doubleSpinBox.value() * 100)

    def start_detect(self):
        self.processedCount = 0
        for vf in self.vfs:
            vf.set_detect_mode(True)
        if not self._source_check():
            return
        self.isProcessing = True
        self.threadNum = self.spinBox_parallel.value()
        self.isParallel = (self.threadNum > 1 and len(self.vfs) > 1)
        self.isPreviewDetect = self.checkBox_preview_detect.isChecked()
        self.model_path = self.modelPath[self.comboBox_model.currentIndex()]
        # self.output_path = self.lineEdit_path.text()
        self.infer = ' deploy/python/infer.py'
        self.model_dir = ' --model_dir=' + self.model_path
        self.use_gpu = ' --use_gpu=' + str(self.isUseGPU)
        self.thread_hold = ' --threshold=' + str(self.doubleSpinBox.value())

        self.executors.clear()
        for i in range(self.threadNum):
            self._start_new_detect_thread()
        self.update_ui()

    def _source_check(self):
        if len(self.vfs) < 1:
            QMessageBox.warning(self, "未添加源", "请点击左边'+'按钮添加视频源", QMessageBox.Ok, QMessageBox.Ok)
            return False
        return True

    def _start_new_detect_thread(self):
        if self.processedCount < len(self.vfs):
            vf = self.vfs[self.processedCount]
            file_name = vf.get_file_name()
            print("开始处理:", file_name)
            video_file = ' --video_file=' + vf.get_path()
            output_dir = (' --output_dir=' +
                          (('output/detect/' + vf.get_file_name_no_ext()) if self.output_path == ''
                           else self.output_path))
            order = (self.pythonPath
                     + self.infer + self.model_dir + video_file + self.use_gpu + output_dir + self.thread_hold)
            executor = DetectCmdExecutor(order, self.thread_lock, self.isParallel)
            executor.setName(file_name)
            executor.gotFrameCount.connect(self._refresh_total_frame)
            # executor.gotFrameDetect.connect(self._refresh_total_processed_bar)
            executor.tempReady.connect(vf.enter_temp_detect_mod)
            if self.isPreviewDetect:
                executor.gotTempImg.connect(vf.set_progressing_img)
            executor.gotPeopleNum.connect(vf.set_progressing_people_num)
            executor.updateProgress.connect(vf.set_progress_bar)
            executor.videoSaved.connect(vf.exit_temp_detect_mod)
            executor.videoSaved.connect(self._start_new_detect_thread)
            executor.videoSaved.connect(self.on_finished_one)
            executor.start()
            self.executors.append(executor)
            self.processedCount += 1

    def _refresh_total_frame(self, new_count: int):
        self.totalFrame += new_count
        print("线程池中总帧数:", self.totalFrame)
        self.refresh_label_process()

    def _refresh_total_processed_bar(self):
        # self.processedFrame += 1
        if len(self.vfs) > 0:
            self.progressBar_process.setValue(int(self.processedCount / len(self.vfs)) * 100)
        # if self.isParallel:
        #     print("总已处理帧:", self.processedFrame)

    def refresh_label_process(self):
        names = []
        for executor in self.executors:
            if executor.is_executing():
                names.append(executor.getName())
        self.label_process.setText("正在处理{}:".format(names))

    def start_track(self):
        self.processedCount = 0
        for vf in self.vfs:
            vf.set_detect_mode(False)
        if not self._source_check():
            return
        self.isPreviewTrack = self.checkBox_preview_track.isChecked()
        self.infer_mot = ' tools/infer_mot.py'
        self.config = ' -c configs/mot/deepsort/deepsort_pcb_pyramid_r101.yml'
        self.save_videos = ' --save_videos'

        self.executors.clear()
        self._start_new_track_thread()

        self.isProcessing = True
        self.update_ui()

    def _start_new_track_thread(self):
        if self.processedCount < len(self.vfs):
            vf = self.vfs[self.processedCount]
            file_name: str = vf.get_file_name()
            print("开始处理:", file_name)
            file_name_no_ext: str = vf.get_file_name_no_ext()
            det_results_dir = ' --det_results_dir=output/detect/' + file_name_no_ext + '/'
            txt_file = 'output/detect/{}/{}.txt'.format(file_name_no_ext, file_name_no_ext)
            if not os.path.exists(txt_file):
                print('文件不存在:' + txt_file)
                QMessageBox.warning(self, '文件不存在', '运行追踪前请先运行检测，确保{}文件存在'.format(txt_file))
                return
            video_file = ' --video_file=' + str(vf.get_path()[8:] if self.isWindows else vf.get_path()[7:])
            track_output_dir = ' --output_dir=output/track/' + file_name_no_ext + '/'
            order = (self.pythonPath +
                     self.infer_mot + self.config + det_results_dir + video_file + track_output_dir + self.save_videos)

            # print(order)
            # return

            executor = TrackCmdExecutor(order, self.thread_lock)
            executor.setName(file_name)
            executor.startedTrack.connect(vf.enter_temp_track_mod)
            executor.updateProgress.connect(vf.set_progress_bar)
            # executor.updateProgress.connect(self._refresh_total_processed_bar)
            if self.isPreviewTrack:
                executor.gotTempImg.connect(vf.set_progressing_img)
            else:
                executor.updateProgress.connect(vf.set_progressing_text)
            executor.gotFrameCount.connect(self._refresh_total_frame)
            executor.finishedTrack.connect(self._start_new_track_thread)
            executor.savedVideo.connect(vf.exit_temp_track_mod)
            executor.savedVideo.connect(self.on_finished_one)
            executor.start()
            self.executors.append(executor)

        self.processedCount += 1

    def update_ui(self):
        is_processing = self.isProcessing
        self.btn_stop.setEnabled(is_processing)
        if is_processing:
            self.btn_stop.setFocus()
        else:
            self.progressBar_process.setValue(0)
        self.frame_detect.setEnabled(not is_processing)
        self.frame_track.setEnabled(not is_processing)
        self.frame_select.setEnabled(not is_processing)
        # self.frame_save.setEnabled(not is_processing)
        self.label_process.setText("正在处理" if is_processing else "等待处理")

    def on_finished_one(self):
        self._refresh_total_processed_bar()
        if self.processedCount >= len(self.vfs):
            self.isProcessing = False
            self.update_ui()

    def on_btn_stop_clicked(self):
        for executor in self.executors:
            executor.terminate()
        for vf in self.vfs:
            vf.exit_temp_detect_mod()
        self.isProcessing = False
        self.executors.clear()
        self.processedFrame = 0
        self.totalFrame = 0
        self.processedCount = 0
        self.btn_stop.setEnabled(False)
        self.progressBar_process.setValue(0)
        self.update_ui()

    # def change_path(self):
    #     path = QFileDialog.getExistingDirectory()
    #     self.savePath = path
    #     self.lineEdit_path.setText(path)

    def switch_gpu_parallel(self):
        self.isUseGPU = self.radioButton_use_gpu.isChecked()
        self.isParallel = self.radioButton_parallel.isChecked()
        self.spinBox_parallel.setEnabled(self.isParallel)

    def switch_save(self):
        self.isSave = self.checkBox_save.checkState()
        self.label_path.setEnabled(self.isSave)
        self.btn_change_path.setEnabled(self.isSave)
        self.lineEdit_path.setEnabled(self.isSave)

    def file_process(self):
        self.processedCount = 0
        # if not self._source_check():
        #     return
        if self.isFileProcessed:
            self.select_win.show()
            return
        self.btn_select_win.setEnabled(False)
        self.btn_select_win.setText('正在处理文件...')
        videos = []
        output_dirs = []
        person_dirs = []
        txt_files = []
        select_person_dirs = []
        for vf in self.vfs:
            videos.append(vf.get_path())
            video_name_no_ext = vf.get_file_name_no_ext()
            output_dir = os.path.abspath('output/frames/{}/all'.format(video_name_no_ext)) + '/'
            person_dir = os.path.abspath('output/frames/person') + '/'
            txt_file = os.path.abspath('output/track/{}/mot_results/{}.txt'.format(video_name_no_ext, video_name_no_ext))
            select_person_dir = os.path.abspath('Market-1501-v15.09.15/bounding_box_test/') + '/'
            if self.isWindows:
                output_dir = output_dir.replace('\\', '/')
                person_dir = person_dir.replace('\\', '/')
                txt_file = txt_file.replace('\\', '/')
                select_person_dir = select_person_dir.replace('\\', '/')
            output_dirs.append(output_dir)
            person_dirs.append(person_dir)
            txt_files.append(txt_file)
            select_person_dirs.append(select_person_dir)
        # print(videos, output_dirs, person_dirs, txt_files, select_person_dirs)
        processor = FileProcessor(videos, output_dirs, person_dirs, txt_files, select_person_dirs)
        processor.finishedOneFileProcess.connect(self.finished_one_file_process)
        processor.finished.connect(self.finished_file_process)
        processor.start()
        self.isProcessing = True
        self.update_ui()

    def finished_one_file_process(self):
        self.processedCount += 1
        self.progressBar_process.setValue(round(self.processedCount / len(self.vfs)) * 100)

    def finished_file_process(self):
        self.processedCount = 0
        self.progressBar_process.setValue(0)
        self.btn_select_win.setEnabled(True)
        self.btn_select_win.setText('选择...')
        self.isProcessing = False
        self.update_ui()
        self.select_win = TargetWin('Market-1501-v15.09.15/bounding_box_test/')
        self.select_win.gotTopImages.connect(self.on_got_top_images)
        self.isFileProcessed = True

    def on_got_top_images(self, images: list):
        self.btn_result.clicked.connect(self.result_win.show)
        for img in images:
            img = str.strip(img)
            file_name = img.split('/')[-1].split('.')[0]
            video_name_no_ext, person, frame = file_name.split('_')
            for vf in self.vfs:
                if vf.get_file_name_no_ext() == video_name_no_ext:
                    vf.set_video_position_with_frame(int(frame))
                    self.result_win.add_item(video_name_no_ext, person, img, vf.get_position_by_frame(int(frame)))
        # self.select_win.hide()
        self.result_win.show()

