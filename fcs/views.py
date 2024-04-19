from django.http import JsonResponse
from django.template.loader import render_to_string
from django.shortcuts import render, redirect
import os
from fcs import models
from django.http import JsonResponse
from mycelery.celery1.tasks import student_detect_task

# Create your views here.
def StudentList(request):
    """学生列表"""
    queryset = models.student_info.objects.all()
    return render(request, 'StudentList.html',{'queryset': queryset})
def ImageList(name,file_object):
    file_name = name + '.jpg'
    # 指定保存文件的文件夹路径
    folder_path = os.path.join(os.getcwd(), 'fcs/static/img')
    # 如果文件夹不存在，则创建它
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    # 保存文件到指定文件夹中
    file_path = os.path.join(folder_path, file_name)
    with open(file_path, mode='wb') as f:
        for chunk in file_object.chunks():
            f.write(chunk)
    f.close()
    return file_path
def StudentAdd(request):
    """添加页面"""
    if request.method == 'GET':
        return render(request, 'StudentAdd.html')
    # 获取用户post数据
    file_object = request.FILES.get('image')
    name = request.POST.get('name')
    ImgUrl = ImageList(name,file_object)
    StudentID = request.POST.get('studentId')
    age = request.POST.get('age')
    # 添加到数据库
    models.student_info.objects.create(StudentID =StudentID, name =name, age =age, ImgUrl = ImgUrl)
    return redirect('/Student/list/')
def StudentDelete(request,nid):
    itmes = models.student_info.objects.get(id=nid)
    file_path = itmes.ImgUrl
    if os.path.exists(file_path):
        # 如果文件存在，删除它
        os.remove(file_path)
        print(f"文件 '{file_path}' 已成功删除。")
    models.student_info.objects.get(id=nid).delete()
    return redirect('/Student/list/')
def StudentEdit(request,nid):
    if request.method == 'GET':
        qurist = models.student_info.objects.filter(id=nid).first()
        path = 'img/'+ qurist.name + '.jpg'
        print(path)
        return render(request,'StuentEdit.html',{'qurist':qurist , 'path':path})
    update_data = {
        'StudentID': request.POST.get('studentId'),
        'age': request.POST.get('age')
        # 添加更多字段和对应的值
    }
    models.student_info.objects.filter(id=nid).update(**update_data)
    return redirect('/Student/list/')
def StudentRecord(request):
    # 获取所有的学生记录对象
    queryset = models.student_record.objects.all()
    return render(request, 'StudentRecord.html', {'queryset': queryset})
def StudentRecordTableData(request):
    # 获取所有的学生记录对象
    queryset = models.student_record.objects.all()
    # 渲染 'student_table_snippet.html' 模板，获取 HTML 字符串
    table_html = render_to_string('student_table_snippet.html', {'queryset': queryset})
    # 返回 JSON 响应
    return JsonResponse({'table_html': table_html})
def start_student_detection(request):
    # 异步执行学生识别任务
    student_detect_task.delay('fcs/DetectPepole')
    return JsonResponse({'message': 'Student detection started successfully.'})
def StudentRecordDelete(request,nid):
    models.student_record.objects.get(id=nid).delete()
    return redirect('/Student/Record/')
