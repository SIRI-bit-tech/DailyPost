from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, FormView
from django.views.generic.edit import FormMixin
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.db.models import Q, Count
from django.utils import timezone
from django.http import HttpResponseRedirect, JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from .models import Article, Category, Tag, Author, Comment, Newsletter
from .forms import CommentForm, NewsletterForm, SearchForm, ContactForm

# Mixins
class SEOMixin:
    """Mixin to add SEO context data to views."""
    def get_seo_context(self):
        return {
            'meta_title': 'The Daily Record Post - Latest News & Updates',
            'meta_description': 'Stay updated with the latest news, trends, and in-depth analysis on The Daily Record Post.',
            'meta_keywords': 'news, blog, articles, daily updates, current events',
            'og_title': 'The Daily Record Post',
            'og_description': 'Latest News & In-depth Analysis',
            'twitter_title': 'The Daily Record Post',
            'twitter_description': 'Latest News & In-depth Analysis',
        }
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_seo_context())
        context['newsletter_form'] = NewsletterForm()
        
        # Recent articles
        context['recent_articles'] = Article.objects.filter(
            status='published',
            published_date__lte=timezone.now()
        ).order_by('-published_date')[:5]
        
        # Categories
        context['categories'] = Category.objects.all()
        
        # Popular tags
        context['popular_tags'] = Tag.objects.annotate(
            num_articles=Count('articles')
        ).order_by('-num_articles')[:10]
        
        return context


