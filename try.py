import pandas as pd

def is_ascii(s):
    return all(ord(c) < 128 for c in s)

def filter_english_books(input_file, output_file):
    try:
        # Load the dataset with low_memory=False to suppress DtypeWarning
        df = pd.read_csv(input_file, low_memory=False)

        # Display the first few rows and columns to understand the structure
        print("Original DataFrame:")
        print(df.head())
        print("Columns in the DataFrame:", df.columns)

        # Check if the necessary columns exist
        required_columns = ['ISBN', 'Book-Title', 'Book-Author', 'Year-Of-Publication', 'Publisher', 'Image-URL-S', 'Image-URL-M', 'Image-URL-L']
        for col in required_columns:
            if col not in df.columns:
                raise ValueError(f"Missing required column: {col}")

        # Filter for English books based on ASCII characters in titles and authors
        df = df[df['Book-Title'].apply(is_ascii) & df['Book-Author'].apply(is_ascii)]

        # Select only the specified columns
        filtered_df = df[required_columns]

        # Check if the filtered DataFrame is empty
        if filtered_df.empty:
            print("There are no English books available in the dataset.")
            return  # Exit the function if no books are found
        else:
            # Save the filtered DataFrame to a new CSV file
            filtered_df.to_csv(output_file, index=False)
            print("Filtered DataFrame:")
            print(filtered_df.head())

            # Ask the user for a book recommendation
            recommended_book = input("Please enter the title of a book you recommend: ")

            # Check if the recommended book is in the filtered DataFrame
            if recommended_book in filtered_df['Book-Title'].values:
                print(f"Thank you for your recommendation! '{recommended_book}' is available.")
            else:
                print(f"Sorry, '{recommended_book}' is not found in the filtered list of English books.")

    except FileNotFoundError:
        print(f"Error: The file '{input_file}' was not found.")
    except pd.errors.EmptyDataError:
        print("Error: The input file is empty.")
    except ValueError as ve:
        print(f"ValueError: {ve}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Example usage
if __name__ == "__main__":
    input_file = 'books.csv'  # Input CSV file containing the book data
    output_file = 'english_books_filtered.csv'  # Output CSV file for filtered data
    filter_english_books(input_file, output_file)