# Strumenti · come si rifà la lista

Tre passi, in quest'ordine. Il primo costa (Places), gli altri due sono gratis
e si possono rilanciare quante volte si vuole.

```bash
node benchmark/strumenti/lista-strutture.mjs      # 1. Places → strutture-grezze.json  (~77 chiamate)
node benchmark/strumenti/arricchisci-social.mjs   # 2. legge le homepage → social-homepage.json
node benchmark/strumenti/scegli-50.mjs            # 3. sceglie → strutture-50.json + .md + escluse
```

Per cambiare la rosa non serve rifare il passo 1: tocca i criteri in testa a
`scegli-50.mjs` (`MAXKM`, `MINRAT`, `MINREC`, i pesi) e rilancia il passo 3.

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
