#!/usr/bin/env node
/* YDG · Legge la homepage di ogni struttura candidata e cerca i link ai social.
   Nessuna API a pagamento: solo fetch pubblici.

   Serve il segnale che manca a Places: chi LAVORA BENE ma COMUNICA MALE.
   Attenzione a cosa vale: trovare il link prova la presenza. NON trovarlo NON
   prova l'assenza (link in JS, footer caricato dopo, sito che blocca i bot):
   esce "da verificare", e si guarda a mano. Mai dare per morto un social
   solo perché il bot non l'ha visto.
*/
import fs from "node:fs";
import path from "node:path";

const RADICE = path.resolve(import.meta.dirname, "..", "..");
const DATI = path.join(RADICE, "benchmark", "dati");
const grezzo = JSON.parse(fs.readFileSync(path.join(DATI, "strutture-grezze.json"), "utf8"));

const MAXKM = Number(process.env.MAXKM || 35);
const PARALLELE = 8;

const candidate = grezzo.strutture.filter(r =>
  r.km != null && r.km <= MAXKM &&
  (r.rating || 0) >= 4.2 &&
  (r.recensioni || 0) >= 60 &&
  (!r.stato || r.stato === "OPERATIONAL")
);

const RETI = {
  instagram: /(?:https?:)?\/\/(?:www\.)?instagram\.com\/([A-Za-z0-9_.]+)/i,
  facebook:  /(?:https?:)?\/\/(?:www\.)?facebook\.com\/([A-Za-z0-9_.\-]+)/i,
  tiktok:    /(?:https?:)?\/\/(?:www\.)?tiktok\.com\/@([A-Za-z0-9_.]+)/i,
  youtube:   /(?:https?:)?\/\/(?:www\.)?youtube\.com\/(?:c\/|channel\/|@)?([A-Za-z0-9_.\-]+)/i,
  linkedin:  /(?:https?:)?\/\/(?:[a-z]{2,3}\.)?linkedin\.com\/(?:company|in)\/([A-Za-z0-9_.\-]+)/i
};
const SCARTA = /^(p|pages|profile|sharer|share|home|tr|plugins|dialog|login|policy|help|about|privacy|terms|embed|watch|results|hashtag|explore|reel|reels|stories)$/i;

async function leggi(url, ms){
  const ctrl = new AbortController();
  const t = setTimeout(() => ctrl.abort(), ms);
  try {
    const r = await fetch(url, { signal: ctrl.signal, redirect: "follow",
      headers: { "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0 Safari/537.36",
                 "Accept-Language": "it,de;q=0.8,en;q=0.6" } });
    if (!r.ok) return { errore: "HTTP " + r.status };
    const testo = await r.text();
    return { html: testo.slice(0, 900000), finale: r.url };
  } catch(e){ return { errore: e.name === "AbortError" ? "timeout" : (e.cause && e.cause.code) || e.message }; }
  finally { clearTimeout(t); }
}

const esito = [];
let fatte = 0;

async function lavora(r){
  const out = { placeId: r.placeId, nome: r.nome, sito: r.sito, social: {}, nota: "" };
  if (!r.sito){ out.nota = "Nessun sito: social non verificabili da qui"; return out; }
  const res = await leggi(r.sito, 9000);
  if (res.errore){ out.nota = "Sito non leggibile (" + res.errore + "): da verificare a mano"; return out; }
  const html = res.html;
  // Tutti i match, non solo il primo: il pixel facebook.com/tr sta in cima
  // alla pagina e coprirebbe il link vero al profilo.
  for (const [rete, re] of Object.entries(RETI)){
    const tutti = [...html.matchAll(new RegExp(re.source, "gi"))];
    const buono = tutti.map(m => m[1]).find(h => h && !SCARTA.test(h));
    if (buono) out.social[rete] = buono;
  }
  out.trovati = Object.keys(out.social).length;
  if (!out.trovati) out.nota = "Nessun link social nella homepage: da verificare a mano";
  return out;
}

console.log("Candidate da leggere: " + candidate.length + " (entro " + MAXKM + " km, ≥4.2★, ≥60 recensioni)");
for (let i = 0; i < candidate.length; i += PARALLELE){
  const lotto = candidate.slice(i, i + PARALLELE);
  const res = await Promise.all(lotto.map(lavora));
  esito.push(...res);
  fatte += lotto.length;
  process.stdout.write("\r  lette " + fatte + "/" + candidate.length + "   ");
}
console.log("");

const conSocial = esito.filter(e => e.trovati > 0).length;
const senza = esito.filter(e => e.sito && e.trovati === 0 && !e.nota.startsWith("Sito non leggibile")).length;
const illeggibili = esito.filter(e => e.nota.startsWith("Sito non leggibile")).length;

fs.writeFileSync(path.join(DATI, "social-homepage.json"), JSON.stringify({
  lettoIl: new Date().toISOString().slice(0,10),
  avvertenza: "Link trovato = social presente. Link NON trovato = DA VERIFICARE, non assente.",
  maxKm: MAXKM, candidate: candidate.length,
  conSocial, senzaLinkInHomepage: senza, sitiIlleggibili: illeggibili,
  strutture: esito
}, null, 2));

console.log("✓ Con almeno un social linkato: " + conSocial);
console.log("✓ Senza alcun link social in homepage (da verificare): " + senza);
console.log("✓ Siti non leggibili: " + illeggibili);
console.log("→ benchmark/dati/social-homepage.json");
