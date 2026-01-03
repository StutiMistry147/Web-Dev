import tkinter as tk
from tkinter import ttk
import csv
import random


LIGHT_BG = "#f0f4f8"
DARK_BG = "#1e1e2f"
CARD_COLORS = {
    "Geography": "#a6d8ff",
    "Science": "#b2f2bb",
    "Programming": "#fff3b0",
    "Literature": "#ffb3b3",
    "Default": "#ffffff"
}
BUTTON_BG = "#4f46e5"
BUTTON_HOVER = "#6366f1"
BUTTON_FG = "#ffffff"

FONT_LARGE = ("Helvetica", 22, "bold")
FONT_MEDIUM = ("Helvetica", 14, "bold")
FONT_SMALL = ("Helvetica", 12)


flashcards = []
with open("flashcards.csv", newline='', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        flashcards.append({
            "question": row["Question"],
            "answer": row["Answer"],
            "category": row.get("Category", "Default"),
            "deck": row.get("Deck", "General")
        })


decks = list(set([card["deck"] for card in flashcards]))


root = tk.Tk()
root.title("Modern Flashcard App")
root.geometry("700x550")
root.config(bg=LIGHT_BG)
root.resizable(False, False)


selected_deck = tk.StringVar(value=decks[0])

current_index = 0
showing_answer = False
theme = "light"
auto_flip = True
filtered_cards = []
progress_label = tk.Label(root, text="", font=FONT_MEDIUM, bg=LIGHT_BG)
progress_label.pack(pady=(10,0))

deck_frame = tk.Frame(root, bg=LIGHT_BG)
deck_frame.pack(pady=5)

tk.Label(deck_frame, text="Select Deck:", font=FONT_SMALL, bg=LIGHT_BG).pack(side="left", padx=5)
deck_dropdown = ttk.Combobox(deck_frame, textvariable=selected_deck, values=decks, state="readonly")
deck_dropdown.pack(side="left")
deck_dropdown.bind("<<ComboboxSelected>>", lambda e: change_deck())


shadow_frame = tk.Frame(root, bg="#d1d1d1")
shadow_frame.pack(pady=20, padx=50, fill="both", expand=True)

card_frame = tk.Frame(shadow_frame, bg="#ffffff", bd=0, relief="flat", padx=25, pady=25)
card_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

card_text = tk.StringVar()
card_label = tk.Label(card_frame, textvariable=card_text,
                      font=FONT_LARGE,
                      wraplength=600,
                      justify="center",
                      bg="#ffffff")
card_label.pack(expand=True)


button_frame = tk.Frame(root, bg=LIGHT_BG)
button_frame.pack(pady=10)

def create_button(master, text, command):
    btn = tk.Button(master, text=text, command=command,
                    width=14, height=1,
                    bg=BUTTON_BG, fg=BUTTON_FG,
                    font=FONT_MEDIUM, bd=0, relief="flat",
                    activebackground=BUTTON_HOVER)
    btn.bind("<Enter>", lambda e: btn.config(bg=BUTTON_HOVER))
    btn.bind("<Leave>", lambda e: btn.config(bg=BUTTON_BG))
    return btn

prev_button = create_button(button_frame, "Previous", lambda: change_card(-1))
answer_button = create_button(button_frame, "Show Answer", lambda: show_answer())
next_button = create_button(button_frame, "Next", lambda: change_card(1))

prev_button.grid(row=0, column=0, padx=10)
answer_button.grid(row=0, column=1, padx=10)
next_button.grid(row=0, column=2, padx=10)

shuffle_frame = tk.Frame(root, bg=LIGHT_BG)
shuffle_frame.pack(pady=5)
shuffle_button = create_button(shuffle_frame, "Shuffle Cards", lambda: shuffle_cards())
shuffle_button.pack()

theme_button = create_button(root, "Toggle Theme", lambda: toggle_theme())
theme_button.pack(pady=10)

def filter_deck(deck_name):
    global filtered_cards
    filtered_cards = [card for card in flashcards if card["deck"] == deck_name]
    random.shuffle(filtered_cards)

def change_deck():
    global current_index
    current_index = 0
    filter_deck(selected_deck.get())
    show_question()

def update_progress():
    progress_label.config(text=f"Card {current_index+1}/{len(filtered_cards)} | "
                               f"{int((current_index+1)/len(filtered_cards)*100)}% completed")

def show_question():
    global showing_answer
    showing_answer = False
    if not filtered_cards:
        card_text.set("No cards in this deck!")
        return
    card = filtered_cards[current_index]
    card_text.set(card["question"])
    answer_button.config(text="Show Answer")
    color = CARD_COLORS.get(card["category"], CARD_COLORS["Default"])
    card_frame.config(bg=color)
    card_label.config(bg=color)
    update_progress()
    if auto_flip:
        root.after(5000, auto_flip_card)

def show_answer():
    global showing_answer
    if not showing_answer:
        card = filtered_cards[current_index]
        card_text.set(card["answer"])
        answer_button.config(text="Next Card")
        showing_answer = True
    else:
        change_card(1)

def auto_flip_card():
    if not showing_answer:
        show_answer()

def change_card(step):
    global current_index
    if not filtered_cards:
        return
    current_index += step
    if current_index >= len(filtered_cards):
        current_index = 0
        random.shuffle(filtered_cards)
    elif current_index < 0:
        current_index = len(filtered_cards) - 1
    show_question()

def shuffle_cards():
    random.shuffle(filtered_cards)
    global current_index
    current_index = 0
    show_question()

def toggle_theme():
    global theme
    if theme == "light":
        root.config(bg=DARK_BG)
        progress_label.config(bg=DARK_BG, fg="#ffffff")
        button_frame.config(bg=DARK_BG)
        shuffle_frame.config(bg=DARK_BG)
        deck_frame.config(bg=DARK_BG)
        theme = "dark"
    else:
        root.config(bg=LIGHT_BG)
        progress_label.config(bg=LIGHT_BG, fg="#000000")
        button_frame.config(bg=LIGHT_BG)
        shuffle_frame.config(bg=LIGHT_BG)
        deck_frame.config(bg=LIGHT_BG)
        theme = "light"

change_deck() 
root.mainloop()
