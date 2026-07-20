import os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import simpledialog
WORK_TIME = 25 * 60
BREAK_TIME = 5 * 60
task_count = 1          
task_start_y = 94      
task_spacing = 35       
time_left = WORK_TIME
running = False
on_break = False

def update_timer():
    global time_left

    if running:
        mins = time_left // 60
        secs = time_left % 60
        timer_label.config(text=f"{mins:02}:{secs:02}")

        if time_left > 0:
            time_left -= 1
        else:
            switch_timer()

        main.after(1000, update_timer)

def toggle_timer():
    global running

    if running:
        running = False
        pressplay.config(text="Start")
    else:
        running = True
        pressplay.config(text="Pause")
        update_timer()
def rename_task(checkbox):
    new_name = simpledialog.askstring(
        "Rename Task",
        "New task name:",
        initialvalue=checkbox.cget("text")
    )

    if new_name:
        checkbox.config(text=new_name)
    
def reset():
    global time_left, running, on_break
    running = False
    on_break = False
    time_left = WORK_TIME
    timer_label.config(text="25:00")
    block_type.config(text="Focus Time")
def switch_timer():
    global time_left, on_break
    on_break = not on_break

    if on_break:
        time_left = BREAK_TIME
        block_type.config(text="Break Time")
    else:
        time_left = WORK_TIME
        block_type.config(text="Focus Time")
def skip():
    switch_timer()
def add_task():
    global task_count

    task_name = simpledialog.askstring("New Task", "Task name:")

    if task_name:
        new_checkbox = ttk.Checkbutton(
            frame1,
            text=task_name,
            style="check_box.TCheckbutton"
        )
        new_checkbox.bind("<Double-Button-1>",lambda event, cb=new_checkbox: rename_task(cb))
        y = task_start_y + task_count * task_spacing

        new_checkbox.place(x=27, y=y, width=200, height=30)

        task_count += 1

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


main = tk.Tk()
main.title("Doro")
main.config(bg="#3a3335")
main.geometry("607x664")
main.update_idletasks()

geometryX = 0
geometryY = 0

main.geometry("+%d+%d"%(geometryX, geometryY))


style = ttk.Style(main)
style.theme_use("clam")

menu = tk.Menu(main)
main.config(menu=menu)
menu_0 = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="Settings", menu=menu_0)

frame = tk.Frame(master=main)
frame.config(bg="#d81e5b")
frame.place(x=33, y=31, width=537, height=225)

style.configure("skip.TButton", background="#e43955", foreground="#fdf0d5")
style.map("skip.TButton", background=[("active", "#f7a292")], foreground=[("active", "#c6d8d3")])

skip = ttk.Button(master=frame, text="Skip", style="skip.TButton",command=skip)
skip.place(x=319, y=166, width=80, height=40)

style.configure("pressplay.TButton", background="#e43955", foreground="#fdf0d5")
style.map("pressplay.TButton", background=[("active", "#f7a292")], foreground=[("active", "#c6d8d3")])

pressplay = ttk.Button(master=frame, text="Press/Play", style="pressplay.TButton",command=toggle_timer)
pressplay.place(x=208, y=169, width=80, height=40)

style.configure("block_type.TLabel", background="#d81e5b", foreground="#fdf0d5", anchor="center")
block_type = ttk.Label(master=frame, text="Focus Time", style="block_type.TLabel")  
block_type.configure(anchor="center")
block_type.place(x=205, y=12, width=80, height=40)

style.configure("timer.TLabel", background="#d81e5b", foreground="#fdf0d5", font=("", 48), anchor="center")
timer_label = ttk.Label(master=frame, text="25:00", style="timer.TLabel")
timer_label.configure(anchor="center")
timer_label.place(x=159, y=73, width=200, height=69)

style.configure("reset.TButton", background="#e43955", foreground="#fdf0d5")
style.map("reset.TButton", background=[("active", "#f7a292")], foreground=[("active", "#c6d8d3")])

reset = ttk.Button(master=frame, text="Reset", style="reset.TButton",command=reset)
reset.place(x=94, y=167, width=80, height=40)

frame1 = tk.Frame(master=main)
frame1.config(bg="#f0544f")
frame1.place(x=38, y=295, width=533, height=316)

style.configure("todo_list.TLabel", background="#f0544f", foreground="#fdf0d5", anchor="center")
todo_list = ttk.Label(master=frame1, text="To-do List", style="todo_list.TLabel")
todo_list.configure(anchor="center")
todo_list.place(x=25, y=26, width=80, height=40)

style.configure("check_box.TCheckbutton", background="#f0544f", foreground="#fdf0d5")
style.map("check_box.TCheckbutton", background=[("active", "#892948")], foreground=[("active", "#c6d8d3")])

check_box = ttk.Checkbutton(master=frame1, text="Example task", style="check_box.TCheckbutton")
check_box.bind(  "<Double-Button-1>",lambda event, cb=check_box: rename_task(cb))
check_box.state(['selected'])


check_box.place(x=27, y=94, width=120, height=30)

style.configure("neww_task.TButton", background="#892948", foreground="#fdf0d5")
style.map("neww_task.TButton", background=[("active", "#d81e5b")], foreground=[("active", "#c6d8d3")])

neww_task = ttk.Button(master=frame1, text="+ New", style="neww_task.TButton",command=add_task)
neww_task.place(x=130, y=31, width=80, height=40)


main.mainloop()