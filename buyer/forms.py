
from django import forms


class LoginForm(forms.Form):
    phone = forms.CharField(label="手机号", max_length=32, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="密码", max_length=64, widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class RegisterForm(forms.Form):
    name = forms.CharField(label="姓名", max_length=32, widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(label="手机号", max_length=32, widget=forms.TextInput(attrs={'class': 'form-control'}))
    id_card = forms.CharField(label="身份证号",  max_length=32, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label="密码", min_length=6, max_length=64, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="确认密码", min_length=6, max_length=64, widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class SearchForm(forms.Form):
    keyword = forms.CharField(label="搜索词（地址：省市） / 标题（碧桂园））", max_length=32, widget=forms.TextInput(attrs={'class': 'form-control'}))