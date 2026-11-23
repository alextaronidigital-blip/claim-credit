"""Proposta di acquisizione · verticale OSPITALITA, brand YDG Studio.

Fusione di due documenti che esistono gia':

  - la proposta standard di Riccardo (Love Luck Tattoo, nov 2026) da' l'impianto:
    testata e numerazione su ogni pagina, chi siamo, chi ci ha scelto, casi studio,
    analisi in superficie, servizi, prezzi, prossimi passi, pagina finale arancio;
  - la proposta di rinnovo di Villa Campomaggio da' il rigore tipografico, la
    profondita' sui servizi e l'impianto economico diviso per voci.

Perche' non parte dai dati: Campomaggio e' un rinnovo, li' i numeri dell'anno
precedente li abbiamo fatti noi. Qui la struttura non ci conosce e noi non sappiamo
come lavora davvero. Quindi si analizza in superficie quello che si vede da fuori,
se ne spiegano le potenzialita', e si passa subito ai servizi e al loro costo.

Tre servizi, una pagina ciascuno:
  - gestione social                     (Alex, Riccardo)
  - gestione advertising                (Alessandro)
  - sviluppo e gestione del sito web    (Nadir)

Esempio compilato su Hotel Heubad (Fie allo Sciliar), presa dalla lista dell'hub.
Per un'altra struttura si cambiano STRUTTURA, ANALISI e DIREZIONE.

Font: dal kit del brand se c'e' (Mac), altrimenti Inter come sostituto per la sola
anteprima. Il PDF definitivo si fa dove c'e' il kit.

Uso:  python3 build_proposta_acquisizione.py
"""
import os, sys, html

HERE = os.path.dirname(os.path.abspath(__file__))
BRAND = os.path.expanduser("~/Desktop/Y/BRAND YDG STUDIO/Preventivo (mockup)/_sorgente")
FONTDIR = os.path.join(BRAND, "font")
KIT = os.path.isdir(FONTDIR)
E = html.escape

# Valori dal Codice del brand v1.0, gli stessi letti dal CSS del sito nuovo.
ORANGE, INK, DEEP = "#FF7900", "#1A1A1A", "#111111"
CARD, GREY, LIGHT, HAIR = "#1E1E1E", "#a9a9a6", "#F2F2F2", "#DEDEDA"

# ─────────────────────────────────────────────── la struttura, da cambiare
STRUTTURA = {
    "nome": "Hotel Heubad",
    "dove": "Hotel con spa, piscine e ristorante · Fiè allo Sciliar (BZ)",
    "data": "Novembre 2026",
    "validita": "Proposta valida per 30 giorni",
}

# Analisi in superficie: quello che si vede da fuori, senza entrare in struttura.
# Niente numeri spacciati per diagnosi: sono osservazioni, e lo diciamo.
ANALISI = {
    "intro": "Una lettura di quello che si vede da fuori, come la farebbe un ospite "
             "che non vi conosce. Il quadro vero lo costruiamo insieme, alla prima chiamata.",
    "funziona": [
        "Una reputazione che pochi hanno: 4,7 di media su oltre 280 recensioni",
        "Ospiti che tornano da dieci anni e lo scrivono",
        "Spa, piscine e ristorante: c'è già tutto quello che serve da raccontare",
        "La posizione, ai piedi dello Sciliar e a due passi dall'Alpe di Siusi",
    ],
    "crescere": [
        "Presenza social: dal sito non si arriva a nessun profilo",
        "Visibilità: chi non vi conosce non ha modo di incontrarvi online",
        "Finestra di prenotazione: inverno ed estate si decidono con mesi di anticipo",
        "Prenotazione diretta: oggi passa soprattutto dai portali, che trattengono commissioni",
    ],
}

DIREZIONE = {
    "intro": "Una presenza che faccia vedere a chi non c'è mai stato quello che gli ospiti "
             "abituali già sanno. È una direzione di partenza: la definiamo insieme a voi.",
    "vedrete": [
        "La struttura raccontata nelle due stagioni, non solo in cartolina",
        "Spa, camere, cucina e persone, fotografate con continuità",
        "Un profilo vivo anche nei mesi in cui si prenota, non solo quando siete pieni",
    ],
    "come": [
        "Un'identità visiva coerente, contenuto dopo contenuto",
        "Campagne verso chi sta scegliendo dove andare, nei mesi giusti",
        "Un sito che converte le visite in prenotazioni diratte",
        "Numeri alla mano ogni tre mesi, sugli stessi indicatori",
    ],
}

