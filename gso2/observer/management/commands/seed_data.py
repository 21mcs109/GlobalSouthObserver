from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from observer.models import Podcast, Internship, AdvisoryMember

class Command(BaseCommand):
    help = 'Seed sample data'
    def handle(self, *args, **kwargs):
        self.seed_podcasts(); self.seed_internships(); self.seed_advisory()
        self.stdout.write(self.style.SUCCESS('✅ Sample data seeded!'))

    def seed_podcasts(self):
        items = [
            {'title':'Indo-Pacific Security: Regional Dynamics Explored','description':'Expert conversation on QUAD, AUKUS, and shifting security architectures in the Indo-Pacific region.','youtube_url':'https://www.youtube.com/@GlobalSouthObserver-z4y','published_at':timezone.now()-timedelta(days=7),'is_featured':True},
            {'title':'BRICS & Global South Diplomacy: New World Order','description':'Analysis of how the expanded BRICS bloc reshapes global governance and economic institutions.','youtube_url':'https://www.youtube.com/@GlobalSouthObserver-z4y','published_at':timezone.now()-timedelta(days=14),'is_featured':True},
            {'title':'Africa Rising: AfCFTA and Continental Integration','description':'Deep dive into the African Continental Free Trade Area and its transformative potential.','youtube_url':'https://www.youtube.com/@GlobalSouthObserver-z4y','published_at':timezone.now()-timedelta(days=21),'is_featured':False},
        ]
        for i in items:
            Podcast.objects.get_or_create(title=i['title'], defaults=i)
        self.stdout.write(f'  ✓ {len(items)} podcasts seeded')

    def seed_internships(self):
        items = [
            {'title':'Geopolitics Research Intern','department':'Research Division','description':'Assist senior analysts in tracking geopolitical developments and drafting policy briefs on Global South affairs.','eligibility':'Final-year undergraduates or postgraduates in political science, international relations or related fields.','duration':'3_months','benefits':'Certificate, letter of recommendation, publication opportunity, senior researcher mentorship.','is_open':True},
            {'title':'Editorial & Media Intern','department':'Communications','description':'Support the editorial team in research writing, fact-checking, social media strategy and multimedia content.','eligibility':'Students in journalism, communications, or political science with strong writing skills.','duration':'2_months','benefits':'Editorial bylines, portfolio building, certificate, mentorship from senior editors.','is_open':True},
            {'title':'Policy & Data Analyst Intern','department':'Policy Unit','description':'Analyse datasets on economic development, governance indicators, and security trends across Global South.','eligibility':'Students in economics, data science, public policy or social sciences with analytical skills.','duration':'3_months','benefits':'Hands-on research experience, certificate, mentorship, publication credit.','is_open':True},
        ]
        for i in items:
            Internship.objects.get_or_create(title=i['title'], defaults=i)
        self.stdout.write(f'  ✓ {len(items)} internships seeded')

    def seed_advisory(self):
        items = [
            {'name':'Prof. Anita Sharma','designation':'Professor of International Relations & Former Foreign Secretary','institution':'Jawaharlal Nehru University, New Delhi','research_area':'South Asian Security & India-China Relations','biography':'A leading authority on South Asian security with 30 years of diplomatic and academic experience.','order':1},
            {'name':'Dr. Kwame Asante','designation':'Senior Fellow & Director, Centre for African Governance','institution':'University of Ghana, Accra','research_area':'African Union Reforms & Pan-African Economics','biography':'Renowned expert in African institutional development and continental integration.','order':2},
            {'name':'Ambassador Maria Elena Vasquez','designation':'Former Ambassador to the United Nations','institution':'Latin American Policy Institute, Mexico City','research_area':'Latin American Diplomacy & Multilateralism','biography':'25 years in diplomatic service representing her country at the UN, OAS, and bilaterally across Europe and Asia.','order':3},
            {'name':'Prof. Li Wei','designation':'Professor of Political Economy & Director, Global South Studies Centre','institution':'Fudan University, Shanghai','research_area':'China-Global South Relations & Belt and Road Initiative','biography':'Foremost scholar on China\'s engagement with developing nations and the BRI.','order':4},
            {'name':'Dr. Fatima Al-Hassan','designation':'Climate Policy Specialist & Senior Research Fellow','institution':'Arab Institute for Strategic Studies, Cairo','research_area':'Climate Justice & Environmental Governance','biography':'Climate policy expert who has participated in all major UN Climate Conferences since 2010.','order':5},
            {'name':'Brigadier (Ret.) Rajiv Menon','designation':'Former Defence Attaché & Military Strategy Analyst','institution':'Institute for Defence Studies and Analyses, New Delhi','research_area':'Indo-Pacific Security & Modern Warfare Doctrine','biography':'32 years in the Indian Army, specialist in strategic deterrence and maritime security.','order':6},
        ]
        for i in items:
            AdvisoryMember.objects.get_or_create(name=i['name'], defaults=i)
        self.stdout.write(f'  ✓ {len(items)} advisory members seeded')
