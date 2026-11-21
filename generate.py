from datetime import date
import os
import urllib.parse

DOMAIN = "https://rollershutter.htkdecor.com.my"
PHONE_DISPLAY = "017-431 5233"
PHONE_TEL = "0174315233"
WA_NUMBER = "60174315233"
PRICE_FROM = "RM 26.00 / ft²"
BRAND_NAME = "HTK Pintu Shutter"
TODAY_STR = date.today().isoformat()

# 1. 已整理、去重并生成标准 URL Slug 的 Kuala Lumpur & Selangor 全地区列表（共 154 个）
regions_data = [
    # --- Kuala Lumpur (KL) ---
    ("ampang-hilir", "Ampang Hilir"),
    ("bandar-damai-perdana", "Bandar Damai Perdana"),
    ("bandar-menjalara", "Bandar Menjalara"),
    ("bandar-tasik-selatan", "Bandar Tasik Selatan"),
    ("bangsar", "Bangsar"),
    ("bangsar-south", "Bangsar South"),
    ("batu", "Batu"),
    ("brickfields", "Brickfields"),
    ("bukit-bintang", "Bukit Bintang"),
    ("bukit-jalil", "Bukit Jalil"),
    ("bukit-kiara", "Bukit Kiara"),
    ("bukit-ledang", "Bukit Ledang"),
    ("bukit-persekutuan", "Bukit Persekutuan"),
    ("bukit-tunku", "Bukit Tunku"),
    ("chan-sow-lin", "Chan Sow Lin"),
    ("cheras", "Cheras"),
    ("city-centre", "City Centre"),
    ("country-heights-damansara", "Country Heights Damansara"),
    ("damansara", "Damansara"),
    ("damansara-heights", "Damansara Heights"),
    ("desa-pandan", "Desa Pandan"),
    ("desa-parkcity", "Desa ParkCity"),
    ("desa-petaling", "Desa Petaling"),
    ("federal-hill", "Federal Hill"),
    ("jalan-ipoh", "Jalan Ipoh"),
    ("jalan-kuching", "Jalan Kuching"),
    ("jalan-sultan-ismail", "Jalan Sultan Ismail"),
    ("jinjang", "Jinjang"),
    ("kenny-hills", "Kenny Hills"),
    ("kampung-baru", "Kampung Baru"),
    ("kepong", "Kepong"),
    ("keramat", "Keramat"),
    ("kl-city", "KL City"),
    ("kl-eco-city", "KL Eco City"),
    ("kl-sentral", "KL Sentral"),
    ("klcc", "KLCC"),
    ("kuchai-lama", "Kuchai Lama"),
    ("mid-valley-city", "Mid Valley City"),
    ("mont-kiara", "Mont Kiara"),
    ("old-klang-road", "Old Klang Road"),
    ("oug", "OUG"),
    ("pandan-indah", "Pandan Indah"),
    ("pandan-jaya", "Pandan Jaya"),
    ("pandan-perdana", "Pandan Perdana"),
    ("pantai", "Pantai"),
    ("pekan-batu", "Pekan Batu"),
    ("pudu", "Pudu"),
    ("salak-selatan", "Salak Selatan"),
    ("segambut", "Segambut"),
    ("sentul", "Sentul"),
    ("seputeh", "Seputeh"),
    ("serdang", "Serdang"),
    ("setapak", "Setapak"),
    ("setiawangsa", "Setiawangsa"),
    ("solaris-dutamas", "Solaris Dutamas"),
    ("sri-damansara", "Sri Damansara"),
    ("sri-hartamas", "Sri Hartamas"),
    ("sri-petaling", "Sri Petaling"),
    ("sungai-besi", "Sungai Besi"),
    ("sungai-penchala", "Sungai Penchala"),
    ("sunway-spk", "Sunway SPK"),
    ("taman-desa", "Taman Desa"),
    ("taman-duta", "Taman Duta"),
    ("taman-melawati", "Taman Melawati"),
    ("taman-tun-dr-ismail", "Taman Tun Dr Ismail"),
    ("taman-permata", "Taman Permata"),
    ("titiwangsa", "Titiwangsa"),
    ("tpm", "TPM"),
    ("wangsa-maju", "Wangsa Maju"),

    # --- Selangor (已自动去除与 KL 重复的 Cheras & Damansara) ---
    ("aman-perdana", "Aman Perdana"),
    ("ampang", "Ampang"),
    ("ara-damansara", "Ara Damansara"),
    ("balakong", "Balakong"),
    ("bandar-botanic", "Bandar Botanic"),
    ("bandar-bukit-tinggi", "Bandar Bukit Tinggi"),
    ("bandar-saujana-putra", "Bandar Saujana Putra"),
    ("bandar-sungai-long", "Bandar Sungai Long"),
    ("bandar-sunway", "Bandar Sunway"),
    ("bangi", "Bangi"),
    ("banting", "Banting"),
    ("batang-kali", "Batang Kali"),
    ("batu-caves", "Batu Caves"),
    ("beranang", "Beranang"),
    ("bestari-jaya-batang-berjuntai", "Bestari Jaya (Batang Berjuntai)"),
    ("bukit-beruntung", "Bukit Beruntung"),
    ("bukit-jelutong", "Bukit Jelutong"),
    ("cyberjaya", "Cyberjaya"),
    ("dengkil", "Dengkil"),
    ("glenmarie", "Glenmarie"),
    ("gombak", "Gombak"),
    ("hulu-langat", "Hulu Langat"),
    ("ijok", "Ijok"),
    ("jenjarom", "Jenjarom"),
    ("jeram", "Jeram"),
    ("kajang", "Kajang"),
    ("kapar", "Kapar"),
    ("kerling", "Kerling"),
    ("klang", "Klang"),
    ("kota-damansara", "Kota Damansara"),
    ("kota-emerald", "Kota Emerald"),
    ("kota-kemuning", "Kota Kemuning"),
    ("kota-warisan", "Kota Warisan"),
    ("kuala-kubu-baru", "Kuala Kubu Baru"),
    ("kuala-selangor", "Kuala Selangor"),
    ("kuang", "Kuang"),
    ("kundang", "Kundang"),
    ("meru", "Meru"),
    ("morib", "Morib"),
    ("mutiara-damansara", "Mutiara Damansara"),
    ("pandamaran", "Pandamaran"),
    ("petaling-jaya", "Petaling Jaya"),
    ("port-klang", "Port Klang"),
    ("puchong", "Puchong"),
    ("pulau-carey", "Pulau Carey"),
    ("pulau-indah", "Pulau Indah"),
    ("pulau-ketam", "Pulau Ketam"),
    ("puncak-alam", "Puncak Alam"),
    ("puncak-jalil", "Puncak Jalil"),
    ("putra-heights", "Putra Heights"),
    ("rasa", "Rasa"),
    ("rawang", "Rawang"),
    ("sabak-bernam", "Sabak Bernam"),
    ("salak-tinggi", "Salak Tinggi"),
    ("saujana-utama", "Saujana Utama"),
    ("sekinchan", "Sekinchan"),
    ("selayang", "Selayang"),
    ("semenyih", "Semenyih"),
    ("sepang", "Sepang"),
    ("serendah", "Serendah"),
    ("seri-kembangan", "Seri Kembangan"),
    ("setia-alam", "Setia Alam"),
    ("setia-eco-park", "Setia Eco Park"),
    ("shah-alam", "Shah Alam"),
    ("sierra-mas", "Sierra Mas"),
    ("ss2", "SS2"),
    ("subang-bestari", "Subang Bestari"),
    ("subang-heights", "Subang Heights"),
    ("subang-jaya", "Subang Jaya"),
    ("subang-perdana", "Subang Perdana"),
    ("sungai-ayer-tawar", "Sungai Ayer Tawar"),
    ("sungai-besar", "Sungai Besar"),
    ("sungai-buloh", "Sungai Buloh"),
    ("sungai-panjang", "Sungai Panjang"),
    ("sungai-pelek", "Sungai Pelek"),
    ("taman-ttdi-jaya", "Taman TTDI Jaya"),
    ("tanjong-duabelas", "Tanjong Duabelas"),
    ("tanjong-karang", "Tanjong Karang"),
    ("tanjong-sepat", "Tanjong Sepat"),
    ("telok-panglima-garang", "Telok Panglima Garang"),
    ("tropicana", "Tropicana"),
    ("ulu-bernam", "Ulu Bernam"),
    ("ulu-klang", "Ulu Klang"),
    ("ulu-yam", "Ulu Yam"),
    ("usj", "USJ"),
    ("usj-heights", "USJ Heights"),
    ("valencia", "Valencia")
]

