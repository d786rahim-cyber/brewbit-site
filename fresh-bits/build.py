import json, html, sys, os
d = os.path.dirname(os.path.abspath(__file__))
data = json.load(open(os.path.join(d, "news.json"), encoding="utf-8"))
head = open(os.path.join(d, "head.html"), encoding="utf-8").read()
e = lambda s: html.escape(s, quote=True)

themes = "".join(f'<div class="theme"><b>Pattern {i}</b>{e(t)}</div>' for i, t in enumerate(data["themes"], 1))
secs = []
for s in data["sections"]:
    cards = "".join(
        f'<article class="card"><span class="when">{e(it["date"])}</span><h3>{e(it["head"])}</h3>'
        f'<p>{e(it["text"])}</p><a class="read" href="{e(it["url"])}">{e(it["src"])} →</a></article>'
        for it in s["items"])
    secs.append(f'<section id="{s["id"]}" data-cat="{s["id"]}"><p class="label">{e(s["title"])}</p>'
                f'<h2>{e(s["blurb"])}</h2><div class="news">{cards}</div></section>')
readers = "".join(f'<a href="{e(r["url"])}">{e(r["name"])}</a>' for r in data["readers"])

body = f'''<div class="page ">
<section class="page-hero">
  <p class="label">Fresh Bits</p>
  <h1>Freshly brewed tech news.</h1>
  <p class="lede">What is new in AI, cybersecurity and IT infrastructure, with links to the original reporting. I follow these areas every week because they shape the systems I run.</p>
  <div class="newsbar">
    <button class="chipbtn" type="button" data-c="all" aria-pressed="true">All</button>
    <button class="chipbtn" type="button" data-c="ai" aria-pressed="false">AI</button>
    <button class="chipbtn" type="button" data-c="cyber" aria-pressed="false">Cybersecurity</button>
    <button class="chipbtn" type="button" data-c="infra" aria-pressed="false">Infrastructure</button>
    <span class="updated">Updated {e(data["updated"])}</span>
  </div>
</section>
<section>
  <p class="label">This week at a glance</p>
  <div class="themes">{themes}</div>
</section>
{chr(10).join(secs)}
<section>
  <p class="label">Where I read</p>
  <div class="readers">{readers}</div>
  <p class="credit">Summaries are my own short notes. Follow each link for the full story. Some reports, such as attributions of attacks, come from a single source.</p>
</section>
<script>
(function(){{var btns=document.querySelectorAll('.chipbtn');var secs=document.querySelectorAll('section[data-cat]');
function show(c){{secs.forEach(function(s){{s.hidden=!(c==='all'||s.getAttribute('data-cat')===c);}});btns.forEach(function(b){{b.setAttribute('aria-pressed',b.getAttribute('data-c')===c?'true':'false');}});}}
btns.forEach(function(b){{b.addEventListener('click',function(){{show(b.getAttribute('data-c'));}});}});}})();
</script>
<footer class="site">© 2026 Daniel Rahim · Houston, Texas · brewbit.tech</footer>
</div>
</body>
</html>
'''
open(os.path.join(d, "..", "news.html"), "w", encoding="utf-8").write(head + body)
print("ok", sum(len(s["items"]) for s in data["sections"]), "stories")
