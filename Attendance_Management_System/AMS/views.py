# -*-coding:utf-8-*-
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.models import User
from django.contrib import auth
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from AMS.models import MyUser,File,Qiandao,Qingjia,Salary,Base_salary
from django.core.urlresolvers import reverse
from AMS.utils import permission_check,permission_check1
import time
from datetime import date
import datetime
from django.db.models import Q


def index(request):
    user = request.user if request.user.is_authenticated() else None
    content = {
        'active_menu': 'homepage',
        'user': user,
    }
    return render(request, 'management/index.html', content)


def signup(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('homepage'))
    state = None
    if request.method == 'POST':
        position = request.POST.get('position', '')
        depth = request.POST.get('depth','')
        password = request.POST.get('password', '')
        repeat_password = request.POST.get('repeat_password', '')
        gonghao = request.POST.get('gonghao', '')
        if password == '' or repeat_password == '':
            state = 'empty'
        elif password != repeat_password:
            state = 'repeat_error'
        else:
            username = request.POST.get('username', '')
            if User.objects.filter(username=username):
                state = 'user_exist'
            else:
                new_user = User.objects.create_user(username=username, password=password,email=request.POST.get('email', ''))
                new_user.save()
                new_my_user = MyUser(user=new_user, depth=depth,permission=0,position=position,email=request.POST.get('email', ''),gonghao=gonghao,password = password,username=username)
                new_my_user.save()
                state = 'success'
    content = {
        'active_menu': 'homepage',
        'state': state,
        'user': None,
    }
    return render(request, 'management/signup.html', content)


def login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('homepage'))
    state = None
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return HttpResponseRedirect(reverse('homepage'))
        else:
            state = 'not_exist_or_password_error'
    content = {
        'active_menu': 'homepage',
        'state': state,
        'user': None
    }
    return render(request, 'management/login.html', content)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('homepage'))

def qiandao(request):
    user = request.user if request.user.is_authenticated() else None
    renyuan_list = MyUser.objects.all()
    state=None
    qiandao_time=None
    number=user.myuser.gonghao
    r_l=MyUser.objects.get(gonghao=number)
    local_time = time.strftime("%Y-%m-%d", time.localtime(time.time()))
    qiandao_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
    if request.method == 'POST':
        if Qiandao.objects.filter(Q(gonghao=r_l.gonghao),Q(date = local_time)).count() is 0:
            qiandao_one = Qiandao(username=r_l.username,gonghao=r_l.gonghao,date=local_time,first_qiandao=qiandao_time,second_qiandao='')
            qiandao_one.save()
            state = 'shang_qiandao'
        elif Qiandao.objects.get(Q(gonghao=r_l.gonghao),Q(date = local_time)).first_qiandao!='' and Qiandao.objects.get(Q(username=r_l.username),Q(date = local_time)).second_qiandao!='':
            state = 'qiandao_over'
        elif Qiandao.objects.get(Q(gonghao=r_l.gonghao),Q(date = local_time)).first_qiandao!='':
            qiandao_two=Qiandao.objects.get(Q(username=r_l.username),Q(date = local_time))
            qiandao_two.second_qiandao=qiandao_time
            qiandao_two.save()
            state = 'xia_qiandao'
        else:
            state='error'

    content = {
        'active_menu': 'homepage',
        'user': user,
        'renyuan_list':renyuan_list,
        'qiandao_time':qiandao_time,
        'state':state
    }
    return render(request, 'management/qiandao.html',content)

@login_required
def set_password(request):
    user = request.user
    state = None
    if request.method == 'POST':
        old_password = request.POST.get('old_password', '')
        new_password = request.POST.get('new_password', '')
        repeat_password = request.POST.get('repeat_password', '')
        if user.check_password(old_password):
            if not new_password:
                state = 'empty'
            elif new_password != repeat_password:
                state = 'repeat_error'
            else:
                user.set_password(new_password)
                user.save()
                state = 'success'
        else:
            state = 'password_error'
    content = {
        'user': user,
        'active_menu': 'homepage',
        'state': state,
    }
    return render(request, 'management/set_password.html', content)

