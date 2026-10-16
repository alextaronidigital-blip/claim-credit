#!/usr/bin/env node
/* YDG · Verticale ospitalità
   Costruisce la lista delle strutture nel raggio di Siusi usando Google Places API (New).

   Uso:
     export GOOGLE_PLACES_KEY=...        (oppure mettila in .env.local)
     node benchmark/strumenti/lista-strutture.mjs            # raccolta completa
     node benchmark/strumenti/lista-strutture.mjs --prova    # 3 sole zone, per testare la chiave
     node benchmark/strumenti/lista-strutture.mjs --quante 50

   Scrive:
     benchmark/dati/strutture-grezze.json   tutto quello che Places restituisce
     benchmark/dati/strutture-50.json       le prime N nello schema dell'hub, pronte da caricare

   Cosa Places NON sa: le stelle (4★, 4★ Sup), la stagionalità reale, i social.
   Quei campi escono "Non classificato" / "Da verificare": si compilano a mano nell'hub.
*/
import fs from "node:fs";
import path from "node:path";

const RADICE = path.resolve(import.meta.dirname, "..", "..");
const ZONE = JSON.parse(fs.readFileSync(path.join(import.meta.dirname, "comuni.json"), "utf8"));
const USCITA = path.join(RADICE, "benchmark", "dati");

