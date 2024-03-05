import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector

# Function to initialize the recommendation page
def initialize_recommendation_page():
    recommendation_window = tk.Toplevel(root)
    recommendation_window.title("Music Recommendation")
    
    # Fetch available genres from the database
    genres = fetch_genres()
    
    # Create dropdown menu for genres
    genre_label = tk.Label(recommendation_window, text="Select Genre:", font=("Helvetica", 12))
    genre_label.pack()
    genre_var = tk.StringVar()
    genre_dropdown = ttk.Combobox(recommendation_window, textvariable=genre_var, values=genres)
    genre_dropdown.pack()
    
    # Function to display songs based on selected genre
    def display_songs():
        selected_genre = genre_var.get()
        if selected_genre:
            songs = fetch_songs_by_genre(selected_genre)
            if songs:
                song_listbox.delete(0, tk.END)
                for song in songs:
                    song_listbox.insert(tk.END, f"{song[1]} - {song[2]}")
            else:
                messagebox.showwarning("No Songs", f"No songs found for genre: {selected_genre}")
        else:
            messagebox.showwarning("No Genre Selected", "Please select a genre.")

    # Create listbox to display recommended songs
    song_listbox = tk.Listbox(recommendation_window, font=("Helvetica", 12), width=50)
    song_listbox.pack()
    
    # Create button to display songs
    display_button = tk.Button(recommendation_window, text="Display Songs", command=display_songs)
    display_button.pack()

# Function to fetch available genres from the database
def fetch_genres():
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM genres")
        genres = [row[0] for row in cursor.fetchall()]
        cursor.close()
        return genres
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error accessing database: {err}")
        return []

# Function to fetch songs based on selected genre
def fetch_songs_by_genre(genre):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM songs JOIN genres ON songs.genre_id = genres.id WHERE genres.name = %s", (genre,))
        songs = cursor.fetchall()
        cursor.close()
        return songs
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error accessing database: {err}")
        return []

# Function to handle user login
def user_login(username, password):
    try:
        cursor = conn.cursor()
        query = "SELECT * FROM users WHERE username = %s AND password = %s"
        cursor.execute(query, (username, password))
        user = cursor.fetchone()
        cursor.close()
        return user
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error accessing database: {err}")
        return None

# Function to handle user login button click
def user_login_button_click():
    username = entry_username.get()
    password = entry_password.get()
    if not username or not password:
        messagebox.showwarning("Missing Information", "Please enter both username and password.")
        return
    user = user_login(username, password)
    if user:
        messagebox.showinfo("Login Successful", "Welcome!")
        initialize_recommendation_page()
        root.withdraw()
    else:
        messagebox.showerror("Login Failed", "Invalid username or password.")

# Function to close the connection and exit the application
def close_connection_and_exit():
    conn.close()
    root.destroy()

# Connect to MySQL database
try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="0108",
        database="music"
    )
except mysql.connector.Error as err:
    messagebox.showerror("Database Connection Error", f"Error connecting to database: {err}")
    exit()

# Create main window
root = tk.Tk()
root.title("Music Recommendation App")
root.configure(bg="lightblue")

# Get the screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
window_width = int(screen_width * 0.75)
window_height = int(screen_height * 0.75)
root.geometry(f"{window_width}x{window_height}")

# Create login frame
frame_login = tk.Frame(root, bg="lightblue")
frame_login.pack(expand=True)

# Create login labels and entry fields
tk.Label(frame_login, text="Login", font=("Helvetica", 16), bg="lightblue").pack()
tk.Label(frame_login, text="Username:", bg="lightblue").pack()
entry_username = tk.Entry(frame_login)
entry_username.pack()

tk.Label(frame_login, text="Password:", bg="lightblue").pack()
entry_password = tk.Entry(frame_login, show="*")
entry_password.pack()

# Create login button
button_user_login = tk.Button(frame_login, text="Login (User)", command=user_login_button_click)
button_user_login.pack()

# Bind closing event to close_connection_and_exit function
root.protocol("WM_DELETE_WINDOW", close_connection_and_exit)

# Run the main event loop
root.mainloop()
