# Build static site: python3 _build/build.py  (run from repo root)
import os,json,html,sys
sys.path.insert(0,os.path.dirname(__file__))
from content import *
OUT=os.path.abspath(os.path.join(os.path.dirname(__file__),'..'))
BASE='https://xingjii.com'
PAGES=[]
def P(lang,path): return ('/zh/' if lang=='zh' else '/')+path
def esc(s): return html.escape(s,quote=True)
def badge(lang,aid,cls=''):
  t=T[lang];b=t['badge']
  return (f'<a class="mas mas-img {cls}" href="https://apps.apple.com/{t["store"]}/app/id{aid}" rel="noopener">'
   f'<img class="on-light" src="/assets/badges/badge-black-{b}.svg" alt="{t["badge_alt"]}" width="{156 if lang=="en" else 140}" height="40">'
   f'<img class="on-dark" src="/assets/badges/badge-white-{b}.svg" alt="" aria-hidden="true" width="{156 if lang=="en" else 140}" height="40"></a>')
def icon(s,size=64,cls='icon',alt=''):
  return f'<img class="{cls}" src="/assets/icons/{s}-256.webp" srcset="/assets/icons/{s}-128.webp 128w, /assets/icons/{s}-256.webp 256w" sizes="{size}px" alt="{esc(alt)}" width="{size}" height="{size}" loading="lazy">'
