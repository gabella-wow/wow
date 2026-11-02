// Worker gabella-report-error: origin, empty, spam, limits, the Discord message. No network. Run: node tests/test_report_worker.mjs
import assert from 'node:assert/strict';
import { handle, memStore, message, validate, PER_CLIENT } from '../tools/report_error/worker.js';

const ENV = { REPORT_WEBHOOK: 'https://discord.invalid/webhook/PLACEHOLDER', RL_SALT: 'test-salt' };
const GOOD = { url: 'https://gabella.site/wow/en/guides/spec-mage-fire/', lang: 'en', w: 1280, v: '2026-11-01', text: 'Talent row 3 is wrong', ms: 4000, hp: '' };

let results = [];
function req(body, { origin = 'https://gabella.site', method = 'POST', ip = '203.0.113.7' } = {}) {
  const headers = { 'content-type': 'text/plain', 'CF-Connecting-IP': ip };
  if (origin) headers.Origin = origin;
  return new Request('https://report.gabella.site/', { method, headers, body: method === 'POST' ? (typeof body === 'string' ? body : JSON.stringify(body)) : undefined });
}
function deps(store = memStore(new Map())) {
  const sent = [];
  return { sent, store, now: () => Date.UTC(2026, 10, 2, 12, 0), fetch: async (url, init) => { sent.push({ url, body: JSON.parse(init.body) }); return new Response(null, { status: 204 }); } };
}
async function check(name, fn) {
  try { await fn(); results.push(`ПРОЙДЕНО ${name}`); } catch (e) { results.push(`УПАЛО ${name}: ${e.message}`); }
}

await check('good report goes to Discord once', async () => {
  const d = deps();
  const r = await handle(req(GOOD), ENV, d);
  assert.equal(r.status, 204);
  assert.equal(r.headers.get('Access-Control-Allow-Origin'), 'https://gabella.site');
  assert.equal(d.sent.length, 1);
  assert.equal(d.sent[0].url, ENV.REPORT_WEBHOOK);
  const c = d.sent[0].body.content;
  assert.match(c, /spec-mage-fire/); assert.match(c, / en /); assert.match(c, /1280px/); assert.match(c, /2026-11-01/); assert.match(c, /Talent row 3/);
  assert.ok(!c.includes('203.0.113.7'), 'no IP in the message');
  assert.deepEqual(d.sent[0].body.allowed_mentions, { parse: [] });
});

await check('foreign origin -> 403, nothing sent', async () => {
  for (const origin of ['https://evil.example', 'http://gabella.site', 'https://gabella.site.evil.example', null]) {
    const d = deps();
    const r = await handle(req(GOOD, { origin }), ENV, d);
    assert.equal(r.status, 403, String(origin));
    assert.equal(r.headers.get('Access-Control-Allow-Origin'), null);
    assert.equal(d.sent.length, 0);
  }
});

await check('empty body / bad json / not an object -> 400', async () => {
  for (const body of ['', 'not json', '[]', 'null', '42']) {
    const d = deps();
    const r = await handle(req(body), ENV, d);
    assert.equal(r.status, 400, JSON.stringify(body));
    assert.equal(d.sent.length, 0);
  }
});

await check('empty note is allowed (the note is optional)', async () => {
  const d = deps();
  const r = await handle(req({ ...GOOD, text: '' }), ENV, d);
  assert.equal(r.status, 204);
  assert.match(d.sent[0].body.content, /без описания/);
});

await check('bad fields -> 400', async () => {
  const bad = [{ url: 'https://evil.example/wow/' }, { url: 'https://gabella.site/wow/en/?email=a@b.c' }, { url: 'https://gabella.site/other/' },
    { lang: 'xx' }, { w: 50 }, { w: '1280' }, { v: '<script>' }, { text: 'x'.repeat(501) }, { text: 42 }];
  for (const b of bad) {
    const d = deps();
    const r = await handle(req({ ...GOOD, ...b }), ENV, d);
    assert.equal(r.status, 400, JSON.stringify(b));
    assert.equal(d.sent.length, 0);
  }
  const big = await handle(req({ ...GOOD, text: 'x'.repeat(5000) }), ENV, deps());
  assert.equal(big.status, 400);
});

await check('spam: honeypot, too fast, link drop -> quiet 202, nothing sent', async () => {
  for (const b of [{ hp: 'http://spam.example' }, { ms: 100 }, { ms: undefined }, { text: 'buy http://a.example http://b.example' }, { text: 'discord.gg/x www.y.example' }]) {
    const d = deps();
    const r = await handle(req({ ...GOOD, ...b }), ENV, d);
    assert.equal(r.status, 202, JSON.stringify(b));
    assert.equal(d.sent.length, 0);
  }
});

await check(`rate limit: ${PER_CLIENT} per client per hour, other clients still pass`, async () => {
  const store = memStore(new Map());
  const d = deps(store);
  for (let i = 0; i < PER_CLIENT; i++) assert.equal((await handle(req(GOOD), ENV, d)).status, 204);
  assert.equal((await handle(req(GOOD), ENV, d)).status, 429);
  assert.equal(d.sent.length, PER_CLIENT);
  assert.equal((await handle(req(GOOD, { ip: '198.51.100.9' }), ENV, d)).status, 204);
});

await check('the store never holds the IP in clear', async () => {
  const map = new Map();
  await handle(req(GOOD), ENV, deps(memStore(map)));
  assert.ok(map.size > 0);
  for (const k of map.keys()) assert.ok(!k.includes('203.0.113'), k);
});

await check('no secrets -> 503; GET -> 405; OPTIONS -> 204 with CORS', async () => {
  assert.equal((await handle(req(GOOD), {}, deps())).status, 503);
  assert.equal((await handle(req(null, { method: 'GET' }), ENV, deps())).status, 405);
  const o = await handle(req(null, { method: 'OPTIONS' }), ENV, deps());
  assert.equal(o.status, 204);
  assert.equal(o.headers.get('Access-Control-Allow-Origin'), 'https://gabella.site');
});

await check('webhook down -> 502', async () => {
  const d = deps(); d.fetch = async () => new Response('x', { status: 500 });
  assert.equal((await handle(req(GOOD), ENV, d)).status, 502);
});

await check('message: backticks cannot break the code block, no markdown pings', async () => {
  const m = message(validate({ ...GOOD, text: '```@everyone``` <@123>' }));
  assert.equal((m.content.match(/```/g) || []).length, 2);
  assert.equal(m.flags, 4);
});

console.log(results.join('\n'));
const failed = results.filter((l) => l.startsWith('УПАЛО')).length;
console.log(failed ? `УПАЛО report_worker: ${failed} of ${results.length}` : `ПРОЙДЕНО report_worker: ${results.length} checks`);
process.exit(failed ? 1 : 0);
