# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-08-22 08:47
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('name', models.CharField(max_length=64, verbose_name='姓名')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='emial_address')),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AuditLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('log_type', models.SmallIntegerField(blank=True, choices=[(0, 'login'), (1, 'cmd'), (2, 'logout')], default=0, null=True)),
                ('content', models.CharField(blank=True, max_length=255, null=True)),
                ('date', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Host',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True)),
                ('ip_addr', models.GenericIPAddressField(unique=True)),
                ('port', models.SmallIntegerField(default=22)),
            ],
        ),
        migrations.CreateModel(
            name='HostGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='HostToRemoteUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('host', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.Host')),
            ],
        ),
        migrations.CreateModel(
            name='IDC',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='RemoteUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=32)),
                ('password', models.CharField(blank=True, max_length=64, null=True)),
                ('auth_type', models.SmallIntegerField(choices=[(0, 'ssh-password'), (1, 'ssh-key')], default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_type', models.CharField(choices=[('cmd', '批量命令'), ('file_transfer', '文件传输')], max_length=64)),
                ('content', models.CharField(max_length=255, verbose_name='任务内容')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TaskLogDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('result', models.TextField(verbose_name='任务执行后的结果')),
                ('status', models.SmallIntegerField(choices=[(0, '正在初始化'), (1, '成功'), (2, '失败'), (3, '超时')], default=0)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('host_to_remote_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.HostToRemoteUser')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.Task')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='remoteuser',
            unique_together=set([('auth_type', 'username', 'password')]),
        ),
        migrations.AddField(
            model_name='hosttoremoteuser',
            name='remote_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.RemoteUser'),
        ),
        migrations.AddField(
            model_name='hostgroup',
            name='host_to_remote_users',
            field=models.ManyToManyField(to='web.HostToRemoteUser'),
        ),
        migrations.AddField(
            model_name='host',
            name='idc',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.IDC'),
        ),
        migrations.AddField(
            model_name='auditlog',
            name='host_to_remote_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='web.HostToRemoteUser'),
        ),
        migrations.AddField(
            model_name='auditlog',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='跳板机账户'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='host_groups',
            field=models.ManyToManyField(blank=True, null=True, to='web.HostGroup'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='host_to_remote_users',
            field=models.ManyToManyField(blank=True, null=True, to='web.HostToRemoteUser'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
        migrations.AlterUniqueTogether(
            name='hosttoremoteuser',
            unique_together=set([('host', 'remote_user')]),
        ),
    ]
