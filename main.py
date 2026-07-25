import os
import tkinter as tk
import customtkinter as ctk
from pygame import mixer
from PIL import Image
ctk.set_appearance_mode('Dark')
WORK_LENGTH = 25 
BREAK_LENGTH = 5 
WORK_TIME = WORK_LENGTH * 60
BREAK_TIME = BREAK_LENGTH * 60
task_count = 1          
task_start_y = 94      
task_spacing = 35       
time_left = WORK_TIME
running = False
on_break = False
settings = None 
settings_image = ctk.CTkImage(dark_image=Image.open("settings_img.png"),size=(30,30))
mixer.init()
def update_timer():
    global time_left

    if running:
        mins = time_left // 60
        secs = time_left % 60
        timer_label.configure(text=f"{mins:02}:{secs:02}")

        if time_left > 0:
            time_left -= 1
        else:
            mixer.Sound("audio/alarm.mp3").play()
            switch_timer()
        main.after(1000, update_timer)

def toggle_timer():
    global running

    if running:
        running = False
        pressplay.configure(text="Start")
    else:
        running = True
        pressplay.configure(text="Pause")
        update_timer()
def rename_task(event,checkbox):
    event.widget.after(100, lambda: checkbox.deselect())
    dialog = ctk.CTkInputDialog(
        text="Rename Task",
        title="New task name:",
        
    
    )
    new_name = dialog.get_input()
    if new_name:
        checkbox.configure(text=new_name)
def del_task(checkbox,btn):
    global task_count
    checkbox.destroy()
    btn.destroy()
    task_count -= 1
def reset():
    global time_left, running, on_break
    running = False
    on_break = False
    time_left = WORK_TIME
    timer_label.configure(text=f"{WORK_LENGTH}:00")
    block_type.configure(text="Focus Time")
def switch_timer():
    global time_left, on_break
    on_break = not on_break

    if on_break:
        time_left = BREAK_TIME
        block_type.configure(text="Break Time")
        timer_label.configure(text=f"{BREAK_LENGTH}:00")
    else:
        time_left = WORK_TIME
        block_type.configure(text="Focus Time")
        timer_label.configure(text=f"{WORK_LENGTH}:00")
def skip_time():
    switch_timer()
def add_task():
    global task_count

    dialog = ctk.CTkInputDialog(text="New Task", title="Task name:",button_fg_color="#e43955",
    button_hover_color="#f7a292",
    text_color="#fdf0d5")
    new_name = dialog.get_input()
    if new_name:
        new_checkbox = ctk.CTkCheckBox(
            frame1,
            text= new_name,
            text_color="#fdf0d5",
            fg_color="#d81e5b",
            hover_color="#892948",
            checkmark_color="white",
            border_color="#fdf0d5",
            width=200, height=30
        )
        new_checkbox.bind("<Double-Button-1>",lambda event: rename_task(event,new_checkbox))
        y = task_start_y + task_count * task_spacing
        del_btn = ctk.CTkButton(master=frame1, 
         text="Delete", 
   
        fg_color="#e43955",
        hover_color="#f7a292",
        text_color="#fdf0d5",
        corner_radius=10
        , width=80, height=40
            )
        del_btn.configure( command=lambda checkbox=new_checkbox,btn= del_btn: del_task(checkbox,btn))
        del_btn.place(x=150, y=y)
        new_checkbox.place(x=27, y=y)

        task_count += 1
def close_settings():
    global settings
    settings.destroy()
    settings = None 
def open_settings():
    global settings 
    # Add a widget to the new window
    if settings is None or not settings.winfo_exists:
        settings = ctk.CTkToplevel(main)
        settings.geometry('300x200')
        settings.title("Settings")
        focus_setting = ctk.CTkLabel(settings, text="Focus Time")
        focus_setting.pack()
        focus_min = ctk.CTkEntry(settings,placeholder_text=str(WORK_LENGTH))
        focus_min.pack()
        break_setting = ctk.CTkLabel(settings, text="Break Time")
        break_setting.pack()
        break_min = ctk.CTkEntry(settings,placeholder_text=str(BREAK_LENGTH))
        break_min.pack()
        settings.protocol("WM_DELETE_WINDOW", close_settings)
        settings.focus()
        settings.lift()
    else:
        settings.focus()
        settings.lift()

