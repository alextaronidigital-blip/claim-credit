"""Proposta di collaborazione · verticale OSPITALITÀ, col brand YDG Studio.

Motore e ingredienti presi dal mockup del preventivo (HTML → Chrome headless → PDF):
`~/Desktop/Y/BRAND YDG STUDIO/Preventivo (mockup)/_sorgente/`. Da lì arrivano font,
asset vettoriali e pattern, così il brand resta uno solo (Codice v1.0, pilastro
`brand-solo-dal-codice`): qui non si inventa nessun valore.

Contenuti: il DOCUMENTO UNICO del verticale (servizi, metodo, prezzi di Nadir) e le due
proposte reali di Hotel Villa Campomaggio che ha girato Riccardo. Campomaggio è l'esempio
compilato: per un'altra struttura si cambiano i dizionari CLIENTE ed ECONOMIA qui sotto,
il resto del documento resta uguale.

Uso:  python3 build_proposta_ospitalita.py
"""
import os, sys, html, subprocess, tempfile, shutil
import fitz

HERE = os.path.dirname(os.path.abspath(__file__))
BRAND = os.path.expanduser("~/Desktop/Y/BRAND YDG STUDIO/Preventivo (mockup)/_sorgente")
ASSET, FONT = os.path.join(BRAND, "asset"), os.path.join(BRAND, "font")
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
OUT = os.path.join(HERE, "Proposta ospitalita - Hotel Villa Campomaggio.pdf")
for p in (BRAND, ASSET, FONT, CHROME):
    if not os.path.exists(p):
        sys.exit(f"manca {p}: il kit del brand deve stare dov'è, non si duplica")

E = html.escape
ORANGE, BLACK, CHARCOAL, SILVER, OFFW = "#FF7900", "#1A1A1A", "#4D4D4D", "#CCCCCC", "#F2F2F2"

# ─────────────────────────────────────────────────────────── il cliente, da cambiare
CLIENTE = {
    "nome": "Hotel Villa Campomaggio",
    "riga1": "Struttura ricettiva e ristorante nel Chianti, 23 camere e suite",
    "riga2": "Riempire la stagione partendo da chi prenota in inverno.",
    "data": "Novembre 2026",
    "stagione_chiusa": "L'hotel chiude a novembre. Le prenotazioni dell'estate no.",
}
TOT = 14
META = f"Proposta di collaborazione · {CLIENTE['nome']}"
WEB = "ydgstudio.com · @ydg_agency"

# ─────────────────────────────────────────────────────────── numeri, tutti verificati
# Gestione: dalla proposta di rinnovo 2027 (Riccardo, 10/11). Voci tecniche: Nadir v6.
ECONOMIA = [
    ("Gestione bassa stagione", "Presidio dell'hotel, campagne prenotazioni, contenuti per le campagne",
     "Dic · Mar, 4 mesi", "1.200 €/mese"),
    ("Gestione alta stagione", "Social completo, 12 contenuti al mese, 2 video, stories e community",
     "Apr · Nov, 8 mesi", "2.000 €/mese"),
    ("Produzione", "4 shooting foto e video nell'anno, modelli inclusi",
     "Nell'anno", "6.200 € una tantum"),
]
TOTALE_ANNO = "27.000 €"
OPZIONALI = [
    ("Sito con prenotazione diretta", "Sito o restyling, pagine, versione mobile, motore di prenotazione collegato",
     "da 1.900 a 2.800 € una tantum", "500 €/anno di manutenzione"),
    ("Booking e Airbnb", "Schede, tariffe e disponibilità, collegamento del channel manager",
     "900 € di avvio", "da 500 a 800 €/anno secondo le camere"),
    ("Tracciamento", "GA4, Tag Manager, Pixel di Meta, conteggio richieste e prenotazioni",
     "500 € una tantum", "incluso nel sito dalla proposta media in su"),
    ("CRM ed email", "Archivio contatti e comunicazioni agli ospiti passati",
     "nessun costo di avvio", "su richiesta"),
]

def svg(name, cls="", style=""):
    s = open(os.path.join(ASSET, name + ".svg"), encoding="utf-8").read()
    return s.replace("<svg ", f'<svg class="{cls}" style="{style}" ', 1)

