
import sys

css = """
/* Extracted from index.html inline styles */
.nav-link {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 6px 12px;
  border-radius: 6px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: #fff;
  text-decoration: none;
  font-size: 12px;
  transition: 0.2s ease;
  white-space: nowrap;
}
.nav-link:hover {
  background: rgba(59, 130, 246, 0.2);
  border-color: #3b82f6;
}

.header-main-actions {
  display: flex; gap: 10px;
}
.header-main-actions a {
  text-decoration: none; display: inline-flex; align-items: center; justify-content: center; padding: 8px 15px; border-radius: 6px; font-size: 13px; font-weight: 600;
}
.header-main-actions a.primary {
  background: var(--button-bg); color: #fff;
}

.header-nav-actions {
  display: flex; flex-wrap: wrap; justify-content: flex-end; gap: 5px; width: 100%; margin-top: 5px; padding-top: 5px; border-top: 1px solid rgba(255,255,255,0.1);
}

.site-header#overview {
  display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 20px; padding: 40px 20px; flex-wrap: wrap; background: url('topbackground.jpg.webp') center/cover no-repeat; position: relative; border-radius: 24px; box-shadow: inset 0 0 100px rgba(0,0,0,0.5); overflow: hidden;
}

.hero-copy {
  flex: 1; width: 100%; max-width: 900px; text-align: center; position: relative; z-index: 1; margin: 0 auto;
}

.hero-copy .eyebrow {
  font-size: 14px; font-weight: 600; color: #8b5cf6; display: block; margin-bottom: 12px; letter-spacing: 1px; text-transform: uppercase;
}

.hero-copy h1 {
  line-height: 1.15; margin: 0 0 20px 0; font-weight: 800; color: #ffffff;
}

.hero-copy p.subtitle1 {
  font-size: 1.2rem; line-height: 1.6; margin: 0 auto 15px auto; color: #e2e8f0; max-width: 800px;
}

.hero-copy p.subtitle2 {
  font-size: 1rem; margin: 0 auto 25px auto; color: #a1a1aa; max-width: 600px;
}
"""

with open('style.css', 'a', encoding='utf-8') as f:
    f.write(css)