# ─────────────────────────────────────────────── chi siamo
STUDIO_FA = ["Social", "Siti web", "Advertising", "Foto", "Video", "Branding",
             "Grafica", "Stampa", "E-commerce"]
PUNTI_FORZA = [
    "Tutto in-house, un'unica regia per ogni contenuto",
    "Presenza e shooting in loco, non solo da remoto",
    "Gestione manuale e strategica, mai automatismi",
    "La stessa squadra che vi segue, con risposte veloci",
    "Report trasparenti: è chiaro cosa portiamo",
]
CLIENTI = ["Hotel Villa Campomaggio", "Ristorante La Gabbia", "Romagna Free",
           "Trattoria Ca' Rossi", "La Piadina della Baracchina", "Somec",
           "Spiedo Imperiale", "Bocon Divino", "Ribò Professional",
           "Lattuga Giulio", "Be Balance Fitness Hub", "Ottica Bonora",
           "Moto 2000", "Ofelia Parrucchiere", "Crazy Beauty"]

# Casi studio: numeri reali, dalle proposte di Campomaggio e dal materiale di Riccardo.
CASI = [
    ("Hotel Villa Campomaggio", "Hotel nel Chianti · 2 stagioni", [
        ("+1.324", "nuovi follower in una stagione"),
        ("392.075", "impression organiche"),
        ("2.741", "visite al sito prima della riapertura"),
        ("€ 0,15", "costo per visita dalle campagne"),
    ]),
    ("La Gabbia Tuscany Lounge", "Ristorante · nuova apertura", [
        ("+1.200.000", "impression su Instagram partendo da 0"),
        ("+285.000", "singoli account raggiunti"),
        ("+3.000", "follower costruiti in una stagione"),
        ("50", "contenuti professionali pubblicati"),
    ]),
    ("Be Balance Fitness Hub", "Centro fitness · nuova apertura", [
        ("+274.000", "impression su IG e FB in 4 mesi"),
        ("+10.000", "visite al profilo"),
        ("+820", "nuovi follower partendo da 0"),
        ("€ 0,05", "costo per click delle campagne"),
    ]),
]

# ─────────────────────────────────────────────── i tre servizi
SERVIZI = [
    {
        "n": "01", "nome": "Gestione social", "chi": "Alex e Riccardo",
        "claim": "Qualcosa da guardare, tutto l'anno.",
        "intro": "In alta stagione si racconta la struttura piena. In bassa si costruisce "
                 "la domanda per quella dopo: i profili restano vivi mentre la gente decide.",
        "a": ("Ogni mese ricevete", [
            "8 contenuti in alta stagione tra foto, video e grafiche",
            "2 video verticali al mese",
            "Storie, commenti e messaggi presidiati",
            "Gestione delle recensioni e della community",
            "Calendario editoriale condiviso in anticipo",
        ]),
        "b": ("Nell'anno", [
            "Shooting di avvio: struttura, camere, spa, ristorante",
            "Uno shooting a stagione, per seguire la montagna che cambia",
            "Instagram, Facebook e Google Business Profile",
            "Profilo TikTok se decidiamo insieme che ha senso",
            "Report ogni tre mesi sugli stessi indicatori",
        ]),
    },
    {
        "n": "02", "nome": "Gestione advertising", "chi": "Alessandro",
        "claim": "Davanti a chi sta ancora scegliendo.",
        "intro": "I contenuti parlano a chi vi ha già trovati. L'advertising vi mette davanti "
                 "a chi non sa che esistete, mentre sta decidendo dove andare.",
        "a": ("Che cosa facciamo", [
            "Campagne su Meta e Google verso i mercati che vi interessano",
            "Pubblico costruito su chi cerca una vacanza in Dolomiti",
            "Campagne di notorietà e campagne che portano prenotazioni",
            "Ottimizzazione continua, non una tantum",
            "Report mensile: costo per visita, costo per contatto, clic al sito",
        ]),
        "b": ("Due cose da chiarire subito", [
            "Il budget pubblicitario non è compreso nel compenso: lo versate "
            "direttamente a Meta e Google e resta vostro",
            "Budget consigliato per una struttura come la vostra: da 400 a 600 €/mese",
            "Si parte dai mesi in cui si decide, non da quelli in cui siete già pieni",
        ]),
    },
    {
        "n": "03", "nome": "Sviluppo e gestione del sito web", "chi": "Nadir",
        "claim": "Il posto dove atterra tutto il resto.",
        "intro": "Contenuti e campagne portano persone da qualche parte. Se quel posto non "
                 "converte, il lavoro di prima si disperde — e la prenotazione resta ai portali.",
        "a": ("Il sito", [
            "Restyling completo, pensato prima per il telefono",
            "Motore di prenotazione collegato: si prenota da voi, non solo dai portali",
            "Pronto in 4–6 settimane dalla conferma",
            "Tracciamento incluso: GA4, Tag Manager, Pixel di Meta",
            "Manutenzione annuale: sicurezza, backup, aggiornamenti",
        ]),
        "b": ("I portali", [
            "Booking e Airbnb: schede, tariffe, disponibilità",
            "Channel manager collegato, niente doppie prenotazioni",
            "Attivazione in 2–3 settimane, per le verifiche delle piattaforme",
            "Monitoraggio mensile, report trimestrale",
            "Commissioni e abbonamenti dei portali restano a vostro carico",
        ]),
    },
]

