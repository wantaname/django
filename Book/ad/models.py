from django.db import models
from db.base_model import BaseModel
# Create your models here.
class Ad(BaseModel):
    name=models.CharField(max_length=20,verbose_name='广告名')
    image=models.ImageField(upload_to='ads',verbose_name='广告图')
    url=models.CharField(max_length=100,verbose_name='链接')

    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural=verbose_name='广告管理'