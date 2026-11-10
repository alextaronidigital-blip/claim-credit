# Strumenti · come si rifà la lista

Tre passi, in quest'ordine. Il primo costa (Places), gli altri due sono gratis
e si possono rilanciare quante volte si vuole.

```bash
node benchmark/strumenti/lista-strutture.mjs --prova   # 2 zone per area: verifica che la chiave risponda
node benchmark/strumenti/lista-strutture.mjs           # 1. Places → strutture-grezze.json (~270-500 chiamate)
node benchmark/strumenti/arricchisci-social.mjs        # 2. legge le homepage → social-homepage.json
node benchmark/strumenti/scegli-50.mjs                 # 3. sceglie → strutture-50.json + .md + escluse
```

Una sola area per volta: `node benchmark/strumenti/lista-strutture.mjs --area cortina`
(gli id sono `siusi`, `campiglio`, `cortina`, `tarvisio`).

Per cambiare la rosa non serve rifare il passo 1: tocca `raggioSceltaKm` in
`comuni.json`, i criteri in testa a `scegli-50.mjs` (`MINRAT`, `MINREC`, i pesi)
o il censimento in `stelle.json`, e rilancia il passo 3.

## Il perimetro
`comuni.json` tiene **quattro aree**, ognuna col suo centro (decisione del 10/11,
vedi `materiali/AGGIORNAMENTO-10-11.md`): Alpe di Siusi, Madonna di Campiglio e le
valli del Trentino, Cortina e il bellunese, Tarvisio e la montagna friulana.
La distanza di ogni struttura si misura **dal centro dell'area più vicina**, non da
un punto solo. 167 zone in tutto: il passo 1 costa, orientativamente 10-20 $ del
credito Google, quindi va sparato sul perimetro giusto, non due volte.

## La fascia
Google **non espone le stelle**. Il censimento di quelle che sappiamo sta in
`stelle.json`, compilato a mano sui nomi esatti con cui Google le scrive, col comune
a sciogliere gli omonimi. Le 5 stelle non entrano in rosa ma non si buttano: restano
in coda con stato `Non in target` e il motivo scritto, così in hub si vedono barrate.
Chi non è censito resta in gioco: una stella non si inventa.

## Cosa sappiamo e cosa no
| Dato | Da dove | Affidabilità |
|---|---|---|
| Nome, comune, indirizzo, telefono | Google Places | alta |
| Rating e numero recensioni | Google Places | alta |
| Sito web | Google Places | alta |
| Social presenti | link nella homepage | **presenza sì, assenza no** |
| Stelle (4★, 4★ Sup) | — | Google non le espone: a mano |
| Stagionalità | — | a mano |
| Follower | — | a mano |
| Fascia di prezzo | — | Google la dà vuota su tutti gli hotel |

«Nessun social» significa *nessun link trovato nella homepage*: il profilo può
esistere lo stesso. Si guarda prima di dirlo al titolare.

La distanza è **in linea d'aria**: 30 km di Dolomiti sono spesso un'ora di guida.
