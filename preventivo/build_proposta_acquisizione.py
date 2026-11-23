"""Proposta di acquisizione · verticale OSPITALITA, brand YDG Studio.

Diversa dalla proposta di rinnovo di Campomaggio: li' si parlava a un cliente che
ci conosce da due stagioni, qui si parla a una struttura che non ci ha mai visti.
Quindi i risultati di Campomaggio diventano la prova, e la fotografia della
struttura diventa l'apertura.

Tre servizi in un documento solo, ognuno con la sua pagina e il suo prezzo:
  - social organico e produzione contenuti   (Alex, Riccardo)
  - advertising                              (Alessandro)
  - sito web, portali e tracciamento         (Nadir)

Esempio compilato su Hotel Heubad (Fie allo Sciliar), presa dalla lista dell'hub.
Per un'altra struttura si cambiano i dizionari STRUTTURA e FOTOGRAFIA.

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
GREY, LIGHT, LINE = "#a9a9a6", "#F2F2F2", "#2B2B2B"

# ─────────────────────────────────────────────── la struttura, da cambiare
STRUTTURA = {
    "nome": "Hotel Heubad",
    "dove": "Fiè allo Sciliar (BZ)",
    "riga1": "Social organico, advertising e sito web in un piano solo.",
    "riga2": "Lavorate bene. Chi non vi conosce ancora non ha modo di saperlo.",
    "data": "Novembre 2026",
}

# Fotografia: SOLO dati pubblici misurati, con la data. Niente stime.
FOTOGRAFIA = {
    "rilevato": "Google Places, 16 ottobre 2026",
    "voto": "4,7", "recensioni": "282", "km": "4",
    "sito": "hotelheubad.com",
    "sommario": "Hotel in stile sobrio con ristorante, saune e piscine coperta e scoperta.",
    "citazione": "«Sono oltre 10 anni che passiamo le vacanze in questo albergo e per noi "
                 "è ormai una seconda casa.»",
    "citazione_fonte": "Recensione Google, 5 stelle, 4 mesi fa",
}

# ─────────────────────────────────────────────── i numeri della prova (Campomaggio)
# Dalla Proposta di rinnovo 2027 e dal consuntivo 2026. Nessuno inventato.
PROVA_ORGANICO = [
    ("+1.324", "nuovi follower Instagram in una stagione"),
    ("392.075", "impression organiche"),
    ("43.429", "persone raggiunte"),
    ("2,89%", "engagement rate"),
]
PROVA_ADV = [
    ("2.741", "visite al sito prima della riapertura"),
    ("€ 0,15", "costo per visita al sito"),
    ("+1.647", "nuovi follower da advertising"),
    ("1.126.165", "impression a pagamento"),
]
PROVA_PRODUZIONE = "78 contenuti, 751 storie, 16 video verticali e 3 shooting in una stagione."

# ─────────────────────────────────────────────── economia
# Sito, portali e tracciamento: listino Nadir, caso B (sito da rifare).
# Social e ADV: adattati da Campomaggio a una struttura sola — DA CONFERMARE.
SETUP = [
    ("Shooting di avvio e prima libreria contenuti", "Foto e video della struttura, delle camere, della spa e del ristorante", "3.500 €"),
    ("Sito con prenotazione diretta", "Restyling completo, versione mobile, collegamento al motore di prenotazione", "2.200 €"),
    ("Booking e Airbnb", "Schede, tariffe, disponibilità e channel manager", "900 €"),
    ("Tracciamento", "GA4, Tag Manager, Pixel di Meta, conteggio richieste e prenotazioni", "incluso nel sito"),
]
SETUP_TOT = "6.600 €"

GESTIONE = [
    ("Social organico · alta stagione", "Dicembre–marzo e giugno–settembre · 8 mesi",
     "8 contenuti al mese, 2 video, storie, community e recensioni", "1.400 €/mese"),
    ("Social organico · bassa stagione", "Aprile–maggio e ottobre–novembre · 4 mesi",
     "Presidio dei profili, contenuti per le campagne, community", "900 €/mese"),
    ("Advertising", "Tutto l'anno · 12 mesi",
     "Campagne su Meta e Google, ottimizzazione e report", "500 €/mese"),
]
GESTIONE_TOT = "20.800 €"

CANONI = [
    ("Manutenzione del sito", "Sicurezza, backup e aggiornamenti", "500 €/anno"),
    ("Gestione Booking e Airbnb", "Monitoraggio mensile, report trimestrale", "da 500 a 800 €/anno"),
    ("Hosting", "SiteGround, fatturato a parte", "140 €/anno"),
]
CANONI_TOT = "da 1.140 €/anno"
TOTALE = "da 28.540 €"
BUDGET_ADV = "da 400 a 600 €/mese"

CONTATTI = [
    ("Riccardo Milonean", "riccardo@ydgstudio.com", "+39 346 615 5886"),
    ("Alessandro Eusebio", "tea.alessandroeusebio@gmail.com", "+39 349 974 5528"),
]

TOT_PAGINE = 15

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
   page-break-after:always;display:flex;flex-direction:column}}
.p.scura{{background:{INK};color:#fff}}
.p.nera{{background:{DEEP};color:#fff}}
.corpo{{flex:1;padding:64px 64px 0;display:flex;flex-direction:column;min-height:0}}
.pie{{padding:0 64px 26px;display:flex;justify-content:space-between;
     font-size:11px;letter-spacing:.075em;text-transform:uppercase;color:#9a9a97}}
.p.scura .pie,.p.nera .pie{{color:#6f6f6c}}

.occhiello{{font-size:11.5px;font-weight:600;letter-spacing:.075em;text-transform:uppercase;
          color:{ORANGE};display:flex;justify-content:space-between}}
.occhiello span{{color:#9a9a97;font-weight:400}}
h1{{font-size:46px;font-weight:600;letter-spacing:-.04em;line-height:1.03;margin:14px 0 0}}
h1 .coda{{color:{ORANGE}}}
.sotto{{font-size:16px;line-height:1.5;color:#5a5a57;margin-top:14px;max-width:62ch}}
.p.scura .sotto,.p.nera .sotto{{color:{GREY}}}

/* Le fasce di dati restano compatte; i blocchi di contenuto riempiono la pagina,
   altrimenti resta un buco in fondo che sembra una dimenticanza. */
.griglia{{display:grid;gap:18px;margin:40px 0 34px;flex:0 0 auto}}
.griglia.cresci{{flex:1;align-items:stretch}}
.card.cresci{{flex:1;display:flex;flex-direction:column;justify-content:center}}
.g2{{grid-template-columns:1fr 1fr}} .g3{{grid-template-columns:repeat(3,1fr)}}
.g4{{grid-template-columns:repeat(4,1fr)}} .g5{{grid-template-columns:repeat(5,1fr)}}
.card{{background:#fff;border-radius:24px;padding:26px 24px}}
.p.scura .card,.p.nera .card{{background:#232323}}
.card.spot{{background:{DEEP};color:#fff}}
.card .n{{font-size:13px;font-weight:600;color:{ORANGE};letter-spacing:.04em}}
.card h3{{font-size:19px;font-weight:600;letter-spacing:-.02em;margin:10px 0 8px;line-height:1.2}}
.card p{{font-size:13.5px;line-height:1.5;color:#5a5a57}}
.card.spot p,.p.scura .card p,.p.nera .card p{{color:{GREY}}}

.dato{{font-size:38px;font-weight:600;letter-spacing:-.03em;color:{ORANGE};line-height:1}}
.dato.bianco{{color:#fff}} .dato.scuro{{color:{INK}}}
.etichetta{{font-size:12.5px;line-height:1.4;color:#5a5a57;margin-top:9px}}
.p.scura .etichetta,.p.nera .etichetta{{color:{GREY}}}

ul{{list-style:none}} li{{font-size:14px;line-height:1.55;color:#5a5a57;
   padding-left:17px;position:relative;margin-bottom:9px}}
li::before{{content:"";position:absolute;left:0;top:8px;width:6px;height:6px;background:{ORANGE}}}
.p.scura li,.p.nera li,.card.spot li{{color:{GREY}}}

table{{width:100%;border-collapse:collapse;margin-top:26px}}
th{{font-size:11px;font-weight:600;letter-spacing:.075em;text-transform:uppercase;color:#9a9a97;
   text-align:left;padding-bottom:12px;border-bottom:1px solid #DEDEDA}}
th.d,td.d{{text-align:right}}
td{{padding:17px 0;border-bottom:1px solid #E6E6E2;vertical-align:top}}
.voce{{font-size:17px;font-weight:600;letter-spacing:-.02em}}
.nota{{font-size:12.5px;color:#7a7a77;margin-top:5px;line-height:1.45}}
.quando{{font-size:12.5px;color:#7a7a77;white-space:nowrap}}
.cifra{{font-size:23px;font-weight:600;letter-spacing:-.025em;white-space:nowrap}}

.fascia{{background:{DEEP};color:#fff;border-radius:24px;padding:26px 34px;
       display:flex;align-items:center;justify-content:space-between;margin-top:22px}}
.fascia .t{{font-size:18px;font-weight:600;letter-spacing:-.02em}}
.fascia .t small{{display:block;font-size:12.5px;font-weight:400;color:{GREY};margin-top:5px;letter-spacing:0}}
.fascia .c{{font-size:52px;font-weight:600;color:{ORANGE};letter-spacing:-.035em}}

.logo{{font-size:30px;font-weight:700;letter-spacing:-.045em}}
.logo b{{color:{ORANGE};font-weight:700}} .logo span{{font-weight:400}}
.cop{{display:grid;grid-template-columns:1fr 1fr;height:100%}}
.cop .sx{{padding:64px;display:flex;flex-direction:column;justify-content:space-between}}
.cop .dx{{background:linear-gradient(145deg,#2a2a2a,{DEEP});position:relative;overflow:hidden}}
.alone{{position:absolute;width:760px;height:760px;right:-230px;top:-150px;border-radius:50%;
      background:radial-gradient(circle,rgba(255,121,0,.42),rgba(255,121,0,0) 66%)}}
.cop h1{{font-size:66px;line-height:1.0}}
.riga{{width:76px;height:3px;background:{ORANGE};margin:26px 0 18px}}
.meta{{font-size:13.5px;color:{GREY};line-height:1.6}}
.meta b{{color:#fff;font-weight:600;display:block;margin-bottom:3px}}
"""

