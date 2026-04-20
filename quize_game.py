import time
import threading #allows you to run code concurrently in separate threads.This is crucial for implementing the timeout functionality without freezing the main program.
import random # Importing the random module to generate random values
import string   # Importing the string module to access string constants like letters and digits
import os  # Importing os module to interact with the operating system (e.g., file existence check)
import matplotlib.pyplot as plt

print("""
============================================================
 Welcome to the Ultimate Quiz Game!

 Rules:
- Choose your category: Science, History, Sports, Movies, or Technology.
- Pick a difficulty: High / Moderate / Low.
- You have 10 seconds to answer each question.
- Every 3 questions, you may play a mini-game to boost your score!
- Earn points, rewards, and see your rank on the leaderboard!

Let's begin!
============================================================
""")

# ------------------ Timed Input ------------------
def timed_input(prompt, timeout=10):
    answer = [None]
    def get_input():#Gets input from the user and stores it in the 'answer' list.
        answer[0] = input(prompt) 
    thread = threading.Thread(target=get_input)
    thread.daemon = True # Allow the main thread to exit even if this thread is still running
    thread.start()
    thread.join(timeout)# Wait for the thread to complete or the timeout to expire
    if thread.is_alive():
        print("\n Time's up!")
        return None
    return answer[0]

# ------------------ Voucher Generator ------------------
def generate_voucher(prefix):
     # Generate a 4-character random string made up of uppercase letters and digits
    suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
     # Combine the given prefix and the random suffix with a hyphen in between, then return the result
    return f"{prefix}-{suffix}"

# ------------------ Word Scramble Mini-Game ------------------
def word_scramble():
    word = random.choice(["apple", "banana", "cherry", "grape"])
    scrambled = ''.join(random.sample(word, len(word)))
    print(f"Unscramble this word: {scrambled}")
    ans = input("Your answer: ").lower()
    if ans == word:
        print("Correct!")
        return 2
    else:
        print(f"Incorrect! The correct word was {word}.")
        return 0

# ------------------ Trivia Fact ------------------
def trivia_fact():
    facts = [
        "Did you know? The Eiffel Tower can be 15 cm taller during the summer.",
        "Trivia: Honey never spoils; pots found in ancient tombs are still edible.",
        "Trivia: Bananas are berries, but strawberries are not.",
    ]
    print(f"\n Trivia: {random.choice(facts)}")

