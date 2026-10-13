"""Build news.html (repo root) from fresh-bits/news.json and fresh-bits/head.html."""
import json, html, os, sys
d = os.path.dirname(os.path.abspath(__file__))
data = json.load(open(os.path.join(d, "news.json"), encoding="utf-8"))
head = open(os.path.join(d, "head.html"), encoding="utf-8").read()
e = lambda s: html.escape(str(s), quote=True)
DESKS = ["tech", "coffee", "cycling", "travel"]
ids = [x["id"] for x in data["desks"]]
assert ids == DESKS, f"desks must be {DESKS}, got {ids}"
seen = set()
for desk in data["desks"]:
    for s in desk["sections"]:
        for it in s["items"]:
            for k in ("date", "head", "text", "src", "url"):
                assert it.get(k), f"missing {k} in {it.get('head')}"
            assert it["url"].startswith(("http://", "https://")), it["url"]
            assert it["head"] not in seen, "duplicate headline: " + it["head"]
            seen.add(it["head"])

def row(it):
    return (f'<li class="row"><span class="when">{e(it["date"])}</span><div><b>{e(it["head"])}</b>'
            f'<p>{e(it["text"])}</p></div><a class="read" href="{e(it["url"])}">{e(it["src"])} →</a></li>')

def block(s):
    if s.get("style") == "list":
        return f'<ul class="rows">{"".join(row(i) for i in s["items"])}</ul>'
    return f'<div class="news n{len(s["items"])}">{"".join(card(i) for i in s["items"])}</div>'

def card(it):
    return (f'<article class="card"><span class="when">{e(it["date"])}</span><h3>{e(it["head"])}</h3>'
            f'<p>{e(it["text"])}</p><a class="read" href="{e(it["url"])}">{e(it["src"])} →</a></article>')

themes = "".join(
    f'<a class="theme t-{dk}" href="#{dk}" style="text-decoration:none;color:inherit"><b>{e(t["desk"])}</b>{e(t["text"])}</a>'
    for dk, t in zip(DESKS, data["themes"]))
desks = []
for desk in data["desks"]:
    subs = "".join(
        f'<div class="sub" id="{e(s["id"])}"><div class="sub-head"><h3>{e(s["title"])}</h3><span>{e(s.get("blurb",""))}</span></div>'
        f'{block(s)}</div>'
        for s in desk["sections"])
    links = ""
    if desk.get("links"):
        lt = {"cycling": "Where to buy and service", "travel": "Plan and book"}.get(desk["id"], "Worth bookmarking")
        links = (f'<div class="sub"><div class="sub-head"><h3>{lt}</h3></div><div class="links">'
                 + "".join(f'<a href="{e(l["url"])}"><b>{e(l["name"])} →</b><span>{e(l.get("note",""))}</span></a>' for l in desk["links"])
                 + '</div></div>')
    desks.append(f'<section class="desk desk-{desk["id"]}" id="{desk["id"]}" data-cat="{desk["id"]}">'
                 f'<div class="desk-head"><span class="kicker">{e(desk["kicker"])}</span><h2>{e(desk["title"])}</h2><p>{e(desk["blurb"])}</p></div>'
                 f'{subs}{links}</section>')
readers = "".join(f'<a href="{e(r["url"])}">{e(r["name"])}</a>' for r in data["readers"])
total = len(seen)
chips = "".join(f'<button class="chipbtn" type="button" data-c="{c}" aria-pressed="{"true" if c=="all" else "false"}">{n}</button>'
                for c, n in [("all","All"),("tech","Technology"),("coffee","Coffee"),("cycling","Cycling"),("travel","Travel")])
body = f'''<div class="page ">
<section class="page-hero">
  <p class="label">Fresh Bits</p>
  <h1>Freshly brewed news, every morning.</h1>
  <p class="lede">One page for what I follow: technology (AI, cybersecurity and infrastructure), coffee and roasting, cycling, and travel. Every story links to the original source, and the page refreshes daily.</p>
</section>
<div class="newsbar">{chips}<span class="updated">Updated {e(data["updated"])} · {total} stories</span></div>
<section>
  <p class="label">Today at a glance</p>
  <div class="themes">{themes}</div>
</section>
{chr(10).join(desks)}
<section>
  <p class="label">Where I read</p>
  <div class="readers">{readers}</div>
  <p class="credit">Summaries are my own short notes. Follow each link for the full story. Deals and prices change quickly, so confirm terms before booking or buying. Some reports come from a single source.</p>
</section>
<script>
(function(){{
var btns=[].slice.call(document.querySelectorAll('.chipbtn'));
var ids=['tech','coffee','cycling','travel'];
function mark(c){{btns.forEach(function(b){{b.setAttribute('aria-pressed',b.getAttribute('data-c')===c?'true':'false');}});}}
function go(c){{
  var el=c==='all'?document.querySelector('.page-hero'):document.getElementById(c);
  if(!el)return; mark(c);
  var off=0;if(c!=='all'){{var tb=document.querySelector('.topbar'),nb=document.querySelector('.newsbar');off=(tb?tb.offsetHeight:0)+(nb&&getComputedStyle(nb).position==='sticky'?nb.offsetHeight:0)+18;}}
  var top=el.getBoundingClientRect().top+window.pageYOffset-off;
  window.scrollTo({{top:top,behavior:'smooth'}});
  try{{history.replaceState(null,'',c==='all'?location.pathname:'#'+c);}}catch(e){{}}
}}
btns.forEach(function(b){{b.addEventListener('click',function(){{go(b.getAttribute('data-c'));}});}});
if('IntersectionObserver' in window){{
  var io=new IntersectionObserver(function(es){{es.forEach(function(en){{if(en.isIntersecting)mark(en.target.id);}});}},{{rootMargin:'-45% 0px -50% 0px'}});
  ids.forEach(function(i){{var el=document.getElementById(i);if(el)io.observe(el);}});
}}
var h=(location.hash||'').slice(1);if(ids.indexOf(h)>-1)setTimeout(function(){{go(h);}},50);
}})();
</script>
<footer class="site">© 2026 Daniel Rahim · Houston, Texas · brewbit.tech</footer>
</div>
</body>
</html>
'''
open(os.path.join(d, "..", "news.html"), "w", encoding="utf-8").write(head + body)
print("ok", total, "stories")