def pagina(corpo, cls="", n=None, occhiello=None, titolo=None, sotto=None):
    testa = ""
    if occhiello:
        testa += f'<div class="occhiello">{occhiello[0]}<span>{occhiello[1]}</span></div>'
    if titolo:
        testa += f"<h1>{titolo}</h1>"
    if sotto:
        testa += f'<p class="sotto">{sotto}</p>'
    pie = ""
    if n:
        pie = (f'<div class="pie"><div>YDG Studio / Proposta di collaborazione · '
               f'{E(STRUTTURA["nome"])}</div><div>P:{n:02d}</div></div>')
    return f'<section class="p {cls}"><div class="corpo">{testa}{corpo}</div>{pie}</section>'

def dati(voci, scuro=False):
    c = "dato bianco" if scuro else "dato"
    return "".join(f'<div class="card"><div class="{c}">{E(v)}</div>'
                   f'<div class="etichetta">{E(t)}</div></div>' for v, t in voci)

def ul(xs):
    return "<ul>" + "".join(f"<li>{x}</li>" for x in xs) + "</ul>"

# ─────────────────────────────────────────────── le pagine
def p01():
    return f"""<section class="p nera"><div class="cop">
<div class="sx">
  <div class="logo"><b>YDG</b><span>STUDIO</span></div>
  <div>
    <h1>Tre servizi.<br><span class="coda">Una regia sola.</span></h1>
    <div class="riga"></div>
    <p class="sotto" style="margin:0">{E(STRUTTURA['riga1'])}<br>{E(STRUTTURA['riga2'])}</p>
  </div>
  <div class="meta"><b>Proposta di collaborazione · {E(STRUTTURA['nome'])}</b>
    {E(STRUTTURA['dove'])} · {E(STRUTTURA['data'])}</div>
</div>
<div class="dx"><div class="alone"></div></div></div></section>"""

