
from django import forms
from .models import House


class LoginForm(forms.Form):
    phone = forms.CharField(label="手机号", max_length=32, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="密码", max_length=64, widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class RegisterForm(forms.Form):
    name = forms.CharField(label="姓名", max_length=32, widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(label="手机号", max_length=32, widget=forms.TextInput(attrs={'class': 'form-control'}))
    id_card = forms.CharField(label="身份证号",  max_length=32, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label="密码", min_length=6, max_length=64, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="确认密码", min_length=6, max_length=64, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    license = forms.ImageField(label="营业执照", required=True, max_length=512, widget=forms.FileInput(attrs={'class': 'form-control'}))


class SellerUpdateForm(forms.Form):
    name = forms.CharField(label="姓名", max_length=32, widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(label="手机号", max_length=32, widget=forms.TextInput(attrs={'class': 'form-control'}))
    id_card = forms.CharField(label="身份证号",  max_length=32, widget=forms.TextInput(attrs={'class': 'form-control'}))
    license = forms.ImageField(label="营业执照", required=True, max_length=512, widget=forms.FileInput(attrs={'class': 'form-control'}))


# 增加房源，直接根据model来生成表单
class CreateForm(forms.Form):
    area = forms.CharField(label="房屋地址", max_length=128, widget=forms.TextInput(
        attrs={'class': 'form-control', 'style': 'height: 40px;'}))
    title = forms.CharField(label="房屋标题", max_length=128, widget=forms.TextInput(
        attrs={'class': 'form-control', 'style': 'height: 40px;'}))
    specs = forms.CharField(label="房屋规格(几室几厅几卫)", max_length=128, widget=forms.TextInput(
        attrs={'class': 'form-control', 'style': 'height: 40px;'}))
    acreage = forms.CharField(label="房屋大小", max_length=64, widget=forms.TextInput(
        attrs={'class': 'form-control', 'style': 'height: 40px;'}))
    price = forms.CharField(label="房屋价格", max_length=128, widget=forms.TextInput(
        attrs={'class': 'form-control', 'style': 'height: 40px;'}))
    introduction = forms.CharField(label="房屋简介", max_length=1024,
                                   widget=forms.Textarea(attrs={'class': 'form-control'}))
    house_img = forms.ImageField(label="房屋图片（可按住ctrl选中多张图片）", widget=forms.ClearableFileInput(
        attrs={'class': 'form-control', 'multiple': True, 'style': 'height: 40px;'}))


# 用户卖家发布房源时的数据验证
class HouseForm(forms.ModelForm):
    class Meta:
        model = House
        fields = ['area', 'title', 'specs', 'acreage', 'price', 'introduction']