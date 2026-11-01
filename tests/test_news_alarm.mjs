// Worker gabella-news-alarm: which workflows each tick starts. No network. Run: node tests/test_news_alarm.mjs
import assert from 'node:assert/strict';
import { feedTick, targets } from '../tools/news_alarm/worker.js';

const at = (h, m) => Date.UTC(2026, 10, 1, h, m);
const name = (u) => u.split('/')[8];

assert.deepEqual(targets(false).map(name), ['news-auto.yml']);                                 // :10 :20 :40 :50
assert.deepEqual(targets(true).map(name), ['news-auto.yml', 'news.yml', 'news-watchdog.yml']); // :00 :30
assert.equal(feedTick(at(3, 0)), true);
assert.equal(feedTick(at(3, 30)), true);
assert.equal(feedTick(at(3, 10)), false);
assert.equal(feedTick(at(3, 20)), false);
assert.equal(feedTick(at(3, 40)), false);
assert.equal(feedTick(at(3, 50)), false);
console.log('ok news_alarm');
