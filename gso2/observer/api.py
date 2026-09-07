import requests
from django.conf import settings

CATEGORY_QUERIES = {
    'indo-pacific':         'Indo-Pacific Region security geopolitics ASEAN',
    'south-asia':           'South Asia India Pakistan Bangladesh Sri Lanka',
    'south-east-asia':      'Southeast Asia Vietnam Philippines Malaysia Thailand',
    'africa-latin-america': 'Africa Latin America South America Brazil diplomacy',
    'europe-middle-east':   'Europe Middle East EU NATO Gulf policy',
    'arctic-north-america': 'Arctic North America US Canada geopolitics',
    'global-south':         'Global South developing nations geopolitics diplomacy',
}

def fetch_news(query='Global South geopolitics', page=1, page_size=12):
    api_key = settings.NEWS_API_KEY
    if not api_key or api_key == 'your_newsapi_key_here':
        return get_fallback_news(query)
    try:
        url = f"{settings.NEWS_API_BASE_URL}everything"
        params = {
            'q': query, 'apiKey': api_key, 'language': 'en',
            'sortBy': 'publishedAt', 'page': page, 'pageSize': page_size,
        }
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        if data.get('status') == 'ok':
            articles = []
            for a in data.get('articles', []):
                if a.get('title') and a.get('title') != '[Removed]':
                    articles.append({
                        'title': a.get('title', ''),
                        'description': a.get('description', '') or '',
                        'url': a.get('url', '#'),
                        'image': a.get('urlToImage') or '/static/images/news-placeholder.svg',
                        'source': a.get('source', {}).get('name', 'Unknown'),
                        'author': a.get('author', '') or 'GSO Staff',
                        'published_at': a.get('publishedAt', ''),
                    })
            return {'articles': articles, 'total': data.get('totalResults', 0), 'success': True}
        return get_fallback_news(query)
    except Exception:
        return get_fallback_news(query)

def fetch_top_headlines(page_size=4):
    api_key = settings.NEWS_API_KEY
    if not api_key or api_key == 'your_newsapi_key_here':
        return get_fallback_news('global news')
    try:
        url = f"{settings.NEWS_API_BASE_URL}everything"
        params = {
            'q': 'Global South geopolitics diplomacy security',
            'apiKey': api_key, 'language': 'en',
            'sortBy': 'publishedAt', 'pageSize': page_size,
        }
        r = requests.get(url, params=params, timeout=10)
        r.raise_for_status()
        data = r.json()
        if data.get('status') == 'ok':
            articles = []
            for a in data.get('articles', []):
                if a.get('title') and a.get('title') != '[Removed]':
                    articles.append({
                        'title': a.get('title', ''),
                        'description': a.get('description', '') or '',
                        'url': a.get('url', '#'),
                        'image': a.get('urlToImage') or '/static/images/news-placeholder.svg',
                        'source': a.get('source', {}).get('name', 'Unknown'),
                        'author': a.get('author', '') or 'GSO Staff',
                        'published_at': a.get('publishedAt', ''),
                    })
            return {'articles': articles, 'success': True}
        return get_fallback_news('global news')
    except Exception:
        return get_fallback_news('global news')

def get_category_query(category):
    return CATEGORY_QUERIES.get(category, 'Global South geopolitics diplomacy')

def get_fallback_news(query=''):
    articles = [
        {'title': 'Global South Nations Present Unified Stand at UN General Assembly',
         'description': 'Representatives from over 80 developing nations convened to present a unified position on UN Security Council reform and climate financing.',
         'url': '#', 'image': '/static/images/news-placeholder.svg',
         'source': 'Global South Observer', 'author': 'GSO Editorial Team', 'published_at': '2025-08-15T09:00:00Z'},
        {'title': 'BRICS Expansion Reshapes Global Economic Architecture',
         'description': 'The expanded BRICS bloc signals a fundamental shift in global economic governance as emerging economies seek alternatives to Bretton Woods institutions.',
         'url': '#', 'image': '/static/images/news-placeholder.svg',
         'source': 'Global South Observer', 'author': 'Research Desk', 'published_at': '2025-08-14T11:30:00Z'},
        {'title': 'Indo-Pacific Security: Regional Powers Navigate Complex Alliances',
         'description': 'Australia, Japan, and India deepen security cooperation amid growing maritime tensions in the Indo-Pacific.',
         'url': '#', 'image': '/static/images/news-placeholder.svg',
         'source': 'Global South Observer', 'author': 'Security Analyst', 'published_at': '2025-08-13T08:15:00Z'},
        {'title': 'African Union Launches Continental Free Trade Zone Implementation Phase',
         'description': 'The AfCFTA enters a critical phase with 42 member states actively trading under the new framework.',
         'url': '#', 'image': '/static/images/news-placeholder.svg',
         'source': 'Global South Observer', 'author': 'Economics Correspondent', 'published_at': '2025-08-12T14:00:00Z'},
        {'title': 'Latin America Digital Diplomacy: A New Era of Technological Sovereignty',
         'description': 'Brazil, Mexico and Argentina lead an initiative for regional digital infrastructure independent of major power blocs.',
         'url': '#', 'image': '/static/images/news-placeholder.svg',
         'source': 'Global South Observer', 'author': 'Technology Editor', 'published_at': '2025-08-11T10:45:00Z'},
        {'title': 'South China Sea: ASEAN Seeks Binding Maritime Code of Conduct',
         'description': 'Southeast Asian nations intensify negotiations for a binding Code of Conduct, with the Philippines and Vietnam leading diplomatic efforts.',
         'url': '#', 'image': '/static/images/news-placeholder.svg',
         'source': 'Global South Observer', 'author': 'Diplomatic Affairs Editor', 'published_at': '2025-08-10T07:30:00Z'},
    ]
    return {'articles': articles, 'total': len(articles), 'success': False}
