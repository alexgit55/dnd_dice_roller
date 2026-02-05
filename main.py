import FreeSimpleGUI as sg

from dice import Die, DiceRoller
from messages import Messages
from roll import RollManager, RollResult

class MainWindow:
    def __init__(self):
        self.roller = DiceRoller()
        self.roll_history = RollManager()
        self.roll_presets = RollManager()
        self.roll_presets.load_from_file('presets.json')
        self.layout = [
            [
                sg.Frame('Roll Presets',
                         layout=[
                             [sg.Listbox(values=self.roll_presets.get_rolls(),
                                         size=(40, 10),
                                         key='roll_preset',
                                         auto_size_text=True,
                                         horizontal_scroll=True,
                                         enable_events=True,
                                         tooltip='Click to load a roll into the dice roller.')],
                             [
                                 sg.Push(),
                                 sg.Button('Add Preset', key='add_preset'),
                                 sg.Push(),
                             ],
                         ],
                ),
                sg.Frame('Dice Roller',
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
                        sg.Frame('Result',
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
                          [sg.Listbox(values=self.roll_history.get_rolls(),
                                      size=(40, 10),
                                      key='roll_history',
                                      auto_size_text=True,
                                      horizontal_scroll=True,
                                      enable_events=True,
                                      tooltip='Click to load a roll into the dice roller.')],
                          [
                              sg.Push(),
                              sg.Button('Clear History', key='clear_history'),
                              sg.Push(),
                          ],
                      ],
                      )
            ],
            [sg.Push(), sg.Button('Exit', key='exit')]
        ]

        self.window = sg.Window('Dice Roller Application', self.layout)

    def run(self):
        while True:
            event, values = self.window.read()
            match event:
                case 'roll':
                    self.roll_dice()
                case 'reset':
                    self.reset_to_default()
                case 'clear_history':
                    self.clear_roll_history()
                case 'roll_history':
                    roll = values['roll_history'][0]
                    self.load_preset(roll)
                case 'roll_preset':
                    roll = values['roll_preset'][0]
                    self.load_preset(roll)
                case _ if event in (sg.WIN_CLOSED, 'exit'):
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
            roll_result = RollResult(num_dice, dice_type, rolls, dice_modifier, dice_total)
            self.update_results(roll_result)
        else:
            for _ in range(num_dice):
                die = Die(dice_type)
                self.roller.add_dice(die)
            dice_total = self.roller.total_roll()
            roll_result = RollResult(num_dice, dice_type, dice_total[0], dice_modifier, dice_total[1])
            self.update_results(roll_result)


    def get_advantage_roll(self):
        if self.window['advantage_roll'].get():
            return self.roller.d20_roll(advantage=1)
        elif self.window['disadvantage_roll'].get():
            return self.roller.d20_roll(advantage=2)
        return self.roller.d20_roll()

    def update_results(self, roll_result: RollResult):
        result_text=f"{roll_result}: "
        if self.window['advantage_roll'].get():
            roll_result.advantage = "advantage_roll"
            self.window['advantage_text'].update(value="Rolling with Advantage")
        elif self.window['disadvantage_roll'].get():
            roll_result.advantage = "disadvantage_roll"
            self.window['advantage_text'].update(value="Rolling with Disadvantage")
        else:
            self.window['advantage_text'].update(value="")

        self.window['total_text'].update(value=result_text)

        if roll_result.num_dice == 1 and self.window['dice_type'].get() == 'd20':
            self.window['message_text'].update(value=f'{Messages.result_message(roll_result.dice_total)}')
        else:
            self.window['message_text'].update(value="")

        self.update_roll_history(roll_result)

    def update_roll_history(self, roll_result):

        self.roll_history.add_roll(roll_result)
        self.window['roll_history'].update(values=self.roll_history.get_rolls())

    def clear_roll_history(self):
        self.roll_history.clear()
        self.window['roll_history'].update(values=self.roll_history.get_rolls())

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

    def load_preset(self, roll):
        self.window['dice_modifier'].update(value=roll.dice_modifier)
        self.window['dice_count'].update(value=roll.num_dice)
        self.window['dice_type'].update(value=roll.dice_type)
        self.window[f'{roll.advantage}'].update(value=True)


if __name__ == '__main__':
    window = MainWindow()
    window.run()