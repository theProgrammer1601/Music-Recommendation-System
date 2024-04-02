# Connect to MySQL database
try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="0108",
        database="music"
    )
    cursor = conn.cursor()

    # Expand the database schema by creating tables for songs and genres
    cursor.execute("CREATE TABLE IF NOT EXISTS songs (id INT AUTO_INCREMENT PRIMARY KEY, title VARCHAR(255), artist VARCHAR(255), genre_id INT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS genres (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255))")

    # Populate genres table with more genres
    genres = [("Pop",), ("Rock",), ("Hip Hop",), ("R&B",), ("Country",)]
    cursor.executemany("INSERT INTO genres (name) VALUES (%s)", genres)

    # Populate songs table with more songs
    songs = [("Song 1", "Artist 1", 1), ("Song 2", "Artist 2", 2), ("Song 3", "Artist 3", 3), ("Song 4", "Artist 4", 4)]
    cursor.executemany("INSERT INTO songs (title, artist, genre_id) VALUES (%s, %s, %s)", songs)

    conn.commit()
    cursor.close()
except mysql.connector.Error as err:
    messagebox.showerror("Database Error", f"Error connecting to database: {err}")
    exit()

# Function to handle user login
def user_login(username, password):
    try:
        cursor = conn.cursor()
        query = "SELECT * FROM users WHERE username = %s AND password = %s"
        cursor.execute(query, (username, password))
        user = cursor.fetchone()
        if user:
            # Fetch user's preferred genres
            query = "SELECT genre_id FROM user_genres WHERE user_id = %s"
            cursor.execute(query, (user[0],))  # Assuming user ID is in the first column
            preferred_genres = [row[0] for row in cursor.fetchall()]
            cursor.close()
            return user, preferred_genres
        cursor.close()
        return None, None
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error accessing database: {err}")
        return None, None

# Function to initialize the recommendation page
def initialize_recommendation_page(user, preferred_genres):
    recommendation_window = tk.Toplevel(root)
    recommendation_window.title("Music Recommendation")

    # Fetch songs based on user's preferred genres
    if preferred_genres:
        query = "SELECT * FROM songs WHERE genre_id IN ({})".format(','.join(map(str, preferred_genres)))
    else:
        # If no preferred genres, fetch all songs
        query = "SELECT * FROM songs"
    cursor.execute(query)
    songs = cursor.fetchall()

    # Display recommended songs
    label_recommendation = tk.Label(recommendation_window, text="Recommended Songs", font=("Helvetica", 16))
    label_recommendation.pack()
    for song in songs:
        song_label = tk.Label(recommendation_window, text=f"{song[1]} - {song[2]}", font=("Helvetica", 12))
        song_label.pack()

# Rest of the code remains unchanged
