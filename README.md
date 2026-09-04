# PhillyEats — Complete Data Bundle

A deployable Streamlit restaurant-discovery app for Philadelphia.

## Included data

- **511 restaurants**
- **14,275 menu items**
- Menu coverage for **337 restaurants** (65.9% of the restaurant dataset)
- Rating and total review-count information from the restaurant dataset
- Ready-to-fill review and photo files

## Main app features

- Discover / Map / Saved navigation
- Search, cuisine, dietary, price, and rating filters
- Rich restaurant cards
- Interactive Philadelphia restaurant map
- Restaurant pop-out with restaurant details + map side-by-side
- Menu tab with item search, sections, descriptions, and prices
- Reviews tab
- Photos tab
- Google Maps directions
- Restaurant website links
- Session-based favorites
- Streamlit Community Cloud ready

## Files

```text
philly_eats_complete_data_app/
├── app.py
├── philadelphia_restaurants.csv
├── menu_items.csv
├── reviews.csv
├── restaurant_photos.csv
├── requirements.txt
├── README.md
├── DATA_FORMATS.md
├── DEPLOY.md
└── .streamlit/
    └── config.toml
```

## Run locally

```bash
python3 -m pip install -r requirements.txt
streamlit run app.py
```

## Deploy

Push the folder to GitHub and deploy `app.py` with Streamlit Community Cloud.

No SerpApi, Google Maps, or Mapbox API key is required for browsing this bundle.