@user_passes_test(permission_check1)
def view_file_list(request):
    user = request.user if request.user.is_authenticated() else None
    query_details = request.GET.get('details', 'all')
    if (not query_details) or File.objects.filter(details=query_details).count() is 0:
        query_details = 'all'
        file_list = File.objects.all()
    else:
        file_list = File.objects.filter(category=query_details)

    if request.method == 'POST':
        keyword = request.POST.get('keyword', '')
        file_list = File.objects.filter(title__contains=keyword)
        query_details = 'all'

    paginator = Paginator(file_list, 5)
    page = request.GET.get('page')
    try:
        file_list = paginator.page(page)
    except PageNotAnInteger:
        file_list = paginator.page(1)
    except EmptyPage:
        file_list = paginator.page(paginator.num_pages)
    content = {
        'user': user,
        'active_menu': 'view_details',
        'query_details': query_details,
        'file_list': file_list,
    }
    return render(request, 'management/view_file_list.html', content)

@user_passes_test(permission_check1)
def detail(request):
    user = request.user if request.user.is_authenticated() else None
    file_id = request.GET.get('id', '')
    if file_id == '':
        return HttpResponseRedirect(reverse('view_file_list'))
    try:
        file = File.objects.get(pk=file_id)
    except File.DoesNotExist:
        return HttpResponseRedirect(reverse('view_file_list'))
    if request.method == 'POST':
        return HttpResponseRedirect(reverse('view_file_list'))
    content = {
        'user': user,
        'active_menu': 'view_book',
        'file': file,
    }
    return render(request, 'management/detail.html', content)

@user_passes_test(permission_check)
def user_manage(request):
    return render(request, 'management/user_manage.html')

@user_passes_test(permission_check)
def add_user(request):
    user = request.user if request.user.is_authenticated() else None
    state = None
    if request.method == 'POST':
        username = request.POST.get('username','')
        position = request.POST.get('position','')
        depth = request.POST.get('depth','')
        gonghao = request.POST.get('gonghao','')
        password= request.POST.get('password','')
        email = request.POST.get('email','')
        if username=='' or depth=='' or gonghao=='' or position=='' or password=='':
            state = 'empty'
        else:
            if User.objects.filter(username=username):
                state = 'user_exist'
            else:
                new_user = User.objects.create_user(username=username, password=password,email=request.POST.get('email', ''))
                new_user.save()
                new_my_user = MyUser(user=new_user, depth=depth,permission=0,position=position,email=request.POST.get('email', ''),gonghao=gonghao,password = password,username=username)
                new_my_user.save()
                state = 'success'
    content ={
        'user':user,
        'active_menu':'user_manage',
        'state':state
    }
    return render(request, 'management/add_user.html',content)

@user_passes_test(permission_check)
def modify_user(request):
    user = request.user if request.user.is_authenticated() else None
    renyuan_list = MyUser.objects.all()
    name = ''
    depth = ''
    state = None
    change_infomation = None
    renyuan_old = None
    renyuan1=None
    need=None
    if request.method == 'POST':
        check_box_list = request.POST.getlist('check_box_list')
        if request.POST.has_key('quanxian'):
            if len(check_box_list) == 0:
                state = 'error'
            else:
                for one_check in check_box_list:
                    renyuan_old = MyUser.objects.get(gonghao=one_check)
                    if renyuan_old.username == user.myuser.username:
                        state = 'youself'
                    else:
                        if renyuan_old.permission ==1:
                            renyuan_old.permission=0
                        else:
                            renyuan_old.permission=1
                        renyuan_old.save()
                        state = 'quanxian_success'
        elif request.POST.has_key('modify'):
            if len(check_box_list)>1:
                state = 'too_many'
            else:
                if len(check_box_list) == 0:
                    state = 'error'
                else:
                    change_infomation = 'change_infomation'
                    need='need'
                    renyuan1 = MyUser.objects.get(gonghao=check_box_list[0])
        elif request.POST.has_key('save'):
            renyuan1 = MyUser.objects.get(gonghao=request.POST.get('gonghao', ''))
            renyuan1.username=request.POST.get('username', '')
            renyuan1.depth = request.POST.get('depth', '')
            renyuan1.password =request.POST.get('password', '')
            renyuan1.gonghao = request.POST.get('gonghao', '')
            renyuan1.position=request.POST.get('position', '')
            renyuan1.email=request.POST.get('email', '')
            if renyuan1.username=='' or renyuan1.depth=='' or renyuan1.password=='' or renyuan1.gonghao=='' or renyuan1.position=='' or renyuan1.email=='':
                state='empty'
            else:
                renyuan1.save()
                state = 'success'

    content ={
        'renyuan_list':renyuan_list,
        'user':user,
        'need':need,
        'renyuan':renyuan1,
        'state':state,
        'select_name':name,
        'select_depth':depth,
        'change_infomation':change_infomation,
        'active_menu':'user_manage',
        'renyuan_old':renyuan_old
    }
    return render(request, 'management/modify_user.html',content)

