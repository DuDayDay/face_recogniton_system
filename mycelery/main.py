import os
from django.core.management import call_command
from celery import Celery

# 设置 Celery 应用的默认配置
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FaceRecognitionSystem.settings')

# 创建 Celery 应用实例
app = Celery('FaceRecognitionSystem')

# 加载 Celery 配置
app.config_from_object('mycelery.config')

# 加载任务模块
app.autodiscover_tasks(['mycelery.celery1'])

# 启动 Celery worker
# if __name__ == '__main__':
#     # 在启动 Celery worker 前不加载数据
#     # call_command('loaddata', 'initial_data.json')  # 加载初始化数据（可选）
#
#     # 启动 Celery worker
#     app.worker_main(['celery', '-A', 'mycelery.main', 'worker', '--loglevel=info'])
#
#     # 在启动 Celery worker 后加载数据
#     # call_command('loaddata', 'initial_data.json')  # 加载初始化数据（可选）
# redis-cli.exe
# 127.0.0.1:6379>shutdown
# (error)NOAUTH Authentication required
# 127.0.0.1:6379>AUTH 2004321
# OK
# 127.0.0.1:6379>shutdown
# not connected>exit
# redis-server.exe
# # celery -A mycelery.main worker -l debug -P eventlet