# ─────────────────────────────────────────────── economia
# Sito, portali e tracciamento: listino Nadir, caso B (sito da rifare).
# Social e ADV: adattati da Campomaggio a una struttura sola — DA CONFERMARE.
PREZZI = [
    {"nome": "Gestione social", "tag": "Alex e Riccardo",
     "avvio": "3.500 €", "avvio_cosa": "Shooting di avvio e prima libreria contenuti",
     "mese": "1.400 €", "mese_nota": "al mese in alta stagione · 900 € in bassa",
     "spot": True},
    {"nome": "Gestione advertising", "tag": "Alessandro",
     "avvio": "incluso", "avvio_cosa": "Impostazione account, pubblici e tracciamento campagne",
     "mese": "500 €", "mese_nota": "al mese, tutto l'anno · budget pubblicitario a parte",
     "spot": False},
    {"nome": "Sito web e portali", "tag": "Nadir",
     "avvio": "3.100 €", "avvio_cosa": "Sito con prenotazione 2.200 € · Booking e Airbnb 900 €",
     "mese": "da 1.140 €", "mese_nota": "all'anno di canoni: manutenzione, portali, hosting",
     "spot": False},
]

RIEPILOGO = [
    ("Avvio", "Una tantum", "Shooting, sito con prenotazione, portali e tracciamento", "6.600 €", True),
    ("Mesi 1–8", "Alta stagione", "Social completo e advertising · dic–mar e giu–set", "1.900 €/mese", True),
    ("Mesi 9–12", "Bassa stagione", "Presidio social e advertising · apr–mag e ott–nov", "1.400 €/mese", True),
    ("Canoni", "Annuali", "Manutenzione sito, gestione portali, hosting", "da 1.140 €/anno", False),
]
TOTALE = "da 28.540 €"
TOTALE_NOTA = "Primo anno completo · avvio 6.600 € + gestione 20.800 € + canoni da 1.140 €"
NOTE_ECONOMIA = [
    "Budget pubblicitario escluso: da 400 a 600 €/mese, versati da voi direttamente a Meta e Google.",
    "Fatture separate per servizio: social e produzione, advertising, sito e portali.",
    "Esclusi: modelli per gli shooting, licenza del motore di prenotazione, commissioni dei portali. "
    "Ogni servizio si può attivare da solo, agli stessi prezzi.",
]

EXTRA = [
    ("Contenuti e produzione", [
        "Video istituzionale per la homepage e le campagne",
        "Shooting dedicato a un'apertura o a una ristrutturazione",
        "Più pubblicazioni al mese",
    ]),
    ("Brand e materiali", [
        "Brochure e PDF di presentazione della struttura",
        "Grafiche per la stampa: menu, biglietti, materiali in camera",
        "CRM ed email marketing verso gli ospiti passati",
    ]),
]

PASSI = [
    ("01", "Conferma della proposta e accessi"),
    ("02", "Chiamata di scoperta e impostazione della strategia"),
    ("03", "Definizione del budget pubblicitario"),
    ("04", "Shooting di avvio in struttura"),
    ("05", "Calendario editoriale, campagne e sito online"),
]
PASSI_CODA = ("Il primo mese è di fondamenta e non si pubblica niente.",
              " La delivery comincia dal secondo: chi parte a pubblicare il primo giorno sta improvvisando.")

