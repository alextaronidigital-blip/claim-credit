"""Proposta di acquisizione · verticale OSPITALITA, brand YDG Studio.

Impianto e linguaggio visivo della proposta standard di Riccardo (Love Luck Tattoo,
novembre 2026): stessa testata, stessa numerazione, stessi occhielli, stesse card,
stessa palette, stessa chiusura arancio. Marchio, icone, loghi dei clienti e sfondo
della copertina sono le immagini estratte da quel PDF (vedi brand/LEGGIMI.md);
il font e' Overused Grotesk, lo stesso incorporato li' e sul sito.

Dalla proposta di Villa Campomaggio arrivano i tre servizi e l'economia per voci.

Non si apre con i dati della struttura: Campomaggio e' un rinnovo e quei numeri li
abbiamo fatti noi. Qui la struttura non ci conosce, quindi si legge in superficie
quello che si vede da fuori e si passa subito ai servizi e ai prezzi.

Nove pagine: copertina · chi siamo e chi ci ha scelto · casi studio · da dove
partiamo e dove vogliamo andare · i tre servizi · la proposta · il riepilogo
economico · come partiamo · grazie.

Esempio su Hotel Heubad (Fie allo Sciliar), dalla lista dell'hub. Per un'altra
struttura si cambiano STRUTTURA e ANALISI.

Uso:  python3 build_proposta_acquisizione.py
"""
import os, sys, html

HERE = os.path.dirname(os.path.abspath(__file__))
BRAND = os.path.join(HERE, "brand")
E = html.escape
U = lambda *p: "file://" + os.path.join(BRAND, *p)

# Palette misurata sulle pagine del PDF di riferimento, non scelta a occhio.
ARANCIO, NERO, GRIGIO, CHIARO = "#FF7900", "#1A1A1A", "#4D4D4D", "#F2F2F2"
EVID = "#F3E3D4"

# ─────────────────────────────────────────────── la struttura, da cambiare
STRUTTURA = {
    "nome": "Hotel Heubad",
    "sotto": "Hotel con spa, piscine e ristorante, Fiè allo Sciliar",
    "data": "Novembre 2026",
}

# Lettura in superficie: osservazioni da fuori, non una diagnosi. Tre per colonna.
ANALISI = {
    "funziona": [("Una reputazione solida", "4,7 su Google, con oltre 280 recensioni"),
                 ("Ospiti fedeli", "C'è chi torna da dieci anni e lo scrive"),
                 ("Molto da raccontare", "Spa, piscine, cucina e lo Sciliar alle spalle")],
    "crescere": [("Presenza social", "Dal sito non si arriva a nessun profilo"),
                 ("Visibilità", "Chi non vi conosce non ha modo di incontrarvi"),
                 ("Prenotazione diretta", "Spostare prenotazioni dai portali al vostro sito")],
    "andare":   [("Profili vivi tutto l'anno", "In inverno e in estate, non solo quando siete pieni"),
                 ("Davanti a chi sceglie", "Campagne nei mesi in cui si decide dove andare"),
                 ("Più prenotazioni dirette", "Un sito che trasforma le visite in camere vendute")],
}

# ─────────────────────────────────────────────── lo studio
# Il documento e' verticale: si mostrano solo i servizi e i clienti dell'ospitalita'.
# Il resto dello studio (e-commerce, stampa, parrucchieri, ottici...) resta nel
# documento standard, non qui.
STUDIO_FA = [("social", "Social"), ("foto", "Foto"), ("video", "Video"),
             ("adv", "Advertising"), ("siti-web", "Siti web")]

# Solo hotel, ristoranti e affini. Un logo che manca in brand/clienti/ esce come
# monogramma provvisorio, e lo script lo dice a fine resa.
CLIENTI = [("villa-campomaggio", "Hotel Villa Campomaggio"), ("la-gabbia", "Ristorante La Gabbia"),
           ("spiedo-imperiale", "Spiedo Imperiale"), ("aloz", "L'Alóz"),
           ("trattoria-ca-rossi", "Trattoria Ca' Rossi"), ("piadina-baracchina", "La Piadina della Baracchina"),
           ("bocon-divino", "Bocon Divino")]
OLTRE = ("Oltre 50", "attività seguite in tutti i settori, dalla Romagna alla Toscana")

