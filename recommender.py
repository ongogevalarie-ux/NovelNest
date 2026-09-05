import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# --------------------------------
# LOAD DATASET
# --------------------------------

books = pd.read_csv("data/novels.csv")


# --------------------------------
# CLEAN DATA
# --------------------------------

books["title"] = books["title"].fillna("Unknown Title")
books["author"] = books["author"].fillna("Unknown Author")
books["genre"] = books["genre"].fillna("Fiction")
books["description"] = books["description"].fillna("")


# --------------------------------
# COMBINE BOOK INFORMATION
# --------------------------------

books["content"] = (
    books["genre"] + " " +
    books["description"] + " " +
    books["author"]
)


# --------------------------------
# CREATE TF-IDF MATRIX
# --------------------------------

vectorizer = TfidfVectorizer(
    stop_words="english"
)

tfidf_matrix = vectorizer.fit_transform(
    books["content"]
)


# --------------------------------
# CALCULATE COSINE SIMILARITY
# --------------------------------

similarity_matrix = cosine_similarity(
    tfidf_matrix
)


# --------------------------------
# RECOMMENDATION FUNCTION
# --------------------------------

def recommend(title, number_of_recommendations=5):

    matching_books = books[
        books["title"].str.lower() == title.lower()
    ]

    if matching_books.empty:
        return []

    book_index = matching_books.index[0]

    similarity_scores = list(
        enumerate(
            similarity_matrix[book_index]
        )
    )

    similarity_scores = sorted(
        similarity_scores,
        key=lambda x: x[1],
        reverse=True
    )

    # Remove the selected book
    similarity_scores = similarity_scores[
        1:number_of_recommendations + 1
    ]

    recommendations = []

    for index, score in similarity_scores:

        recommendations.append({
            "title": books.iloc[index]["title"],
            "author": books.iloc[index]["author"],
            "genre": books.iloc[index]["genre"],
            "rating": books.iloc[index]["rating"],
            "year": books.iloc[index]["year"],
            "cover_id": books.iloc[index]["cover_id"],
            "similarity": round(score, 3)
        })

    return recommendations


# --------------------------------
# TEST
# --------------------------------

if __name__ == "__main__":

    print(
        "Number of novels:",
        len(books)
    )

    print(
        "TF-IDF matrix shape:",
        tfidf_matrix.shape
    )

    recommendations = recommend(
        books.iloc[0]["title"]
    )

    print(
        f"\nRecommendations for "
        f"{books.iloc[0]['title']}:\n"
    )

    for novel in recommendations:

        print(
            f"{novel['title']} - "
            f"{novel['author']} - "
            f"Similarity: "
            f"{novel['similarity']}"
        )