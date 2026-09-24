// KennyShop Whatnot cover maker.
// node make-cover.mjs --category contemporary|activewear --photo photos/x.jpg \
//   --brands free-people,anthropologie,aritzia --out out/name.png
//   [--live "LIVE FRIDAY 7 PM EST"] [--fit auto|fill|whole] [--pos "center 40%" (fill) or "55" (whole: % down)] [--zoom 115%]
//   [--nudge B:0,-80] (move slot A/B/C by x,y pixels; repeatable)
import { chromium } from 'playwright-core';
import fs from 'fs'; import path from 'path'; import { fileURLToPath } from 'url';
const dir = path.dirname(fileURLToPath(import.meta.url));

const CATEGORIES = {
  contemporary: { label: 'PREMIUM CONTEMPORARY', live: 'LIVE FRIDAY 7 PM EST' },
  activewear:   { label: 'PREMIUM ACTIVEWEAR',   live: 'LIVE [DAY] AT [TIME] EST' },
};
// Display names for typed fallback tiles (used when logos/<slug>.png is missing)
const NAMES = {
  'anthropologie':'ANTHROPOLOGIE','free-people':'Free People','revolve':'REVOLVE','aritzia':'ARITZIA',
  'skims':'SKIMS','polo':'RALPH LAUREN','alo':'alo','lululemon':'lululemon','fp-movement':'FP MOVEMENT',
  'nike':'NIKE','white-fox':'WHITE FOX','patagonia':'patagonia',
};

const args = {}; const nudge = {};
for (let i = 2; i < process.argv.length; i += 2) {
  const k = process.argv[i].replace(/^--/, ''), v = process.argv[i + 1];
  if (k === 'nudge') { const [slot, xy] = v.split(':'); nudge[slot] = xy.split(',').map(Number); }
  else args[k] = v;
}
const cat = CATEGORIES[args.category];
if (!cat || !args.photo || !args.brands || !args.out) {
  console.error('Need --category (contemporary|activewear), --photo, --brands a,b,c, --out'); process.exit(1);
}
const brands = args.brands.split(',').slice(0, 3).map(s => s.trim())
  .map(slug => ({ slug, name: NAMES[slug] || slug.replace(/-/g, ' ').toUpperCase() }));
const cfg = { category: cat.label, live: args.live || cat.live, photo: 'file://' + path.resolve(args.photo),
  brands, fit: args.fit || 'auto', pos: args.pos, zoom: args.zoom, nudge };

const b = await chromium.launch({
  executablePath: process.env.CHROME || '/opt/pw-browsers/chromium-1194/chrome-linux/chrome',
  args: ['--allow-file-access-from-files'] });
const pg = await b.newPage({ viewport: { width: 1080, height: 1440 } });
await pg.addInitScript(c => { window.CFG = c; }, cfg);
await pg.goto('file://' + path.join(dir, 'template.html'));
const fit = await pg.waitForFunction(() => window.READY, null, { timeout: 15000 }).then(h => h.jsonValue());
fs.mkdirSync(path.dirname(path.resolve(args.out)), { recursive: true });
await (await pg.$('#cover')).screenshot({ path: path.resolve(args.out) });
await b.close();
console.log(`saved ${args.out} (${cat.label}, photo fit: ${fit})`);
