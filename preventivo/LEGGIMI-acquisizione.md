# Proposta di acquisizione · verticale ospitalità

> **Stato al 24/11: in pausa, non va mandata così.** La versione su Hotel Heubad è un
> esercizio di impaginazione. La proposta vera si costruisce **quando un cliente si dimostra
> interessato**, su misura, dopo la brochure. Prima di riprenderla, leggere il brief qui sotto.

## Il brief per la proposta vera (feedback del 24/11)

Si parla di cifre alte: la proposta deve essere **più articolata** di un preventivo a schema.

1. **In linea con la brochure**, non con il preventivo standard.
2. **Tante immagini del loro territorio e della struttura.** Si fa leva sui punti di forza e
   di debolezza **della zona e della struttura**, non solo dei profili social.
3. **Ci presentiamo come studio, non come organigramma.** Niente «Alessandro fa l'ADV,
   Nadir il sito». Il messaggio è: *queste sono le cose che faremo, siamo un team.*
4. **Prezzo unico da studio.** «La proposta ad hoc per voi è X mila euro per X, Y, Z.» Chi
   fattura cosa si spiega **in fase di chiusura**, non nel documento.
5. **Manca il perché sceglierci**, cioè quello che ha fatto la differenza a Villa Campomaggio:
   - chat sempre attiva;
   - un referente, ma sempre qualcun altro pronto a intervenire;
   - un team dedicato al progetto;
   - cura delle varie pagine perché siano coerenti fra loro;
   - shooting stagionali;
   - identità visiva sia nelle foto sia nei video;
   - copywriting in più lingue, se serve.
6. **Il sito non è nel pacchetto di base.** Si decide caso per caso:
   - **subito**, se la loro situazione web è critica;
   - **dopo**, come cross-sell, una volta fatta la proposta lato marketing.
7. **L'advertising va spiegato molto di più.** È la parte che può fare la differenza e cambia
   tutto a seconda dell'obiettivo:
   - campagna di **notorietà o traffico al profilo**: una cosa;
   - campagna con **obiettivo prenotazioni**: un'altra, che proponiamo noi.
8. **Solo casi studio di ospitalità.**

Il generatore qui sotto resta valido come motore (brand, font, loghi, controllo
sforamenti): cambia la struttura delle pagine, non l'impianto.

---

**Cos'è.** La proposta che portiamo a una struttura che non ci conosce: gestione social,
gestione advertising, sviluppo e gestione del sito web, con il prezzo di ciascuno e il
quadro economico del primo anno.

Compilata su **Hotel Heubad** (Fiè allo Sciliar), presa dalla lista dell'hub. Per un'altra
struttura si cambiano `STRUTTURA` e `ANALISI` in testa allo script.

- `Proposta ospitalita - Hotel Heubad.pdf` · 9 pagine, 16:9
- `_anteprime_acquisizione/` · una PNG per pagina
- `build_proposta_acquisizione.py` + `rendi.mjs` · rigenerano tutto in pochi secondi
- `brand/` · marchio, font, icone, loghi e copertina (vedi `brand/LEGGIMI.md`)

## Il brand è quello del documento standard, non un'imitazione

L'impianto visivo è quello della proposta standard di Riccardo (Love Luck Tattoo,
novembre 2026). Gli asset non sono ridisegnati: **sono estratti da quel PDF**.

| Cosa | Da dove |
|---|---|
| Marchio YDG Studio, chiaro e scuro | immagini del PDF di Riccardo |
| Sfondo della copertina con l'alone arancio | immagine 1920×1080 del PDF di Riccardo |
| Le nove icone di «cosa fa lo studio» | immagini del PDF di Riccardo |
| I quindici loghi dei clienti | immagini del PDF di Riccardo |
| Font Overused Grotesk, Book e SemiBold | lo stesso incorporato nel PDF; open source, licenza OFL |
| Palette | misurata sui pixel delle pagine: `#F2F2F2`, `#1A1A1A`, `#4D4D4D`, `#FF7900`, `#F3E3D4` |

Elementi ricorrenti presi uguali: testata con marchio e «Proposta di collaborazione ·
nome» su ogni pagina, numerazione `02 / 09` in basso a sinistra, occhiello col quadratino
arancio sulle pagine chiare e arancio senza quadratino su quelle scure, card scure con la
barra arancio in cima, card grigie sulle pagine scure, tabella economica con la fascia
`#F3E3D4` e la barra arancio a sinistra, chiusura arancio piena.