CONTATTI = [("Riccardo Milonean", "riccardo@ydgstudio.com", "+39 346 615 5886"),
            ("Alessandro Eusebio", "tea.alessandroeusebio@gmail.com", "+39 349 974 5528")]


# ─────────────────────────────────────────────── impianto grafico
def css():
    if KIT:
        facce = "".join(
            f"@font-face{{font-family:'Brand';src:url('file://{FONTDIR}/{f}');"
            f"font-weight:{w};font-style:normal;font-display:block}}"
            for f, w in (("OverusedGrotesk-Book.woff2", 400),
                         ("OverusedGrotesk-Medium.woff2", 500),
                         ("OverusedGrotesk-SemiBold.woff2", 600),
                         ("OverusedGrotesk-Bold.woff2", 700)))
        famiglia = "'Brand', 'Inter', sans-serif"
    else:
        facce, famiglia = "", "'Inter', 'Inter Display', sans-serif"
    return facce + f"""
*{{margin:0;padding:0;box-sizing:border-box;-webkit-print-color-adjust:exact;print-color-adjust:exact}}
html,body{{font-family:{famiglia};background:{INK}}}
.p{{width:1280px;height:720px;position:relative;overflow:hidden;background:{LIGHT};color:{INK};
   page-break-after:always;display:flex;flex-direction:column;padding:44px 56px 58px}}
.p.scura{{background:{DEEP};color:#fff}}
.p.arancio{{background:{ORANGE};color:{INK}}}

/* testata e numerazione, su ogni pagina: e' la firma del documento standard */
.testa{{display:flex;justify-content:space-between;align-items:center;flex:0 0 auto}}
.marchio{{display:flex;align-items:center;gap:9px;font-size:23px;font-weight:700;letter-spacing:-.045em}}
.marchio .st{{font-weight:400;letter-spacing:-.02em}}
.marchio .seg{{width:17px;height:17px;background:currentColor;
  clip-path:polygon(100% 0,100% 100%,30% 72%,0 50%,30% 28%)}}
.doc{{font-size:12.5px;color:#8c8c89}}
.p.scura .doc{{color:#7d7d7a}} .p.arancio .doc{{color:rgba(26,26,26,.62)}}
.pag{{position:absolute;left:56px;bottom:26px;font-size:12px;color:#8c8c89}}
.pag b{{color:{INK};font-weight:600}}
.p.scura .pag b{{color:#fff}} .p.scura .pag{{color:#7d7d7a}}

.corpo{{flex:1;display:flex;flex-direction:column;min-height:0;padding-top:46px}}
.occhiello{{display:flex;align-items:center;gap:10px;font-size:11.5px;font-weight:600;
          letter-spacing:.11em;text-transform:uppercase;color:{INK}}}
.occhiello::before{{content:"";width:9px;height:9px;background:{ORANGE};flex:0 0 auto}}
.p.scura .occhiello{{color:#fff}}
h1{{font-size:40px;font-weight:600;letter-spacing:-.035em;line-height:1.05;margin:13px 0 0}}
.sotto{{font-size:15.5px;line-height:1.5;color:#5f5f5c;margin-top:12px;max-width:86ch}}
.sotto b{{color:{INK};font-weight:600}}
.p.scura .sotto{{color:{GREY}}} .p.scura .sotto b{{color:#fff}}

.griglia{{display:grid;gap:17px;margin-top:34px;flex:0 0 auto}}
.griglia.cresci{{flex:1;align-items:stretch;min-height:0}}
.g2{{grid-template-columns:1fr 1fr}} .g3{{grid-template-columns:repeat(3,1fr)}}
.g4{{grid-template-columns:repeat(4,1fr)}} .g5{{grid-template-columns:repeat(5,1fr)}}

/* le card nere con la barra arancio in cima sono l'elemento ricorrente */
.card{{background:{CARD};color:#fff;border-radius:18px;padding:24px 24px 26px;position:relative;
     overflow:hidden;display:flex;flex-direction:column}}
.card.barra{{border-top:4px solid {ORANGE}}}
.card.chiara{{background:#fff;color:{INK}}}
.card.spot{{background:{ORANGE};color:{INK}}}
.card h3{{font-size:18px;font-weight:600;letter-spacing:-.022em;margin:0 0 13px}}
.occh{{font-size:11px;font-weight:600;letter-spacing:.1em;text-transform:uppercase;
     color:{ORANGE};margin-bottom:9px}}
.card.spot .occh{{color:rgba(26,26,26,.6)}}
.card p{{font-size:13.5px;line-height:1.52;color:{GREY}}}
.card.chiara p,.card.spot p{{color:#5f5f5c}}
.card.spot p{{color:rgba(26,26,26,.72)}}

ul{{list-style:none}}
li{{font-size:13.5px;line-height:1.5;padding-left:17px;position:relative;margin-bottom:11px;color:{GREY}}}
li:last-child{{margin-bottom:0}}
li::before{{content:"";position:absolute;left:0;top:7px;width:6px;height:6px;border-radius:50%;background:{ORANGE}}}
.card.chiara li{{color:#5f5f5c}}
.card.spot li{{color:rgba(26,26,26,.82)}} .card.spot li::before{{background:{INK}}}
li b{{color:#fff;font-weight:600}} .card.spot li b{{color:{INK}}}

.dato{{font-size:30px;font-weight:600;letter-spacing:-.035em;color:{ORANGE};line-height:1.05}}
.et{{font-size:12px;line-height:1.4;color:{GREY};margin-top:6px}}
.riga-dato{{padding:13px 0;border-bottom:1px solid rgba(255,255,255,.1)}}
.riga-dato:last-child{{border-bottom:0;padding-bottom:0}}

/* tabella del riepilogo economico, con la barra arancio a sinistra */
table{{width:100%;border-collapse:collapse;margin-top:22px}}
th{{font-size:10.5px;font-weight:600;letter-spacing:.1em;text-transform:uppercase;color:#8c8c89;
   text-align:left;padding:0 0 11px}}
th.d{{text-align:right}}
td{{padding:9px 0;border-bottom:1px solid {HAIR};vertical-align:middle}}
tr.evid td{{background:#FAEDE0}}
tr.evid td:first-child{{box-shadow:inset 4px 0 0 {ORANGE}}}
td.q{{padding-left:17px;width:168px}}
td.d{{text-align:right;padding-right:17px;white-space:nowrap}}
.voce{{font-size:16px;font-weight:600;letter-spacing:-.02em}}
.sub{{font-size:12px;color:#8c8c89;margin-top:3px}}
.cosa{{font-size:14px;color:#5f5f5c}}
.cifra{{font-size:20px;font-weight:600;letter-spacing:-.025em}}

.fascia{{background:{DEEP};color:#fff;border-radius:18px;padding:17px 30px;margin-top:12px;
       display:flex;align-items:center;justify-content:space-between}}
.fascia .t{{font-size:17px;font-weight:600;letter-spacing:-.02em}}
.fascia .t small{{display:block;font-size:12px;font-weight:400;color:{GREY};margin-top:5px;letter-spacing:0}}
.fascia .c{{font-size:42px;font-weight:600;color:{ORANGE};letter-spacing:-.035em}}
.note{{margin-top:13px}}
.note div{{font-size:11.5px;color:#8c8c89;line-height:1.5}}

/* copertina e chiusura */
.p.cop{{background:{DEEP};color:#fff;justify-content:flex-start}}
.alone{{position:absolute;width:1100px;height:1100px;right:-300px;bottom:-620px;border-radius:50%;
      background:radial-gradient(circle,rgba(255,121,0,.85),rgba(255,121,0,.22) 48%,rgba(255,121,0,0) 70%)}}
.cop .corpo{{justify-content:center;position:relative;z-index:1}}
.cop h1{{font-size:68px;line-height:1.02;letter-spacing:-.04em}}
.cop h1 .n{{color:{ORANGE};display:block}}
.cop .dove{{font-size:16px;color:{GREY};margin-top:22px}}
.ins{{font-size:11.5px;font-weight:600;letter-spacing:.11em;text-transform:uppercase;color:{ORANGE}}}
.p.arancio h1{{font-size:56px;line-height:1.05}}
.p.arancio .occhiello{{color:{INK}}} .p.arancio .occhiello::before{{background:{INK}}}
.p.arancio .pag,.p.arancio .pag b{{color:rgba(26,26,26,.6)}}
.cont{{display:flex;gap:64px;margin-top:40px}}
.cont .k{{font-size:10.5px;font-weight:600;letter-spacing:.11em;text-transform:uppercase;
        color:rgba(26,26,26,.6);margin-bottom:7px}}
.cont .v{{font-size:16px;font-weight:600}}
.valid{{font-size:12px;color:rgba(26,26,26,.6);margin-top:30px}}

.pill{{display:inline-flex;align-items:center;gap:8px;background:#fff;border-radius:11px;
     padding:11px 14px;font-size:13px;font-weight:500}}
.p.scura .pill{{background:{CARD};color:#fff}}
.pill .pt{{width:7px;height:7px;border-radius:50%;background:{ORANGE};flex:0 0 auto}}
"""


