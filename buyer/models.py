from django.db import models


# Create your models here.
class User(models.Model):
    """用户表"""
    name = models.CharField(verbose_name='姓名', max_length=32, null=False)
    phone = models.CharField(verbose_name="手机号",max_length=32, null=False)
    password = models.CharField(verbose_name='密码', max_length=32, null=False)
    id_card = models.CharField(verbose_name="身份证号",max_length=32, null=False)

    # 对当前表进行设置
    class Meta:
        db_table = 'buyer_user'
        verbose_name = '买家'
        verbose_name_plural = verbose_name

    # 在 str 魔法方法中, 返回用户名称
    def __str__(self):
        return self.name