/* ---- chiave ---- */
function chiave(){
  if (process.env.GOOGLE_PLACES_KEY) return process.env.GOOGLE_PLACES_KEY.trim();
  const f = path.join(RADICE, ".env.local");
  if (fs.existsSync(f)){
    const m = fs.readFileSync(f, "utf8").match(/^\s*GOOGLE_PLACES_KEY\s*=\s*(.+)\s*$/m);
    if (m) return m[1].trim().replace(/^["']|["']$/g, "");
  }
  console.error("✗ Chiave mancante. Metti GOOGLE_PLACES_KEY in .env.local (nella radice del repo) o nell'ambiente.");
  process.exit(1);
}
const KEY = chiave();

const argv = process.argv.slice(2);
const PROVA = argv.includes("--prova");
const QUANTE = Number((argv.find(a => a.startsWith("--quante")) || "").split("=")[1] || argv[argv.indexOf("--quante")+1]) || 50;

/* ---- utilità ---- */
const km = (aLat, aLon, bLat, bLon) => {
  const R = 6371, r = Math.PI/180;
  const dLat = (bLat-aLat)*r, dLon = (bLon-aLon)*r;
  const h = Math.sin(dLat/2)**2 + Math.cos(aLat*r)*Math.cos(bLat*r)*Math.sin(dLon/2)**2;
  return 2*R*Math.asin(Math.sqrt(h));
};
const attendi = ms => new Promise(r => setTimeout(r, ms));

const CAMPI = [
  "places.id","places.displayName","places.location","places.rating","places.userRatingCount",
  "places.websiteUri","places.nationalPhoneNumber","places.formattedAddress","places.addressComponents",
  "places.primaryType","places.types","places.businessStatus","places.priceLevel","places.googleMapsUri",
  "nextPageToken"
].join(",");

async function cerca(testo, pageToken){
  const corpo = {
    textQuery: testo,
    languageCode: "it",
    includedType: "lodging",
    maxResultCount: 20,
    locationRestriction: { rectangle: {
      low:  { latitude: ZONE.centro.lat - 0.62, longitude: ZONE.centro.lon - 0.90 },
      high: { latitude: ZONE.centro.lat + 0.62, longitude: ZONE.centro.lon + 0.90 }
    }}
  };
  if (pageToken) corpo.pageToken = pageToken;
  const r = await fetch("https://places.googleapis.com/v1/places:searchText", {
    method: "POST",
    headers: { "Content-Type":"application/json", "X-Goog-Api-Key": KEY, "X-Goog-FieldMask": CAMPI },
    body: JSON.stringify(corpo)
  });
  const j = await r.json().catch(() => ({}));
  if (!r.ok){
    const msg = (j.error && j.error.message) || r.statusText;
    if (r.status === 403 || r.status === 400) { console.error("\n✗ Places rifiuta la chiamata: " + msg + "\n  (chiave non abilitata, restrizioni troppo strette, o fatturazione non attiva)"); process.exit(2); }
    console.error("  ! " + r.status + " " + msg);
    return { places: [] };
  }
  return j;
}

/* ---- raccolta ---- */
const trovate = new Map();
const zone = PROVA ? ZONE.zone.slice(0, 3) : ZONE.zone;
let chiamate = 0;

for (const zona of zone){
  let token = null, pagina = 0;
  do {
    const res = await cerca("hotel " + zona, token);
    chiamate++;
    (res.places || []).forEach(p => { if (!trovate.has(p.id)) trovate.set(p.id, p); });
    token = res.nextPageToken || null;
    pagina++;
    await attendi(120);
  } while (token && pagina < 3);
  process.stdout.write("\r  " + zona.padEnd(34) + " → " + String(trovate.size).padStart(4) + " strutture, " + chiamate + " chiamate   ");
}
console.log("\n✓ Raccolta chiusa: " + trovate.size + " strutture distinte, " + chiamate + " chiamate a Places.");

/* ---- normalizzazione ---- */
const CATENE = ["falkensteiner","marriott","hilton","nh hotel","mercure","best western","sheraton","b&b hotel","ibis","radisson","accor","club med","tui blue","aminess","dolomiti wellness group"];
const comp = (p, tipo) => {
  const c = (p.addressComponents || []).find(x => (x.types || []).includes(tipo));
  return c ? (c.shortText || c.longText || "") : "";
};
const localita = comune => {
  const c = (comune || "").toLowerCase();
  if (/bolzano|bozen|merano|meran|bressanone|brixen|chiusa|klausen/.test(c)) return "Città d'arte";
  if (/caldaro|kaltern|carezza|lago/.test(c)) return "Lago";
  return "Montagna";
};

const righe = [...trovate.values()].map(p => {
  const lat = p.location && p.location.latitude, lon = p.location && p.location.longitude;
  const d = (lat != null && lon != null) ? km(ZONE.centro.lat, ZONE.centro.lon, lat, lon) : null;
  const nome = (p.displayName && p.displayName.text) || "";
  const tipi = p.types || [];
  const rec = p.userRatingCount || 0;
  const rat = p.rating || 0;
  const sito = p.websiteUri || "";
  // Pre-punteggio: reputazione alta = ha i soldi; sito assente = ha il problema.
  // Il punteggio vero lo calcola l'hub quando social e sito sono stati giudicati.
  const reputazione = Math.min(rec, 400) / 400 * Math.max(0, Math.min(1, (rat - 3.6) / 1.2));
  const potenziale = Math.round(60 * reputazione + (sito ? 0 : 40));
  return {
    placeId: p.id,
    nome,
    comune: comp(p, "administrative_area_level_3") || comp(p, "locality") || "",
    provincia: comp(p, "administrative_area_level_2") || "",
    regione: comp(p, "administrative_area_level_1") || "",
    indirizzo: p.formattedAddress || "",
    km: d == null ? null : Math.round(d),
    rating: rat || null,
    recensioni: rec || null,
    sito,
    telefono: p.nationalPhoneNumber || "",
    maps: p.googleMapsUri || "",
    fasciaPrezzo: p.priceLevel || "",
    tipoPrincipale: p.primaryType || "",
    tipi,
    stato: p.businessStatus || "",
    catena: CATENE.some(c => nome.toLowerCase().includes(c)),
    potenziale
  };
});

const scartate = [];
const buone = righe.filter(r => {
  const perche = [];
  if (r.stato && r.stato !== "OPERATIONAL") perche.push("non operativa (" + r.stato + ")");
  if (r.km == null || r.km > ZONE.raggioKm) perche.push("fuori raggio (" + r.km + " km)");
  if ((r.recensioni || 0) < 25) perche.push("meno di 25 recensioni");
  if (r.tipi.some(t => /campground|rv_park|camping/.test(t))) perche.push("campeggio");
  if (!r.tipi.some(t => /lodging|hotel|resort|bed_and_breakfast|guest_house|inn/.test(t))) perche.push("non è una struttura ricettiva");
  if (perche.length){ scartate.push({ nome:r.nome, comune:r.comune, perche }); return false; }
  return true;
}).sort((a,b) => b.potenziale - a.potenziale || (b.recensioni||0) - (a.recensioni||0));

fs.mkdirSync(USCITA, { recursive: true });
fs.writeFileSync(path.join(USCITA, "strutture-grezze.json"), JSON.stringify({
  fonte: "Google Places API (New) · places:searchText",
  raccoltoIl: new Date().toISOString().slice(0,10),
  centro: ZONE.centro, raggioKm: ZONE.raggioKm,
  chiamate, trovate: righe.length, inTarget: buone.length,
  strutture: righe, scartate
}, null, 2));

/* ---- le prime N nello schema dell'hub ---- */
const oggi = new Date().toISOString().slice(0,10);
const scelte = buone.slice(0, QUANTE).map(r => ({
  _placeId: r.placeId,
  nome: r.nome,
  verticale: "Hotel di lusso",
  categoria: "Non classificato",
  tipoLocalita: localita(r.comune),
  comune: r.comune, provincia: r.provincia, regione: r.regione,
  apertura: "Da verificare",
  stato: "Da valutare",
  canale: "Da definire",
  km: r.km,
  lingua: "Italiano + Tedesco",
  catena: r.catena,
  sito: { url: r.sito, assente: !r.sito, voto: 0, nota: r.sito ? "" : "Nessun sito trovato su Google: da confermare a mano" },
  seo: { voto: 0, nota: "" },
  google: { rating: r.rating, recensioni: r.recensioni, nota: "Da Google Places il " + oggi },
  note: [r.indirizzo, r.telefono, r.maps].filter(Boolean).join(" · "),
  creataIl: oggi
}));

fs.writeFileSync(path.join(USCITA, "strutture-50.json"), JSON.stringify({
  fonte: "Google Places API (New)", raccoltoIl: oggi, quante: scelte.length, strutture: scelte
}, null, 2));

console.log("✓ In target (entro " + ZONE.raggioKm + " km, ≥25 recensioni, operative): " + buone.length);
console.log("✓ Scritti:");
console.log("   benchmark/dati/strutture-grezze.json  (" + righe.length + " strutture + " + scartate.length + " scartate con il motivo)");
console.log("   benchmark/dati/strutture-50.json      (" + scelte.length + " pronte per l'hub)");
console.log("\nPrime 10 per potenziale:");
buone.slice(0,10).forEach((r,i) => console.log(
  "  " + String(i+1).padStart(2) + ". " + r.nome.slice(0,42).padEnd(44) +
  (r.comune || "–").padEnd(22) + String(r.km).padStart(3) + " km  " +
  (r.rating ? r.rating + "★" : "–") + " (" + (r.recensioni||0) + ")" + (r.sito ? "" : "  · senza sito")
));
