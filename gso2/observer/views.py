from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, ListView
from django.http import JsonResponse
from django.utils import timezone

from .models import (
    Post, Author, Podcast, Internship, AdvisoryMember, Subscriber
)
from .forms import (
    SubscriberForm, ContactForm, ResearchApplicationForm,
    AuthorRegistrationForm, AuthorLoginForm, PostSubmissionForm
)

POST_CATEGORIES = [
    {'slug': 'global-south',         'label': 'Global South'},
    {'slug': 'indo-pacific',         'label': 'Indo-Pacific Region'},
    {'slug': 'south-asia',           'label': 'South Asia'},
    {'slug': 'south-east-asia',      'label': 'South East Asia'},
    {'slug': 'africa-latin-america', 'label': 'Africa & Latin America'},
    {'slug': 'europe-middle-east',   'label': 'Europe & Middle East'},
    {'slug': 'arctic-north-america', 'label': 'Arctic & North America'},
]


# ── HOME ──────────────────────────────────────────────────────────────────────

class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        published = Post.objects.filter(status='published').select_related('author__user')
        ctx['latest_posts']   = published.order_by('-published_at')[:6]
        ctx['trending_posts'] = published.order_by('-views')[:5]
        ctx['featured_post']  = published.order_by('-published_at').first()
        ctx['subscribe_form'] = SubscriberForm()
        return ctx


# ── NEWS (from DB posts) ──────────────────────────────────────────────────────

class NewsView(TemplateView):
    template_name = 'news.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        category = self.request.GET.get('category', 'all')
        page_num = int(self.request.GET.get('page', 1))
        per_page = 12

        qs = Post.objects.filter(status='published').select_related('author__user')
        if category and category != 'all':
            qs = qs.filter(category=category)
        qs = qs.order_by('-published_at')

        total  = qs.count()
        offset = (page_num - 1) * per_page
        posts  = qs[offset:offset + per_page]

        ctx.update({
            'posts':            posts,
            'total':            total,
            'current_category': category,
            'current_page':     page_num,
            'has_next':         total > page_num * per_page,
            'has_prev':         page_num > 1,
            'news_categories':  POST_CATEGORIES,
        })
        return ctx


def news_ajax_view(request):
    """AJAX: return posts JSON for a category."""
    category = request.GET.get('category', 'all')
    qs = Post.objects.filter(status='published').select_related('author__user')
    if category and category != 'all':
        qs = qs.filter(category=category)
    qs = qs.order_by('-published_at')[:12]
    data = [{
        'title':        p.title,
        'url':          p.get_absolute_url(),
        'image':        p.image.url if p.image else '/static/images/news-placeholder.svg',
        'description':  p.content[:200],
        'author':       str(p.author),
        'author_url':   p.author.get_absolute_url(),
        'published_at': p.published_at.strftime('%Y-%m-%d') if p.published_at else '',
        'category':     p.get_category_display(),
        'views':        p.views,
    } for p in qs]
    return JsonResponse({'posts': data, 'total': len(data)})


# ── POST DETAIL ───────────────────────────────────────────────────────────────

def post_detail_view(request, slug):
    post    = get_object_or_404(Post, slug=slug, status='published')
    post.increment_views()
    related = Post.objects.filter(
        status='published', category=post.category
    ).exclude(pk=post.pk).order_by('-published_at')[:3]
    return render(request, 'post/detail.html', {'post': post, 'related': related})


# ── AUTHOR REGISTER ───────────────────────────────────────────────────────────

def author_register_view(request):
    if request.user.is_authenticated and hasattr(request.user, 'author_profile'):
        return redirect('author_dashboard')
    if request.method == 'POST':
        form = AuthorRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome {user.get_full_name() or user.username}! Your author account is ready.')
            return redirect('author_dashboard')
    else:
        form = AuthorRegistrationForm()
    return render(request, 'author/register.html', {'form': form})


