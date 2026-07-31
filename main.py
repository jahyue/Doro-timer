import tkinter as tk
import customtkinter as ctk
from pygame import mixer
from PIL import Image
from plyer import notification
import json
ctk.set_appearance_mode('Dark')
         
task_start_y = 75      
task_spacing = 35      

 
settings_image = ctk.CTkImage(dark_image=Image.open("media/settings_img.png"),size=(30,30))
mixer.init()
class timerLogic:
    def __init__(self,master):
        self.master = master
        self.alarm = mixer.Sound("media/alarm.mp3")
        self.timer_job = None
    def update_timer(self):
        if not self.master.focusdore_active:    
            if self.master.time_left > 0:
                self.master.time_left -= 1
            else:
                if self.master.play_alarm_active.get():
                    self.alarm.play()
                self.skip_time()
                self.notify("Focus session complete!", "Time for a break.")
        elif not self.master.on_break:
            if self.master.time_left >= 0:
                self.master.time_left += 1
        else:
            if self.master.time_left > 0:
                self.master.time_left -= 1
            else:
                if self.master.play_alarm_active.get():
                    self.alarm.play()
                self.skip_time()
                
                self.notify("Break complete!", "Time to focus!")

                
        if self.master.running:
            self.mins = self.master.time_left // 60
            self.secs = self.master.time_left % 60
            self.master.timer_frame.timer_label.configure(text=f"{self.mins:02}:{self.secs:02}")
            self.timer_job = self.master.main.after(1000, self.update_timer)  
        else:
            self.timer_job = None
    def start_stop(self):

        if self.master.running:
            self.master.running = False
            self.master.timer_frame.pressplay.configure(text="Start")
            if self.timer_job:
                self.master.main.after_cancel(self.timer_job)
                self.timer_job = None
        else:
            self.master.running = True
            self.master.timer_frame.pressplay.configure(text="Pause")
            if self.timer_job is None:
                self.update_timer()
    def reset(self):
        self.master.running = False
        if self.timer_job:
            self.master.main.after_cancel(self.timer_job)
            self.timer_job = None

        if self.master.on_break == False and not self.master.focusdore_active:
            self.master.time_left = self.master.work_length * 60
            self.master.timer_frame.timer_label.configure(text=f"{self.master.work_length}:00")
            self.master.timer_frame.block_type.configure(text="Focus Time")
            self.master.timer_frame.pressplay.configure(text="Start")
        elif self.master.on_break == False :
            self.master.time_left = 0
            self.master.timer_frame.timer_label.configure(text=f"00:00")
            self.master.timer_frame.block_type.configure(text="Focus Time")
            self.master.timer_frame.pressplay.configure(text="Start")
        else:
            self.master.time_left = self.master.break_length * 60
            self.master.timer_frame.timer_label.configure(text=f"{self.master.break_length}:00")
            self.master.timer_frame.block_type.configure(text="Break Time")
            self.master.timer_frame.pressplay.configure(text="Start")

    def skip_time(self):
    
        self.master.on_break = not self.master.on_break
        if self.master.on_break and self.master.focusdore_active:
            self.display = round(self.master.time_left / 60 / 5)
            self.master.time_left = self.display * 60
            self.master.timer_frame.block_type.configure(text="Break Time")
            self.master.timer_frame.timer_label.configure(text=f"{self.display}:00")
        elif self.master.on_break:
            self.master.time_left = self.master.break_length * 60
            self.master.timer_frame.block_type.configure(text="Break Time")
            self.master.timer_frame.timer_label.configure(text=f"{self.master.break_length}:00")
        elif not self.master.focusdore_active:
            self.master.time_left = self.master.work_length * 60
            self.master.timer_frame.block_type.configure(text="Focus Time")
            self.master.timer_frame.timer_label.configure(text=f"{self.master.work_length}:00")
        else:
            self.master.time_left = 0
            self.master.timer_frame.timer_label.configure(text=f"00:00")
            self.master.timer_frame.block_type.configure(text="Focus Time")
        if self.master.on_break:
            if self.master.auto_break_active.get():
                self.master.running = True
                self.master.timer_frame.pressplay.configure(text="Pause")
                if self.timer_job is None:
                    self.update_timer()
        else:
            if self.master.auto_focus_active.get():
                self.master.running = True
                self.master.timer_frame.pressplay.configure(text="Pause")
                if self.timer_job is None:
                    self.update_timer()
    def pick_mode(self,choice):
        if choice == "Focustime":
            self.master.focusdore_active = True
            self.master.running = False
            self.master.time_left = 0
            self.master.timer_frame.block_type.configure(text="Focus Time")
            self.master.on_break = False
            self.reset()
        else:
            self.master.focusdore_active = False
            self.reset()
    def notify(self, title, message):
        if self.master.desk_notif_active.get():
            notification.notify(title=title,message=message,app_name="Doro",timeout=5)