# ------------------ Question Bank ------------------
question_bank = {
    "science": {
        "high": [
            ("What particle has no electric charge?", "b", ["A. Proton", "B. Neutron", "C. Electron", "D. Ion"]),
            ("Which gas is used in fluorescent lamps?", "a", ["A. Argon", "B. Oxygen", "C. Nitrogen", "D. CO2"]),
            ("What is the chemical symbol for gold?", "c", ["A. Go", "B. Ag", "C. Au", "D. Gd"]),
            ("Which planet has the most moons?", "d", ["A. Mars", "B. Earth", "C. Neptune", "D. Saturn"]),
            ("What part of the brain controls breathing?", "a", ["A. Medulla", "B. Cerebrum", "C. Cerebellum", "D. Thalamus"]),
        ],
        "moderate": [
            ("Which planet is closest to the Sun?", "c", ["A. Venus", "B. Earth", "C. Mercury", "D. Mars"]),
            ("Normal pH of human blood?", "b", ["A. 5.5", "B. 7.4", "C. 6.8", "D. 8.1"]),
            ("Which vitamin is produced by sunlight?", "a", ["A. Vitamin D", "B. Vitamin C", "C. Vitamin A", "D. Vitamin B12"]),
            ("What is HCl commonly known as?", "c", ["A. Bleach", "B. Acetic Acid", "C. Hydrochloric Acid", "D. Nitric Acid"]),
            ("Which organ purifies blood in the human body?", "d", ["A. Heart", "B. Lungs", "C. Intestine", "D. Kidney"]),
        ],
        "low": [
            ("Water boils at?", "a", ["A. 100°C", "B. 90°C", "C. 80°C", "D. 70°C"]),
            ("H2O is?", "a", ["A. Water", "B. Salt", "C. Oxygen", "D. Acid"]),
            ("Sun rises in the?", "c", ["A. South", "B. West", "C. East", "D. North"]),
            ("Our planet is called?", "a", ["A. Earth", "B. Mars", "C. Venus", "D. Moon"]),
            ("Animals that eat both plants and meat are?", "d", ["A. Herbivores", "B. Carnivores", "C. Insectivores", "D. Omnivores"]),
        ],
    },
    "history": {
        "high": [
            ("Who was the first Mughal Emperor?", "c", ["A. Akbar", "B. Aurangzeb", "C. Babur", "D. Shah Jahan"]),
            ("Who wrote Arthashastra?", "a", ["A. Chanakya", "B. Ashoka", "C. Kautilya", "D. Harsha"]),
            ("Where did Napoleon face final defeat?", "b", ["A. Trafalgar", "B. Waterloo", "C. Vienna", "D. Leipzig"]),
            ("Who discovered America?", "c", ["A. Magellan", "B. Vasco da Gama", "C. Columbus", "D. Drake"]),
            ("When did the French Revolution begin?", "a", ["A. 1789", "B. 1889", "C. 1689", "D. 1589"]),
        ],
        "moderate": [
            ("Year of American Independence?", "a", ["A. 1776", "B. 1876", "C. 1676", "D. 1976"]),
            ("Who built the Red Fort?", "b", ["A. Akbar", "B. Shah Jahan", "C. Humayun", "D. Jahangir"]),
            ("Who was India's first Prime Minister?", "c", ["A. Gandhi", "B. Rajendra Prasad", "C. Nehru", "D. Patel"]),
            ("Which war ended with the Treaty of Versailles?", "d", ["A. WW2", "B. Boer War", "C. Civil War", "D. WW1"]),
            ("Capital of Mauryan Empire?", "a", ["A. Pataliputra", "B. Delhi", "C. Agra", "D. Taxila"]),
        ],
        "low": [
            ("Taj Mahal was built by?", "b", ["A. Akbar", "B. Shah Jahan", "C. Jahangir", "D. Humayun"]),
            ("Mahatma Gandhi led?", "a", ["A. Dandi March", "B. Green Revolution", "C. Chipko Movement", "D. None"]),
            ("India got freedom in?", "c", ["A. 1950", "B. 1945", "C. 1947", "D. 1960"]),
            ("Who was the father of India?", "a", ["A. Gandhi", "B. Nehru", "C. Patel", "D. Bose"]),
            ("The Great Wall is in?", "b", ["A. India", "B. China", "C. Nepal", "D. Egypt"]),
        ],
    },
    "sports": {
        "high": [
            ("Which country has won most FIFA World Cups?", "c", ["A. Germany", "B. Italy", "C. Brazil", "D. France"]),
            ("First Indian to win Olympic gold?", "b", ["A. Milkha Singh", "B. Abhinav Bindra", "C. Neeraj Chopra", "D. Sachin"]),
            ("How many players in cricket team?", "a", ["A. 11", "B. 9", "C. 10", "D. 12"]),
            ("Which sport uses a puck?", "d", ["A. Football", "B. Baseball", "C. Basketball", "D. Ice Hockey"]),
            ("What is the full form of IPL?", "c", ["A. International Premier League", "B. Indoor Premier League", "C. Indian Premier League", "D. Independent Pro League"]),
        ],
        "moderate": [
            ("Olympics held every?", "d", ["A. 2 years", "B. 3 years", "C. Annually", "D. 4 years"]),
            ("How long is a football match?", "a", ["A. 90 minutes", "B. 60 minutes", "C. 80 minutes", "D. 70 minutes"]),
            ("What sport is Serena Williams famous for?", "b", ["A. Badminton", "B. Tennis", "C. Volleyball", "D. Table Tennis"]),
            ("Which sport has 'love' as a score?", "c", ["A. Badminton", "B. Cricket", "C. Tennis", "D. Basketball"]),
            ("Who is known as 'The God of Cricket'?", "a", ["A. Sachin Tendulkar", "B. Kohli", "C. Dhoni", "D. Dravid"]),
        ],
        "low": [
            ("Sport played with a bat and ball?", "a", ["A. Cricket", "B. Football", "C. Tennis", "D. Swimming"]),
            ("In which game do we use a net?", "b", ["A. Chess", "B. Volleyball", "C. Golf", "D. Boxing"]),
            ("Which game is played on ice?", "d", ["A. Rugby", "B. Baseball", "C. Cricket", "D. Ice Hockey"]),
            ("A soccer team has how many players?", "a", ["A. 11", "B. 6", "C. 9", "D. 12"]),
            ("Which game is known as 'The Gentleman's Game'?", "c", ["A. Football", "B. Basketball", "C. Cricket", "D. Rugby"]),
        ],
    },
    "movies": {
        "high": [
            ("First film to win 11 Oscars?", "a", ["A. Ben-Hur", "B. Avatar", "C. Titanic", "D. LOTR"]),
            ("Which movie has the line 'I'll be back'?", "b", ["A. Matrix", "B. Terminator", "C. Gladiator", "D. Predator"]),
            ("Actor who played Joker in 'The Dark Knight'?", "c", ["A. Bale", "B. Jared Leto", "C. Heath Ledger", "D. Joaquin"]),
            ("Director of 'Titanic'?", "d", ["A. Nolan", "B. Spielberg", "C. Tarantino", "D. Cameron"]),
            ("Movie with alien and flying bike scene?", "a", ["A. E.T.", "B. Star Wars", "C. Avatar", "D. Gravity"]),
        ],
        "moderate": [
            ("Who directed 'Inception'?", "b", ["A. Spielberg", "B. Nolan", "C. Cameron", "D. Tarantino"]),
            ("Which series has Harry Potter?", "c", ["A. Twilight", "B. Narnia", "C. Harry Potter", "D. LOTR"]),
            ("Who voiced Buzz Lightyear?", "a", ["A. Tim Allen", "B. Tom Hanks", "C. Will Smith", "D. Chris Pratt"]),
            ("Which is NOT a Marvel superhero?", "d", ["A. Iron Man", "B. Thor", "C. Spider-Man", "D. Batman"]),
            ("Which country made 'Parasite'?", "b", ["A. Japan", "B. South Korea", "C. China", "D. Thailand"]),
        ],
        "low": [
            ("Famous Disney mouse?", "a", ["A. Mickey", "B. Goofy", "C. Donald", "D. Jerry"]),
            ("Which is an animated movie?", "b", ["A. Titanic", "B. Frozen", "C. Jaws", "D. Matrix"]),
            ("Movie with talking lion?", "c", ["A. Nemo", "B. Bolt", "C. Lion King", "D. Tarzan"]),
            ("Which character has a magic wand?", "a", ["A. Harry Potter", "B. Iron Man", "C. Hulk", "D. Superman"]),
            ("Which is a superhero film?", "b", ["A. Frozen", "B. Spider-Man", "C. Inside Out", "D. Barbie"]),
        ],
    },
    "technology": {
        "high": [
            ("What does CPU stand for?", "a", ["A. Central Processing Unit", "B. Control Processing Unit", "C. Central Performance Unit", "D. Control Performance Unit"]),
            ("Which company introduced the first commercially successful microprocessor?", "a", ["A. Intel", "B. AMD", "C. IBM", "D. Motorola"]),
            ("Who conceptualized the Analytical Engine?", "a", ["A. Charles Babbage", "B. Alan Turing", "C. John von Neumann", "D. Ada Lovelace"]),
            ("What principle does Moore's Law state?", "a", ["A. Transistor count doubles every 18 months", "B. Processor speed doubles every 2 years", "C. Memory capacity doubles every year", "D. Storage cost halves every year"]),
            ("Which language is primarily used for system programming?", "b", ["A. Java", "B. C", "C. Python", "D. Ruby"]),
        ],
        "moderate": [
            ("What does RAM stand for?", "b", ["A. Read and Accessible Memory", "B. Random Access Memory", "C. Rapid Access Memory", "D. Random Archived Memory"]),
            ("Which part directs all computer operations?", "b", ["A. GPU", "B. CPU", "C. SSD", "D. PSU"]),
            ("What device modulates digital signals to analog?", "b", ["A. Router", "B. Modem", "C. Switch", "D. Hub"]),
            ("What is a malicious software that replicates itself?", "c", ["A. Worm", "B. Trojan", "C. Virus", "D. Spyware"]),
            ("Which is non-volatile storage?", "b", ["A. RAM", "B. Hard Disk Drive", "C. Cache", "D. Register"]),
        ],
        "low": [
            ("What does GPU stand for?", "a", ["A. Graphics Processing Unit", "B. General Processing Unit", "C. Graphical Primary Unit", "D. None"]),
            ("Which device points and clicks on a screen?", "c", ["A. Monitor", "B. Keyboard", "C. Mouse", "D. Speaker"]),
            ("Which one is an input device?", "b", ["A. Printer", "B. Mouse", "C. Speaker", "D. Monitor"]),
            ("Which one displays output on a computer?", "c", ["A. Keyboard", "B. Speaker", "C. Screen", "D. Hard Drive"]),
            ("What is the main circuit board called?", "a", ["A. Motherboard", "B. Router", "C. Modem", "D. Switch"]),
        ],
    }
}

