"""The home hero in the reader's time of day: dawn, day, dusk or night by the local hour, the same hours as the
radio's "On air" (assets/radio/stations.json, made by tools/make_radio.py from AIR). The page is static, so the
browser picks: a script in <head> sets html[data-tod] and preloads only that variant; the hero <picture> carries
data-srcset templates with {tod}, filled in by a tiny script right after it (the preload scanner fetches nothing extra).
Without JS the <noscript> copy shows dawn. Changing on an open page and the quiet switch live in assets/tod/tod.js."""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
PARTS = ['dawn', 'day', 'dusk', 'night']
RADIO = {'morning': 'dawn', 'day': 'day', 'evening': 'dusk', 'night': 'night'}
MOBILE_MEDIA = '(max-width: 719px) and (max-aspect-ratio: 2/3)'
MOBILE_W = (600, 800, 1000)   # phone cuts, tools/make_images.MOBILE_W
TEXT = {
    'ru': {'auto': 'по вашему времени', 'reset': 'По времени', 'label': 'Время суток'},
    'en': {'auto': 'by your local time', 'reset': 'Local time', 'label': 'Time of day'},
    'uk': {'auto': 'за вашим часом', 'reset': 'За часом', 'label': 'Час доби'},
    'de': {'auto': 'nach deiner Ortszeit', 'reset': 'Ortszeit', 'label': 'Tageszeit'},
    'fr': {'auto': 'selon votre heure', 'reset': 'Heure locale', 'label': 'Moment de la journée'},
    'es': {'auto': 'según tu hora', 'reset': 'Hora local', 'label': 'Momento del día'},
    'pt': {'auto': 'pelo seu horário', 'reset': 'Horário local', 'label': 'Período do dia'},
    'it': {'auto': 'secondo la tua ora', 'reset': 'Ora locale', 'label': 'Momento della giornata'},
    'pl': {'auto': 'według twojego czasu', 'reset': 'Czas lokalny', 'label': 'Pora dnia'},
}
# part(h) for an hour 0..23; B = bounds(). Kept as one string: tests run it in node against the radio's hours.
PART_JS = "function part(h){return h>=B[0]&&h<B[1]?'dawn':h>=B[1]&&h<B[2]?'day':h>=B[2]&&h<B[3]?'dusk':'night'}"


def _air():
    with open(os.path.join(HERE, 'assets', 'radio', 'stations.json'), encoding='utf-8') as f:
        return {RADIO[p['id']]: p for p in json.load(f)['air']}


def bounds():
    air = _air()
    return [air[t]['from'] for t in PARTS]


def names(lang):
    return {t: p['name'].get(lang) or p['name']['en'] for t, p in _air().items()}


def _set(root, name, widths, ext):
    return ', '.join(f'{root}assets/art/{name}-{w}.{ext} {w}w' for w in widths)


def _lqip(name, w):
    """A tiny blurred copy of a hero cut as a data URI: painted under the picture until the real one arrives (cold load)."""
    try:
        import base64, io
        from PIL import Image, ImageFilter
        with Image.open(os.path.join(HERE, 'assets', 'art', name)) as im:
            im = im.convert('RGB')
            im = im.resize((w, max(1, round(w * im.height / im.width))), Image.LANCZOS).filter(ImageFilter.GaussianBlur(.6))
            buf = io.BytesIO()
            im.save(buf, 'WEBP', quality=45, method=6)
        return 'data:image/webp;base64,' + base64.b64encode(buf.getvalue()).decode()
    except Exception:
        return ''


_LQ = {}


def lqip():
    """{tod: [wide, phone]} for the home hero (index.src.html .hero-art background)."""
    if not _LQ:
        for t in PARTS:
            _LQ[t] = [_lqip(f'hero_{t}-960.webp', 32), _lqip(f'hero_{t}-m-600.webp', 20)]
    return _LQ


