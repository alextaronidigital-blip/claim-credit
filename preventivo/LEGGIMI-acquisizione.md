# Proposta di acquisizione · verticale ospitalità

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
| 2 | Chi siamo | cosa fa lo studio (9 icone) e chi ci ha scelto (15 loghi) |
| 3 | Casi studio | Villa Campomaggio, La Gabbia, Romagna Free: quattro numeri ciascuno |
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

## Da dove vengono i numeri

| Dove | Fonte |
|---|---|
| P3 casi studio | proposta di rinnovo 2027 Campomaggio; proposta Love Luck per La Gabbia e Romagna Free |
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
