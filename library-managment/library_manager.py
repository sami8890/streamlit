import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime

# Set page configuration
st.set_page_config(
    page_title="Personal Library Manager",
    page_icon="📚",
    layout="wide"
)

# Initialize session state variables if they don't exist
if 'library' not in st.session_state:
    st.session_state.library = []
    
if 'file_path' not in st.session_state:
    st.session_state.file_path = "library.json"

# Auto-load library on startup
if 'initialized' not in st.session_state:
    st.session_state.initialized = True
    # Try to load the library automatically on first run
    if os.path.exists(st.session_state.file_path):
        try:
            with open(st.session_state.file_path, 'r') as file:
                st.session_state.library = json.load(file)
        except:
            st.error("Failed to load library file automatically.")
    
# Function to load library from file
def load_library():
    try:
        if os.path.exists(st.session_state.file_path):
            with open(st.session_state.file_path, 'r') as file:
                st.session_state.library = json.load(file)
            st.success(f"Library loaded from {st.session_state.file_path}")
        else:
            st.info("No existing library file found. Starting with an empty library.")
    except Exception as e:
        st.error(f"Error loading library: {e}")

# Function to save library to file
def save_library():
    try:
        with open(st.session_state.file_path, 'w') as file:
            json.dump(st.session_state.library, file, indent=4)
        return True
    except Exception as e:
        st.error(f"Error saving library: {e}")
        return False

