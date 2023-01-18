from django.db import models


# Create your models here.
class User(models.Model):
    """ 用户表 """
    name = models.CharField(verbose_name='姓名',  max_length=32, null=False)
    phone = models.CharField(verbose_name="手机号", max_length=32, null=False)
    password = models.CharField(verbose_name='密码',  max_length=32, null=False)
    id_card = models.CharField(verbose_name="身份证号", max_length=32, null=False)
    succ = models.CharField(verbose_name="统一社会信用代码", max_length=32, null=False)
    license = models.ImageField(verbose_name="营业执照", upload_to='license', default='')

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
    name = models.CharField(verbose_name='区域名称', max_length=32, null=False)

    class Meta:
        db_table = 'address'
        verbose_name = '地区'
        verbose_name_plural = verbose_name


class House(models.Model):
    """ 房屋信息表 """
    user = models.ForeignKey(User, verbose_name='房屋用户', on_delete=models.CASCADE)
    area = models.ForeignKey(Area, verbose_name='房屋地区', on_delete=models.CASCADE)
    title = models.CharField(verbose_name="房屋标题", max_length=64, null=None)
    specs = models.CharField(verbose_name="房屋规格",max_length=64, null=None) # 几室几厅几卫
    acreage = models.IntegerField(verbose_name="房屋大小", default=0)
    address = models.CharField(verbose_name="房屋地址", max_length=192, null=None)
    price = models.IntegerField(verbose_name="价格单价", default=0)
    introduction = models.TextField(verbose_name="房屋简介")  # 房屋设施，房屋优点
    house_img = models.ImageField(verbose_name="房屋主图片", upload_to='house', default='')

    class Meta:
        db_table = 'house'
        verbose_name = '房屋信息'
        verbose_name_plural = verbose_name


class HouseImage(models.Model):
    """ 房屋具体图片表 """
    house = models.ForeignKey(House, verbose_name='房屋信息', on_delete=models.CASCADE)
    url = models.ImageField(verbose_name='房屋具体图片', upload_to='house', default='' )

    class Meta:
        db_table = 'house_image'
        verbose_name = '房屋图片'
        verbose_name_plural = verbose_name
