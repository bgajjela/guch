
from pathlib import Path
from urllib.parse import quote_plus
from html import escape
import math
import re

import folium
from folium.plugins import MarkerCluster
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
from streamlit_folium import st_folium


# ============================================================
# App config
# ============================================================
st.set_page_config(
    page_title="PhillyEats",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

APP_DIR = Path(__file__).parent
CSV_PATH = APP_DIR / "philadelphia_restaurants.csv"

CUISINE_ICONS = {
    "Italian": "🍝",
    "Chinese": "🥡",
    "Mexican": "🌮",
    "Japanese": "🍣",
    "Indian": "🍛",
    "Sushi": "🍣",
    "American": "🍔",
    "Vegan": "🌱",
    "Vegetarian": "🥗",
    "Halal": "🥙",
    "Seafood": "🦞",
    "Mediterranean": "🫒",
    "Middle Eastern": "🧆",
    "Thai": "🍜",
    "Korean": "🥘",
    "Vietnamese": "🍜",
    "Ramen": "🍜",
    "Pizza": "🍕",
    "Brunch": "🥞",
    "Cafe": "☕",
    "Breakfast": "🍳",
    "Bakery": "🥐",
    "Bar": "🍸",
    "Restaurant": "🍽️",
}

QUICK_FILTERS = [
    ("Top rated", "⭐"),
    ("Most reviewed", "🔥"),
    ("Vegan", "🌱"),
    ("Halal", "🥙"),
    ("Italian", "🍝"),
    ("Sushi", "🍣"),
    ("Mexican", "🌮"),
    ("Indian", "🍛"),
]


# ============================================================
# Styling
# ============================================================
st.markdown(
    """
    <style>
      :root {
        --pe-bg: #fbfbfa;
        --pe-card: #ffffff;
        --pe-text: #171717;
        --pe-muted: #6b6b6b;
        --pe-border: rgba(23,23,23,.10);
        --pe-soft: rgba(23,23,23,.045);
      }

      .stApp {
        background: var(--pe-bg);
      }

      .block-container {
        max-width: 1320px;
        padding-top: 1.6rem;
        padding-bottom: 3rem;
      }

      /* Keep Streamlit chrome from covering the product navigation. */
      [data-testid="stHeader"],
      [data-testid="stToolbar"],
      [data-testid="stDecoration"] {
        display: none !important;
      }

      .pe-brand {
        font-size: 1.45rem;
        line-height: 1;
        font-weight: 850;
        letter-spacing: -.035em;
        color: var(--pe-text);
        margin: .15rem 0 .25rem 0;
      }

      .pe-kicker {
        font-size: .83rem;
        color: var(--pe-muted);
        margin-bottom: .1rem;
      }

      .pe-hero {
        padding: 1.45rem 1.55rem;
        border: 1px solid var(--pe-border);
        border-radius: 24px;
        background:
          radial-gradient(circle at 85% 20%, rgba(255,255,255,.95), transparent 30%),
          linear-gradient(135deg, rgba(245,238,226,.95), rgba(239,244,238,.95));
        margin: .35rem 0 1.1rem 0;
      }

      .pe-hero-title {
        font-size: clamp(1.8rem, 4vw, 3rem);
        font-weight: 850;
        letter-spacing: -.045em;
        line-height: 1.03;
        margin: 0 0 .45rem 0;
        color: var(--pe-text);
      }

      .pe-hero-copy {
        max-width: 720px;
        color: var(--pe-muted);
        font-size: 1rem;
        line-height: 1.55;
      }

      .pe-section-title {
        font-size: 1.28rem;
        font-weight: 800;
        letter-spacing: -.025em;
        margin: .25rem 0 .15rem 0;
      }

      .pe-section-copy {
        color: var(--pe-muted);
        font-size: .9rem;
        margin-bottom: .65rem;
      }

      .pe-card {
        border: 1px solid var(--pe-border);
        border-radius: 20px;
        background: var(--pe-card);
        overflow: hidden;
        margin-bottom: .55rem;
      }

      .pe-card-cover {
        min-height: 105px;
        padding: 1.05rem;
        display: flex;
        align-items: flex-end;
        justify-content: space-between;
        background:
          radial-gradient(circle at 90% 20%, rgba(255,255,255,.9), transparent 28%),
          linear-gradient(135deg, rgba(246,241,232,.95), rgba(237,242,240,.95));
      }

      .pe-card-icon {
        font-size: 2.5rem;
        line-height: 1;
        filter: saturate(.92);
      }

      .pe-card-body {
        padding: .92rem 1rem .8rem 1rem;
      }

      .pe-card-name {
        font-size: 1.04rem;
        font-weight: 800;
        letter-spacing: -.018em;
        line-height: 1.2;
        color: var(--pe-text);
        margin-bottom: .24rem;
      }

      .pe-meta {
        color: var(--pe-muted);
        font-size: .86rem;
        line-height: 1.45;
      }

      .pe-badge {
        display: inline-block;
        border: 1px solid var(--pe-border);
        background: rgba(255,255,255,.88);
        border-radius: 999px;
        padding: .22rem .48rem;
        font-size: .76rem;
        font-weight: 700;
        margin: .12rem .16rem .05rem 0;
      }

      .pe-rating {
        display: inline-block;
        border-radius: 999px;
        background: #171717;
        color: white;
        padding: .27rem .5rem;
        font-size: .78rem;
        font-weight: 800;
      }

      .pe-detail {
        border: 1px solid var(--pe-border);
        background: white;
        border-radius: 22px;
        padding: 1.15rem;
        margin-bottom: .8rem;
      }

      .pe-detail-name {
        font-size: 1.55rem;
        font-weight: 850;
        letter-spacing: -.035em;
        line-height: 1.08;
        margin-bottom: .3rem;
      }

      .pe-detail-address {
        color: var(--pe-muted);
        font-size: .9rem;
        margin-top: .3rem;
      }

      .pe-empty {
        border: 1px dashed rgba(23,23,23,.18);
        border-radius: 20px;
        padding: 2rem 1.25rem;
        text-align: center;
        background: rgba(255,255,255,.6);
      }

      .pe-map-note {
        font-size: .82rem;
        color: var(--pe-muted);
        margin: .2rem 0 .5rem 0;
      }

      div[data-testid="stButton"] button,
      div[data-testid="stLinkButton"] a {
        border-radius: 999px !important;
        font-weight: 700 !important;
        min-height: 42px;
      }

      div[data-testid="stButton"] button[kind="primary"] {
        color: #ffffff !important;
        box-shadow: none !important;
      }

      div[data-testid="stButton"] button[kind="secondary"] {
        color: #171717 !important;
        background: #ffffff !important;
        border-color: rgba(23,23,23,.15) !important;
      }

      div[data-testid="stButton"] button p {
        color: inherit !important;
        opacity: 1 !important;
      }

      div[data-testid="stTextInput"] input {
        border-radius: 14px;
        min-height: 48px;
      }

      div[data-testid="stSelectbox"] [data-baseweb="select"] > div,
      div[data-testid="stMultiSelect"] [data-baseweb="select"] > div {
        border-radius: 13px;
      }

      div[data-testid="stExpander"] {
        border: 1px solid var(--pe-border);
        border-radius: 16px;
        background: white;
      }

      [data-testid="stMetric"] {
        background: var(--pe-soft);
        border: 1px solid var(--pe-border);
        border-radius: 15px;
        padding: .65rem .8rem;
      }

      @media (max-width: 700px) {
        .block-container {
          padding-left: .8rem;
          padding-right: .8rem;
        }
        .pe-hero {
          padding: 1.15rem;
        }
        .pe-card-cover {
          min-height: 88px;
        }
      }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# Data
# ============================================================
@st.cache_data(show_spinner=False)
def load_data():
    df = pd.read_csv(CSV_PATH)

    for col in ["rating", "review_count", "latitude", "longitude"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    text_cols = [
        "place_id", "data_id", "name", "price", "type", "types",
        "address", "phone", "website", "labels", "search_neighborhoods"
    ]
    for col in text_cols:
        if col not in df.columns:
            df[col] = ""
        df[col] = df[col].fillna("").astype(str)

    df = df.dropna(subset=["latitude", "longitude"]).copy()
    df = df[
        df["latitude"].between(-90, 90)
        & df["longitude"].between(-180, 180)
    ].copy()

    df["_row_id"] = range(len(df))

    df["search_blob"] = (
        df["name"] + " " + df["type"] + " " + df["types"] + " "
        + df["labels"] + " " + df["address"] + " "
        + df["search_neighborhoods"]
    ).str.lower()

    df["recommended_score"] = (
        df["rating"].fillna(0) * 3.4
        + df["review_count"].fillna(0).clip(lower=0).apply(math.log1p)
    )

    return df


df = load_data()


# ============================================================
# Helpers
# ============================================================
def safe_site(url):
    url = str(url or "").strip()
    if not url:
        return None
    if url.startswith(("http://", "https://")):
        return url
    return "https://" + url


def google_maps_url(row):
    q = f"{row.get('name','')} {row.get('address','')}".strip()
    if not q:
        q = f"{row['latitude']},{row['longitude']}"
    return "https://www.google.com/maps/search/?api=1&query=" + quote_plus(q)


def clean_neighborhood(value):
    if not value:
        return ""
    first = str(value).split(",")[0].strip()
    first = re.sub(r"\s+Philadelphia\s+PA$", "", first, flags=re.I)
    return first


def primary_cuisine(row):
    haystack = f"{row.get('types','')} {row.get('type','')} {row.get('labels','')}".lower()

    checks = [
        ("Italian", ["italian"]),
        ("Chinese", ["chinese"]),
        ("Mexican", ["mexican", "taco"]),
        ("Japanese", ["japanese"]),
        ("Sushi", ["sushi"]),
        ("Indian", ["indian"]),
        ("American", ["american"]),
        ("Vegan", ["vegan"]),
        ("Vegetarian", ["vegetarian"]),
        ("Halal", ["halal"]),
        ("Seafood", ["seafood"]),
        ("Mediterranean", ["mediterranean"]),
        ("Middle Eastern", ["middle eastern"]),
        ("Thai", ["thai"]),
        ("Korean", ["korean"]),
        ("Vietnamese", ["vietnamese"]),
        ("Ramen", ["ramen"]),
        ("Pizza", ["pizza"]),
        ("Brunch", ["brunch"]),
        ("Breakfast", ["breakfast"]),
        ("Bakery", ["bakery"]),
        ("Cafe", ["cafe", "coffee"]),
        ("Bar", ["bar", "pub"]),
    ]

    for label, needles in checks:
        if any(n in haystack for n in needles):
            return label

    typ = str(row.get("type") or "").replace(" restaurant", "").strip()
    return typ.title() if typ and typ.lower() != "restaurant" else "Restaurant"


def cuisine_icon(row):
    cuisine = primary_cuisine(row)
    return CUISINE_ICONS.get(cuisine, "🍽️")


def rating_text(value):
    return "New" if pd.isna(value) else f"{float(value):.1f}"


def review_text(value):
    if pd.isna(value):
        return "No review count"
    n = int(value)
    if n >= 1000:
        return f"{n/1000:.1f}k reviews"
    return f"{n:,} reviews"


def restaurant_tags(row, max_tags=3):
    tags = []
    cuisine = primary_cuisine(row)
    if cuisine and cuisine != "Restaurant":
        tags.append(cuisine)

    labels = [
        x.strip()
        for x in str(row.get("labels") or "").split(",")
        if x.strip() and x.strip().lower() != "restaurants"
    ]

    pretty = {
        "vegan restaurants": "Vegan",
        "vegetarian restaurants": "Vegetarian",
        "halal restaurants": "Halal",
        "gluten free restaurants": "Gluten-free",
        "italian restaurants": "Italian",
        "chinese restaurants": "Chinese",
        "mexican restaurants": "Mexican",
        "japanese restaurants": "Japanese",
        "indian restaurants": "Indian",
    }

    for item in labels:
        label = pretty.get(item.lower(), item.title())
        if label not in tags:
            tags.append(label)

    return tags[:max_tags]


def card_html(row):
    name = escape(str(row.get("name") or "Restaurant"))
    cuisine = escape(primary_cuisine(row))
    icon = cuisine_icon(row)
    rating = rating_text(row.get("rating"))
    reviews = escape(review_text(row.get("review_count")))
    price = escape(str(row.get("price") or ""))
    hood = escape(clean_neighborhood(row.get("search_neighborhoods")))
    address = escape(str(row.get("address") or ""))
    tags = restaurant_tags(row, 3)
    badges = "".join(f'<span class="pe-badge">{escape(t)}</span>' for t in tags)
    secondary = " · ".join(x for x in [cuisine, price, hood] if x)

    return f"""
    <div class="pe-card">
      <div class="pe-card-cover">
        <div class="pe-card-icon">{icon}</div>
        <div class="pe-rating">★ {rating}</div>
      </div>
      <div class="pe-card-body">
        <div class="pe-card-name">{name}</div>
        <div class="pe-meta">{secondary}</div>
        <div class="pe-meta" style="margin-top:.12rem;">{reviews}</div>
        <div style="margin-top:.38rem;">{badges}</div>
        <div class="pe-meta" style="margin-top:.4rem;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">📍 {address}</div>
      </div>
    </div>
    """


def set_selected(row_id):
    st.session_state["selected_id"] = int(row_id)


def toggle_saved(row_id):
    saved = st.session_state.setdefault("saved_ids", set())
    row_id = int(row_id)
    if row_id in saved:
        saved.remove(row_id)
    else:
        saved.add(row_id)



@st.dialog("Restaurant details", width="large", icon="🍽️")
def restaurant_dialog(row_id):
    match = df[df["_row_id"] == int(row_id)]
    if match.empty:
        st.error("Restaurant not found.")
        return

    row = match.iloc[0]
    rid = int(row["_row_id"])

    name_raw = str(row.get("name") or "Restaurant")
    cuisine_raw = primary_cuisine(row)
    icon = cuisine_icon(row)
    price_raw = str(row.get("price") or "")
    hood_raw = clean_neighborhood(row.get("search_neighborhoods"))
    address_raw = str(row.get("address") or "")
    phone_raw = str(row.get("phone") or "")
    rating_raw = rating_text(row.get("rating"))
    reviews_raw = review_text(row.get("review_count"))
    lat = float(row["latitude"])
    lon = float(row["longitude"])

    tags = restaurant_tags(row, 6)

    name = escape(name_raw)
    cuisine = escape(cuisine_raw)
    price = escape(price_raw)
    hood = escape(hood_raw)
    address = escape(address_raw)
    phone = escape(phone_raw)
    rating = escape(rating_raw)
    reviews = escape(reviews_raw)
    tag_html = "".join(
        f'<span class="tag">{escape(t)}</span>' for t in tags
    )

    maps_url = escape(google_maps_url(row), quote=True)
    website_raw = safe_site(row.get("website"))
    website = escape(website_raw, quote=True) if website_raw else ""

    meta_parts = [x for x in [cuisine, price, hood] if x]
    meta_line = " · ".join(meta_parts)

    website_button = (
        f'<a class="action secondary" href="{website}" target="_blank" rel="noopener">Website</a>'
        if website
        else '<span class="action secondary disabled">No website</span>'
    )

    # One HTML component owns the entire restaurant sheet. This avoids
    # Streamlit's responsive columns moving the map below the details.
    sheet = f"""
    <!doctype html>
    <html>
      <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link
          rel="stylesheet"
          href="https://cdn.jsdelivr.net/npm/leaflet@1.9.4/dist/leaflet.css"
        >
        <style>
          * {{ box-sizing: border-box; }}
          html, body {{
            margin: 0;
            padding: 0;
            background: transparent;
            color: #171717;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
          }}
          .sheet {{
            display: grid;
            grid-template-columns: minmax(225px, .82fr) minmax(355px, 1.38fr);
            gap: 18px;
            width: 100%;
            align-items: stretch;
          }}
          .info {{
            min-width: 0;
            padding: 8px 2px 4px 2px;
          }}
          .icon {{
            font-size: 43px;
            line-height: 1;
            margin: 0 0 12px 0;
          }}
          h1 {{
            font-size: 27px;
            line-height: 1.08;
            letter-spacing: -.035em;
            margin: 0 0 7px 0;
            overflow-wrap: anywhere;
          }}
          .meta {{
            color: #686868;
            font-size: 14px;
            line-height: 1.45;
          }}
          .rating-row {{
            display: flex;
            align-items: center;
            flex-wrap: wrap;
            gap: 8px;
            margin: 13px 0 10px 0;
          }}
          .rating {{
            display: inline-block;
            padding: 5px 9px;
            border-radius: 999px;
            background: #171717;
            color: #fff;
            font-weight: 800;
            font-size: 13px;
          }}
          .tags {{
            margin: 7px 0 12px 0;
          }}
          .tag {{
            display: inline-block;
            padding: 4px 8px;
            margin: 2px 4px 2px 0;
            border: 1px solid rgba(23,23,23,.13);
            border-radius: 999px;
            font-size: 12px;
            font-weight: 650;
            background: #fff;
          }}
          .line {{
            color: #4e4e4e;
            font-size: 13px;
            line-height: 1.45;
            margin: 6px 0;
            overflow-wrap: anywhere;
          }}
          .actions {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 8px;
            margin-top: 14px;
          }}
          .action {{
            min-height: 42px;
            display: flex;
            align-items: center;
            justify-content: center;
            text-decoration: none;
            border-radius: 999px;
            font-size: 13px;
            font-weight: 750;
          }}
          .primary {{
            background: #171717;
            color: white;
          }}
          .secondary {{
            border: 1px solid rgba(23,23,23,.16);
            color: #171717;
            background: white;
          }}
          .disabled {{
            color: #999;
            background: #f6f6f6;
          }}
          .map-panel {{
            min-width: 0;
            border: 1px solid rgba(23,23,23,.10);
            background: #f2f2f0;
            border-radius: 18px;
            overflow: hidden;
            position: relative;
          }}
          #restaurant-map {{
            width: 100%;
            height: 405px;
            min-height: 405px;
          }}
          .map-label {{
            position: absolute;
            z-index: 1000;
            left: 12px;
            top: 12px;
            max-width: calc(100% - 24px);
            padding: 7px 10px;
            border-radius: 10px;
            background: rgba(255,255,255,.94);
            box-shadow: 0 1px 8px rgba(0,0,0,.12);
            font-size: 12px;
            font-weight: 700;
          }}
          @media (max-width: 620px) {{
            .sheet {{
              grid-template-columns: minmax(190px, .8fr) minmax(270px, 1.2fr);
              gap: 10px;
            }}
            #restaurant-map {{
              height: 380px;
              min-height: 380px;
            }}
            h1 {{ font-size: 22px; }}
            .icon {{ font-size: 36px; }}
          }}
        </style>
      </head>
      <body>
        <div class="sheet">
          <section class="info">
            <div class="icon">{icon}</div>
            <h1>{name}</h1>
            <div class="meta">{meta_line}</div>

            <div class="rating-row">
              <span class="rating">★ {rating}</span>
              <span class="meta">{reviews}</span>
            </div>

            <div class="tags">{tag_html}</div>

            <div class="line">📍 {address}</div>
            {f'<div class="line">☎ {phone}</div>' if phone else ''}

            <div class="actions">
              <a class="action primary" href="{maps_url}" target="_blank" rel="noopener">Directions</a>
              {website_button}
            </div>
          </section>

          <section class="map-panel">
            <div class="map-label">{name}</div>
            <div id="restaurant-map" aria-label="Map showing {name}"></div>
          </section>
        </div>

        <script src="https://cdn.jsdelivr.net/npm/leaflet@1.9.4/dist/leaflet.js"></script>
        <script>
          (function () {{
            const lat = {lat:.8f};
            const lon = {lon:.8f};

            const map = L.map("restaurant-map", {{
              zoomControl: true,
              scrollWheelZoom: true
            }}).setView([lat, lon], 16);

            L.tileLayer(
              "https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png",
              {{
                maxZoom: 19,
                attribution: "&copy; OpenStreetMap contributors"
              }}
            ).addTo(map);

            L.circleMarker([lat, lon], {{
              radius: 9,
              color: "#ffffff",
              weight: 3,
              fillColor: "#171717",
              fillOpacity: 1
            }}).addTo(map)
              .bindPopup({name_raw!r})
              .openPopup();

            setTimeout(function () {{
              map.invalidateSize();
            }}, 150);
          }})();
        </script>
      </body>
    </html>
    """

    components.html(
        sheet,
        height=435,
        scrolling=False,
    )

    saved = st.session_state.setdefault("saved_ids", set())
    is_saved = rid in saved

    if st.button(
        "♥ Saved" if is_saved else "♡ Save restaurant",
        key=f"dialog_save_{rid}",
        use_container_width=True,
    ):
        toggle_saved(rid)
        st.toast("Removed from saved" if is_saved else "Restaurant saved")



def render_actions(row, prefix):
    rid = int(row["_row_id"])
    saved = st.session_state.setdefault("saved_ids", set())
    is_saved = rid in saved

    a, b = st.columns([1, 1])
    if a.button(
        "♥ Saved" if is_saved else "♡ Save",
        key=f"{prefix}_save_{rid}",
        use_container_width=True,
    ):
        toggle_saved(rid)
        st.rerun()

    if b.button(
        "View",
        key=f"{prefix}_view_{rid}",
        use_container_width=True,
        type="primary",
    ):
        set_selected(rid)
        restaurant_dialog(rid)


def render_detail(row, prefix="detail"):
    rid = int(row["_row_id"])
    name = escape(str(row.get("name") or "Restaurant"))
    cuisine = escape(primary_cuisine(row))
    icon = cuisine_icon(row)
    price = escape(str(row.get("price") or ""))
    hood = escape(clean_neighborhood(row.get("search_neighborhoods")))
    address = escape(str(row.get("address") or ""))
    phone = escape(str(row.get("phone") or ""))
    rating = rating_text(row.get("rating"))
    reviews = escape(review_text(row.get("review_count")))
    tags = restaurant_tags(row, 6)
    tag_html = "".join(f'<span class="pe-badge">{escape(t)}</span>' for t in tags)

    st.markdown(
        f"""
        <div class="pe-detail">
          <div style="font-size:2.6rem;line-height:1;margin-bottom:.7rem;">{icon}</div>
          <div class="pe-detail-name">{name}</div>
          <div class="pe-meta">{cuisine}{(" · " + price) if price else ""}{(" · " + hood) if hood else ""}</div>
          <div style="margin:.65rem 0 .45rem 0;">
            <span class="pe-rating">★ {rating}</span>
            <span class="pe-meta" style="margin-left:.45rem;">{reviews}</span>
          </div>
          <div>{tag_html}</div>
          <div class="pe-detail-address">📍 {address}</div>
          {f'<div class="pe-detail-address">☎ {phone}</div>' if phone else ''}
        </div>
        """,
        unsafe_allow_html=True,
    )

    website = safe_site(row.get("website"))
    c1, c2 = st.columns(2)
    c1.link_button(
        "Directions",
        google_maps_url(row),
        key=f"{prefix}_maps_{rid}",
        use_container_width=True,
        type="primary",
    )
    if website:
        c2.link_button(
            "Website",
            website,
            key=f"{prefix}_site_{rid}",
            use_container_width=True,
        )
    else:
        c2.button(
            "No website",
            key=f"{prefix}_nosite_{rid}",
            disabled=True,
            use_container_width=True,
        )

    saved = st.session_state.setdefault("saved_ids", set())
    if st.button(
        "Remove from saved" if rid in saved else "Save restaurant",
        key=f"{prefix}_save_{rid}",
        use_container_width=True,
    ):
        toggle_saved(rid)
        st.rerun()


def nearest_restaurant(dataframe, lat, lon):
    if lat is None or lon is None or dataframe.empty:
        return None

    lat0 = math.radians(float(lat))
    lon0 = math.radians(float(lon))

    def distance(row):
        lat1 = math.radians(float(row["latitude"]))
        lon1 = math.radians(float(row["longitude"]))
        dlat = lat1 - lat0
        dlon = lon1 - lon0
        a = (
            math.sin(dlat / 2) ** 2
            + math.cos(lat0) * math.cos(lat1) * math.sin(dlon / 2) ** 2
        )
        return 2 * 6371 * math.asin(min(1, math.sqrt(a)))

    d = dataframe.apply(distance, axis=1)
    idx = d.idxmin()
    return dataframe.loc[idx] if float(d.loc[idx]) <= 0.08 else None


def build_map(dataframe, zoom_start=11):
    center = [
        float(dataframe["latitude"].median()),
        float(dataframe["longitude"].median()),
    ]

    m = folium.Map(
        location=center,
        zoom_start=zoom_start,
        tiles="OpenStreetMap",
        control_scale=True,
        prefer_canvas=True,
    )

    cluster = MarkerCluster(
        options={
            "showCoverageOnHover": False,
            "spiderfyOnMaxZoom": True,
            "disableClusteringAtZoom": 16,
        }
    ).add_to(m)

    for _, row in dataframe.iterrows():
        rating = row.get("rating")
        if pd.isna(rating):
            color = "gray"
        elif float(rating) >= 4.7:
            color = "darkgreen"
        elif float(rating) >= 4.4:
            color = "green"
        else:
            color = "blue"

        name = escape(str(row.get("name") or "Restaurant"))
        cuisine = escape(primary_cuisine(row))
        address = escape(str(row.get("address") or ""))

        popup = f"""
        <div style="width:235px;font-family:Arial,sans-serif;">
          <div style="font-size:16px;font-weight:700;margin-bottom:4px;">{name}</div>
          <div style="font-size:12px;color:#555;margin-bottom:5px;">{cuisine}</div>
          <div style="font-size:12px;margin-bottom:5px;">★ {rating_text(rating)} · {escape(review_text(row.get("review_count")))}</div>
          <div style="font-size:12px;">{address}</div>
        </div>
        """

        folium.Marker(
            [float(row["latitude"]), float(row["longitude"])],
            tooltip=f"{name} · ★ {rating_text(rating)}",
            popup=folium.Popup(popup, max_width=275),
            icon=folium.Icon(color=color, icon="cutlery", prefix="fa"),
            rise_on_hover=True,
        ).add_to(cluster)

    if len(dataframe) > 1:
        m.fit_bounds(
            [
                [float(dataframe["latitude"].min()), float(dataframe["longitude"].min())],
                [float(dataframe["latitude"].max()), float(dataframe["longitude"].max())],
            ],
            padding=(24, 24),
        )

    return m


# ============================================================
# State
# ============================================================
if "saved_ids" not in st.session_state:
    st.session_state["saved_ids"] = set()

if "selected_id" not in st.session_state:
    best = df.sort_values(
        ["recommended_score", "review_count"],
        ascending=[False, False],
    ).iloc[0]
    st.session_state["selected_id"] = int(best["_row_id"])

if "view" not in st.session_state:
    st.session_state["view"] = "Discover"

if "quick_filter" not in st.session_state:
    st.session_state["quick_filter"] = None

if "results_limit" not in st.session_state:
    st.session_state["results_limit"] = 18


# ============================================================
# Brand / navigation
# ============================================================
brand_col, nav_col = st.columns([1.15, 2.35], vertical_alignment="center")

with brand_col:
    st.markdown(
        '<div class="pe-kicker">Philadelphia restaurant guide</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="pe-brand">PhillyEats</div>',
        unsafe_allow_html=True,
    )

with nav_col:
    n1, n2, n3 = st.columns(3)
    current_view = st.session_state.get("view", "Discover")

    if n1.button(
        "Discover",
        key="nav_discover",
        type="primary" if current_view == "Discover" else "secondary",
        use_container_width=True,
    ):
        st.session_state["view"] = "Discover"
        st.rerun()

    if n2.button(
        "Map",
        key="nav_map",
        type="primary" if current_view == "Map" else "secondary",
        use_container_width=True,
    ):
        st.session_state["view"] = "Map"
        st.rerun()

    if n3.button(
        "Saved",
        key="nav_saved",
        type="primary" if current_view == "Saved" else "secondary",
        use_container_width=True,
    ):
        st.session_state["view"] = "Saved"
        st.rerun()

view = st.session_state.get("view", "Discover")

st.markdown(
    '<div style="height:.65rem;border-bottom:1px solid rgba(23,23,23,.09);margin-bottom:1rem;"></div>',
    unsafe_allow_html=True,
)


# ============================================================
# Hero / search
# ============================================================
if view == "Discover":
    st.markdown(
        """
        <div class="pe-hero">
          <div class="pe-hero-title">Find your next favorite place.</div>
          <div class="pe-hero-copy">
            Explore Philadelphia restaurants by cuisine, dietary preference,
            neighborhood, rating, popularity, and price.
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