def _mix(t):
    a, b = (26, 26, 26), (255, 121, 0)
    return "#%02X%02X%02X" % tuple(round(a[k] + (b[k]-a[k])*t) for k in range(3))

def glow(cx, cy, rx, ry, gamma=1.4):
    stops = ", ".join(f"{_mix(max(0.0, 1-d)**gamma)} {d*100:.0f}%" for d in [k/12 for k in range(13)])
    return f"background:{BLACK} radial-gradient(ellipse {rx*100:.0f}% {ry*100:.0f}% at {cx*100:.0f}% {cy*100:.0f}%, {stops});"

CSS = f"""
@font-face{{font-family:"Overused Grotesk";src:url("font/OverusedGrotesk-SemiBold.ttf");font-weight:600}}
@font-face{{font-family:"Overused Grotesk";src:url("font/OverusedGrotesk-Book.ttf");font-weight:400}}
:root{{--o:{ORANGE};--k:{BLACK};--c:{CHARCOAL};--s:{SILVER};--w:{OFFW}}}
@page{{size:1920px 1080px;margin:0}}
html,body{{margin:0;padding:0}}
body{{font-family:"Overused Grotesk",Inter,Arial,sans-serif;font-weight:400;-webkit-print-color-adjust:exact;print-color-adjust:exact}}
.slide{{width:1920px;height:1080px;position:relative;overflow:hidden;break-after:page;box-sizing:border-box}}
.dark{{background:var(--k);color:var(--w)}} .light{{background:var(--w);color:var(--k)}} .orange{{background:var(--o);color:var(--k)}}
.hdr{{position:absolute;top:58px;left:120px;right:120px;display:flex;justify-content:space-between;align-items:center;z-index:2}}
.hdr svg{{height:32px;width:auto;display:block}}
.dark .hdr svg{{color:var(--w)}} .light .hdr svg,.orange .hdr svg{{color:var(--k)}}
.meta,.ftr{{font-size:20px}}
.dark .meta,.dark .ftr{{color:var(--s)}} .light .meta,.light .ftr{{color:var(--c)}} .orange .meta,.orange .ftr{{color:var(--k)}}
.ftr{{position:absolute;bottom:54px;left:120px;right:120px;display:flex;justify-content:space-between;z-index:2}}
.ftr b{{font-weight:600}}
.box{{position:absolute;top:178px;left:120px;right:120px;bottom:130px;z-index:2}}
.eye{{font-weight:600;font-size:25px;letter-spacing:.14em;text-transform:uppercase;display:flex;align-items:center;gap:14px}}
.dark .eye{{color:var(--o)}} .light .eye,.orange .eye{{color:var(--k)}}
.light .eye::before{{content:"";width:14px;height:14px;background:var(--o);display:block}}
h1{{font-weight:600;font-size:50px;line-height:1.12;margin:16px 0 0;letter-spacing:-.005em}}
.lead{{font-size:28px;line-height:1.42;margin:20px 0 0;max-width:1300px}}
.dark .lead{{color:var(--s)}} .light .lead{{color:var(--c)}}
.big{{font-weight:600;font-size:130px;line-height:1.0;letter-spacing:-.02em}}
.o{{color:var(--o)}}
.note{{font-size:20px;line-height:1.4}}
.dark .note{{color:var(--s)}} .light .note{{color:var(--c)}}
ul.l{{list-style:none;margin:0;padding:0}}
ul.l li{{font-size:28px;line-height:1.38;padding:0 0 18px 34px;position:relative}}
ul.l li::before{{content:"";position:absolute;left:0;top:15px;width:12px;height:12px;border-radius:50%;background:var(--o)}}
.tight li{{padding-bottom:9px !important;font-size:25px}}
.orange ul.l li::before,.card.or ul.l li::before{{background:var(--k)}}
.card{{border-radius:18px;padding:40px 44px;box-sizing:border-box}}
.card.k{{background:var(--k);color:var(--w)}} .card.c{{background:var(--c);color:var(--w)}} .card.or{{background:var(--o);color:var(--k)}}
.card h3{{font-weight:600;font-size:28px;margin:0 0 22px}}
.k .sub,.c .sub{{color:var(--s)}}
.sub{{font-size:20px;line-height:1.35}}
.grid{{display:grid;gap:32px}}
.num{{font-weight:600;font-size:96px;line-height:.9;color:var(--o);letter-spacing:-.02em}}
.tag{{display:inline-block;font-weight:600;font-size:20px;letter-spacing:.12em;text-transform:uppercase;padding:9px 18px;border-radius:999px}}
.kpi{{font-weight:600;font-size:50px;line-height:1;color:var(--o)}}
"""

