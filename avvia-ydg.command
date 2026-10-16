#!/bin/bash
# ---------------------------------------------------------------
#  YDG · Verticale ospitalità
#  Apre una sessione di Claude che gira SUL TUO MAC, quindi con
#  accesso ai tuoi file e al tuo browser.
#  Si lancia con un doppio clic, oppure da Terminale:
#      bash ~/Downloads/avvia-ydg.command
# ---------------------------------------------------------------

CARTELLA="$HOME/YDG-Ospitalita"
REPO="https://github.com/alextaronidigital-blip/claim-credit.git"

ok()   { printf "\033[32m✓\033[0m %s\n" "$1"; }
no()   { printf "\033[31m✗\033[0m %s\n" "$1"; }
info() { printf "\033[33m→\033[0m %s\n" "$1"; }
titolo(){ printf "\n\033[1m%s\033[0m\n" "$1"; }

titolo "YDG · avvio sessione locale"

# --- 1. Node -----------------------------------------------------
titolo "1. Controllo Node"
if command -v node >/dev/null 2>&1; then
  ok "Node $(node -v) presente"
else
  no "Node non è installato."
  info "Scaricalo da https://nodejs.org (versione LTS), installalo, poi rilancia questo script."
  echo; read -n 1 -s -r -p "Premi un tasto per chiudere."; exit 1
fi

# --- 2. Claude Code ----------------------------------------------
titolo "2. Controllo Claude Code"
if command -v claude >/dev/null 2>&1; then
  ok "Claude Code presente"
else
  no "Claude Code non è installato."
  read -r -p "Lo installo adesso con npm? [s/n] " risposta
  case "$risposta" in
    s|S|y|Y)
      info "Installo… (può metterci un minuto)"
      if npm install -g @anthropic-ai/claude-code; then
        ok "Installato"
      else
        no "Installazione fallita. Prova a mano:  npm install -g @anthropic-ai/claude-code"
        echo; read -n 1 -s -r -p "Premi un tasto per chiudere."; exit 1
      fi
      ;;
    *) info "Ok, non installo niente. Senza Claude Code lo script non può proseguire."
       echo; read -n 1 -s -r -p "Premi un tasto per chiudere."; exit 1 ;;
  esac
fi

# --- 3. Cartella di lavoro ---------------------------------------
titolo "3. Cartella di lavoro"
if [ -d "$CARTELLA/.git" ]; then
  ok "Cartella già presente: $CARTELLA"
  info "Scarico gli ultimi aggiornamenti…"
  git -C "$CARTELLA" pull --ff-only 2>/dev/null && ok "Aggiornata" || info "Niente da aggiornare (o serve il login a GitHub)"
elif command -v git >/dev/null 2>&1; then
  info "Scarico il progetto in $CARTELLA …"
  if git clone "$REPO" "$CARTELLA" 2>/dev/null; then
    ok "Progetto scaricato"
  else
    info "Clone non riuscito (probabilmente serve il login a GitHub). Creo una cartella vuota."
    mkdir -p "$CARTELLA"
  fi
else
  mkdir -p "$CARTELLA"
  ok "Cartella creata: $CARTELLA"
fi

cd "$CARTELLA" || exit 1

# --- 4. Avvio ----------------------------------------------------
titolo "4. Avvio della sessione"
echo
echo "   Sto per aprire Claude DENTRO questa cartella, sul tuo Mac."
echo "   Da lì potrà leggere e scrivere i tuoi file locali."
echo
echo "   Prima cosa da scrivergli, copia e incolla:"
echo
printf "\033[33m   Riprendiamo il verticale ospitalità YDG. Leggi il repo in questa\n"
printf "   cartella. Devo creare la chiave Google Places e poi fare la lista\n"
printf "   delle 50 strutture. Guidami tu.\033[0m\n"
echo
read -n 1 -s -r -p "   Premi un tasto per partire…"
echo; echo

if claude remote-control --help >/dev/null 2>&1; then
  exec claude remote-control
else
  exec claude
fi