search_col, sort_col = st.columns([2.5, 1], vertical_alignment="bottom")
with search_col:
    search = st.text_input(
        "Search restaurants",
        placeholder="Search restaurants, cuisines, neighborhoods, vegan, halal…",
        key="search_text",
    ).strip().lower()

with sort_col:
    sort_by = st.selectbox(
        "Sort",
        ["Recommended", "Rating", "Most reviewed", "Name A–Z"],
        key="sort_by",
    )


# ============================================================
# Quick filters
# ============================================================
if view == "Discover":
    st.markdown('<div class="pe-section-title">Browse by mood</div>', unsafe_allow_html=True)
    quick_cols = st.columns(4)
    for i, (label, icon) in enumerate(QUICK_FILTERS):
        col = quick_cols[i % 4]
        active = st.session_state.get("quick_filter") == label
        if col.button(
            f"{icon} {label}",
            key=f"quick_{label}",
            type="primary" if active else "secondary",
            use_container_width=True,
        ):
            st.session_state["quick_filter"] = None if active else label
            st.session_state["results_limit"] = 18
            st.rerun()


# ============================================================
# Filters
# ============================================================
all_labels = set()
for value in df["labels"]:
    for item in str(value).split(","):
        item = item.strip()
        if item and item.lower() != "restaurants":
            all_labels.add(item)