play = input("Do you want to play? (yes/no): ").lower()
if play != "yes":
    print("Thanks for visiting!")
    quit()

num_players = int(input("How many players are playing? "))
players = [input(f"Enter Player {i+1} name: ").strip() for i in range(num_players)]

category = input("Choose a category: Science / History / Sports / Movies / Technology: ").lower()
difficulty = input("Choose difficulty: High / Moderate / Low: ").lower()

if category not in question_bank or difficulty not in question_bank[category]:
    print("Invalid category or difficulty. Please restart.")
    quit()

questions = question_bank[category][difficulty]
leaderboard_file = "leaderboard.txt"
player_scores = {}

for player_name in players:
    print(f"\n Now it's {player_name}'s turn!")
    score = 0
    question_no = 0
    start_time = time.time() 

    for q_text, correct_option, options in questions:
        question_no += 1
        print(f"\n{question_no}. {q_text}")
        for opt in options:
            print(opt)

        ans = timed_input("Your answer (A/B/C/D): ", 10)

        if ans and ans.lower() == correct_option:
            score += 1
            print(" Correct!")
        else:
            print(f" Incorrect! Correct answer is --> {correct_option.upper()}")

        if question_no % 3 == 0:
            if input("Do you want to play a mini-game? (yes/no): ").lower() == "yes":
                mini_game_points = word_scramble()
                score += mini_game_points
                print(f"Total Points after mini-game: {score}")
            trivia_fact()

    end_time = time.time()
    total_time = end_time - start_time

    try:
        percentage = (score * 100) / question_no
    except ZeroDivisionError:
        percentage = 0

    reward = ""
    voucher = ""

    if percentage >= 90:
        reward = " Gold Medal +  $50 Gift Card"
        voucher = generate_voucher("GOLD")
    elif 75 <= percentage < 90:
        reward = " Silver Medal +  $20 Discount Coupon"
        voucher = generate_voucher("SILV")
    elif 50 <= percentage < 75:
        reward = " Bronze Medal +  E-Certificate"
        voucher = generate_voucher("BRNZ")
    else:
        reward = " Better luck next time! Keep practicing!"

    print(f"\n🏱 Reward for {player_name}: {reward}")
    if voucher:
        print(f" Your Voucher Code: {voucher}")

    with open(leaderboard_file, "a", encoding="utf-8") as file:
        file.write(f"{player_name} - {score}/{question_no} - {percentage:.2f}% - {int(total_time)}s - {reward} - Voucher: {voucher}\n")

    player_scores[player_name] = score

