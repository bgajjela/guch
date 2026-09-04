
# PhillyEats

A polished restaurant-discovery prototype built with Streamlit and the included Philadelphia restaurant dataset.

## Product experience

- Consumer-style Discover view
- Hero search
- Quick cuisine / dietary collections
- Rating, cuisine, dietary, and price filters
- Recommended / rating / review-count sorting
- Rich restaurant cards
- Restaurant pop-out modal with focused map and place details
- Save / unsave restaurants during the browser session
- Map-first exploration with marker clustering
- Click a marker to inspect a restaurant
- Dedicated restaurant detail treatment
- Google Maps directions
- Restaurant website links
- Responsive layout
- No SerpApi key required for browsing

## Run locally

```bash
python3 -m pip install --upgrade -r requirements.txt
streamlit run app.py
```

Then open:

```text
http://localhost:8501
```

## Deploy to Streamlit Community Cloud

1. Create a GitHub repository.
2. Push this entire folder, including `.streamlit/config.toml`.
3. In Streamlit Community Cloud, create a new app.
4. Choose the repository and `app.py`.
5. Deploy and share the resulting `*.streamlit.app` URL.

No API secrets are required for this version.

## Files

```text
philly_eats_rich/
├── app.py
├── philadelphia_restaurants.csv
├── requirements.txt
├── README.md
├── .gitignore
└── .streamlit/
    └── config.toml
```

## Notes

- Restaurant “Recommended” ranking is a local heuristic using rating and review volume.
- Saved restaurants are intentionally session-only in this prototype.
- The base map uses OpenStreetMap through Folium/Leaflet.
- Google Maps buttons open the restaurant as a search/directions destination; no Google Maps API key is embedded.


## Restaurant pop-out

The View button opens a large restaurant sheet. The restaurant information and
interactive Leaflet map are rendered in one self-contained component, so the
map remains on the right side on desktop instead of being pushed below by
Streamlit's responsive column layout.
