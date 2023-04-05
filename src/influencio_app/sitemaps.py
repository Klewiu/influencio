from django.contrib import sitemaps
from django.urls import reverse
from apps.pages.models import Movie


class StaticViewsSitemap(sitemaps.Sitemap):
    priority = 0.8
    changefreq = 'monthly'

    # The below method returns all urls defined in urls.py file

    def items(self):

        urls =  [
            '/', 
            '/travel', 
            '/sztuka', 
            '/beauty', 
            '/funny', 
            '/lifestyle', 
            '/gaming', 
            '/sport', 
            '/contact', 
            '/privacy',
            '/about',
            '/about',
            '/creators',
            '/articles',
            ]
        
        movies = Movie.objects.all()
        for movie in movies:
            urls.append(f'/?author={movie.author}')

        return urls

    def location(self, item):
        return item