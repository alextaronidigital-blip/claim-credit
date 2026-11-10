#!/usr/bin/env node
/* YDG · Sceglie le 50 dal raccolto. Nessuna nuova chiamata a Places.
   Legge: strutture-grezze.json (Places) + social-homepage.json (link social)
   Scrive: strutture-50.json (schema hub) + strutture-50.md (da leggere)

   Entra tutto il bacino, ordinato. Il bersaglio sta in cima: struttura che
   LAVORA BENE (Google alto, molte recensioni) ma COMUNICA MALE (social
   assenti o non presidiati) — ha i soldi e ha il problema. Fuori restano solo
   garni/pensioni/residence e chi su Google lavora male; le 5 stelle entrano
   ma segnate. Stringere la lista tocca a chi fa outreach, non a questo file.

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
/* Nessun tetto: entra tutto il bacino. La rosa non la stringiamo noi, la
   stringe chi fa outreach, che ha il contesto per farlo. Un numero si puo'
   ancora passare da riga di comando, per guardare solo le prime N. */
const QUANTE = Number(process.argv[2]) || Infinity;

/* Il raccolto di ottobre e' precedente alle quattro aree: ha un centro solo,
   Siusi, e nessun campo "area". Glielo attribuiamo qui, senza inventare: tutto
   quel raccolto stava per definizione nel raggio di Siusi. */
const VECCHIO = !!grezzo.centro && !grezzo.aree;
const areaDi = r => r.area || (VECCHIO ? "siusi" : "");
if (VECCHIO) console.log("(raccolto in formato vecchio, centro unico " + grezzo.centro.nome + ": attribuito tutto all'area Siusi)");

/* --- le stelle, che Google non espone: compilate a mano in stelle.json --- */
const STELLE = JSON.parse(fs.readFileSync(path.join(import.meta.dirname, "stelle.json"), "utf8"));
const piatto = n => (n || "")
  .toLowerCase()
  .normalize("NFD").replace(/[\u0300-\u036f]/g, "")
  .replace(/&/g, " e ")
  .replace(/[^a-z0-9]+/g, " ")
  .trim();
const CINQUE = new Map(STELLE.cinqueStelle.map(x => [piatto(x.nome), x.comune ? piatto(x.comune) : null]));
// Marcatori che una struttura si mette da sola in casa: li leggiamo, non li deduciamo.
const CINQUE_NOME = /\b5\s*(stelle|sterne|star)\b|\*{5}|relais & ch|\bluxury (maison|lodge|retreat)\b/i;
function cinqueStelle(r){
  const n = piatto(r.nome);
  // Corrispondenza esatta sul nome normalizzato, piu' il comune dove serve:
  // "Hotel La Perla" di Corvara e' 5 stelle, l'omonimo di Canazei no;
  // "Alpenroyal Hotel" di Selva e' 5 stelle, "Hotel Alpenroyal" di Castelrotto no.
  if (CINQUE.has(n)) {
    const c = CINQUE.get(n);
    if (!c || c === piatto(r.comune)) return "censita a mano come 5 stelle";
  }
  if (CINQUE_NOME.test(r.nome || "")) return "il nome dichiara 5 stelle / lusso";
  return null;
}

const ZONE = JSON.parse(fs.readFileSync(path.join(import.meta.dirname, "comuni.json"), "utf8"));
const MAXKM = ZONE.raggioSceltaKm || 35, MINRAT = 4.3, MINREC = 80;

/* Seconda porta, per la fascia 3 stelle. Un 3 stelle di valle ha meno
   recensioni di un 4 superior pur lavorando bene: la soglia di 80 lo tagliava
   fuori per dimensione, non per qualita'. Chi ha poche recensioni ma un voto
   alto entra lo stesso, segnato, cosi' si vede da dove e' passato. */