def page(theme, body, n=None, bg="", extra="", meta=META):
    num = f"<b>{n:02d}</b> / {TOT:02d}" if n else ""
    return (f'<section class="slide {theme}" style="{bg}">{extra}'
            f'<div class="hdr">{svg("logo-germoglio-centro")}<div class="meta">{E(meta)}</div></div>'
            f'<div class="box">{body}</div>'
            f'<div class="ftr"><span>{num}</span><span>{E(WEB)}</span></div></section>')

def ul(xs, cls="l"):
    return f'<ul class="{cls}">' + "".join(f"<li>{E(x)}</li>" for x in xs) + "</ul>"

# ── 01 copertina
def p01():
    body = (f'<div style="position:absolute;top:150px;left:0;right:0">'
            f'<div class="eye">Proposta di collaborazione</div>'
            f'<div class="big" style="margin-top:34px">Facciamo crescere<br><span class="o">{E(CLIENTE["nome"])}</span></div>'
            f'<div class="lead" style="margin-top:40px;color:var(--s)">{E(CLIENTE["riga1"])}<br>{E(CLIENTE["riga2"])}</div></div>')
    return page("dark", body, 1, glow(0.88, 1.12, 0.62, 1.05, 1.45), meta=f"{CLIENTE['data']} · {CLIENTE['nome']}")

# ── 02 il problema dell'albergatore
def p02():
    pb = [("Le commissioni", "Ogni prenotazione che passa dai portali lascia una percentuale per strada. Il sito che prende la prenotazione diretta sposta una parte di quel giro in casa: stesso ospite, stessa notte, senza commissione."),
          ("La voce che manca", "Chi vi trova su Google o sui portali va a cercarvi su Instagram. Se trova foto vecchie e nessuna risposta, sceglie la struttura accanto che gliela dà."),
          ("Il lavoro a mano", "Tariffe e disponibilità aggiornate a mano su più canali: prima o poi si vende due volte la stessa camera, o si resta con la camera vuota a prezzo pieno.")]
    cards = "".join(f'<div class="card k" style="min-height:430px"><div class="num">{i+1:02d}</div>'
                    f'<h3 style="margin-top:26px">{E(t)}</h3><div style="font-size:25px;line-height:1.42;color:var(--s)">{E(d)}</div></div>'
                    for i, (t, d) in enumerate(pb))
    body = (f'<div class="eye">Il punto di partenza</div><h1>Tre cose che costano, ogni stagione</h1>'
            f'<p class="lead">Non parliamo di «essere sui social». Parliamo di dove una struttura perde ospiti e margine.</p>'
            f'<div class="grid" style="grid-template-columns:repeat(3,1fr);gap:32px;margin-top:40px">{cards}</div>')
    return page("light", body, 2)

# ── 03 chi siamo
def p03():
    servizi = [("social", "Social"), ("siti-web", "Siti web"), ("foto", "Foto"), ("video", "Video"),
               ("adv", "Adv"), ("grafica", "Grafica")]
    tiles = "".join(f'<div style="display:flex;align-items:center;gap:22px">'
                    f'{svg("icona-cerchio-" + k, style="width:72px;height:72px;flex:none;color:" + ORANGE)}'
                    f'<span style="font-size:28px;font-weight:600;white-space:nowrap">{v}</span></div>' for k, v in servizi)
    forza = ["Tutto in-house, un'unica regia per ogni contenuto",
             "Veniamo in struttura: gli shooting li facciamo noi, non li appaltiamo",
             "Gestione manuale e strategica, mai automatismi",
             "La stessa squadra dall'inizio alla fine, risposte dirette alla direzione",
             "Report trasparenti: si vede cosa portiamo"]
    body = (f'<div class="eye">Chi siamo</div><h1>Uno studio di comunicazione digitale,<br>con un verticale sull\'ospitalità.</h1>'
            f'<p class="lead">YDG Studio lavora con PMI e attività locali dal 2022. Sull\'ospitalità abbiamo costruito da zero i profili di un hotel e del suo ristorante, e li seguiamo da due stagioni.</p>'
            f'<div class="grid" style="grid-template-columns:1fr 1fr;margin-top:50px;gap:40px">'
            f'<div><div class="sub" style="font-weight:600;letter-spacing:.12em;text-transform:uppercase;margin-bottom:26px;color:var(--c)">Cosa fa lo studio</div>'
            f'<div class="grid" style="grid-template-columns:1fr 1fr;gap:34px 14px">{tiles}</div></div>'
            f'<div class="card k" style="height:100%"><h3>Come lavoriamo</h3>{ul(forza)}</div></div>')
    return page("light", body, 3)

