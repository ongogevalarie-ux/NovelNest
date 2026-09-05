import streamlit as st
import pandas as pd
from recommender import books, recommend


# --------------------------------
# PAGE CONFIGURATION
# --------------------------------

st.set_page_config(
    page_title="NovelNest",
    page_icon="📚",
    layout="wide"
)


# --------------------------------
# TITLE
# --------------------------------

st.title("📚 NovelNest")

st.write(
    "Discover novels based on your interests and reading preferences."
)


# --------------------------------
# SEARCH & FILTERS
# --------------------------------

st.sidebar.header("🔎 Search & Filters")

search = st.sidebar.text_input(
    "Search by title"
)

authors = ["All Authors"] + sorted(
    books["author"].dropna().unique().tolist()
)

selected_author = st.sidebar.selectbox(
    "Filter by author",
    authors
)

genres = ["All Genres"] + sorted(
    books["genre"].dropna().unique().tolist()
)

selected_genre = st.sidebar.selectbox(
    "Filter by genre",
    genres
)

minimum_rating = st.sidebar.slider(
    "Minimum rating",
    min_value=0.0,
    max_value=5.0,
    value=0.0,
    step=0.1
)

minimum_year = st.sidebar.slider(
    "Published from",
    min_value=int(books["year"].min()),
    max_value=int(books["year"].max()),
    value=int(books["year"].min())
)


# --------------------------------
# APPLY FILTERS
# --------------------------------

filtered_books = books.copy()

if search:
    filtered_books = filtered_books[
        filtered_books["title"].str.contains(
            search,
            case=False,
            na=False
        )
    ]

if selected_author != "All Authors":
    filtered_books = filtered_books[
        filtered_books["author"] == selected_author
    ]

if selected_genre != "All Genres":
    filtered_books = filtered_books[
        filtered_books["genre"] == selected_genre
    ]

filtered_books = filtered_books[
    filtered_books["rating"].fillna(0) >= minimum_rating
]

filtered_books = filtered_books[
    filtered_books["year"].fillna(0) >= minimum_year
]


# --------------------------------
# DISPLAY NOVELS
# --------------------------------

st.subheader("📖 Available Novels")

if filtered_books.empty:

    st.warning(
        "No novels match your search criteria."
    )

else:

    st.write(
        f"Found **{len(filtered_books)}** novel(s)."
    )

    for _, novel in filtered_books.head(20).iterrows():

        col1, col2 = st.columns([1, 3])

        with col1:

            cover_id = novel["cover_id"]

            if pd.notna(cover_id) and str(cover_id).strip():

                cover_url = (
                    f"https://covers.openlibrary.org/"
                    f"b/id/{int(cover_id)}-M.jpg"
                )

                st.image(
                    cover_url,
                    width=130
                )

        with col2:

            st.write(
                f"### 📖 {novel['title']}"
            )

            st.write(
                f"**Author:** {novel['author']}"
            )

            st.write(
                f"**Genre:** {novel['genre']}"
            )

            st.write(
                f"**Year:** {novel['year']}"
            )

            st.write(
                f"**Rating:** ⭐ {novel['rating']}"
            )

        st.divider()


# --------------------------------
# RECOMMENDATIONS
# --------------------------------

st.subheader("🤖 Get Recommendations")

if not filtered_books.empty:

    selected_novel = st.selectbox(
        "Choose a novel:",
        filtered_books["title"]
    )

    if st.button("✨ Recommend Novels"):

        recommendations = recommend(
            selected_novel
        )

        st.subheader(
            f"Recommendations similar to "
            f"'{selected_novel}'"
        )

        for novel in recommendations:

            col1, col2 = st.columns([1, 3])

            with col1:

                cover_id = novel["cover_id"]

                if pd.notna(cover_id) and str(cover_id).strip():

                    cover_url = (
                        f"https://covers.openlibrary.org/"
                        f"b/id/{int(cover_id)}-M.jpg"
                    )

                    st.image(
                        cover_url,
                        width=130
                    )

            with col2:

                st.write(
                    f"### 📖 {novel['title']}"
                )

                st.write(
                    f"**Author:** {novel['author']}"
                )

                st.write(
                    f"**Genre:** {novel['genre']}"
                )

                st.write(
                    f"**Similarity:** "
                    f"{novel['similarity']}"
                )

            st.divider()