const MINREC_PICCOLE = 30, MINRAT_PICCOLE = 4.5;
const piccolaMaBuona = r => (r.recensioni || 0) >= MINREC_PICCOLE
  && (r.recensioni || 0) < MINREC && (r.rating || 0) >= MINRAT_PICCOLE;
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
  else if (piccolaMaBuona(r)) add(15, "Piccola ma ben giudicata (" + rec + " recensioni, " + rat + "\u2605)");
  else if (rec <= 800) add(10, rec + " recensioni");
  else if (rec > 1200) add(-15, "Macchina già rodata (" + rec + " recensioni): quasi sempre con agenzia");

  // Il problema da vendere: lavora bene e non comunica.
  if (!r.sito) add(40, "Nessun sito web");
  else if (s && s.nota && s.nota.startsWith("Sito non leggibile")) add(0, "Sito non leggibile dal bot: social da verificare");
  else if (s && s.trovati === 0) add(35, "Nessun link social in homepage (da verificare)");
  else if (s && !s.social.instagram) add(15, "Instagram non linkato in homepage");
  else if (s && s.trovati <= 1) add(8, "Un solo social linkato");

  const dove = r.daCentro || "Siusi";
  if (r.km <= 20) add(12, "A " + r.km + " km da " + dove); else add(8, "A " + r.km + " km da " + dove);

  // Decisione del 10/11: le catene restano dentro, non si escludono a priori.
  // Resta una penalita' lieve, perche' il marketing centralizzato e' comunque
  // un ostacolo: lo si scopre al primo contatto.
  if (r.catena) add(-5, "Catena o gruppo: marketing forse centralizzato, da scoprire al contatto");
  if (GRANDI.test(r.nome)) add(-10, "Grande resort: già presidiato");
  if (cinqueStelle(r)) add(-45, "5 stelle: fuori dalla fascia 4★ / 4★ superior");

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
  if (r.km == null || r.km > MAXKM) perche.push("oltre " + MAXKM + " km dal centro della sua area (" + r.km + ")");
  if ((r.rating || 0) < MINRAT) perche.push("rating sotto " + MINRAT + " (" + (r.rating || "–") + "): non lavora bene");
  if ((r.recensioni || 0) < MINREC && !piccolaMaBuona(r))
    perche.push("troppo poche recensioni (" + (r.recensioni || 0) + "): ne servono " + MINREC + ", o " + MINREC_PICCOLE + " con almeno " + MINRAT_PICCOLE + "\u2605");
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
/* Le 5 stelle non entrano nella rosa, ma non si buttano: restano in coda
   marcate "Non in target", cosi in hub si vedono barrate col motivo. */
const inGioco = valutate.filter(r => !cinqueStelle(r));
const fuoriFascia = valutate.filter(r => cinqueStelle(r));
const scelte = inGioco.slice(0, QUANTE).concat(fuoriFascia);

