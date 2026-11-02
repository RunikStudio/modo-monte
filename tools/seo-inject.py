#!/usr/bin/env python3
"""Inyecta metadatos SEO (description, canonical, Open Graph, Twitter, JSON-LD)
en todas las páginas del sitio Modo Monte."""
import json
import os

BASE = "https://modomonte.com"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---------------------------------------------------------------- metadata --
PAGES = {
    "index.html": {
        "title": "Modo Monte | Glamping en Alpa Corral, Córdoba",
        "desc": "Glamping en Alpa Corral, Córdoba. Domos con vistas a las sierras, "
                "desayunos caseros, caminatas guiadas, tirolesa y escapadas en grupo. "
                "Reservá tu estadía online.",
        "og": "Glamping en Alpa Corral, Córdoba",
        "img": "/images/og-modo-monte.jpg",
    },
    "alojamientos.html": {
        "title": "Alojamientos | Domos Flora, Alba y Lucía | Modo Monte",
        "desc": "Conocé los alojamientos de Modo Monte en Alpa Corral: domos Flora, Alba y "
                "Lucía, tarifa general, escapadita en manada y verano a la vista. Reservá online.",
        "og": "Alojamientos en domos - Alpa Corral",
        "img": "/images/Domos/FLORA.webp",
    },
    "amenities.html": {
        "title": "Amenities | Todo lo que incluye tu domo | Modo Monte",
        "desc": "Desayunos caseros, wifi, cocina equipada, climatización y todos los servicios "
                "de tu domo en Alpa Corral, Córdoba.",
        "og": "Amenities de los domos Modo Monte",
        "img": "/images/Amenities/01.webp",
    },
    "caminatas.html": {
        "title": "Caminatas guiadas | Río Las Barrancas, Talita y El Cajón | Modo Monte",
        "desc": "Caminatas guiadas por las sierras de Alpa Corral: Río Las Barrancas, Río Talita, "
                "Río Escondido, El Cajón y San Bartolomé. Salidas todos los días con guías locales.",
        "og": "Caminatas guiadas en Alpa Corral",
        "img": "/images/Caminatas/RIO LAS BARRANCAS.webp",
    },
    "nosotros.html": {
        "title": "Nosotros | La historia de Modo Monte | Alpa Corral",
        "desc": "Conocé Modo Monte: glamping con raíces en Alpa Corral, Córdoba. Un proyecto "
                "que acerca la montaña y las actividades al aire libre en un solo lugar.",
        "og": "La historia de Modo Monte",
        "img": "/images/Nosotros/3c8d6ab9-dc77-4c7f-8e50-9d0cf69f01fc.webp",
    },
    "tirolesa.html": {
        "title": "Tirolesa | 35 metros sobre el río Las Barrancas | Modo Monte",
        "desc": "Viví la tirolesa de Modo Monte: 35 metros de altura sobre el río Las Barrancas, "
                "en el corazón de las sierras de Alpa Corral, Córdoba.",
        "og": "Tirolesa sobre el río Las Barrancas",
        "img": "/images/Tirolesa/01.webp",
    },
    "ubicacion.html": {
        "title": "Ubicación | Alpa Corral, sierras del sur de Córdoba | Modo Monte",
        "desc": "Cómo llegar a Modo Monte en Alpa Corral, en el sur de la provincia de Córdoba. "
                "Rutas, distancias, acceso y contacto.",
        "og": "Ubicación de Modo Monte en Alpa Corral",
        "img": "/images/Ubicacion/20251214_094300.webp",
    },
    "wikiloc.html": {
        "title": "Wikiloc | Rutas y tracks de Modo Monte | Alpa Corral",
        "desc": "Descargá las rutas y los tracks de Modo Monte en Wikiloc: caminatas guiadas, "
                "ríos de montaña y tesoros de Alpa Corral.",
        "og": "Rutas de Modo Monte en Wikiloc",
        "img": "/images/Wikiloc/FRAN Y AMA.webp",
    },
    "alojamientos/flora.html": {
        "title": "Domo Flora | Alojamiento con ventanal panorámico | Modo Monte",
        "desc": "Domo Flora en Alpa Corral: ventanal panorámico, cama queen, cocina equipada y "
                "terraza privada con fogonero. Capacidad para 2 personas.",
        "og": "Domo Flora en Alpa Corral",
        "img": "/images/Domos/FLORA/01.webp",
    },
    "alojamientos/alba.html": {
        "title": "Domo Alba | Alojamiento en Alpa Corral | Modo Monte",
        "desc": "Domo Alba en Alpa Corral: cama amplia, cocina equipada y todos los servicios "
                "de Modo Monte a pasos del río Las Barrancas.",
        "og": "Domo Alba en Alpa Corral",
        "img": "/images/Domos/ALBA.webp",
    },
    "alojamientos/lucia.html": {
        "title": "Domo Lucía | Alojamiento con vista al valle | Modo Monte",
        "desc": "Domo Lucía en Alpa Corral: habitación amplia con ventanal, King size y "
                "equipamiento completo para 2 personas.",
        "og": "Domo Lucía en Alpa Corral",
        "img": "/images/Domos/LUCIA.webp",
    },
    "alojamientos/tarifa-general.html": {
        "title": "Tarifa General | Tarifas y condiciones de estadía | Modo Monte",
        "desc": "Tarifa general de los domos de Modo Monte: qué incluye la estadía, noches "
                "mínimas, descuentos por estadías de semana y tarifas de temporada alta y baja.",
        "og": "Tarifa general de los domos Modo Monte",
        "img": "/images/TarifaGeneral/01.webp",
    },
    "alojamientos/escapadita-en-manada.html": {
        "title": "Escapadita en Manada | Combo para grupos de 4 a 9 personas | Modo Monte",
        "desc": "Escapadita en Manada: 2 noches en domos, desayunos caseros, fogón de bienvenida "
                "y trekking guiado por las sierras de Alpa Corral para grupos de 4 a 9 personas.",
        "og": "Escapadita en Manada en Alpa Corral",
        "img": "/images/EscapaditaEnManada/01.webp",
    },
    "alojamientos/verano-a-la-vista.html": {
        "title": "Verano a la Vista | 4 noches en domos con actividades | Modo Monte",
        "desc": "Verano a la Vista: 4 noches en domos en las sierras, desayunos caseros, travesía "
                "por Alpa y tirolesa a 35 metros sobre el río Las Barrancas.",
        "og": "Verano a la Vista en Alpa Corral",
        "img": "/images/VeranoALaVista/01.webp",
    },
    "caminatas/barrancas.html": {
        "title": "Río Las Barrancas | Caminata guiada | Modo Monte",
        "desc": "Caminata guiada por el río Las Barrancas en Alpa Corral: sierras, cascadas y "
                "paisajes de montaña con guías locales.",
        "og": "Caminata guiada por el río Las Barrancas",
        "img": "/images/Caminatas/RIO_LAS_BARRANCAS/01.webp",
    },
    "caminatas/bartolome.html": {
        "title": "San Bartolomé | Caminata guiada | Modo Monte",
        "desc": "Caminata guiada a San Bartolomé, uno de los miradores más altos de las sierras "
                "de Alpa Corral, Córdoba.",
        "og": "Caminata guiada a San Bartolomé",
        "img": "/images/Caminatas/EL CAJON/00.webp",
    },
    "caminatas/cajon.html": {
        "title": "El Cajón | Caminata guiada | Modo Monte",
        "desc": "Caminata guiada por El Cajón en Alpa Corral: un cañón de piedra entre sierras, "
                "con piletas naturales y fósiles del Cretácico.",
        "og": "Caminata guiada por El Cajón",
        "img": "/images/Caminatas/EL_CAJON/00.webp",
    },
    "caminatas/escondido.html": {
        "title": "Río Escondido | Caminata guiada | Modo Monte",
        "desc": "Caminata guiada por el río Escondido en Alpa Corral: un río de montaña entre "
                "piedras y pools de agua colorida.",
        "og": "Caminata guiada por el río Escondido",
        "img": "/images/Caminatas/RIO_ESCONDIDO/01.webp",
    },
    "caminatas/talita.html": {
        "title": "Río Talita | Caminata guiada | Modo Monte",
        "desc": "Caminata guiada por el río Talita en Alpa Corral: cascadas, natatorios naturales "
                "y un baño de montaña en las sierras de Córdoba.",
        "og": "Caminata guiada por el río Talita",
        "img": "/images/Caminatas/RIO_TALITA/02.webp",
    },
}

