from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from django.utils import timezone

from .models import Article, Category, Tag

class ArticleSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9
    
    def items(self):
        return Article.objects.filter(
            status='published', 
            published_date__lte=timezone.now()
        ).order_by('-published_date')
    
    def lastmod(self, obj):
        return obj.updated_date
    
    def location(self, obj):
        return obj.get_absolute_url()


class CategorySitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.8
    
    def items(self):
        return Category.objects.all()
    
    def lastmod(self, obj):
        return obj.updated_at
    
    def location(self, obj):
        return obj.get_absolute_url()


class TagSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.7
    
    def items(self):
        return Tag.objects.all()
    
    def location(self, obj):
        return obj.get_absolute_url()


class StaticViewSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.5
    
    def items(self):
        return [
            'news:home',
            'news:about',
            'news:contact',
            'news:privacy_policy',
            'news:terms_of_service',
            'news:sitemap_page',
        ]
    
    def location(self, item):
        return reverse(item)