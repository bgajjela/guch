# Deploy to Streamlit Community Cloud

## 1. Push to GitHub

```bash
cd philly_eats_complete_data_app
git init
git add .
git commit -m "Deploy PhillyEats"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/philly-eats.git
git push -u origin main
```

## 2. Deploy

In Streamlit Community Cloud select:

- Repository: `YOUR_USERNAME/philly-eats`
- Branch: `main`
- Main file path: `app.py`

Then click **Deploy**.

The generated `*.streamlit.app` URL can be shared publicly.
