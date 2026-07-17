import tkinter as tk

WORK_TIME = 25 * 60
BREAK_TIME = 5 * 60

timer = WORK_TIME
running = False
on_break = False

def update_timer():
    global timer

    if running:
        mins = timer // 60
        secs = timer % 60
        label.config(text=f"{mins:02}:{secs:02}")

        if timer > 0:
            timer -= 1
        else:
            switch_timer()

        root.after(1000, update_timer)

def start():
    global running
    if not running:
        running = True
        update_timer()
def stop():
    global running
    if running:
        running = False
        update_timer()

def reset():
    global timer, running, on_break
    running = False
    on_break = False
    timer = WORK_TIME
    label.config(text="25:00")

def switch_timer():
    global timer, on_break
    on_break = not on_break

    if on_break:
        timer = BREAK_TIME
        title.config(text="Break Time")
    else:
        timer = WORK_TIME
        title.config(text="Focus Time")
def skip():
    switch_timer()

root = tk.Tk()
root.title("Pomodoro Timer")
root.geometry("300x250")

title = tk.Label(root, text="Focus Time", font=("Arial", 20))
title.pack(pady=20)

label = tk.Label(root, text="25:00", font=("Arial", 40))
label.pack()

start_button = tk.Button(root, text="Start", command=start)

start_button.pack(side='left',expand=True)

stop_button = tk.Button(root, text="Stop", command=stop)
stop_button.pack(side='left',expand=True)

skip_button = tk.Button(root, text="Skip", command=skip)
skip_button.pack(side='left',expand=True)

reset_button = tk.Button(root, text="Reset", command=reset)
reset_button.pack(side='left',expand=True)

root.mainloop()