# Campomaggio: proposta di rinnovo 2027 (stagione 2026). La Gabbia: proposta Love Luck.
# L'Aloz: DOCUMENTO UNICO, caso 6. Numeri non ce ne sono, quindi le righe sono fatti
# (cosa era, cosa abbiamo fatto), non risultati. Ed e' stato un avvio una tantum:
# niente che faccia pensare a una gestione continuativa che oggi non c'e'.
CASI = [
    ("villa-campomaggio", "Hotel Villa Campomaggio", "Hotel in Toscana · stagione 2026", [
        ("+1.324", "Nuovi follower Instagram"),
        ("392.000", "Impression Instagram"),
        ("2.741", "Visite al sito prima della riapertura"),
        ("0,15 €", "Costo per visita al sito"),
    ]),
    ("la-gabbia", "La Gabbia Tuscany Lounge", "Ristorante · nuova apertura", [
        ("+1.200.000", "Impression partendo da 0 (8 mesi)"),
        ("+285.000", "Singoli account raggiunti"),
        ("+3.000", "Follower costruiti in una stagione"),
        ("50", "Contenuti professionali pubblicati"),
    ]),
    ("aloz", "L'Alóz", "Bed & breakfast di 3 camere · Lugo (RA)", [
        ("Da zero", "Struttura nuova, nessuna presenza social prima"),
        ("Giugno 2026", "Lancio dei profili, primo mese"),
        ("3 camere", "Anthurium, Begonia, Ciclamino: i pilastri del racconto"),
        ("Avvio completo", "Calendario, copy, shooting, grafica e report di lancio"),
    ]),
]

# ─────────────────────────────────────────────── i tre servizi
SERVIZI = [
    ("social", "Gestione social", "Alex e Riccardo", [
        "8 contenuti al mese, foto, video e grafiche",
        "2 video verticali al mese",
        "Storie, commenti, messaggi e recensioni",
        "Uno shooting a stagione in struttura",
        "Instagram, Facebook e Google Business"]),
    ("adv", "Gestione advertising", "Alessandro", [
        "Campagne su Meta e Google",
        "Pubblico su chi cerca le Dolomiti",
        "Notorietà e prenotazioni, nei mesi giusti",
        "Ottimizzazione continua",
        "Report mensile su costi e risultati"]),
    ("siti-web", "Sviluppo e gestione sito web", "Nadir", [
        "Restyling pensato per il telefono",
        "Prenotazione diretta collegata",
        "Booking e Airbnb con channel manager",
        "Tracciamento GA4 e Pixel di Meta",
        "Online in 4–6 settimane"]),
]

# ─────────────────────────────────────────────── economia
# Sito, portali e tracciamento: listino Nadir, caso B (sito da rifare).
# Social e advertising: adattati da Campomaggio a una struttura sola — DA CONFERMARE.
PREZZI = [
    {"nome": "Gestione social", "spot": True,
     "avvio": "3.500 €", "avvio_nota": "Shooting di avvio e prima libreria di contenuti",
     "poi": "1.400 €", "poi_unita": "/ mese", "poi_nota": "In alta stagione, 8 mesi · 900 €/mese in bassa"},
    {"nome": "Gestione advertising", "spot": False,
     "avvio": "Incluso", "avvio_nota": "Account, pubblici e tracciamento delle campagne",
     "poi": "500 €", "poi_unita": "/ mese", "poi_nota": "Tutto l'anno · budget inserzioni a parte"},
    {"nome": "Sito web e portali", "spot": False,
     "avvio": "3.100 €", "avvio_nota": "Sito con prenotazione 2.200 € · Booking e Airbnb 900 €",
     "poi": "1.140 €", "poi_unita": "/ anno", "poi_nota": "Manutenzione, gestione portali e hosting"},
]

RIEPILOGO = [
    ("Avvio", "Una tantum", "Shooting, sito con prenotazione, portali e tracciamento", "6.600 €", True),
    ("Alta stagione", "8 mesi · dic–mar, giu–set", "Social completo e advertising", "1.900 € / mese", True),
    ("Bassa stagione", "4 mesi · apr–mag, ott–nov", "Presidio social e advertising", "1.400 € / mese", True),
    ("Canoni", "Annuali", "Manutenzione del sito, gestione portali, hosting", "da 1.140 € / anno", False),
]
TOTALE = ("Totale primo anno", "Avvio + 12 mesi di gestione + canoni", "da 28.540 €")
NOTE = ["* Budget inserzioni Meta e Google esterno al preventivo: consigliati 400–600 € al mese.",
        "* Fatture separate per servizio. Ogni servizio si può attivare anche da solo, agli stessi prezzi.",
        "* Esclusi modelli per gli shooting, licenza del motore di prenotazione e commissioni dei portali."]