main = ctk.CTk()
main.title("Doro")
main.configure(bg="#3a3335")
main.geometry("607x664")
main.update_idletasks()

geometryX = 0
geometryY = 0

main.geometry("+%d+%d"%(geometryX, geometryY))






frame = ctk.CTkFrame(master=main,
    fg_color="#d81e5b", 
    width=537, 
    height=225,
    corner_radius=15)
frame.place(x=33, y=31)
settings_btn = ctk.CTkButton(frame,image=settings_image,
    fg_color="#e43955",
    hover_color="#f7a292",
    text_color="#fdf0d5",text="",
    corner_radius=10,width=30,height=30, command=open_settings)
settings_btn.place(x=319,y=15)
skip = ctk.CTkButton(master=frame, 
    text="Skip",
    command=skip_time, 
    fg_color="#e43955",
    hover_color="#f7a292",
    text_color="#fdf0d5",
    corner_radius=10
    , width=80, height=40)
skip.place(x=319, y=166)


pressplay = ctk.CTkButton(master=frame,
    text="Press/Play",
    command=toggle_timer,
    fg_color="#e43955",
    hover_color="#f7a292",
    text_color="#fdf0d5",
    corner_radius=10
    , width=80, height=40)
pressplay.place(x=208, y=169)


block_type = ctk.CTkLabel(
    frame,
    text="Focus Time",
    fg_color="#e43955",
    text_color="#fdf0d5",
    corner_radius=10
    , width=80, height=40)  
block_type.configure(anchor="center")
block_type.place(x=205, y=12)


timer_label = ctk.CTkLabel(master=frame,
    text=f"{WORK_LENGTH}:00", 
    text_color="#fdf0d5",
    fg_color="transparent",
    font=("Segoe UI",48,"bold"),
    width=200, height=69)
timer_label.configure(anchor="center")
timer_label.place(x=159, y=73)


reset = ctk.CTkButton(master=frame, 
    text="Reset", 
    command=reset,
    fg_color="#e43955",
    hover_color="#f7a292",
    text_color="#fdf0d5",
    corner_radius=10
    , width=80, height=40
    )
reset.place(x=94, y=167)

frame1 = ctk.CTkFrame(master=main,fg_color="#f0544f",width=533, height=316,corner_radius=15)

frame1.place(x=38, y=295)


todo_list = ctk.CTkLabel(frame1,
    text="To-do List",
    text_color="#fdf0d5",
    fg_color="transparent",
    font=("Segoe UI",20,"bold")
    , width=80, height=40
)
todo_list.configure(anchor="center")
todo_list.place(x=25, y=26)



check_box = ctk.CTkCheckBox(frame1,
    text="Example task",
    text_color="#fdf0d5",
    fg_color="#d81e5b",
    hover_color="#892948",
    checkmark_color="white",
    border_color="#fdf0d5"
    , width=120, height=30
)
check_box.bind(  "<Double-Button-1>",lambda event: rename_task(event,check_box))
check_box.select()


check_box.place(x=27, y=94)
del_btn = ctk.CTkButton(master=frame1, 
    text="Delete", 
   
    fg_color="#e43955",
    hover_color="#f7a292",
    text_color="#fdf0d5",
    corner_radius=10
    , width=80, height=40
    )
del_btn.configure( command=lambda checkbox=check_box,btn= del_btn: del_task(checkbox,btn))
del_btn.place(x=150, y=94)


neww_task = ctk.CTkButton(frame1,
    text="+ New",
    command=add_task,
    fg_color="#892949",
    hover_color="#d82e5b",
    text_color="#fdf1d5",
    width=81,
    height=41,
    corner_radius=11
    )
neww_task.place(x=131, y=31)


main.mainloop()