@user_passes_test(permission_check)
def delete_user(request):
    user = request.user if request.user.is_authenticated() else None
    renyuan_list = MyUser.objects.all()
    name = ''
    depth = ''
    state = None
    if request.method == 'POST':
        check_box_list = request.POST.getlist('check_box_list')
        if len(check_box_list) == 0:
            state = 'error'
        else:
            for one_check in check_box_list:
                renyuan_old = MyUser.objects.get(gonghao=one_check)
                if renyuan_old.username == 'admin':
                    state = 'admin_error'
                else:
                    MyUser.objects.get(gonghao=one_check).delete()
                    state = 'success'

    content = {
        'renyuan_list': renyuan_list,
        'user': user,
        'state': state,
        'select_name': name,
        'select_depth': depth,
        'active_menu': 'user_manage'
    }
    return render(request, 'management/delete_user.html',content)

@user_passes_test(permission_check)
def qingjia_manage(request):
    return render(request,'management/qingjia_manage.html')

@user_passes_test(permission_check)
def shenpi_qingjia(request):
    user = request.user if request.user.is_authenticated() else None
    state = None
    if user.myuser.username=='admin':
        qingjia_list = Qingjia.objects.all()
        person_list = MyUser.objects.all()
    else:
        qingjia_list = Qingjia.objects.filter(approve_person = user.myuser.username)
        person_list = MyUser.objects.all()
    if request.method == 'POST':
        a_qingjia = Qingjia.objects.get(id=int(request.POST.get('modify', '')))
        approve_result = request.POST.get('result', '')
        a_qingjia.approve_result = approve_result
        a_qingjia.save()
    paginator = Paginator(qingjia_list, 5)
    page = request.GET.get('page')
    try:
        qingjia_list = paginator.page(page)
    except PageNotAnInteger:
        qingjia_list = paginator.page(1)
    except EmptyPage:
        qingjia_list = paginator.page(paginator.num_pages)
    content = {
        'state':state,
        'user': user,
        'qingjia_list':qingjia_list,
        'active_menu': 'qingjia_manage',
        'person_list':person_list
    }
    return render(request,'management/shenpi_qingjia.html',content)

def write_note(request):
    user = request.user if request.user.is_authenticated() else None
    state = None
    if request.method == 'POST':
        from_date = request.POST.get('from_date','')
        to_date = request.POST.get('to_date','')
        reason = request.POST.get('reason','')
        if from_date == '' or to_date == '' or reason == '':
            state = 'empty'
        else:
            approve_person=''
            gonghao = user.myuser.gonghao
            approve_result = u'待审批'
            approve_person_depth = MyUser.objects.get(gonghao = user.myuser.gonghao).depth
            if MyUser.objects.get(Q(depth = approve_person_depth),Q(position = u'经理')):
                approve_person = MyUser.objects.get(Q(depth = approve_person_depth),Q(position = u'经理')).username
            new_qingjia = Qingjia(from_date=from_date, to_date=to_date, gonghao=gonghao, cause=reason, approve_result=approve_result, approve_person=approve_person)
            new_qingjia.save()
            state = 'success'
    content = {
        'state':state,
        'user': user,
        'active_menu': 'qingjia_manage',
    }
    return render(request,'management/write_note.html',content)

