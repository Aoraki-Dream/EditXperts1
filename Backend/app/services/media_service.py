import os
import cv2
import numpy as np
from paddleocr import PaddleOCR

# 初始化PaddleOCR，使用中文语言包和角度分类
ocr = PaddleOCR(use_angle_cls=True, lang='ch')

def process_image(username, img, picname):
    """
    处理上传的图像，执行OCR识别，并返回识别到的文本内容。

    :param username: str 用户名，用于创建用户目录
    :param img: FileStorage 上传的图像文件
    :param picname: str 保存图像的文件名
    :return: list 识别到的文本内容列表
    """
    # 读取图像文件并解码为ndarray
    file = img.read()
    file = cv2.imdecode(np.frombuffer(file, np.uint8), cv2.IMREAD_COLOR)

    # 创建保存图像的用户目录
    imgfile1_path = f"./static/images/{username}/"
    if not os.path.exists(imgfile1_path):
        os.makedirs(imgfile1_path)
    
    # 保存解码后的图像到指定路径
    img1_path = os.path.join(imgfile1_path, picname)
    cv2.imwrite(filename=img1_path, img=file)

    # 使用OCR进行文本识别
    result = ocr.ocr(img1_path, cls=True)
    texts = []
    for res in result:
        for line in res:
            text, confidence = line[-1]
            texts.append(text)

    # 删除处理完的图片
    if os.path.exists(img1_path):
        os.remove(img1_path)
    
    return texts
