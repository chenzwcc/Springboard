# -*- coding:utf-8 -*-
# @Time : 2018/8/21 9:21

import paramiko

transport = paramiko.Transport(('192.168.228.130',22))
transport.connect(username='chenzwcc',password='chenzwcc')
ssh = paramiko.SSHClient()
ssh._transport = transport
stdin,stdout,stderr = ssh.exec_command('ifconfig')
print(stdout.read().decode('utf8'))
transport.close()



557
<!--<ul class="collapse in">-->
											<!--<li><a href="{% url 'batch_cmd' %}">批量命令</a></li>-->
											<!--<li class=""><a href="{% url 'file_transfer' %}">批量文件传送</a></li>-->

										<!--</ul>-->