def view_note(request):
    user = request.user if request.user.is_authenticated() else None
    state = None
    one_qingjia = None
    if Qingjia.objects.filter(gonghao = user.myuser.gonghao).count() is 0:
        print
        qingjia_list = Qingjia.objects.all()
    else:
        qingjia_list = Qingjia.objects.filter(gonghao = user.myuser.gonghao)

    if request.method == 'POST':
        if request.POST.has_key('modify'):
            qingjia_id = request.POST.get('select','')
            if Qingjia.objects.get(id = qingjia_id).approve_result != u'待审批':
                state = 'approve'
            else:
                state = 'modify'
                one_qingjia =Qingjia.objects.get(id=qingjia_id)
        elif request.POST.has_key('back'):
            #保存修改数据
            id = request.POST.get('hidden_id','')
            now_date = date.today()
            from_date = request.POST.get('start_time','')
            to_date = request.POST.get('to_time','')
            cause = request.POST.get('cause_1','')
            qj=Qingjia.objects.get(id=id)
            qj.now_date = now_date
            qj.from_date = from_date
            qj.to_date = to_date
            qj.cause = cause
            qj.save()

        else:
            keyword = request.POST.get('keyword', '')
            qingjia_list = Qingjia.objects.filter(now_date__contains=keyword)

    paginator = Paginator(qingjia_list, 5)
    page = request.GET.get('page')
    try:
        qingjia_list = paginator.page(page)
    except PageNotAnInteger:
        qingjia_list = paginator.page(1)
    except EmptyPage:
        qingjia_list = paginator.page(paginator.num_pages)
    content = {
        'state':state,
        'user': user,
        'active_menu': 'view_details',
        'qingjia_list': qingjia_list,
        'one_qingjia':one_qingjia
    }
    return render(request,'management/view_note.html',content)


@user_passes_test(permission_check)
def salary_manage(request):
    return render(request, 'management/salary_manage.html')

@user_passes_test(permission_check)
def base_salary(request):
    user = request.user if request.user.is_authenticated() else None
    state = None
    p=None
    state1=None
    salary_list = Salary.objects.values('depth','position','base_salary','jiaban','queqing','qingjia').distinct()
    for a_salary in Salary.objects.all():
        if not Base_salary.objects.filter(depth=a_salary.depth).filter(position = a_salary.position):
            a=Base_salary(depth=a_salary.depth,position=a_salary.position,base_salary=a_salary.base_salary,jiaban=a_salary.jiaban,queqing=a_salary.queqing,qingjia=a_salary.qingjia)
            a.save()
    base_salary = Base_salary.objects.all()
    if request.method == 'POST':
        if request.POST.has_key('add'):
            state = 'add'
        elif request.POST.has_key('save'):
            depth = request.POST.get('depth','')
            position = request.POST.get('position','')
            base_price = request.POST.get('base_price','')
            jiaban = request.POST.get('jiaban', '')
            queqing = request.POST.get('queqing', '')
            qingjia =request.POST.get('qingjia', '')
            if depth=='' or position == '' or base_price =='':
                state = 'empty'
            else:
                if MyUser.objects.filter(Q(depth = depth),Q(position=position)):
                    for one_person in MyUser.objects.filter(Q(depth = depth),Q(position=position)):
                        for i in ['3','4','5']:
                            salary = Salary(name = one_person.username, gonghao = one_person.gonghao, depth = depth , position = position,base_salary = base_price,jiaban = jiaban,queqing=queqing,qingjia=qingjia,mouth_time=i)
                            salary.save()
        elif  request.POST.has_key('modify'):
            state = 'modify'
            id = request.POST.get('select_id1','')
            p = Base_salary.objects.get(id=id)
        elif request.POST.has_key('modify_save'):
            p = Base_salary.objects.get(id=request.POST.get('modify_id',''))
            p_depth = p.depth
            p_position = p.position
            p.base_salary = request.POST.get('change_price','')
            p.jiaban = request.POST.get('jiaban','')
            p.queqing = request.POST.get('queqing', '')
            p.qingjia =request.POST.get('qingjia', '')
            p.save()
            for one_p in MyUser.objects.filter(Q(depth=p_depth), Q(position=p_position)):
                ss=Salary.objects.filter(gonghao = one_p.gonghao)
                for s in ss:
                    s.base_salary = request.POST.get('change_price', '')
                    s.jiaban = request.POST.get('jiaban', '')
                    s.queqing = request.POST.get('queqing', '')
                    s.qingjia =request.POST.get('qingjia', '')
                    if request.POST.get('change_price','')=='':
                        state1='empty'
                    else:
                        state1='modify_success'
                        s.save()

    paginator = Paginator(salary_list, 5)
    page = request.GET.get('page')
    try:
        salary_list = paginator.page(page)
    except PageNotAnInteger:
        salary_list = paginator.page(1)
    except EmptyPage:
        salary_list = paginator.page(paginator.num_pages)
    content = {
        'state':state,
        'state1':state1,
        'user': user,
        'salary_list':salary_list,
        'active_menu': 'salary_manage',
        'p':p,
        'base_salary':base_salary,
    }
    return render(request, 'management/base_salary.html',content)

