import tkinter as tk
from tkinter import messagebox
import random

# Word categories
categories = {
    "Animals": ["tiger", "elephant", "giraffe", "zebra", "kangaroo", "dolphin", "crocodile", "butterfly"],
    "Fruits": ["apple", "banana", "orange", "grape", "pineapple", "mango", "blueberry", "strawberry"],
    "Countries": ["india", "canada", "germany", "france", "brazil", "australia", "russia", "italy"],
    "Colors": ["red", "blue", "yellow", "green", "purple", "orange", "maroon", "violet"],
    "Sports": ["cricket", "soccer", "badminton", "baseball", "hockey", "tennis", "volleyball", "basketball"]
}

# Game variables
chosen_word = ""
display = []
attempts = 0

def generate_hint(word):
    """Generate a hint based on word length."""
    if len(word) <= 4:  # Short words: No hint
        return "No hint available for short words."
    hint = list("-" * len(word))
    reveal_count = 1 if 5 <= len(word) <= 7 else 2  # Medium words: 1 letter; Long words: 2 letters
    indices = random.sample(range(len(word)), reveal_count)
    for index in indices:  #loop to give indices to random words and generate random indices
        hint[index] = word[index]
    return "".join(hint)

def start_game(category):
    global chosen_word, display, attempts
    if category == "Select a category":
        messagebox.showwarning("Warning", "Please select a valid category.")
        return

    chosen_word = random.choice(categories[category])
    display.clear() # clear the list from previous game
    display.extend(["_"] * len(chosen_word))
    attempts = len(chosen_word) + 3  # Word length + 3 attempts

    word_label.config(text=" ".join(display)) # replace the chosen word with _
    hint = generate_hint(chosen_word)   #calling of generate hint function
    hint_label.config(text=f"Hint: {hint}")   # updating hints on the _ 
    attempts_label.config(text=f"Attempts Remaining: {attempts}")
    guess_entry.delete(0, tk.END)

def check_guess(event=None):
    global attempts
    guess = guess_entry.get().lower()   #converting entry to lower case
    guess_entry.delete(0, tk.END)       #deleting previous enteries

    if len(guess) != 1 or not guess.isalpha():
        messagebox.showerror("Error", "Please enter only one valid letter.")
        return

    if guess in display:
        messagebox.showinfo("Info", "You already guessed that letter!")
        return

    if guess in chosen_word:
        for index in range(len(chosen_word)):
            if chosen_word[index] == guess:
                display[index] = guess
        word_label.config(text=" ".join(display))
        if "_" not in display:
            messagebox.showinfo("Congratulations!", f"You guessed the word: {chosen_word}")
            reset_game()
    else:
        attempts -= 1
        attempts_label.config(text=f"Attempts Remaining: {attempts}")
        if attempts == 0:
            messagebox.showinfo("Game Over", f"You ran out of attempts! The word was: {chosen_word}")
            reset_game()

def reset_game():
    category_var.set("Select a category")
    word_label.config(text="")
    hint_label.config(text="Hint: ")
    attempts_label.config(text="Attempts Remaining: 0")
    guess_entry.delete(0, tk.END)

# GUI Setup
root = tk.Tk()
root.title("Word Raider Game")
root.geometry("500x400")

# Dropdown for categories
category_var = tk.StringVar(value="Select a category")
category_menu = tk.OptionMenu(root, category_var, *categories.keys())
category_menu.pack(pady=10)

# Start button
start_button = tk.Button(root, text="Start Game", command=lambda: start_game(category_var.get()))
start_button.pack(pady=5)

# Word display
word_label = tk.Label(root, text="", font=("Arial", 16))
word_label.pack(pady=10)

# Hint display
hint_label = tk.Label(root, text="Hint: ", font=("Arial", 12), fg="blue")
hint_label.pack(pady=5)

# Attempts remaining
attempts_label = tk.Label(root, text="Attempts Remaining: 0", font=("Arial", 12))
attempts_label.pack(pady=5)

# Guess entry
guess_entry = tk.Entry(root, font=("Arial", 14))
guess_entry.pack(pady=10)

# Bind "Enter" key to check_guess
root.bind('<Return>', check_guess)

# Submit guess button
submit_button = tk.Button(root, text="Submit Guess", command=check_guess)
submit_button.pack(pady=5)

# Run the main loop
root.mainloop()
