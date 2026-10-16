# Chiave Google Places — come si fa (10 minuti)

Serve per schedare le 50 strutture senza copiarle a mano da Maps: nome, comune,
distanza da Siusi, rating, numero di recensioni, sito web. La chiave è tua, resta
sul tuo Mac, non entra in git.

## 1. Progetto Google Cloud
1. Vai su https://console.cloud.google.com/ con l'account Google dell'agenzia.
2. In alto, selettore dei progetti → **Nuovo progetto** → nome `YDG Ospitalita` → **Crea**.
3. Assicurati che in alto sia selezionato quel progetto.

## 2. Fatturazione
Places non risponde senza un account di fatturazione, anche se poi non paghi.
1. Menu ☰ → **Fatturazione** → **Collega un account di fatturazione** (o creane uno con la carta).
2. Google dà **200 $/mese di credito gratuito** su Maps/Places: la nostra raccolta
   costa circa **5-8 $**, quindi non arriva all'addebito. Ma la carta la chiede.

## 3. Attiva l'API giusta
1. Menu ☰ → **API e servizi** → **Libreria**.
2. Cerca **Places API (New)** → **Abilita**.
   ⚠️ Non "Places API" vecchia: lo script usa la New (`places:searchText`).

## 4. Crea la chiave
1. **API e servizi** → **Credenziali** → **+ Crea credenziali** → **Chiave API**.
2. Copia la chiave (`AIza...`) e tienila da parte un minuto.
3. **Modifica chiave** → in *Restrizioni API* scegli **Limita chiave** → spunta solo
   **Places API (New)** → **Salva**.
   Le restrizioni per IP/referrer lasciale **nessuna**: lo script gira dal tuo Mac.

## 5. Mettila dove lo script la trova
Nella radice del repo (`~/YDG-Ospitalita` o la cartella del progetto), crea il file
`.env.local` con una riga:

```
GOOGLE_PLACES_KEY=AIza...la-tua-chiave...
```

`.env.local` è già in `.gitignore`: non finisce su GitHub.

## 6. Prova e poi raccogli
```bash
node benchmark/strumenti/lista-strutture.mjs --prova   # 3 zone, verifica che la chiave risponda
node benchmark/strumenti/lista-strutture.mjs           # tutte le zone, scrive i due JSON
```

Escono:
- `benchmark/dati/strutture-grezze.json` — tutto il raccolto, più le scartate **col motivo**
- `benchmark/dati/strutture-50.json` — le 50 migliori nello schema dell'hub

## Cosa Google NON sa
Le **stelle** (4★, 4★ Sup), la **stagionalità** vera e i **social**. Quei campi escono
`Non classificato` / `Da verificare` e si compilano nell'hub: meglio un buco dichiarato
che un numero inventato.
