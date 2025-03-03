import tkinter as tk
import random

global Grid_letters, stage, time_remaining, won # These variables will be used in the submission function.

stage = 1
time_remaining = 60
won = 0 # Changes to '1' if the player wins, which stops the timer from counting down.

alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

"""
We generate a puzzle with number of letters equal to the current stage (which I will call k).
- We sample k letters from the alphabet.
- We sample k numbers from 0 to 24, which will indicate where to place the letters in the grid.
- Then these pairs of letters and positions are placed into the grid.
- The variable "letters" contains a list with the grid in order at the end of the process.
"""
def generate_stage(stage):
    letters = [None] * 25
    sample_letters = random.sample(alphabet, stage) # Sample k letters from the alphabet
    sample_positions = random.sample(range(25), stage) # Sample k positions from 0 to 24 for these letters
    for i in range(stage):
        letters[sample_positions[i]] = sample_letters[i] # Place i'th generated letter into i'th generated position
    return letters

"""
Update the grid when the player completes a stage, to match the new generated grid.
- The 'display_references' store references for the labels in the grid.
- We update each label to show the letter in the newly generated grid.
"""
def update_grid(letters):
    for i in range(25):
        if letters[i] == None:
            display_references[i].config(text="")
        else:
            display_references[i].config(text=letters[i])

"""
Submit the current letter.
"""
def submit(event):
    global Grid_letters, stage, time_remaining, won # We need to be able to change these variables when we move to the next stage or apply a time penalty.
    
    inp = answer.get().upper() # Get what the user inputted (and normalise to uppercase).
    answer.delete(0, tk.END) # OPTIONAL - Clear the answer box. You may find it faster to play with this disabled.
    if time_remaining > 0:
        if inp in alphabet and len(inp) == 1:  # Ensure input is a single letter.
            if inp in Grid_letters: # If the input is in the grid, the answer is incorrect.
                feedback.config(text="Incorrect - 5 second penalty", fg="red") # Change feedback to say wrong answer.
                time_remaining = time_remaining - 5
            else:
                feedback.config(text="Correct", fg="white") # Change feedback to say correct answer.
                stage = stage + 1
                if stage < 26:
                    Grid_letters = generate_stage(stage) # Generate a new stage...
                    update_grid(Grid_letters) #...then update the grid.
                else: # 25 stages have been completed
                    answer.config(state="disabled") # Disable input, because the game is over. Then we change displays to be green for the win screen.
                    for i in range(25):
                        display_references[i].config(text="*", bg="#00FF00")
                    feedback.config(text="You win!", fg="black", bg="#00FF00")
                    timer_display.config(fg="black", bg="#00FF00")
                    root.config(background="green")
                    won = 1
                    
        else:
            feedback.config(text="Input one letter only.", fg="yellow")

"""
The timer, to be shown at the bottom of the game, and count down by 1 per second.
"""
def timer():
    global stage, time_remaining, won

    if time_remaining > 0 and won == 0: # If the game has not ended...
        time_remaining -= 1 # Tick down the timer
        timer_display.config(text=f"Time left: {time_remaining}") # Update the timer display to show the new time
        root.after(1000, timer) # After 1000 milliseconds, activate the timer again to remove another second.
    elif won == 0: # The game has ended. If it is not because the player won, then it means the time ran out.
        for i in range(25):
                        display_references[i].config(text="X", bg="#222222")
        timer_display.config(text="Time expired.") # Disable input, because the game is over, and turn displays red for the loss screen.
        feedback.config(text=f"Time up! You reached stage: {stage}", fg="red", bg="#222222")
        timer_display.config(fg="red", bg="#222222")
        answer.config(state="disabled")

Grid_letters = generate_stage(stage) # Generate a puzzle for stage 1.

root = tk.Tk() # Make main window.
root.configure(background="blue") # Make main window blue.

display_references = [] # We need references for our grid labels, so that we can change them when the player moves on to the next stage.
    
for i in range(5):
    for j in range(5):
        index = i * 5 + j # Iterate through the grid in reading order.
        display = tk.Label(root, text=Grid_letters[index], relief="raised", bg="blue", fg="white", width=2, height=1, font=("Futura", 72, "bold"))
        display.grid(row=i, column=j) # Put the label in the right place for reading order 5x5 grid.
        display_references.append(display) # Set a reference, so we can update the letter later.

answer = tk.Entry(root, width=15) # Make an entry box for the answer.
answer.grid(row=5,column=2)
answer.bind("<Return>", submit) # Submit the answer with submit function when the player presses Enter.

feedback = tk.Label(root, text="Submit any letter not present in the grid.", bg="blue", fg="white", font=("Arial", 24))
feedback.grid(row=6, column=0, columnspan=5)

timer_display = tk.Label(root, text=f"Time left: {time_remaining}", bg="blue", fg="white", font=("Arial", 24, "bold"))
timer_display.grid(row=7, column=0, columnspan=5) # This timer display will be changed later by the timer function.

timer() # Start the timer ticking.
    
root.mainloop()

