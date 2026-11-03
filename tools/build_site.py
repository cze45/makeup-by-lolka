"""Pravi index.html za GitHub Pages iz table za računar (project/Racunar.dc.html).

Tabla je responzivna, pa jedna strana služi i za telefon. Šabloni ({{…}}, sc-for, sc-if) se popune
početnim stanjem, /_blob/ adrese se zamene fajlovima iz assets/, a logika table je prepisana u običan JS.
Pokreni iz korena repoa:  python tools/build_site.py
"""
import json, re, html
from pathlib import Path

root = Path(__file__).resolve().parent.parent
s = (root / 'project/Racunar.dc.html').read_text(encoding='utf-8')
blobs = json.loads((root / 'assets/blobs.json').read_text(encoding='utf-8'))

head = s[:s.index('</head>')]
head = head.replace('<script src="./support.js"></script>\n', '')
head = re.sub(r'<title>.*?</title>', '<title>Makeup by Lolka – šminkanje i kursevi šminkanja, Beograd</title>', head)
style = s[s.index('<helmet>') + 8:s.index('</helmet>')].strip()
assert style.startswith('<style>') and style.endswith('</style>')
style = style[7:-8].strip()
body = s[s.index('</helmet>') + 9:s.index('</x-dc>')]
# inline display:inline-flex sa platna bi pregazio sakrivanje dugmeta u zaglavlju na telefonu
INL = 'style="display: inline-flex; align-items: center; justify-content: center; gap: 8px"'
assert body.count(INL) == 1
body = body.replace(INL, 'style="align-items: center; justify-content: center; gap: 8px"')

# kursevi, isti podaci kao u renderVals() table
COURSES = [
    dict(key='Za sebe', name='Našminkaj se sama', ph='Fotografija: polaznica šminka sebe ispred ogledala', who='Za devojke koje žele da nauče da se šminkaju same.',
         facts=[('2 h 30 min', 0), ('Dve ili više: 65 € po osobi', 0)], known=1, price='80 €', priceNote='jedna osoba', cta='Prijavi se za kurs', src=''),
    dict(key='Za posao', name='Profesionalni bazni kurs', ph='Fotografija: polaznica radi šminku na modelu', who='Za one koje žele da se bave šminkanjem.',
         facts=[('5 dana', 0), ('Individualni pristup', 0), ('Rad 1 na 1 sa klijentima', 0)], known=1, price='350 €', priceNote='pet dana', cta='Prijavi se za kurs',
         src='/_blob/ba9395848187ee19adad1b8856c7a125'),
    dict(key='Za šminkere', name='Usavršavanje 1:1', ph='Fotografija: Lolka i šminkerka rade zajedno', who='Za šminkere koji već rade i žele sledeći nivo.',
         facts=[('Individualno, 1 na 1', 0), ('Trajanje', 1)], known=0, price='', priceNote='', cta='Pitaj za termin', src='')]
DECK = [
    dict(ph='Rad polaznice baznog kursa', src='/_blob/ba9395848187ee19adad1b8856c7a125', who='Polaznica baznog kursa'),
    dict(ph='Krupni kadar, bazna obuka', src='/_blob/c65366fdad6536fae8bed13e6d7c8377', who='Polaznica baznog kursa'),
    dict(ph='Rad polaznice baznog kursa', src='', who='Polaznica baznog kursa'),
    dict(ph='Šminka na modelu, bazna obuka', src='', who='Model, bazna obuka'),
    dict(ph='Video: kako izgleda grupni kurs', src='', who='Grupni kurs, reel')]
POS = {0: 'dcard d0', 1: 'dcard d1', -1: 'dcard dm1', 2: 'dcard d2', -2: 'dcard dm2'}


def ifs(t, flags, var):
    """Razreši <sc-if value="{{var.X}}"> prema flags[X]."""
    pat = r'<sc-if value="\{\{%s(\w+)\}\}"[^>]*>(.*?)</sc-if>' % (re.escape(var + '.') if var else '')
    return re.sub(pat, lambda m: m.group(2) if flags.get(m.group(1)) else '', t, flags=re.S)


def fill(t, vals, var):
    return re.sub(r'\{\{%s\.(\w+)\}\}' % var, lambda m: html.escape(str(vals.get(m.group(1), '')), quote=True), t)


def loop(t, name, render):
    a = t.index('<sc-for list="{{%s}}"' % name)
    b = t.index('</sc-for>', a)
    inner_start = t.index('>', a) + 1
    if name == 'courses':  # unutra je još jedan sc-for (facts), pa se zatvara tek drugi </sc-for>
        b = t.index('</sc-for>', b + 9)
    return t[:a] + render(t[inner_start:b]) + t[b + 9:]


def course(tpl, i, c):
    t = tpl
    fa = t.index('<sc-for list="{{c.facts}}"')
    fb = t.index('</sc-for>', fa)
    fi = t[t.index('>', fa) + 1:fb]
    t = t[:fa] + ''.join(fill(ifs(fi, {'tag': tag}, 'f'), {'t': txt}, 'f') for txt, tag in c['facts']) + t[fb + 9:]
    t = ifs(t, {'hasImg': c['src'], 'noImg': not c['src'], 'known': c['known'], 'unknown': not c['known'], 'hasGrp': 0}, 'c')
    return fill(t, dict(c, cls='crs', hid='a-crs-h-%d' % i), 'c')


def card(tpl, i, d):
    n = len(DECK)
    k = i if i <= 2 else i - n
    t = ifs(tpl, {'hasImg': d['src'], 'noImg': not d['src']}, 'd')
    return fill(t, dict(d, cls=POS[k], cur='true' if k == 0 else 'false', aria='%d od %d: %s' % (i + 1, n, d['who'])), 'd')


body = loop(body, 'courses', lambda tpl: ''.join(course(tpl, i, c) for i, c in enumerate(COURSES)))
body = loop(body, 'deck', lambda tpl: ''.join(card(tpl, i, d) for i, d in enumerate(DECK)))
body = ifs(body, {'menuOpen': 0, 'menuClosed': 1, 'mqPlaying': 1, 'mqPaused': 0}, '')
body = re.sub(r'\s+on[A-Z]\w*="\{\{[^}]*\}\}"', '', body)  # događaje kači skripta ispod
START = dict(accent='#6E1A2B', mnavCls='mnav', menuLabel='Otvori meni', menuExpanded='false', mqCls='mqs', mqPaused='false',
             mqLabel='Pauziraj utiske', snapCls='', cmp='50', cmpTxt='Prvi dan levo, peti dan desno', deckPos='1 / %d' % len(DECK))
body = re.sub(r'\{\{(\w+)\}\}', lambda m: START[m.group(1)], body)
assert '{{' not in body and '<sc-' not in body, 'ostao je nerazrešen šablon'

page = head + '<style>\n' + style + '\n</style>\n</head>\n<body>' + body + '<script src="assets/sajt.js" defer></script>\n</body>\n</html>\n'
page = re.sub(r'/_blob/[0-9a-f]{32}', lambda m: blobs[m.group(0)], page)
(root / 'index.html').write_text(page, encoding='utf-8')
print('index.html', len(page))
