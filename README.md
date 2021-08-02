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

创建Market-1501-v15.09.15文件夹，用来存放Re-ID的query和bounding-box-test

## 3：

运行main.py
