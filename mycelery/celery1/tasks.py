# tasks.py
import os
from fcs import models
from FaceRecognitionSystem.FaceRe import FaceRecognition
from mycelery.main import app
@app.task
def student_detect_task(detefolder):
    KnowPepolePath = 'fcs/static/img'
    files = os.listdir(detefolder)
    for file in files:
        if file.endswith('.jpg') or file.endswith('.jpeg') or file.endswith('.png'):
            filepath = os.path.join(detefolder, file)
            f = FaceRecognition(filepath, KnowPepolePath)
            text = f.ShowImage(imgshow='disabled', waytocong='mindistance')
            if isinstance(text, str):
                info = models.student_info.objects.filter(name=text).first()
                if info:
                    StudentID = info.StudentID
                    name = info.name
                    models.student_record.objects.create(StudentID=StudentID, name=name)
                    os.remove(filepath)  # 删除文件
            else:
                print(f"识别失败: {file}")
