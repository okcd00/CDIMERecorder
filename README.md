# CDIMERecorder
@okcd00 wants to record the top-ranked candidate words in Chinese IME.


## 结果文件

**当前进度 (22/11/19 15:00)： `微软输入法` - `双字全拼` - `anben`** 

> 由于 `typist` 方法是模拟输入，所以时间消耗较大，给出平均耗时作为参考：   
> 单字全拼，top-80 候选时，全序列：`424it [11:09:56, 94.80s/it]`     
> 双字全拼，top-16 候选时，单序列：`424it [4:46:17, 40.51s/it]` x 424 times    
> 三字全拼，top-8 候选时，单序列：`424it [4:46:17, 40.51s/it]` x (424 x 424) times    
> 当具有较为准确的 OCR 方法时，耗时约为 23s 和 14s (使用 PaddleHub-OCR 测试)。

| IME      |    Result File | Description | Recording Logs  |
| :-------- | :--------: | --- | :--: |
| Microsoft |   [结果文件]('./release/input_candidates.microsoft.json')<br>  | 微软输入法，关闭动态词频调整、自学习与云服务 | [原始录入日志 (单字全拼)]('./release/microsoft/input_candidates.typist.1c40_log.txt') &#x2705; <br>[原始录入日志 (双字全拼)]('./release/microsoft/input_candidates.typist.2c16_log.txt') &#x1F40C; <br>[原始录入日志 (三字全拼)]('./release/microsoft/input_candidates.typist.3c8_log.txt') &#x23F3; |
| Tencent |   [结果文件]('./release/input_candidates.tencent.json')<br>  | QQ 输入法，关闭云组词、智能推荐、表情包 | [原始录入日志 (单字全拼)]('./release/tencent/input_candidates.typist.1c40_log.txt') &#x23F3; <br>[原始录入日志 (双字全拼)]('./release/tencent/input_candidates.typist.2c16_log.txt') &#x23F3; <br>[原始录入日志 (三字全拼)]('./release/input_candidates.typist.3c8_log.txt') &#x23F3; |
| Sogou |   [结果文件]('./release/input_candidates.sogou.json')<br>  | 搜狗输入法，待后续追加 | [原始录入日志 (单字全拼)]('./release/sogou/input_candidates.typist.1c40_log.txt') &#x23F3; <br>[原始录入日志 (双字全拼)]('./release/sogou/input_candidates.typist.2c16_log.txt') &#x23F3; <br>[原始录入日志 (三字全拼)]('./release/sogou/input_candidates.typist.3c8_log.txt') &#x23F3; |

## setup

conda 环境
```
# 在命令行输入以下命令，创建名为paddle_env的环境
# 此处为加速下载，使用清华源
conda create --name paddle_env python=3.8 --channel https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
# source D:/Anaconda/Scripts/activate paddle_env
```

安装 paddlepaddle
```
# pip
pip install paddlepaddle -i https://mirror.baidu.com/pypi/simple
```

安装 PaddleOCR
```
# Shapely 直接 pip 可能装不好，repo 里也准备了 whl 用于安装
pip install ./dist/Shapely-1.8.2-cp38-cp38-win_amd64.whl 
pip install "paddleocr>=2.0.1"
```

可能会出现没有 14.0 以上 C++ 构建工具环境的问题，去网站下载个
```
error: Microsoft Visual C++ 14.0 or greater is required. Get it with "Microsoft C++ Build Tools": https://visualstudio.microsoft.com/visual-cpp-build-tools/
```

PaddleOCR 老出问题，转而安装 PaddleHub
用 PaddleHub 装载 ICDAR2015 数据集训练出来的 [Differentiable Binarization+CRNN](https://arxiv.org/pdf/1507.05717.pdf) OCR 模型：
```
pip install paddlehub -i https://mirror.baidu.com/pypi/simple
# hub install chinese_ocr_db_crnn_server==1.1.3
# 跟我一样 hub 指令无效的，可以直接调用 src/paddle_hub.py 自动下载模型文件。
```

关于 `win32gui 找不到指定的模块` 问题
```
# 去找环境的 scripts 目录
# cd D:\Anaconda\Scripts
python pywin32_postinstall.py -install
```