def p02():
    f = FOTOGRAFIA
    corpo = f"""<div class="griglia g4">
  <div class="card"><div class="dato">{f['voto']}</div><div class="etichetta">voto medio su Google</div></div>
  <div class="card"><div class="dato">{f['recensioni']}</div><div class="etichetta">recensioni, quasi tutte positive</div></div>
  <div class="card"><div class="dato">0</div><div class="etichetta">profili social raggiungibili dal sito</div></div>
  <div class="card spot"><div class="dato">{f['km']} km</div><div class="etichetta">dall'Alpe di Siusi</div></div>
</div>
<div class="card cresci" style="margin-bottom:34px;display:flex;gap:34px;align-items:center;flex-direction:row">
  <div style="flex:1"><p style="font-size:19px;line-height:1.45;letter-spacing:-.015em">{E(f['citazione'])}</p>
    <p class="nota" style="margin-top:11px">{E(f['citazione_fonte'])}</p></div>
  <div style="width:1px;height:66px;background:#E0E0DC"></div>
  <div style="width:290px"><p class="nota" style="margin:0">Come vi descrive Google oggi</p>
    <p style="font-size:13.5px;line-height:1.5;color:#5a5a57;margin-top:7px">{E(f['sommario'])}</p></div>
</div>"""
    return pagina(corpo, n=2, occhiello=("01 · Da dove partite", f"Rilevato da {f['rilevato']}"),
                  titolo='La reputazione c\'è. <span class="coda">La presenza no.</span>',
                  sotto="Questi sono dati pubblici, misurati dall'esterno senza chiedervi niente. "
                        "Il quadro completo lo costruiamo insieme alla prima chiamata.")

