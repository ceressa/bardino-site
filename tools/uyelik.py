# -*- coding: utf-8 -*-
"""Bardino uyelik metinlerini bardino.app/uyelik/ altina yazar.

    python tools/uyelik.py                     uyelik/kosullar.html, uyelik/aydinlatma.html
    python tools/uyelik.py --onizleme          taslagi kapilari atlayarak uyelik-onizleme/'ye
                                               yazar (git disi, noindex; ayni derinlik, CSS calisir)

Kaynak bardino reposundaki docs/KOSULLAR.md ve docs/AYDINLATMA.md (varsayilan
yer: bu reponun yanindaki ../../mobile/bardino; --docs ile degisir). Elle HTML
duzeltme yok: metin degisirse md degisir, bu betik yeniden kosar.

Uc oyun bu iki adresi uyelik kartindan aciyor (BardinoConfig.kosullarUrl,
aydinlatmaUrl) ve merkez `ayarlar.js ac` bu sayfalar yayinda degilse acmiyor.

Yayin kapilari; biri tutmazsa hicbir sey yazilmaz:
- TASLAK / DRAFT notu kalmamali.
- Doldurulmamis koseli parantez kalmamali ([unvan], [adres] ...). Markdown
  baglantisi [ad](adres) sayilmaz.
- Iki metin de ayni surumu soylemeli ("Surum: v1" / "Version: v1"); merkez
  sayfada bu surumu ariyor.
"Hukuki gozden gecirme icin notlar" bolumu avukata yazilmis ic nottur,
yayinlanmaz.
"""
import argparse
import html
import os
import re
import sys

try:
    import markdown
except ImportError:
    sys.exit("markdown paketi gerekli: python -m pip install markdown")

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SAYFALAR = [
    {
        "md": "KOSULLAR.md", "cikti": "kosullar.html", "yol": "kosullar",
        "baslik_en": "Bardino Membership Terms",
        "aciklama": "Decimo, Colmo ve Palmo'daki ücretsiz Bardino üyeliğinin koşulları.",
    },
    {
        "md": "AYDINLATMA.md", "cikti": "aydinlatma.html", "yol": "aydinlatma",
        "baslik_en": "Bardino Membership: Personal Data Protection Notice",
        "aciklama": "Bardino üyeliğinde işlenen kişisel veriler hakkında KVKK aydınlatma metni.",
    },
]

NOT_BASLIGI = re.compile(r"\n---\n+## Hukuki gözden geçirme için notlar\n.*", re.S)
TASLAK = re.compile(r"\b(TASLAK|DRAFT)\b")
BOS_YER = re.compile(r"\[[^\]\n]*\](?!\()")
SURUM_TR = re.compile(r"Sürüm:\s*(v\d+)")
SURUM_EN = re.compile(r"Version:\s*(v\d+)")


def bol(metin):
    """TR ve EN yarilar; aralarinda iki yatay cizgi var."""
    parca = re.split(r"\n---\n---\n", metin)
    if len(parca) != 2:
        raise ValueError("TR/EN ayiraci (---/---) bulunamadi")
    tr, en = parca
    return NOT_BASLIGI.sub("\n", tr).rstrip() + "\n", en.strip() + "\n"


def denetle(ad, tr, en):
    hatalar = []
    for dil, m in (("TR", tr), ("EN", en)):
        if TASLAK.search(m):
            hatalar.append("%s %s: taslak notu duruyor" % (ad, dil))
        for b in BOS_YER.findall(m):
            hatalar.append("%s %s: doldurulmamis yer %s" % (ad, dil, b))
    s_tr, s_en = SURUM_TR.search(tr), SURUM_EN.search(en)
    if not s_tr or not s_en:
        hatalar.append("%s: surum satiri yok (Sürüm: vN / Version: vN)" % ad)
    elif s_tr.group(1) != s_en.group(1):
        hatalar.append("%s: TR %s, EN %s" % (ad, s_tr.group(1), s_en.group(1)))
    return hatalar, (s_tr.group(1) if s_tr else None)


