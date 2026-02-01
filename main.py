import os #asks questions like: where's the file, how to build paths from code to file
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

#project_folder = os.path.abspath(__file__) #answers: where's the file by showing its physical location in the pc(full address)
project_folder = os.path.dirname(os.path.abspath(__file__))#taking only the file from the whole address
log_folder = os.path.join(project_folder, "logs")#joins the folder 'logs' with proper structure ('\')
os.makedirs(log_folder, exist_ok=True)#creates folder and checks if it exists
file_path = os.path.join(log_folder, "log.txt")#adds file 'log.txt' to folder path with structure

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
    plt.plot(dates, energies, marker='o', linestyle='-', color='teal')
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
        


while True:
    print("select: ")
    print("1. enter data \n2. view data \n3. graphical representation of data\n\ta) full data\n\tb) avg of 7 days \n4. exit")
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
    else:
        break