# --------------------------------------------------------------- JSON-LD ----
ORG = {
    "@type": "LodgingBusiness",
    "@id": BASE + "/#organization",
    "name": "Modo Monte",
    "alternateName": "Modo Monte Glamping",
    "url": BASE + "/",
    "logo": BASE + "/images/LOGOTIPO-01.png",
    "image": BASE + "/images/og-modo-monte.jpg",
    "description": "Glamping en domos en Alpa Corral, sierras del sur de Córdoba. Alojamientos, "
                   "caminatas guiadas, tirolesa y actividades al aire libre.",
    "telephone": "+5493513265647",
    "priceRange": "$$",
    "address": {
        "@type": "PostalAddress",
        "addressLocality": "Alpa Corral",
        "addressRegion": "Córdoba",
        "addressCountry": "AR",
    },
    "geo": {"@type": "GeoCoordinates", "latitude": -31.7265, "longitude": -64.6900},
    "sameAs": ["https://www.instagram.com/modo.monte.alpa"],
    "openingHoursSpecification": [{
        "@type": "OpeningHoursSpecification",
        "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
        "opens": "00:00", "closes": "23:59",
    }],
    "makesOffer": [
        {"@type": "Offer", "name": "Domo Flora", "category": "Alojamiento"},
        {"@type": "Offer", "name": "Domo Alba", "category": "Alojamiento"},
        {"@type": "Offer", "name": "Domo Lucía", "category": "Alojamiento"},
        {"@type": "Offer", "name": "Escapadita en Manada", "category": "Combo"},
        {"@type": "Offer", "name": "Verano a la Vista", "category": "Combo"},
    ],
}

