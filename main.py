from tkinter import *
import pandas
import random

# ---------------------------- CONSTANTS ------------------------------- #

BG_COLOR = "#B1DDC6"
current_card = {}
to_learn = {}

try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/German to Romanian - Sheet1.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")


# ---------------------------- FUNCTIONS ------------------------------- #

def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(card_title, text="German", fill="black")
    canvas.itemconfig(card_word, text=current_card["German"], fill="black")
    canvas.itemconfig(card_bg, image=card_front_img)
    flip_timer = window.after(3000, flip_card)


def flip_card():
    global current_card
    canvas.itemconfig(card_title, text="Romanian", fill="white")
    canvas.itemconfig(card_word, text=current_card["Romanian"], fill="white")
    canvas.itemconfig(card_bg, image=card_back_img)


def is_known():
    to_learn.remove(current_card)
    data_to_learn = pandas.DataFrame(to_learn)
    data_to_learn.to_csv("data/words_to_learn.csv", index=False)
    next_card()


# ---------------------------- UI SETUP  ------------------------------- #

window = Tk()
window.title("Flash Cards")
window.config(padx=50, pady=50, bg=BG_COLOR)

flip_timer = window.after(3000, flip_card)

### Canvas
canvas = Canvas(window, width=800, height=526, highlightthickness=0)
card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")
card_bg = canvas.create_image(400, 263, image=card_front_img)
card_title = canvas.create_text(400, 150, text="Title", font=("Ariel", 40, "italic"))
card_word = canvas.create_text(400, 263, text="Word", font=("Ariel", 60, "bold"))
canvas.config(bg=BG_COLOR)
canvas.grid(row=0, column=0, columnspan=2)

### Buttons
wrong_button_image = PhotoImage(file="images/wrong.png")
right_button_image = PhotoImage(file="images/right.png")

unknown_button = Button(window, image=wrong_button_image, highlightthickness=0, command=next_card)
unknown_button.grid(row=1, column=0)

known_button = Button(window, image=right_button_image, highlightthickness=0, command=is_known)
known_button.grid(row=1, column=1)

### Chemam functia ca sa apara din prima cuvintele.
next_card()

window.mainloop()
