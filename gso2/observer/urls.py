from django.urls import path
from . import views

urlpatterns = [
    # ── Public pages ───────────────────────────────────────────────────
    path('', views.HomeView.as_view(), name='home'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('news/', views.NewsView.as_view(), name='news'),
    path('news/ajax/', views.news_ajax_view, name='news_ajax'),
    path('leadership/', views.LeadershipView.as_view(), name='leadership'),
    path('internships/', views.InternshipsView.as_view(), name='internships'),
    path('political-consultancy/', views.PoliticalView.as_view(), name='political'),
    path('podcasts/', views.PodcastsView.as_view(), name='podcasts'),
    path('subscribe/', views.SubscribeView.as_view(), name='subscribe'),
    path('api/subscribe/', views.subscribe_ajax, name='subscribe_ajax'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('privacy/', views.PrivacyView.as_view(), name='privacy'),
    path('terms/', views.TermsView.as_view(), name='terms'),

    # ── Posts ──────────────────────────────────────────────────────────
    path('post/<slug:slug>/', views.post_detail_view, name='post_detail'),

    # ── Author auth ────────────────────────────────────────────────────
    path('author/register/', views.author_register_view, name='author_register'),
    path('author/login/',    views.author_login_view,    name='author_login'),
    path('author/logout/',   views.author_logout_view,   name='author_logout'),

    # ── Author dashboard ───────────────────────────────────────────────
    path('author/dashboard/',         views.author_dashboard_view,   name='author_dashboard'),
    path('author/submit/',            views.author_submit_post_view, name='author_submit'),
    path('author/edit/<int:pk>/',     views.author_edit_post_view,   name='author_edit_post'),

    # ── Public author profile ──────────────────────────────────────────
    path('author/<str:username>/', views.author_public_profile_view, name='author_public_profile'),
]
