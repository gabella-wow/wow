"""«Нашёл ошибку» on the data pages: a quiet button at the end of the page data (right before the Discord line .dcta)
and a small dialog. The report goes to the Worker tools/report_error (Discord of Gabella Team, read once a day) with the
page address (no query, no hash), the language, the screen width and the build version; no IP, no personal data.
seo.main() calls inject() on every finished page; only the pages of wants() get the button."""
import re
from html import escape
import json

REPORT_URL = 'https://report.gabella.site/'   # the Worker's custom domain (tools/report_error/wrangler.toml)

# button, dialog title, field label, what is attached, send, cancel, sending, sent, limit, failed
TX = {
    'ru': ('Нашёл ошибку', 'Ошибка на странице', 'Что не так (необязательно)',
           'Вместе с сообщением отправим адрес страницы, язык, ширину экрана и версию сборки. IP и личные данные не собираем.',
           'Отправить', 'Отмена', 'Отправляем…', 'Отправлено. Сообщения разбираем каждый день.',
           'Слишком много сообщений. Попробуйте через час.', 'Не отправилось. Попробуйте позже или напишите в Discord.'),
    'en': ('Found an error', 'Error on this page', 'What is wrong (optional)',
           'We also send the page address, language, screen width and build version. No IP, no personal data.',
           'Send', 'Cancel', 'Sending…', 'Sent. We review reports every day.',
           'Too many reports. Try again in an hour.', 'Not sent. Try again later or write to us on Discord.'),
    'uk': ('Знайшов помилку', 'Помилка на сторінці', 'Що не так (необов’язково)',
           'Разом із повідомленням надішлемо адресу сторінки, мову, ширину екрана й версію збірки. IP та особисті дані не збираємо.',
           'Надіслати', 'Скасувати', 'Надсилаємо…', 'Надіслано. Повідомлення розбираємо щодня.',
           'Забагато повідомлень. Спробуйте за годину.', 'Не надіслалося. Спробуйте пізніше або напишіть у Discord.'),
    'de': ('Fehler gefunden', 'Fehler auf dieser Seite', 'Was stimmt nicht (optional)',
           'Mitgesendet werden Seitenadresse, Sprache, Bildschirmbreite und Build-Version. Keine IP, keine persönlichen Daten.',
           'Senden', 'Abbrechen', 'Wird gesendet…', 'Gesendet. Wir prüfen Meldungen täglich.',
           'Zu viele Meldungen. Versuch es in einer Stunde erneut.', 'Nicht gesendet. Versuch es später oder schreib uns auf Discord.'),
    'es': ('Encontré un error', 'Error en esta página', 'Qué está mal (opcional)',
           'También enviamos la dirección de la página, el idioma, el ancho de pantalla y la versión. Sin IP ni datos personales.',
           'Enviar', 'Cancelar', 'Enviando…', 'Enviado. Revisamos los avisos cada día.',
           'Demasiados avisos. Inténtalo dentro de una hora.', 'No se envió. Inténtalo más tarde o escríbenos en Discord.'),
    'fr': ('J’ai trouvé une erreur', 'Erreur sur cette page', 'Ce qui ne va pas (facultatif)',
           'Nous joignons l’adresse de la page, la langue, la largeur d’écran et la version. Ni IP ni données personnelles.',
           'Envoyer', 'Annuler', 'Envoi…', 'Envoyé. Nous lisons les signalements chaque jour.',
           'Trop de signalements. Réessayez dans une heure.', 'Échec de l’envoi. Réessayez plus tard ou écrivez-nous sur Discord.'),
    'it': ('Ho trovato un errore', 'Errore in questa pagina', 'Cosa non va (facoltativo)',
           'Inviamo anche indirizzo della pagina, lingua, larghezza dello schermo e versione. Niente IP né dati personali.',
           'Invia', 'Annulla', 'Invio…', 'Inviato. Leggiamo le segnalazioni ogni giorno.',
           'Troppe segnalazioni. Riprova tra un’ora.', 'Invio non riuscito. Riprova più tardi o scrivici su Discord.'),
    'pl': ('Znalazłem błąd', 'Błąd na tej stronie', 'Co jest nie tak (opcjonalnie)',
           'Wysyłamy też adres strony, język, szerokość ekranu i wersję. Bez IP i danych osobowych.',
           'Wyślij', 'Anuluj', 'Wysyłanie…', 'Wysłano. Zgłoszenia przeglądamy codziennie.',
           'Za dużo zgłoszeń. Spróbuj za godzinę.', 'Nie wysłano. Spróbuj później lub napisz do nas na Discordzie.'),
    'pt': ('Encontrei um erro', 'Erro nesta página', 'O que está errado (opcional)',
           'Também enviamos o endereço da página, o idioma, a largura da tela e a versão. Sem IP nem dados pessoais.',
           'Enviar', 'Cancelar', 'Enviando…', 'Enviado. Revisamos os avisos todo dia.',
           'Avisos demais. Tente de novo em uma hora.', 'Não enviado. Tente mais tarde ou escreva para nós no Discord.'),
}

# The data pages: classes, builds and talents, specs (gear 13–30), tier list, dungeons, the second screen, the talent calculator.
DATA = re.compile(r'(classes/[a-z]+/|guides/(builds|builds-[a-z]+|spec-[a-z-]+|tier-list|dungeons(/[a-z-]+)?)/|play/|talents/([a-z]+/)?)$')