# ── AUTHOR LOGIN ──────────────────────────────────────────────────────────────

def author_login_view(request):
    if request.user.is_authenticated and hasattr(request.user, 'author_profile'):
        return redirect('author_dashboard')
    if request.method == 'POST':
        form = AuthorLoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user is None:
                messages.error(request, 'Invalid username or password.')
            elif not hasattr(user, 'author_profile'):
                messages.error(request, 'No author account found. Please register first.')
            elif not user.author_profile.is_approved:
                messages.error(request, 'Your account is suspended. Contact admin.')
            else:
                login(request, user)
                return redirect('author_dashboard')
    else:
        form = AuthorLoginForm()
    return render(request, 'author/login.html', {'form': form})


def author_logout_view(request):
    logout(request)
    messages.success(request, 'Logged out successfully.')
    return redirect('home')


# ── AUTHOR DASHBOARD ──────────────────────────────────────────────────────────

@login_required(login_url='/author/login/')
def author_dashboard_view(request):
    if not hasattr(request.user, 'author_profile'):
        return redirect('author_register')
    author = request.user.author_profile
    posts  = author.posts.all().order_by('-created_at')
    ctx = {
        'author':          author,
        'posts':           posts,
        'total_posts':     posts.count(),
        'published_posts': posts.filter(status='published').count(),
        'pending_posts':   posts.filter(status='pending').count(),
        'rejected_posts':  posts.filter(status='rejected').count(),
        'total_views':     author.total_views,
    }
    return render(request, 'author/dashboard.html', ctx)


# ── AUTHOR SUBMIT POST ────────────────────────────────────────────────────────

@login_required(login_url='/author/login/')
def author_submit_post_view(request):
    if not hasattr(request.user, 'author_profile'):
        return redirect('author_register')
    if request.method == 'POST':
        form = PostSubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            post        = form.save(commit=False)
            post.author = request.user.author_profile
            if request.user.author_profile.can_publish_directly:
                post.status       = 'published'
                post.published_at = timezone.now()
                messages.success(request, '✓ Your post has been published directly!')
            else:
                post.status = 'pending'
                messages.success(request, '✓ Post submitted! It will go live after admin review.')
            post.save()
            return redirect('author_dashboard')
    else:
        form = PostSubmissionForm()
    return render(request, 'author/submit.html', {'form': form})


# ── AUTHOR EDIT POST ──────────────────────────────────────────────────────────

@login_required(login_url='/author/login/')
def author_edit_post_view(request, pk):
    if not hasattr(request.user, 'author_profile'):
        return redirect('author_register')
    post = get_object_or_404(Post, pk=pk, author=request.user.author_profile)
    if post.status == 'published':
        messages.error(request, 'Published posts cannot be edited. Contact admin.')
        return redirect('author_dashboard')
    if request.method == 'POST':
        form = PostSubmissionForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            p = form.save(commit=False)
            p.status = 'pending'   # re-submit for review after edit
            p.save()
            messages.success(request, 'Post updated and resubmitted for review.')
            return redirect('author_dashboard')
    else:
        form = PostSubmissionForm(instance=post)
    return render(request, 'author/submit.html', {'form': form, 'editing': True, 'post': post})


# ── PUBLIC AUTHOR PROFILE ─────────────────────────────────────────────────────

def author_public_profile_view(request, username):
    user   = get_object_or_404(User, username=username)
    author = get_object_or_404(Author, user=user)
    posts  = author.posts.filter(status='published').order_by('-published_at')
    return render(request, 'author/profile.html', {
        'author':       author,
        'posts':        posts,
        'total_views':  author.total_views,
        'post_count':   posts.count(),
    })


# ── SUBSCRIBE AJAX ────────────────────────────────────────────────────────────

def subscribe_ajax(request):
    if request.method == 'POST':
        form = SubscriberForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True, 'message': 'Thank you for subscribing!'})
        errors = {f: list(e) for f, e in form.errors.items()}
        return JsonResponse({'success': False, 'errors': errors})
    return JsonResponse({'success': False})