print("\n Leaderboard:")
# Check if the leaderboard file exists
if os.path.exists(leaderboard_file):
    # Open the file in read mode with UTF-8 encoding
    with open(leaderboard_file, "r", encoding="utf-8") as file:
        # Read the entire content of the file and print it to the consoleyes
        print(file.read())

 # ------------------ Leaderboard Chart ------------------

# Read leaderboard data
if os.path.exists(leaderboard_file):
    with open(leaderboard_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    names = []
    scores = []
    for line in lines:
        try:
            name, score_part = line.strip().split(" - ")
            score = int(score_part.split("/")[0])
            names.append(name)
            scores.append(score)
        except:
            continue

    if names:
        plt.figure(figsize=(10, 6))
        bars = plt.barh(names, scores, color='skyblue')
        plt.xlabel("Scores")
        plt.ylabel("Players")
        plt.title("Leaderboard")
        plt.tight_layout()

        # Annotate bars with scores
        for bar, score in zip(bars, scores):
            plt.text(score + 0.1, bar.get_y() + bar.get_height()/2, str(score), va='center')

        plt.show()
    else:
        print("No leaderboard data to display.")
else:
    print("Leaderboard file not found.")
       

# ------------------ Plot All Players' Scores ------------------
def plot_all_scores(score_dict, total_questions):
    names = list(score_dict.keys())
    scores = list(score_dict.values())

    plt.figure(figsize=(10, 5))
    bars = plt.bar(names, scores, color='skyblue')
    plt.ylim(0, total_questions)
    plt.title(" Players' Quiz Performance")
    plt.xlabel("Players")
    plt.ylabel("Score")
    plt.axhline(y=total_questions/2, color='red', linestyle='--', label='Average')
    plt.legend()

    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval + 0.1, int(yval), ha='center')

    plt.tight_layout()
    plt.show()

plot_all_scores(player_scores, len(questions))
print("\nThanks for playing! Come back soon for more challenges! 🎮")
