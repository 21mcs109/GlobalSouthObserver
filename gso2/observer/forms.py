from django import forms
from django.contrib.auth.models import User
from .models import (
    Subscriber, ContactMessage, ResearchApplication,
    Author, Post
)


# ── AUTHOR REGISTRATION ───────────────────────────────────────────────────────

class AuthorRegistrationForm(forms.Form):
    # User fields
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control','placeholder':'First Name'}))
    last_name  = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Last Name'}))
    username   = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Username (used for login)'}))
    email      = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'Email Address'}))
    password1  = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password (min 8 characters)'}))
    password2  = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Confirm Password'}))
    # Author fields
    bio             = forms.CharField(label='Short Bio', required=False, widget=forms.Textarea(attrs={'class':'form-control','placeholder':'Brief biography about yourself (shown on your public profile)','rows':3}))
    photo           = forms.ImageField(label='Profile Photo', required=False, widget=forms.FileInput(attrs={'class':'form-control'}))
    website         = forms.URLField(required=False, widget=forms.URLInput(attrs={'class':'form-control','placeholder':'https://your-website.com'}))
    twitter_handle  = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'class':'form-control','placeholder':'@your_twitter_handle'}))
    linkedin_url    = forms.URLField(required=False, widget=forms.URLInput(attrs={'class':'form-control','placeholder':'https://linkedin.com/in/yourprofile'}))

    def clean_username(self):
        username = self.cleaned_data['username'].strip()
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('This username is already taken. Please choose another.')
        return username

    def clean_email(self):
        email = self.cleaned_data['email'].strip().lower()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('An account with this email already exists.')
        return email

    def clean_password1(self):
        p = self.cleaned_data.get('password1', '')
        if len(p) < 8:
            raise forms.ValidationError('Password must be at least 8 characters.')
        return p

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get('password1')
        p2 = cleaned.get('password2')
        if p1 and p2 and p1 != p2:
            self.add_error('password2', 'Passwords do not match.')
        return cleaned

    def save(self):
        cd = self.cleaned_data
        user = User.objects.create_user(
            username=cd['username'],
            email=cd['email'],
            password=cd['password1'],
            first_name=cd['first_name'],
            last_name=cd['last_name'],
        )
        Author.objects.create(
            user=user,
            bio=cd.get('bio', ''),
            photo=cd.get('photo'),
            website=cd.get('website', ''),
            twitter_handle=cd.get('twitter_handle', ''),
            linkedin_url=cd.get('linkedin_url', ''),
        )
        return user


# ── AUTHOR LOGIN ──────────────────────────────────────────────────────────────

class AuthorLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Username','autofocus':True}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password'}))


# ── POST SUBMISSION ───────────────────────────────────────────────────────────

class PostSubmissionForm(forms.ModelForm):
    class Meta:
        model  = Post
        fields = ['title','category','image','keywords','content']
        widgets = {
            'title':    forms.TextInput(attrs={'class':'form-control','placeholder':'Article title — clear and descriptive'}),
            'category': forms.Select(attrs={'class':'form-control'}),
            'image':    forms.FileInput(attrs={'class':'form-control','accept':'image/*'}),
            'keywords': forms.TextInput(attrs={'class':'form-control','placeholder':'e.g. diplomacy, BRICS, India, geopolitics (comma separated)'}),
            'content':  forms.Textarea(attrs={'class':'form-control','placeholder':'Write your full article here...','rows':18}),
        }

    def clean_title(self):
        title = self.cleaned_data.get('title', '').strip()
        if len(title) < 10:
            raise forms.ValidationError('Title must be at least 10 characters.')
        return title

    def clean_content(self):
        content = self.cleaned_data.get('content', '').strip()
        if len(content.split()) < 200:
            raise forms.ValidationError('Article must be at least 200 words.')
        return content

    def clean_keywords(self):
        kw = self.cleaned_data.get('keywords', '').strip()
        if not kw:
            raise forms.ValidationError('Please provide at least one keyword.')
        return kw


# ── EXISTING FORMS (unchanged) ────────────────────────────────────────────────

class SubscriberForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ['email']
        widgets = {'email': forms.EmailInput(attrs={'class':'form-control','placeholder':'Enter your email address'})}
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Subscriber.objects.filter(email=email, is_active=True).exists():
            raise forms.ValidationError("This email is already subscribed.")
        return email

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name','email','subject','message']
        widgets = {
            'name':    forms.TextInput(attrs={'class':'form-control','placeholder':'Your Full Name'}),
            'email':   forms.EmailInput(attrs={'class':'form-control','placeholder':'Your Email Address'}),
            'subject': forms.TextInput(attrs={'class':'form-control','placeholder':'Subject'}),
            'message': forms.Textarea(attrs={'class':'form-control','placeholder':'Your message...','rows':5}),
        }

class ResearchApplicationForm(forms.ModelForm):
    class Meta:
        model = ResearchApplication
        fields = ['name','email','phone','university','program','internship','cover_letter']
        widgets = {
            'name':         forms.TextInput(attrs={'class':'form-control','placeholder':'Full Name'}),
            'email':        forms.EmailInput(attrs={'class':'form-control','placeholder':'Email Address'}),
            'phone':        forms.TextInput(attrs={'class':'form-control','placeholder':'Phone Number'}),
            'university':   forms.TextInput(attrs={'class':'form-control','placeholder':'University / Institution'}),
            'program':      forms.TextInput(attrs={'class':'form-control','placeholder':'Academic Program / Degree'}),
            'internship':   forms.Select(attrs={'class':'form-control'}),
            'cover_letter': forms.Textarea(attrs={'class':'form-control','placeholder':'Why do you want to intern with us?','rows':5}),
        }
