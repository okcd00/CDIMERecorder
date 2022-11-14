# CDIMERecorder
@okcd00 wants to record the top-ranked candidate words in Chinese IME.


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