def testa(cls=""):
    return (f'<div class="testa"><div class="marchio">YDG<span class="seg"></span>'
            f'<span class="st">STUDIO</span></div>'
            f'<div class="doc">Proposta di collaborazione · {E(STRUTTURA["nome"])}</div></div>')


def pagina(corpo, n, cls="", occhiello=None, titolo=None, sotto=None):
    t = ""
    if occhiello:
        t += f'<div class="occhiello">{E(occhiello)}</div>'
    if titolo:
        t += f"<h1>{titolo}</h1>"
    if sotto:
        t += f'<p class="sotto">{sotto}</p>'
    return (f'<section class="p {cls}">{testa()}'
            f'<div class="corpo">{t}{corpo}</div>'
            f'<div class="pag"><b>{n:02d}</b> / {TOT_PAGINE}</div></section>')


def ul(xs):
    return "<ul>" + "".join(f"<li>{x}</li>" for x in xs) + "</ul>"


def card(titolo, voci, cls="barra", occh=None):
    o = f'<div class="occh">{E(occh)}</div>' if occh else ""
    return f'<div class="card {cls}">{o}<h3>{E(titolo)}</h3>{ul(voci)}</div>'


# ─────────────────────────────────────────────── le pagine
TOT_PAGINE = 15

def p01():
    return f"""<section class="p cop"><div class="alone"></div>{testa()}
<div class="corpo">
  <div class="ins">Proposta di collaborazione</div>
  <h1 style="margin-top:22px">Facciamo crescere<span class="n">{E(STRUTTURA['nome'])}</span></h1>
  <div class="dove">{E(STRUTTURA['dove'])}</div>
</div>
<div class="pag" style="color:#7d7d7a">{E(STRUTTURA['data'])}</div></section>"""

