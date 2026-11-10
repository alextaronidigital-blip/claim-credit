# Proposta di collaborazione · verticale ospitalità

**Cos'è.** Il template della proposta che portiamo agli albergatori, nel brand YDG Studio.
Compilato su **Hotel Villa Campomaggio** per vederlo pieno: per un'altra struttura si
cambiano due dizionari e il resto resta.

- `Proposta ospitalita - Hotel Villa Campomaggio.pdf` · 14 pagine, 16:9
- `_anteprime/` · una PNG per pagina
- `build_proposta_ospitalita.py` · rigenera tutto in pochi secondi

## Come si adatta a un'altra struttura

In testa allo script ci sono due blocchi:

- `CLIENTE`: nome, le due righe di copertina, la data, la frase sulla stagione.
- `ECONOMIA` + `TOTALE_ANNO`: le righe del riepilogo economico.

Cambiati quelli, `python3 build_proposta_ospitalita.py` rifà PDF e anteprime. Le pagine
che parlano del metodo, dei servizi, del team e delle condizioni valgono per tutti.
Le pagine 7 (casi studio) e 8 (da dove partiamo) vanno riviste caso per caso: la 8 è la
fotografia di quella struttura.

## Da dove vengono i contenuti

| Pagina | Fonte |
|---|---|
| 2 problemi, 4 servizi, 5 metodo, 12 voci opzionali | `materiali/YDG - Ospitalita - DOCUMENTO UNICO 10-11.docx` |
| 6 stagione, 9 cosa ricevete, 10 investimento, 11 condizioni | Proposta di rinnovo 2027 Villa Campomaggio e La Gabbia (Riccardo, 10/11) |
| 7 casi studio | numeri della stessa proposta di rinnovo e della proposta Collinelli |
| 13 team | composizione decisa il 28/09, confermata il 10/11 |

Nessun numero è inventato: quello che non risulta da queste fonti non è in pagina.

## Brand

Font, loghi, icone e alone arancio arrivano dal kit del mockup
(`~/Desktop/Y/BRAND YDG STUDIO/Preventivo (mockup)/_sorgente/`), che a sua volta li
prende dal `.ai`. Lo script non duplica nulla: se quella cartella non c'è, si ferma.
Valori solo dal Codice del brand v1.0 (pilastro `brand-solo-dal-codice`).

## Cosa manca ancora

I prezzi di social e ADV nel DOCUMENTO UNICO restano da decidere: qui le cifre di
gestione sono quelle reali di Campomaggio, quindi il PDF è completo come esempio ma non
è ancora un listino. Quando i pacchetti saranno fissati, la pagina 10 diventa il listino.
