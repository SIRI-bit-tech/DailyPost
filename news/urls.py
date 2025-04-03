from django.urls import path
from django.views.generic import TemplateView
from . import views

app_name = 'news'

urlpatterns = [
    # Home
    path('', views.HomePageView.as_view(), name='home'),
    
    # Article detail
    path('article/<int:year>/<int:month>/<int:day>/<slug:slug>/', 
        views.ArticleDetailView.as_view(), name='article_detail'),
    
    # Categories
    path('categories/', views.CategoryListView.as_view(), name='category_list'),
    path('category/<slug:slug>/', views.CategoryDetailView.as_view(), name='category_detail'),
    
    # Tags
    path('tag/<slug:slug>/', views.TagDetailView.as_view(), name='tag_detail'),
    
    # Author
    path('author/<str:username>/', views.AuthorDetailView.as_view(), name='author_detail'),
    
    # Search
    path('search/', views.SearchView.as_view(), name='search'),
    
    # Newsletter
    path('newsletter/', views.NewsletterSubscriptionView.as_view(), name='newsletter'),
    path('newsletter/success/', 
        TemplateView.as_view(template_name='news/newsletter_success.html'),
        name='newsletter_success'),
    path('newsletter/signup/ajax/', views.newsletter_signup_ajax, name='newsletter_signup_ajax'),
    
    # Contact
    path('contact/', views.ContactFormView.as_view(), name='contact'),
    path('contact/success/', 
        TemplateView.as_view(template_name='news/contact_success.html'),
        name='contact_success'),
    
       # Static pages
    path('about/', views.about_view, name='about'),
    path('privacy-policy/', views.privacy_policy_view, name='privacy_policy'),
    path('terms-of-service/', views.terms_of_service_view, name='terms_of_service'),
    path('sitemap-page/', views.sitemap_page, name='sitemap_page'),
    
    # Additional pages
    path('careers/', views.careers_view, name='careers'),
    path('advertise/', views.advertise_view, name='advertise'),
    path('submit-news/', views.submit_news_view, name='submit_news'),
    path('opinion-submission/', views.opinion_submission_view, name='opinion_submission'),
    path('faq/', views.faq_view, name='faq'),
    path('accessibility/', views.accessibility_view, name='accessibility'),
]