# -*- coding:utf-8 -*-
# @Time : 2018/8/20 13:19
import sys ,os


if __name__ == '__main__':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Springboard.settings")
    import django
    django.setup()

    from backend import main
    interactive_obj = main.ArgvHandle(sys.argv)
    interactive_obj.call()