# ── 04 i cinque servizi
def p04():
    s = [("Gestione social", "Piano editoriale, contenuti, pubblicazione, community sui profili della struttura e del ristorante."),
         ("Sito con prenotazione", "Sito o restyling con motore di prenotazione diretta collegato, pagine per le offerte."),
         ("Booking e Airbnb", "Schede curate, tariffe e disponibilità allineate, channel manager collegato e monitorato."),
         ("CRM ed email", "Archivio contatti e comunicazioni agli ospiti già passati. Opzionale, su richiesta."),
         ("Advertising", "Campagne Meta e Google sui mercati che prenotano, con il budget che decidete voi.")]
    cards = "".join(f'<div class="card c" style="border-top:8px solid {ORANGE};border-radius:6px 6px 18px 18px;min-height:360px">'
                    f'<h3>{E(t)}</h3><div style="font-size:25px;line-height:1.4">{E(d)}</div></div>' for t, d in s)
    body = (f'<div class="eye">I servizi</div><h1>Cinque leve, una sola regia</h1>'
            f'<p class="lead">Si attivano insieme o una alla volta. Quello che non serve oggi resta fuori dal preventivo.</p>'
            f'<div class="grid" style="grid-template-columns:repeat(5,1fr);gap:24px;margin-top:50px">{cards}</div>')
    return page("dark", body, 4)

# ── 05 il metodo, i sette passi
def p05():
    steps = [("Chiamata di scoperta", "Come lavorate, dove perdete ospiti, cosa avete già provato."),
             ("Proposta", "Servizi, tempi e prezzi tagliati sulla struttura."),
             ("Accessi e intake", "Le domande a voi e ai vostri ospiti, gli accessi, la Bibbia della struttura."),
             ("Shooting", "Foto e video in struttura: senza materiale non parte niente."),
             ("Strategia e piano", "Dati, piano editoriale e piano campagne, presentati e approvati."),
             ("Si parte", "Pubblicazioni, campagne, sito online."),
             ("Il ritmo", "Ottimizzazione continua e report.")]
    cols = "".join(f'<div style="border-top:2px solid {CHARCOAL};padding-top:26px;position:relative">'
                   f'<div style="position:absolute;top:-2px;left:0;width:{(i+1)*14}%;height:2px;background:{ORANGE}"></div>'
                   f'<div class="num" style="font-size:72px">{i+1:02d}</div>'
                   f'<div style="font-weight:600;font-size:25px;margin:22px 0 10px">{E(t)}</div>'
                   f'<div style="font-size:20px;line-height:1.4;color:var(--s)">{E(d)}</div></div>' for i, (t, d) in enumerate(steps))
    body = (f'<div class="eye">Il metodo</div><h1>Dal primo contatto alla stagione piena</h1>'
            f'<p class="lead">Il primo mese è di fondamenta e non si pubblica: strategia, intake, shooting. La pubblicazione parte dal secondo.</p>'
            f'<div class="grid" style="grid-template-columns:repeat(7,1fr);gap:22px;margin-top:90px">{cols}</div>')
    return page("dark", body, 5)