class timerFrame:
    def __init__(self,master,logic):
        self.master = master
        self.logic = logic
        self.frame = ctk.CTkFrame(master=self.master.main,
        fg_color="#d81e5b", 
        width=480, 
        height=190,
        corner_radius=15)
        self.frame.place(x=20, y=25)
        self.mode_picker = ctk.CTkOptionMenu(self.frame,values=["Pomodoro","Focustime"],command=self.logic.pick_mode)
        self.mode_picker.place(x=18,y=12)
        self.settings_btn = ctk.CTkButton(self.frame,image=settings_image,command=self.master.settings.open_settings,
        fg_color="#e43955",
        hover_color="#f7a292",
        text_color="#fdf0d5",text="",
        corner_radius=10,width=30,height=30)
        self.settings_btn.place(x=400,y=12)

        self.skip = ctk.CTkButton(master=self.frame, 
        text="Finish Block",
        command=self.logic.skip_time, 
        fg_color="#e43955",
        hover_color="#f7a292",
        text_color="#fdf0d5",
        corner_radius=10
        , width=75, height=36)
        self.skip.place(x=315, y=145)


        self.pressplay = ctk.CTkButton(master=self.frame,
        text="Start",
        command=self.logic.start_stop,
        fg_color="#e43955",
        hover_color="#f7a292",
        text_color="#fdf0d5",
        corner_radius=10
        , width=75, height=36)
        self.pressplay.place(x=200, y=145)


        self.block_type = ctk.CTkLabel(
        self.frame,
        text="Focus Time",
        fg_color="#e43955",
        text_color="#fdf0d5",
        corner_radius=10
        , width=80, height=40)  
        self.block_type.configure(anchor="center")
        self.block_type.place(x=185, y=12)


        self.timer_label = ctk.CTkLabel(master=self.frame,
        text=f"{self.master.work_length}:00", 
        text_color="#fdf0d5",
        fg_color="transparent",
        font=("Segoe UI",42,"bold"),
        width=180, height=60)
        self.timer_label.configure(anchor="center")
        self.timer_label.place(x=145, y=60)
        

        self.reset = ctk.CTkButton(master=self.frame, 
        text="Reset", 
        command=self.logic.reset,
        fg_color="#e43955",
        hover_color="#f7a292",
        text_color="#fdf0d5",
        corner_radius=10
        , width=75, height=36
        )
        self.reset.place(x=85, y=145)

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
            width=270, height=30
        )
        self.task.bind("<Double-Button-1>",lambda event: self.rename_task(event,self.task))
        
        self.del_btn = ctk.CTkButton(master=self.master, 
        text="Delete", 
        fg_color="#e43955",
        hover_color="#f7a292",
        text_color="#fdf0d5",
        corner_radius=10
        , width=65, height=30
            )
        self.del_btn.configure( command=lambda: self.del_task())
        self.del_btn.place(x=315, y=self.y)
        self.task.place(x=27, y=self.y)
    def rename_task(self,event,checkbox):
        event.widget.after(100, lambda: checkbox.deselect())
        self.dialog = ctk.CTkInputDialog(
        text="Rename Task",
        title="New task name:",
    )
        self.new_name = self.dialog.get_input()
        if self.new_name:
            self.name = self.new_name
            self.task.configure(text=self.name) 
            self.app.save()
    def del_task(self):
        
        self.task.destroy()
        self.del_btn.destroy()
        if self in self.app.task_list:
            self.app.task_list.remove(self)
        self.app.refresh_task_list()    
        self.app.save()