def p03():
    corpo = f"""<div class="griglia g3 cresci">
  <div class="card"><div class="n">01</div><h3>Chi vi conosce già torna</h3>
    <p>Le recensioni parlano di clienti che tornano da dieci anni. È la prova che
       l'esperienza funziona: il problema non è il prodotto.</p></div>
  <div class="card"><div class="n">02</div><h3>Chi non vi conosce non vi trova</h3>
    <p>Dal vostro sito non si arriva a nessun profilo social. Chi sta scegliendo dove
       andare cerca immagini recenti, e non ne trova.</p></div>
  <div class="card"><div class="n">03</div><h3>Si decide mesi prima</h3>
    <p>L'inverno e l'estate in Alto Adige si prenotano con largo anticipo. Nei mesi in
       cui si decide, oggi, non siete nella conversazione.</p></div>
</div>"""
    return pagina(corpo, n=3, occhiello=("01 · Da dove partite", "Il nodo"),
                  titolo='Il passaparola funziona. <span class="coda">Ma si ferma a chi c\'è già stato.</span>',
                  sotto="Tre cose che abbiamo notato guardandovi da fuori, come farebbe un ospite nuovo.")

def p04():
    corpo = f"""<div class="griglia g4">{dati(PROVA_ORGANICO, True)}</div>
<div class="card spot cresci" style="margin-bottom:34px;display:flex;justify-content:space-between;align-items:center;flex-direction:row">
  <div><h3 style="margin:0">La produzione dietro quei numeri</h3>
    <p style="margin-top:7px">{E(PROVA_PRODUZIONE)}</p></div>
  <div class="dato" style="font-size:30px">2 brand<br><span style="font-size:13px;color:#a9a9a6;font-weight:400">seguiti insieme</span></div>
</div>"""
    return pagina(corpo, "scura", n=4, occhiello=("02 · Che cosa sappiamo fare", "Hotel Villa Campomaggio · stagione 2026"),
                  titolo='Non è una previsione. <span class="coda">È quello che abbiamo fatto.</span>',
                  sotto="Hotel e ristorante nel Chianti, seguiti da due stagioni su contenuti organici, "
                        "advertising e produzione. I numeri sono i loro, verificabili.")

def p05():
    corpo = f"""<div class="griglia g4">{dati(PROVA_ADV, True)}</div>
<div class="card spot cresci" style="margin-bottom:34px">
  <h3 style="margin:0">Il punto che conta</h3>
  <p style="margin-top:7px">L'hotel era chiuso. Le campagne hanno portato 2.741 visite al sito
     <b style="color:#fff">prima</b> della riapertura, a 15 centesimi l'una, lavorando sui mercati
     esteri che prenotano con mesi di anticipo. È lo stesso meccanismo che serve a voi.</p>
</div>"""
    return pagina(corpo, "scura", n=5, occhiello=("02 · Che cosa sappiamo fare", "Meta Ads · 25 febbraio – 31 ottobre 2026"),
                  titolo='L\'advertising, <span class="coda">in cifre.</span>',
                  sotto="Spesa pubblicitaria del cliente nell'anno: 2.903 €. Questo è il ritorno.")

