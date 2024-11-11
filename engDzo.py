import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load the dataset
df = pd.read_csv('books.csv')

# Print the columns to check their names
print("Columns in the DataFrame:", df.columns)

# Strip whitespace from column names
df.columns = df.columns.str.strip()

# Check the columns again after stripping
print("Columns after stripping whitespace:", df.columns)

# Clean the data
try:
    df['Book-Title'] = df['Book-Title'].str.lower().str.replace(r'[^\w\s]', '', regex=True)
    df['Book-Author'] = df['Book-Author'].str.lower().str.replace(r'[^\w\s]', '', regex=True)
    df['Description'] = df['Description'].str.lower().str.replace(r'[^\w\s]', '', regex=True)
except KeyError as e:
    print(f"KeyError: {e}. Please check the column names in your CSV file.")
    exit()

# Drop duplicates
df.drop_duplicates(subset='Book-Title', inplace=True)

# Create TF-IDF vectorizer
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(df['Description'].fillna(''))

# Calculate cosine similarity
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

# Recommendation function
def recommend_books(title, language='English', n=5):
    # Get the index of the book that matches the title
    try:
        idx = df.index[df['Book-Title'] == title.lower()].tolist()[0]
    except IndexError:
        return f"Book titled '{title}' not found in the database."

    # Get the pairwise similarity scores of all books with that book
    sim_scores = list(enumerate(cosine_sim[idx]))

    # Sort the books based on the similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the scores of the N most similar books
    sim_scores = sim_scores[1:n+1]

    # Get the book indices
    book_indices = [i[0] for i in sim_scores]

    # Filter for the specified language
    recommended_books = df.iloc[book_indices]
    language_filtered_books = recommended_books[recommended_books['Language'] == language]

    return language_filtered_books[['Book-Title', 'Book-Author', 'Year-Of-Publication', 'Publisher', 'ISBN', 'Image-URL-S', 'Image-URL-M', 'Image-URL-L']]

# Example usage
if __name__ == "__main__":
    user_input = input("Enter the title of the book you want recommendations for: ").strip()
    language_choice = input("Enter the language (English/Dzongkha): ").strip()
    
    recommended_books = recommend_books(user_input, language=language_choice)
    
    if isinstance(recommended_books, str):
        print(recommended_books)  # Print the error message
    else:
        print("Recommended Books:")
        print(recommended_books.to_string(index=False))