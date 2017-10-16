from django.db import models


class Country(models.Model):
    title_ru = models.CharField(max_length=60)
    title_en = models.CharField(max_length=60)
    #slug = models.SlugField(max_length=200, db_index=True, unique=True)

    class Meta:
        db_table = '_countries'
        ordering = ('id',)

    def __str__(self):
        return self.title_ru


class City(models.Model):
    city_name = models.CharField(max_length=60)
    country = models.ForeignKey(Country, related_name='country_country_id')
    #slug = models.SlugField(max_length=200, db_index=True, unique=True)

    class Meta:
        db_table = '_cities'

    def __str__(self):
        return self.city_name
