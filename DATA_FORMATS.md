# Optional data formats

The app already includes `menu_items.csv`.

## reviews.csv

Replace the empty template with your review data.

Supported columns:

```text
place_id
data_id
reviewer_name
rating
review_text
review_date
likes
review_url
```

The app also accepts common aliases including `text`, `snippet`,
`author_name`, `user_name`, and `date`.

Restaurant matching uses `place_id` and/or `data_id`.

## restaurant_photos.csv

Supported columns:

```text
place_id
data_id
photo_url
photo_path
caption
```

- `photo_url`: public HTTPS image URL.
- `photo_path`: image path relative to the app folder, for example
  `photos/my_restaurant_1.jpg`.
- You may also use common aliases such as `image_url`, `url`, `path`,
  or `image_path`.

For a large photo library, hosting photos externally and storing URLs in
`restaurant_photos.csv` is recommended.

## menu_items.csv

Bundled columns:

```text
record_key
place_id
data_id
restaurant_name
address
section
item_name
description
price
currency
source_url
source_type
raw_text
```

The restaurant pop-out automatically loads matching menu items by place ID.
