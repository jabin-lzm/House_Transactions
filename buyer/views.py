from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from buyer.forms import LoginForm, RegisterForm, SearchForm
from buyer.models import User, Log, Message

from seller.models import House, Area
from seller.models import Message as M
from seller.models import User as U

import hashlib
from django.contrib import messages
import requests
from django.db.models import Q


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
            password = login_form.cleaned_data.get('password')
            user = User.objects.filter(phone=phone).first()
            print(user)

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
                    User.objects.create(name=name, phone=phone, id_card=id_card, password=hashcode(password2))
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
            return redirect('/login_buyer/')

        # 获取用户ip位置 27.221.64.1,山东济南的ip地址
        # client_ip, _ = get_client_ip(request)
        client_ip = '27.221.64.1'

        # 请求高德API
        url = 'https://restapi.amap.com/v3/ip'
        params = {
            'ip': client_ip,
            'output': 'json',
            'key': '3de19d6e7460b268e5c9568094c8674b'
        }
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            result = response.json()
            if result['status'] == '1':
                # adcode = result['adcode']  # 获取城市编码
                province = result['province']  # 获取省份
                city = result['city']  # 获取城市
                # district = result['district']  # 获取区县
            else:
                messages.error(request, '无法获取您当前的位置，请手动到搜索页面查找')
                return redirect('/home_buyer/')
        else:
            messages.error(request, '无法获取您当前的位置，请手动到搜索页面查找')
            return redirect('/home_buyer/')

        address = f"{province}{city}"

        # 使用省份和城市匹配房源
        houses = []
        areas = Area.objects.filter(name=address).prefetch_related('house_set')

        for area in areas:
            houses.extend(area.house_set.all())

        context = {'houses': houses, 'address': address}

        return render(request, 'home_buyer.html', context=context)


class BuyerHouseDetail(View):
    def get(self, request, house_id):
        if not request.session.get('is_login', None):
            messages.error(request, '请先登录！')
            return redirect('/login_buyer/')

        house = get_object_or_404(House, id=house_id)

        return render(request, 'buyer_house_detail.html', locals())


class SearchView(View):
    def get(self, request):
        if not request.session.get('is_login', None):
            messages.error(request, '请先登录！')
            return redirect('/login_buyer/')

        search_form = SearchForm(request.GET)
        if search_form.is_valid():
            keyword = search_form.cleaned_data['keyword']
            # 根据关键词进行搜索，可以使用Q对象来实现多条件查询
            houses = House.objects.filter(Q(area__name__contains=keyword) | Q(title__icontains=keyword))

        return render(request, 'search.html', locals())


class BuyerMessages(View):
    # 展示消息
    def get(self, request):
        if not request.session.get('is_login', None):
            messages.error(request, '请先登录！')
            return redirect('/login_buyer/')

        # buyer = User.objects.filter(phone=request.session['phone']).first()
        message_list = M.objects.filter(receiver_id=request.session['phone'])
        print(message_list)

        return render(request, 'messages_buyer.html', {'messages': message_list})


class BuyerSendMessage(View):
    """ 发送消息 """
    def get(self, request):
        if not request.session.get('is_login', None):
            messages.error(request, '请先登录！')
            return redirect('/login_buyer/')

        return render(request, 'buyer_send_message.html', locals())

    def post(self, request):
        if not request.session.get('is_login', None):
            messages.error(request, '请先登录！')
            return redirect('/login_buyer/')

        phone_buyer = request.POST.get('phone')
        content_buyer = request.POST.get('content')

        sender = User.objects.filter(phone=request.session['phone']).first()
        receiver = U.objects.filter(phone=phone_buyer).first()

        message = Message(sender=sender, receiver=receiver, content=content_buyer)
        message.save()
        messages.success(request, '消息发送成功.')

        return redirect('/buyer_messages/')


def hashcode(s, salt='17373252'):
    s += salt
    h = hashlib.sha256()
    h.update(s.encode())
    return h.hexdigest()