@user_passes_test(permission_check)
def salary_detail(request):
    user = request.user if request.user.is_authenticated() else None
    state = None
    one_salary = None
    all_user = MyUser.objects.all()
    salary_list = Salary.objects.all().order_by('mouth_time')
    for a_user in all_user:
        if a_user.username == 'admin':
            continue
        days = Qiandao.objects.filter(gonghao = a_user.gonghao)
        qingjias = Qingjia.objects.filter(gonghao = a_user.gonghao)
        all_jiaban = 0
        all_queqing = 0
        all_qingjia = 0
        mouth_list = set([])
        for one_day in days:
            mouth_list.add(one_day.first_qiandao.split('-')[1])
        for mouth in mouth_list:
            for one_day in days:
                if mouth == one_day.first_qiandao.split('-')[1]:
                    weekdend = datetime.datetime.strptime(one_day.first_qiandao,'%Y-%m-%d %H:%M:%S').weekday()
                    if weekdend == 6 or weekdend == 0:#加班
                        start_time = time.mktime(time.strptime(one_day.first_qiandao,'%Y-%m-%d %H:%M:%S'))
                        end_time = time.mktime(time.strptime(one_day.second_qiandao,'%Y-%m-%d %H:%M:%S'))
                        one_day_jiaban_time = (end_time-start_time)/60/60
                        all_jiaban+=one_day_jiaban_time
                    else:#不加班
                        start_time = time.mktime(time.strptime(one_day.first_qiandao,'%Y-%m-%d %H:%M:%S'))
                        end_time = time.mktime(time.strptime(one_day.second_qiandao,'%Y-%m-%d %H:%M:%S'))
                        one_day_daka_time = (end_time-start_time)/60/60
                        if one_day_daka_time==9:#正常上班
                            pass
                        elif one_day_daka_time>9:
                            all_jiaban+=one_day_daka_time-9
                        else:
                            all_queqing+=9-one_day_daka_time
            for one_qingjia in qingjias:
                if one_qingjia.approve_result == u'通过':
                    from_time = time.mktime(time.strptime(one_qingjia.from_date, '%Y-%m-%d %H:%M'))
                    to_time = time.mktime(time.strptime(one_qingjia.to_date, '%Y-%m-%d %H:%M'))
                    one_qingjia_time = (to_time - from_time) / 60 / 60
                    all_qingjia+=one_qingjia_time
            if all_jiaban>all_qingjia:
                tiaoxiu = all_qingjia
            else:
                tiaoxiu = all_jiaban
                all_qingjia = all_qingjia-all_jiaban
            if Salary.objects.filter(Q(gonghao = a_user.gonghao),Q(mouth_time = int(mouth))):
                modify_s = Salary.objects.get(Q(gonghao = a_user.gonghao),Q(mouth_time = int(mouth)))
                modify_s.jiaban_hour = all_jiaban
                modify_s.queqing_hour = all_queqing
                modify_s.tiaoxiu = tiaoxiu
                if mouth.startswith('0'):
                    mouth = mouth.replace('0','')
                modify_s.mouth_time = mouth
                modify_s.total_salary = float(modify_s.base_salary)+float(all_jiaban)*float(modify_s.jiaban)-float(all_queqing)*float(modify_s.queqing)+(float(modify_s.jiangjin) if modify_s.jiangjin!='' else 0.00)
                modify_s.save()

    if request.method == 'POST':
        if request.POST.has_key('back'):
            return render(request,'management/salary_manage.html',{"user": user})
        elif request.POST.has_key('modify'):
            salary_id = request.POST.get('select','')
            state = 'modify'
            one_salary = Salary.objects.get(id=salary_id)
        elif request.POST.has_key('modify_save'):
            a_salary = Salary.objects.get(id=request.POST.get('modify_id',''))
            a_salary.ti_cheng = request.POST.get('jixiao','')
            a_salary.jiangjin = request.POST.get('jiangjin','')
            a_salary.base_salary = request.POST.get('change_price','')
            a_salary.save()
        elif request.POST.has_key('select'):
            search_mouth = request.POST.get('search_mouth','')
            search_gonghao = request.POST.get('search_gonghao','')
            if search_mouth != '' and search_gonghao != '':
                search_mouth = search_mouth.replace('2017-0','')
                salary_list = Salary.objects.filter(mouth_time=search_mouth).filter(gonghao = search_gonghao)
            elif search_mouth == '' and search_gonghao != '':
                salary_list = Salary.objects.filter(gonghao = search_gonghao)
            elif search_mouth != '' and search_gonghao == '':
                search_mouth = search_mouth.replace('2017-0','')
                salary_list = Salary.objects.filter(mouth_time=search_mouth)
    paginator = Paginator(salary_list, 5)
    page = request.GET.get('page')
    try:
        salary_list = paginator.page(page)
    except PageNotAnInteger:
        salary_list = paginator.page(1)
    except EmptyPage:
        salary_list = paginator.page(paginator.num_pages)
    content = {
        'user': user,
        'active_menu': 'salary_manage',
        'salary_list':salary_list,
        'one_salary':one_salary,
        'state':state
    }
    return render(request, 'management/salary_detail.html',content)