# 2. 附近地区映射表（子页面底部仅展示附近几个地区，未列出的地区会自动从列表中补足）
nearby_map = {
    "aman-perdana": ["meru", "klang", "setia-alam", "kapar", "bandar-bukit-tinggi", "shah-alam"],
    "ampang-hilir": ["ampang", "klcc", "city-centre", "pandan-indah", "keramat", "titiwangsa"],
    "ampang": ["ampang-hilir", "pandan-indah", "pandan-jaya", "pandan-perdana", "ulu-klang", "cheras"],
    "ara-damansara": ["subang-jaya", "glenmarie", "petaling-jaya", "tropicana", "kota-damansara", "bandar-sunway"],
    "balakong": ["seri-kembangan", "cheras", "kajang", "bandar-sungai-long", "bandar-damai-perdana", "serdang"],
    "bandar-botanic": ["bandar-bukit-tinggi", "klang", "pandamaran", "port-klang", "telok-panglima-garang", "kota-kemuning"],
    "bandar-bukit-tinggi": ["bandar-botanic", "klang", "pandamaran", "port-klang", "telok-panglima-garang", "jenjarom"],
    "bandar-damai-perdana": ["cheras", "balakong", "bandar-sungai-long", "kajang", "seri-kembangan", "desa-petaling"],
    "bandar-menjalara": ["kepong", "sri-damansara", "desa-parkcity", "segambut", "jinjang", "taman-tun-dr-ismail"],
    "bandar-saujana-putra": ["puchong", "putra-heights", "cyberjaya", "jenjarom", "telok-panglima-garang", "sepang"],
    "bandar-sungai-long": ["kajang", "balakong", "cheras", "bandar-damai-perdana", "hulu-langat", "semenyih"],
    "bandar-sunway": ["subang-jaya", "usj", "petaling-jaya", "puchong", "glenmarie", "ss2"],
    "bandar-tasik-selatan": ["sungai-besi", "sri-petaling", "bukit-jalil", "desa-petaling", "cheras", "salak-selatan"],
    "bangi": ["kajang", "putrajaya", "cyberjaya", "seri-kembangan", "semenyih", "sepang"],
    "banting": ["telok-panglima-garang", "jenjarom", "morib", "pulau-carey", "sepang", "dengkil"],
    "bangsar": ["bangsar-south", "kl-sentral", "brickfields", "damansara-heights", "kl-eco-city", "mid-valley-city"],
    "bangsar-south": ["bangsar", "kl-eco-city", "mid-valley-city", "petaling-jaya", "taman-desa", "old-klang-road"],
    "batu-caves": ["selayang", "gombak", "sentul", "jalan-ipoh", "kepong", "ulu-klang"],
    "cheras": ["bandar-damai-perdana", "balakong", "ampang", "pandan-perdana", "pudu", "bandar-tasik-selatan"],
    "cyberjaya": ["putrajaya", "puchong", "dengkil", "bangi", "seri-kembangan", "sepang"],
    "damansara": ["damansara-heights", "kota-damansara", "mutiara-damansara", "tropicana", "petaling-jaya", "sri-hartamas"],
    "damansara-heights": ["bangsar", "sri-hartamas", "mont-kiara", "bukit-tunku", "taman-tun-dr-ismail", "kl-sentral"],
    "desa-parkcity": ["bandar-menjalara", "kepong", "sri-damansara", "segambut", "jinjang", "taman-tun-dr-ismail"],
    "desa-petaling": ["sungai-besi", "sri-petaling", "kuchai-lama", "salak-selatan", "bandar-tasik-selatan", "bukit-jalil"],
    "gombak": ["batu-caves", "selayang", "setapak", "wangsa-maju", "ulu-klang", "taman-melawati"],
    "kajang": ["bangi", "bandar-sungai-long", "balakong", "semenyih", "putrajaya", "hulu-langat"],
    "kepong": ["bandar-menjalara", "sri-damansara", "desa-parkcity", "jinjang", "segambut", "selayang"],
    "klang": ["bandar-bukit-tinggi", "bandar-botanic", "port-klang", "meru", "kapar", "pandamaran"],
    "klcc": ["city-centre", "bukit-bintang", "ampang-hilir", "kampung-baru", "jalan-sultan-ismail", "titiwangsa"],
    "kota-damansara": ["mutiara-damansara", "tropicana", "damansara", "sungai-buloh", "ara-damansara", "petaling-jaya"],
    "kota-kemuning": ["shah-alam", "putra-heights", "puchong", "bandar-botanic", "telok-panglima-garang", "usj"],
    "kuchai-lama": ["old-klang-road", "oug", "sri-petaling", "sungai-besi", "taman-desa", "bukit-jalil"],
    "mont-kiara": ["sri-hartamas", "solaris-dutamas", "segambut", "damansara-heights", "taman-tun-dr-ismail", "bukit-tunku"],
    "mutiara-damansara": ["kota-damansara", "damansara", "tropicana", "petaling-jaya", "sri-hartamas", "bandar-sunway"],
    "petaling-jaya": ["ss2", "damansara", "subang-jaya", "bandar-sunway", "bangsar-south", "taman-tun-dr-ismail"],
    "port-klang": ["klang", "pandamaran", "bandar-bukit-tinggi", "pulau-indah", "bandar-botanic", "kapar"],
    "puchong": ["subang-jaya", "usj", "seri-kembangan", "puncak-jalil", "putra-heights", "cyberjaya"],
    "putrajaya": ["cyberjaya", "bangi", "kajang", "seri-kembangan", "dengkil", "sepang"],
    "rawang": ["kundang", "serendah", "selayang", "batang-kali", "kuang", "kota-emerald"],
    "selayang": ["batu-caves", "kepong", "gombak", "rawang", "jinjang", "sentul"],
    "semenyih": ["kajang", "bangi", "beranang", "bandar-sungai-long", "hulu-langat", "dengkil"],
    "seri-kembangan": ["balakong", "puchong", "puncak-jalil", "bukit-jalil", "serdang", "cyberjaya"],
    "setia-alam": ["shah-alam", "meru", "aman-perdana", "klang", "bukit-jelutong", "setia-eco-park"],
    "shah-alam": ["glenmarie", "subang-jaya", "kota-kemuning", "setia-alam", "bukit-jelutong", "klang"],
    "sri-hartamas": ["mont-kiara", "solaris-dutamas", "damansara-heights", "taman-tun-dr-ismail", "segambut", "bukit-tunku"],
    "sri-petaling": ["bukit-jalil", "sungai-besi", "kuchai-lama", "oug", "desa-petaling", "seri-kembangan"],
    "subang-jaya": ["usj", "bandar-sunway", "puchong", "glenmarie", "petaling-jaya", "shah-alam"],
    "sungai-besi": ["sri-petaling", "desa-petaling", "bandar-tasik-selatan", "kuchai-lama", "bukit-jalil", "salak-selatan"],
    "sungai-buloh": ["kota-damansara", "kuang", "kundang", "valencia", "sierra-mas", "subang-bestari"],
    "taman-tun-dr-ismail": ["damansara", "damansara-heights", "mont-kiara", "sri-hartamas", "petaling-jaya", "bandar-menjalara"],
    "usj": ["subang-jaya", "bandar-sunway", "puchong", "putra-heights", "shah-alam", "glenmarie"],
    "wangsa-maju": ["setapak", "setiawangsa", "keramat", "taman-melawati", "ulu-klang", "gombak"],
}