# Home Page View
class HomePageView(SEOMixin, ListView):
    model = Article
    template_name = 'news/home.html'
    context_object_name = 'articles'
    paginate_by = 10
    
    def get_queryset(self):
        return Article.objects.filter(
            status='published',
            published_date__lte=timezone.now()
        ).order_by('-published_date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Featured articles (most viewed)
        context['featured_articles'] = self.get_queryset().order_by('-view_count')[:5]
        
        return context


# Article Detail View
class ArticleDetailView(SEOMixin, FormMixin, DetailView):
    model = Article
    template_name = 'news/article_detail.html'
    context_object_name = 'article'
    form_class = CommentForm
    
    def get_success_url(self):
        return reverse('news:article_detail', kwargs=self.kwargs)
    
    def get_object(self):
        article = get_object_or_404(
            Article,
            slug=self.kwargs['slug'],
            published_date__year=self.kwargs['year'],
            published_date__month=self.kwargs['month'],
            published_date__day=self.kwargs['day'],
            status='published'
        )
        
        # Increment view count
        article.view_count += 1
        article.save()
        
        return article
    
    def get_seo_context(self):
        article = self.get_object()
        return {
            'meta_title': article.meta_title or article.title,
            'meta_description': article.meta_description or article.summary,
            'meta_keywords': article.meta_keywords,
            'og_title': article.og_title or article.title,
            'og_description': article.og_description or article.summary,
            'twitter_title': article.twitter_title or article.title,
            'twitter_description': article.twitter_description or article.summary,
        }
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article = self.get_object()
        
        # Comments
        context['comments'] = article.comments.filter(approved=True).order_by('created_at')
        
        # Related articles
        context['related_articles'] = Article.objects.filter(
            status='published',
            published_date__lte=timezone.now(),
            category=article.category
        ).exclude(id=article.id).order_by('-published_date')[:3]
        
        return context
    
    @method_decorator(csrf_protect)
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
    
    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.article = self.get_object()
        comment.save()
        messages.success(self.request, "Your comment has been submitted and is awaiting approval.")
        return super().form_valid(form)


# Category Views
class CategoryListView(SEOMixin, ListView):
    model = Category
    template_name = 'news/category_list.html'
    context_object_name = 'categories'


class CategoryDetailView(SEOMixin, ListView):
    template_name = 'news/category_detail.html'
    context_object_name = 'articles'
    paginate_by = 10
    
    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['slug'])
        return Article.objects.filter(
            category=self.category,
            status='published',
            published_date__lte=timezone.now()
        ).order_by('-published_date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        
        # SEO for category page
        context['meta_title'] = f"{self.category.name} - Articles | The Daily Record Post"
        context['meta_description'] = self.category.meta_description or f"Browse all articles in the {self.category.name} category at The Daily Record Post."
        
        return context


# Tag Views
class TagDetailView(SEOMixin, ListView):
    template_name = 'news/tag_detail.html'
    context_object_name = 'articles'
    paginate_by = 10
    
    def get_queryset(self):
        self.tag = get_object_or_404(Tag, slug=self.kwargs['slug'])
        return Article.objects.filter(
            tags=self.tag,
            status='published',
            published_date__lte=timezone.now()
        ).order_by('-published_date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = self.tag
        
        # SEO for tag page
        context['meta_title'] = f"{self.tag.name} - Tagged Articles | The Daily Record Post"
        context['meta_description'] = f"Browse all articles tagged with {self.tag.name} at The Daily Record Post."
        
        return context


# Author View
class AuthorDetailView(SEOMixin, ListView):
    template_name = 'news/author_detail.html'
    context_object_name = 'articles'
    paginate_by = 10
    
    def get_queryset(self):
        self.author = get_object_or_404(Author, user__username=self.kwargs['username'])
        return Article.objects.filter(
            author=self.author,
            status='published',
            published_date__lte=timezone.now()
        ).order_by('-published_date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['author'] = self.author
        
        # SEO for author page
        author_name = self.author.user.get_full_name() or self.author.user.username
        context['meta_title'] = f"Articles by {author_name} | The Daily Record Post"
        context['meta_description'] = f"Read all articles written by {author_name} at The Daily Record Post."
        
        return context


# Search View
class SearchView(SEOMixin, ListView):
    template_name = 'news/search_results.html'
    context_object_name = 'articles'
    paginate_by = 10
    
    def get_queryset(self):
        query = self.request.GET.get('q', '')
        self.query = query
        
        if query:
            return Article.objects.filter(
                Q(title__icontains=query) | 
                Q(content__icontains=query) | 
                Q(summary__icontains=query) |
                Q(meta_keywords__icontains=query) |
                Q(category__name__icontains=query) |
                Q(tags__name__icontains=query),
                status='published',
                published_date__lte=timezone.now()
            ).distinct().order_by('-published_date')
        return Article.objects.none()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.query
        
        # SEO for search page
        context['meta_title'] = f"Search Results for '{self.query}' | The Daily Record Post"
        context['meta_description'] = f"Browse search results for '{self.query}' at The Daily Record Post."
        
        return context


# Newsletter Subscription
class NewsletterSubscriptionView(FormView):
    template_name = 'news/newsletter_form.html'
    form_class = NewsletterForm
    success_url = reverse_lazy('news:newsletter_success')
    
    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Thank you for subscribing! Please check your email to confirm your subscription.")
        return super().form_valid(form)


@require_POST
def newsletter_signup_ajax(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    return JsonResponse({'success': False, 'message': 'Invalid request'})


# Contact Form View
class ContactFormView(FormView):
    template_name = 'news/contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('news:contact_success')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['meta_title'] = "Contact Us | The Daily Record Post"
        context['meta_description'] = "Get in touch with The Daily Record Post editorial team."
        return context
    
    def form_valid(self, form):
        # Process the form data (e.g., send email)
        form.send_email()
        messages.success(self.request, "Thank you for your message. We'll get back to you soon.")
        return super().form_valid(form)


# About Us Page
def about_view(request):
    return render(request, 'news/about.html', {
        'meta_title': 'About Us | The Daily Record Post',
        'meta_description': 'Learn more about The Daily Record Post, our mission and our team.',
    })


# Privacy Policy Page
def privacy_policy_view(request):
    return render(request, 'news/privacy_policy.html', {
        'meta_title': 'Privacy Policy | The Daily Record Post',
        'meta_description': 'The Daily Record Post privacy policy and terms of service.',
    })


# Terms of Service Page
def terms_of_service_view(request):
    return render(request, 'news/terms.html', {
        'meta_title': 'Terms of Service | The Daily Record Post',
        'meta_description': 'The Daily Record Post terms of service and usage agreement.',
    })


# Sitemap view for SEO
def sitemap_page(request):
    categories = Category.objects.all()
    tags = Tag.objects.all()
    articles = Article.objects.filter(status='published', published_date__lte=timezone.now())
    
    return render(request, 'news/sitemap.html', {
        'categories': categories,
        'tags': tags,
        'articles': articles,
        'meta_title': 'Sitemap | The Daily Record Post',
        'meta_description': 'Browse all content on The Daily Record Post through our sitemap.',
    })


# FAQ Page
def faq_view(request):
    return render(request, 'news/faq.html', {
        'meta_title': 'Frequently Asked Questions | The Daily Record Post',
        'meta_description': 'Find answers to the most commonly asked questions about The Daily Record Post, our content, subscriptions, and policies.',
    })


# Careers Page
def careers_view(request):
    return render(request, 'news/careers.html', {
        'meta_title': 'Careers | The Daily Record Post',
        'meta_description': 'Join our team at The Daily Record Post. Explore current job openings and career opportunities in journalism, technology, marketing, and more.',
    })


# Accessibility Page
def accessibility_view(request):
    return render(request, 'news/accessibility.html', {
        'meta_title': 'Accessibility Statement | The Daily Record Post',
        'meta_description': 'Learn about The Daily Record Post\'s commitment to accessibility and how we strive to make our content available to all readers.',
    })


# Advertise Page
def advertise_view(request):
    return render(request, 'news/advertise.html', {
        'meta_title': 'Advertise With Us | The Daily Record Post',
        'meta_description': 'Promote your brand to our engaged audience. Explore advertising opportunities and partnership options with The Daily Record Post.',
    })


# Submit News Page
def submit_news_view(request):
    return render(request, 'news/submit_news.html', {
        'meta_title': 'Submit News | The Daily Record Post',
        'meta_description': 'Submit a news tip, story idea, or press release to The Daily Record Post. Share your community news with our editorial team.',
    })


# Opinion Submission Page
def opinion_submission_view(request):
    return render(request, 'news/opinion_submission.html', {
        'meta_title': 'Submit Opinion | The Daily Record Post',
        'meta_description': 'Submit a letter to the editor, op-ed, or opinion piece to The Daily Record Post. Share your perspective with our readers and community.',
    })