fs.writeFileSync(path.join(DATI, "strutture-50.json"), JSON.stringify({
  fonte: "Google Places API (New) del " + grezzo.raccoltoIl + " + link social letti dalle homepage",
  selezionatoIl: oggi,
  aree: ZONE.aree.map(a => ({ id:a.id, nome:a.nome, quante: scelte.filter(r => areaDi(r) === a.id && !cinqueStelle(r)).length })),
  criteri: "Entro " + MAXKM + " km dal centro della propria area, ≥" + MINRAT + "★, ≥" + MINREC + " recensioni, hotel (no garni/pensioni/residence), fascia da 3\u2605 a 4\u2605 superior. Ordinate per: social assenti o non presidiati, reputazione, dimensione, vicinanza.",
  nonSappiamo: "Stelle, stagionalità e follower: da compilare in hub. Un social non trovato dal bot è DA VERIFICARE, non assente.",
  bersaglio: STELLE._bersaglio,
  bacino: bacino.length, fuoriBacino: fuori.length,
  quante: inGioco.length, fuoriFascia: fuoriFascia.length,
  strutture: scelte.map(r => {
    const s = r.s || {};
    const social = {};
    ["instagram","facebook","tiktok","youtube","linkedin"].forEach(k => {
      social[k] = { presente: !!(s.social && s.social[k]), daProporre: !(s.social && s.social[k]), handle: (s.social && s.social[k]) || "", follower: null };
    });
    const cinque = cinqueStelle(r);
    return {
      _placeId: r.placeId,
      nome: r.nome, verticale: "Hotel di lusso",
      categoria: cinque ? "5 stelle" : "Non classificato",
      tipoLocalita: localita(r.comune),
      comune: r.comune, provincia: r.provincia, regione: r.regione,
      area: r.areaNome || (ZONE.aree.find(a => a.id === areaDi(r)) || {nome:""}).nome,
      apertura: "Da verificare",
      stato: cinque ? "Non in target" : "Da valutare",
      motivoEsclusione: cinque
        ? "Fuori fascia: 5 stelle (" + cinque + "). Il bersaglio va da 3\u2605 a 4\u2605 superior."
        : "",
      canale: "Da definire",
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
  (cinqueStelle(r) ? "`FUORI` " : "") + (piccolaMaBuona(r) ? "`piccola` " : "") + r.nome.replace(/\|/g,"/"), r.comune || "–",
  (ZONE.aree.find(a => a.id === areaDi(r)) || {nome:"–"}).nome.split(" ")[0], r.km + " km",
  r.rating + "★ (" + r.recensioni + ")", segnale(r), r.v.totale
].join(" | ") + " |";

fs.writeFileSync(path.join(DATI, "strutture-50.md"),
  "# Le " + inGioco.length + " strutture in gioco, piu' " + fuoriFascia.length + " fuori fascia\n\n" +
  "**Fonte**: Google Places API (New), raccolto il " + grezzo.raccoltoIl + " · **social**: link letti dalle homepage.\n\n" +
  "**Aree**: " + ZONE.aree.map(a => a.nome + " (" + scelte.filter(r => areaDi(r) === a.id && !cinqueStelle(r)).length + ")").join(" · ") + "\n\n" +
  "**Bacino**: " + bacino.length + " hotel entro " + MAXKM + " km dal centro della propria area, almeno " + MINRAT + "★ e " + MINREC +
  " recensioni, esclusi garni, pensioni e residence (" + fuori.length + " scartate, col motivo, in `strutture-escluse.json`).\n\n" +
  "**Come sono ordinate**: in cima chi lavora bene su Google e non comunica — nessun sito, nessun social linkato, Instagram assente. È il bersaglio dell'hub: ha i soldi e ha il problema.\n\n" +
  "**Attenzione**: «nessun social» vuol dire *nessun link trovato nella homepage*, non che il profilo non esista. Va guardato a mano prima di dirlo al titolare.\n" +
  "**Soglia**: almeno " + MINREC + " recensioni, oppure " + MINREC_PICCOLE + " con almeno " + MINRAT_PICCOLE + "\u2605 \u2014 la seconda porta serve ai 3 stelle, piccoli ma non per questo deboli. In tabella sono segnate `piccola`.\n" +
  "**Fascia**: bersaglio da 3\u2605 a 4\u2605 superior. Le " + fuoriFascia.length + " strutture da 5 stelle stanno in coda alla tabella, segnate `FUORI`, non buttate.\n" +
  "**Le stelle Google non le espone**: quelle che sappiamo stanno in `strumenti/stelle.json`, compilate a mano. Chi non c'\u00e8 resta da verificare.\n" +
  "**La distanza è in linea d'aria** e si misura dal centro della sua area: 30 km di Dolomiti sono spesso un'ora di guida.\n\n" +
  "| Struttura | Comune | Area | Distanza | Google | Social in homepage | Presel. |\n|---|---|---|---|---|---|---|\n" +
  scelte.map(riga).join("\n") + "\n");

console.log("Bacino: " + bacino.length + " · scartate: " + fuori.length + " · in gioco: " + inGioco.length + " · 5 stelle fuori fascia: " + fuoriFascia.length);
console.log("Entrate dalla porta piccola (" + MINREC_PICCOLE + "-" + (MINREC-1) + " recensioni, \u2265" + MINRAT_PICCOLE + "\u2605): " + scelte.filter(piccolaMaBuona).length);
console.log("Fra le scelte — senza sito: " + scelte.filter(r => !r.sito).length +
            " · nessun social in homepage: " + scelte.filter(r => r.sito && r.s && r.s.trovati === 0).length +
            " · senza Instagram: " + scelte.filter(r => r.s && r.s.trovati > 0 && !r.s.social.instagram).length);
ZONE.aree.forEach(a => console.log("  " + a.nome.slice(0,44).padEnd(46) + String(scelte.filter(r => areaDi(r) === a.id && !cinqueStelle(r)).length).padStart(3) + " in rosa"));
console.log("Entro 20 km: " + scelte.filter(r => r.km <= 20).length + " · 21-35 km: " + scelte.filter(r => r.km > 20).length);
console.log("\nPrime 15:");
scelte.slice(0,15).forEach((r,i) => console.log("  " + String(i+1).padStart(2) + ". " + r.nome.slice(0,38).padEnd(40) + (r.comune||"–").slice(0,16).padEnd(18) + String(r.km).padStart(3) + " km  " + r.rating + "★ (" + r.recensioni + ")  " + segnale(r).replace(/\*\*/g,"") + "  [" + r.v.totale + "]"));