def p02():
    pill = "".join(f'<div class="pill"><span class="pt"></span>{E(x)}</div>' for x in STUDIO_FA)
    corpo = f"""<div class="griglia g2 cresci" style="grid-template-columns:1.05fr .95fr">
  <div>
    <div class="occh" style="color:#8c8c89">Cosa fa lo studio</div>
    <div style="display:flex;flex-wrap:wrap;gap:10px;margin-top:4px">{pill}</div>
  </div>
  {card("I nostri punti di forza", PUNTI_FORZA)}
</div>"""
    return pagina(corpo, 2, occhiello="Chi siamo",
                  titolo="Un'unica squadra per tutta la vostra comunicazione digitale.",
                  sotto="<b>YDG Studio</b> è uno studio di comunicazione digitale con base in Romagna. "
                        "Aiutiamo PMI, brand e attività locali a crescere online con una comunicazione "
                        "curata, coerente e fatta su misura.")

def p03():
    c = "".join(f'<div class="card" style="padding:17px 20px;justify-content:center">'
                f'<div style="font-size:14.5px;font-weight:500;line-height:1.3">{E(x)}</div></div>'
                for x in CLIENTI)
    corpo = f'<div class="griglia g5 cresci" style="gap:13px">{c}</div>'
    return pagina(corpo, 3, "scura", occhiello="Hanno scelto YDG Studio",
                  titolo="Oltre 50 attività ci hanno affidato la loro presenza digitale.",
                  sotto="Ristoranti, hotel, negozi e studi professionali. Settori diversi, "
                        "stesso metodo.")

def p04():
    c = ""
    for nome, sotto, voci in CASI:
        righe = "".join(f'<div class="riga-dato"><div class="dato">{E(v)}</div>'
                        f'<div class="et">{E(t)}</div></div>' for v, t in voci)
        c += (f'<div class="card barra"><h3 style="margin-bottom:3px">{E(nome)}</h3>'
              f'<div class="et" style="margin:0 0 7px">{E(sotto)}</div>{righe}</div>')
    corpo = f'<div class="griglia g3 cresci">{c}</div>'
    return pagina(corpo, 4, "scura", occhiello="Casi studio",
                  titolo="Risultati reali, su settori diversi.",
                  sotto="Numeri dei nostri clienti, verificabili. Non proiezioni.")