PASSI = ["Conferma della proposta e accessi",
         "Chiamata di scoperta e impostazione della strategia",
         "Definizione del budget pubblicitario",
         "Shooting di avvio in struttura",
         "Calendario editoriale, campagne e sito online"]
EXTRA = [("Contenuti extra", ["Video istituzionale per sito e campagne",
                              "Shooting dedicato a un'apertura o a un evento",
                              "Più pubblicazioni al mese"]),
         ("Promozione e brand", ["Brochure e PDF di presentazione",
                                 "Grafica per la stampa: menu, materiali in camera",
                                 "CRM ed email agli ospiti passati"])]

CONTATTO = ("riccardo@ydgstudio.com", "+39 346 615 5886")
VALIDITA = "*Proposta valida per 30 giorni"
TOT = 9


# ─────────────────────────────────────────────── impianto grafico
def css():
    facce = "".join(
        f"@font-face{{font-family:'OG';src:url('{U('font', f)}') format('woff2');"
        f"font-weight:{w};font-style:normal;font-display:block}}"
        for f, w in (("OverusedGrotesk-Book.woff2", 400), ("OverusedGrotesk-Medium.woff2", 500),
                     ("OverusedGrotesk-SemiBold.woff2", 600), ("OverusedGrotesk-Bold.woff2", 700)))
    return facce + f"""
*{{margin:0;padding:0;box-sizing:border-box;-webkit-print-color-adjust:exact;print-color-adjust:exact}}
html,body{{font-family:'OG',sans-serif;background:{NERO}}}
.p{{width:1280px;height:720px;position:relative;overflow:hidden;background:{CHIARO};color:{NERO};
   page-break-after:always}}
.p.scura{{background:{NERO};color:#F4F4F4}}
.p.arancio{{background:{ARANCIO};color:{NERO}}}

.testa{{position:absolute;left:80px;right:80px;top:36px;height:24px;display:flex;
       justify-content:space-between;align-items:center}}
.testa img{{height:22px;display:block}}
.doc{{font-size:12.5px;font-weight:400;color:#6E6E6E}}
.p.scura .doc{{color:#BDBDBD}} .p.arancio .doc{{color:{NERO}}}
.pag{{position:absolute;left:80px;bottom:34px;font-size:12px;color:#6E6E6E}}
.pag b{{font-weight:600;color:{NERO}}}
.p.scura .pag{{color:#9A9A9A}} .p.scura .pag b{{color:#F4F4F4}}

.corpo{{position:absolute;left:80px;right:80px;top:112px;bottom:70px;display:flex;flex-direction:column}}
.occhiello{{display:flex;align-items:center;gap:11px;font-size:13px;font-weight:600;
          letter-spacing:.17em;text-transform:uppercase}}
.occhiello::before{{content:"";width:10px;height:10px;background:{ARANCIO}}}
.p.scura .occhiello{{color:{ARANCIO}}} .p.scura .occhiello::before{{display:none}}
h1{{font-size:33px;font-weight:600;letter-spacing:-.015em;line-height:1.12;margin-top:12px}}
.sotto{{font-size:16.5px;font-weight:400;color:#5C5C5C;line-height:1.45;margin-top:10px}}
.sotto b{{font-weight:600;color:{NERO}}}
.p.scura .sotto{{color:#BDBDBD}}

.card{{border-radius:14px;padding:22px 24px;background:{NERO};color:#F4F4F4;position:relative;overflow:hidden}}
.card.barra{{border-top:5px solid {ARANCIO}}}
.card.grigia{{background:{GRIGIO}}}
.card.arancio{{background:{ARANCIO};color:{NERO}}}
.card.bianca{{background:#fff;color:{NERO}}}
.card h3{{font-size:18px;font-weight:600;letter-spacing:-.01em;line-height:1.2}}

ul{{list-style:none}}
li{{font-size:15.5px;font-weight:400;line-height:1.35;padding-left:21px;position:relative;margin-top:11px}}
li::before{{content:"";position:absolute;left:0;top:7px;width:8px;height:8px;border-radius:50%;background:{ARANCIO}}}
.card.arancio li::before{{background:{NERO}}}
ul.largo li{{font-size:17px;line-height:1.35;margin-top:19px;padding-left:23px}}
ul.largo li::before{{top:8px;width:9px;height:9px}}

.label{{font-size:11.5px;font-weight:600;letter-spacing:.16em;text-transform:uppercase}}

/* tabella del riepilogo, come nel documento standard */
table{{width:100%;border-collapse:collapse;margin-top:22px}}
th{{font-size:11.5px;font-weight:600;letter-spacing:.16em;text-transform:uppercase;text-align:left;
   padding:0 22px 11px}}
th.d,td.d{{text-align:right}}
td{{padding:12px 22px;border-bottom:1px solid #DADADA;vertical-align:middle}}
tr.evid td{{background:{EVID}}}
tr.evid td:first-child{{box-shadow:inset 5px 0 0 {ARANCIO}}}
tr.tot td{{border-bottom:0;padding-top:15px}}
.v{{font-size:16.5px;font-weight:600}}
.s{{font-size:12px;color:#6E6E6E;margin-top:2px}}
.c{{font-size:15.5px;color:#4A4A4A}}
.n{{font-size:17px;font-weight:600;white-space:nowrap}}
"""


