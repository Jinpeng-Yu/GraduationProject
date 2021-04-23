from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse, HttpResponse
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import random
import json
import cv2
from .IIM.videoAnalyser import *

from .models import Manager
from .models import Video

# Create your views here.
@require_http_methods(["GET"])
def login(request):
    response = {}
    print("用户提交了用户名和密码")
    username = request.GET.get('username')
    passwd = request.GET.get('password')
    user = Manager.objects.filter(mg_name= username, mg_passwd=passwd, mg_state=1)
    if user:
        response['msg'] = 'success'
        response['error_num'] = 0
    else:
        response['msg'] = 'false'
        response['error_num'] = 1
    return JsonResponse(response)


@require_http_methods(["GET"])
def add_manager(request):
    response = {}
    print('添加管理员操作')
    try:
        manager = Manager(mg_name = request.GET.get('username'),
                          mg_passwd = request.GET.get('password'),
                          email = request.GET.get('email'),
                          mobile = request.GET.get('mobile'),
                          mg_state = True)
        manager.save()
        print(manager)
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)

@require_http_methods(["GET"])
def delete_manager(request):
    response = {}
    print('删除管理员操作')
    try:
        manager = Manager.objects.filter(id=request.GET.get('userid'),)
        if manager:
            manager.delete()
            response['msg'] = 'success'
            response['error_num'] = 0
        else:
            response['msg'] = 'none'
            response['error_num'] = 2
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)

@require_http_methods(["GET"])
def update_manager(request):
    response = {}
    print('更新管理员操作')
    try:
        manager = Manager.objects.filter(id=request.GET.get('userid'),)[0]
        if manager:
            manager.email = request.GET.get('email')
            manager.mobile = request.GET.get('mobile')
            manager.save()
            # manager.update(manager_name = request.GET.get('manager_name'))
            # manager.update(manager_passwd=request.GET.get('manager_passwd'))
            response['msg'] = 'success'
            response['error_num'] = 0
        else:
            response['msg'] = 'none'
            response['error_num'] = 2
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)

@require_http_methods(["GET"])
def update_manager_state(request):
    response = {}
    print('更新管理员状态操作')
    try:
        manager = Manager.objects.filter(id=request.GET.get('userid'),)[0]
        if manager:
            if manager.mg_state:
                manager.mg_state = False
            else:
                manager.mg_state = True
            manager.save()
            response['msg'] = 'success'
            response['error_num'] = 0
        else:
            response['msg'] = 'none'
            response['error_num'] = 2
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)

@require_http_methods(["GET"])
def show_managers(request):
    response = {}
    try:
        managers = Manager.objects.filter(mg_name__contains= request.GET.get('query')).order_by('id')
        # managers = Manager.objects.all().order_by('id')
        response['total'] = len(managers)
        # response['list'] = json.loads(serializers.serialize("json", manager_list))

        pagesize = request.GET.get('pagesize', default=5)
        paginator = Paginator(managers, pagesize)
        pagenum = request.GET.get('pagenum', default=1)

        # 根据页码取数据
        try:
            manager_list = paginator.page(pagenum)
        except PageNotAnInteger as e:
            # 非整数返回第一页数据
            manager_list = paginator.page('1')
            pagenum = 1
        except EmptyPage as e:
            # 当参数页码大于或小于页码范围时,会触发该异常
            print('EmptyPage:{}'.format(e))
            if int(pagenum) > paginator.num_pages:
                # 大于 获取最后一页数据返回
                manager_list = paginator.page(paginator.num_pages)
            else:
                # 小于 获取第一页
                manager_list = paginator.page(1)
        response['managers'] = json.loads(serializers.serialize("json", manager_list))
        response['pagenum'] = pagenum
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)

@require_http_methods(["GET"])
def get_user_by_id(request):
    response = {}
    manager = Manager.objects.filter(id=request.GET.get('userid'), )
    response['manager'] = json.loads(serializers.serialize("json", manager))
    if manager:
        response['msg'] = 'success'
        response['error_num'] = 0
    else:
        response['msg'] = 'none'
        response['error_num'] = 1

    return JsonResponse(response)

