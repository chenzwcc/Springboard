# -*- coding:utf-8 -*-
# @Time : 2018/8/20 11:08
from django.contrib.auth import authenticate
from web import models

from backend.paramiko_ssh import ssh_connect

class SshHandler(object):
    """跳板机交互脚本"""
    def __init__(self,argv_handler_instance):
        self.argv_handler_instance = argv_handler_instance
        self.models = models

    def auth(self):
        """登录认证程序"""
        count = 0
        while count <3:
            username = input("请输入跳板机账号:").strip()
            password = input("请输入对应密码:").strip()
            user = authenticate(username=username,password=password)
            if user:
                self.user= user
                return True
            else:
                count +=1

    def interactive(self):
        """启动用户交互脚本"""
        if self.auth():
            print("以下为本用户可操作的所有主机组及对应主机")
            while True:
                host_group_list = self.user.host_groups.all()
                for index,host_group in enumerate(host_group_list):

                    print("%s.\t%s[%s]"%(index,host_group.name,host_group.host_to_remote_users.count()))
                print("z.\t未分组主机[%s]" % (self.user.host_to_remote_users.count()))
                choice = input("请选择要操作的主机组:").strip()
                if choice.isdigit():
                    choice=int(choice)
                    selected_host_group = host_group_list[choice]
                elif choice =='z':
                    selected_host_group = self.user
                while True:
                    for index,host_to_user in enumerate(selected_host_group.host_to_remote_users.all()):
                        print("%s.\t%s"%(index,host_to_user))
                    choice = input("请选择要操作的主机:").strip()
                    if choice.isdigit():
                        choice = int(choice)
                        selected_host_to_user_obj = selected_host_group.host_to_remote_users.all()[choice]
                        print('going to logon %s' %selected_host_to_user_obj)
                        ssh_connect(self,selected_host_to_user_obj)
                    if choice == 'b':
                        break