Non serve più rigenerarlo sul Mac: font e marchio sono veri anche qui.

## Le 9 pagine

| | Pagina | Cosa c'è |
|---|---|---|
| 1 | Copertina | «Facciamo crescere Hotel Heubad» sullo sfondo vero |
| 2 | Chi siamo | i cinque servizi dell'ospitalità e i sette clienti del settore |
| 3 | Casi studio | Villa Campomaggio, La Gabbia, L'Alóz |
| 4 | Analisi iniziale | cosa funziona già · dove possiamo crescere · dove vogliamo andare |
| 5 | Il servizio | i tre servizi, ognuno col suo referente e cinque voci |
| 6 | La proposta | avvio e gestione di ciascun servizio |
| 7 | Investimento | il riepilogo del primo anno, con il totale |
| 8 | Prossimi passi | i cinque passi per partire e i servizi su richiesta |
| 9 | Grazie | contatti e validità |

**Perché non parte dai numeri della struttura.** Campomaggio è un rinnovo: i numeri
dell'anno prima li abbiamo fatti noi. Qui la struttura non ci conosce e noi non sappiamo
come lavora. In pagina 4 ci sono solo osservazioni da fuori, dichiarate come tali; i
numeri veri sono quelli dei nostri clienti, in pagina 3.

## È verticale: solo ospitalità

Il documento standard dello studio mostra tutti i settori. Questo no: è il modo in cui ci
presentiamo agli hotel, quindi in pagina 2 restano solo i clienti del settore (Villa
Campomaggio, La Gabbia, Spiedo Imperiale, L'Alóz, Ca' Rossi, La Piadina della Baracchina,
Bocon Divino) e i cinque servizi che vendiamo qui. Il numero complessivo, «oltre 50
attività», resta in una card a parte: è vero e dà peso, ma non mescola i loghi.

**L'Alóz** non ha numeri in nessuna fonte, e oggi non è in gestione: è stato un lancio una
tantum (giugno 2026). La sua card racconta cosa era e cosa abbiamo fatto, non risultati, e
nessuna parola fa pensare a un presidio continuativo. Il titolo della pagina dice «con
cui abbiamo lavorato», non «che seguiamo». Prima di usarla serve il permesso di Enrica
Maccolini a citarla per nome.

**Il suo logo manca**: in pagina 2 e 3 esce un monogramma provvisorio, e lo script lo
segnala a fine resa. Basta mettere il logo, tondo e con fondo trasparente, in
`brand/clienti/aloz.png` e rigenerare.

## Da dove vengono i numeri

| Dove | Fonte |
|---|---|
| P3 casi studio | proposta di rinnovo 2027 Campomaggio; proposta Love Luck per La Gabbia; DOCUMENTO UNICO caso 6 per L'Alóz |
| P4 analisi | scheda dell'hub, Google Places del 16/10/2026 |
| P6 sito, portali, tracciamento | listino Nadir, caso B (sito da rifare) |
| P6 advertising | DOCUMENTO UNICO, minimo 500 €/mese se presa da sola |
| P7 budget inserzioni | DOCUMENTO UNICO, 400-600 €/mese |

**Da approvare prima che esca dallo studio: le cifre del social.** 1.400 €/mese in alta
stagione, 900 € in bassa, 3.500 € di shooting di avvio. Nel DOCUMENTO UNICO la gestione
è 1.200/2.000, ma per **due brand** (Campomaggio) — e il documento stesso dice che per una
struttura sola va rivista. Qui è scalata su un brand solo, non dimezzata.

**Volutamente assente**: la riga «operazione in regime forfettario, IVA non applicata»
del documento di Riccardo. È il suo regime personale; qui si fattura in tre, con partite
IVA diverse.

## Stagionalità

L'Alto Adige lavora **due** stagioni, inverno ed estate (decisione del 10/11): alta
stagione 8 mesi, dicembre-marzo e giugno-settembre; bassa i 4 di mezzo. Campomaggio, in
Toscana, ne ha una sola.

## Controllo degli sforamenti

`rendi.mjs` misura l'altezza reale del contenuto di ogni pagina e segnala quelle che
superano i 720px. Esclude gli elementi `position:absolute` e quelli inline, che
segnalerebbero sforamenti inesistenti.
