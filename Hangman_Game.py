from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import random
import webbrowser

root = Tk()
root.title("Hangman")
root.iconbitmap('Resources/Media/Icon/Hangman_Game_Icon.ico')
root.resizable(0, 0)


def movies_dict():
    file = open("Resources/Data/movies.txt", "r")
    temp_dict = {}
    for line in file.readlines():
        li = line.split("=")
        rl_and_h = li[1].split(".")
        temp_dict[li[0]] = [rl_and_h[0], rl_and_h[1]]
    file.close()
    return temp_dict


file = open("Resources/Saves/last_game.txt", "r")
temp_dict = {}
for line in file.readlines():
    li = line.split("=")
    li.append("")
    temp_dict[li[0]] = "".join(li[1].split("\n"))
file.close()

movie = temp_dict["movie"]
hint_for_movie = temp_dict["hint_for_movie"]
release_year = temp_dict["release_year"]
result = temp_dict["result"]
display_line = temp_dict["display_line"]
right_answer = temp_dict["right_answer"]
letters_in_movie = temp_dict["letters_in_movie"].split(".")
correct_guesses = temp_dict["correct_guesses"].split(".")
wrong_guesses = temp_dict["wrong_guesses"].split(".")
mistakes = int(temp_dict["mistakes"])
streak = int(temp_dict["streak"])
played_level = bool(int(temp_dict["played_level"]))
skipped_level = bool(int(temp_dict["skipped_level"]))
game_ended = int(temp_dict["game_ended"])

title_label = Label(root, text="Hangman", justify=CENTER, font="Times 32")
title_label.grid(row=0, column=0, columnspan=2, padx=20)

streak_label = Label(root, text="Streak: " + str(streak))
streak_label.grid(row=0, column=3, columnspan=2, padx=10)

guess_field = Entry(root, width=2, font=20)
guess_field.grid(row=1, column=0, padx=10)

release_year_label = Label(root, text="Release Year: " + release_year, justify=CENTER)
release_year_label.grid(row=3, column=0, padx=10)

hint_for_movie_label = Label(root, text="Hint: " + hint_for_movie, justify=CENTER)
hint_for_movie_label.grid(row=3, column=1, padx=10)

result_label = Label(root, text=result, wraplength=120, justify=CENTER)
result_label.grid(row=4, column=0, columnspan=2, rowspan=2, padx=10)

if wrong_guesses != [""]:
    wrong_guesses_label = Label(root, text="" + " ".join([l.upper() for l in wrong_guesses]), justify=CENTER)
    wrong_guesses_label.grid(row=5, column=2, columnspan=2, padx=10)

display_line_label = Label(root, text=display_line, font="Calibri 16")
display_line_label.grid(row=2, column=0, columnspan=2, padx=10)

stage_0 = ImageTk.PhotoImage(Image.open("Resources/Media/Stages/Stage_0_White_Background.png"))
stage_1 = ImageTk.PhotoImage(Image.open("Resources/Media/Stages/Stage_1_White_Background.png"))
stage_2 = ImageTk.PhotoImage(Image.open("Resources/Media/Stages/Stage_2_White_Background.png"))
stage_3 = ImageTk.PhotoImage(Image.open("Resources/Media/Stages/Stage_3_White_Background.png"))
stage_4 = ImageTk.PhotoImage(Image.open("Resources/Media/Stages/Stage_4_White_Background.png"))
stage_5 = ImageTk.PhotoImage(Image.open("Resources/Media/Stages/Stage_5_White_Background.png"))
stage_6 = ImageTk.PhotoImage(Image.open("Resources/Media/Stages/Stage_6_White_Background.png"))

images = [stage_0, stage_1, stage_2, stage_3, stage_4, stage_5, stage_6]

stage = Label(root, image=images[mistakes], bg="White")
stage.grid(row=1, column=2, columnspan=3, rowspan=3)


