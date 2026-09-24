// Renders each cover to out/<id>.png.
// Usage: node render.mjs <contemporary-photo> [activewear-photo]
import { chromium } from 'playwright-core';
import fs from 'fs'; import path from 'path'; import { fileURLToPath } from 'url';
const dir = path.dirname(fileURLToPath(import.meta.url));
const ph = n => { const p = process.argv[2+n]; return p ? 'file://'+path.resolve(p) : 'placeholder.svg'; };
const html = fs.readFileSync(path.join(dir,'covers.html'),'utf8').replace('PHOTO_1',ph(0)).replace('PHOTO_2',ph(1));
const tmp = path.join(dir,'.render.html'); fs.writeFileSync(tmp,html);
const b = await chromium.launch({executablePath: process.env.CHROME || '/opt/pw-browsers/chromium-1194/chrome-linux/chrome'});
const pg = await b.newPage({viewport:{width:1080,height:1440}});
await pg.goto('file://'+tmp); await pg.evaluate(()=>document.fonts.ready); await pg.waitForTimeout(500);
fs.mkdirSync(path.join(dir,'out'),{recursive:true});
for (const id of ['contemporary','activewear']) await (await pg.$('#'+id)).screenshot({path:path.join(dir,'out',id+'.png')});
await b.close(); fs.unlinkSync(tmp); console.log('done');