# ── 06 la stagione
def p06():
    mesi = ["Dic","Gen","Feb","Mar","Apr","Mag","Giu","Lug","Ago","Set","Ott","Nov"]
    barre = "".join(f'<div style="text-align:center"><div style="height:16px;border-radius:999px;background:{ORANGE if i < 4 else CHARCOAL}"></div>'
                    f'<div class="sub" style="margin-top:12px;color:var(--c)">{m}</div></div>' for i, m in enumerate(mesi))
    bassa = ["Presidio dei profili, 2 post al mese", "Campagne per le prenotazioni sui mercati esteri",
             "6 video dedicati alle campagne", "Recensioni e community", "Nessuno shooting: si lavora sull'archivio"]
    alta = ["Gestione completa: Instagram, Facebook, TikTok, Google Business", "12 contenuti al mese",
            "2 video al mese, stories, commenti e messaggi", "Campagne Meta, ottimizzazione e report",
            "4 shooting distribuiti nella stagione"]
    body = (f'<div class="eye">La stagione</div><h1>{E(CLIENTE["stagione_chiusa"])}</h1>'
            f'<p class="lead">Chi sceglie la vostra zona per l\'estate decide tra dicembre e marzo, soprattutto dall\'estero. '
            f'Spegnere la comunicazione in quei mesi significa essere assenti quando la domanda si forma.</p>'
            f'<div class="grid" style="grid-template-columns:repeat(12,1fr);gap:10px;margin-top:40px">{barre}</div>'
            f'<div class="grid" style="grid-template-columns:1fr 1.25fr;gap:32px;margin-top:40px">'
            f'<div class="card or"><h3>Bassa stagione · 4 mesi</h3>{ul(bassa, "l tight")}</div>'
            f'<div class="card k"><h3>Alta stagione · 8 mesi</h3>{ul(alta, "l tight")}</div></div>')
    return page("light", body, 6)

# ── 07 casi studio (numeri reali)
def p07():
    casi = [("La Gabbia Tuscany Lounge", "Ristorante dell'hotel · da zero, stagione 2025",
             [("3.030", "Follower Instagram costruiti partendo da zero"), ("1.200.000", "Impression in una stagione"),
              ("285.000+", "Persone raggiunte"), ("+30", "Recensioni positive in più")]),
            ("Hotel Villa Campomaggio", "Struttura ricettiva · due stagioni",
             [("80", "Contenuti professionali pubblicati"), ("16", "Video verticali"),
              ("3", "Shooting stagionali"), ("2", "Brand seguiti con un'unica regia")]),
            ("Romagna Free", "Forno e pasticceria senza glutine",
             [("+893.000", "Impression su IG e FB in 4 mesi"), ("+128.000", "Account raggiunti"),
              ("+2.300", "Nuovi follower"), ("0,06 €", "Costo per click delle campagne")])]
    cards = ""
    for nome, sett, ms in casi:
        rows = "".join(f'<div style="padding:14px 0;border-top:1px solid {CHARCOAL}"><div class="kpi">{E(v)}</div>'
                       f'<div class="sub" style="margin-top:8px">{E(l)}</div></div>' for v, l in ms)
        cards += (f'<div class="card k"><div style="font-weight:600;font-size:28px">{E(nome)}</div>'
                  f'<div class="sub" style="margin:6px 0 20px">{E(sett)}</div>{rows}</div>')
    body = (f'<div class="eye">Casi studio</div><h1>Numeri veri, non promesse</h1>'
            f'<div class="grid" style="grid-template-columns:repeat(3,1fr);gap:32px;margin-top:44px">{cards}</div>')
    return page("light", body, 7)

# ── 08 da dove partiamo
def p08():
    ok = ["Due stagioni di contenuti già in archivio", "Coerenza fra i due brand, distinti ma della stessa mano",
          "Sala quasi sempre piena e nuovi clienti al ristorante", "Rapporto diretto con la direzione"]
    gr = ["Un'unica regia per hotel e ristorante, camere e suite comprese",
          "Quattro shooting all'anno invece di tre, uno dedicato alle camere",
          "Presenza nella finestra di prenotazione, da dicembre a marzo",
          "TikTok con una linea editoriale dedicata per ciascun brand",
          "Advertising sui mercati esteri che prenotano con anticipo"]
    body = (f'<div class="eye">Da dove partiamo</div><h1>Cosa funziona, e dove si cresce</h1>'
            f'<p class="lead">Una fotografia onesta. La strategia di dettaglio nasce dai dati, nelle prime settimane.</p>'
            f'<div class="grid" style="grid-template-columns:1fr 1fr;gap:32px;margin-top:44px">'
            f'<div class="card k" style="min-height:460px"><h3>Cosa funziona già</h3>{ul(ok)}</div>'
            f'<div class="card or" style="min-height:460px"><h3>Dove possiamo crescere</h3>{ul(gr)}</div></div>')
    return page("dark", body, 8)

