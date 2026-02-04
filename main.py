import os #asks questions like: where's the file, how to build paths from code to file
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

#project_folder = os.path.abspath(__file__) #answers: where's the file by showing its physical location in the pc(full address)
project_folder = os.path.dirname(os.path.abspath(__file__))#taking only the file from the whole address
#log_folder = os.path.join(project_folder, "logs")#joins the folder 'logs' with proper structure ('\')
#os.makedirs(log_folder, exist_ok=True)#creates folder and checks if it exists
#file_path = os.path.join(log_folder, "log.txt")#adds file 'log.txt' to folder path with structure; dont want to make log folder, just put data in log.txt
file_path = os.path.join(project_folder, "log.txt")

def data_enter(): #enter data into log.txt
    #date = input("enter today's date: ")#remove this, make date auto detect
    date = datetime.now().strftime("%Y-%m-%d")  
    task = input("enter task performed today: ")
    cycle_day = input("enter days after latest menstruation: ")# day 0 means the day period started, day 1...
    energy = int(input("enter energy levels during task(1-5): "))
    note = input("any notes: ")

    if energy<=3:
        feedback = ("low energy. rest up")
    else:
        feedback= ("high energy. maintain it.")
    print(feedback)

    reason = input("enter reason: ")

    with open(file_path, "a") as f:
        f.write(f"{date} | {task} | {cycle_day} | {energy} | {note} | {reason}\n")
    print(f"enter file path: {file_path}")#enter values


def view_all():
    with open(file_path, "r") as f:
        content = f.read()
    print(content)#display values   

def plot_data():
    dates = []
    energies = []

    if not os.path.exists(file_path):
        print("no data to plot yet")
        return
    with open(file_path, "r") as f:
        for line in f:
            parts = line.strip().split(" | ")
            if len(parts) >= 4:
                dates.append(parts[0])
                try:
                    energy = int(parts[3])
                    dates.append(parts[0])
                    energies.append(energy)
                except ValueError:
                    continue
    
    if not energies:
        print("energies not present")
        return
    plt.figure(figsize=(10,5))
    plt.plot(dates, energies, marker='o')
    plt.title("Energy Levels Over Time")
    plt.xlabel("Date")
    plt.ylabel("Energy (1-5)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def avg_energy_7():
    today = datetime.now().date()
    seven_days_ago = today - timedelta(days=7)

    energies = []

    with open(file_path, "r") as f:
        for line in f:
            parts = line.strip().split(" | ")
            if len(parts) >= 4:
                try:
                    log_date =datetime.strptime(parts[0], '%Y-%m-%d').date()
                    energy = int(parts[3])

                    if seven_days_ago <= log_date <= today:
                        energies.append(energy)

                except ValueError:
                    continue
    if not energies:
        print("No data available for the last 7 days.")
        return

    avg = sum(energies) / len(energies)
    print("Average energy (last 7 days):", round(avg, 2))
        

def edit_data():
    if not os.path.exists(file_path):
        print("no log found")
        return
    with open(file_path, "r") as f:
        lines = f.readlines()
    if not lines:
        print("data not present, cannot edit.")
        return 
    
    print("existing entries: ")
    for i, line in enumerate(lines):
        print(f"{i}:{line.strip()}")

    index = int(input("enter index of entry to edit: "))
    if index < 0 or index >= len(lines):
        print("invalid index")
        return
    
    parts = lines[index].strip().split(" | ")
    print("current values(press enter to keep the same): ")
    date = parts[0]
    task = input(f"task[{parts[1]}]: ") or parts[1]
    cycle_day = input(f"cycle day[{parts[2]}]: ") or parts[2]
    energy = input(f"energy[{parts[3]}]: ") or parts[3]
    note = input(f"note [{parts[4]}]: ") or parts[4]
    reason = input(f"reason [{parts[5]}]: ") or parts[5]

    edited_line = f"{date} | {task} | {cycle_day} | {energy} | {note} | {reason} | [EDITED]\n"
    with open(file_path, "a") as f:
        f.write(edited_line)

    print("entry entered and saved. Original entry preserved.")


while True:
    print("1. enter data \n2. view data \n3. graphical representation of data\n\ta) full data\n\tb) avg of 7 days \n4. edit data\n 5.exit")
    choice = int(input("choose: "))

    if choice == 1:
        data_enter()
    elif choice == 2:
        view_all()
    elif choice == 3:
        choose_plot = input("a or b: ")
        if choose_plot == 'a':
            plot_data()
        elif choose_plot == 'b':
            avg_energy_7()
    elif choice == 4:
        edit_data()
    else:
        break