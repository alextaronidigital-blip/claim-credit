#!/usr/bin/env node
/* YDG · Sceglie le 50 dal raccolto. Nessuna nuova chiamata a Places.
   Legge: strutture-grezze.json (Places) + social-homepage.json (link social)
   Scrive: strutture-50.json (schema hub) + strutture-50.md (da leggere)

   Il bersaglio dell'hub: struttura che LAVORA BENE (Google alto, molte
   recensioni) ma COMUNICA MALE (social assenti o non presidiati). Ha i soldi
   e ha il problema. Fuori fascia: 5★ lusso e grandi resort (già con agenzia),
   garni/pensioni/residence (non reggono una fee da 10k/mese).

   Quello che NON sappiamo e non inventiamo: le stelle, la stagionalità, i
   follower. Escono "Non classificato" / "Da verificare" e si compilano in hub.
   La fascia di prezzo Google non la dà per nessun hotel: criterio eliminato.
*/
import fs from "node:fs";
import path from "node:path";

const RADICE = path.resolve(import.meta.dirname, "..", "..");
const DATI = path.join(RADICE, "benchmark", "dati");
const grezzo = JSON.parse(fs.readFileSync(path.join(DATI, "strutture-grezze.json"), "utf8"));
const socialFile = path.join(DATI, "social-homepage.json");
const soc = fs.existsSync(socialFile) ? JSON.parse(fs.readFileSync(socialFile, "utf8")) : { strutture: [] };
const SOC = new Map(soc.strutture.map(s => [s.placeId, s]));
const QUANTE = Number(process.argv[2]) || 50;

const MAXKM = 35, MINRAT = 4.3, MINREC = 80;
const GRANDI = /\bresort\b|\bslh\b|relais & ch|luxury|\bspa resort\b/i;
const FUORIFASCIA = /\bgarni\b|pension|pensione|residence|appartement|apartments|appartamenti|camping|rifugio|ostello|hostel|\brooms\b|zimmer|\bbaita\b|\bb&b\b|bed (and|&) breakfast/i;
const TIPI_OK = /^(hotel|resort_hotel|lodging|inn|extended_stay_hotel)$/;

function valuta(r, s){
  const parti = []; let t = 0;
  const add = (p, perche) => { if (p) { t += p; parti.push([p, perche]); } };
  const rat = r.rating || 0, rec = r.recensioni || 0;

  if (rat >= 4.6) add(20, "Reputazione eccellente (" + rat + "★)");
  else add(15, "Buona reputazione (" + rat + "★)");

  if (rec >= 80 && rec <= 500) add(20, "Dimensione giusta (" + rec + " recensioni)");
  else if (rec <= 800) add(10, rec + " recensioni");
  else if (rec > 1200) add(-15, "Macchina già rodata (" + rec + " recensioni): quasi sempre con agenzia");

  // Il problema da vendere: lavora bene e non comunica.
  if (!r.sito) add(40, "Nessun sito web");
  else if (s && s.nota && s.nota.startsWith("Sito non leggibile")) add(0, "Sito non leggibile dal bot: social da verificare");
  else if (s && s.trovati === 0) add(35, "Nessun link social in homepage (da verificare)");
  else if (s && !s.social.instagram) add(15, "Instagram non linkato in homepage");
  else if (s && s.trovati <= 1) add(8, "Un solo social linkato");

  if (r.km <= 20) add(12, "A " + r.km + " km da Siusi"); else add(8, "A " + r.km + " km da Siusi");

  if (r.catena) add(-20, "Catena o gruppo: marketing centralizzato");
  if (GRANDI.test(r.nome)) add(-10, "Grande resort: già presidiato");

  return { totale: Math.max(0, Math.min(100, t)), parti: parti.sort((a,b) => b[0]-a[0]) };
}

const localita = c => {
  const x = (c || "").toLowerCase();
  if (/bolzano|bozen|merano|meran|bressanone|brixen|chiusa|klausen/.test(x)) return "Città d'arte";
  if (/caldaro|kaltern|carezza|lago/.test(x)) return "Lago";
  return "Montagna";
};

const fuori = [];
const bacino = grezzo.strutture.filter(r => {
  const perche = [];
  if (r.km == null || r.km > MAXKM) perche.push("oltre " + MAXKM + " km (" + r.km + ")");
  if ((r.rating || 0) < MINRAT) perche.push("rating sotto " + MINRAT + " (" + (r.rating || "–") + "): non lavora bene");
  if ((r.recensioni || 0) < MINREC) perche.push("meno di " + MINREC + " recensioni");
  if (r.stato && r.stato !== "OPERATIONAL") perche.push("non operativa");
  if (!TIPI_OK.test(r.tipoPrincipale || "")) perche.push("tipo " + (r.tipoPrincipale || "ignoto"));
  if (FUORIFASCIA.test(r.nome)) perche.push("garni / pensione / residence: fuori fascia di spesa");
  // Scheda senza via (indirizzo che parte dal CAP): voce di località, non una struttura.
  if (/^\s*\d{5}\s/.test(r.indirizzo || "")) perche.push("scheda Google senza indirizzo vero: non è una struttura");
  if (perche.length){ fuori.push({ nome:r.nome, comune:r.comune, perche }); return false; }
  return true;
});

const valutate = bacino
  .map(r => { const s = SOC.get(r.placeId); return { ...r, s, v: valuta(r, s) }; })
  .sort((a,b) => b.v.totale - a.v.totale || (b.recensioni||0) - (a.recensioni||0));

