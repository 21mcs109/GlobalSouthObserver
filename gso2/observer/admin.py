from django.contrib import admin
from django.utils import timezone
from django.utils.html import format_html
from .models import (
    AuthorGroup, Author, Post,
    Subscriber, ContactMessage, Podcast,
    Internship, LeadershipApplication, ResearchApplication, AdvisoryMember
)

admin.site.site_header  = "Global South Observer Admin"
admin.site.site_title   = "GSO Admin"
admin.site.index_title  = "GSO Administration Panel"


# ── AUTHOR GROUP ──────────────────────────────────────────────────────────────

@admin.register(AuthorGroup)
class AuthorGroupAdmin(admin.ModelAdmin):
    list_display  = ['name', 'can_publish_directly', 'member_count', 'created_at']
    list_filter   = ['can_publish_directly']
    search_fields = ['name', 'description']

    def member_count(self, obj):
        return obj.members.count()
    member_count.short_description = 'Members'


# ── AUTHOR ────────────────────────────────────────────────────────────────────

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display  = ['full_name', 'username', 'email', 'group', 'is_approved',
                      'post_count', 'total_views', 'created_at']
    list_filter   = ['is_approved', 'group', 'created_at']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'user__email']
    raw_id_fields = ['user']
    actions       = ['approve_authors', 'suspend_authors']

    def full_name(self, obj):
        return obj.user.get_full_name() or obj.user.username
    full_name.short_description = 'Name'

    def username(self, obj):
        return obj.user.username
    username.short_description = 'Username'

    def email(self, obj):
        return obj.user.email
    email.short_description = 'Email'

    def post_count(self, obj):
        return obj.posts.count()
    post_count.short_description = 'Posts'

    def total_views(self, obj):
        return obj.total_views
    total_views.short_description = 'Total Views'

    @admin.action(description='✓ Approve selected authors')
    def approve_authors(self, request, queryset):
        queryset.update(is_approved=True)
        self.message_user(request, f'{queryset.count()} authors approved.')

    @admin.action(description='✗ Suspend selected authors')
    def suspend_authors(self, request, queryset):
        queryset.update(is_approved=False)
        self.message_user(request, f'{queryset.count()} authors suspended.')


# ── POST ──────────────────────────────────────────────────────────────────────

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display  = ['title', 'author_name', 'category', 'status_badge',
                      'views', 'created_at', 'published_at']
    list_filter   = ['status', 'category', 'created_at']
    search_fields = ['title', 'author__user__username', 'author__user__first_name',
                      'keywords', 'content']
    readonly_fields = ['slug', 'views', 'created_at', 'updated_at']
    ordering      = ['-created_at']
    actions       = ['publish_posts', 'reject_posts']

    fieldsets = (
        ('Post Info', {
            'fields': ('title', 'slug', 'author', 'category', 'image', 'keywords')
        }),
        ('Content', {'fields': ('content',)}),
        ('Status', {
            'fields': ('status', 'published_at', 'rejection_reason')
        }),
        ('Stats', {
            'fields': ('views', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def author_name(self, obj):
        return str(obj.author)
    author_name.short_description = 'Author'

    def status_badge(self, obj):
        colours = {
            'published': '#28a745',
            'pending':   '#ffc107',
            'rejected':  '#dc3545',
        }
        colour = colours.get(obj.status, '#6c757d')
        return format_html(
            '<span style="background:{};color:#fff;padding:3px 10px;'
            'border-radius:12px;font-size:.75rem;font-weight:700;">{}</span>',
            colour, obj.get_status_display()
        )
    status_badge.short_description = 'Status'

    @admin.action(description='✓ Publish selected posts')
    def publish_posts(self, request, queryset):
        count = queryset.update(status='published', published_at=timezone.now())
        self.message_user(request, f'{count} posts published successfully.')

    @admin.action(description='✗ Reject selected posts')
    def reject_posts(self, request, queryset):
        count = queryset.update(status='rejected')
        self.message_user(request, f'{count} posts rejected.')


# ── EXISTING MODELS ───────────────────────────────────────────────────────────

@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display  = ['email', 'subscribed_at', 'is_active']
    list_filter   = ['is_active']
    search_fields = ['email']

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display  = ['name', 'email', 'subject', 'created_at', 'is_read']
    list_filter   = ['is_read']
    search_fields = ['name', 'email', 'subject']

@admin.register(Podcast)
class PodcastAdmin(admin.ModelAdmin):
    list_display  = ['title', 'published_at', 'is_featured']
    list_filter   = ['is_featured']
    search_fields = ['title']

@admin.register(Internship)
class InternshipAdmin(admin.ModelAdmin):
    list_display  = ['title', 'department', 'duration', 'is_open']
    list_filter   = ['is_open', 'duration']
    search_fields = ['title', 'department']

@admin.register(LeadershipApplication)
class LeadershipApplicationAdmin(admin.ModelAdmin):
    list_display  = ['name', 'email', 'organization', 'created_at', 'is_reviewed']
    list_filter   = ['is_reviewed']
    search_fields = ['name', 'email', 'organization']

@admin.register(ResearchApplication)
class ResearchApplicationAdmin(admin.ModelAdmin):
    list_display  = ['name', 'email', 'university', 'program', 'created_at', 'is_reviewed']
    list_filter   = ['is_reviewed']
    search_fields = ['name', 'email', 'university']

@admin.register(AdvisoryMember)
class AdvisoryMemberAdmin(admin.ModelAdmin):
    list_display  = ['name', 'designation', 'institution', 'order']
    search_fields = ['name', 'institution', 'research_area']
    ordering      = ['order', 'name']
