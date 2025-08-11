import tkinter as tk
import random

import character

class DiceRollerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("D&D Dice Roller")
        self.frame_variable=tk.IntVar(self)
        self.frame_variable.set(0)
        self.frames={}
        self.create_widgets()
        self.show_frame() # Display the initial frame
        
    def create_widgets(self):
        #Top Frame
        top_frame=tk.Frame(self, bg="lightblue")
        dice_roll_type=tk.Label(top_frame, bg="lightblue", text="Select which type of roll you want to perform: ")
        dice_roll_type.pack(pady=20)       
        tk.Radiobutton(top_frame, bg="lightblue", text="General Dice Roll", variable=self.frame_variable, value=0,
                   command=self.show_frame).pack()
        tk.Radiobutton(top_frame, bg="lightblue", text="Skill Check", variable=self.frame_variable, value=1,
                   command=self.show_frame).pack()
        tk.Radiobutton(top_frame, bg="lightblue", text="Saving Throw", variable=self.frame_variable, value=2,
                   command=self.show_frame).pack()
        top_frame.pack()
        
        #General Frame
        general_frame=tk.Frame(self, bg="red")
        number_of_dice_label=tk.Label(general_frame,text="How many Dice to Roll?")
        number_of_dice_label.pack()
        self.frames[0]=general_frame
        general_frame.pack()
        
        # Skill Check Frame
        skill_check_frame=tk.Frame(self, bg="blue")
        skill_check_label=tk.Label(skill_check_frame,text="Which Skill check to roll?")
        skill_check_label.pack()
        self.frames[1]=skill_check_frame
        skill_check_frame.pack()
        
        #Saving Throw Frame
        saving_throw_frame=tk.Frame(self, bg="blue")
        saving_throw_label=tk.Label(saving_throw_frame,text="Which Saving Throw to Roll?")
        saving_throw_label.pack()
        self.frames[2]=saving_throw_frame
        saving_throw_frame.pack()
    
    def show_frame(self):
        frame=self.frame_variable.get()
        if frame==1:
            self.frames[0].pack_forget()
            self.frames[2].pack_forget()
            self.frames[1].pack()
        elif frame==2:
            self.frames[0].pack_forget()
            self.frames[1].pack_forget()
            self.frames[2].pack()
        else:
            self.frames[1].pack_forget()
            self.frames[2].pack_forget()
            self.frames[0].pack()
        
      
if __name__ == "__main__":
    app = DiceRollerApp()
    app.mainloop()