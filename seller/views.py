from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from seller.forms import LoginForm, RegisterForm, CreateForm, SellerUpdateForm
from seller.models import User, Log, House, HouseImage, Area
import hashlib
from django.contrib import messages


class LoginSeller(View):
    """ 卖家登入 """
    def get(self, request):
        if request.session.get('is_login', None):
            return redirect('/home_seller/')
        login_form = LoginForm()
        return render(request, 'login_seller.html', locals())

    def post(self, request):
        login_form = LoginForm(request.POST)
        message = '请检查填写的内容！'
        if login_form.is_valid():
            phone = login_form.cleaned_data['phone']
            password = login_form.cleaned_data['password']
            user = User.objects.filter(phone=phone).first()

            if user.password == hashcode(password):
                request.session['is_login'] = True
                request.session['phone'] = user.phone
                Log.objects.create(user_id=phone, action='登入')
                return redirect('/home_seller/')
            else:
                message = '手机号或密码错误，也许没有注册！'
        return render(request, 'login_seller.html', locals())


class LogoutSeller(View):
    """
    登出
    """
    def get(self, request):
        if request.session.get('is_login', None):
            Log.objects.create(user_id=request.session['phone'], action='登出')
            request.session.flush()
            messages.success(request, '登出成功！')
        return redirect('/login_seller/')


class RegisterSeller(View):
    """ 商家注册 """
    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'register_seller.html', locals())

    def post(self, request):
        register_form = RegisterForm(request.POST, request.FILES)
        message = '请检查填写的内容！'
        if register_form.is_valid():
            name = register_form.cleaned_data['name']
            phone = register_form.cleaned_data['phone']
            id_card = register_form.cleaned_data['id_card']
            license_ = request.FILES.get('license')
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            if password1 == password2:
                same_id_users = User.objects.filter(phone=phone)
                if same_id_users:
                    message = '该用户被注册！'
                else:
                    User.objects.create(name=name, phone=phone, id_card=id_card, license=license_, password=hashcode(password2))
                    Log.objects.create(user_id=phone, action='注册')
                    messages.success(request, '注册成功！')
                    return redirect('/login_seller/')
            else:
                message = '两次输入的密码不一致！'
        return render(request, 'register_seller.html', locals())


class HomeSeller(View):
    """
    个人中心
    """
    def get(self, request):
        if not request.session.get('is_login', None):
            messages.error(request, '请先登录！')
            return redirect('/login_seller/')

        seller = User.objects.filter(phone=request.session['phone']).first()
        houses = House.objects.filter(user_id=request.session['phone'])

        return render(request, 'home_seller.html', locals())


class SellerUpdate(View):
    def get(self, request):
        if not request.session.get('is_login', None):
            messages.error(request, '请先登录！')
            return redirect('/login_seller/')

        form = SellerUpdate
        return render(request, 'seller_update.html', locals())

    def post(self, request):
        form = SellerUpdateForm(request.POST, request.FILES)
        user = User.objects.filter(phone=request.session['phone']).first()

        if form.is_valid():
            name = form.cleaned_data['name']
            phone = form.cleaned_data['phone']
            id_card = form.cleaned_data['id_card']
            lic = request.FILES.get('license')
            # password默认不变
            user.name = name
            user.phone = phone
            user.id_card = id_card
            user.license = lic
            user.save()

            # 在Python中，类的实例（包括模型实例）是引用对象，因此修改模型实例的属性值并不会导致查询返回的对象的属性值发生改变。
            # 因此，你在修改user对象的电话号码后，如果你想让所有和该用户关联的房源的user_id属性值也发生变化，
            # 需要分别修改每个房源对象的user_id属性值
            houses = House.objects.filter(user_id=request.session['phone'])

            for house in houses:
                house.user_id = phone
                house.save()

            Log.objects.create(user_id=user.phone, action='修改用户')
            messages.success(request, '用户信息修改成功！')

            # 重新获取 修改后houses
            houses = House.objects.filter(user_id=user.phone)
            context = {
                'update_user': user,
                'houses': houses
            }
            return render(request, 'home_seller.html', context=context)

        return render(request, 'home_seller.html', locals())


class MyHouses(View):
    """
    我的房源
    """
    def get(self, request):
        if not request.session.get('is_login', None):
            messages.error(request, '请先登录！')
            return redirect('/login_seller/')

        phone = request.session['phone']
        houses = House.objects.filter(user_id=phone)

        return render(request, 'my_houses.html', locals())


