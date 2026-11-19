import os
import urllib.parse

DOMAIN = "https://rollershutter.htkdecor.com.my"

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

# 2. 通用页面模板
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

    <link rel="icon" type="image/svg+xml" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><circle cx='50' cy='50' r='50' fill='%23d97706'/><text x='50%' y='58%' font-size='38' font-weight='bold' fill='white' text-anchor='middle' dominant-baseline='middle'>HTK</text></svg>">
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
        "name": "HTK Pintu Shutter - {area_name}",
        "telephone": "+60174315233",
        "priceRange": "From RM 26.00 / ft²",
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
            <span><i class="fas fa-phone-alt text-warning me-2"></i> Call Direct: <a href="tel:0174315233" class="text-white text-decoration-none fw-bold">017-431 5233</a></span>
        </div>
    </div>

    <nav class="navbar navbar-expand-lg navbar-light bg-white shadow-sm py-3 sticky-top">
        <div class="container">
            <a class="navbar-brand fw-bold text-dark" href="{domain}/">
                <i class="fas fa-store text-warning me-2"></i> HTK Pintu Shutter | {area_name}
            </a>
            <div>
                <a href="{domain}/" class="btn btn-outline-secondary btn-sm rounded-pill px-3 me-2">Home</a>
                <a href="https://wa.me/60174315233?text={wa_text}" class="btn btn-success btn-sm rounded-pill px-3"><i class="fab fa-whatsapp me-1"></i> WhatsApp</a>
            </div>
        </div>
    </nav>

    <header class="hero-section text-center">
        <div class="container">
            <span class="hero-badge mb-3"><i class="fas fa-map-marker-alt me-1"></i> {area_name} Specialist</span>
            <h1 class="display-4 fw-bold mb-4">{h1_text}</h1>
            <div class="mb-3"><span class="badge bg-warning text-dark fs-6 px-3 py-2 rounded-pill fw-bold"><i class="fas fa-tag me-1"></i> Installation Rate from RM 26.00 / ft²</span></div>
            <p class="lead col-lg-8 mx-auto mb-5 text-light">
                Professional roller shutter installation, automated motor repairs, and urgent 24/7 maintenance tailored for commercial shoplots, factories, and residential properties in <strong>{area_name}</strong>.
            </p>
            <div class="d-flex justify-content-center gap-3 flex-wrap">
                <a href="https://wa.me/60174315233?text={wa_text}" class="btn btn-whatsapp btn-lg">
                    <i class="fab fa-whatsapp me-2"></i> WhatsApp for Quote
                </a>
                <a href="tel:0174315233" class="btn btn-phone btn-lg">
                    <i class="fas fa-phone-alt me-2"></i> Call: 017-431 5233
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

                    <h2 class="fw-bold mb-4">Reliable Shutter Services in {area_name}</h2>
                    <p class="mb-4">Operating a shoplot, warehouse, or factory in {area_name}? When your roller shutter jams or needs an automated motor upgrade, our technical team provides rapid on-site troubleshooting across Selangor &amp; KL.</p>

                    <div class="p-4 bg-white rounded-4 shadow-sm border-start border-warning border-4 mb-4">
                        <p class="fw-bold mb-2 text-dark"><i class="fas fa-tools text-warning me-2"></i>Our Shutter Solutions in {area_name}:</p>
                        <ul class="list-unstyled mb-0 text-secondary">
                            <li class="mb-2"><i class="fas fa-check text-warning me-2"></i> Heavy-Duty Industrial &amp; Commercial Roller Shutters</li>
                            <li class="mb-2"><i class="fas fa-check text-warning me-2"></i> Urgent Roller Shutter Repair, Spring &amp; Slat Replacement</li>
                            <li class="mb-2"><i class="fas fa-check text-warning me-2"></i> Automated Motor &amp; Remote Control Setup</li>
                            <li class="mb-0"><i class="fas fa-check text-warning me-2"></i> New Roller Shutter Supply &amp; Install (From RM 26.00 / ft²)</li>
                        </ul>
                    </div>
                </div>

                <div class="col-lg-6">
                    <div class="bg-white p-5 rounded-4 shadow-sm border text-center">
                        <span class="badge bg-warning text-dark fw-bold mb-2 px-3 py-2 rounded-pill">Fast On-Site Response</span>
                        <h3 class="fw-bold mb-3">Need Immediate Assistance?</h3>
                        <p class="text-muted mb-4">Send us your shutter dimensions or issue via WhatsApp for a fast quotation in {area_name}.</p>
                        <a href="https://wa.me/60174315233?text={wa_text}" class="btn btn-whatsapp btn-lg w-100 mb-3">
                            <i class="fab fa-whatsapp me-2"></i> Chat on WhatsApp Now
                        </a>
                        <a href="tel:0174315233" class="btn btn-outline-dark btn-lg w-100 rounded-pill">
                            <i class="fas fa-phone-alt me-2"></i> Call 017-431 5233
                        </a>
                    </div>
                </div>
            </div>
        </div>

        <!-- 折叠隐藏的雪隆地区链接矩阵 -->
        <section class="py-5 bg-light border-top mt-5">
            <div class="container text-center">
                <h4 class="fw-bold mb-3 text-dark"><i class="fas fa-map-marked-alt text-warning me-2"></i>Serviced Areas in Selangor &amp; Kuala Lumpur</h4>
                <p class="text-muted small mb-3">We provide professional roller shutter installation and urgent repair across all major districts and industrial parks in Klang Valley:</p>
                
                <button class="btn btn-warning fw-bold text-dark rounded-pill px-4" type="button" data-bs-toggle="collapse" data-bs-target="#allServicedAreas" aria-expanded="false" aria-controls="allServicedAreas">
                    Show All Serviced Areas (查看所有服务地区 - {total_count})
                </button>
                
                <div class="collapse mt-4" id="allServicedAreas">
                    <div class="row row-cols-2 row-cols-md-4 row-cols-lg-5 g-2">
                        {areas_html}
                    </div>
                </div>
            </div>
        </section>
    </main>

    <footer class="bg-dark text-white py-4 text-center small">
        <div class="container">
            <p class="mb-1 text-light">Hotline: <a href="tel:0174315233" class="text-warning text-decoration-none fw-bold">017-431 5233</a></p>
            <p class="mb-0 text-light opacity-75">&copy; 2026 HTK Pintu Shutter. {area_name} Roller Shutter Specialist.</p>
        </div>
    </footer>

    <div class="mobile-bottom-bar d-md-none">
        <div class="row g-2">
            <div class="col-6">
                <a href="tel:0174315233" class="btn btn-dark w-100 rounded-pill fw-bold py-2"><i class="fas fa-phone-alt me-1 text-warning"></i> Call Now</a>
            </div>
            <div class="col-6">
                <a href="https://wa.me/60174315233?text={wa_text}" class="btn btn-success w-100 rounded-pill fw-bold py-2"><i class="fab fa-whatsapp me-1"></i> WhatsApp</a>
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""