# ── 09 cosa ricevete ogni mese
def p09():
    cols = [("Contenuti", ["12 contenuti al mese in alta stagione", "2 video verticali al mese", "Foto e grafiche dagli shooting"]),
            ("Gestione e community", ["Instagram, Facebook, TikTok", "Google Business Profile", "Commenti, messaggi e recensioni"]),
            ("Advertising", ["Campagne Meta sulle prenotazioni", "Mercati esteri nella finestra giusta", "Budget media a parte"]),
            ("Strategia e report", ["Calendario editoriale condiviso", "Rapporto diretto con la direzione", "Report di stagione"])]
    cards = "".join(f'<div class="card c" style="border-top:8px solid {ORANGE};border-radius:6px 6px 18px 18px;min-height:470px">'
                    f'<h3>{E(t)}</h3>{ul(xs, "l tight")}</div>' for t, xs in cols)
    body = (f'<div class="eye">Il servizio</div><h1>Cosa ricevete</h1>'
            f'<div class="grid" style="grid-template-columns:repeat(4,1fr);gap:28px;margin-top:70px">{cards}</div>')
    return page("dark", body, 9)

# ── 10 investimento
def p10():
    rows = "".join(f'<div style="display:grid;grid-template-columns:1fr 360px 380px;align-items:center;padding:24px 34px;border-top:1px solid {SILVER}">'
                   f'<div><div style="font-weight:600;font-size:28px">{E(a)}</div><div class="sub" style="color:var(--c);margin-top:6px">{E(b)}</div></div>'
                   f'<div style="font-size:25px;color:var(--c)">{E(c)}</div>'
                   f'<div style="font-weight:600;font-size:28px;text-align:right">{E(d)}</div></div>' for a, b, c, d in ECONOMIA)
    head = (f'<div style="display:grid;grid-template-columns:1fr 360px 380px;padding:0 34px 16px" class="sub">'
            f'<div style="font-weight:600;letter-spacing:.12em;text-transform:uppercase">Fase</div>'
            f'<div style="font-weight:600;letter-spacing:.12em;text-transform:uppercase">Periodo</div>'
            f'<div style="font-weight:600;letter-spacing:.12em;text-transform:uppercase;text-align:right">Investimento</div></div>')
    tot = (f'<div style="display:grid;grid-template-columns:1fr 380px;align-items:center;padding:26px 34px;background:{ORANGE};color:{BLACK};border-radius:14px;margin-top:18px">'
           f'<div style="font-weight:600;font-size:28px">Totale gestione annua</div>'
           f'<div style="font-weight:600;font-size:50px;text-align:right">{E(TOTALE_ANNO)}</div></div>')
    body = (f'<div class="eye">Investimento</div><h1>Il riepilogo economico</h1>'
            f'<p class="lead">Dodici mesi, con l\'intensità che cambia tra bassa e alta stagione. IVA esclusa.</p>'
            f'<div style="margin-top:36px">{head}{rows}{tot}</div>'
            f'<p class="note" style="margin-top:22px">Budget pubblicitario e condizioni alla pagina successiva. Voci tecniche opzionali a pagina 12.</p>')
    return page("light", body, 10)

# ── 11 budget e condizioni
def p11():
    cond = [("Fatturazione mensile", "Una fattura sola, anche quando i brand seguiti sono due."),
            ("Produzione dilazionabile", "I 6.200 € della produzione si possono ripartire nel corso dell'anno."),
            ("Trasferte escluse", "Le trasferte per gli shooting sono a rimborso spese documentato."),
            ("Budget ADV separato", "Il budget pubblicitario non è compreso nel compenso di gestione.")]
    rows = "".join(f'<div style="padding:22px 0;border-top:1px solid {CHARCOAL}">'
                   f'<div style="font-weight:600;font-size:28px">{E(a)}</div>'
                   f'<div class="sub" style="margin-top:8px">{E(b)}</div></div>' for a, b in cond)
    body = (f'<div class="eye">Condizioni</div><h1>Budget pubblicitario e condizioni</h1>'
            f'<div class="grid" style="grid-template-columns:1fr 1.1fr;gap:44px;margin-top:44px">'
            f'<div class="card or" style="min-height:430px"><div class="sub" style="font-weight:600;letter-spacing:.12em;text-transform:uppercase">Budget Meta consigliato</div>'
            f'<div class="big" style="font-size:96px;margin:18px 0 10px">400 · 600 €</div>'
            f'<div style="font-size:28px;line-height:1.4">al mese, tutto l\'anno. Circa 6.000 € all\'anno.</div>'
            f'<div style="font-size:25px;line-height:1.4;margin-top:22px">È spesa pubblicitaria vostra, versata direttamente a Meta, separata dal compenso dello studio. '
            f'Più peso da dicembre a marzo, nella finestra di prenotazione, meno in piena estate.</div></div>'
            f'<div>{rows}</div></div>')
    return page("dark", body, 11)

