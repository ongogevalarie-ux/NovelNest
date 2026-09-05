import requests
import pandas as pd
import time

BOOKS_NEEDED = 500
BOOKS_PER_REQUEST = 100

url = "https://openlibrary.org/search.json"

params = {
    "q": "subject:fiction",
    "fields": "key,title,author_name,first_publish_year,subject,cover_i",
    "limit": BOOKS_PER_REQUEST,
    "page": 1
}

books = []

while len(books) < BOOKS_NEEDED:

    print(f"Downloading page {params['page']}...")

    response = requests.get(
        url,
        params=params,
        timeout=30
    )

    response.raise_for_status()

    data = response.json()

    for book in data.get("docs", []):

        title = book.get("title")

        authors = book.get(
            "author_name",
            []
        )

        if not title or not authors:
            continue

        subjects = book.get(
            "subject",
            []
        )

        books.append({
            "title": title,
            "author": authors[0],
            "genre": subjects[0] if subjects else "Fiction",
            "description": " ".join(subjects[:10]),
            "rating": 0,
            "year": book.get(
                "first_publish_year",
                0
            ),
            "cover_id": book.get(
                "cover_i",
                ""
            )
        })

        if len(books) >= BOOKS_NEEDED:
            break

    params["page"] += 1

    time.sleep(1)


# Remove duplicate titles
df = pd.DataFrame(books)

df = df.drop_duplicates(
    subset=["title"],
    keep="first"
)

df = df.head(BOOKS_NEEDED)

# Create ID
df.insert(
    0,
    "id",
    range(1, len(df) + 1)
)

# Save dataset
df.to_csv(
    "data/novels.csv",
    index=False
)

print()
print("Dataset created successfully!")
print("Number of novels:", len(df))
print()
print(df.head())