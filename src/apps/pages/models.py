from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib import admin
from django.contrib.auth.models import User




category_choices = (
    ('TRAVEL', 'TRAVEL'), ('SZTUKA', 'SZTUKA'), ('BEAUTY','BEAUTY'), ('ŚMIESZNE', 'ŚMIESZNE'),
    ('GAMING', 'GAMING'), ('LIFESTYLE', 'LIFESTYLE'), ('SPORT','SPORT'),)

source_choices = (
    ('YouTube', 'YouTube'), ('TikTok', 'TikTok'), ('Instagram','Instagram'), ('Other', 'Other'),)
# Create your models here.

# OPTIONAL IPMODEL CLASS FOR CUSTOM RATING/LIKE BUTTON
# TO BE DEVELOPED...
class IpModel(models.Model):
    ip = models.CharField(max_length=100, verbose_name = 'IP')
    def __str__(self):
        return self.ip


#MOVIES CLASS
class Movie (models.Model):
    category = models.CharField(max_length=50, verbose_name='Kategoria filmu', default= 'unassigned', null=False, choices=category_choices)
    source = models.CharField(max_length=50, verbose_name='Źródło filmu', default= 'unassigned', null=False, choices=source_choices)
    promotion = models.BooleanField(default=False, verbose_name='PROMOCJA FILMU')
    author = models.CharField(max_length=50, verbose_name='Nazwa influencera')
    title = models.CharField(max_length=80, verbose_name='Nazwa filmu')
    content = models.TextField(max_length=10000, verbose_name='HTML EMBEDED do filmu')
    date_posted = models.DateTimeField(default=timezone.now)
    youtube_url = models.URLField(blank=True, max_length=300)
    tiktok_url = models.URLField(blank=True, max_length=300)
    insta_url = models.URLField(blank=True, max_length=300)
    fire_likes = models.ManyToManyField(IpModel, related_name="fire_likes", blank=True)
    fire_likes_count = models.IntegerField(default=0, null=True, blank=True)


    class Meta:
        verbose_name = ("Movie")
        verbose_name_plural = ("Movies")

    def __str__(self):
        return self.author +' - '+ self.title 

    def get_absolute_url(self):
        return reverse("_detail", kwargs={"pk": self.pk})
    
    #allows sorting column in django admin
    #fire likes -> for further development
    @admin.display(ordering='fire_likes')
    def fire_likes_count(self):
        return self.fire_likes.count()



#ARTICLES POST CLASS
class Post(models.Model):
    title =models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    image = models.ImageField(upload_to='article_pics', null=True, blank=True)
    updated_on = models.DateTimeField(auto_now= True)
    author = models.ForeignKey(User, on_delete= models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})
    
    class Meta:
        ordering = ['-date_posted']


