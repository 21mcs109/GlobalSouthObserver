# 🌐 The Global South Observer
**Voice of Global South** — Academic Research | Leadership Training | Political Consultancy | News Analysis

## Quick Start (3 commands)
```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```
Open → **http://127.0.0.1:8000**

## Full Setup
```bash
# 1. Create virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Migrate database
python manage.py makemigrations
python manage.py migrate

# 4. Create admin user
python manage.py createsuperuser

# 5. Seed sample data (podcasts, internships, advisory board)
python manage.py seed_data

# 6. Run server
python manage.py runserver
```

## NewsAPI Key (already set)
The API key `16028ee041dd4f37ba9c619ea1ee9a08` is pre-configured in `settings.py`.
To change it, edit `globalsouthobserver/settings.py` → `NEWS_API_KEY`.

## Social Media Links (configured)
- Email: contactglobalsouthobserver@gmail.com
- YouTube: https://www.youtube.com/@GlobalSouthObserver-z4y
- LinkedIn: https://www.linkedin.com/groups/40128007/
- Instagram: https://www.instagram.com/globalsouthobserver/
- X (Twitter): https://x.com/globalsouthobsr
- WhatsApp: https://chat.whatsapp.com/C6cLmw72c8KI2cx3gUOkaT

## Admin Panel
URL: http://127.0.0.1:8000/admin/

## Pages & Sub-navs
| Page | Sub-nav Sections |
|---|---|
| About Us | About Us, Who We Are, What We Offer, Terms, Privacy, Third Party, Subscription & Refund |
| Leadership | Founder Column, Editorial Board, Advisory Board, Research Fellows |
| News Updates | Global South, Indo-Pacific, South Asia, South East Asia, Africa & Latin America, Europe & Middle East, Arctic & North America |
| Research Internship | Certificate Courses, Leadership Programs, Seminars & Workshops |
| Political Consultancy | Political Research, Social Media & Communication, Election Strategy, Election Survey |
| Subscribe Us | Membership, Research Archive, Journal, Policy Documents, Annual Reports |
| Contact Us | Write for Us, Email ID, Website Link, Social Media |
