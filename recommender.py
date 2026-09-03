import pandas as pd

# Load the dataset
books = pd.read_csv("data/novels.csv")

# Combine important text information
books["content"] = (
    books["genre"].fillna("") + " " +
    books["description"].fillna("") + " " +
    books["author"].fillna("")
)

# Display the title and combined content
print(books[["title", "content"]].head())