from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class Manager(models.Model):
    # 系统管理员 on_delete 用于指定数据删除方式
    # 管理员姓名
    mg_name = models.CharField(max_length=64)
    # 密码
    mg_passwd = models.CharField(max_length=64)
    # 邮箱
    email = models.CharField(max_length=64)
    # 电话
    mobile = models.CharField(max_length=64)
    # 状态
    mg_state = models.BooleanField(blank=True)
    # 创建时间
    add_time = models.DateTimeField(default = timezone.now)
    # 更新时间
    update_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.manager_name

class Video(models.Model):
    # video_name
    video_name = models.CharField(max_length=64)
    # url
    video_url = models.CharField(max_length=64)
    # create_time
    add_time = models.DateTimeField(auto_now=True)