SITE = {
    "@type": "WebSite",
    "@id": BASE + "/#website",
    "url": BASE + "/",
    "name": "Modo Monte",
    "inLanguage": "es-AR",
    "publisher": {"@id": BASE + "/#organization"},
}

def breadcrumb(path, names):
    """names ordenados de la raiz a la hoja: ['Inicio', 'Alojamientos', 'Flora']"""
    parts = path.replace(".html", "").split("/")
    urls = [BASE + "/"]
    for i in range(1, len(parts)):
        urls.append(BASE + "/" + "/".join(parts[:i]))
    urls.append(BASE + "/" + path)

    items = []
    for i, (name, url) in enumerate(zip(names, urls)):
        items.append({"@type": "ListItem", "position": i + 1, "name": name, "item": url})
    return {"@type": "BreadcrumbList", "itemListElement": items}


def jsonld_for(path, meta):
    blocks = []
    if path == "index.html":
        blocks.append(ORG)
        blocks.append(SITE)
    else:
        parts = path.replace(".html", "").split("/")
        if len(parts) == 1:
            names = ["Inicio", meta["og"]]
        else:
            leaf = parts[-1].replace("-", " ").title()
            parent = parts[-2].replace("-", " ").title()
            if parent == "Alojamientos":
                parent = "Alojamientos"
            elif parent == "Caminatas":
                parent = "Caminatas"
            names = ["Inicio", parent, leaf]
        blocks.append(breadcrumb(path, names))

    # tipo específico por sección
    if path.startswith("alojamientos/") and path not in ("alojamientos/tarifa-general.html",
                                                          "alojamientos/escapadita-en-manada.html",
                                                          "alojamientos/verano-a-la-vista.html"):
        domo = {"flora": "Flora", "alba": "Alba", "lucia": "Lucía"}[parts[-1]]
        blocks.append({
            "@type": "LodgingBusiness",
            "name": "Domo " + domo,
            "url": BASE + "/" + path,
            "image": BASE + meta["img"],
            "description": meta["desc"],
            "containedInPlace": {"@type": "LodgingBusiness", "name": "Modo Monte", "@id": BASE + "/#organization"},
            "amenityFeature": [
                {"@type": "LocationFeatureSpecification", "name": "Desayunos incluidos", "value": True},
                {"@type": "LocationFeatureSpecification", "name": "Wifi", "value": True},
                {"@type": "LocationFeatureSpecification", "name": "Cocina equipada", "value": True},
                {"@type": "LocationFeatureSpecification", "name": "Terraza privada", "value": True},
            ],
            "address": {"@type": "PostalAddress", "addressLocality": "Alpa Corral",
                         "addressRegion": "Córdoba", "addressCountry": "AR"},
        })
    elif path.startswith("caminatas/"):
        blocks.append({
            "@type": "TouristAttraction",
            "name": meta["og"],
            "url": BASE + "/" + path,
            "image": BASE + meta["img"],
            "description": meta["desc"],
            "touristType": "Caminata guiada",
            "isAccessibleForFree": False,
            "provider": {"@id": BASE + "/#organization"},
        })
    elif path in ("alojamientos/escapadita-en-manada.html", "alojamientos/verano-a-la-vista.html",
                  "alojamientos/tarifa-general.html"):
        blocks.append({
            "@type": "TouristAttraction",
            "name": meta["og"],
            "url": BASE + "/" + path,
            "image": BASE + meta["img"],
            "description": meta["desc"],
            "touristType": "Combo de escapada",
            "provider": {"@id": BASE + "/#organization"},
        })
    elif path in ("alojamientos.html", "caminatas.html", "amenities.html"):
        blocks.append({
            "@type": "CollectionPage",
            "name": meta["og"],
            "url": BASE + "/" + path,
            "description": meta["desc"],
            "isPartOf": {"@id": BASE + "/#website"},
        })
    return blocks


