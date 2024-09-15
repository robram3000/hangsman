import tkinter as tk
from customtkinter import CTk, CTkButton, CTkLabel, CTkFrame, CTkImage
import random
from PIL import Image
import time

countries_with_hints = {
    "CANADA": "Known for maple syrup and hockey.",
    "FRANCE": "Famous for the Eiffel Tower and French cuisine.",
    "GERMANY": "Known for Oktoberfest and sausages.",
    "ITALY": "Famous for pasta, pizza, and the Colosseum.",
    "JAPAN": "Known for sushi, cherry blossoms, and anime.",
    "BRAZIL": "Famous for its carnivals and soccer.",
    "INDIA": "Known for its diverse culture and spicy cuisine.",
    "CHINA": "Famous for the Great Wall and Chinese cuisine.",
    "RUSSIA": "Known for its vast size and rich history.",
    "SPAIN": "Famous for its bullfighting and flamenco dancing.",
    "AUSTRALIA": "Known for kangaroos, koalas, and the Outback.",
    "UNITED STATES": "Famous for its diverse landscape and Hollywood.",
    "UNITED KINGDOM": "Known for the Royal Family and Big Ben.",
    "EGYPT": "Famous for the pyramids and the Sphinx.",
    "MEXICO": "Known for its tacos, tequila, and mariachi music."
}

class HangmanGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Hangman: Guess the Country")
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width // 2) - (800 // 2)
        y = (screen_height // 2) - (505 // 2)
        self.root.geometry(f"{800}x{505}+{x}+{y}")
        self.load_checkpoint()
        self.create_start_screen()

    def load_checkpoint(self):
        self.level = 1
        self.country, self.hint = random.choice(list(countries_with_hints.items()))
        self.guesses = set()
        self.incorrect_guesses = 0
        self.max_incorrect = 5

    def create_start_screen(self):
        image_path = "Weather/hangsman/hangmans.jpg" 
        pil_image = Image.open(image_path)
        ctk_image = CTkImage(pil_image, size=(800, 505))
        self.clear_screen()

        main_frame = CTkFrame(master=self.root, width=800, height=505)
        main_frame.place(x=0, y=0)

        self.background = CTkLabel(master=main_frame, image=ctk_image, text="")
        self.background.place(relx=0.5, rely=0.5, anchor="center")
      
        self.start_button = CTkButton(self.root, text="Start", command=self.start_game, font=("Helvetica", 12), fg_color="Black", hover_color="#666563", width=130, height=30, bg_color="#515151")
        self.start_button.place(relx=0.12, rely=0.54, anchor="center")

        self.quit_button = CTkButton(self.root, text="Quit", command=self.quit_game, font=("Helvetica", 12), fg_color="Black", hover_color="#666563", width=130, height=30, bg_color="#515151")
        self.quit_button.place(relx=0.12, rely=0.62, anchor="center")

    def start_game(self):
        self.clear_screen()
        self.create_widgets()
        self.update_display()
        self.start_timer()

    def create_widgets(self):
        self.word_display = CTkLabel(self.root, font=("Helvetica", 20))
        self.word_display.place(relx=0.5, rely=0.6, anchor="center")

        self.hangman_display = CTkFrame(self.root, width=250, height=250, fg_color="#4f4f4d")
        self.hangman_display.place(relx=0.5, rely=0.28, anchor="center")

        self.hint_label = CTkLabel(self.root, text=f"Hint: {self.hint}", font=("Helvetica", 12))
        self.hint_label.place(relx=0.5, rely=0.65, anchor="center")

        self.message_label = CTkLabel(self.root, font=("Helvetica", 10), text="")
        self.message_label.place(relx=0.5, rely=0.69, anchor="center")

        self.timer_label = CTkLabel(self.root, font=("Helvetica", 16))
        self.timer_label.place(relx=0.33, rely=0.75, anchor="center")

        self.attempts_label = CTkLabel(self.root, font=("Helvetica", 16), text=f"Attempts: {self.incorrect_guesses}/{self.max_incorrect}")
        self.attempts_label.place(relx=0.75, rely=0.75, anchor="center")

        self.button_frame = CTkFrame(self.root )
        self.button_frame.place(relx=0.5, rely=0.89, anchor="center")

        self.create_buttons()

    def create_buttons(self):
        def generate_random_letters(length):
            letters = [chr(i) for i in range(65, 91)]
            return random.choices(letters, k=length)

        country_letters = list(self.country)
        random_letters = generate_random_letters(20 - len(country_letters))
        button_letters = country_letters + random_letters

        random.shuffle(button_letters)

        self.buttons = {}
        for i in range(20):
            button_text = button_letters[i]
            button = CTkButton(self.button_frame, text=button_text, command=lambda bt=button_text: self.make_guess(bt), width=40, height=40)
            button.grid(row=i // 10, column=i % 10, padx=5, pady=5)
            self.buttons[button_text] = button

        for button in self.buttons.values():
            button.configure(state="normal")

    def draw_hangman(self):
        if not hasattr(self, 'canvas'):
            self.canvas = tk.Canvas(self.hangman_display, width=500, height=250, bg=self.hangman_display.cget("fg_color"))
            self.canvas.pack()
        else:
            self.canvas.delete("all")

        if self.incorrect_guesses >= 1:
            self.draw_arc(55, 215, 205, 235)
            self.draw_line(130, 225, 130, 55)

        if self.incorrect_guesses >= 2:
            self.draw_line(130, 55, 205, 55)

        if self.incorrect_guesses >= 3:
            self.draw_line(167.5, 55, 167.5, 80)
            self.draw_oval(150, 80, 200, 130)

        if self.incorrect_guesses >= 4:
            self.draw_line(167.5, 155, 142.5, 175)
            self.draw_line(167.5, 155, 192.5, 175)

        if self.incorrect_guesses >= 5:
            self.draw_line(175, 200, 150, 220)
            self.draw_line(175, 200, 200, 220)

    def draw_arc(self, x1, y1, x2, y2):
        self.canvas.create_arc(x1, y1, x2, y2, start=0, extent=180, width=10, style='arc', outline='Black')
        self.root.update()
        time.sleep(0.5)

    def draw_line(self, x1, y1, x2, y2):
        self.canvas.create_line(x1, y1, x2, y2, width=10, fill='Black')
        self.root.update()
        time.sleep(0.5)

    def draw_oval(self, x1, y1, x2, y2):
        self.canvas.create_oval(x1, y1, x2, y2)
        self.root.update()
        time.sleep(0.5)

    def update_display(self):
        if hasattr(self, 'country'): 
            display_word = " ".join(letter if letter in self.guesses else "_" for letter in self.country)
        else:
            display_word = ""
        self.word_display.configure(text=display_word)
        self.attempts_label.configure(text=f"Attempts: {self.incorrect_guesses}/{self.max_incorrect}")

        if display_word.replace(" ", "") == self.country:
            self.message_label.configure(text=f"Congratulations! You guessed the country: {self.country}!", text_color="green")
            self.disable_input()
            self.stop_timer()
            self.clear_message_label()
            self.reset_game()  
            return

        if self.incorrect_guesses >= self.max_incorrect:
            self.message_label.configure(text=f"You lost! The country was {self.country}.", text_color="red")
            self.disable_input()
            self.stop_timer()
            self.gameover()

    def update_word_display(self):
        if hasattr(self, 'country'): 
            display_word = " ".join(letter if letter in self.guesses else "_" for letter in self.country)
        else:
            display_word = ""
        self.word_display.configure(text=display_word)

    def gameover(self):
        self.clear_screen()

        gameover_image_path = "Weather/hangsman/gameover.png"
        gameover_image = Image.open(gameover_image_path)
        gameover_ctk_image = CTkImage(gameover_image, size=(800, 505))

        gameover_frame = CTkFrame(master=self.root, width=800, height=505)
        gameover_frame.place(x=0, y=0)

        self.gameover_background = CTkLabel(master=gameover_frame, image=gameover_ctk_image, text="")
        self.gameover_background.place(relx=0.5, rely=0.5, anchor="center")

        play_again_button = CTkButton(self.root, text="Play Again", command=self.start_game, font=("Helvetica", 12), fg_color="#736969", hover_color="#666563", width=130, height=30, bg_color="#736969",text_color="Black" )
        play_again_button.place(relx=0.5, rely=0.7, anchor="center")

        quit_button = CTkButton(self.root, text="Quit", command=self.quit_game, font=("Helvetica", 12), fg_color="#736969", hover_color="#666563", width=130, height=30, bg_color="#736969",text_color="Black")
        quit_button.place(relx=0.5, rely=0.8, anchor="center")

    def make_guess(self, guess):
        guess = guess.upper()
        if guess in self.guesses:
            self.message_label.configure(text="You already guessed that letter.", text_color="orange")
            return
        self.guesses.add(guess)

        if guess in self.country:
            self.message_label.configure(text=f"Good guess! {guess} is in the word.", text_color="green")
        else:
            self.incorrect_guesses += 1
            self.message_label.configure(text=f"Incorrect guess! {guess} is not in the word.", text_color="red")

        self.draw_hangman()
        self.update_display()

    def clear_message_label(self):
        self.message_label.configure(text="", text_color="black")
        
    def disable_input(self):
        for button in self.buttons.values():
            button.configure(state="disabled")

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def start_timer(self):
        self.time_remaining = 60
        self.update_timer()

    def update_timer(self):
        if self.time_remaining > 0:
            self.timer_label.configure(text=f"Time Remaining: {self.time_remaining} seconds")
            self.time_remaining -= 1
            self.timer_id = self.root.after(1000, self.update_timer)
        else:
            self.message_label.configure(text=f"Time's up! The country was {self.country}.", text_color="red")
            self.disable_input()
            self.stop_timer()
            self.gameover()

    def stop_timer(self):
        if hasattr(self, 'timer_id'):
            self.root.after_cancel(self.timer_id)

    def reset_game(self):
        print("Resetting game...")
        self.country, self.hint = random.choice(list(countries_with_hints.items()))
        self.guesses = set()
        self.incorrect_guesses = 0
        self.stop_timer()
        self.start_timer()
        self.hint_label.configure(text=f"Hint: {self.hint}")
        self.attempts_label.configure(text=f"Attempts: {self.incorrect_guesses}/{self.max_incorrect}")
        self.clear_message_label()
        self.update_word_display()  
        for button in self.buttons.values():
            button.destroy()
        self.create_buttons()
        print("Game reset.")
        
        self.root.after(2000, self.clear_message_label)

    def quit_game(self):
        self.root.destroy()

if __name__ == "__main__":
    root = CTk()
    game = HangmanGame(root)
    root.mainloop()