def testa(tema="chiaro", destra=None):
    logo = "logo-chiaro.png" if tema == "scuro" else "logo-scuro.png"
    d = destra or f"Proposta di collaborazione · {STRUTTURA['nome']}"
    return f'<div class="testa"><img src="{U(logo)}" alt="YDG Studio"><div class="doc">{E(d)}</div></div>'


def pagina(n, corpo, tema="chiaro", occhiello=None, titolo=None, sotto=None):
    cls = {"chiaro": "", "scuro": "scura", "arancio": "arancio"}[tema]
    t = ""
    if occhiello: t += f'<div class="occhiello">{E(occhiello)}</div>'
    if titolo: t += f"<h1>{titolo}</h1>"
    if sotto: t += f'<p class="sotto">{sotto}</p>'
    return (f'<section class="p {cls}">{testa("scuro" if tema == "scuro" else "chiaro")}'
            f'<div class="corpo">{t}{corpo}</div>'
            f'<div class="pag"><b>{n:02d}</b> / {TOT:02d}</div></section>')


def ul(xs):
    return "<ul>" + "".join(f"<li>{E(x)}</li>" for x in xs) + "</ul>"


# ─────────────────────────────────────────────── le pagine
def p01():
    return f"""<section class="p scura" style="background:{NERO} url('{U('copertina.png')}') center/cover">
{testa("scuro", f"{STRUTTURA['data']} · {STRUTTURA['nome']}")}
<div style="position:absolute;left:80px;right:80px;top:226px">
  <div class="label" style="color:{ARANCIO};font-size:14px">Proposta di collaborazione</div>
  <div style="font-size:76px;font-weight:600;letter-spacing:-.03em;line-height:1.08;margin-top:26px">
    Facciamo crescere<br><span style="color:{ARANCIO}">{E(STRUTTURA['nome'])}</span></div>
  <div style="font-size:18px;color:#D9D9D9;margin-top:28px">{E(STRUTTURA['sotto'])}</div>
</div></section>"""


MANCANTI = []

def logo(slug, nome, px):
    """Il logo vero se c'e' in brand/clienti/, altrimenti un monogramma provvisorio."""
    if os.path.exists(os.path.join(BRAND, "clienti", slug + ".png")):
        return f'<img src="{U("clienti", slug + ".png")}" style="width:{px}px;height:{px}px;flex:0 0 auto">'
    if nome not in MANCANTI:
        MANCANTI.append(nome)
    lettere = "".join(w[0] for w in nome.replace("'", " ").split() if w[0].isalpha())[:2].upper()
    return (f'<div style="width:{px}px;height:{px}px;border-radius:50%;background:{CHIARO};color:{NERO};'
            f'display:flex;align-items:center;justify-content:center;flex:0 0 auto;'
            f'font-size:{round(px * .36)}px;font-weight:600;letter-spacing:-.02em">{E(lettere)}</div>')


