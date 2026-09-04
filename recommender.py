import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load the novel dataset
books = pd.read_csv("data/novels.csv")

# Combine important information about each novel
books["content"] = (
    books["genre"].fillna("") + " " +
    books["description"].fillna("") + " " +
    books["author"].fillna("")
)

# Create the TF-IDF vectorizer
vectorizer = TfidfVectorizer(stop_words="english")

# Convert novel content into numerical vectors
tfidf_matrix = vectorizer.fit_transform(books["content"])

# Calculate similarity between all novels
similarity_matrix = cosine_similarity(tfidf_matrix)

print("Similarity matrix shape:", similarity_matrix.shape)


def recommend(title, number_of_recommendations=5):

    # Find the selected novel
    matching_books = books[
        books["title"].str.lower() == title.lower()
    ]

    # Check if the novel exists
    if matching_books.empty:
        return []

    # Get the index of the selected novel
    book_index = matching_books.index[0]

    # Get similarity scores
    similarity_scores = list(
        enumerate(similarity_matrix[book_index])
    )

    # Sort from most similar to least similar
    similarity_scores = sorted(
        similarity_scores,
        key=lambda x: x[1],
        reverse=True
    )

    # Remove the selected novel itself
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
            "similarity": round(score, 3)
        })

    return recommendations


# Test the recommendation system
recommendations = recommend("The Hobbit")

print("\nRecommendations for The Hobbit:\n")

for novel in recommendations:
    print(
        f"{novel['title']} - "
        f"{novel['author']} - "
        f"Similarity: {novel['similarity']}"
    )