# -*- coding: utf-8 -*-
"""bardino.app'in kendi gizlilik sayfasi: privacy.html (EN) ve tr/privacy.html.

    python tools/gizlilik.py

Oyunlarin gizlilik politikalari kendi sitelerinde; bu sayfa yalniz bu web
sitesini anlatiyor. Sitede cerez, analitik, form, hesap ve dis kaynak yok;
bunu degistiren biri bu metni de degistirmeli. Barindirma: GitHub Pages,
onunde Cloudflare (yanit basliginda server: cloudflare).
"""
import html
import os

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TARIH = {"en": "14 October 2026", "tr": "14 Ekim 2026"}

METIN = {
    "en": {
        "title": "Privacy on bardino.app",
        "desc": "What the bardino.app website does with your data: no cookies, no analytics, nothing loaded from other servers.",
        "home": "Bardino home",
        "updated": "Last updated",
        "body": [
            ("p", "This page is about this website, bardino.app. Each game has its own privacy policy: "
                  '<a href="https://decimo.bardino.app/privacy-policy.html">Decimo</a>, '
                  '<a href="https://colmo.bardino.app/privacy.html">Colmo</a> and '
                  '<a href="https://palmo.bardino.app/privacy.html">Palmo</a>.'),
            ("h2", "What this site does not do"),
            ("p", "It sets no cookies and runs no analytics or advertising. It has no forms and no accounts. "
                  "It loads no fonts, scripts or images from other servers. We do not collect or store anything about visitors ourselves."),
            ("h2", "Hosting"),
            ("p", "The site is published with GitHub Pages and delivered through Cloudflare. Like any web server, they receive "
                  "your IP address and browser details with each request and may keep them in their logs to deliver and protect "
                  "the site. Their own policies apply: "
                  '<a href="https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement">GitHub</a>, '
                  '<a href="https://www.cloudflare.com/privacypolicy/">Cloudflare</a>.'),
            ("h2", "E-mail"),
            ("p", "If you write to info@bardino.app, we use your address and your message only to reply to you."),
            ("h2", "Contact"),
            ("p", "Bardino Technology, <!--email_off--><a href=\"mailto:info@bardino.app\">info@bardino.app</a><!--/email_off-->"),
        ],
    },
    "tr": {
        "title": "bardino.app'te gizlilik",
        "desc": "bardino.app web sitesinin verilerinizle ne yaptığı: çerez yok, analitik yok, başka sunuculardan hiçbir şey yüklenmiyor.",
        "home": "Bardino ana sayfa",
        "updated": "Son güncelleme",
        "body": [
            ("p", "Bu sayfa yalnız bu web sitesini, bardino.app'i anlatır. Her oyunun kendi gizlilik politikası var: "
                  '<a href="https://decimo.bardino.app/privacy-policy.html">Decimo</a>, '
                  '<a href="https://colmo.bardino.app/tr/privacy.html">Colmo</a> ve '
                  '<a href="https://palmo.bardino.app/tr/privacy.html">Palmo</a>.'),
            ("h2", "Bu sitenin yapmadıkları"),
            ("p", "Çerez kullanmaz, analitik ya da reklam çalıştırmaz. Formu ve üyeliği yoktur. Başka sunuculardan yazı tipi, "
                  "betik ya da görsel yüklemez. Ziyaretçiler hakkında kendimiz hiçbir şey toplamaz ve saklamayız."),
            ("h2", "Barındırma"),
            ("p", "Site GitHub Pages ile yayımlanır ve Cloudflare üzerinden sunulur. Her web sunucusu gibi bunlar da her istekte "
                  "IP adresinizi ve tarayıcı bilgilerinizi alır; siteyi sunmak ve korumak için kayıtlarında tutabilir. "
                  "Onların kendi politikaları geçerlidir: "
                  '<a href="https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement">GitHub</a>, '
                  '<a href="https://www.cloudflare.com/privacypolicy/">Cloudflare</a>.'),
            ("h2", "E-posta"),
            ("p", "info@bardino.app adresine yazarsanız adresinizi ve mesajınızı yalnız size yanıt vermek için kullanırız."),
            ("h2", "İletişim"),
            ("p", "Bardino Technology, <!--email_off--><a href=\"mailto:info@bardino.app\">info@bardino.app</a><!--/email_off-->"),
        ],
    },
}


def sayfa(dil):
    m = METIN[dil]
    kok = "" if dil == "en" else "../"
    ev = "./" if dil == "en" else "./"
    govde = "\n".join("<%s>%s</%s>" % (tag, icerik, tag) for tag, icerik in m["body"])
    return """<!DOCTYPE html>
<html lang="{dil}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} - Bardino Technology</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="https://bardino.app/{yol}privacy.html">
<link rel="alternate" hreflang="en" href="https://bardino.app/privacy.html">
<link rel="alternate" hreflang="tr" href="https://bardino.app/tr/privacy.html">
<link rel="alternate" hreflang="x-default" href="https://bardino.app/privacy.html">
<meta name="theme-color" content="#FDF6F0" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#15132A" media="(prefers-color-scheme: dark)">
<link rel="icon" href="{kok}favicon-32.png" sizes="32x32" type="image/png">
<link rel="icon" href="{kok}favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="{kok}assets/site.css">
</head>
<body class="doc-page">
<!-- tools/gizlilik.py uretti. Elle duzenleme. -->
<header class="site-head">
  <div class="wrap">
    <a class="doc-home" href="{ev}" aria-label="{home}"><img src="{kok}assets/bardino-mark.svg" width="38" height="38" alt=""><span>Bardino</span></a>
    <nav class="site-nav" aria-label="{home}">
      <div class="lang" role="group" aria-label="Language / Dil">
        <a href="{kok}privacy.html" hreflang="en" lang="en"{cur_en}>English</a>
        <a href="{kok}tr/privacy.html" hreflang="tr" lang="tr"{cur_tr}>Türkçe</a>
      </div>
    </nav>
  </div>
</header>
<main id="main" class="wrap doc">
<article>
<h1>{title}</h1>
<p>{updated}: {tarih}</p>
{govde}
</article>
</main>
<footer class="site-foot">
  <div class="wrap">
    <p class="fine">&copy; 2026 Bardino Technology</p>
  </div>
</footer>
</body>
</html>
""".format(dil=dil, title=html.escape(m["title"]), desc=html.escape(m["desc"]),
           yol="" if dil == "en" else "tr/", kok=kok, ev=ev, home=html.escape(m["home"]),
           cur_en=' aria-current="page"' if dil == "en" else "",
           cur_tr=' aria-current="page"' if dil == "tr" else "",
           updated=m["updated"], tarih=TARIH[dil], govde=govde)


def main():
    for dil, yol in (("en", "privacy.html"), ("tr", os.path.join("tr", "privacy.html"))):
        with open(os.path.join(SITE, yol), "w", encoding="utf-8", newline="\n") as f:
            f.write(sayfa(dil))
        print("yazildi", yol)


if __name__ == "__main__":
    main()