# Function to add a book
def add_book(title, author, year, genre, read_status):
    # Check if book already exists
    for book in st.session_state.library:
        if book["title"].lower() == title.lower() and book["author"].lower() == author.lower():
            return False, "This book already exists in your library!"
    
    book = {
        "title": title,
        "author": author,
        "year": year,
        "genre": genre,
        "read": read_status,
        "date_added": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    st.session_state.library.append(book)
    if save_library():
        return True, f"'{title}' by {author} added to your library!"
    return False, "Failed to save the library after adding the book."

# Function to remove a book
def remove_book(index):
    if 0 <= index < len(st.session_state.library):
        removed_book = st.session_state.library.pop(index)
        if save_library():
            return True, f"'{removed_book['title']}' by {removed_book['author']} removed from your library!"
        return False, "Failed to save the library after removing the book."
    return False, "Invalid book index."

# Function to edit a book
def edit_book(index, title, author, year, genre, read_status):
    if 0 <= index < len(st.session_state.library):
        st.session_state.library[index] = {
            "title": title,
            "author": author,
            "year": year,
            "genre": genre,
            "read": read_status,
            "date_added": st.session_state.library[index].get("date_added", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        }
        if save_library():
            return True, f"'{title}' by {author} updated successfully!"
        return False, "Failed to save the library after updating the book."
    return False, "Invalid book index."

# Function to search for books
def search_books(search_term, search_by):
    results = []
    search_term = search_term.lower()
    
    for book in st.session_state.library:
        if search_by == "Title" and search_term in book["title"].lower():
            results.append(book)
        elif search_by == "Author" and search_term in book["author"].lower():
            results.append(book)
        elif search_by == "Genre" and search_term in book["genre"].lower():
            results.append(book)
        elif search_by == "Year" and search_term in str(book["year"]):
            results.append(book)
        elif search_by == "All Fields":
            if (search_term in book["title"].lower() or 
                search_term in book["author"].lower() or 
                search_term in book["genre"].lower() or 
                search_term in str(book["year"])):
                results.append(book)
    
    return results

# Function to get library statistics
def get_statistics():
    total_books = len(st.session_state.library)
    read_books = sum(1 for book in st.session_state.library if book["read"])
    
    # Genre statistics
    genres = {}
    for book in st.session_state.library:
        genre = book["genre"]
        if genre in genres:
            genres[genre] += 1
        else:
            genres[genre] = 1
    
    # Author statistics
    authors = {}
    for book in st.session_state.library:
        author = book["author"]
        if author in authors:
            authors[author] += 1
        else:
            authors[author] = 1
    
    # Year statistics
    years = {}
    for book in st.session_state.library:
        year = book["year"]
        decade = (year // 10) * 10
        if decade in years:
            years[decade] += 1
        else:
            years[decade] = 1
    
    if total_books > 0:
        percentage_read = (read_books / total_books) * 100
    else:
        percentage_read = 0
        
    return {
        "total_books": total_books,
        "read_books": read_books,
        "percentage_read": percentage_read,
        "genres": genres,
        "authors": authors,
        "decades": years
    }

# Function to create a backup
def create_backup():
    backup_path = f"library_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    try:
        with open(backup_path, 'w') as file:
            json.dump(st.session_state.library, file, indent=4)
        return True, f"Backup created successfully at {backup_path}"
    except Exception as e:
        return False, f"Error creating backup: {e}"

# Function to display books in a table
def display_books_table(books, with_actions=False):
    if not books:
        st.info("No books to display.")
        return
    
    # Create a DataFrame for display
    df = pd.DataFrame(books)
    
    # Reorder and rename columns for better display
    display_columns = ["title", "author", "year", "genre", "read", "date_added"]
    display_names = ["Title", "Author", "Year", "Genre", "Read", "Date Added"]
    
    # Ensure all columns exist (for older data that might not have all fields)
    for col in display_columns:
        if col not in df.columns:
            df[col] = ""
    
    df = df[display_columns]
    df.columns = display_names
    
    # Convert boolean to Yes/No for better display
    df["Read"] = df["Read"].map({True: "Yes", False: "No"})
    
    # Display the table
    st.dataframe(df, use_container_width=True)
    
    # If actions are needed (for edit/delete)
    if with_actions and books:
        col1, col2 = st.columns(2)
        with col1:
            book_options = [f"{book['title']} by {book['author']}" for book in books]
            selected_book = st.selectbox("Select a book:", book_options)
            selected_index = book_options.index(selected_book)
        
        with col2:
            action = st.radio("Choose action:", ["Edit", "Remove"])
        
        if action == "Edit":
            edit_book_form(selected_index)
        elif action == "Remove":
            if st.button("Confirm Removal"):
                success, message = remove_book(selected_index)
                if success:
                    st.success(message)
                else:
                    st.error(message)

# Function to display edit book form
def edit_book_form(index):
    book = st.session_state.library[index]
    
    with st.form(key=f"edit_book_form_{index}"):
        st.subheader(f"Edit: {book['title']}")
        
        title = st.text_input("Title", value=book["title"])
        author = st.text_input("Author", value=book["author"])
        year = st.number_input("Publication Year", min_value=1000, max_value=datetime.now().year, value=book["year"])
        genre = st.text_input("Genre", value=book["genre"])
        read_status = st.checkbox("I have read this book", value=book["read"])
        
        submitted = st.form_submit_button("Update Book")
        
        if submitted:
            if title and author:  # Basic validation
                success, message = edit_book(index, title, author, year, genre, read_status)
                if success:
                    st.success(message)
                else:
                    st.error(message)
            else:
                st.error("Title and author are required!")

# Main app
def main():
    st.title("📚 Personal Library Manager")
    
    # Sidebar for navigation
    st.sidebar.title("Menu")
    page = st.sidebar.radio(
        "Select an option:",
        ["View Library", "Add a Book", "Manage Books", "Search for Books", "Statistics", "Settings"]
    )
    
    # Manual load/save buttons
    with st.sidebar.expander("File Operations"):
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Load Library"):
                load_library()
        with col2:
            if st.button("Save Library"):
                if save_library():
                    st.success("Library saved successfully!")
    
    # Display current library stats in sidebar
    stats = get_statistics()
    st.sidebar.markdown("---")
    st.sidebar.subheader("Quick Stats")
    st.sidebar.markdown(f"📚 Total Books: **{stats['total_books']}**")
    st.sidebar.markdown(f"✅ Read: **{stats['read_books']}** ({stats['percentage_read']:.1f}%)")
    
    # Display page based on selection
    if page == "View Library":
        st.header("Your Library")
        
        # Filtering options
        with st.expander("Filter Options"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                filter_read = st.radio("Read Status:", ["All", "Read", "Unread"])
            
            with col2:
                if stats["genres"]:
                    genres = ["All"] + list(stats["genres"].keys())
                    filter_genre = st.selectbox("Genre:", genres)
                else:
                    filter_genre = "All"
            
            with col3:
                sort_by = st.selectbox("Sort By:", ["Title", "Author", "Year", "Date Added"])
                sort_order = st.radio("Order:", ["Ascending", "Descending"])
        
        # Apply filters
        filtered_books = st.session_state.library.copy()
        
        if filter_read == "Read":
            filtered_books = [book for book in filtered_books if book["read"]]
        elif filter_read == "Unread":
            filtered_books = [book for book in filtered_books if not book["read"]]
        
        if filter_genre != "All":
            filtered_books = [book for book in filtered_books if book["genre"] == filter_genre]
        
        # Apply sorting
        sort_key = sort_by.lower()
        if sort_key == "date added":
            sort_key = "date_added"
        
        reverse_sort = sort_order == "Descending"
        filtered_books = sorted(filtered_books, key=lambda x: x.get(sort_key, ""), reverse=reverse_sort)
        
        # Display the filtered and sorted books
        st.subheader(f"Showing {len(filtered_books)} of {stats['total_books']} books")
        display_books_table(filtered_books)
    
    elif page == "Add a Book":
        st.header("Add a New Book")
        
        with st.form("add_book_form"):
            title = st.text_input("Title")
            author = st.text_input("Author")
            year = st.number_input("Publication Year", min_value=1000, max_value=datetime.now().year, value=2023)
            genre = st.text_input("Genre")
            read_status = st.checkbox("I have read this book")
            
            submitted = st.form_submit_button("Add Book")
            
            if submitted:
                if title and author:  # Basic validation
                    success, message = add_book(title, author, year, genre, read_status)
                    if success:
                        st.success(message)
                    else:
                        st.error(message)
                else:
                    st.error("Title and author are required!")
    
    elif page == "Manage Books":
        st.header("Manage Your Books")
        
        if not st.session_state.library:
            st.info("Your library is empty. Add some books first!")
        else:
            display_books_table(st.session_state.library, with_actions=True)
    
    elif page == "Search for Books":
        st.header("Search for Books")
        
        search_by = st.radio("Search by:", ["Title", "Author", "Genre", "Year", "All Fields"], horizontal=True)
        search_term = st.text_input(f"Enter search term:")
        
        if search_term:
            results = search_books(search_term, search_by)
            
            if results:
                st.success(f"Found {len(results)} matching books!")
                display_books_table(results)
            else:
                st.info(f"No books found matching '{search_term}' in {search_by.lower()}.")
    
    elif page == "Statistics":
        st.header("Library Statistics")
        
        stats = get_statistics()
        
        # Basic stats
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Books", stats["total_books"])
        with col2:
            st.metric("Read Books", stats["read_books"])
        with col3:
            st.metric("Percentage Read", f"{stats['percentage_read']:.1f}%")
        
        # Visualizations
        if stats["total_books"] > 0:
            st.subheader("Reading Status")
            read_data = pd.DataFrame({
                "Status": ["Read", "Unread"],
                "Count": [stats["read_books"], stats["total_books"] - stats["read_books"]]
            })
            st.bar_chart(read_data.set_index("Status"))
            
            # Genre distribution
            if stats["genres"]:
                st.subheader("Genre Distribution")
                genre_data = pd.DataFrame({
                    "Genre": list(stats["genres"].keys()),
                    "Count": list(stats["genres"].values())
                })
                genre_data = genre_data.sort_values("Count", ascending=False)
                st.bar_chart(genre_data.set_index("Genre"))
            
            # Top authors
            if stats["authors"]:
                st.subheader("Top Authors")
                author_data = pd.DataFrame({
                    "Author": list(stats["authors"].keys()),
                    "Books": list(stats["authors"].values())
                })
                author_data = author_data.sort_values("Books", ascending=False).head(10)
                st.bar_chart(author_data.set_index("Author"))
            
            # Publication decades
            if stats["decades"]:
                st.subheader("Books by Decade")
                decade_data = pd.DataFrame({
                    "Decade": [f"{decade}s" for decade in stats["decades"].keys()],
                    "Books": list(stats["decades"].values())
                })
                decade_data = decade_data.sort_values("Decade")
                st.bar_chart(decade_data.set_index("Decade"))
    
    elif page == "Settings":
        st.header("Settings")
        
        # File path settings
        st.subheader("Library File")
        new_file_path = st.text_input("Library File Path", st.session_state.file_path)
        if new_file_path != st.session_state.file_path:
            if st.button("Update File Path"):
                st.session_state.file_path = new_file_path
                st.success(f"File path updated to {new_file_path}")
        
        # Backup options
        st.subheader("Backup")
        if st.button("Create Backup"):
            success, message = create_backup()
            if success:
                st.success(message)
            else:
                st.error(message)
        
        # Reset library
        st.subheader("Reset Library")
        st.warning("This will delete all books in your library!")
        if st.button("Reset Library"):
            if st.session_state.get("confirm_reset", False):
                st.session_state.library = []
                save_library()
                st.success("Library reset successfully!")
                st.session_state.confirm_reset = False
            else:
                st.session_state.confirm_reset = True
                st.warning("Are you sure? Click 'Reset Library' again to confirm.")
        
        # Cancel reset if needed
        if st.session_state.get("confirm_reset", False):
            if st.button("Cancel Reset"):
                st.session_state.confirm_reset = False
        
        # Import/Export
        st.subheader("Import/Export")
        
        # Export as CSV
        if st.button("Export as CSV"):
            if st.session_state.library:
                df = pd.DataFrame(st.session_state.library)
                csv = df.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name="library_export.csv",
                    mime="text/csv",
                )
            else:
                st.error("Library is empty, nothing to export!")

if __name__ == "__main__":
    main()