# ------------------------------------------------------------------ utils --
def canonical(path):
    if path == "index.html":
        return BASE + "/"
    return BASE + "/" + path.replace("/index.html", "/")


def head_block(path, meta):
    url = canonical(path)
    img = meta["img"]
    img_url = BASE + img if img.startswith("/") else url.rsplit("/", 1)[0] + "/" + img
    lines = [
        "",
        '    <!-- ===== SEO ===== -->',
        '    <meta name="description" content="%s">' % meta["desc"],
        '    <meta name="author" content="Modo Monte">',
        '    <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">',
        '    <meta name="theme-color" content="#844C43">',
        '    <link rel="canonical" href="%s">' % url,
        '    <link rel="sitemap" type="application/xml" href="/sitemap.xml">',
        '    <link rel="apple-touch-icon" href="/favicon.png">',
        '    <link rel="manifest" href="/site.webmanifest">',
        '',
        '    <!-- Open Graph -->',
        '    <meta property="og:type" content="website">',
        '    <meta property="og:site_name" content="Modo Monte">',
        '    <meta property="og:locale" content="es_AR">',
        '    <meta property="og:title" content="%s">' % meta["title"],
        '    <meta property="og:description" content="%s">' % meta["desc"],
        '    <meta property="og:url" content="%s">' % url,
        '    <meta property="og:image" content="%s">' % img_url,
        '    <meta property="og:image:width" content="1200">',
        '    <meta property="og:image:height" content="630">',
        '    <meta property="og:image:alt" content="%s">' % meta["og"],
        '',
        '    <!-- Twitter -->',
        '    <meta name="twitter:card" content="summary_large_image">',
        '    <meta name="twitter:title" content="%s">' % meta["title"],
        '    <meta name="twitter:description" content="%s">' % meta["desc"],
        '    <meta name="twitter:image" content="%s">' % img_url,
    ]
    return "\n".join(lines)


def jsonld_block(path, meta):
    blocks = jsonld_for(path, meta)
    out = ['    <!-- Datos estructurados (schema.org) -->',
           '    <script type="application/ld+json">']
    for b in blocks:
        out.append(json.dumps(b, ensure_ascii=False, indent=4))
    out.append('    </script>')
    return "\n".join(out)


def inject(path, meta):
    full = os.path.join(ROOT, path)
    src = open(full, encoding="utf-8").read()
    if 'name="description"' in src:          # ya inyectado
        return False
    # título
    import re
    src = re.sub(r"<title>.*?</title>", "<title>%s</title>" % meta["title"], src, count=1, flags=re.S)
    # punto de inserción: luego del bloque de favicon
    m = re.search(r'<link rel="shortcut icon"[^>]*>\n', src)
    assert m, path
    block = head_block(path, meta) + "\n\n" + jsonld_block(path, meta) + "\n"
    src = src[:m.end()] + block + src[m.end():]
    open(full, "w", encoding="utf-8").write(src)
    return True


for path, meta in PAGES.items():
    if inject(path, meta):
        print("SEO ok:", path)

# --------------------------------------------------------------- extras ----
# sitemap
today = "2024-01-01"
priority = {
    "index.html": "1.0", "alojamientos.html": "0.9", "caminatas.html": "0.9",
    "amenities.html": "0.8", "ubicacion.html": "0.8", "nosotros.html": "0.7",
    "tirolesa.html": "0.7", "wikiloc.html": "0.6",
}
items = []
for path in PAGES:
    pr = priority.get(path, "0.8")
    items.append(
        "  <url>\n    <loc>%s</loc>\n    <lastmod>%s</lastmod>\n"
        "    <changefreq>monthly</changefreq>\n    <priority>%s</priority>\n  </url>"
        % (canonical(path), today, pr)
    )
with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            + "\n".join(items) + "\n</urlset>\n")
print("sitemap ok")

# robots
with open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8") as f:
    f.write("User-agent: *\n"
            "Allow: /\n"
            "\n"
            "# Sin áreas privadas ni panel de administración\n"
            "Disallow: /reformas/\n"
            "\n"
            "Sitemap: %s/sitemap.xml\n" % BASE)
print("robots ok")

# manifest
with open(os.path.join(ROOT, "site.webmanifest"), "w", encoding="utf-8") as f:
    json.dump({
        "name": "Modo Monte",
        "short_name": "Modo Monte",
        "description": "Glamping en Alpa Corral, Córdoba",
        "start_url": "/",
        "display": "standalone",
        "background_color": "#F3ECE6",
        "theme_color": "#844C43",
        "lang": "es-AR",
        "icons": [
            {"src": "/favicon.png", "sizes": "512x512", "type": "image/png"},
        ],
    }, f, indent=4, ensure_ascii=False)
print("manifest ok")
