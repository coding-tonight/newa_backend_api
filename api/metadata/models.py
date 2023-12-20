from django.db import models

# Create your models here.


class Province(models.Model):
    province_name = models.IntegerField(null=True)

    class Meta:
        db_table = 'provinces'

    def __str__(self):
        return self.province_name


class Districts(models.Model):
    province = models.ForeignKey(
        Province, related_name="+", on_delete=models.PROTECT)
    district_name = models.CharField(max_length=45)

    class Meta:
        db_table = 'districts'

    def __str__(self):
        return self.district_name


class City(models.Model):
    district = models.ForeignKey(
        Districts, related_name="+", on_delete=models.PROTECT)
    city_name = models.CharField(max_length=45)

    class Meta:
        db_table = 'cities'

    
    def __str__(self):
        return self.city_name


class MetaData(models.Model):
    website_name = models.CharField(max_length=45)
    logo = models.ImageField(upload_to='uploads/metadata/')
    phone_number = models.CharField(max_length=14)
    email_address = models.CharField()
    facebook = models.CharField(null=True)
    linkedin = models.CharField(null=True)
    youtube = models.CharField(null=True)
    instagram = models.CharField(null=True)

    class Meta:
        db_table = 'metadata'
    
    def __str__(self):
        return self.website_name

    