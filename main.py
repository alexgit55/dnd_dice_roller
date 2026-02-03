import FreeSimpleGUI as sg

from dice import Die, DiceRoller
from messages import Messages

class MainWindow:
    def __init__(self):
        self.roller = DiceRoller()
        self.roll_history = []
        self.layout = [
            [sg.Frame('Dice Roller',
                layout=
                [
                    [
                        sg.Column(
                            layout=[
                                [sg.Text('How many Dice to Roll?')],
                                [sg.Spin(values=[i for i in range(1,20)],
                                        initial_value=1,
                                        key='dice_count',
                                        size=(5, 1),)
                                ]
                            ]),
                        sg.Column(
                            layout=[
                                [sg.Text("Select the type of Dice to Roll:")],
                                [sg.Combo(values=Die.get_dice_types(),
                                          default_value='d20',
                                          auto_size_text=True,
                                          key='dice_type',
                                          readonly=True,
                                          enable_events=True,)]
                            ]),
                        sg.Column(
                            layout=[
                                [sg.Text("Modifier to add to the roll?")],
                                [sg.Spin(values=[i for i in range(-20, 20)],
                                         key='dice_modifier',
                                         initial_value=0,
                                         size=(5, 1),)]
                            ]
                        )
                    ],
                    [sg.HorizontalSeparator()],
                    [
                        sg.Push(),
                        sg.Radio("Normal",
                            key='normal_roll',
                            group_id='advantage',
                            default=True),
                        sg.Radio("Advantage",
                            key='advantage_roll',
                            group_id='advantage',
                            default=False),
                        sg.Radio("Disadvantage",
                                 key='disadvantage_roll',
                                 group_id='advantage',
                                 default=False),
                        sg.Push(),
                    ],
                    [sg.HorizontalSeparator()],
                    [
                        sg.Push(),
                        sg.Button("Roll", key='roll'),
                        sg.Button("Reset", key='reset'),
                        sg.Push(),
                    ],
                    [
                        sg.Push(),
                        sg.Frame('Results',
                                 layout=[
                                     [sg.Text('', key='advantage_text')],
                                     [sg.Text('', key='total_text')],
                                     [sg.Text('', key='message_text')]
                                 ]
                                 ),
                        sg.Push(),
                    ]
                ]),
             sg.Frame('Roll History',
                      layout=[
                          [sg.Listbox(values=self.roll_history, size=(30, 10), key='roll_history')]],
                      )
            ]
        ]

        self.window = sg.Window('Dice Roller Application', self.layout)

    def run(self):
        while True:
            event, values = self.window.read()
            if event == 'roll':
                self.roll_dice()
            if event == 'reset':
                self.reset_to_default()
            if event == sg.WINDOW_CLOSED:
                break

        self.window.close()

    def roll_dice(self):
        self.roller.clear_dice()
        num_dice=int(self.window['dice_count'].get())
        dice_modifier=int(self.window['dice_modifier'].get())
        dice_type = self.window['dice_type'].get()
        if dice_type == 'd20' and num_dice == 1:
            rolls=self.get_advantage_roll()
            dice_total=rolls[1]
            self.update_results(num_dice=num_dice,
                                dice_type=dice_type,
                                dice_rolls=rolls,
                                dice_total=dice_total,
                                dice_modifier=dice_modifier)
        else:
            for _ in range(num_dice):
                die = Die(dice_type)
                self.roller.add_dice(die)
            dice_total = self.roller.total_roll()
            self.update_results(num_dice=num_dice,
                                dice_type=dice_type,
                                dice_rolls=dice_total[0],
                                dice_total=dice_total[1],
                                dice_modifier=dice_modifier)


    def get_advantage_roll(self):
        if self.window['advantage_roll'].get():
            return self.roller.d20_roll(advantage=1)
        elif self.window['disadvantage_roll'].get():
            return self.roller.d20_roll(advantage=2)
        return self.roller.d20_roll()

    def update_results(self, num_dice, dice_type, dice_rolls, dice_total=0, dice_modifier=0):
        total = dice_total + dice_modifier
        sign = "+" if dice_modifier >= 0 else "-"
        result_text=f"{num_dice}{dice_type}{sign}{dice_modifier}: "
        if self.window['advantage_roll'].get():
            self.window['advantage_text'].update(value="Rolling with Advantage")
            result_text += f"{dice_rolls[0]} {dice_total} {sign} {abs(dice_modifier)} = {total}"
        elif self.window['disadvantage_roll'].get():
            self.window['advantage_text'].update(value="Rolling with Disadvantage")
            result_text += f"{dice_rolls[0]} {dice_total} {sign} {abs(dice_modifier)} = {total}"
        else:
            self.window['advantage_text'].update(value="")
            if num_dice == 1:
                result_text += f"{dice_total} {sign} {abs(dice_modifier)} = {total}"
            else:
                result_text += f"{dice_rolls} {dice_total} {sign} {abs(dice_modifier)} = {total}"
        self.window['total_text'].update(value=result_text)

        if num_dice == 1 and self.window['dice_type'].get() == 'd20':
            self.window['message_text'].update(value=f'{Messages.result_message(dice_total)}')
        else:
            self.window['message_text'].update(value="")

        self.update_roll_history(result_text)

    def update_roll_history(self, result_text):

        self.roll_history.append(result_text)
        self.window['roll_history'].update(values=self.roll_history)

    def reset_to_default(self):
        self.window['advantage_roll'].update(value=False)
        self.window['disadvantage_roll'].update(value=False)
        self.window['normal_roll'].update(value=True)
        self.window['advantage_text'].update(value="")
        self.window['total_text'].update(value="")
        self.window['message_text'].update(value="")
        self.window['dice_modifier'].update(value=0)
        self.window['dice_count'].update(value=1)
        self.window['dice_type'].update(value='d20')

if __name__ == '__main__':
    window = MainWindow()
    window.run()