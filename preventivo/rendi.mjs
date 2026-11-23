/* Resa del documento: HTML → Chromium → PDF + una PNG per pagina.
   Su Mac lo stesso lavoro lo fa Chrome headless dal kit del brand; qui sta
   a parte perché Playwright in questo container è quello di Node, non di Python. */
import { createRequire } from "node:module";
import path from "node:path";
import fs from "node:fs";

// Gli import ESM non guardano NODE_PATH: Playwright sta fuori dal progetto,
// quindi lo si risolve con require, che invece lo guarda.
const { chromium } = createRequire(import.meta.url)(
  process.env.PLAYWRIGHT_PATH || "playwright");

const [sorgente, pdf, anteprime] = process.argv.slice(2);
fs.mkdirSync(anteprime, { recursive: true });

const b = await chromium.launch({ args: ["--no-sandbox"] });
const pg = await b.newPage({ viewport: { width: 1280, height: 720 } });
await pg.goto("file://" + path.resolve(sorgente));
await pg.waitForTimeout(800);

// Gli sforamenti si controllano a macchina: una pagina che straborda si vede
// solo stampata, e a quel punto è tardi.
// Si misura solo il contenuto nel flusso: gli elementi decorativi in position
// absolute (l'alone arancio della copertina) escono apposta dal riquadro e
// vengono ritagliati, quindi conterebbero come sforamenti falsi.
const sfori = await pg.evaluate(() => [...document.querySelectorAll(".p")]
  .map((p, i) => {
    const alto = p.getBoundingClientRect().top;
    const giu = [...p.querySelectorAll("*")]
      .filter(el => {
        const s = getComputedStyle(el);
        // Gli elementi inline (<b>, <span>) riportano la scatola del font, piu'
        // alta della riga: conterebbero sempre qualche pixel di troppo.
        return s.position !== "absolute" && !s.display.startsWith("inline");
      })
      .map(el => el.getBoundingClientRect().bottom - alto);
    const pad = parseFloat(getComputedStyle(p).paddingBottom) || 0;
    return { n: i + 1, h: Math.round(Math.max(0, ...giu) + pad) };
  })
  .filter(x => x.h > 721));

const pagine = await pg.$$(".p");
for (let i = 0; i < pagine.length; i++)
  await pagine[i].screenshot({ path: path.join(anteprime, String(i + 1).padStart(2, "0") + ".png") });

await pg.pdf({ path: pdf, width: "1280px", height: "720px", printBackground: true,
               margin: { top: "0", bottom: "0", left: "0", right: "0" } });
await b.close();
console.log(JSON.stringify({ pagine: pagine.length, sfori }));
