// Alarm of the news automation. Every 10 minutes starts
//   gabella-wow/wow          news-auto.yml  (watcher of Blizzard, short note on the site; public repo, free minutes)
// every 30 minutes starts
//   gabella-wow/wow          news.yml       (feed assets/news.json, RSS; public repo)
// and with the same tick (:00, :30) starts
//   gabella-wow/wow          news-watchdog.yml  (alert if news-auto is silent > 25 min; its own GitHub cron ran only every 2.7-5.7 h on 31.10)
// The Discord workflow news in gabella-bot is OFF until further notice (not dispatched).
// GitHub's own cron is late by hours. The token lives only in the Worker secret GH_DISPATCH_TOKEN
// (fine-grained, these two repositories only, Actions: read and write). The workflows decide by their switches
// (variables NEWS_AUTO / NEWS_DISCORD): the alarm sends no mode.
const SITE = 'https://api.github.com/repos/gabella-wow/wow/actions/workflows/news-auto.yml/dispatches';
const FEED = 'https://api.github.com/repos/gabella-wow/wow/actions/workflows/news.yml/dispatches';
const WATCHDOG = 'https://api.github.com/repos/gabella-wow/wow/actions/workflows/news-watchdog.yml/dispatches';

export function targets(withFeed) {
  return withFeed ? [SITE, FEED, WATCHDOG] : [SITE];
}

async function dispatch(env, withFeed) {
  const out = [];
  for (const url of targets(withFeed)) {
    const r = await fetch(url, {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${env.GH_DISPATCH_TOKEN}`,
        Accept: 'application/vnd.github+json',
        'X-GitHub-Api-Version': '2022-11-28',
        'User-Agent': 'gabella-news-alarm',
      },
      body: JSON.stringify({ ref: 'main' }),
    });
    console.log(`dispatch ${url.split('/')[5]}/${url.split('/')[8]}: ${r.status}`);   // 204 = started; 401/403 = token; 404 = workflow not on main yet
    out.push(r.status);
  }
  return out;
}

// every third tick (:00 and :30)
export function feedTick(scheduledTime) {
  const minute = new Date(scheduledTime).getUTCMinutes();
  return minute < 10 || (minute >= 30 && minute < 40);
}

export default {
  async scheduled(event, env, ctx) {
    ctx.waitUntil(dispatch(env, feedTick(event.scheduledTime)));
  },
  async fetch() {                        // no workers.dev address (workers_dev = false); this only answers that it is alive
    return new Response('gabella news alarm\n', { headers: { 'content-type': 'text/plain' } });
  },
};