def p02():
    icone = "".join(
        f'<div style="display:flex;align-items:center;gap:11px">'
        f'<img src="{U("icone", f + ".png")}" style="width:38px;height:38px">'
        f'<span style="font-size:17px;font-weight:600">{E(t)}</span></div>' for f, t in STUDIO_FA)
    carte = "".join(
        f'<div class="card grigia" style="display:flex;flex-direction:column;align-items:center;'
        f'justify-content:center;gap:14px;padding:18px 16px;text-align:center">'
        f'{logo(f, t, 78)}<span style="font-size:16px;font-weight:600;line-height:1.2">{E(t)}</span></div>'
        for f, t in CLIENTI)
    carte += (f'<div class="card arancio" style="display:flex;flex-direction:column;justify-content:center;padding:22px 24px">'
              f'<div style="font-size:40px;font-weight:600;letter-spacing:-.03em;line-height:1">{E(OLTRE[0])}</div>'
              f'<div style="font-size:15px;line-height:1.35;margin-top:10px">{E(OLTRE[1])}</div></div>')
    corpo = f"""
<div style="display:flex;justify-content:space-between;margin-top:26px">{icone}</div>
<div class="label" style="color:{ARANCIO};margin-top:28px">Nell'ospitalità hanno già scelto YDG Studio</div>
<div style="display:grid;grid-template-columns:repeat(4,1fr);grid-auto-rows:1fr;gap:14px;margin-top:16px;flex:1">{carte}</div>"""
    return pagina(2, corpo, "scuro", "Chi siamo",
                  "Comunicazione digitale per hotel e ristoranti.",
                  "Studio con base in Romagna. Social, advertising e sito con un'unica regia, "
                  "shooting in struttura e report trasparenti.")


def p03():
    c = ""
    for slug, nome, sotto, voci in CASI:
        righe = "".join(
            f'<div style="padding:11px 0;border-top:1px solid #3A3A3A">'
            f'<div style="font-size:28px;font-weight:600;letter-spacing:-.02em;color:{ARANCIO};line-height:1.1">{E(v)}</div>'
            f'<div style="font-size:13px;color:#D9D9D9;margin-top:3px">{E(t)}</div></div>' for v, t in voci)
        c += (f'<div class="card" style="padding:22px 26px 12px;display:flex;flex-direction:column">'
              f'<div style="display:flex;align-items:center;gap:13px;margin-bottom:13px">'
              f'{logo(slug, nome, 42)}'
              f'<div><div style="font-size:17px;font-weight:600">{E(nome)}</div>'
              f'<div style="font-size:12.5px;color:#BDBDBD;margin-top:2px">{E(sotto)}</div></div></div>'
              f'{righe}</div>')
    corpo = f'<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:20px;margin-top:26px;flex:1">{c}</div>'
    return pagina(3, corpo, "chiaro", "Casi studio", "Hotel, ristoranti e B&B con cui abbiamo lavorato",
                  "Strutture diverse per dimensione e per fase: una stagione consolidata, una nuova "
                  "apertura, un lancio da zero.")


def p04():
    def col(titolo, voci, cls):
        sec = "rgba(26,26,26,.7)" if cls in ("arancio", "bianca") else "#BDBDBD"
        if cls == "bianca": sec = "#5C5C5C"
        pallino = NERO if cls == "arancio" else ARANCIO
        v = "".join(
            f'<div style="padding:17px 0;border-top:1px solid {"rgba(26,26,26,.16)" if cls else "#333"}">'
            f'<div style="display:flex;align-items:center;gap:11px"><span style="width:9px;height:9px;'
            f'border-radius:50%;background:{pallino};flex:0 0 auto"></span>'
            f'<span style="font-size:19px;font-weight:600;letter-spacing:-.01em">{E(t)}</span></div>'
            f'<div style="font-size:15px;line-height:1.4;color:{sec};margin:6px 0 0 20px">{E(d)}</div></div>'
            for t, d in voci)
        return (f'<div class="card {cls}" style="padding:26px 28px 10px">'
                f'<h3 style="font-size:22px;margin-bottom:16px">{E(titolo)}</h3>{v}</div>')
    corpo = f"""<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:18px;margin-top:26px;flex:1">
  {col("Cosa funziona già", ANALISI['funziona'], "")}
  {col("Dove possiamo crescere", ANALISI['crescere'], "arancio")}
  {col("Dove vogliamo andare", ANALISI['andare'], "bianca")}
</div>"""
    return pagina(4, corpo, "chiaro", "Analisi iniziale", "Da dove partiamo, dove vogliamo andare",
                  "Una fotografia di quello che si vede da fuori. La strategia di dettaglio nasce "
                  "nelle prime settimane, insieme a voi.")