def html_yap(m, en):
    # Ic baglantilar: md dosya adlari yayindaki adrese doner.
    for s in SAYFALAR:
        m = m.replace("](%s)" % s["md"], "](%s%s)" % (s["yol"], "#en" if en else ""))
    m = m.replace("İngilizce metin aşağıda. / English version below.",
                  "[English version below](#en)")
    # KVKK m.11 haklari "a) ..." satirlari: alt alta kalsin diye listeye.
    m = re.sub(r"(?m)^([a-zçğ]\) )", r"- \1", m)
    govde = markdown.markdown(m, extensions=["tables"], output_format="html")
    return govde.replace("<table>", '<div class="doc-table"><table>').replace("</table>", "</table></div>")


def sayfa(s, tr, en, surum, onizleme):
    baslik = re.search(r"^# (.+)$", tr, re.M).group(1)
    url = "https://bardino.app/uyelik/" + s["yol"]
    robots = '<meta name="robots" content="noindex">\n' if onizleme else ""
    return """<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{baslik} - Bardino</title>
<meta name="description" content="{aciklama}">
{robots}<link rel="canonical" href="{url}">
<meta name="theme-color" content="#FDF6F0" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#15132A" media="(prefers-color-scheme: dark)">
<link rel="icon" href="../favicon-32.png" sizes="32x32" type="image/png">
<link rel="icon" href="../favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="../assets/site.css">
</head>
<body class="doc-page">
<!-- tools/uyelik.py uretti, kaynak bardino/docs/{md} ({surum}). Elle duzenleme. -->
<header class="site-head">
  <div class="wrap">
    <a class="doc-home" href="../tr/" aria-label="Bardino ana sayfa"><img src="../assets/bardino-mark.svg" width="38" height="38" alt=""><span>Bardino</span></a>
    <nav class="site-nav" aria-label="Dil">
      <div class="lang" role="group" aria-label="Dil / Language">
        <a href="#tr" hreflang="tr" lang="tr">Türkçe</a>
        <a href="#en" hreflang="en" lang="en">English</a>
      </div>
    </nav>
  </div>
</header>
<main id="main" class="wrap doc">
<article id="tr" lang="tr">
{tr}
</article>
<article id="en" lang="en" aria-label="{baslik_en}">
{en}
</article>
</main>
<footer class="site-foot">
  <div class="wrap">
    <p class="fine">&copy; 2026 Bardino Technology &middot; <a href="mailto:info@bardino.app">info@bardino.app</a></p>
  </div>
</footer>
</body>
</html>
""".format(baslik=html.escape(baslik), aciklama=html.escape(s["aciklama"]), robots=robots,
           url=url, md=s["md"], surum=surum or "taslak", tr=html_yap(tr, False),
           en=html_yap(en, True), baslik_en=html.escape(s["baslik_en"]))


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("--docs", default=os.path.join(SITE, "..", "..", "mobile", "bardino", "docs"))
    ap.add_argument("--onizleme", action="store_true")
    a = ap.parse_args()

    hazir, hatalar, surumler = [], [], set()
    for s in SAYFALAR:
        with open(os.path.join(a.docs, s["md"]), encoding="utf-8") as f:
            tr, en = bol(f.read().replace("\r\n", "\n"))
        h, surum = denetle(s["md"], tr, en)
        hatalar += h
        surumler.add(surum)
        hazir.append((s, tr, en, surum))
    if len(surumler) > 1:
        hatalar.append("iki metnin surumu farkli: %s" % sorted(map(str, surumler)))

    if hatalar and not a.onizleme:
        print("YAYINLANMADI, %d sorun:" % len(hatalar))
        for h in hatalar:
            print("  - " + h)
        sys.exit(1)

    hedef = os.path.join(SITE, "uyelik-onizleme" if a.onizleme else "uyelik")
    os.makedirs(hedef, exist_ok=True)
    for s, tr, en, surum in hazir:
        yol = os.path.join(hedef, s["cikti"])
        with open(yol, "w", encoding="utf-8", newline="\n") as f:
            f.write(sayfa(s, tr, en, surum, bool(a.onizleme)))
        print("yazildi", yol)
    if hatalar:
        print("ONIZLEME, yayina hazir degil (%d sorun)" % len(hatalar))


if __name__ == "__main__":
    main()
