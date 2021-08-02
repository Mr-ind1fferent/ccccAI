# ccccAI
# 使用说明
## 1:

创建models文件夹将,利用PaddleDetection将权重导出并放入

```
models/
      model1/infer_cfg.yml
             model.pdiparams
             model.pdiparams.info
             model.pdmodel
```

## 2：

创建Market-1501-v15.09.15文件夹，用来存放Re-ID的query和bounding_box_test

## 3：

运行main.py打开使用界面 

![image](https://user-images.githubusercontent.com/74087260/127842218-ad6b2869-8039-42a2-8b87-4ddc3882d933.png)

## 4：

首先界面右上角选择你自己准备的模型，并选择置信度和GPU或CPU加速。再添加你想要检测的视频（如果使用CPU多线程则线程数量对应视频数量），点击开始检测即可开始行人目标检测

## 5：

检测完毕之后的检测结果，将会被存放在output/detect。接着开始追踪，追踪完毕之后追踪结果会被存放在output/track当中

## 6：

### 多镜头使用说明：

添加两个及以上的视频（视频以数字命名且不要有下划线）且同个人在不同视频中都有出现。点击选择进行选择需要寻找的目标，根据追踪的结果，会自动将每个视频中的每个ID的图片单独抠出，存放在Market-1501-v15.09.15/bounding_box_test，每一个视频中的每一个id的一张图片会被存放在query文件夹中。

如下图：![image](https://user-images.githubusercontent.com/74087260/127846011-8c29477d-6b53-484f-8ebf-8810b99b1f02.png)


## 7：
选择一个id进行多镜头追踪，追踪完毕后会输出在输入的视频中目标的id、目标的图片和在视频中出现的当前帧
如下图：

![image](https://user-images.githubusercontent.com/74087260/127847880-4d7426da-ba7d-4e1c-81c0-91100ebbc014.png)


## 8：
并且输出图会保存在show.png中