diet_pretty = {
    "vegan restaurants": "Vegan",
    "vegetarian restaurants": "Vegetarian",
    "halal restaurants": "Halal",
    "gluten free restaurants": "Gluten-free",
}
diet_options = sorted(
    {diet_pretty.get(x.lower(), x.title()) for x in all_labels},
    key=str.lower,
)

cuisine_options = sorted(
    {primary_cuisine(row) for _, row in df.iterrows() if primary_cuisine(row) != "Restaurant"},
    key=str.lower,
)

price_options = sorted(
    [x for x in df["price"].unique() if str(x).strip()],
    key=lambda x: (len(str(x)), str(x)),
)

with st.expander("Filters", expanded=False):
    f1, f2, f3, f4 = st.columns(4)
    with f1:
        min_rating = st.slider(
            "Minimum rating",
            0.0, 5.0, 0.0, 0.1,
            key="min_rating",
        )
    with f2:
        cuisines = st.multiselect(
            "Cuisine",
            cuisine_options,
            key="cuisine_filter",
        )
    with f3:
        dietary = st.multiselect(
            "Dietary / labels",
            diet_options,
            key="dietary_filter",
        )
    with f4:
        prices = st.multiselect(
            "Price",
            price_options,
            key="price_filter",
        )


# ============================================================
# Apply filters
# ============================================================
filtered = df.copy()

