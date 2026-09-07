'use strict';
document.addEventListener('DOMContentLoaded', () => {
  initNavbar();
  initBackToTop();
  initScrollAnimations();
  initAlertDismiss();
  initFooterSubscribe();
  initSubNavHighlight();
  initTickerDuplicate();
});

/* Hamburger + dropdowns */
function initNavbar() {
  const hamburger = document.getElementById('hamburger');
  const navList   = document.getElementById('nav-list');
  if (!hamburger || !navList) return;

  hamburger.addEventListener('click', () => {
    const open = navList.classList.toggle('open');
    hamburger.classList.toggle('open', open);
    hamburger.setAttribute('aria-expanded', String(open));
  });

  // Mobile: tap nav-link-main to toggle dropdown
  document.querySelectorAll('.nav-item.has-dropdown .nav-link-main').forEach(link => {
    link.addEventListener('click', e => {
      if (window.innerWidth <= 768) {
        e.preventDefault();
        link.closest('.nav-item').classList.toggle('mob-open');
      }
    });
  });

  // Close on outside click
  document.addEventListener('click', e => {
    if (!e.target.closest('.main-navbar')) {
      navList.classList.remove('open');
      hamburger.classList.remove('open');
      hamburger.setAttribute('aria-expanded', 'false');
    }
  });

  // Sticky shadow
  window.addEventListener('scroll', () => {
    document.querySelector('.main-navbar').style.boxShadow =
      window.scrollY > 40 ? '0 4px 20px rgba(0,0,0,.4)' : '';
  }, {passive: true});
}

/* Back to top */
function initBackToTop() {
  const btn = document.getElementById('back-to-top');
  if (!btn) return;
  window.addEventListener('scroll', () => btn.classList.toggle('visible', window.scrollY > 400), {passive:true});
  btn.addEventListener('click', () => window.scrollTo({top:0, behavior:'smooth'}));
}

/* Scroll animations */
function initScrollAnimations() {
  const els = document.querySelectorAll('[data-animate]');
  if (!els.length) return;
  const io = new IntersectionObserver(entries => {
    entries.forEach((entry, i) => {
      if (entry.isIntersecting) {
        const parent = entry.target.parentElement;
        const siblings = parent ? [...parent.querySelectorAll('[data-animate]')] : [];
        const idx = siblings.indexOf(entry.target);
        setTimeout(() => entry.target.classList.add('in-view'), idx * 70);
        io.unobserve(entry.target);
      }
    });
  }, {threshold: 0.1, rootMargin:'0px 0px -30px 0px'});
  els.forEach(el => io.observe(el));
}

/* Alert dismiss */
function initAlertDismiss() {
  document.querySelectorAll('.alert-close').forEach(btn => {
    btn.addEventListener('click', () => btn.closest('.alert')?.remove());
  });
  document.querySelectorAll('.alert').forEach(a => {
    setTimeout(() => { a.style.transition='opacity .4s'; a.style.opacity='0'; setTimeout(()=>a.remove(),400); }, 6000);
  });
}

/* Footer newsletter */
function initFooterSubscribe() {
  const form = document.getElementById('footer-subscribe-form');
  const msg  = document.getElementById('footer-nl-msg');
  if (!form) return;
  form.addEventListener('submit', async e => {
    e.preventDefault();
    const email = form.querySelector('input[name="email"]').value.trim();
    if (!email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      if(msg){ msg.textContent='Please enter a valid email.'; msg.className='nl-msg error'; }
      return;
    }
    const csrf = document.cookie.match(/csrftoken=([^;]+)/)?.[1] || '';
    try {
      const res = await fetch('/api/subscribe/', {
        method:'POST',
        headers:{'Content-Type':'application/x-www-form-urlencoded','X-CSRFToken':csrf},
        body:`email=${encodeURIComponent(email)}&csrfmiddlewaretoken=${encodeURIComponent(csrf)}`
      });
      const data = await res.json();
      if(msg){
        msg.textContent = data.success ? '✓ Subscribed successfully!' : (data.errors?.email?.[0] || 'Error, try again.');
        msg.className = 'nl-msg ' + (data.success ? 'success' : 'error');
      }
      if (data.success) form.reset();
    } catch { if(msg){ msg.textContent='Network error.'; msg.className='nl-msg error'; } }
  });
}

/* Sub-nav active highlight via IntersectionObserver */
function initSubNavHighlight() {
  const btns = document.querySelectorAll('.sub-nav-btn[data-target]');
  if (!btns.length) return;
  const sections = [...btns].map(b => document.getElementById(b.dataset.target)).filter(Boolean);
  const io = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        btns.forEach(b => b.classList.remove('active'));
        const active = document.querySelector(`.sub-nav-btn[data-target="${entry.target.id}"]`);
        if (active) active.classList.add('active');
      }
    });
  }, {threshold: 0.35, rootMargin:'-80px 0px -60% 0px'});
  sections.forEach(s => io.observe(s));

  // Smooth scroll on sub-nav click
  btns.forEach(btn => {
    btn.addEventListener('click', () => {
      const el = document.getElementById(btn.dataset.target);
      if (el) { const top = el.getBoundingClientRect().top + window.scrollY - 110; window.scrollTo({top, behavior:'smooth'}); }
    });
  });
}

/* Duplicate ticker items for seamless loop */
function initTickerDuplicate() {
  const ticker = document.querySelector('.ticker');
  if (ticker) ticker.innerHTML += ticker.innerHTML;
}

/* AJAX news category fetch (news page) */
window.fetchNewsByCategory = async function(category, page=1) {
  const grid    = document.getElementById('news-grid');
  const spinner = document.getElementById('news-spinner');
  if (!grid) return;
  spinner && (spinner.style.display='flex');
  grid.style.opacity='0.3';
  try {
    const res = await fetch(`/api/news/?category=${encodeURIComponent(category)}&page=${page}`);
    const data = await res.json();
    renderNewsGrid(grid, data.articles || []);
    history.pushState({}, '', `?category=${category}`);
  } catch {
    grid.innerHTML = '<div class="empty-state"><i class="bi bi-wifi-off"></i><p>Failed to load news. Please try again.</p></div>';
  } finally {
    spinner && (spinner.style.display='none');
    grid.style.opacity='1';
  }
};

function renderNewsGrid(grid, articles) {
  if (!articles.length) {
    grid.innerHTML = '<div class="empty-state"><i class="bi bi-newspaper"></i><p>No articles found for this category.</p></div>';
    return;
  }
  grid.innerHTML = articles.map(a => `
    <article class="news-card" data-animate>
      <div class="card-img-wrap">
        <img src="${a.image||'/static/images/news-placeholder.svg'}" alt="${esc(a.title)}" loading="lazy" onerror="this.src='/static/images/news-placeholder.svg'"/>
        <span class="card-source">${esc(a.source)}</span>
      </div>
      <div class="card-body">
        <h3 class="card-title"><a href="${a.url}" target="_blank" rel="noopener noreferrer">${esc(a.title)}</a></h3>
        <p class="card-desc">${esc((a.description||'').slice(0,130))}</p>
        <div class="card-meta">
          <span><i class="bi bi-person"></i> ${esc((a.author||'GSO Staff').slice(0,25))}</span>
          <span><i class="bi bi-calendar3"></i> ${(a.published_at||'').slice(0,10)}</span>
        </div>
        <a href="${a.url}" class="card-read-more" target="_blank" rel="noopener noreferrer">Read More <i class="bi bi-arrow-right"></i></a>
      </div>
    </article>`).join('');
}

function esc(str) {
  const d = document.createElement('div');
  d.textContent = str || '';
  return d.innerHTML;
}
