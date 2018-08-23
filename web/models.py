from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


# Create your models here.


class Host(models.Model):
    """主机表"""
    name = models.CharField(max_length=64, unique=True)
    ip_addr = models.GenericIPAddressField(unique=True)
    port = models.SmallIntegerField(default=22)
    idc = models.ForeignKey("IDC")

    def __str__(self):
        return "%s" % self.name


class HostGroup(models.Model):
    """主机组表"""
    name = models.CharField(max_length=64, unique=True)
    host_to_remote_users = models.ManyToManyField("HostToRemoteUser")

    def __str__(self):
        return self.name


class HostToRemoteUser(models.Model):
    """绑定主机和远程用户的对应关系表"""
    host = models.ForeignKey('Host')
    remote_user = models.ForeignKey('RemoteUser')

    class Meta:
        unique_together = ('host', 'remote_user')

    def __str__(self):
        return "%s_%s" % (self.host, self.remote_user)


class RemoteUser(models.Model):
    """远程要管理的主机的账号信息表"""
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=64, blank=True, null=True)
    auth_type_choices = ((0, 'ssh-password'), (1, 'ssh-key'))
    auth_type = models.SmallIntegerField(choices=auth_type_choices, default=0)

    class Meta:
        unique_together = ('auth_type', 'username', 'password')

    def __str__(self):
        return '%s_%s' % (self.username, self.password)


class UserProfileManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            name=name,
        )
        user.is_superuser = True
        user.save(using=self._db)
        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    """跳板机账户表"""
    name = models.CharField(max_length=64, verbose_name='姓名')
    email = models.EmailField(max_length=255, unique=True, verbose_name='emial_address')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    objects = UserProfileManager()

    host_to_remote_users = models.ManyToManyField('HostToRemoteUser', blank=True, null=True)
    host_groups = models.ManyToManyField('HostGroup', blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):
        return self.email


class IDC(models.Model):
    """机房信息表"""
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name


class AuditLog(models.Model):
    """审计日志表"""
    user = models.ForeignKey('UserProfile', verbose_name='跳板机账户',blank=True,null=True)
    host_to_remote_user = models.ForeignKey('HostToRemoteUser',blank=True,null=True)
    log_type_choices = ((0, 'login'), (1, 'cmd'), (2, 'logout'))
    log_type = models.SmallIntegerField(choices=log_type_choices, default=0,blank=True,null=True)
    content = models.CharField(max_length=255,blank=True,null=True)
    date = models.DateTimeField(auto_now_add=True,blank=True,null=True)

    def __str__(self):
        return "%s_%s" % (self.host_to_remote_user, self.content)


class Task(models.Model):
    """批量任务"""
    task_type_choices = (('cmd','批量命令'),('file_transfer','文件传输'))
    task_type = models.CharField(choices=task_type_choices,max_length=64)
    content = models.CharField(max_length=255,verbose_name='任务内容')
    user = models.ForeignKey('UserProfile')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s %s"%(self.task_type,self.content)

class TaskLogDetail(models.Model):
    """存储批量任务执行的结果"""
    task = models.ForeignKey('Task')
    host_to_remote_user = models.ForeignKey('HostToRemoteUser')
    result = models.TextField(verbose_name='任务执行后的结果')
    status_choices = ((0,'正在初始化'),(1,'成功'),(2,'失败'),(3,'超时'))
    status = models.SmallIntegerField(choices=status_choices,default=0)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s %s"%(self.task,self.host_to_remote_user)