# 3. 地区场景差异化文案（降低 154 页内容重复度，贴合本地搜索意图）
AREA_ANGLES = [
    (
        "commercial",
        "Whether you run a retail shoplot, F&amp;B outlet, or showroom in {area_name}, a jammed or faulty roller shutter disrupts daily operations. We handle new installations, spring/slat repairs, and motor upgrades cleanly and promptly."
    ),
    (
        "industrial",
        "Warehouses, workshops, and industrial lots around {area_name} rely on durable shutters and smooth motor operation. Our technicians inspect alignment, springs, tracks, and control units to get heavy shutters moving reliably again."
    ),
    (
        "mixed",
        "From shopfronts and garages to commercial units in {area_name}, we provide straightforward pricing starting from {price_from}, urgent breakdown repairs, and reliable automated shutter motor solutions across Selangor &amp; KL."
    )
]

region_lookup = {slug: name for slug, name in regions_data}


def get_area_body_copy(slug, area_name):
    idx = sum(ord(ch) for ch in slug) % len(AREA_ANGLES)
    _, template_str = AREA_ANGLES[idx]
    return template_str.format(area_name=area_name, price_from=PRICE_FROM)


def build_nearby_html(current_slug, max_items=6):
    selected_slugs = []
    for candidate in nearby_map.get(current_slug, []):
        if candidate != current_slug and candidate in region_lookup and candidate not in selected_slugs:
            selected_slugs.append(candidate)
        if len(selected_slugs) == max_items:
            break

    if len(selected_slugs) < max_items:
        all_slugs = [s for s, _ in regions_data if s != current_slug]
        start_idx = next((i for i, (s, _) in enumerate(regions_data) if s == current_slug), 0)
        ordered = all_slugs[start_idx:] + all_slugs[:start_idx]
        for s in ordered:
            if s not in selected_slugs:
                selected_slugs.append(s)
            if len(selected_slugs) == max_items:
                break

    cards = [
        f'    <div class="col"><a href="{DOMAIN}/{s}/" class="btn btn-sm btn-outline-secondary w-100 text-truncate">{region_lookup[s]}</a></div>'
        for s in selected_slugs
    ]
    return "\n".join(cards), len(selected_slugs)