class F:
  def __init__(s): s.items=[]
  def __call__(s,items):
    s.items+=items
    return '<div class="faq">'+''.join(f'<details><summary>{q}</summary><div class="a"><p>{a}</p></div></details>' for q,a in items)+'</div>'
  def ld(s):
    if not s.items: return ''
    d={"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in s.items]}
    return '<script type="application/ld+json">'+json.dumps(d,ensure_ascii=False)+'</script>'
def page(lang,path,title,desc,body,head='',faq=None,noindex=False):
  t=T[lang]; en=P('en',path); zh=P('zh',path); me=P(lang,path); other=zh if lang=='en' else en
  nav_l=[P(lang,'#apps') if path=='' else P(lang,'')+'#apps',P(lang,'')+'#guides',P(lang,'support/'),P(lang,'privacy/')]
  nav=''.join(f'<li><a href="{h}">{n}</a></li>' for n,h in zip(t['nav'],nav_l))
  sw=f'<div class="lang" role="group" aria-label="{t["lang_label"]}"><a href="{en}" hreflang="en" lang="en"{" aria-current=page" if lang=="en" else ""}>EN</a><a href="{zh}" hreflang="zh-Hans" lang="zh-Hans"{" aria-current=page" if lang=="zh" else ""}>中文</a></div>'
  fa=''.join(f'<li><a href="{P(lang,"apps/"+s+"/")}">{APPS[s]["short"]}</a></li>' for s in ORDER)+f'<li><span>{t["soon_name"]} · {t["soon"]}</span></li>'
  alt='' if noindex else f'<link rel="canonical" href="{BASE}{me}"><link rel="alternate" hreflang="en" href="{BASE}{en}"><link rel="alternate" hreflang="zh-Hans" href="{BASE}{zh}"><link rel="alternate" hreflang="x-default" href="{BASE}{en}">'
  h=f'''<!doctype html>
<html lang="{'zh-Hans' if lang=='zh' else 'en'}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title><meta name="description" content="{esc(desc)}">{'<meta name="robots" content="noindex">' if noindex else ''}
<meta name="theme-color" content="#ffffff" media="(prefers-color-scheme: light)"><meta name="theme-color" content="#000000" media="(prefers-color-scheme: dark)">
{alt}<meta property="og:type" content="website"><meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}"><meta property="og:url" content="{BASE}{me}">
<link rel="icon" type="image/svg+xml" href="/favicon.svg"><link rel="stylesheet" href="/assets/style.css"><script src="/assets/site.js" defer></script>{head}{faq.ld() if faq else ''}</head><body>
<div class="langbar" role="status">{t['langbar']} <a href="{other}">{t['langbar_go']}</a> · <button type="button" style="background:none;border:0;color:var(--text-2);cursor:pointer;font:inherit">{t['close']}</button></div>
<header class="nav"><div class="wrap"><a class="brand" href="{P(lang,'')}"><span class="brand-mark"></span>{t['studio']}</a>
<button class="menu-btn" type="button" aria-label="Menu" aria-expanded="false" aria-controls="nl">☰</button><ul class="nav-links" id="nl">{nav}</ul>{sw}</div></header>
<main>{body}</main>
<footer><div class="wrap"><div class="foot"><div><a class="brand" href="{P(lang,'')}"><span class="brand-mark"></span>{t['studio']}</a><p style="margin-top:12px;max-width:320px">{t['tagline']}</p></div>
<div><h4>{t['foot_apps']}</h4><ul>{fa}</ul></div><div><h4>{t['foot_res']}</h4><ul><li><a href="{P(lang,'')}#guides">{t['nav'][1]}</a></li><li><a href="{P(lang,'support/')}">{t['nav'][2]}</a></li><li><a href="{P(lang,'privacy/')}">{t['nav'][3]}</a></li></ul></div>
<div><h4>{t['contact']}</h4><ul><li><a href="mailto:{EMAIL}">{EMAIL}</a></li></ul></div></div>
<div class="foot-bottom"><span>© 2026 {t['studio']}. {t['rights']}</span>{sw}</div></div></footer></body></html>
'''
  fn=os.path.join(OUT,me.lstrip('/'),'index.html') if not path.endswith('.html') else os.path.join(OUT,me.lstrip('/'))
  os.makedirs(os.path.dirname(fn),exist_ok=True); open(fn,'w').write(h)
  if not noindex: PAGES.append(me)

for L in ('en','zh'):
  t=T[L]; st=t['studio']
  # ---- home
  cards=''
  for s in ORDER:
    a=A[s][L]; n=APPS[s]['name'][L]
    cards+=f'<article class="card"><div class="card-head">{icon(s,64,alt=n+" icon")}<div><h3>{n}</h3><p class="muted" style="font-size:15px">{a["card"]}</p></div></div><ul>{"".join(f"<li>{p}</li>" for p in a["pts"])}</ul><div class="card-foot">{badge(L,APPS[s]["id"])}<a href="{P(L,"apps/"+s+"/")}">{t["more"]}</a></div></article>'
  cards+=f'<article class="card soon" aria-label="{t["soon"]}"><div class="card-head"><div class="icon icon-ph" style="width:64px;height:64px">?</div><div><h3>{t["soon_name"]}</h3><p class="muted" style="font-size:15px">{t["soon_desc"]}</p></div></div><div class="card-foot"><span class="badge-soon">{t["soon"]}</span><span class="tag">{t["soon_note"]}</span></div></article>'
  TASK={'en':{'compressbox':('🗜️','Compress images','Shrink a folder of photos or screenshots before sharing or uploading.'),'imagerenamer':('🏷️','Batch rename images','Give hundreds of files clean, ordered names without touching originals.'),'cloudbridge':('🖥️','Get files from a server','Preview and download files from your VPS, NAS or SFTP server.')},
        'zh':{'compressbox':('🗜️','压缩图片','分享或上传前，把一整个文件夹的照片、截图变小。'),'imagerenamer':('🏷️','批量重命名图片','给几百个文件起整齐有序的名字，原文件不动。'),'cloudbridge':('🖥️','从服务器取文件','预览并下载 VPS、NAS 或 SFTP 服务器上的文件。')}}[L]
  TO=['compressbox','imagerenamer','cloudbridge']
  tasks=''.join(f'<div class="task"><div class="emoji" aria-hidden="true">{TASK[s][0]}</div><h3>{TASK[s][1]}</h3><p>{TASK[s][2]}</p><div class="links"><a href="{P(L,"apps/"+s+"/")}">{t["open_app"].format(APPS[s]["short"])}</a><a href="{P(L,"guides/"+APPS[s]["guide"]+"/")}">{t["read_guide"].format(G[APPS[s]["guide"]][L]["t"])}</a></div></div>' for s in TO)
  guides=''.join(f'<a class="guide" href="{P(L,"guides/"+APPS[s]["guide"]+"/")}"><span class="tag">{APPS[s]["short"]}</span><h3>{G[APPS[s]["guide"]][L]["t"]}</h3><span class="more">{t["read"]}</span></a>' for s in TO)
  prom=''.join(f'<div><div class="ico" aria-hidden="true">{e}</div><h3>{h}</h3><p>{p}</p></div>' for e,h,p in t['promise'])
  body=f'''<section class="hero"><div class="wrap"><div class="hero-icons">{''.join(icon(s,72,cls='icon') for s in ORDER)}<div class="icon-ph" aria-hidden="true">?</div></div>
<div class="pill">{t['localpill']}</div><h1>{t['tagline']}</h1><p class="lead">{t['lead']}</p><a class="btn" href="#apps">{t['browse']}</a></div></section>
<section id="apps" class="alt"><div class="wrap"><div class="center" style="margin-bottom:48px"><h2>{t['apps_h']}</h2><p class="lead">{t['apps_lead']}</p></div><div class="grid">{cards}</div></div></section>
<section id="tasks"><div class="wrap center"><h2>{t['task_h']}</h2><p class="lead">{t['task_lead']}</p></div><div class="wrap"><div class="tasks">{tasks}</div></div></section>
<section id="guides" class="alt"><div class="wrap center"><h2>{t['guides_h']}</h2><p class="lead">{t['guides_lead']}</p></div><div class="wrap"><div class="guides">{guides}</div></div></section>
<section id="privacy"><div class="wrap center"><h2>{t['promise_h']}</h2><p class="lead">{t['promise_lead']}</p></div><div class="wrap"><div class="promise">{prom}</div></div></section>'''
  page(L,'',f'{st} – {"Focused Mac tools" if L=="en" else "专注的 Mac 小工具"}',t['lead'],body)
  # ---- app pages
  for s in ORDER:
    ap=APPS[s]; a=A[s][L]; n=ap['name'][L]; f=F(); g=G[ap['guide']][L]
    shots=''.join(f'<img src="/assets/shots/{s}-{k}.webp" alt="{ap["short"]} screenshot {k}" width="1280" height="800" loading="lazy">' for k in range(1,5))
    fe=''.join(f'<div><div class="promise"><div class="ico" aria-hidden="true" style="margin:0">{e}</div></div><h3 style="margin-top:16px">{h}</h3><p>{p}</p></div>' for e,h,p in a['feats'])
    body=f'''<section class="app-hero"><div class="wrap">{icon(s,160,alt=n+" icon")}<div>
<p class="crumbs"><a href="{P(L,'')}#apps">{t['nav'][0]}</a> › {ap['short']}</p><h1>{n}</h1><p class="lead" style="margin-top:8px">{a['sub']}</p>
<div class="app-cta">{badge(L,ap['id'])}<span class="pill" style="margin:0">🔒 {a['pill']}</span></div>
<div class="meta"><span>🖥 {ap['os'][L]}</span><span>⚙️ <span class="ph">{t['chip']}</span></span><span>💲 {t['price']}</span><span>📦 {ap['size']}</span></div>
<p class="subnav"><a href="{P(L,'apps/'+s+'/support/')}">{t['support']}</a><a href="{P(L,'apps/'+s+'/privacy/')}">{t['privacy']}</a></p></div></div></section>
<div class="shots" tabindex="0" role="region" aria-label="Screenshots">{shots}</div>
<section><div class="wrap"><p class="lead" style="max-width:760px">{a['lead']}</p><h2 style="margin-top:64px">{t['feat_h']}</h2><div class="features">{fe}</div></div></section>
<section class="alt"><div class="wrap two"><div><h2>{t['who_h']}</h2><ul class="check">{''.join(f'<li>{w}</li>' for w in a['who'])}</ul></div><div class="card"><h3>🔒 {t['priv_h']}</h3><ul>{''.join(f'<li>{w}</li>' for w in a['priv'])}</ul><a href="{P(L,'apps/'+s+'/privacy/')}">{t['see_privacy']}</a></div></div></section>
<section><div class="wrap two"><div><h2>{t['faq_h']}</h2>{f(a['faq'])}<p style="margin-top:24px"><a href="{P(L,'apps/'+s+'/support/')}">{t['see_support']}</a></p></div><div><p class="eyebrow">{t['related']}</p><a class="guide" style="margin-top:16px" href="{P(L,'guides/'+ap['guide']+'/')}"><h3>{g['t']}</h3><span class="more">{t['read']}</span></a></div></div></section>'''
    page(L,f'apps/{s}/',f'{n} | {st}',a['lead'],body,head=f'<meta name="apple-itunes-app" content="app-id={ap["id"]}">',faq=f)
    # support
    f=F(); secs=''
    for h,ps in SUP[s][L]:
      if ps=='FAQ': secs+=f'<h2>{h}</h2>'+f(a['faq']); continue
      secs+=f'<h2>{h}</h2>'+''.join(ps)
    body=f'''<article class="article" style="max-width:860px"><p class="crumbs"><a href="{P(L,'apps/'+s+'/')}">{ap['short']}</a> › {t['support']}</p><h1 style="margin-top:16px">{t['app_support'].format(ap['short'])}</h1><p class="lead">{a['sub']}</p>
<div class="contact"><div style="flex:1;min-width:220px"><p class="eyebrow">{t['email_pending']}</p><h3 style="margin-top:6px">{EMAIL}</h3><p class="muted" style="margin:4px 0 0">{t['reply']}</p></div><a class="btn" href="mailto:{EMAIL}?subject={ap['short']}%20Support">{t['email_btn']}</a></div>
{secs}<div class="callout"><h3>{t['bug_h']}</h3><p class="muted">{t['bug']}</p></div>
<p class="subnav"><a href="{P(L,'apps/'+s+'/privacy/')}">{t['app_privacy'].format(ap['short'])}</a><a href="https://apps.apple.com/{t['store']}/app/id{ap['id']}" rel="noopener">App Store</a></p></article>'''
    page(L,f'apps/{s}/support/',f'{t["app_support"].format(ap["short"])} | {st}',a['sub'],body,faq=f)
    # privacy
    pv=PRIV[s]; secs=''.join((f'<h2>{h}</h2>' if h else '')+p.replace('{E}',EMAIL) for h,p in pv[L])
    body=f'''<article class="article legal"><p class="crumbs"><a href="{P(L,'apps/'+s+'/')}">{ap['short']}</a> › {t['privacy']}</p><h1 style="margin-top:16px">{t['app_privacy'].format(ap['short'])}</h1><p class="muted">{t['last'].format(pv['date'][L])}</p>{secs}
<p class="subnav"><a href="{P(L,'apps/'+s+'/support/')}">{t['back_support']}</a><a href="{P(L,'privacy/')}">{t['p_h']}</a></p></article>'''
    page(L,f'apps/{s}/privacy/',f'{t["app_privacy"].format(ap["short"])} | {st}',a['priv'][0],body)
  # ---- guides
  for slug,gd in G.items():
    s=gd['app']; ap=APPS[s]; g=gd[L]; f=F()
    steps=''
    for k,(h,p,shot) in enumerate(g['steps'],1):
      body_p=p if p.startswith('<') else f'<p class="muted">{p}</p>'
      fig=f'<figure><img src="/assets/shots/{s}-{shot}.webp" alt="{esc(h)}" width="1280" height="800" loading="lazy"><figcaption>{h}</figcaption></figure>' if shot else ''
      steps+=f'<li><h3>{h}</h3>{body_p}{fig}</li>'
    body=f'''<article class="article"><p class="crumbs"><a href="{P(L,'')}#guides">{t['breadcrumb_g']}</a> › {ap['short']}</p><p class="tag" style="margin-top:24px">{t['g_tag'].format(ap['short'],gd['mins'])}</p><h1>{g['t']}</h1><p class="lead">{g['intro']}</p>
<ol>{steps}</ol><div class="callout">{g['callout']}</div>
<h2>{t['faq_h']}</h2>{f(A[s][L]['faq'][:3])}
<div class="cta-box">{icon(s,56)}<div style="flex:1;min-width:200px"><h3>{t['try_app'].format(ap['name'][L])}</h3><p class="muted">{g['cta']}</p></div>{badge(L,ap['id'])}</div>
<p class="muted" style="font-size:14px;margin-top:24px">{t['g_updated']}</p></article>'''
    page(L,f'guides/{slug}/',f'{g["t"]} | {st}',g['intro'],body,faq=f)
  # ---- hubs
  f=F(); grp=''
  for s in ORDER:
    ap=APPS[s]
    grp+=f'<h2 id="{s}" style="display:flex;align-items:center;gap:12px">{icon(s,40)}{ap["name"][L]}</h2>{f(A[s][L]["faq"][:2])}<p class="subnav"><a href="{P(L,"apps/"+s+"/support/")}">{t["app_support"].format(ap["short"])} →</a><a href="{P(L,"apps/"+s+"/privacy/")}">{t["privacy"]}</a><a href="https://apps.apple.com/{t["store"]}/app/id{ap["id"]}" rel="noopener">App Store</a></p>'
  body=f'''<article class="article" style="max-width:860px"><h1>{t['s_h']}</h1><p class="lead">{t['s_lead']}</p>
<div class="contact"><div style="flex:1;min-width:220px"><p class="eyebrow">{t['email_pending']}</p><h3 style="margin-top:6px">{EMAIL}</h3><p class="muted" style="margin:4px 0 0">{t['reply']}</p></div><a class="btn" href="mailto:{EMAIL}">{t['email_btn']}</a></div>
<div class="callout"><h3>{t['bug_h']}</h3><p class="muted">{t['bug']}</p></div>{grp}</article>'''
  page(L,'support/',f'{t["s_h"]} | {st}',t['s_lead'],body,faq=f)
  items=''.join(f'<h2 id="{s}">{APPS[s]["name"][L]}</h2><p>{A[s][L]["priv"][0]}{"; " if L=="en" else "；"}{A[s][L]["priv"][1]}{"." if L=="en" else "。"}</p><p><a href="{P(L,"apps/"+s+"/privacy/")}">{t["app_privacy"].format(APPS[s]["short"])} →</a> <span class="muted">({t["last"].format(PRIV[s]["date"][L])})</span></p>' for s in ORDER)
  body=f'''<article class="article legal"><h1>{t['p_h']}</h1><p class="lead" style="margin-top:24px">{t['p_lead']}</p>
<nav class="toc"><a href="#summary">{'Summary' if L=='en' else '概要'}</a>{''.join(f' · <a href="#{s}">{APPS[s]["short"]}</a>' for s in ORDER)}</nav>
<h2 id="summary">{'Summary' if L=='en' else '概要'}</h2><p>{t['p_summary']}</p>{items}
<h2>{'Contact' if L=='en' else '联系我们'}</h2><p><a href="mailto:{EMAIL}">{EMAIL}</a></p></article>'''
  page(L,'privacy/',f'{t["p_h"]} | {st}',t['p_lead'],body)
  # ---- 404
  body=f'<section class="hero"><div class="wrap"><h1>{t["nf_h"]}</h1><p class="lead">{t["nf_p"]}</p><a class="btn" href="{P(L,"")}">{t["nf_home"]}</a></div></section>'
  page(L,'404.html',f'{t["nf_h"]} | {st}',t['nf_p'],body,noindex=True)

# old guide slugs -> new (redirect stubs)
for slug,gd in G.items():
  fn=os.path.join(OUT,'guides',gd['old']+'.html'); new=f'/guides/{slug}/'
  open(fn,'w').write(f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Moved</title><meta name="robots" content="noindex"><link rel="canonical" href="{BASE}{new}"><meta http-equiv="refresh" content="0; url={new}"></head><body><p><a href="{new}">This guide has moved.</a></p></body></html>\n')
# sitemap with hreflang
def pair(u): return u[3:] and '/'+u[4:] if u.startswith('/zh/') else u
sm=['<?xml version="1.0" encoding="UTF-8"?>','<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
for u in PAGES:
  en=u[3:] if u.startswith('/zh/') else u; zh='/zh'+en
  sm.append(f'<url><loc>{BASE}{u}</loc><lastmod>2026-10-15</lastmod><xhtml:link rel="alternate" hreflang="en" href="{BASE}{en}"/><xhtml:link rel="alternate" hreflang="zh-Hans" href="{BASE}{zh}"/><xhtml:link rel="alternate" hreflang="x-default" href="{BASE}{en}"/></url>')
sm.append('</urlset>'); open(os.path.join(OUT,'sitemap.xml'),'w').write('\n'.join(sm)+'\n')
open(os.path.join(OUT,'robots.txt'),'w').write(f'User-agent: *\nAllow: /\n\nSitemap: {BASE}/sitemap.xml\n')
open(os.path.join(OUT,'CNAME'),'w').write('xingjii.com\n')
print(len(PAGES),'pages')
