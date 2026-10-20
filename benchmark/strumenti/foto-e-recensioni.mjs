#!/usr/bin/env node
/* YDG · Per ogni struttura schedata prende da Google Places la foto principale
   e le recensioni testuali. Le foto finiscono in benchmark/foto/<id>.jpg,
   il resto in benchmark/dati/dettagli.json.

   La chiave NON deve finire nella pagina pubblicata: le foto si scaricano qui
   e si pubblicano come file accanto alla pagina, così nessuno la vede.
*/
import fs from "node:fs";
import path from "node:path";

const RADICE = path.resolve(import.meta.dirname, "..", "..");
const DATI = path.join(RADICE, "benchmark", "dati");
const FOTO = path.join(RADICE, "benchmark", "foto");
const chiave = () => {
  if (process.env.GOOGLE_PLACES_KEY) return process.env.GOOGLE_PLACES_KEY.trim();
  const m = fs.readFileSync(path.join(RADICE, ".env.local"), "utf8").match(/^\s*GOOGLE_PLACES_KEY\s*=\s*(.+)\s*$/m);
  if (!m) { console.error("✗ chiave mancante"); process.exit(1); }
  return m[1].trim().replace(/^["']|["']$/g, "");
};
const KEY = chiave();

// Le righe da arricchire: id del documento + placeId, dal file di carico
const righe = JSON.parse(fs.readFileSync(path.join(DATI, "righe-da-arricchire.json"), "utf8"));
const CAMPI = "id,displayName,photos,reviews,editorialSummary,rating,userRatingCount,regularOpeningHours.openNow";

fs.mkdirSync(FOTO, { recursive: true });
const esito = [];
let scaricate = 0, senzaFoto = 0, errori = 0;

for (const r of righe){
  const out = { id: r.id, placeId: r.placeId, nome: r.nome };
  try {
    const d = await fetch("https://places.googleapis.com/v1/places/" + r.placeId + "?languageCode=it", {
      headers: { "X-Goog-Api-Key": KEY, "X-Goog-FieldMask": CAMPI }
    }).then(x => x.json());
    if (d.error){ out.errore = d.error.message; errori++; esito.push(out); continue; }
    out.sommario = (d.editorialSummary && d.editorialSummary.text) || "";
    out.recensioni = (d.reviews || []).slice(0, 3).map(v => ({
      voto: v.rating,
      testo: ((v.originalText && v.originalText.text) || (v.text && v.text.text) || "").slice(0, 600),
      lingua: (v.originalText && v.originalText.languageCode) || "",
      quando: v.relativePublishTimeDescription || "",
      autore: (v.authorAttribution && v.authorAttribution.displayName) || ""
    }));
    const foto = (d.photos || [])[0];
    if (foto){
      const img = await fetch("https://places.googleapis.com/v1/" + foto.name +
        "/media?maxWidthPx=900&skipHttpRedirect=false&key=" + KEY);
      if (img.ok){
        const buf = Buffer.from(await img.arrayBuffer());
        fs.writeFileSync(path.join(FOTO, r.id + ".jpg"), buf);
        out.foto = r.id + ".jpg";
        out.fotoAttribuzione = ((foto.authorAttributions || [])[0] || {}).displayName || "";
        scaricate++;
      } else { out.errore = "foto HTTP " + img.status; errori++; }
    } else { senzaFoto++; }
  } catch(e){ out.errore = String(e.message || e); errori++; }
  esito.push(out);
  process.stdout.write("\r  " + esito.length + "/" + righe.length + " · foto " + scaricate + " · senza foto " + senzaFoto + " · errori " + errori + "   ");
  await new Promise(r => setTimeout(r, 80));
}
console.log("");
fs.writeFileSync(path.join(DATI, "dettagli.json"), JSON.stringify({
  presoIl: new Date().toISOString().slice(0,10),
  fonte: "Google Places API (New) · places details + photo media",
  quante: esito.length, conFoto: scaricate, senzaFoto, errori,
  strutture: esito
}, null, 2));
console.log("✓ foto scaricate: " + scaricate + " · senza foto: " + senzaFoto + " · errori: " + errori);
console.log("→ benchmark/foto/ e benchmark/dati/dettagli.json");