@user_passes_test(permission_check)
def comment_manage(request):
    return render(request, 'management/comment_manage.html')

@user_passes_test(permission_check)
def add_comment(request):
    user = request.user if request.user.is_authenticated() else None
    state = None
    if request.method == 'POST':
        title = request.POST.get('title','')
        content = request.POST.get('details','')
        public_time = time.strftime("%Y-%m-%d", time.localtime(time.time()))
        if title=='' or content=='':
            state = 'empty'
        else:
            new_file=File(title=title,details=content,public_time=public_time)
            new_file.save()
            state='success'
    content ={
        'user':user,
        'active_menu':'comment_manage',
        'state':state
    }
    return render(request, 'management/add_comment.html',content)

@user_passes_test(permission_check)
def modify_comment(request):
    user = request.user if request.user.is_authenticated() else None
    file_list = File.objects.all()
    paginator = Paginator(file_list, 5)
    page = request.GET.get('page')
    try:
        file_list = paginator.page(page)
    except PageNotAnInteger:
        file_list = paginator.page(1)
    except EmptyPage:
        file_list = paginator.page(paginator.num_pages)
    state = None
    need = None
    file = None
    if request.method == 'POST':
        if request.POST.has_key('change'):
            need = 'modify'
            file_id = request.POST.get('check_radio','')
            file = File.objects.get(pk=file_id)
        elif request.POST.has_key('select'):
            state= 'show'
            file_id = request.POST.get('check_radio', '')
            file = File.objects.get(pk=file_id)
        else:
            keyword = request.POST.get('keyword', '')
            if keyword!='':
                file_list = File.objects.filter(title__contains=keyword)
            else:
                file=File.objects.get(pk=request.POST.get('file_need_id',''))
                file.title=request.POST.get('title','')
                file.details = request.POST.get('details', '')
                if file.title=='' or file.details=='':
                    state='empty'
                else:
                    file.save()
                    state = 'success'

    content ={
        'file_list':file_list,
        'file':file,
        'user':user,
        'state':state,
        'need':need,
        'active_menu':'user_manage'
    }
    return render(request, 'management/modify_comment.html',content)

@user_passes_test(permission_check)
def delete_comment(request):
    user = request.user if request.user.is_authenticated() else None
    file_list = File.objects.all()
    paginator = Paginator(file_list, 5)
    page = request.GET.get('page')
    try:
        file_list = paginator.page(page)
    except PageNotAnInteger:
        file_list = paginator.page(1)
    except EmptyPage:
        file_list = paginator.page(paginator.num_pages)
    state = None
    need = None
    file = None
    if request.method == 'POST':
        if request.POST.has_key('delete'):
            file_id = request.POST.get('check_radio','')
            if file_id=='':
                state = 'error'
            else:
                File.objects.get(pk=file_id).delete()
                state = 'delete_success'
        else:
            keyword = request.POST.get('keyword', '')
            if keyword != '':
                file_list = File.objects.filter(title__contains=keyword)

    content = {
        'file_list': file_list,
        'file': file,
        'user': user,
        'state': state,
        'need': need,
        'active_menu': 'user_manage'
    }
    return render(request, 'management/delete_comment.html',content)