def p06():
    corpo = """<div class="griglia g3 cresci">
  <div class="card"><div class="n">01</div><h3>Social organico</h3>
    <p>Contenuti, shooting, profili, community. Costruisce l'immagine e la mantiene viva
       tutto l'anno. <b>Alex e Riccardo.</b></p></div>
  <div class="card"><div class="n">02</div><h3>Advertising</h3>
    <p>Campagne su Meta e Google verso chi sta scegliendo dove andare, nei mesi giusti.
       <b>Alessandro.</b></p></div>
  <div class="card"><div class="n">03</div><h3>Sito, portali, dati</h3>
    <p>Il sito che riceve il traffico, Booking e Airbnb allineati, il tracciamento che
       dice che cosa ha funzionato. <b>Nadir.</b></p></div>
</div>"""
    return pagina(corpo, n=6, occhiello=("03 · I tre servizi", "Una regia sola"),
                  titolo='Tre fronti, <span class="coda">un solo interlocutore.</span>',
                  sotto="Si possono prendere anche separati. Insieme lavorano meglio: le campagne "
                        "spingono su un sito che converte, i contenuti danno alle campagne qualcosa da mostrare.")

def p07():
    corpo = f"""<div class="griglia g2 cresci">
  <div class="card"><h3 style="margin-top:0">Ogni mese ricevete</h3>
    {ul(["8 contenuti in alta stagione, foto e video",
         "2 video verticali al mese",
         "Storie, commenti e messaggi presidiati",
         "Gestione delle recensioni e della community",
         "Calendario editoriale condiviso in anticipo"])}</div>
  <div class="card"><h3 style="margin-top:0">Nell'anno</h3>
    {ul(["Shooting di avvio: struttura, camere, spa, ristorante",
         "Uno shooting a stagione, per seguire la montagna che cambia",
         "Instagram, Facebook e Google Business Profile",
         "Profilo TikTok se decidiamo che ha senso",
         "Report ogni tre mesi sugli stessi indicatori"])}</div>
</div>"""
    return pagina(corpo, n=7, occhiello=("03 · I tre servizi", "01 · Social organico"),
                  titolo='Qualcosa da guardare, <span class="coda">tutto l\'anno.</span>',
                  sotto="In alta stagione si racconta la struttura piena. In bassa si costruisce la "
                        "domanda per quella dopo: i profili restano vivi mentre la gente decide.")

def p08():
    corpo = f"""<div class="griglia g2 cresci">
  <div class="card"><h3 style="margin-top:0">Che cosa facciamo</h3>
    {ul(["Campagne su Meta e Google verso i mercati che vi interessano",
         "Pubblico costruito su chi cerca una vacanza in Dolomiti",
         "Campagne di notorietà e campagne che portano prenotazioni",
         "Ottimizzazione continua, non una tantum",
         "Report mensile: costo per visita, costo per contatto, clic al sito"])}</div>
  <div class="card spot"><h3 style="margin-top:0">Due cose da chiarire subito</h3>
    {ul(["Il budget pubblicitario non è compreso nel compenso: lo versate "
         "direttamente a Meta e Google, e resta vostro",
         f"Budget consigliato per una struttura come la vostra: {BUDGET_ADV}",
         "Partiamo dai mesi in cui si decide, non da quelli in cui siete già pieni"])}</div>
</div>"""
    return pagina(corpo, n=8, occhiello=("03 · I tre servizi", "02 · Advertising"),
                  titolo='Davanti a chi sta <span class="coda">ancora scegliendo.</span>',
                  sotto="L'organico parla a chi vi ha già trovati. L'advertising vi mette davanti a "
                        "chi non sa che esistete, mentre sta decidendo dove andare.")