def p05():
    c = "".join(
        f'<div class="card barra" style="padding:28px 28px">'
        f'<div style="display:flex;align-items:center;gap:15px;min-height:90px;padding-bottom:18px;border-bottom:1px solid #333">'
        f'<img src="{U("icone", ic + ".png")}" style="width:52px;height:52px">'
        f'<div><h3 style="font-size:21px">{E(nome)}</h3>'
        f'<div style="font-size:13.5px;color:#BDBDBD;margin-top:3px">{E(chi)}</div></div></div>'
        f'<ul class="largo">' + "".join(f"<li>{E(x)}</li>" for x in voci) + '</ul></div>' for ic, nome, chi, voci in SERVIZI)
    corpo = f'<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:18px;margin-top:26px;flex:1">{c}</div>'
    return pagina(5, corpo, "chiaro", "Il servizio", "Tre servizi, un solo interlocutore",
                  "Insieme lavorano meglio: le campagne spingono su un sito che converte, i contenuti "
                  "danno alle campagne qualcosa da mostrare. Ognuno si attiva anche da solo.")


def p06():
    c = ""
    for v in PREZZI:
        cls = "arancio" if v["spot"] else "grigia"
        sec = "rgba(26,26,26,.72)" if v["spot"] else "#D9D9D9"
        fil = "rgba(26,26,26,.25)" if v["spot"] else "rgba(255,255,255,.18)"
        c += f"""<div class="card {cls}" style="padding:24px 26px;display:flex;flex-direction:column">
  <h3 style="font-size:19px">{E(v['nome'])}</h3>
  <div class="label" style="margin-top:20px;color:{sec}">Avvio</div>
  <div style="font-size:46px;font-weight:600;letter-spacing:-.03em;line-height:1.05;margin-top:6px">{E(v['avvio'])}</div>
  <div style="font-size:13px;line-height:1.4;color:{sec};margin-top:6px">{E(v['avvio_nota'])}</div>
  <div style="height:1px;background:{fil};margin:20px 0 18px"></div>
  <div class="label" style="color:{sec}">Gestione</div>
  <div style="display:flex;align-items:baseline;gap:8px;margin-top:6px">
    <span style="font-size:46px;font-weight:600;letter-spacing:-.03em;line-height:1.05">{E(v['poi'])}</span>
    <span style="font-size:17px">{E(v['poi_unita'])}</span></div>
  <div style="font-size:13px;line-height:1.4;color:{sec};margin-top:6px">{E(v['poi_nota'])}</div>
</div>"""
    corpo = f'<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:18px;margin-top:26px;flex:1">{c}</div>'
    return pagina(6, corpo, "scuro", "La proposta", "Impostazione + gestione, servizio per servizio")


def p07():
    righe = "".join(
        f'<tr class="{"evid" if ev else ""}"><td style="width:250px"><div class="v">{E(q)}</div>'
        f'<div class="s">{E(s)}</div></td><td><div class="c">{E(c)}</div></td>'
        f'<td class="d"><div class="n">{E(n)}</div></td></tr>' for q, s, c, n, ev in RIEPILOGO)
    t, ts, tn = TOTALE
    righe += (f'<tr class="tot"><td><div class="v" style="font-size:19px">{E(t)}</div></td>'
              f'<td><div class="c">{E(ts)}</div></td>'
              f'<td class="d"><div style="font-size:30px;font-weight:600;letter-spacing:-.02em;color:{ARANCIO}">{E(tn)}</div></td></tr>')
    note = "".join(f'<div style="font-size:12px;color:#5C5C5C;line-height:1.6">{E(x)}</div>' for x in NOTE)
    corpo = f"""<table><tr><th>Periodo</th><th>Cosa ottenete</th><th class="d">Investimento</th></tr>{righe}</table>
<div style="margin-top:auto">{note}</div>"""
    return pagina(7, corpo, "chiaro", "Investimento", "Il riepilogo economico",
                  "<b>Avvio + dodici mesi di gestione</b>: il percorso completo per un anno, "
                  "con le due stagioni dell'Alto Adige.")


