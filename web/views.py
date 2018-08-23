import json

from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

# Create your views here.
from backend.multitask import MultiTaskManger
from web import models


def dashbord(request):
    return render(request,'index.html')

def acc_login(request):
    err_msg=''
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username,password=password)
        if user:
            login(request,user)
            return redirect('/')
        else:
            err_msg = '密码或用户名错误！'

    return render(request,'login.html',{'err_msg':err_msg})

@login_required
def web_ssh(request):
    return render(request,'web_ssh.html')

@login_required
def host_mgr(request):
    return render(request,'host_mgr.html')

@login_required
def file_transfer(request):
    return render(request,'file_transfer.html')

@login_required
def batch_task_mgr(request):
    task_data = json.loads(request.POST.get('task_data'))
    task_obj = MultiTaskManger(request)
    response = {
        'task_id':task_obj.task_obj.id,
        "selected_hosts":list(task_obj.task_obj.tasklogdetail_set.all().values('id',
                    'host_to_remote_user__host__ip_addr',
                   'host_to_remote_user__host__name',
                   'host_to_remote_user__remote_user__username',
                                                                               ))
    }
    return HttpResponse(json.dumps(response))

def task_result(request):
    task_id = request.GET['task_id']
    sub_tasklog_objs = models.TaskLogDetail.objects.filter(task_id=task_id)
    log_data = list(sub_tasklog_objs.values('id','status','result'))
    return HttpResponse(json.dumps(log_data))