def p09():
    corpo = f"""<div class="griglia g2 cresci">
  <div class="card"><h3 style="margin-top:0">Il sito</h3>
    {ul(["Restyling completo, pensato prima per il telefono",
         "Motore di prenotazione collegato: si prenota da voi, non solo dai portali",
         "Pronto in 4–6 settimane dalla conferma",
         "Tracciamento incluso: GA4, Tag Manager, Pixel di Meta",
         "Manutenzione annuale: sicurezza, backup, aggiornamenti"])}</div>
  <div class="card"><h3 style="margin-top:0">I portali</h3>
    {ul(["Booking e Airbnb: schede, tariffe, disponibilità",
         "Channel manager collegato, niente doppie prenotazioni",
         "Attivazione in 2–3 settimane, dipende dalle verifiche delle piattaforme",
         "Monitoraggio mensile, report trimestrale",
         "Commissioni e abbonamenti dei portali restano a vostro carico"])}</div>
</div>"""
    return pagina(corpo, n=9, occhiello=("03 · I tre servizi", "03 · Sito, portali, dati"),
                  titolo='Il posto dove <span class="coda">atterra tutto il resto.</span>',
                  sotto="Contenuti e campagne portano persone da qualche parte. Se quel posto non "
                        "converte, il lavoro di prima si disperde.")

def p10():
    corpo = """<div class="griglia g5 cresci" style="gap:14px">
  <div class="card"><div class="n">01</div><h3>Chiamata</h3><p>Un'ora: la struttura, la stagione, i numeri che avete già.</p></div>
  <div class="card"><div class="n">02</div><h3>Accessi</h3><p>Profili, sito, portali, analytics. E le domande al titolare.</p></div>
  <div class="card"><div class="n">03</div><h3>Shooting</h3><p>Due giorni in struttura: camere, spa, ristorante, esterni.</p></div>
  <div class="card"><div class="n">04</div><h3>Strategia</h3><p>Piano editoriale, campagne, sito. Presentati e approvati.</p></div>
  <div class="card spot"><div class="n">05</div><h3>Si parte</h3><p>Dal secondo mese: pubblicazioni, campagne, sito online.</p></div>
</div>"""
    return pagina(corpo, n=10, occhiello=("04 · Come lavoriamo", "I primi due mesi"),
                  titolo='Il primo mese <span class="coda">non si pubblica niente.</span>',
                  sotto="Si costruiscono le fondamenta: capire la struttura, fotografarla, decidere "
                        "che cosa raccontare. Chi parte a pubblicare il primo giorno sta improvvisando.")

def p11():
    mesi = [("Dic","a"),("Gen","a"),("Feb","a"),("Mar","a"),("Apr","b"),("Mag","b"),
            ("Giu","a"),("Lug","a"),("Ago","a"),("Set","a"),("Ott","b"),("Nov","b")]
    barre = "".join(
        f'<div style="flex:1;text-align:center"><div style="height:34px;border-radius:9px;'
        f'background:{ORANGE if t=="a" else "#E2E2DE"}"></div>'
        f'<div style="font-size:11.5px;color:#7a7a77;margin-top:8px">{m}</div></div>'
        for m, t in mesi)
    corpo = f"""<div class="griglia g2 cresci">
  <div class="card"><h3 style="margin-top:0">Alta stagione · 8 mesi</h3>
    <p>Dicembre–marzo e giugno–settembre. Gestione piena: 8 contenuti al mese, 2 video,
       storie, community, campagne attive su entrambi i fronti.</p></div>
  <div class="card"><h3 style="margin-top:0">Bassa stagione · 4 mesi</h3>
    <p>Aprile–maggio e ottobre–novembre. Presidio dei profili e campagne che costruiscono
       la domanda per la stagione dopo. Non è un periodo morto: è quello in cui si decide.</p></div>
</div>
<div style="display:flex;gap:9px;margin:0 0 34px">{barre}</div>"""
    return pagina(corpo, n=11, occhiello=("04 · Come lavoriamo", "Il calendario"),
                  titolo='Due stagioni, <span class="coda">non una.</span>',
                  sotto="L'Alto Adige lavora d'inverno e d'estate. Il piano segue quel ritmo, "
                        "invece di spalmare lo stesso sforzo su dodici mesi uguali.")

def p12():
    righe = "".join(f"""<tr><td><div class="voce">{E(v)}</div><div class="nota">{E(d)}</div></td>
      <td class="d"><div class="cifra">{E(c)}</div></td></tr>""" for v, d, c in SETUP)
    corpo = f"""<table><tr><th>Avvio · una tantum</th><th class="d">Investimento</th></tr>{righe}</table>
<div class="fascia"><div class="t">Totale di avvio<small>Si salda alla conferma e all'avvio del lavoro</small></div>
  <div class="c">{E(SETUP_TOT)}</div></div>"""
    return pagina(corpo, n=12, occhiello=("05 · Proposta economica", "Servizio per servizio"),
                  titolo='Quello che si fa <span class="coda">una volta sola.</span>')