def p05():
    corpo = f"""<div class="griglia g2 cresci">
  {card("Cosa funziona già", ANALISI['funziona'])}
  {card("Dove possiamo crescere", ANALISI['crescere'], "spot")}
</div>"""
    return pagina(corpo, 5, occhiello="Analisi iniziale", titolo="Da dove partiamo",
                  sotto=E(ANALISI["intro"]))

def p06():
    corpo = f"""<div class="griglia g2 cresci">
  {card("Cosa vedrete sui profili", DIREZIONE['vedrete'])}
  {card("Come lo costruiamo", DIREZIONE['come'], "spot")}
</div>"""
    return pagina(corpo, 6, occhiello="La direzione", titolo="Dove vogliamo andare",
                  sotto=E(DIREZIONE["intro"]))

def p07():
    c = "".join(f'<div class="card barra"><div class="occh">{E(s["n"])} · {E(s["chi"])}</div>'
                f'<h3>{E(s["nome"])}</h3><p>{E(s["claim"])}</p></div>' for s in SERVIZI)
    corpo = f'<div class="griglia g3 cresci">{c}</div>'
    return pagina(corpo, 7, "scura", occhiello="I servizi",
                  titolo="Tre fronti, un solo interlocutore.",
                  sotto="Si possono attivare anche separati. Insieme lavorano meglio: le campagne "
                        "spingono su un sito che converte, i contenuti danno alle campagne "
                        "qualcosa da mostrare.")

def servizio(s, n):
    corpo = f"""<div class="griglia g2 cresci">
  {card(s['a'][0], s['a'][1])}
  {card(s['b'][0], s['b'][1], "spot")}
</div>"""
    return pagina(corpo, n, occhiello=f"Servizio {s['n']} · {s['nome']}",
                  titolo=E(s["claim"]), sotto=E(s["intro"]))

def p08(): return servizio(SERVIZI[0], 8)
def p09(): return servizio(SERVIZI[1], 9)
def p10(): return servizio(SERVIZI[2], 10)

def p11():
    c = ""
    for v in PREZZI:
        cls = "card spot" if v["spot"] else "card barra"
        sec = "rgba(26,26,26,.6)" if v["spot"] else "#8c8c89"
        c += f"""<div class="{cls}">
  <div class="occh">{E(v['tag'])}</div><h3 style="margin-bottom:16px">{E(v['nome'])}</h3>
  <div style="font-size:12px;letter-spacing:.09em;text-transform:uppercase;color:{sec}">Avvio</div>
  <div style="font-size:27px;font-weight:600;letter-spacing:-.03em;margin-top:4px">{E(v['avvio'])}</div>
  <div style="font-size:12.5px;line-height:1.45;color:{sec};margin-top:5px">{E(v['avvio_cosa'])}</div>
  <div style="height:1px;background:{sec};opacity:.28;margin:16px 0"></div>
  <div style="font-size:12px;letter-spacing:.09em;text-transform:uppercase;color:{sec}">Poi</div>
  <div style="font-size:27px;font-weight:600;letter-spacing:-.03em;margin-top:4px">{E(v['mese'])}</div>
  <div style="font-size:12.5px;line-height:1.45;color:{sec};margin-top:5px">{E(v['mese_nota'])}</div>
</div>"""
    corpo = f'<div class="griglia g3 cresci">{c}</div>'
    return pagina(corpo, 11, occhiello="La proposta", titolo="Quanto costa, servizio per servizio",
                  sotto="Ogni voce si può prendere da sola. Qui sotto, nella pagina seguente, "
                        "il quadro completo del primo anno.")

def p12():
    righe = ""
    for q, sub, cosa, cifra, evid in RIEPILOGO:
        righe += (f'<tr class="{"evid" if evid else ""}"><td class="q"><div class="voce">{E(q)}</div>'
                  f'<div class="sub">{E(sub)}</div></td>'
                  f'<td><div class="cosa">{E(cosa)}</div></td>'
                  f'<td class="d"><div class="cifra">{E(cifra)}</div></td></tr>')
    note = "".join(f"<div>{E(x)}</div>" for x in NOTE_ECONOMIA)
    corpo = f"""<table><tr><th class="q">Periodo</th><th>Cosa ottenete</th>
  <th class="d">Investimento</th></tr>{righe}</table>
<div class="fascia"><div class="t">Totale primo anno<small>{E(TOTALE_NOTA)}</small></div>
  <div class="c">{E(TOTALE)}</div></div>
<div class="note">{note}</div>"""
    return pagina(corpo, 12, occhiello="Investimento", titolo="Il riepilogo economico",
                  sotto="La fascia evidenziata è il percorso completo: avvio più dodici mesi di gestione.")

