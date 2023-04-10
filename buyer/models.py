from django.db import models
from seller.models import User as S


class User(models.Model):
    """用户表"""
    name = models.CharField(verbose_name='姓名', max_length=32, null=False)
    phone = models.CharField(verbose_name="手机号", max_length=32, primary_key=True, null=False)
    password = models.CharField(verbose_name='密码', max_length=64, null=False)
    id_card = models.CharField(verbose_name="身份证号", max_length=32, null=False)

    # 对当前表进行设置
    class Meta:
        db_table = 'buyer_user'
        verbose_name = '买家'
        verbose_name_plural = verbose_name

    # 在 str 魔法方法中, 返回用户名称
    def __str__(self):
        return self.name


class Log(models.Model):
    """
    日志表
    """
    id = models.AutoField(verbose_name='序号', primary_key=True)
    time = models.DateTimeField(verbose_name='时间', auto_now_add=True)
    user = models.ForeignKey(User, verbose_name='用户', on_delete=models.CASCADE)
    action = models.CharField(verbose_name='操作', max_length=30)

    class Meta:
        verbose_name = '日志'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return '[{}] {} {}'.format(self.time, self.user, self.action)


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='buyer_sent_messages')
    receiver = models.ForeignKey(S, on_delete=models.CASCADE, related_name='seller_received_messages')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