def save_game():
    global movie, hint_for_movie, release_year, result, display_line, right_answer, letters_in_movie
    global correct_guesses, wrong_guesses, mistakes, streak, played_level, skipped_level, temp_dict
    file = open("Resources/Saves/last_game.txt", "w")
    data = "movie=" + movie + "\nhint_for_movie=" + hint_for_movie + "\nrelease_year=" + release_year + \
           "\nresult=" + result + "\ndisplay_line=" + display_line + "\nright_answer=" + right_answer + \
           "\nletters_in_movie=" + ".".join(letters_in_movie) + "\ncorrect_guesses=" + ".".join(correct_guesses) + \
           "\nwrong_guesses=" + ".".join(wrong_guesses) + "\nmistakes=" + str(mistakes) + "\nstreak=" + str(streak) + \
           "\nplayed_level=" + str(int(played_level)) + "\nskipped_level=" + str(int(skipped_level)) + "\ngame_ended=" \
           + str(game_ended)
    file.write(data)


def update_streak_label():
    global mistakes, streak_label, streak, result, skipped_level
    if skipped_level or mistakes > 0:
        streak = 0
    # dotenv.set_key("Resources/Saves/last_game.txt", "streak", str(streak))
    streak_label.grid_forget()
    streak_label = Label(root, text="Streak: " + str(streak))
    streak_label.grid(row=0, column=3, columnspan=2, padx=10)


def update_stage():
    global mistakes, stage
    stage.grid_forget()
    stage = Label(root, image=images[mistakes])
    stage.grid(row=1, column=2, columnspan=3, rowspan=3)


def update_display_line():
    global display_line
    global display_line_label
    display_line_label.grid_forget()
    display_line_label = Label(root, text=display_line, font="Calibri 16")
    display_line_label.grid(row=2, column=0, columnspan=2, padx=10)


def update_result():
    global result_label
    result_label.grid_forget()
    result_label = Label(root, text=result, wraplength=120, justify=CENTER)
    result_label.grid(row=4, column=0, columnspan=2, rowspan=2, padx=10)


def update_wrong_guesses_label():
    global wrong_guesses_label
    if mistakes == 1:
        wrong_guesses_label.grid_forget()
        wrong_guesses_label = Label(root, text="Wrong Guess: " + " ".join([l.upper() for l in wrong_guesses]),
                                    justify=CENTER)
        wrong_guesses_label.grid(row=5, column=2, columnspan=2, padx=10)
    elif mistakes > 1:
        wrong_guesses_label.grid_forget()
        wrong_guesses_label = Label(root, text="Wrong Guesses: " + " ".join([l.upper() for l in wrong_guesses]),
                                    justify=CENTER)
        wrong_guesses_label.grid(row=5, column=2, columnspan=2, padx=10)


def new_game(x=""):
    global movie, result, letters_in_movie, correct_guesses, wrong_guesses, mistakes, display_line, guess_field
    global try_guess, right_answer, wrong_guesses_label, hint_for_movie, release_year
    global release_year_label, hint_for_movie_label, played_level, skipped_level, game_ended

    game_ended = 0
    root.bind('<Return>', check_guess)

    if played_level:
        skipped_level = False
    else:
        skipped_level = True
    played_level = False

    prev_movie = movie
    movies = movies_dict()
    mv = random.choice(list(movies.keys()))
    mv_words = mv.split("_")
    movie = " ".join(["".join([":" if letter == "." else letter for letter in word]) for word in mv_words]).lower()

    while movie == prev_movie:
        mv = random.choice(list(movies.keys()))
        mv_words = mv.split("_")
        movie = " ".join(["".join([":" if letter == "." else letter for letter in word]) for word in mv_words]).lower()

    letters_in_movie = list(set([letter for letter in movie if letter.isalpha()]))
    release_year = movies[mv][0]
    hint_for_movie = "".join((" ".join(movies[mv][1].split("_"))).split("\n"))
    right_answer = " ".join([letter + " " for letter in movie])

    result = ""
    mistakes = 0
    correct_guesses = []
    wrong_guesses = []

    display_line = "".join(["_ " if letter in "abcdefghijklmnopqrstuvwxyz" else letter + " " for letter in movie])

    update_streak_label()
    update_result()
    update_display_line()
    update_stage()

    guess_field = Entry(root, width=2, font=20, borderwidth=5)
    guess_field.grid(row=1, column=0, padx=10)

    try_guess = Button(root, text="Try!", command=check_guess, cursor="hand2")
    try_guess.grid(row=1, column=1)

    try:
        wrong_guesses_label.grid_forget()
    except NameError:
        pass
    wrong_guesses_label = Label(root, text="", justify=CENTER)
    wrong_guesses_label.grid(row=5, column=2, columnspan=2, padx=10)

    release_year_label.grid_forget()
    release_year_label = Label(root, text="Release Year: " + release_year, justify=CENTER)
    release_year_label.grid(row=3, column=0, padx=10)

    hint_for_movie_label.grid_forget()
    hint_for_movie_label = Label(root, text="Hint: " + hint_for_movie, justify=CENTER)
    hint_for_movie_label.grid(row=3, column=1, padx=10)