def wants(path):
    return bool(DATA.fullmatch(path))


CSS = ('<style>'
       '.rep{margin:40px 0 0}.rep+.dcta{margin-top:16px}'
       '.rep-b{display:inline-flex;align-items:center;min-height:44px;padding:0 16px;border:1px solid var(--pline);border-radius:7px;'
       'background:var(--panel-2);color:var(--muted);font:inherit;font-size:var(--fs-14);font-weight:600;cursor:pointer;'
       'transition:border-color .2s,color .2s}'
       '.rep-b:hover{border-color:var(--gold);color:var(--fg)}'
       '.repd{width:min(480px,calc(100vw - 32px));max-width:none;margin:auto;padding:0;border:1px solid var(--line);border-radius:10px;'
       'background:var(--surface);color:var(--fg)}'
       '.repd::backdrop{background:rgba(0,0,0,.6)}'
       '.rep-f{display:grid;gap:12px;padding:20px}'
       '.rep-f h2{margin:0;font-family:var(--font-body);font-size:var(--fs-22);font-weight:600;line-height:1.25}'
       '.rep-f label{font-size:var(--fs-14);color:var(--muted)}'
       '.rep-f textarea{width:100%;min-height:96px;padding:10px 12px;font:inherit;resize:vertical;border:1px solid var(--fline);'
       'border-radius:7px;background:var(--panel-2);color:var(--fg)}'
       '.rep-n{margin:0;font-size:var(--fs-13);color:var(--muted)}'
       '.rep-s{margin:0;min-height:1.4em;font-size:var(--fs-14)}.rep-s:empty{display:none}'
       '.rep-a{display:flex;flex-wrap:wrap;gap:8px}.rep-a .btn{flex:1 1 120px;white-space:normal;text-align:center}'
       '.rep-hp{position:absolute;left:-9999px;width:1px;height:1px;overflow:hidden}'
       '</style>')

JS = """<script>
(function () {
  var b = document.querySelector('.rep-b'), d = document.getElementById('repDlg');
  if (!b || !d || !d.showModal) { if (b) b.parentNode.hidden = true; return; }
  var f = d.querySelector('form'), s = d.querySelector('.rep-s'), go = f.querySelector('[type=submit]'), m = JSON.parse(d.dataset.m), t0 = 0;
  b.addEventListener('click', function () { s.textContent = ''; go.disabled = false; t0 = Date.now(); d.showModal(); });
  d.querySelector('.rep-c').addEventListener('click', function () { d.close(); });
  d.addEventListener('click', function (e) { if (e.target === d) d.close(); });
  d.addEventListener('close', function () { b.focus(); });
  f.addEventListener('submit', function (e) {
    e.preventDefault();
    go.disabled = true; s.textContent = m[0];
    fetch(d.dataset.u, { method: 'POST', credentials: 'omit', headers: { 'content-type': 'text/plain' }, body: JSON.stringify({
      url: location.origin + location.pathname, lang: d.dataset.l, w: window.innerWidth, v: b.dataset.v,
      text: f.elements.text.value.trim(), hp: f.elements.website.value, ms: Date.now() - t0 }) })
      .then(function (r) { if (r.status === 429) throw 429; if (!r.ok) throw 0; s.textContent = m[1]; f.elements.text.value = ''; setTimeout(function () { if (d.open) d.close(); }, 2000); })
      .catch(function (x) { s.textContent = x === 429 ? m[2] : m[3]; go.disabled = false; });
  });
})();
</script>
"""


def button(lang, version):
    return (f'<p class="rep"><button class="rep-b" type="button" aria-haspopup="dialog" aria-controls="repDlg" data-v="{escape(version)}">'
            f'{escape(TX[lang][0])}</button></p>\n')


def dialog(lang):
    btn, title, label, note, send, cancel, *msgs = TX[lang]
    return (f'<dialog class="repd" id="repDlg" aria-labelledby="repT" data-l="{lang}" data-u="{REPORT_URL}" data-m="{escape(json.dumps(msgs, ensure_ascii=False))}">'
            f'<form class="rep-f" method="dialog"><h2 id="repT">{escape(title)}</h2>'
            f'<label for="repX">{escape(label)}</label><textarea id="repX" name="text" rows="4" maxlength="500"></textarea>'
            '<div class="rep-hp" aria-hidden="true"><label for="repW">Website</label><input id="repW" name="website" tabindex="-1" autocomplete="off"></div>'
            f'<p class="rep-n">{escape(note)}</p><p class="rep-s" role="status" aria-live="polite"></p>'
            f'<div class="rep-a"><button class="btn" type="submit">{escape(send)}</button>'
            f'<button class="btn ghost rep-c" type="button">{escape(cancel)}</button></div></form></dialog>\n')


def inject(html, path, lang, version):
    """The page with the button (before the Discord line), its styles (end of head) and the dialog with its script
    (end of body). Pages outside wants() and pages that already have it come back unchanged."""
    if not wants(path) or 'id="repDlg"' in html:
        return html
    i = html.find('<p class="dcta">')
    assert i > 0, f'report: no Discord line (.dcta) on {lang}/{path}'
    html = html[:i] + button(lang, version) + html[i:]
    html = html.replace('</head>', CSS + '\n</head>', 1)
    j = html.rindex('</body>')
    return html[:j] + dialog(lang) + JS + html[j:]
