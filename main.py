import time
import asyncio

def load_commands(filename):
    all_commands = [] 

    with open("commands.txt", "r") as file:
        for line in file:
            parts = line.split() # turns each row 00:05 10000 into a array ["00:05", "10000"]
            
            #converting the minutes and seconds input into total seconds
            timestamp = parts[0]
            m, s = timestamp.split(":")
            total_seconds = int(m) * 60 + int(s)
            
            #convert valve string "10100" to a list of Booleans
            #checks each character: if it's 1, it becomes True
            valve_string = parts[1]
            #goes through each valve value 1 or 0 in the string and turns it into either T or F
            tf_array = [char == "1" for char in valve_string]

            all_commands.append([total_seconds, tf_array])

        return all_commands
    
async def run_sequence(commands):
    print("--- Sequence Starting ----")
    #records the exact time that the test starts like a stopwatch
    start_time = time.perf_counter()
    #keeping track of which command we are waiting on
    current_index = 0
    #while loop to finish all commands in the list
    while current_index < len(commands):
        elapsed_time = time.perf_counter() - start_time

        target_time = commands[current_index][0]
        tf_flags = commands[current_index][1]

        if elapsed_time >= target_time:
            print(f"Time: {elapsed_time:.2f}s | Triggering Valves: {tf_flags}")
           
            # --- THIS IS WHERE YOU TRIGGER YOUR HARDWARE ---
            # Example: ValveActuate(tf_flags)
            
            # Move to the next command in the list

            current_index += 1
    print("--- Sequence Complete ---")


async def main():

    my_tasks = load_commands("commands.txt")
    
    await run_sequence(my_tasks)

if __name__ == "__main__":
    asyncio.run(main())
    