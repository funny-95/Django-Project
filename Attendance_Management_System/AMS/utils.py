# -*-coding:utf-8 -*-

def permission_check(user):
    if user.is_authenticated():
        return user.myuser.permission == 1
    else:
        return False

def permission_check1(user):
    if user.is_authenticated():
        return user.myuser.permission == 0
    else:
        return False