class taskframe:
    def __init__(self,master):
        self.master = master
        self.frame1 = ctk.CTkFrame(master=self.master.main,fg_color="#f0544f",width=480, height=300,corner_radius=15)

        self.frame1.place(x=20, y=225)


        self.todo_list = ctk.CTkLabel(self.frame1,

        text="To-do List",
        text_color="#fdf0d5",
        fg_color="transparent",
        font=("Segoe UI",22,"bold")
        , width=80, height=40
        )
        self.todo_list.configure(anchor="center")
        self.todo_list.place(x=25, y=20)

        

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
        self.new_task.place(x=145, y=20)
    def add_task(self):
        self.dialog = ctk.CTkInputDialog(text="New Task", title="Task name:",button_fg_color="#e43955",
        button_hover_color="#f7a292",
        text_color="#fdf0d5")
        self.new_name = self.dialog.get_input()
        if self.new_name:
            y = task_start_y +len(self.master.task_list) * task_spacing
            self.master.task_list.append(task(self.frame1,self.new_name,y,self.master))
            self.app.save()
            
class settingsWindow:
    def __init__(self,master):
        self.master = master
        self.settings = None
        
        self.temp_auto_focus = ctk.BooleanVar(value=self.master.auto_focus_active.get())
        self.temp_auto_break = ctk.BooleanVar(value=self.master.auto_break_active.get())
        self.temp_desk_notif = ctk.BooleanVar(value=self.master.desk_notif_active.get())
        self.temp_play_alarm = ctk.BooleanVar(value=self.master.play_alarm_active.get())
    def close_settings(self):
        # Destroys the object
        self.settings.destroy()
        self.settings = None
    def open_settings(self):
        self.temp_auto_focus.set(self.master.auto_focus_active.get())
        self.temp_auto_break.set(self.master.auto_break_active.get())
        self.temp_desk_notif.set(self.master.desk_notif_active.get())
        self.temp_play_alarm.set(self.master.play_alarm_active.get())
        if self.settings is None or not self.settings.winfo_exists():
            self.settings = ctk.CTkToplevel(self.master.main)
            self.settings.iconphoto(True, self.master.icon)
            self.settings.geometry('320x330')
            self.settings.title("Settings")
            self.settings.grid_columnconfigure(0, weight=1)
            self.settings.grid_columnconfigure(1, weight=1)
            self.focus_setting = ctk.CTkLabel(self.settings, text="Focus Time")
            self.focus_setting.grid(row=0,column=0, padx=20, pady=10)
            self.focus_min = ctk.CTkEntry(self.settings)
            self.focus_min.insert(0, str(self.master.work_length))
            self.focus_min.grid(row=0,column=1, padx=20, pady=10)
            self.break_setting = ctk.CTkLabel(self.settings, text="Break Time")
            self.break_setting.grid(row=1,column=0, padx=20, pady=10)
            self.break_min = ctk.CTkEntry(self.settings)
            self.break_min.insert(0, str(self.master.break_length))
            self.break_min.grid(row=1,column=1, padx=20, pady=10)
            self.save_button = ctk.CTkButton(self.settings,text="Save",command=self.save_settings)
            self.save_button.grid(row=6,column=0,columnspan=2,pady=20,padx=20)
            self.auto_focus = ctk.CTkCheckBox(self.settings,text="Auto-Start Focus",variable=self.temp_auto_focus)
            self.auto_focus.grid(row=2,column=0,columnspan=2,padx=20,pady=8,sticky="w")
            self.auto_break = ctk.CTkCheckBox(self.settings,text="Auto-Start Break",variable=self.temp_auto_break)
            self.auto_break.grid(row=3,column=0,columnspan=2,padx=20,pady=8,sticky="w")
            self.desk_notif = ctk.CTkCheckBox(self.settings,text="Desktop Notifications",variable=self.temp_desk_notif)
            self.desk_notif.grid(row=4,column=0,columnspan=2,padx=20,pady=8,sticky="w")
            self.play_alarm = ctk.CTkCheckBox(self.settings,text="Play Alarm Sound",variable=self.temp_play_alarm)
            self.play_alarm.grid(row=5,column=0,columnspan=2,padx=20,pady=8,sticky="w")
            self.settings.protocol("WM_DELETE_WINDOW", self.close_settings)
            self.settings.focus()
            self.settings.lift()
        else:
            # Focusses the window if you press it again
            self.settings.focus()
            self.settings.lift()
    def save_settings(self):
        # Saves from input from the text boxes
        try:
            focus = max(1, int(self.focus_min.get()))
            brk = max(1, int(self.break_min.get()))

            self.master.work_length = focus
            self.master.break_length = brk
            self.master.logic.reset()
        except ValueError:
            pass
        self.master.auto_focus_active.set(self.temp_auto_focus.get())
        self.master.auto_break_active.set(self.temp_auto_break.get())
        self.master.desk_notif_active.set(self.temp_desk_notif.get())
        self.master.play_alarm_active.set(self.temp_play_alarm.get())
        self.master.save()
        self.close_settings()