def p13():
    c = "".join(card(t, v) for t, v in EXTRA)
    corpo = f'<div class="griglia g2 cresci">{c}</div>'
    return pagina(corpo, 13, "scura", occhiello="Facciamo di più",
                  titolo="Cosa potremmo fare di più",
                  sotto="Servizi extra da aggiungere quando servono, con quotazioni dedicate.")

def p14():
    punti = "".join(
        f'<div><div style="width:13px;height:13px;border-radius:50%;background:{ORANGE}"></div>'
        f'<div style="font-size:30px;font-weight:600;letter-spacing:-.03em;margin:20px 0 9px">{n}</div>'
        f'<div style="font-size:13.5px;line-height:1.5;color:#5f5f5c">{E(t)}</div></div>'
        for n, t in PASSI)
    corpo = f"""<div style="position:relative;margin-top:52px">
  <div style="position:absolute;left:6px;right:6px;top:6px;height:1px;background:{HAIR}"></div>
  <div style="position:relative;display:grid;grid-template-columns:repeat(5,1fr);gap:26px">{punti}</div>
</div>
<p class="sotto" style="margin-top:auto;margin-bottom:8px;font-size:16px">
  <b>{E(PASSI_CODA[0])}</b>{E(PASSI_CODA[1])}</p>"""
    return pagina(corpo, 14, occhiello="Prossimi passi", titolo="Come partiamo")

def p15():
    c = "".join(f'<div><div class="k">{E(n)}</div><div class="v">{E(m)}</div>'
                f'<div class="v" style="font-weight:400;margin-top:3px">{E(t)}</div></div>'
                for n, m, t in CONTATTI)
    return f"""<section class="p arancio">{testa()}
<div class="corpo" style="justify-content:center">
  <div class="occhiello">Grazie</div>
  <h1 style="margin-top:16px">Diamo forma al racconto di<br>{E(STRUTTURA['nome'])}</h1>
  <div class="cont">{c}</div>
  <div class="valid">{E(STRUTTURA['validita'])}</div>
</div>
<div class="pag"><b>{TOT_PAGINE}</b> / {TOT_PAGINE}</div></section>"""

PAGINE = [p01, p02, p03, p04, p05, p06, p07, p08, p09, p10, p11, p12, p13, p14, p15]


# ─────────────────────────────────────────────── resa
OUT = os.path.join(HERE, f"Proposta ospitalita - {STRUTTURA['nome']}.pdf")
ANTEPRIME = os.path.join(HERE, "_anteprime_acquisizione")

def documento():
    return ("<!doctype html><html lang='it'><head><meta charset='utf-8'>"
            f"<style>{css()}</style></head><body>"
            + "".join(p() for p in PAGINE) + "</body></html>")

def rendi():
    """HTML sul disco, poi Chromium via Node: qui Playwright e' quello di Node."""
    import json, subprocess
    sorgente = os.path.join(HERE, "_proposta.html")
    open(sorgente, "w", encoding="utf8").write(documento())
    amb = dict(os.environ)
    amb.setdefault("NODE_PATH", "/opt/node-tools/node_modules")
    amb.setdefault("PLAYWRIGHT_PATH", "/opt/node-tools/node_modules/playwright")
    r = subprocess.run(["node", os.path.join(HERE, "rendi.mjs"), sorgente, OUT, ANTEPRIME],
                       capture_output=True, text=True, cwd=HERE, env=amb)
    if r.returncode:
        sys.exit("resa fallita:\n" + r.stderr[-1500:])
    troppo = json.loads(r.stdout.strip().splitlines()[-1])["sfori"]
    for t in troppo:
        print(f"  ! pagina {t['n']}: {t['h']}px, sfora di {t['h']-720}")
    return troppo

if __name__ == "__main__":
    if not KIT:
        print("· kit del brand assente: anteprima con Inter al posto di Overused Grotesk.")
        print("  Il PDF definitivo va rifatto dove c'e' il kit, su Mac.")
    sfori = rendi()
    print(f"✓ {len(PAGINE)} pagine → {OUT}")
    print(f"✓ anteprime → {ANTEPRIME}")
    print("✗ pagine che sforano: " + str(len(sfori)) if sfori else "✓ nessuna pagina sfora")
