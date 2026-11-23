# Proposta di acquisizione · verticale ospitalità

**Cos'è.** La proposta che portiamo a una struttura che non ci conosce. Tre servizi in un
documento solo — social organico, advertising, sito e portali — ognuno con la sua pagina
e il suo prezzo, più il quadro economico complessivo.

Compilata su **Hotel Heubad** (Fiè allo Sciliar), presa dalla lista dell'hub, per vederla
piena. Per un'altra struttura si cambiano `STRUTTURA` e `FOTOGRAFIA` in testa allo script.

- `Proposta ospitalita - Hotel Heubad.pdf` · 15 pagine, 16:9
- `_anteprime_acquisizione/` · una PNG per pagina
- `build_proposta_acquisizione.py` + `rendi.mjs` · rigenerano tutto

## Perché non è la proposta di Campomaggio

Quella è un **rinnovo**: parla a chi ci conosce da due stagioni, quindi si apre con
«cosa abbiamo fatto insieme». Questa è un'**acquisizione**: chi la legge non ci ha mai
visti. Quindi l'impianto si ribalta.

| | Rinnovo (Campomaggio) | Acquisizione (questa) |
|---|---|---|
| Apertura | i nostri risultati con loro | la fotografia della **loro** struttura |
| I numeri di Campomaggio | consuntivo | **prova** che il metodo funziona |
| Servizi | gestione social, sito «su richiesta» | tre servizi pari grado, una pagina ciascuno |
| Economia | un totale | setup, ricorrente e canoni separati, poi il totale |

## Le 15 pagine

1. Copertina · 2-3 Da dove partite (fotografia e nodo) · 4-5 Che cosa sappiamo fare
(organico e advertising) · 6 I tre servizi · 7 Social organico · 8 Advertising ·
9 Sito, portali, dati · 10 Come lavoriamo · 11 Il calendario · 12 Avvio ·
13 Ricorrente · 14 Il totale · 15 Contatti

## Da dove vengono i numeri

| Dove | Fonte |
|---|---|
| P2 fotografia della struttura | scheda dell'hub, Google Places del 16/10/2026 |
| P4-P5 risultati | Proposta di rinnovo 2027 Campomaggio, consuntivo stagione 2026 |
| P12 sito, portali, tracciamento | listino Nadir, caso B (sito da rifare) |
| P8 budget pubblicitario | DOCUMENTO UNICO, 400-600 €/mese |
| P13 ADV | DOCUMENTO UNICO, minimo 500 €/mese se presa da sola |

**L'unica cosa non ancora approvata: le due cifre del social organico** (1.400 €/mese in
alta, 900 € in bassa) e lo shooting di avvio a 3.500 €. Nel DOCUMENTO UNICO le cifre di
gestione sono 1.200/2.000, ma sono quelle di Campomaggio **per due brand** — e il
documento stesso dice che per una struttura sola vanno riviste. Qui sono scalate su un
brand solo, non dimezzate: i costi fissi non si dimezzano. **Vanno confermate da Alex,
Riccardo e Alessandro prima che il PDF esca dallo studio.**

Niente è inventato sulla struttura: in pagina 2 ci sono solo dati pubblici misurati, con
la data del rilevamento in alto a destra. Nessuna promessa di risultato.

## Stagionalità

Campomaggio è Toscana: chiude a novembre, alta stagione aprile-ottobre. L'Alto Adige
lavora **due** stagioni, inverno ed estate (decisione del 10/11). Quindi qui alta stagione
sono 8 mesi, dicembre-marzo e giugno-settembre, e bassa sono i 4 di mezzo. È anche un
argomento di vendita: i mesi di bassa sono quelli in cui si prenota.

## Font e brand

Lo script usa il kit del brand se lo trova
(`~/Desktop/Y/BRAND YDG STUDIO/Preventivo (mockup)/_sorgente/`) e in quel caso compone in
**Overused Grotesk**, il font del sito. Se il kit non c'è — per esempio in una sessione
cloud — ripiega su **Inter** e lo dichiara a schermo: serve per vedere l'impaginazione,
non per mandare il PDF al cliente. **Il PDF definitivo si genera dove c'è il kit.**

Colori dal Codice del brand v1.0, gli stessi letti dal CSS del sito: arancio `#FF7900`,
fondo `#1A1A1A`, fondo profondo `#111111`, grigio dei testi `#a9a9a6`, raggi 24px,
titoli a interlinea 1.03 e spaziatura -.04em, etichette a .075em. Firma dei titoli come
sul sito: prima parte scura, coda arancio, punto finale.

Il logo in copertina è composto a testo. Quello vettoriale sta nel kit: quando si genera
sul Mac va sostituito.

## Controllo degli sforamenti

`rendi.mjs` misura l'altezza reale di ogni pagina nel browser e segnala quelle che
superano i 720px. Una pagina che straborda si vede solo stampata, e a quel punto è tardi.
