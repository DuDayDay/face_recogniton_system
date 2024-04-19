import pickle
import face_recognition
from PIL import Image, ImageDraw, ImageFont
import os
import numpy as np
"""
Face Recognition
输入参数：file:检测图像的相对地址
        KnowPepolePath:存放已知人像存放文件夹子的位置
注意：KownPepole文件夹中不能存放其他数据，且不要改文件名，若需要改，请删除图像后重新加载
"""
class FaceRecognition:
    def __init__(self, file, KnowPepolePath):
        self.file = file
        self.img = Image.open(self.file)
        self.KnowPepolePath = KnowPepolePath
    # 图像降采样
    def DownImage(self):
        """ 降低输入检测图像的大小，提高检测效率"""
        size = self.img.size
        if size[0] > 2000 or size[1] > 2000:
            down_image = self.img.resize((round(size[0] / 10), round(size[1] / 10)))

        elif size[0] >1000 and size[0]<2000 or size[1] >1000 and size[1]<2000:
            down_image = self.img.resize((round(size[0] / 5), round(size[1] / 5)))

        else:
            down_image = self.img
        return down_image
    # 对比人物编码
    def KownPepole(self):
        """对每个已知人像进行编码并存入KnowEcoding.pkl中，但KnowPepole文件夹中的图像增加或减少时可以动态调整KnowEcoding.pkl,使其可以与KownPepole中的图像相对应"""
        # 检查是否存在保存的编码文件
        know_ecodings_file = 'KnowEcodings.pkl'
        if os.path.exists(know_ecodings_file):
            with open(know_ecodings_file, 'rb') as f:
                KnowEcoding, KnownImage_files = pickle.load(f)
        else:
            KnowEcoding = []
            KnownImage_files = []
        # 获取所有图像文件
        all_image_files = os.listdir(self.KnowPepolePath)

        # 检查是否有新的图像文件生成
        new_image_files = [img_file for img_file in all_image_files if img_file not in KnownImage_files]

        # 更新编码并保存
        for img_file in new_image_files:
            img_path = os.path.join(self.KnowPepolePath, img_file)
            img_path = img_path.replace("\\", "/")  # 修正路径分隔符
            known_image = face_recognition.load_image_file(img_path)
            biden_encoding = face_recognition.face_encodings(known_image)
            # 将新文件的编码添加到列表的尾部
            KnowEcoding.append(biden_encoding[0])
            # 将新文件名添加到列表的尾部
            KnownImage_files.append(img_file)
        # 检查是否有被删除的图像文件
        removed_image_files = [img_file for img_file in KnownImage_files if img_file not in all_image_files]
        for img_file in removed_image_files:
            index = KnownImage_files.index(img_file)
            # 从列表中删除相应的编码和文件名
            del KnowEcoding[index]
            del KnownImage_files[index]

        # 将编码保存到文件中
        with open(know_ecodings_file, 'wb') as f:
            pickle.dump((KnowEcoding, KnownImage_files), f)
        KnowEcoding = np.array(KnowEcoding)
        return KnowEcoding, KnownImage_files
    # 图像类型转换
    def ImageConvert(self, img):
        img = img.convert('RGB')
        img= np.array(img)
        return img
    # 检测图像位置识别
    def FaceRecog(self):
        down_image = self.DownImage()
        img_np = self.ImageConvert(down_image)
        # 返回每个人脸的位置信息：(top, right, bottom, left)
        face_locations = face_recognition.face_locations(img_np)
        if not face_locations:
            print("未检测到人脸")
            # 设置一个默认的最大人脸框
            largest_face_location = []
        else:
            # 寻找最大的人脸框
            max_area = 0
            largest_face_location = None
            for face_location in face_locations:
                top, right, bottom, left = face_location
                area = (bottom - top) * (right - left)
                if area > max_area:
                    max_area = area
                    largest_face_location = face_location
        return largest_face_location, img_np
    # 基于阈值的图像识别
    def FaceClass(self):
        [face_locations, img_np] = self.FaceRecog()
        [KnowEcodings, KnownImage_files] = self.KownPepole()
        if face_locations == []:
            # 返回一个空的结果列表
            return [], KnownImage_files
        else:
            Detect_encoding = face_recognition.face_encodings(img_np, [face_locations])[0]
            results = face_recognition.compare_faces(KnowEcodings, Detect_encoding, tolerance=0.45)
            # face_recognition.distances = face_recognition.face_distance()
            return results, KnownImage_files
    # 基于位置信息的图像识别
    def FaceClass_usedistance(self):
        [face_locations, img_np] = self.FaceRecog()
        [KnowEcodings, KnownImage_files] = self.KownPepole()

        if not face_locations:
            # 如果未检测到人脸，返回空结果列表
            return [], KnownImage_files
        else:
            # 获取检测到的人脸编码
            detected_encodings = face_recognition.face_encodings(img_np, [face_locations])[0]

            # 计算检测到的人脸编码与已知编码的相似度
            distances = face_recognition.face_distance(KnowEcodings, detected_encodings)
            mindistance = np.min(distances)
            if mindistance > 0.5:
                print('比配度过低')
                mindistance = round(1-mindistance, 2)
                return mindistance, KnownImage_files
            else:
                # 寻找最小距离对应的索引
                min_index = np.argmin(distances)

                # 获取对应索引处的结果
                result = [False] * len(KnowEcodings)
                result[min_index] = True
                return result, KnownImage_files
    def ShowImage(self, imgshow='abled', waytocong ='tolerance'):
        """识别信息的展示，默认情况下imgshow='able'，及展示识别后的图像，若不行展现，imgshow='disabled'
        waytocong='tolerance'是通过阈值来攀比的，waytocong='mindistance'是使用最小距离来判决"""
        DownImage = self.DownImage()
        if waytocong == 'tolerance':
            [result, KnownImage_files] = self.FaceClass()
        elif waytocong == 'mindistance':
            [result, KnownImage_files] = self.FaceClass_usedistance()
        else:
            print('waytocong的参数输入错误')
        if result == []:
            print("没有检测到人脸因此无法识别")
            # text = 'No faces found'
            text = 1
        else:
            largest_face_location, _ = self.FaceRecog()
            top, right, bottom, left = largest_face_location
            size = DownImage.size
            # 指定文字的起始位置
            position = (right, top)
            # 设置文字的颜色
            fill_color = (255, 255, 255)
            draw = ImageDraw.Draw(DownImage)
            if type(result) == type([]):
                files_name = [os.path.splitext(file)[0] for file in KnownImage_files]
                # 将列表转换为字符串
                text = ', '.join([value_b for value_a, value_b in zip(result, files_name) if value_a])
                if text == None:
                    # text = "无法与数据库中的人物匹配"
                    text = 1
            else:
                # text = '匹配的为:'+str(result)+'\n' + '匹配度过低，数据库中没有该人'
                text = 1
            font = ImageFont.truetype("simsun.ttc", 16)
            draw.text(position, text, fill=fill_color, font=font)
            # 标记最大人脸框
            if largest_face_location:
                draw.rectangle([left, top, right, bottom], outline="red", width=2)
            # 显示图像
            if imgshow == 'abled':
                DownImage.show()
        return text

def Detectfile(path):
    # 获取文件夹中所有文件
    files = os.listdir(path)
    # 滤除出图片文件
    img_files = [f for f in files if f.endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.JPG'))]
    img_paths = []
    for img_file in img_files:
        img_path = os.path.join(path, img_file)
        #遍历每个图像的相对路径2
        img_path.replace("\\", "/")
        img_paths.append(img_path)
    return img_paths


