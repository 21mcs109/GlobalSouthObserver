from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.db.models import F, Sum
import uuid


# ── AUTHOR SYSTEM ─────────────────────────────────────────────────────────────

class AuthorGroup(models.Model):
    """Admin-created groups whose members can publish without approval."""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    can_publish_directly = models.BooleanField(
        default=True,
        help_text='Members bypass admin approval and publish directly.'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Author Group'
        verbose_name_plural = 'Author Groups'

    def __str__(self):
        return self.name


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='author_profile')
    bio = models.TextField(blank=True)
    photo = models.ImageField(upload_to='authors/', blank=True, null=True)
    website = models.URLField(blank=True)
    twitter_handle = models.CharField(max_length=100, blank=True)
    linkedin_url = models.URLField(blank=True)
    group = models.ForeignKey(
        AuthorGroup, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='members'
    )
    is_approved = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Author'
        verbose_name_plural = 'Authors'

    def __str__(self):
        return self.user.get_full_name() or self.user.username

    @property
    def can_publish_directly(self):
        return bool(self.group and self.group.can_publish_directly)

    @property
    def total_views(self):
        return self.posts.filter(status='published').aggregate(
            total=Sum('views'))['total'] or 0

    @property
    def published_count(self):
        return self.posts.filter(status='published').count()

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('author_public_profile', kwargs={'username': self.user.username})


# ── POST ──────────────────────────────────────────────────────────────────────

class Post(models.Model):
    CATEGORY_CHOICES = [
        ('global-south',        'Global South'),
        ('indo-pacific',        'Indo-Pacific Region'),
        ('south-asia',          'South Asia'),
        ('south-east-asia',     'South East Asia'),
        ('africa-latin-america','Africa & Latin America'),
        ('europe-middle-east',  'Europe & Middle East'),
        ('arctic-north-america','Arctic & North America'),
    ]
    STATUS_CHOICES = [
        ('pending',   'Pending Review'),
        ('published', 'Published'),
        ('rejected',  'Rejected'),
    ]

    title            = models.CharField(max_length=300)
    slug             = models.SlugField(max_length=320, unique=True, blank=True)
    author           = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='posts')
    category         = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    image            = models.ImageField(upload_to='posts/%Y/%m/')
    keywords         = models.CharField(max_length=500, help_text='Comma-separated keywords')
    content          = models.TextField()
    status           = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    views            = models.PositiveIntegerField(default=0)
    rejection_reason = models.TextField(blank=True)
    created_at       = models.DateTimeField(auto_now_add=True)
    updated_at       = models.DateTimeField(auto_now=True)
    published_at     = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title)[:280]
            uid  = uuid.uuid4().hex[:6]
            self.slug = f"{base}-{uid}" if base else uid
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('post_detail', kwargs={'slug': self.slug})

    def increment_views(self):
        Post.objects.filter(pk=self.pk).update(views=F('views') + 1)


# ── EXISTING MODELS (unchanged) ───────────────────────────────────────────────

class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    class Meta:
        ordering = ['-subscribed_at']
    def __str__(self):
        return self.email

class ContactMessage(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    subject = models.CharField(max_length=300)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    class Meta:
        ordering = ['-created_at']
    def __str__(self):
        return f"{self.name} — {self.subject}"

class Podcast(models.Model):
    title = models.CharField(max_length=300)
    description = models.TextField()
    youtube_url = models.URLField()
    published_at = models.DateTimeField()
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-published_at']
    def __str__(self):
        return self.title
    def get_embed_url(self):
        if 'watch?v=' in self.youtube_url:
            vid = self.youtube_url.split('watch?v=')[-1].split('&')[0]
            return f"https://www.youtube.com/embed/{vid}"
        if 'youtu.be/' in self.youtube_url:
            vid = self.youtube_url.split('youtu.be/')[-1].split('?')[0]
            return f"https://www.youtube.com/embed/{vid}"
        return self.youtube_url

class Internship(models.Model):
    DURATION_CHOICES = [
        ('1_month','1 Month'),('2_months','2 Months'),
        ('3_months','3 Months'),('6_months','6 Months'),('flexible','Flexible')
    ]
    title = models.CharField(max_length=300)
    department = models.CharField(max_length=200)
    description = models.TextField()
    eligibility = models.TextField()
    duration = models.CharField(max_length=20, choices=DURATION_CHOICES, default='3_months')
    benefits = models.TextField()
    is_open = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-created_at']
    def __str__(self):
        return self.title

class LeadershipApplication(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    organization = models.CharField(max_length=300)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_reviewed = models.BooleanField(default=False)
    class Meta:
        ordering = ['-created_at']
    def __str__(self):
        return f"{self.name} — {self.organization}"

class ResearchApplication(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    university = models.CharField(max_length=300)
    program = models.CharField(max_length=200)
    internship = models.ForeignKey(Internship, on_delete=models.SET_NULL, null=True, blank=True)
    cover_letter = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_reviewed = models.BooleanField(default=False)
    class Meta:
        ordering = ['-created_at']
    def __str__(self):
        return f"{self.name} — {self.university}"

class AdvisoryMember(models.Model):
    name = models.CharField(max_length=200)
    designation = models.CharField(max_length=300)
    institution = models.CharField(max_length=300)
    research_area = models.CharField(max_length=300)
    biography = models.TextField()
    photo = models.ImageField(upload_to='advisory/', blank=True, null=True)
    photo_url = models.URLField(blank=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['order', 'name']
    def __str__(self):
        return self.name
    def get_photo(self):
        if self.photo:
            return self.photo.url
        if self.photo_url:
            return self.photo_url
        return '/static/images/default-avatar.svg'