def p13():
    righe = "".join(f"""<tr><td><div class="voce">{E(v)}</div><div class="nota">{E(d)}</div></td>
      <td><div class="quando">{E(q)}</div></td>
      <td class="d"><div class="cifra">{E(c)}</div></td></tr>""" for v, q, d, c in GESTIONE)
    canoni = " · ".join(f"{v} {c}" for v, _, c in CANONI)
    corpo = f"""<table><tr><th>Gestione</th><th>Periodo</th><th class="d">Investimento</th></tr>{righe}</table>
<div class="card" style="margin-top:18px;display:flex;justify-content:space-between;align-items:center;padding:18px 24px">
  <div><div class="nota" style="margin:0;font-weight:600;color:#5a5a57">Canoni annuali</div>
    <div class="nota" style="margin-top:4px">{E(canoni)}</div></div>
  <div class="cifra" style="font-size:19px">{E(CANONI_TOT)}</div></div>
<div class="fascia" style="margin-top:14px"><div class="t">Gestione nel primo anno<small>Budget pubblicitario escluso, versato da voi direttamente alle piattaforme</small></div>
  <div class="c">{E(GESTIONE_TOT)}</div></div>"""
    return pagina(corpo, n=13, occhiello=("05 · Proposta economica", "Ricorrente"),
                  titolo='Quello che si fa <span class="coda">ogni mese.</span>')

def p14():
    corpo = f"""<div class="fascia" style="margin-top:8px;padding:34px"><div class="t" style="font-size:22px">Totale primo anno
  <small>Avvio {E(SETUP_TOT)} · gestione {E(GESTIONE_TOT)} · canoni {E(CANONI_TOT)}</small></div>
  <div class="c" style="font-size:62px">{E(TOTALE)}</div></div>
<div class="griglia g3 cresci" style="margin-top:26px">
  <div class="card"><h3 style="margin-top:0">Budget pubblicitario</h3>
    <p>{E(BUDGET_ADV)}, versati direttamente a Meta e Google. Non passano da noi e
       restano sotto il vostro controllo.</p></div>
  <div class="card"><h3 style="margin-top:0">Come si fattura</h3>
    <p>Fatture separate per servizio: social e produzione, advertising, sito e portali.
       L'avvio alla conferma, la gestione mensile.</p></div>
  <div class="card"><h3 style="margin-top:0">Che cosa non è compreso</h3>
    <p>Modelli per gli shooting, licenza del motore di prenotazione, commissioni dei
       portali, trasferte a rimborso documentato.</p></div>
</div>"""
    return pagina(corpo, n=14, occhiello=("05 · Proposta economica", "Il totale"),
                  titolo='In chiaro, <span class="coda">senza sorprese.</span>',
                  sotto="Ogni servizio si può prendere da solo. Questo è il quadro completo.")

def p15():
    c = "".join(f"""<div><div style="height:1px;background:{LINE};margin-bottom:17px"></div>
      <div style="font-size:17px;font-weight:600;letter-spacing:-.02em">{E(n)}</div>
      <div style="font-size:13.5px;color:{GREY};margin-top:7px;line-height:1.6">{E(m)}<br>{E(t)}</div>
      </div>""" for n, m, t in CONTATTI)
    return f"""<section class="p nera"><div class="cop">
<div class="sx">
  <div class="logo"><b>YDG</b><span>STUDIO</span></div>
  <div><h1 style="font-size:62px">Parliamone.</h1>
    <p class="sotto" style="max-width:46ch">Se anche solo una delle tre parti vi interessa,
       partiamo da quella. La prima chiamata è un'ora e non costa niente.</p></div>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:34px">{c}</div>
</div>
<div class="dx"><div class="alone"></div></div></div></section>"""

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
    if sfori:
        print(f"✗ {len(sfori)} pagine sforano: vanno accorciate prima di mandarla.")
    else:
        print("✓ nessuna pagina sfora il formato")
