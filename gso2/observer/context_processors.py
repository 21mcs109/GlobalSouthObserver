from django.conf import settings

def site_context(request):
    return {
        'SITE_NAME': settings.SITE_NAME,
        'SITE_TAGLINE': settings.SITE_TAGLINE,
        'SOCIAL_LINKS': settings.SOCIAL_LINKS,
        'NAV_ITEMS': [
            {
                'name': 'Home', 'url': 'home', 'subs': []
            },
            {
                'name': 'About Us', 'url': 'about', 'subs': [
                    {'name': 'About Us', 'url': 'about', 'anchor': '#about-us'},
                    {'name': 'Who We Are?', 'url': 'about', 'anchor': '#who-we-are'},
                    {'name': 'What We Are Offering?', 'url': 'about', 'anchor': '#what-we-offer'},
                    {'name': 'Our Terms & Conditions', 'url': 'about', 'anchor': '#terms'},
                    {'name': 'Privacy Policy', 'url': 'about', 'anchor': '#privacy'},
                    {'name': 'Third Party Material', 'url': 'about', 'anchor': '#third-party'},
                    {'name': 'Subscription & Refund Policy', 'url': 'about', 'anchor': '#subscription'},
                ]
            },
            {
                'name': 'Leadership', 'url': 'leadership', 'subs': [
                    {'name': 'Founder Column', 'url': 'leadership', 'anchor': '#founder'},
                    {'name': 'Editorial Board', 'url': 'leadership', 'anchor': '#editorial'},
                    {'name': 'Advisory Board', 'url': 'leadership', 'anchor': '#advisory'},
                    {'name': 'Research Fellows', 'url': 'leadership', 'anchor': '#fellows'},
                ]
            },
            {
                'name': 'News Updates', 'url': 'news', 'subs': [
                    {'name': 'Indo-Pacific Region', 'url': 'news', 'anchor': '?category=indo-pacific'},
                    {'name': 'South Asia', 'url': 'news', 'anchor': '?category=south-asia'},
                    {'name': 'South East Asia', 'url': 'news', 'anchor': '?category=south-east-asia'},
                    {'name': 'Africa & Latin America', 'url': 'news', 'anchor': '?category=africa-latin-america'},
                    {'name': 'Europe & Middle East', 'url': 'news', 'anchor': '?category=europe-middle-east'},
                    {'name': 'Arctic & North America', 'url': 'news', 'anchor': '?category=arctic-north-america'},
                ]
            },
            {
                'name': 'Research Internship', 'url': 'internships', 'subs': [
                    {'name': 'Certificate Courses', 'url': 'internships', 'anchor': '#certificate'},
                    {'name': 'Leadership Programs', 'url': 'internships', 'anchor': '#leadership-programs'},
                    {'name': 'Seminars, Workshops & Conferences', 'url': 'internships', 'anchor': '#seminars'},
                ]
            },
            {
                'name': 'Political Consultancy', 'url': 'political', 'subs': [
                    {'name': 'Political Research & Public Opinion', 'url': 'political', 'anchor': '#research'},
                    {'name': 'Social Media & Political Communication', 'url': 'political', 'anchor': '#social-media'},
                    {'name': 'Election Strategy & Campaigns', 'url': 'political', 'anchor': '#election'},
                    {'name': 'Election Survey & Data Analysis', 'url': 'political', 'anchor': '#survey'},
                ]
            },
            {
                'name': 'Podcast', 'url': 'podcasts', 'subs': []
            },
            {
                'name': 'Subscribe Us', 'url': 'subscribe', 'subs': [
                    {'name': 'Subscribe for Membership', 'url': 'subscribe', 'anchor': '#membership'},
                    {'name': 'Research Archived', 'url': 'subscribe', 'anchor': '#archive'},
                    {'name': 'Journal of Global South Quarterly', 'url': 'subscribe', 'anchor': '#journal'},
                    {'name': 'New Policy Documents', 'url': 'subscribe', 'anchor': '#policy-docs'},
                    {'name': 'Annual Reports', 'url': 'subscribe', 'anchor': '#annual'},
                ]
            },
            {
                'name': 'Contact Us', 'url': 'contact', 'subs': [
                    {'name': 'Write for Us', 'url': 'contact', 'anchor': '#write-for-us'},
                    {'name': 'Email ID', 'url': 'contact', 'anchor': '#email'},
                    {'name': 'Website Link', 'url': 'contact', 'anchor': '#website'},
                    {'name': 'Social Media', 'url': 'contact', 'anchor': '#social'},
                ]
            },
        ],
    }
