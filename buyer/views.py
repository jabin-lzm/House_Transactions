from django.shortcuts import render, redirect
from django.views import View

from buyer.forms import LoginForm, RegisterForm
from buyer.models import User, Log
import hashlib
from django.contrib import messages


class IndexBuyer(View):
    """ 主页 """
    def get(self, request):
        return redirect('/login_buyer/')


class LoginBuyer(View):
    """ 买家登入 """
    def get(self, request):
        if request.session.get('is_login', None):
            return redirect('/home_buyer/')
        login_form = LoginForm()
        return render(request, 'login_buyer.html', locals())

    def post(self, request):
        login_form = LoginForm(request.POST)
        message = '请检查填写的内容！'
        if login_form.is_valid():
            phone = login_form.cleaned_data['phone']
            password = login_form.cleaned_data['password']
            user = User.objects.filter(phone=phone).first()
            print(hashcode(password))
            print(user.password)
            if user.password == hashcode(password):
                request.session['is_login'] = True
                request.session['phone'] = user.phone
                Log.objects.create(user_id=phone, action='登入')
                return redirect('/home_buyer/')
            else:
                message = '手机号或密码错误，也许没有注册！'
        return render(request, 'login_buyer.html', locals())


class LogoutBuyer(View):
    """
    登出
    """
    def get(self, request):
        if request.session.get('is_login', None):
            Log.objects.create(user_id=request.session['phone'], action='登出')
            request.session.flush()
            messages.success(request, '登出成功！')
        return redirect('/login_buyer/')


class RegisterBuyer(View):
    """ 买家注册 """

    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'register_buyer.html', locals())

    def post(self, request):
        register_form = RegisterForm(request.POST)
        message = '请检查填写的内容！'
        if register_form.is_valid():
            name = register_form.cleaned_data['name']
            phone = register_form.cleaned_data['phone']
            id_card = register_form.cleaned_data['id_card']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            if password1 == password2:
                same_id_users = User.objects.filter(phone=phone)
                if same_id_users:
                    message = '该用户被注册！'
                else:
                    User.objects.create(name=name, phone=phone, id_card=id_card, password=hashcode(password2) )
                    Log.objects.create(user_id=phone, action='注册')
                    messages.success(request, '注册成功！')
                    return redirect('/login_buyer/')
            else:
                message = '两次输入的密码不一致！'
        return render(request, 'register_buyer.html', locals())


class HomeBuyer(View):
    """
    个人中心
    """
    def get(self, request):
        if not request.session.get('is_login', None):
            messages.error(request, '请先登录！')
            return redirect('/login/')


def hashcode(s, salt='17373252'):
    s += salt
    h = hashlib.sha256()
    h.update(s.encode())
    return h.hexdigest()