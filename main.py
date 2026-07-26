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
task_start_y = 94      
task_spacing = 35       

 
settings_image = ctk.CTkImage(dark_image=Image.open("settings_img.png"),size=(30,30))
mixer.init()
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

class timerLogic:
    def __init__(self,master):
        self.master = master
        
    def update_timer(self):
        if self.master.time_left > 0:
            self.master.time_left -= 1

        if self.master.running:
            self.mins = self.master.time_left // 60
            self.secs = self.master.time_left % 60
            self.master.timer_frame.timer_label.configure(text=f"{self.mins:02}:{self.secs:02}")
        else:
            mixer.Sound("audio/alarm.mp3").play()
            self.switch_timer()
        self.master.main.after(1000, self.update_timer)

    def start_stop(self):

        if self.master.running:
            self.master.running = False
            self.master.timer_frame.pressplay.configure(text="Start")
        else:
            self.master.running = True
            self.master.timer_frame.pressplay.configure(text="Pause")
            self.update_timer()
    def reset(self):
        self.master.running = False

        if self.master.on_break == False:
            self.master.time_left = WORK_TIME
            self.master.timer_frame.timer_label.configure(text=f"{WORK_LENGTH}:00")
            self.master.timer_frame.block_type.configure(text="Focus Time")
        else:
            self.master.time_left = BREAK_TIME
            self.master.timer_frame.timer_label.configure(text=f"{BREAK_LENGTH}:00")
            self.master.timer_frame.block_type.configure(text="Break Time")

    def skip_time(self):
        
        self.master.on_break = not self.master.on_break

        if self.master.on_break:
            self.master.time_left = BREAK_TIME
            self.master.timer_frame.block_type.configure(text="Break Time")
            self.master.timer_frame.timer_label.configure(text=f"{BREAK_LENGTH}:00")
        else:
            self.master.time_left = WORK_TIME
            self.master.timer_frame.block_type.configure(text="Focus Time")
            self.master.timer_frame.timer_label.configure(text=f"{WORK_LENGTH}:00")


class timerFrame:
    def __init__(self,master,logic):
        self.logic = logic
        self.frame = ctk.CTkFrame(master=master,
        fg_color="#d81e5b", 
        width=537, 
        height=225,
        corner_radius=15)
        self.frame.place(x=33, y=31)
        
        self.settings_btn = ctk.CTkButton(self.frame,image=settings_image,
        fg_color="#e43955",
        hover_color="#f7a292",
        text_color="#fdf0d5",text="",
        corner_radius=10,width=30,height=30)
        self.settings_btn.place(x=319,y=15)

        self.skip = ctk.CTkButton(master=self.frame, 
        text="Skip",
        command=self.logic.skip_time, 
        fg_color="#e43955",
        hover_color="#f7a292",
        text_color="#fdf0d5",
        corner_radius=10
        , width=80, height=40)
        self.skip.place(x=319, y=166)


        self.pressplay = ctk.CTkButton(master=self.frame,
        text="Press/Play",
        command=self.logic.start_stop,
        fg_color="#e43955",
        hover_color="#f7a292",
        text_color="#fdf0d5",
        corner_radius=10
        , width=80, height=40)
        self.pressplay.place(x=208, y=169)


        self.block_type = ctk.CTkLabel(
        self.frame,
        text="Focus Time",
        fg_color="#e43955",
        text_color="#fdf0d5",
        corner_radius=10
        , width=80, height=40)  
        self.block_type.configure(anchor="center")
        self.block_type.place(x=205, y=12)


        self.timer_label = ctk.CTkLabel(master=self.frame,
        text=f"{WORK_LENGTH}:00", 
        text_color="#fdf0d5",
        fg_color="transparent",
        font=("Segoe UI",48,"bold"),
        width=200, height=69)
        self.timer_label.configure(anchor="center")
        self.timer_label.place(x=159, y=73)
        

        self.reset = ctk.CTkButton(master=self.frame, 
        text="Reset", 
        command=self.logic.reset,
        fg_color="#e43955",
        hover_color="#f7a292",
        text_color="#fdf0d5",
        corner_radius=10
        , width=80, height=40
        )
        self.reset.place(x=94, y=167)

class task:
    def __init__(self,master,name,y,app):
        self.master = master
        self.app = app
        self.name = name
        self.y = y
        self.task = ctk.CTkCheckBox(
            self.master,
            text= self.name,
            text_color="#fdf0d5",
            fg_color="#d81e5b",
            hover_color="#892948",
            checkmark_color="white",
            border_color="#fdf0d5",
            width=200, height=30
        )
        self.task.bind("<Double-Button-1>",lambda event: self.rename_task(event,self.task))
        
        self.del_btn = ctk.CTkButton(master=self.master, 
        text="Delete", 
        fg_color="#e43955",
        hover_color="#f7a292",
        text_color="#fdf0d5",
        corner_radius=10
        , width=80, height=40
            )
        self.del_btn.configure( command=lambda: self.del_task())
        self.del_btn.place(x=150, y=self.y)
        self.task.place(x=27, y=self.y)
    def rename_task(self,event,checkbox):
        event.widget.after(100, lambda: checkbox.deselect())
        self.dialog = ctk.CTkInputDialog(
        text="Rename Task",
        title="New task name:",
    )
        self.new_name = self.dialog.get_input()
        if self.new_name:
            self.task.configure(text=self.new_name)
    def del_task(self):
        
        self.task.destroy()
        self.del_btn.destroy()
        self.app.task_list.remove(self) 


class taskframe:
    def __init__(self,master):
        self.master = master
        self.frame1 = ctk.CTkFrame(master=self.master.main,fg_color="#f0544f",width=533, height=316,corner_radius=15)

        self.frame1.place(x=38, y=295)


        self.todo_list = ctk.CTkLabel(self.frame1,
        text="To-do List",
        text_color="#fdf0d5",
        fg_color="transparent",
        font=("Segoe UI",20,"bold")
        , width=80, height=40
        )
        self.todo_list.configure(anchor="center")
        self.todo_list.place(x=25, y=26)

        

        self.new_task = ctk.CTkButton(self.frame1,
        text="+ New",
        command=self.add_task,
        fg_color="#892949",
        hover_color="#d82e5b",
        text_color="#fdf1d5",
        width=81,
        height=41,
        corner_radius=11
        )
        self.new_task.place(x=131, y=31)
    def add_task(self):
        self.dialog = ctk.CTkInputDialog(text="New Task", title="Task name:",button_fg_color="#e43955",
        button_hover_color="#f7a292",
        text_color="#fdf0d5")
        self.new_name = self.dialog.get_input()
        if self.new_name:
            y = task_start_y +len(self.master.task_list) * task_spacing
            self.master.task_list.append(task(self.frame1,self.new_name,y,self.master))
            
class settingsWindow:
    def __init__(self):
        pass
class app:
    def __init__(self):
        # Variables
        self.task_list = []                
        self.time_left = WORK_TIME
        self.running = False
        self.on_break = False    
        self.settings = None 

        # Create main app
        self.main = ctk.CTk()
        self.main.title("Doro")
        self.main.configure(bg="#3a3335")
        self.main.geometry("607x664")
        self.main.update_idletasks()
        self.main.geometry("+%d+%d"%(0, 0))

        # Create Timer & Task Frames
        self.create_timer_frame()
        self.create_tasks_frame()
            
    def create_timer_frame(self):
        self.logic = timerLogic(self)
        self.timer_frame = timerFrame(self.main,self.logic)
    def create_tasks_frame(self):
        self.task_frame = taskframe(self)
root = app()

root.main.mainloop()