# ── 12 voci opzionali (prezzi Nadir)
def p12():
    rows = "".join(f'<div style="display:grid;grid-template-columns:1fr 420px 420px;align-items:center;padding:24px 34px;border-top:1px solid {SILVER}">'
                   f'<div><div style="font-weight:600;font-size:28px">{E(a)}</div><div class="sub" style="color:var(--c);margin-top:6px">{E(b)}</div></div>'
                   f'<div style="font-weight:600;font-size:25px">{E(c)}</div>'
                   f'<div style="font-size:25px;color:var(--c);text-align:right">{E(d)}</div></div>' for a, b, c, d in OPZIONALI)
    head = (f'<div style="display:grid;grid-template-columns:1fr 420px 420px;padding:0 34px 16px" class="sub">'
            f'<div style="font-weight:600;letter-spacing:.12em;text-transform:uppercase">Voce</div>'
            f'<div style="font-weight:600;letter-spacing:.12em;text-transform:uppercase">Avvio</div>'
            f'<div style="font-weight:600;letter-spacing:.12em;text-transform:uppercase;text-align:right">Ricorrente</div></div>')
    body = (f'<div class="eye">Voci opzionali</div><h1>Sito, portali e tracciamento</h1>'
            f'<p class="lead">Si aggiungono alla gestione quando servono. Chi ha già un sito che funziona parte senza.</p>'
            f'<div style="margin-top:36px">{head}{rows}<div style="border-top:1px solid {SILVER}"></div></div>'
            f'<p class="note" style="margin-top:22px">Hosting 140 € all\'anno a parte. La licenza del motore di prenotazione resta in capo alla struttura. '
            f'Il sito è pronto in 4-6 settimane, i portali in 2-3.</p>')
    return page("light", body, 12)

# ── 13 team
def p13():
    soci = [("A", "Alex", "Fondatore"), ("R", "Riccardo", "Socio · Responsabile Social Media"), ("N", "Nadir", "Socio · Responsabile Siti Web")]
    coll = [("Claudio", "Strategia & Copywriter"), ("Gianmarco", "Videomaker"), ("Kevin", "Video Editor"),
            ("Mihaela", "Photographer"), ("Lia", "Graphic Designer"), ("Alessandro", "Ads Specialist")]
    sc = "".join(f'<div class="card c" style="display:flex;align-items:center;gap:28px;padding:34px 38px">'
                 f'<div style="width:96px;height:96px;border-radius:50%;background:{ORANGE};color:{BLACK};display:flex;align-items:center;justify-content:center;font-weight:600;font-size:44px;flex:none">{i}</div>'
                 f'<div><div style="font-weight:600;font-size:28px">{E(n)}</div><div class="sub" style="margin-top:6px">{E(r)}</div></div></div>' for i, n, r in soci)
    cc = "".join(f'<div style="border-top:1px solid {CHARCOAL};padding:20px 0"><div style="font-weight:600;font-size:25px">{E(n)}</div>'
                 f'<div class="sub" style="color:var(--s);margin-top:4px">{E(r)}</div></div>' for n, r in coll)
    body = (f'<div class="eye">Il team</div><h1>Le persone dietro YDG Studio</h1>'
            f'<p class="lead">Una squadra affiatata: le stesse persone seguono il progetto dall\'inizio alla fine.</p>'
            f'<div class="grid" style="grid-template-columns:repeat(3,1fr);gap:28px;margin-top:44px">{sc}</div>'
            f'<div class="sub" style="font-weight:600;letter-spacing:.12em;text-transform:uppercase;margin:46px 0 4px;color:var(--o)">I collaboratori</div>'
            f'<div class="grid" style="grid-template-columns:repeat(6,1fr);gap:0 30px">{cc}</div>')
    return page("dark", body, 13)