# ── ALL OTHER EXISTING VIEWS (unchanged) ─────────────────────────────────────

class AboutView(TemplateView):
    template_name = 'about.html'
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['about_sections'] = [
            {'id':'about-us',    'label':'About Us'},
            {'id':'who-we-are',  'label':'Who We Are?'},
            {'id':'what-we-offer','label':'What We Are Offering?'},
            {'id':'terms',       'label':'Our Terms & Conditions'},
            {'id':'privacy',     'label':'Privacy Policy'},
            {'id':'third-party', 'label':'Third Party Material'},
            {'id':'subscription','label':'Subscription & Refund Policy'},
        ]
        return ctx

class LeadershipView(TemplateView):
    template_name = 'leadership.html'
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['leadership_sections'] = [
            {'id':'founder',   'label':'Founder Column'},
            {'id':'editorial', 'label':'Editorial Board'},
            {'id':'advisory',  'label':'Advisory Board'},
            {'id':'fellows',   'label':'Research Fellows'},
        ]
        ctx['advisory_members'] = AdvisoryMember.objects.all()
        return ctx

class InternshipsView(TemplateView):
    template_name = 'internship.html'
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['internship_sections'] = [
            {'id':'certificate',        'label':'Certificate Courses'},
            {'id':'leadership-programs','label':'Leadership Programs'},
            {'id':'seminars',           'label':'Seminars, Workshops & Conferences'},
        ]
        ctx['form']             = ResearchApplicationForm()
        ctx['open_internships'] = Internship.objects.filter(is_open=True)
        return ctx
    def post(self, request, *args, **kwargs):
        form = ResearchApplicationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Application submitted!')
            return redirect('internships')
        ctx = self.get_context_data()
        ctx['form'] = form
        return render(request, self.template_name, ctx)

class PoliticalView(TemplateView):
    template_name = 'political.html'
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['political_sections'] = [
            {'id':'research',    'label':'Political Research & Public Opinion'},
            {'id':'social-media','label':'Social Media & Political Communication'},
            {'id':'election',    'label':'Election Strategy & Campaigns'},
            {'id':'survey',      'label':'Election Survey & Data Analysis'},
        ]
        return ctx

class PodcastsView(ListView):
    model = Podcast
    template_name = 'podcasts.html'
    context_object_name = 'podcasts'
    paginate_by = 9

class SubscribeView(TemplateView):
    template_name = 'subscribe.html'
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['form'] = SubscriberForm()
        ctx['subscribe_sections'] = [
            {'id':'membership', 'label':'Subscribe for Membership'},
            {'id':'archive',    'label':'Research Archived'},
            {'id':'journal',    'label':'Journal of Global South Quarterly'},
            {'id':'policy-docs','label':'New Policy Documents'},
            {'id':'annual',     'label':'Annual Reports'},
        ]
        return ctx
    def post(self, request, *args, **kwargs):
        form = SubscriberForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you for subscribing!')
            return redirect('subscribe')
        ctx = self.get_context_data()
        ctx['form'] = form
        return render(request, self.template_name, ctx)

class ContactView(TemplateView):
    template_name = 'contact.html'
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['form'] = ContactForm()
        ctx['contact_sections'] = [
            {'id':'write-for-us','label':'Write for Us'},
            {'id':'email',       'label':'Email ID'},
            {'id':'website',     'label':'Website Link'},
            {'id':'social',      'label':'Social Media'},
        ]
        return ctx
    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Message sent. We will respond within 2 business days.')
            return redirect('contact')
        ctx = self.get_context_data()
        ctx['form'] = form
        return render(request, self.template_name, ctx)

class PrivacyView(TemplateView):
    template_name = 'privacy.html'

class TermsView(TemplateView):
    template_name = 'terms.html'

def custom_404(request, exception):
    return render(request, '404.html', status=404)