def game_end():
    global guess_field, try_guess, played_level, skipped_level, game_ended
    played_level = True
    skipped_level = False
    guess_field.grid_forget()
    guess_field = Entry(root, width=2, font=20, state=DISABLED, cursor="X_cursor")
    guess_field.grid(row=1, column=0, padx=10)
    try_guess.grid_forget()
    try_guess = Button(root, text="Try!", state=DISABLED, cursor="X_cursor")
    try_guess.grid(row=1, column=1)
    game_ended = 1
    root.bind('<Return>', new_game)
    save_game()


def check_guess(x=""):
    global display_line, letters_in_movie, guess_field, mistakes, result, correct_guesses, wrong_guesses, right_answer
    global streak
    guess = guess_field.get()
    guess = guess.lower()
    if guess in letters_in_movie:
        if guess in correct_guesses:
            result = "You have already guessed that letter :)"
        else:
            display_line = ""
            correct_guesses.append(guess)
            for letter in movie:
                if letter == guess or letter in correct_guesses or not letter.isalpha():
                    display_line += letter + " "
                else:
                    display_line += "_ "
            if "".join(display_line.split()) == "".join(movie.split()):
                result = "You win!!"
                if mistakes == 0:
                    streak += 1
                game_end()
            else:
                result = "Right guess"
    else:
        if guess in wrong_guesses:
            result = "You have already tried this letter!"
        elif not guess.isalpha():
            result = "Invalid Input"
        elif len(guess) == 0:
            result = "You didn't enter any value."
        elif len(guess) > 1:
            result = "You can only guess one letter at a time."
        else:
            streak = 0
            if mistakes < 5:
                wrong_guesses.append(guess)
                mistakes += 1
                result = "Wrong guess!! :("
            else:
                mistakes += 1
                wrong_guesses.append(guess)
                result = "Game Over!!!\n The movie was:\n" \
                         + " ".join([word[0].upper() + word[1:] for word in movie.split()])
                update_stage()
                update_wrong_guesses_label()
                game_end()
    guess_field.delete(0, END)
    update_result()
    update_wrong_guesses_label()
    update_display_line()
    update_stage()
    update_streak_label()


def quit_game():
    save_game()

    ask = messagebox.askyesno("Hangman", "Do you want to quit the game?")
    if ask:
        root.quit()


root.bind('<Return>', check_guess)


if movie == "" or game_ended:
    new_game()

try_guess = Button(root, text="Try!", command=check_guess, cursor="hand2")
try_guess.grid(row=1, column=1)

button_new_game = Button(root, text="New Game", command=new_game, cursor="hand2")
button_new_game.grid(row=6, column=0, padx=10, pady=20)

button_quit_game = Button(root, text="Quit Game", command=quit_game, cursor="hand2")
button_quit_game.grid(row=6, column=2, padx=10, pady=20)

credit_img = Image.open("Resources/Media/Credits/Credit.PNG")
credit_img = credit_img.resize((229, 30), Image.ANTIALIAS)
credit_image = ImageTk.PhotoImage(credit_img)


def go_to(url):
    webbrowser.open_new_tab(url)


footer_label = Button(root, image=credit_image, bg="White",
                      command=lambda: go_to("https://cyantarantula.github.io/My-Portfolio/"), cursor="hand2")
footer_label.grid(row=7, column=0, columnspan=5, padx=10, pady=5)

root.mainloop()