# ── 14 grazie
def p14():
    st = ["Conferma della proposta", "Definizione del budget pubblicitario", "Firma dell'accordo",
          "Primo shooting in struttura", "Avvio di gestione e campagne"]
    cols = "".join(f'<div style="position:relative;padding-top:50px">'
                   f'<div style="position:absolute;top:0;left:0;width:22px;height:22px;border-radius:50%;background:{BLACK}"></div>'
                   f'<div style="font-weight:600;font-size:50px">{i+1:02d}</div>'
                   f'<div style="font-size:25px;line-height:1.38;margin-top:12px">{E(t)}</div></div>' for i, t in enumerate(st))
    body = (f'<div style="position:absolute;top:120px;left:0;right:0"><div class="eye">Come partiamo</div>'
            f'<div class="big" style="margin-top:28px;font-size:96px">Grazie del tempo<br>che ci avete dato.</div>'
            f'<div style="position:relative;margin-top:60px"><div style="position:absolute;top:10px;left:0;right:0;height:2px;background:{BLACK};opacity:.25"></div>'
            f'<div class="grid" style="grid-template-columns:repeat(5,1fr);gap:36px;position:relative">{cols}</div></div>'
            f'<div style="display:flex;gap:90px;margin-top:70px">'
            f'<div><div class="sub" style="font-weight:600;letter-spacing:.12em;text-transform:uppercase">Email</div>'
            f'<div style="font-size:28px;font-weight:600;margin-top:8px">alextaroni@whydg.com</div></div>'
            f'<div><div class="sub" style="font-weight:600;letter-spacing:.12em;text-transform:uppercase">Telefono</div>'
            f'<div style="font-size:28px;font-weight:600;margin-top:8px">+39 339 114 9663</div></div></div>'
            f'<div class="note" style="margin-top:26px;color:var(--k)">Proposta valida 30 giorni · IVA esclusa</div></div>')
    return page("orange", body, 14)

PAGINE = [p01, p02, p03, p04, p05, p06, p07, p08, p09, p10, p11, p12, p13, p14]

if __name__ == "__main__":
    tmp = tempfile.mkdtemp(prefix="ydg_osp_")
    # il font si carica da un percorso relativo: si lavora accanto al kit
    work = tempfile.mkdtemp(prefix="ydg_work_", dir=BRAND)
    for d in ("font", "asset"):
        os.symlink(os.path.join(BRAND, d), os.path.join(work, d))
    hp = os.path.join(work, "proposta.html")
    open(hp, "w", encoding="utf-8").write(
        f'<!doctype html><html lang="it"><head><meta charset="utf-8"><style>{CSS}</style></head>'
        f'<body>{"".join(f() for f in PAGINE)}</body></html>')
    pdf = os.path.join(tmp, "out.pdf")
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                    f"--user-data-dir={tmp}/prof", "--virtual-time-budget=8000",
                    "--run-all-compositor-stages-before-draw", f"--print-to-pdf={pdf}", "file://" + hp],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    doc = fitz.open(pdf)
    doc.set_metadata({"title": f"Proposta di collaborazione · {CLIENTE['nome']}", "author": "YDG Studio",
                      "subject": "Verticale ospitalità · proposta di collaborazione"})
    doc.save(OUT, garbage=3, deflate=True)
    print("PDF:", OUT, len(doc), "pagine,", os.path.getsize(OUT)//1024, "KB")
    prev = os.path.join(HERE, "_anteprime")
    shutil.rmtree(prev, ignore_errors=True); os.makedirs(prev)
    for i, pg in enumerate(doc):
        pg.get_pixmap(matrix=fitz.Matrix(1500/pg.rect.width, 1500/pg.rect.width), alpha=False).save(
            os.path.join(prev, f"{i+1:02d}.png"))
    shutil.rmtree(work, ignore_errors=True); shutil.rmtree(tmp, ignore_errors=True)
