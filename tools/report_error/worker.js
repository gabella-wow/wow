// «Нашёл ошибку» on the data pages of gabella.site/wow/ -> one short message in the Discord channel of Gabella Team
// (read once a day). The page sends: the page address (no query, no hash), the language, the screen width, the build
// version and an optional note. Nothing else is stored or forwarded: no IP, no user agent, no cookies.
// Secrets (wrangler secret put, never in the repo): REPORT_WEBHOOK — the Discord webhook URL; RL_SALT — a random string
// for the hash of the client address in the rate limit. Optional KV binding RL (wrangler.toml) keeps the limit across
// isolates; without it the limit lives in the memory of one isolate.

const ORIGINS = ['https://gabella.site'];
const PAGE_PREFIX = 'https://gabella.site/wow/';
const LANGS = ['ru', 'en', 'uk', 'de', 'es', 'fr', 'it', 'pl', 'pt'];
const MAX_BODY = 4096;        // bytes of the request body
const MAX_TEXT = 500;         // characters of the note
const MAX_URL = 300;
const PER_CLIENT = 3;         // reports per client per hour
const PER_HOUR = 60;          // reports per hour from everyone (Discord stays quiet during a flood)
const MIN_MS = 800;           // a person needs more than this between opening the form and sending it
const HOUR = 3600 * 1000;
const COUNT_PATH = '/c';       // the visit beacon: {k:'visit'|'char'}, one per browser per day
const COUNT_TTL = 120 * 86400; // seconds a day counter lives in KV

function cors(origin) {
  return ORIGINS.includes(origin)
    ? { 'Access-Control-Allow-Origin': origin, 'Access-Control-Allow-Methods': 'POST', 'Access-Control-Allow-Headers': 'content-type', 'Access-Control-Max-Age': '86400', Vary: 'Origin' }
    : { Vary: 'Origin' };
}

function reply(status, origin, msg = '') {
  return new Response(status === 204 ? null : msg, { status, headers: { 'content-type': 'text/plain; charset=utf-8', 'cache-control': 'no-store', ...cors(origin) } });
}

// The checked report, or a string with the reason it was refused.
export function validate(data) {
  if (!data || typeof data !== 'object' || Array.isArray(data)) return 'body';
  if (data.hp) return 'spam';                                       // the honeypot field is invisible to people
  const { url, lang, w, v, ms } = data;
  const text = data.text == null ? '' : data.text;
  if (typeof url !== 'string' || url.length > MAX_URL || !url.startsWith(PAGE_PREFIX) || /[?#\s<>]/.test(url)) return 'url';
  if (!LANGS.includes(lang)) return 'lang';
  if (!Number.isInteger(w) || w < 200 || w > 10000) return 'width';
  if (typeof v !== 'string' || !/^[0-9A-Za-z.\-]{1,24}$/.test(v)) return 'version';
  if (typeof text !== 'string' || text.length > MAX_TEXT) return 'text';
  if (!Number.isFinite(ms) || ms < MIN_MS) return 'spam';            // sent by a script the moment the page opened
  if ((text.match(/https?:\/\/|www\.|discord\.gg/gi) || []).length > 1) return 'spam';   // link drops
  return { url, lang, w, v, text: text.replace(/[\x00-\x08\x0B-\x1F\x7F]/g, '').trim() };
}

// The Discord message: plain text, mentions and link previews off, the note in a code block (no markdown tricks).
export function message(r) {
  const note = r.text ? '```\n' + r.text.replace(/`/g, "'") + '\n```' : '(без описания)';
  return {
    content: `**Ошибка на сайте** · ${r.lang} · ${r.w}px · сборка ${r.v}\n<${r.url}>\n${note}`,
    allowed_mentions: { parse: [] },
    flags: 4,                         // SUPPRESS_EMBEDS
  };
}

export async function clientKey(ip, salt) {
  const buf = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(`${salt}|${ip}`));
  return [...new Uint8Array(buf)].slice(0, 16).map((b) => b.toString(16).padStart(2, '0')).join('');
}

// Counter store: the KV binding, or a Map in this isolate (tests, or no KV yet).
const memory = new Map();
export function memStore(map = memory) {
  return {
    async get(k) { const e = map.get(k); return e && e.until > Date.now() ? e.n : 0; },
    async put(k, n) { map.set(k, { n, until: Date.now() + HOUR }); },
  };
}
function kvStore(kv) {
  return {
    async get(k) { return Number(await kv.get(k)) || 0; },
    async put(k, n) { await kv.put(k, String(n), { expirationTtl: 3600 }); },
  };
}

// Day counters cnt:YYYY-MM-DD:visit|char (UTC). Only a number per key: no IP, no user agent, no id. A read+write is not atomic,
// so under a burst a few hits can be lost; fine for a ratio.
const countMem = new Map();
export function dayKey(now, k) { return `cnt:${new Date(now).toISOString().slice(0, 10)}:${k}`; }
async function count(request, origin, env, deps, now) {
  const raw = await request.text();
  if (!raw || raw.length > 64) return reply(400, origin, 'body');
  let data;
  try { data = JSON.parse(raw); } catch { return reply(400, origin, 'json'); }
  if (!data || typeof data !== 'object' || (data.k !== 'visit' && data.k !== 'char')) return reply(400, origin, 'kind');
  const key = dayKey(now, data.k);
  if (deps.counts) deps.counts.set(key, (deps.counts.get(key) || 0) + 1);
  else if (env.RL) await env.RL.put(key, String((Number(await env.RL.get(key)) || 0) + 1), { expirationTtl: COUNT_TTL });
  else countMem.set(key, (countMem.get(key) || 0) + 1);
  return reply(204, origin);
}

export async function handle(request, env, deps = {}) {
  const origin = request.headers.get('Origin') || '';
  const send = deps.fetch || fetch;
  const now = deps.now ? deps.now() : Date.now();
  const store = deps.store || (env.RL ? kvStore(env.RL) : memStore());

  if (!ORIGINS.includes(origin)) return reply(403, origin, 'origin');
  if (request.method === 'OPTIONS') return reply(204, origin);
  if (request.method !== 'POST') return reply(405, origin, 'method');
  if (new URL(request.url).pathname === COUNT_PATH) return count(request, origin, env, deps, now);
  if (!env.REPORT_WEBHOOK || !env.RL_SALT) return reply(503, origin, 'not configured');

  const raw = await request.text();
  if (!raw || raw.length > MAX_BODY) return reply(400, origin, 'body');
  let data;
  try { data = JSON.parse(raw); } catch { return reply(400, origin, 'json'); }
  const r = validate(data);
  if (typeof r === 'string') return reply(r === 'spam' ? 202 : 400, origin, r);   // spam gets a quiet «accepted»: no hint to retry

  const hour = Math.floor(now / HOUR);
  const ip = request.headers.get('CF-Connecting-IP') || '';
  const kc = `c:${await clientKey(ip, env.RL_SALT)}:${hour}`, ka = `a:${hour}`;
  const [nc, na] = [await store.get(kc), await store.get(ka)];
  if (nc >= PER_CLIENT || na >= PER_HOUR) return reply(429, origin, 'limit');
  await store.put(kc, nc + 1);
  await store.put(ka, na + 1);

  const res = await send(env.REPORT_WEBHOOK, { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify(message(r)) });
  if (!res.ok) { console.log(`webhook ${res.status}`); return reply(502, origin, 'upstream'); }
  return reply(204, origin);
}

export default { fetch: (request, env) => handle(request, env) };