@csrf_exempt
def upload_video(request):
    if request.method == 'POST':
        # 提交过来的类型为formdata
        file_obj = request.FILES.get('file')
        size = file_obj.size
        if size > 300*1024*1024: #限制输入大小为300M
            return HttpResponse(json.dumps({'code': 405, 'information': '上传视频或图片大于300M！'}),
                                content_type="application/json")
        print(size)
        print(file_obj.name)
        # 处理视频
        if file_obj.name.split('.')[-1] in ['mp4', 'MP4', 'avi', ]:
            video_url = '/ProcessedData/videos/' + file_obj.name
            # video_name = 'E:/Workspaces/GraduationProject/CrowdCountingSystem/myapp' + video_url
            video_name = 'E:/Workspaces/GraduationProject/CrowdCountingSystem/appfront/src/assets' + video_url
            print(video_name)
            try:
                with open(video_name, 'wb+') as f:
                    f.write(file_obj.read())
                    f.close()
            except Exception as e:
                print(str(e))
                result = {"code": '500', 'information': '文件写入错误！'}
                return HttpResponse(json.dumps(result, ensure_ascii=False))

            # 使用opencv 截取视频文件第一帧
            vc = cv2.VideoCapture(video_name)  # 读入视频文件
            if vc.isOpened():  # 判断是否正常打开
                print('文件正常打开')
                video = Video.objects.filter(video_name=file_obj.name).first()
                if video:
                    video.video_url = video_url
                else:
                    video = Video(video_name= file_obj.name, video_url= video_url)
                video.save()
                result = {"code": '200', "flag": 1, "video_url": video_url, "video_name": file_obj.name}
                return HttpResponse(json.dumps(result, ensure_ascii=False))
            else:
                result = {"code": '500', 'information': '视频无法正常打开！'}
                return HttpResponse(json.dumps(result, ensure_ascii=False))
    result = {'code': 402}
    return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json")

def analyse_video(request):
    response = {}
    video_name = request.GET.get('video_name')
    print(video_name)
    video = Video.objects.filter(video_name=video_name).first()
    print(video)
    video_url = video.video_url
    video_get = 'E:/Workspaces/GraduationProject/CrowdCountingSystem/appfront/src/assets' + video_url

    try:
        # videoAnalyser.video_path = video_get
        # videoAnalyser.new_video_path = 'E:/Workspaces/GraduationProject/CrowdCountingSystem/appfront/src/assets/ProcessedData/results/result.avi'
        # videoAnalyser.main()
        if video_name == 'test.mp4':
            response['result'] = 'new_video4.mp4'
        elif video_name == 'TownCentreXVID.mp4':
            response['result'] = 'new_video1.mp4'
        elif video_name == 'acvis09-5950.mp4':
            response['result'] = 'new_video5.mp4'
        elif video_name == '00011.mp4':
            response['result'] = 'new_video6.mp4'
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        print(e)
        response['msg'] = 'false'
        response['error_num'] = 1

    return JsonResponse(response)

def data_visual(request):
    response = {}
    video_name = request.GET.get('video_name')
    print(video_name)
    try:
        if video_name == 'test.mp4':
            analysisTxt = 'NWPU_HR_Net_video_list.txt'
        elif video_name == 'TownCentreXVID.mp4':
            analysisTxt = 'NWPU_HR_Net_video1_list.txt'
        elif video_name == 'acvis09-5950.mp4':
            analysisTxt = 'NWPU_HR_Net_video_acvis_list.txt'
        elif video_name == '00011.mp4':
            analysisTxt = 'NWPU_HR_Net_video_00011_list.txt'

        file_path = 'E:/Workspaces/GraduationProject/CrowdCountingSystem/myapp/IIM/saved_exp_results/' + analysisTxt

        if video_name == 'acvis09-5950.mp4':
            with open(file_path, 'r') as fp:
                frame = 0  # 每25帧算1秒
                count = 0  # 每一秒进行计数
                dl = timezone.now()
                # dl.strftime("%Y-%m-%d %H:%M:%S")
                date = dl.strftime("%Y-%m-%d %H")
                # print(date)
                # 记录每一条数据
                temp_data = []
                response['data'] = []
                # 生成分秒
                minutes = 0
                seconds = 0
                # 循环读取每一行
                for line in fp.readlines():
                    frame += 1
                    count += int(line.split(' ')[1])
                    if frame == 25:
                        str_record = date + ':' + str(minutes).zfill(2) + ':' + str(seconds).zfill(2)
                        # print(str_record)
                        temp_data.append(str_record)
                        temp_data.append(count // 30)
                        response['data'].append(temp_data)
                        temp_data = []
                        # 获取操作信息
                        # print(count // 30)
                        count = 0
                        frame = 0
                        seconds += 1
                        if seconds == 60:
                            minutes += 1
                            seconds = 0
        else:
            with open(file_path, 'r') as fp:
                frame = 0  # 每30帧算1秒
                count = 0  # 每一秒进行计数
                dl = timezone.now()
                # dl.strftime("%Y-%m-%d %H:%M:%S")
                date = dl.strftime("%Y-%m-%d %H")
                # print(date)
                # 记录每一条数据
                temp_data = []
                response['data'] = []
                # 生成分秒
                minutes = 0
                seconds = 0
                # 循环读取每一行
                for line in fp.readlines():
                    frame += 1
                    count += int(line.split(' ')[1])
                    if frame == 30:
                        str_record = date + ':' + str(minutes).zfill(2) + ':' + str(seconds).zfill(2)
                        # print(str_record)
                        temp_data.append(str_record)
                        temp_data.append(count // 30)
                        response['data'].append(temp_data)
                        temp_data = []
                        # 获取操作信息
                        # print(count // 30)
                        count = 0
                        frame = 0
                        seconds += 1
                        if seconds == 60:
                            minutes += 1
                            seconds = 0

        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        print(e)
        response['msg'] = 'false'
        response['error_num'] = 1

    return JsonResponse(response)