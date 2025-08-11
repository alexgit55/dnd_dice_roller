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
        self.frames[0]=top_frame
        top_frame.pack(fill=tk.X)
        dice_roll_type=tk.Label(top_frame, bg="lightblue", text="Select which type of roll you want to perform: ")
        dice_roll_type.pack(pady=20)       
        tk.Radiobutton(top_frame, bg="lightblue", text="General Dice Roll", variable=self.frame_variable, value=2,
                   command=self.show_frame).pack()
        tk.Radiobutton(top_frame, bg="lightblue", text="Skill Check", variable=self.frame_variable, value=3,
                   command=self.show_frame).pack()
        tk.Radiobutton(top_frame, bg="lightblue", text="Saving Throw", variable=self.frame_variable, value=4,
                   command=self.show_frame).pack()
        top_frame.pack()
        
        # Create a separator
        separator = tk.Frame(top_frame, height=2, bd=1, relief=tk.SUNKEN)
        separator.pack(fill=tk.X, padx=5, pady=5)
        
        #General Frame
        general_frame=tk.Frame(self, bg="red")
        self.frames[2]=general_frame
        number_of_dice_label=tk.Label(general_frame,text="How many Dice to Roll?")
        number_of_dice_label.pack()
        number_of_dice=tk.Spinbox(general_frame, from_=1, to=20, width=5)
        number_of_dice.pack()
        dice_modifier_label=tk.Label(general_frame,text="Modifier to add to the roll?")
        dice_modifier_label.pack()
        dice_modifier=tk.Spinbox(general_frame, from_=-20, to=20, width=5,textvariable=tk.IntVar(general_frame, value=0))
        dice_modifier.pack()
        general_frame.pack()
        
        # Skill Check Frame
        skill_check_frame=tk.Frame(self, bg="blue")
        self.frames[3]=skill_check_frame
        skill_check_label=tk.Label(skill_check_frame,text="Which Skill check to roll?")
        skill_check_label.pack()      
        skill_check_frame.pack()
        
        #Saving Throw Frame
        saving_throw_frame=tk.Frame(self, bg="blue")
        saving_throw_label=tk.Label(saving_throw_frame,text="Which Saving Throw to Roll?")
        saving_throw_label.pack()
        self.frames[4]=saving_throw_frame
        saving_throw_frame.pack()
        
        # Bottom Roll Frame
        bottom_frame=tk.Frame(self, bg="lightgreen")
        self.frames[1]=bottom_frame
        # Create a separator
        separator = tk.Frame(bottom_frame, height=2, bd=1, relief=tk.SUNKEN)
        separator.pack(fill=tk.X, padx=5, pady=5)
        roll_button=tk.Button(bottom_frame, text="Roll Dice")
        roll_button.pack(pady=20)
        self.result_label=tk.Label(bottom_frame, text="")
        self.result_label.pack()
        bottom_frame.pack(fill=tk.X, pady=10)

    
    def show_frame(self):
        frame=self.frame_variable.get()
        if frame==3:
            self.frames[2].pack_forget()
            self.frames[4].pack_forget()
            self.frames[3].pack(before=self.frames[1])
        elif frame==4:
            self.frames[2].pack_forget()
            self.frames[3].pack_forget()
            self.frames[4].pack(before=self.frames[1])
        else:
            self.frames[3].pack_forget()
            self.frames[4].pack_forget()
            self.frames[2].pack(before=self.frames[1])


if __name__ == "__main__":
    app = DiceRollerApp()
    app.mainloop()