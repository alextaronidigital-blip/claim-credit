# Proposta di acquisizione · verticale ospitalità

**Cos'è.** La proposta che portiamo a una struttura che non ci conosce. Tre servizi in un
documento solo — gestione social, gestione advertising, sviluppo e gestione del sito web —
ognuno con la sua pagina e il suo prezzo, più il quadro economico complessivo.

Compilata su **Hotel Heubad** (Fiè allo Sciliar), presa dalla lista dell'hub. Per un'altra
struttura si cambiano `STRUTTURA`, `ANALISI` e `DIREZIONE` in testa allo script.

- `Proposta ospitalita - Hotel Heubad.pdf` · 15 pagine, 16:9
- `_anteprime_acquisizione/` · una PNG per pagina
- `build_proposta_acquisizione.py` + `rendi.mjs` · rigenerano tutto

## È una fusione di due documenti che esistevano già

| Da | Cosa prende |
|---|---|
| **Love Luck Tattoo** (Riccardo, nov 2026) | l'impianto: testata e numerazione su ogni pagina, chi siamo, chi ci ha scelto, casi studio, analisi in superficie, servizi, prezzi, prossimi passi, chiusura arancio |
| **Villa Campomaggio** (rinnovo 2027) | il rigore tipografico, la profondità sui servizi, l'economia divisa per voci |

**Perché non parte dai numeri.** Campomaggio è un rinnovo: i numeri dell'anno precedente
li abbiamo fatti noi, quindi aprire con quelli ha senso. Qui la struttura non ci conosce e
noi non sappiamo come lavora davvero. Si analizza in superficie quello che si vede da
fuori, se ne spiegano le potenzialità, e si passa subito ai servizi e al loro costo.

## Le 15 pagine

1 Copertina · 2 Chi siamo · 3 Hanno scelto YDG Studio · 4 Casi studio ·
5 **Da dove partiamo** (cosa funziona già / dove possiamo crescere) · 6 Dove vogliamo
andare · 7 I tre servizi · 8 Gestione social · 9 Gestione advertising ·
10 Sviluppo e gestione del sito · 11 Quanto costa, servizio per servizio ·
12 Il riepilogo economico · 13 Cosa potremmo fare di più · 14 Come partiamo · 15 Grazie

## Da dove vengono i numeri

| Dove | Fonte |
|---|---|
| P4 casi studio | Proposta di rinnovo 2027 Campomaggio, consuntivo 2026, proposta Love Luck |
| P5 analisi | scheda dell'hub, Google Places del 16/10/2026 |
| P10-P11 sito, portali, tracciamento | listino Nadir, caso B (sito da rifare) |
| P9 budget pubblicitario | DOCUMENTO UNICO, 400-600 €/mese |
| P11 advertising | DOCUMENTO UNICO, minimo 500 €/mese se presa da sola |

**L'unica cosa non ancora approvata: le due cifre del social organico** (1.400 €/mese in
alta, 900 € in bassa) e lo shooting di avvio a 3.500 €. Nel DOCUMENTO UNICO le cifre di
gestione sono 1.200/2.000, ma sono quelle di Campomaggio **per due brand** — e il
documento stesso dice che per una struttura sola vanno riviste. Qui sono scalate su un
brand solo, non dimezzate: i costi fissi non si dimezzano. **Vanno confermate da Alex,
Riccardo e Alessandro prima che il PDF esca dallo studio.**

In pagina 5 nessun dato è inventato: sono osservazioni dall'esterno, dichiarate come tali,
e nessuna promessa di risultato.

## Stagionalità

Campomaggio è Toscana: chiude a novembre, una stagione sola. L'Alto Adige ne lavora **due**,
inverno ed estate (decisione del 10/11). Qui alta stagione sono 8 mesi, dicembre-marzo e
giugno-settembre, e bassa sono i 4 di mezzo. È anche un argomento di vendita: i mesi di
bassa sono quelli in cui si prenota.

## Font, logo e brand

Lo script usa il kit del brand se lo trova
(`~/Desktop/Y/BRAND YDG STUDIO/Preventivo (mockup)/_sorgente/`) e in quel caso compone in
**Overused Grotesk**, il font del sito. Se il kit non c'è — per esempio in una sessione
cloud — ripiega su **Inter** e lo dichiara a schermo: serve per vedere l'impaginazione,
non per mandare il PDF al cliente. **Il PDF definitivo si genera dove c'è il kit.**

⚠️ **Il marchio in testata è un segnaposto**: "YDG ◂ STUDIO" composto a testo, con il segno
disegnato in CSS. Quello vero è vettoriale e sta nel kit. Va sostituito quando si genera
sul Mac, altrimenti il documento esce con un logo che somiglia ma non è il nostro.

Colori dal Codice del brand v1.0: arancio `#FF7900`, fondo `#1A1A1A`, fondo profondo
`#111111`, card `#1E1E1E`, grigio dei testi `#a9a9a6`. Elementi ricorrenti presi dal
documento standard: occhiello con quadratino arancio, card scure con barra arancio in
cima, una card arancio per contrasto, tabella economica con la fascia evidenziata, pagina
finale arancio piena.

## Controllo degli sforamenti

`rendi.mjs` misura l'altezza reale del contenuto di ogni pagina nel browser e segnala
quelle che superano i 720px. Esclude gli elementi `position:absolute` (l'alone arancio
della copertina, che esce apposta dal riquadro) e quelli inline, che riportano la scatola
del font invece della riga: senza quei due filtri segnalava sforamenti che non esistono.
