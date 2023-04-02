from django.db import models


# Create your models here.
class User(models.Model):
    """ 用户表 """
    name = models.CharField(verbose_name='姓名',  max_length=32, null=False)
    phone = models.CharField(verbose_name="手机号", max_length=32, primary_key=True, null=False)
    password = models.CharField(verbose_name='密码',  max_length=64, null=False)
    id_card = models.CharField(verbose_name="身份证号", max_length=32, null=False)
    license = models.ImageField(verbose_name="营业执照", upload_to='license', max_length=512)

    # 对当前表进行设置
    class Meta:
        db_table = 'seller_user'
        verbose_name = '卖家'
        verbose_name_plural = verbose_name

    # 在 str 魔法方法中, 返回用户名称
    def __str__(self):
        return self.name


class Area(models.Model):
    """ 地区表 """
    name = models.CharField(verbose_name='区域名称', max_length=50, null=False)

    class Meta:
        db_table = 'address'
        verbose_name = '地区'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class House(models.Model):
    """ 房屋信息表 """
    user = models.ForeignKey(User, verbose_name='房屋用户', on_delete=models.CASCADE)
    area = models.ForeignKey(Area, verbose_name='房屋地址', on_delete=models.CASCADE)
    title = models.CharField(verbose_name="房屋标题", max_length=64, null=None)
    specs = models.CharField(verbose_name="房屋规格(几室几厅几卫)", max_length=64, null=None)
    acreage = models.CharField(verbose_name="房屋大小", max_length=128)
    price = models.CharField(verbose_name="房屋价格", max_length=128)
    introduction = models.TextField(verbose_name="房屋简介")  # 房屋设施，房屋优点
    house_img = models.ImageField(verbose_name="房屋主图片", upload_to='house', max_length=512)

    class Meta:
        db_table = 'house'
        verbose_name = '房屋信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class HouseImage(models.Model):
    """ 房屋具体图片表 """
    house = models.ForeignKey(House, verbose_name='房屋信息', on_delete=models.CASCADE)
    url = models.ImageField(verbose_name='房屋具体图片', upload_to='house', max_length=512)
    upload_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'house_image'
        verbose_name = '房屋图片'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.house.title


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