def head_js(lang, root='@@ROOT@@', mobile=True, widths=(960, 1440, 1920, 2560, 3840), sizes='(max-aspect-ratio: 16/9) 180vh, 100vw', msizes='100vw', lq=False):
    pre = [['image/avif', 'not all and ' + MOBILE_MEDIA if mobile else '', _set(root, 'hero_{tod}', widths, 'avif'), sizes]]
    if mobile:
        pre.insert(0, ['image/avif', MOBILE_MEDIA, _set(root, 'hero_{tod}-m', MOBILE_W, 'avif'), msizes])
    data = {'B': bounds(), 'N': names(lang), 'X': TEXT[lang], 'A': pre}
    if lq:
        data['L'] = lqip()
    return ('<script>(function(){var D=' + json.dumps(data, ensure_ascii=False) + ',B=D.B,K="gabella-tod",P=["dawn","day","dusk","night"],d=document.documentElement;'
            + PART_JS + ';var q=(location.search.match(/[?&]tod=(dawn|day|dusk|night)\\b/)||[])[1],s=null;'
            'try{s=localStorage.getItem(K)}catch(e){}if(P.indexOf(s)<0)s=null;'
            'var t=q||s||part(new Date().getHours());d.setAttribute("data-tod",t);'
            'var L=D.L&&D.L[t];if(L&&L[0])d.style.setProperty("--lq","url("+L[0]+")"),d.style.setProperty("--lqm","url("+(L[1]||L[0])+")");'
            'window.GabellaTod={part:part,bounds:B,now:t,pinned:!!(q||s),url:!!q,key:K,names:D.N,text:D.X};'
            'D.A.forEach(function(a){var l=document.createElement("link");l.rel="preload";l.as="image";l.type=a[0];'
            'if(a[1])l.media=a[1];l.setAttribute("fetchpriority","high");l.setAttribute("imagesrcset",a[2].replace(/\\{tod\\}/g,t));'
            'l.setAttribute("imagesizes",a[3]);document.head.appendChild(l)})})();</script>\n')


def hero(root='@@ROOT@@', cls='hero-art', fx='dawn', mobile=True, widths=(960, 1440, 1920, 2560, 3840),
         sizes='(max-aspect-ratio: 16/9) 180vh, 100vw', img_w=1920, img_h=1072, msizes='100vw', amb=False):
    # msizes: the phone cut's width. The home band is the full screen width (aspect 600/768 on top), not 78vh tall
    def sources(name, attr):
        out = ''
        if mobile:
            for ext in ('avif', 'webp'):
                out += f'<source media="{MOBILE_MEDIA}" type="image/{ext}" {attr}="{_set(root, name + "-m", MOBILE_W, ext)}" sizes="{msizes}">'
        for ext in ('avif', 'webp'):
            out += f'<source type="image/{ext}" {attr}="{_set(root, name, widths, ext)}" sizes="{sizes}">'
        return out
    fxa = f' data-fx="{fx}" data-cut=".95"' if fx else ''   # data-cut: the phone cut, make_images.CUTS
    live = (f'<picture class="{cls}"{fxa} data-tod-art>{sources("hero_{tod}", "data-srcset")}'
            f'<img data-src="{root}assets/art/hero_{{tod}}-{img_w}.webp" width="{img_w}" height="{img_h}" alt="" fetchpriority="high" decoding="async"></picture>')
    fill = ('<script>(function(p,t){p.querySelectorAll("[data-srcset]").forEach(function(e){e.srcset=e.getAttribute("data-srcset").replace(/\\{tod\\}/g,t)});'
            'var i=p.querySelector("img");i.src=i.getAttribute("data-src").replace(/\\{tod\\}/g,t)})(document.currentScript.previousElementSibling,GabellaTod.now)</script>')
    still = (f'<noscript><picture class="{cls}">{sources("hero_dawn", "srcset")}'
             f'<img src="{root}assets/art/hero_dawn-{img_w}.webp" width="{img_w}" height="{img_h}" alt="" decoding="async"></picture></noscript>')
    ambi = ''
    if amb:   # ultrawide sides: the same scene, small and blurred (index.src.html .hero-amb); tod.js changes it with the hero
        ambi = ('<img class="hero-amb" data-tod-amb data-src="' + root + 'assets/art/hero_{tod}-960.webp" width="960" height="536" alt="" aria-hidden="true" loading="lazy" decoding="async">'
                '<script>(function(i,t){i.src=i.getAttribute("data-src").replace(/\\{tod\\}/g,t)})(document.currentScript.previousElementSibling,GabellaTod.now)</script>')
        still += f'<noscript><img class="hero-amb" src="{root}assets/art/hero_dawn-960.webp" width="960" height="536" alt="" aria-hidden="true" decoding="async"></noscript>'
    return live + fill + ambi + still


def apply(html, lang, **kw):
    """Home and the leveling guide: the head script, the hero picture (@@TOD_HERO@@) and the switch slot (@@TOD_SW@@)."""
    if '@@TOD_HERO@@' not in html:
        return html
    head_kw = {k: kw[k] for k in ('root', 'mobile', 'widths', 'sizes', 'msizes') if k in kw}
    head_kw['lq'] = kw.get('cls', 'hero-art') == 'hero-art'   # the home hero only: its CSS paints --lq
    html = html.replace('</head>', head_js(lang, **head_kw) + '</head>', 1)
    html = html.replace('@@TOD_HERO@@', hero(**kw), 1)
    return html.replace('@@TOD_SW@@', '<div class="todsw" data-tod-sw></div>', 1)
