import socket
import time
import random
from datetime import datetime

HOST = 'localhost'  # Or your Boundary proxy address
PORT = 33761
SLEEP_DELAY = 10.0  # Initial estimate - crucial to adjust this
MIN_NUMBER = 0
MAX_NUMBER = 54321

def play_game():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        f = s.makefile('rwb')

        # Read initial messages
        for i in range(5):
            print(f.readline().decode('utf-8').strip())

        # Initial game setup
        game_counter = 1
        start_time = None

        while True:
            # Get game prompt
            print(f.readline().decode('utf-8').strip())
            print(f.readline().decode('utf-8').strip())
            print(f.readline().decode('utf-8').strip())
            print(f.readline().decode('utf-8').strip())

            if start_time is None:
                # First guess: Seed based on *current* time
                start_time = datetime.now()
                initial_seed = int((start_time.timestamp() * 1000000)) % 1000000
                random.seed(initial_seed)
                predicted_number = random.randint(MIN_NUMBER, MAX_NUMBER)
                print(f"Game {game_counter}: Initial guess based on current time")
            else:
                # Subsequent guesses: Predict based on SLEEP_DELAY
                seed_time = start_time.timestamp() + SLEEP_DELAY
                predicted_seed = int((seed_time * 1000000)) % 1000000
                random.seed(predicted_seed)
                predicted_number = random.randint(MIN_NUMBER, MAX_NUMBER)
                print(f"Game {game_counter}: Predicting with SLEEP_DELAY = {SLEEP_DELAY}")

            # Send guess
            guess_str = str(predicted_number) + '\n'
            f.write(guess_str.encode('utf-8'))
            f.flush()
            print(f"Guessing: {predicted_number}")

            # Get response
            response = f.readline().decode('utf-8').strip()
            print(response)

            if "You guessed right!" in response:
                # Extract and print the flag
                flag = f.readline().decode('utf-8').strip()
                print("Flag:", flag)
                break
            else:
                # Update start_time *after* receiving incorrect response
                f.readline()
                f.readline()
                f.readline()
                start_time = datetime.now()

                #Adjust the sleep delay
                SLEEP_DELAY = 10.0

                game_counter += 1

if __name__ == "__main__":
    play_game()