def p08():
    punti = "".join(
        f'<div><div style="width:17px;height:17px;border-radius:50%;background:{ARANCIO};position:relative;z-index:1"></div>'
        f'<div style="font-size:30px;font-weight:600;margin-top:18px">{i:02d}</div>'
        f'<div style="font-size:15.5px;line-height:1.35;margin-top:8px;color:#3A3A3A">{E(t)}</div></div>'
        for i, t in enumerate(PASSI, 1))
    extra = "".join(
        f'<div style="flex:1"><div style="font-size:16px;font-weight:600;color:{ARANCIO}">{E(t)}</div>{ul(v)}</div>'
        for t, v in EXTRA)
    corpo = f"""<div style="position:relative;margin-top:34px">
  <div style="position:absolute;left:8px;right:0;top:8px;height:1px;background:#CFCFCF"></div>
  <div style="display:grid;grid-template-columns:repeat(5,1fr);gap:26px">{punti}</div>
</div>
<div class="card" style="margin-top:auto;display:flex;gap:56px;padding:22px 30px">
  <div style="width:210px;flex:0 0 auto"><div class="label" style="color:{ARANCIO}">Su richiesta</div>
    <div style="font-size:14px;color:#BDBDBD;line-height:1.45;margin-top:9px">Da aggiungere quando servono, con quotazioni dedicate.</div></div>
  {extra}
</div>"""
    return pagina(8, corpo, "chiaro", "Prossimi passi", "Come partiamo",
                  "<b>Il primo mese è di fondamenta</b>: si studia la struttura, si fotografa, si imposta. "
                  "Dal secondo si pubblica.")


def p09():
    return f"""<section class="p arancio">{testa("chiaro")}
<div style="position:absolute;left:80px;right:80px;top:226px">
  <div class="label" style="font-size:14px">Grazie</div>
  <div style="font-size:64px;font-weight:600;letter-spacing:-.03em;line-height:1.1;margin-top:24px">
    Diamo forma al racconto di<br>{E(STRUTTURA['nome'])}</div>
  <div style="display:flex;gap:44px;margin-top:44px">
    <div><div class="label">Email</div><div style="font-size:19px;font-weight:600;margin-top:8px">{E(CONTATTO[0])}</div></div>
    <div><div class="label">Telefono</div><div style="font-size:19px;font-weight:600;margin-top:8px">{E(CONTATTO[1])}</div></div>
  </div>
  <div style="font-size:12.5px;margin-top:30px">{E(VALIDITA)}</div>
</div></section>"""


PAGINE = [p01, p02, p03, p04, p05, p06, p07, p08, p09]


# ─────────────────────────────────────────────── resa
OUT = os.path.join(HERE, f"Proposta ospitalita - {STRUTTURA['nome']}.pdf")
ANTEPRIME = os.path.join(HERE, "_anteprime_acquisizione")


def documento():
    return ("<!doctype html><html lang='it'><head><meta charset='utf-8'>"
            f"<style>{css()}</style></head><body>"
            + "".join(p() for p in PAGINE) + "</body></html>")


def rendi():
    """HTML sul disco, poi Chromium via Node (rendi.mjs)."""
    import json, subprocess, glob
    for vecchia in glob.glob(os.path.join(ANTEPRIME, "*.png")):
        os.remove(vecchia)
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
        print(f"  ! pagina {t['n']}: {t['h']}px, sfora di {t['h'] - 720}")
    return troppo


if __name__ == "__main__":
    if not os.path.isdir(BRAND):
        sys.exit("manca la cartella brand/ accanto allo script")
    sfori = rendi()
    print(f"✓ {len(PAGINE)} pagine → {OUT}")
    print(f"✓ anteprime → {ANTEPRIME}")
    print(f"✗ pagine che sforano: {len(sfori)}" if sfori else "✓ nessuna pagina sfora")
    if MANCANTI:
        print("! logo provvisorio (monogramma) per: " + ", ".join(MANCANTI)
              + " — mettere il logo vero in brand/clienti/ e rigenerare")