if search:
    filtered = filtered[filtered["search_blob"].str.contains(search, regex=False)]

if min_rating > 0:
    filtered = filtered[filtered["rating"].fillna(0) >= min_rating]

if cuisines:
    filtered = filtered[
        filtered.apply(lambda r: primary_cuisine(r) in cuisines, axis=1)
    ]

if dietary:
    reverse_pretty = {v: k for k, v in diet_pretty.items()}
    for d in dietary:
        needle = reverse_pretty.get(d, d).lower()
        filtered = filtered[
            (
                filtered["labels"].str.lower().str.contains(needle, regex=False)
                | filtered["types"].str.lower().str.contains(d.lower(), regex=False)
            )
        ]

if prices:
    filtered = filtered[filtered["price"].isin(prices)]

quick_filter = st.session_state.get("quick_filter")
if quick_filter == "Top rated":
    filtered = filtered[filtered["rating"].fillna(0) >= 4.6]
elif quick_filter == "Most reviewed":
    filtered = filtered[filtered["review_count"].fillna(0) >= 1000]
elif quick_filter in {"Vegan", "Halal", "Italian", "Sushi", "Mexican", "Indian"}:
    needle = quick_filter.lower()
    filtered = filtered[
        filtered["search_blob"].str.contains(needle, regex=False)
    ]

