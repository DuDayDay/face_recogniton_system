from django.db import models
# Create your models here.
class student_info(models.Model):
    name = models.CharField(max_length=10,verbose_name="姓名",default='zhan')
    StudentID = models.CharField(max_length=10, verbose_name="学号",default='xxx')
    age = models.IntegerField(verbose_name="年龄",default=0)
    ImgUrl = models.URLField(verbose_name="图像地址",default='http:')
class student_record(models.Model):
    name = models.CharField(max_length=10,verbose_name="姓名")
    StudentID = models.CharField(max_length=10, verbose_name="学号", default='xxx')
    time = models.DateTimeField(verbose_name="识别时间", auto_now_add=True)