def json_escape(text):
    return text.replace("\\", "\\\\").replace('"', '\\"').replace("\n", " ")


# 生成根目录的 favicon.svg 文件（确保 Googlebot 能抓取到独立图标文件）
FAVICON_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <rect width="100" height="100" rx="20" fill="#d97706"/>
  <text x="50%" y="54%" font-family="Arial, sans-serif" font-size="56" font-weight="bold" fill="white" text-anchor="middle" dominant-baseline="middle">H</text>
</svg>
"""
with open("favicon.svg", "w", encoding="utf-8") as f:
    f.write(FAVICON_SVG)


# 4. 通用页面模板（不含 FAQ 模块，聚焦核心服务与高转化询盘）
PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <meta name="description" content="{description}">
    <link rel="canonical" href="{canonical_url}" />

    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{description}">
    <meta property="og:url" content="{canonical_url}">
    <meta property="og:type" content="website">

    <link rel="icon" href="{domain}/favicon.svg" type="image/svg+xml">
    <link rel="icon" href="{domain}/favicon.png" sizes="96x96" type="image/png">
    <link rel="shortcut icon" href="{domain}/favicon.ico">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">

    <script type="application/ld+json">
    [
      {{
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
          {{
            "@type": "ListItem",
            "position": 1,
            "name": "Home",
            "item": "{domain}/"
          }}{breadcrumb_second}
        ]
      }},
      {{
        "@context": "https://schema.org",
        "@type": "LocalBusiness",
        "name": "{brand_name} - {area_name}",
        "telephone": "+{wa_number}",
        "priceRange": "From {price_from}",
        "address": {{
          "@type": "PostalAddress",
          "addressLocality": "{area_name}",
          "addressRegion": "Selangor & Kuala Lumpur",
          "addressCountry": "MY"
        }},
        "url": "{canonical_url}"
      }}
    ]
    </script>

    <style>
        :root {{ --primary-color: #d97706; --primary-hover: #b45309; --dark-color: #1e293b; }}
        body {{ font-family: 'Segoe UI', system-ui, -apple-system, sans-serif; background-color: #f8fafc; color: #334155; padding-bottom: 70px; }}
        @media (min-width: 768px) {{ body {{ padding-bottom: 0; }} }}
        .top-bar {{ background-color: #0f172a; color: #94a3b8; font-size: 0.875rem; }}
        .hero-section {{ background: linear-gradient(rgba(15, 23, 42, 0.85), rgba(15, 23, 42, 0.85)), url('{img_prefix}photo1.jpg'); background-size: cover; background-position: center; color: white; padding: 90px 0; }}
        .hero-badge {{ background-color: rgba(217, 119, 6, 0.2); color: #fbbf24; border: 1px solid rgba(251, 191, 36, 0.3); border-radius: 50px; padding: 6px 16px; font-size: 0.875rem; font-weight: 600; display: inline-block; }}
        .btn-whatsapp {{ background-color: #25D366; color: white; font-weight: 700; border-radius: 50px; padding: 12px 30px; box-shadow: 0 4px 14px rgba(37, 211, 102, 0.4); transition: all 0.2s ease; }}
        .btn-whatsapp:hover {{ background-color: #1da851; color: white; transform: translateY(-2px); }}
        .btn-phone {{ background-color: var(--primary-color); color: white; font-weight: 700; border-radius: 50px; padding: 12px 30px; box-shadow: 0 4px 14px rgba(217, 119, 6, 0.4); transition: all 0.2s ease; }}
        .btn-phone:hover {{ background-color: var(--primary-hover); color: white; transform: translateY(-2px); }}
        .mobile-bottom-bar {{ position: fixed; bottom: 0; left: 0; right: 0; z-index: 9999; background: #ffffff; border-top: 1px solid #e2e8f0; padding: 10px 15px; box-shadow: 0 -4px 12px rgba(0,0,0,0.1); }}
    </style>
</head>
<body>
    <div class="top-bar py-2 px-3 d-none d-md-block">
        <div class="container d-flex justify-content-between align-items-center">
            <span><i class="fas fa-map-marker-alt text-warning me-2"></i>Serving {area_name}, Selangor &amp; Kuala Lumpur</span>
            <span><i class="fas fa-phone-alt text-warning me-2"></i> Call Direct: <a href="tel:{phone_tel}" class="text-white text-decoration-none fw-bold">{phone_display}</a></span>
        </div>
    </div>

    <nav class="navbar navbar-expand-lg navbar-light bg-white shadow-sm py-3 sticky-top">
        <div class="container">
            <a class="navbar-brand fw-bold text-dark" href="{domain}/">
                <i class="fas fa-store text-warning me-2"></i> {brand_name} | {area_name}
            </a>
            <div>
                <a href="{domain}/" class="btn btn-outline-secondary btn-sm rounded-pill px-3 me-2">Home</a>
                <a href="https://wa.me/{wa_number}?text={wa_text}" class="btn btn-success btn-sm rounded-pill px-3"><i class="fab fa-whatsapp me-1"></i> WhatsApp</a>
            </div>
        </div>
    </nav>

    <header class="hero-section text-center">
        <div class="container">
            <span class="hero-badge mb-3"><i class="fas fa-map-marker-alt me-1"></i> {area_name} Specialist</span>
            <h1 class="display-4 fw-bold mb-4">{h1_text}</h1>
            <div class="mb-3"><span class="badge bg-warning text-dark fs-6 px-3 py-2 rounded-pill fw-bold"><i class="fas fa-tag me-1"></i> Installation Rate from {price_from}</span></div>
            <p class="lead col-lg-8 mx-auto mb-5 text-light">
                Professional roller shutter installation, automated motor repairs, and urgent repair for commercial shoplots, factories, and residential properties in <strong>{area_name}</strong>.
            </p>
            <div class="d-flex justify-content-center gap-3 flex-wrap">
                <a href="https://wa.me/{wa_number}?text={wa_text}" class="btn btn-whatsapp btn-lg">
                    <i class="fab fa-whatsapp me-2"></i> WhatsApp for Fast Quote
                </a>
                <a href="tel:{phone_tel}" class="btn btn-phone btn-lg">
                    <i class="fas fa-phone-alt me-2"></i> Call: {phone_display}
                </a>
            </div>
        </div>
    </header>

    <main class="py-5">
        <div class="container">
            <div class="row align-items-center g-5">
                <div class="col-lg-6">
                    <div class="row g-3 mb-4">
                        <div class="col-6">
                            <img src="{img_prefix}photo1.jpg" loading="lazy" alt="Roller Shutter Installation in {area_name}" class="img-fluid rounded-3 shadow-sm" style="height: 180px; object-fit: cover; width: 100%;">
                        </div>
                        <div class="col-6">
                            <img src="{img_prefix}photo2.jpg" loading="lazy" alt="Automated Roller Shutter Repair Service in {area_name}" class="img-fluid rounded-3 shadow-sm" style="height: 180px; object-fit: cover; width: 100%;">
                        </div>
                    </div>

                    <h2 class="fw-bold mb-3">Reliable Shutter Services in {area_name}</h2>
                    <p class="mb-4">{area_body_copy}</p>

                    <div class="p-4 bg-white rounded-4 shadow-sm border-start border-warning border-4 mb-4">
                        <p class="fw-bold mb-2 text-dark"><i class="fas fa-tools text-warning me-2"></i>Our Shutter Solutions in {area_name}:</p>
                        <ul class="list-unstyled mb-0 text-secondary">
                            <li class="mb-2"><i class="fas fa-check text-warning me-2"></i> Heavy-Duty Industrial &amp; Commercial Roller Shutters</li>
                            <li class="mb-2"><i class="fas fa-check text-warning me-2"></i> Urgent Roller Shutter Repair, Spring &amp; Slat Replacement</li>
                            <li class="mb-2"><i class="fas fa-check text-warning me-2"></i> Automated Motor &amp; Remote Control Setup</li>
                            <li class="mb-0"><i class="fas fa-check text-warning me-2"></i> New Roller Shutter Supply &amp; Install (From {price_from})</li>
                        </ul>
                    </div>
                </div>

                <div class="col-lg-6">
                    <div class="bg-white p-5 rounded-4 shadow-sm border text-center">
                        <span class="badge bg-warning text-dark fw-bold mb-2 px-3 py-2 rounded-pill">Fast On-Site Response</span>
                        <h3 class="fw-bold mb-3">Get a Quote or Fix in {area_name}</h3>
                        <p class="text-muted mb-3">Snap a photo of your shutter or share approximate width &times; height on WhatsApp—no complicated steps.</p>
                        <div class="text-start bg-light rounded-3 p-3 mb-4 small text-secondary">
                            <div class="mb-1"><i class="fas fa-check-circle text-success me-2"></i><strong>New Installation:</strong> Share rough size &amp; location</div>
                            <div class="mb-1"><i class="fas fa-check-circle text-success me-2"></i><strong>Jammed / Broken Spring:</strong> Snap a photo of the shutter</div>
                            <div><i class="fas fa-check-circle text-success me-2"></i><strong>Motor / Remote Issue:</strong> Tell us what happened</div>
                        </div>
                        <a href="https://wa.me/{wa_number}?text={wa_text}" class="btn btn-whatsapp btn-lg w-100 mb-3">
                            <i class="fab fa-whatsapp me-2"></i> Send Photo / Quote on WhatsApp
                        </a>
                        <a href="tel:{phone_tel}" class="btn btn-outline-dark btn-lg w-100 rounded-pill">
                            <i class="fas fa-phone-alt me-2"></i> Call {phone_display}
                        </a>
                    </div>
                </div>
            </div>
        </div>

        <section class="py-5 bg-light border-top mt-5">
            <div class="container text-center">
                <h4 class="fw-bold mb-3 text-dark"><i class="fas fa-map-marked-alt text-warning me-2"></i>{areas_heading}</h4>
                <p class="text-muted small mb-3">{areas_desc}</p>

                <button class="btn btn-warning fw-bold text-dark rounded-pill px-4" type="button" data-bs-toggle="collapse" data-bs-target="#allServicedAreas" aria-expanded="false" aria-controls="allServicedAreas">
                    {areas_button_text} ({total_count})
                </button>

                <div class="collapse mt-4" id="allServicedAreas">
                    <div class="row row-cols-2 row-cols-md-3 row-cols-lg-3 g-2 justify-content-center">
                        {areas_html}
                    </div>
                </div>
            </div>
        </section>
    </main>

    <footer class="bg-dark text-white py-4 text-center small">
        <div class="container">
            <p class="mb-1 text-light">Hotline: <a href="tel:{phone_tel}" class="text-warning text-decoration-none fw-bold">{phone_display}</a></p>
            <p class="mb-0 text-light opacity-75">&copy; 2026 {brand_name}. {area_name} Roller Shutter Specialist.</p>
        </div>
    </footer>

    <div class="mobile-bottom-bar d-md-none">
        <div class="row g-2">
            <div class="col-6">
                <a href="tel:{phone_tel}" class="btn btn-dark w-100 rounded-pill fw-bold py-2"><i class="fas fa-phone-alt me-1 text-warning"></i> Call Now</a>
            </div>
            <div class="col-6">
                <a href="https://wa.me/{wa_number}?text={wa_text}" class="btn btn-success w-100 rounded-pill fw-bold py-2"><i class="fab fa-whatsapp me-1"></i> WhatsApp</a>
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""

# 5. 拼装主页使用的全部地区卡片 HTML 矩阵
all_areas_html_list = [
    f'    <div class="col"><a href="{DOMAIN}/{s}/" class="btn btn-sm btn-outline-secondary w-100 text-truncate">{n}</a></div>'
    for s, n in regions_data
]
combined_all_