if sort_by == "Recommended":
    filtered = filtered.sort_values(
        ["recommended_score", "rating", "review_count"],
        ascending=[False, False, False],
        na_position="last",
    )
elif sort_by == "Rating":
    filtered = filtered.sort_values(
        ["rating", "review_count"],
        ascending=[False, False],
        na_position="last",
    )
elif sort_by == "Most reviewed":
    filtered = filtered.sort_values(
        ["review_count", "rating"],
        ascending=[False, False],
        na_position="last",
    )
else:
    filtered = filtered.sort_values(
        "name",
        key=lambda s: s.str.lower(),
    )


# ============================================================
# DISCOVER
# ============================================================
if view == "Discover":
    if filtered.empty:
        st.markdown(
            """
            <div class="pe-empty">
              <div style="font-size:2rem;">🔎</div>
              <div style="font-weight:800;font-size:1.15rem;margin:.4rem 0;">No matches found</div>
              <div class="pe-meta">Try a broader search or remove a filter.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.stop()

    count_col, clear_col = st.columns([3, 1], vertical_alignment="center")
    with count_col:
        st.markdown(
            f'<div class="pe-section-title">{len(filtered):,} restaurants</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div class="pe-section-copy">Top matches from your current search and filters.</div>',
            unsafe_allow_html=True,
        )
    with clear_col:
        if quick_filter:
            if st.button("Clear quick filter", key="clear_quick", use_container_width=True):
                st.session_state["quick_filter"] = None
                st.rerun()

    # Featured row
    featured = filtered.head(6)
    st.markdown('<div class="pe-section-title">Top picks</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="pe-section-copy">Highly rated places with strong review volume.</div>',
        unsafe_allow_html=True,
    )

    featured_cols = st.columns(3)
    for i, (_, row) in enumerate(featured.iterrows()):
        with featured_cols[i % 3]:
            st.markdown(card_html(row), unsafe_allow_html=True)
            render_actions(row, "featured")

    st.markdown('<div class="pe-section-title" style="margin-top:1.2rem;">Explore more</div>', unsafe_allow_html=True)

    limit = min(st.session_state["results_limit"], len(filtered))
    visible = filtered.head(limit)

    grid = st.columns(3)
    for i, (_, row) in enumerate(visible.iterrows()):
        with grid[i % 3]:
            st.markdown(card_html(row), unsafe_allow_html=True)
            render_actions(row, "list")

    if limit < len(filtered):
        if st.button(
            f"Show more ({len(filtered)-limit:,} remaining)",
            key="show_more",
            use_container_width=True,
        ):
            st.session_state["results_limit"] += 18
            st.rerun()



# ============================================================
# MAP
# ============================================================
elif view == "Map":
    if filtered.empty:
        st.info("No restaurants match the current filters.")
        st.stop()

    st.markdown('<div class="pe-section-title">Explore the map</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="pe-map-note">{len(filtered):,} restaurants · drag to pan · scroll/pinch to zoom · click a marker</div>',
        unsafe_allow_html=True,
    )

    map_col, detail_col = st.columns([2.15, 1], gap="large")

    with map_col:
        m = build_map(filtered)
        map_state = st_folium(
            m,
            key="main_map",
            height=650,
            use_container_width=True,
            returned_objects=["last_object_clicked"],
        )

    clicked = (map_state or {}).get("last_object_clicked")
    if clicked:
        nearest = nearest_restaurant(
            filtered,
            clicked.get("lat"),
            clicked.get("lng"),
        )
        if nearest is not None:
            st.session_state["selected_id"] = int(nearest["_row_id"])

    with detail_col:
        selected_match = filtered[
            filtered["_row_id"] == int(st.session_state["selected_id"])
        ]
        if selected_match.empty:
            selected_match = filtered.head(1)
        render_detail(selected_match.iloc[0], "map_detail")


# ============================================================
# SAVED
# ============================================================
else:
    saved_ids = st.session_state.setdefault("saved_ids", set())
    saved_df = df[df["_row_id"].isin(saved_ids)].copy()

    st.markdown('<div class="pe-section-title">Saved restaurants</div>', unsafe_allow_html=True)

    if saved_df.empty:
        st.markdown(
            """
            <div class="pe-empty">
              <div style="font-size:2rem;">♡</div>
              <div style="font-weight:800;font-size:1.15rem;margin:.4rem 0;">Nothing saved yet</div>
              <div class="pe-meta">Save restaurants from Discover or Map and they’ll appear here during this session.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f'<div class="pe-section-copy">{len(saved_df):,} saved place{"s" if len(saved_df) != 1 else ""}.</div>',
            unsafe_allow_html=True,
        )

        saved_grid = st.columns(3)
        for i, (_, row) in enumerate(saved_df.iterrows()):
            with saved_grid[i % 3]:
                st.markdown(card_html(row), unsafe_allow_html=True)
                render_actions(row, "saved")

        st.divider()
        st.markdown('<div class="pe-section-title">Saved on the map</div>', unsafe_allow_html=True)
        saved_map = build_map(saved_df, zoom_start=12)
        st_folium(
            saved_map,
            key="saved_map",
            height=520,
            use_container_width=True,
            returned_objects=[],
        )


# ============================================================
# Footer
# ============================================================
st.markdown(
    """
    <div style="margin-top:2rem;padding-top:1rem;border-top:1px solid rgba(23,23,23,.08);color:#777;font-size:.8rem;">
      PhillyEats prototype · restaurant data loaded from the bundled CSV · map tiles © OpenStreetMap contributors
    </div>
    """,
    unsafe_allow_html=True,
)