class HouseDetailView(View):
    def get(self, request, house_id):
        if not request.session.get('is_login', None):
            messages.error(request, '请先登录！')
            return redirect('/login_seller/')

        house = get_object_or_404(House, id=house_id)

        return render(request, 'house_detail.html', locals())


class HouseCreateView(View):
    def get(self, request):
        if not request.session.get('is_login', None):
            messages.error(request, '请先登录！')
            return redirect('/login_seller/')
        create_form = CreateForm()
        return render(request, 'house_create.html', locals())

    def post(self, request):
        create_from = CreateForm(request.POST, request.FILES)
        message = "请检查填写的内容"
        # 检测连接的用户
        # for key, value in request.session.items():
        #     print(key, value)
        user = User.objects.filter(phone=request.session['phone']).first()

        if create_from.is_valid():
            area = create_from.cleaned_data['area']
            title = create_from.cleaned_data['title']
            specs = create_from.cleaned_data['specs']
            acreage = create_from.cleaned_data['acreage']
            price = create_from.cleaned_data['price']
            introduction = create_from.cleaned_data['introduction']
            house_images = create_from.cleaned_data['house_img']
            img = request.FILES.getlist('house_img')
            area = Area.objects.create(name=area)
            house = House.objects.create(user_id=user.phone, title=title, specs=specs, acreage=acreage, area=area,
                                 price=price, introduction=introduction, house_img=house_images)
            for img in img:
                HouseImage.objects.create(url=img, house=house)
            Log.objects.create(user_id=user.phone, action="增加房源")
            messages.success(request, '增加成功！')
            return redirect('/my_houses/')

        return render(request, 'house_create.html', locals())


class HouseUpdateView(View):
    def get(self, request, house_id):
        if not request.session.get('is_login', None):
            messages.error(request, '请先登录！')
            return redirect('/login_seller/')

        user = User.objects.filter(phone=request.session['phone']).first()
        house = get_object_or_404(House, id=house_id)

        if house.user_id != user.phone:
            messages.error(request, '无权修改此房源！')
            return redirect('/my_houses/')
        else:
            update_form = CreateForm()
            return render(request, 'house_update.html', locals())

    def post(self, request, house_id):
        if not request.session.get('is_login', None):
            messages.error(request, '请先登录！')
            return redirect('/login_seller/')

        user = User.objects.filter(phone=request.session['phone']).first()
        house = get_object_or_404(House, id=house_id)

        if house.user_id != user.phone:
            messages.error(request, '无权修改房源！')
            return redirect('/my_houses/')
        else:
            update_form = CreateForm(request.POST, request.FILES)

            if update_form.is_valid():
                area = update_form.cleaned_data['area']
                title = update_form.cleaned_data['title']
                specs = update_form.cleaned_data['specs']
                acreage = update_form.cleaned_data['acreage']
                price = update_form.cleaned_data['price']
                introduction = update_form.cleaned_data['introduction']
                house_images = update_form.cleaned_data['house_img']
                img = request.FILES.getlist('house_img')

                area = Area.objects.create(name=area)
                house.area = area
                house.title = title
                house.specs = specs
                house.acreage = acreage
                house.price = price
                house.introduction = introduction
                house.house_img = house_images
                house.save()

                HouseImage.objects.filter(house=house).delete()
                for img in img:
                    HouseImage.objects.create(url=img, house=house)

                Log.objects.create(user_id=user.phone, action='修改房源')
                messages.success(request, '修改成功！')
                return redirect('/my_houses/')

            return render(request, 'house_update.html', locals())


class HouseDeleteView(View):
    #  get() 方法用于展示房源删除确认页面，而 post() 方法用于删除房源，并跳转到房源列表页面。
    def get(self, request, house_id):
        if not request.session.get('is_login', None):
            messages.error(request, '请先登录！')
            return redirect('/login_seller/')
        user = User.objects.filter(phone=request.session['phone']).first()
        house = get_object_or_404(House, id=house_id)
        if house.user_id != user.phone:
            messages.error(request, '无权删除此房源！')
            return redirect('/my_houses/')
        return render(request, 'house_delete.html', {'house': house})

    def post(self, request, house_id):
        user = User.objects.filter(phone=request.session['phone']).first()
        house = get_object_or_404(House, id=house_id)
        if house.user_id != user.phone:
            messages.error(request, '无权删除此房源！')
            return redirect('/my_houses/')
        house.delete()
        Log.objects.create(user_id=user.phone, action="删除房源")
        messages.success(request, '删除成功！')
        return redirect('/my_houses/')


def hashcode(s, salt='17373252'):
    s += salt
    h = hashlib.sha256()
    h.update(s.encode())
    return h.hexdigest()

