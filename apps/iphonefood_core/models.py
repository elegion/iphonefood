from django.db import models


class Menu(models.Model):
    name = models.CharField(max_length=200)
    source = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name


class Category(models.Model):
    menu = models.ForeignKey(Menu)
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name


class Dish(models.Model):
    category = models.ForeignKey(Category)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, default='')
    price = models.PositiveIntegerField(blank=True, null=True)
    photo = models.ImageField(upload_to='dishes', blank=True, null=True)
    photo_url = models.URLField(blank=True, null=True)

    rating = models.PositiveSmallIntegerField(blank=True, null=True, help_text=u'Bigger rating --> top place')

    def __unicode__(self):
        return self.name


class Address(models.Model):
    city = models.CharField(max_length=200)
    district = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    