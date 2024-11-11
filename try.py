import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load dataset
df = pd.read_csv('books.csv')

# Debug: Print the columns to check for issues
print("Columns in the DataFrame:", df.columns)

# Clean the data
df.columns = df.columns.str.strip()  # Strip whitespace from column names

# Check if required columns exist
required_columns = ['Book-Title', 'Description']
for col in required_columns:
    if col not in df.columns:
        print(f"Error: Column '{col}' not found in the dataset.")
        exit()

# Clean the 'Book-Title' and 'Description' columns
df['Book-Title'] = df['Book-Title'].str.lower().str.replace(r'[^\w\s]', '', regex=True)
df['Description'] = df['Description'].str.lower().str.replace(r'[^\w\s]', '', regex=True)

# Drop duplicates
df.drop_duplicates(subset='Book-Title', inplace=True)

# Create TF-IDF vectorizer
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(df['Description'].fillna(''))  # Fill NaN with empty string

# Calculate cosine similarity
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

# Recommendation function
def recommend_books(title, cosine_sim=cosine_sim, df=df, n=5):
    # Get the index of the book that matches the title
    try:
        idx = df.index[df['Book-Title'] == title].tolist()[0]
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

    # Return the top N most similar books
    return df['Book-Title'].iloc[book_indices]

# Example usage
if __name__ == "__main__":
    # Prompt user for the book title
    user_input = input("Enter the title of the book you want recommendations for: ").strip().lower()
    
    # Recommend books based on user input
    recommended_books = recommend_books(user_input)
    
    # Check if the result is a string or a DataFrame
    if isinstance(recommended_books, str):
        print(recommended_books)  # Print the error message
    else:
        print("Recommended Books:")
        print(recommended_books.to_string(index=False))