class app:
    def __init__(self):
        # Variables
        self.task_list = []                
        self.running = False
        self.on_break = False
        self.work_length = 25 
        self.break_length = 5 
        self.time_left = self.work_length * 60
        self.focusdore_active = False
        self.main.iconbitmap("media/icon.ico")
        # Create main app
        self.main = ctk.CTk()
        self.main.title("Doro")
        self.main.configure(bg="#3a3335")
        self.main.geometry("520x540")
        self.main.update_idletasks()
        self.main.geometry("+%d+%d"%(0, 0))
        # Create Settings Variables
        
        self.auto_focus_active = ctk.BooleanVar(value=True)
        self.auto_break_active = ctk.BooleanVar(value=True)
        self.desk_notif_active = ctk.BooleanVar(value=True)
        self.play_alarm_active = ctk.BooleanVar(value=True)
        self.settings = settingsWindow(self)
        # Create Timer & Task Frames
        self.create_timer_frame()
        self.create_tasks_frame()
        self.load()
        self.main.protocol("WM_DELETE_WINDOW", self.on_close)
            
    def create_timer_frame(self):
        self.logic = timerLogic(self)
        self.timer_frame = timerFrame(self,self.logic)
    def create_tasks_frame(self):
        self.task_frame = taskframe(self)
    def refresh_task_list(self):
        for i,task in enumerate(self.task_list):
            y = task_start_y + i * task_spacing
            task.task.place(x=27,y=y)
            task.del_btn.place(x=315,y=y)
    def save(self): 
        data = {
        "work_length": self.work_length,
        "break_length": self.break_length,
        "focusdore_active": self.focusdore_active,

        "settings": {
            "auto_focus": self.auto_focus_active.get(),
            "auto_break": self.auto_break_active.get(),
            "desktop_notifications": self.desk_notif_active.get(),
            "play_alarm": self.play_alarm_active.get()
        },

        "tasks": [
            {
                "name": task.name,
                "completed": bool(task.task.get())
            }
            for task in self.task_list
        ]
    }

        with open("save.json", "w") as file:
            json.dump(data, file, indent=4)    
    def load(self):
        try:
            with open("save.json", "r") as file:
                data = json.load(file)

            self.work_length = data.get("work_length", 25)
            self.break_length = data.get("break_length", 5)
            self.focusdore_active = data.get("focusdore_active", False)

            self.time_left = (
            0 if self.focusdore_active
            else self.work_length * 60
            )

            settings = data.get("settings", {})

            self.auto_focus_active.set(settings.get("auto_focus", True))
            self.auto_break_active.set(settings.get("auto_break", True))
            self.desk_notif_active.set(settings.get("desktop_notifications", True))
            self.play_alarm_active.set(settings.get("play_alarm", True))

            self.logic.reset()
            if self.focusdore_active:
                self.timer_frame.mode_picker.set("Focustime")
            else:
                self.timer_frame.mode_picker.set("Pomodoro")

        
            self.task_list.clear()

            for task_data in data.get("tasks", []):
                y = task_start_y + len(self.task_list) * task_spacing

                new_task = task(
                self.task_frame.frame1,
                task_data["name"],
                y,
                self
                )

                if task_data.get("completed", False):
                    new_task.task.select()

                self.task_list.append(new_task)

        except FileNotFoundError:
            pass

        except json.JSONDecodeError:
            print("Save file is corrupted.")
    def on_close(self):
        self.save()
        self.main.destroy()
root = app()

root.main.mainloop()



