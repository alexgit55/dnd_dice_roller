import tkinter as tk
import random

import character

class DiceRollerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("D&D Dice Roller")
        self.config(bg="lightblue")  # Add this line
        self.frame_variable=tk.IntVar(self)
        self.frame_variable.set(2)  # Default to General Dice Roll
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
        separator = tk.Frame(top_frame, height=2, bd=1, relief=tk.SUNKEN, bg="lightblue")
        separator.pack(fill=tk.X, padx=5, pady=5)
        
        #General Frame
        general_frame=tk.Frame(self, bg="lightblue")
        self.frames[2]=general_frame
        dice_type=tk.StringVar(general_frame)
        dice_type.set("d20")  # Default value
        dice_type_label=tk.Label(general_frame, bg="lightblue", text="Select the type of Dice to Roll:")
        dice_type_label.pack()
        dice_type_menu=tk.OptionMenu(general_frame, dice_type, "d4", "d6", "d8", "d10", "d12", "d20")
        dice_type_menu.config(bg="lightblue")
        dice_type_menu.pack()
        number_of_dice_label=tk.Label(general_frame, bg="lightblue", text="How many Dice to Roll?")
        number_of_dice_label.pack()
        number_of_dice=tk.Spinbox(general_frame, bg="lightblue", from_=1, to=20, width=5)
        number_of_dice.pack()
        dice_modifier_label=tk.Label(general_frame, bg="lightblue", text="Modifier to add to the roll?")
        dice_modifier_label.pack()
        dice_modifier=tk.Spinbox(general_frame, bg="lightblue", from_=-20, to=20, width=5,textvariable=tk.IntVar(general_frame, value=0))
        dice_modifier.pack()
        general_frame.pack(fill=tk.X, pady=10)
        
        # Skill Check Frame
        skill_check_frame=tk.Frame(self, bg="lightblue")
        self.frames[3]=skill_check_frame
        skill_check_label=tk.Label(skill_check_frame, bg="lightblue", text="Which Skill check to roll?")
        skill_check_label.pack()      
        skill_check_frame.pack()
        
        #Saving Throw Frame
        saving_throw_frame=tk.Frame(self, bg="lightblue")
        saving_throw_label=tk.Label(saving_throw_frame, bg="lightblue", text="Which Saving Throw to Roll?")
        saving_throw_label.pack()
        self.frames[4]=saving_throw_frame
        saving_throw_frame.pack()
        
        # Bottom Roll Frame
        bottom_frame=tk.Frame(self, bg="lightblue")
        self.frames[1]=bottom_frame
        # Create a separator
        separator = tk.Frame(bottom_frame, height=2, bd=1, relief=tk.SUNKEN, bg="lightblue")
        separator.pack(fill=tk.X, padx=5, pady=5)
        roll_button=tk.Button(bottom_frame, text="Roll Dice", command=self.roll_dice)
        roll_button.pack(pady=20)
        reset_button=tk.Button(bottom_frame, text="Reset", command=lambda: self.frames[2].pack_forget())
        self.result_label=tk.Label(bottom_frame, bg="lightblue", text="")
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

    def roll_dice(self):
        frame = self.frame_variable.get()
        if frame == 2:  # General Dice Roll
            dice_type = self.frames[2].children['!optionmenu'].cget('text')
            number_of_dice = int(self.frames[2].children['!spinbox'].get())
            dice_modifier = int(self.frames[2].children['!spinbox2'].get())
            rolls=[]
            for _ in range(number_of_dice):
                type=int(dice_type[1:])
                roll=random.randint(1,type)
                rolls.append(roll)
            result=sum(rolls)+dice_modifier
            if dice_modifier < 0:
                self.result_label.config(text=f"Rolls: {rolls} - {abs(dice_modifier)}, Total: {result}")
            elif dice_modifier > 0:
                self.result_label.config(text=f"Rolls: {rolls} + {dice_modifier}, Total: {result}")
            else:
                self.result_label.config(text=f"Rolls: {rolls}, Total: {result}")

if __name__ == "__main__":
    app = DiceRollerApp()
    app.mainloop()