# 3. 拼装所有地区卡片的 HTML 矩阵
areas_html_list = [
    f'    <div class="col"><a href="{DOMAIN}/{s}/" class="btn btn-sm btn-outline-secondary w-100 text-truncate">{n}</a></div>'
    for s, n in regions_data
]
combined_areas_html = "\n".join(areas_html_list)
total_areas = len(regions_data)

# 4. 生成根目录主页 (index.html)
home_wa_text = urllib.parse.quote("Hi, I need roller shutter service in Selangor / KL")
home_html = PAGE_TEMPLATE.format(
    domain=DOMAIN,
    title="Roller Shutter Selangor & KL | 017-431 5233 CALL HTK Shutter",
    description="Professional roller shutter installation (from RM 26/ft²), urgent repair & automated motor services across Selangor & Kuala Lumpur. Fast response!",
    canonical_url=f"{DOMAIN}/",
    breadcrumb_second="",
    area_name="Selangor & KL",
    h1_text="Selangor & KL Roller Shutter 017-431 5233 CALL HTK",
    img_prefix="",
    wa_text=home_wa_text,
    total_count=total_areas,
    areas_html=combined_areas_html
)
with open("index.html", "w", encoding="utf-8") as f:
    f.write(home_html)

# 5. 循环生成各地区子页 & 收集 Sitemap URLs
sitemap_urls = [f"  <url><loc>{DOMAIN}/</loc></url>"]

for slug, name in regions_data:
    os.makedirs(slug, exist_ok=True)
    file_path = os.path.join(slug, "index.html")
    wa_text = urllib.parse.quote(f"Hi, I need roller shutter service in {name}")
    
    breadcrumb_item2 = f""",
          {{
            "@type": "ListItem",
            "position": 2,
            "name": "Roller Shutter {name}",
            "item": "{DOMAIN}/{slug}/"
          }}"""

    sub_html = PAGE_TEMPLATE.format(
        domain=DOMAIN,
        title=f"Roller Shutter {name} | 017-431 5233 CALL HTK Shutter",
        description=f"Professional roller shutter installation (from RM 26/ft²), urgent repair and automated motor services in {name}, Selangor & KL. Fast response!",
        canonical_url=f"{DOMAIN}/{slug}/",
        breadcrumb_second=breadcrumb_item2,
        area_name=name,
        h1_text=f"{name} Roller Shutter 017-431 5233 CALL HTK",
        img_prefix="../",
        wa_text=wa_text,
        total_count=total_areas,
        areas_html=combined_areas_html
    )

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(sub_html)

    sitemap_urls.append(f"  <url><loc>{DOMAIN}/{slug}/</loc></url>")

# 6. 自动生成精准无死链的 sitemap.xml
sitemap_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
sitemap_content += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
sitemap_content += "\n".join(sitemap_urls) + "\n"
sitemap_content += '</urlset>'

with open("sitemap.xml", "w", encoding="utf-8") as f:
    f.write(sitemap_content)

print(f"成功生成主页、{total_areas} 个雪隆区子页面，以及对应的 sitemap.xml！")