const oggi = new Date().toISOString().slice(0,10);
const scelte = valutate.slice(0, QUANTE);

fs.writeFileSync(path.join(DATI, "strutture-50.json"), JSON.stringify({
  fonte: "Google Places API (New) del " + grezzo.raccoltoIl + " + link social letti dalle homepage",
  selezionatoIl: oggi,
  criteri: "Entro " + MAXKM + " km da Siusi, ≥" + MINRAT + "★, ≥" + MINREC + " recensioni, hotel (no garni/pensioni/residence). Ordinate per: social assenti o non presidiati, reputazione, dimensione, vicinanza.",
  nonSappiamo: "Stelle, stagionalità e follower: da compilare in hub. Un social non trovato dal bot è DA VERIFICARE, non assente.",
  bacino: bacino.length, fuoriBacino: fuori.length, quante: scelte.length,
  strutture: scelte.map(r => {
    const s = r.s || {};
    const social = {};
    ["instagram","facebook","tiktok","youtube","linkedin"].forEach(k => {
      social[k] = { presente: !!(s.social && s.social[k]), daProporre: !(s.social && s.social[k]), handle: (s.social && s.social[k]) || "", follower: null };
    });
    return {
      _placeId: r.placeId,
      nome: r.nome, verticale: "Hotel di lusso", categoria: "Non classificato",
      tipoLocalita: localita(r.comune),
      comune: r.comune, provincia: r.provincia, regione: r.regione,
      apertura: "Da verificare", stato: "Da valutare", canale: "Da definire",
      km: r.km, lingua: "Italiano + Tedesco", catena: r.catena,
      sito: { url: r.sito, assente: !r.sito, voto: 0, nota: r.sito ? "" : "Nessun sito su Google: da confermare a mano" },
      seo: { voto: 0, nota: "" },
      google: { rating: r.rating, recensioni: r.recensioni, nota: "Da Google Places il " + grezzo.raccoltoIl },
      social,
      note: [r.indirizzo, r.telefono, r.maps, s.nota].filter(Boolean).join(" · "),
      _preselezione: r.v.totale,
      _perche: r.v.parti.map(p => (p[0] > 0 ? "+" : "") + p[0] + " " + p[1]),
      creataIl: oggi
    };
  })
}, null, 2));

fs.writeFileSync(path.join(DATI, "strutture-escluse.json"), JSON.stringify({ quante: fuori.length, escluse: fuori }, null, 2));

const segnale = r => {
  const s = r.s;
  if (!r.sito) return "**nessun sito**";
  if (s && s.nota && s.nota.startsWith("Sito non leggibile")) return "da verificare";
  if (!s || s.trovati === 0) return "**nessun social**";
  const k = Object.keys(s.social);
  return k.length + " (" + k.map(x => x.slice(0,2).toUpperCase()).join(" ") + ")";
};
const riga = r => "| " + [
  r.nome.replace(/\|/g,"/"), r.comune || "–", r.km + " km",
  r.rating + "★ (" + r.recensioni + ")", segnale(r), r.v.totale
].join(" | ") + " |";

fs.writeFileSync(path.join(DATI, "strutture-50.md"),
  "# Le " + scelte.length + " strutture — primo giro\n\n" +
  "**Fonte**: Google Places API (New), raccolto il " + grezzo.raccoltoIl + " · **social**: link letti dalle homepage.\n\n" +
  "**Bacino**: " + bacino.length + " hotel entro " + MAXKM + " km da " + grezzo.centro.nome + ", almeno " + MINRAT + "★ e " + MINREC +
  " recensioni, esclusi garni, pensioni e residence (" + fuori.length + " scartate, col motivo, in `strutture-escluse.json`).\n\n" +
  "**Come sono ordinate**: in cima chi lavora bene su Google e non comunica — nessun sito, nessun social linkato, Instagram assente. È il bersaglio dell'hub: ha i soldi e ha il problema.\n\n" +
  "**Attenzione**: «nessun social» vuol dire *nessun link trovato nella homepage*, non che il profilo non esista. Va guardato a mano prima di dirlo al titolare.\n" +
  "**Le stelle non ci sono**: Google non le espone. Categoria e stagionalità si compilano in hub.\n" +
  "**La distanza è in linea d'aria**: 30 km di Dolomiti sono spesso un'ora di guida.\n\n" +
  "| Struttura | Comune | Distanza | Google | Social in homepage | Presel. |\n|---|---|---|---|---|---|\n" +
  scelte.map(riga).join("\n") + "\n");

console.log("Bacino: " + bacino.length + " · scartate: " + fuori.length + " · scelte: " + scelte.length);
console.log("Fra le scelte — senza sito: " + scelte.filter(r => !r.sito).length +
            " · nessun social in homepage: " + scelte.filter(r => r.sito && r.s && r.s.trovati === 0).length +
            " · senza Instagram: " + scelte.filter(r => r.s && r.s.trovati > 0 && !r.s.social.instagram).length);
console.log("Entro 20 km: " + scelte.filter(r => r.km <= 20).length + " · 21-35 km: " + scelte.filter(r => r.km > 20).length);
console.log("\nPrime 15:");
scelte.slice(0,15).forEach((r,i) => console.log("  " + String(i+1).padStart(2) + ". " + r.nome.slice(0,38).padEnd(40) + (r.comune||"–").slice(0,16).padEnd(18) + String(r.km).padStart(3) + " km  " + r.rating + "★ (" + r.recensioni + ")  " + segnale(r).replace(/\*\*/g,"") + "  [" + r.v.totale + "]"));
