import tkinter as tk

import src.engine.ElevatorSystem as ElevatorSystem


class Simulation:
    def __init__(self, window, config):
        self.window = window

        self.window.title("Elevators simulation")

        frame = tk.Frame(self.window, width=300, height=300)
        frame.pack(expand=True, fill=tk.BOTH)  # .grid(row=0,column=0)
        self.canvas = tk.Canvas(frame, bg='#FFFFFF')

        horizontal_bar = tk.Scrollbar(frame, orient=tk.HORIZONTAL)
        horizontal_bar.pack(side=tk.BOTTOM, fill=tk.X)
        horizontal_bar.config(command=self.canvas.xview)

        vertical_bar = tk.Scrollbar(frame, orient=tk.VERTICAL)
        vertical_bar.pack(side=tk.RIGHT, fill=tk.Y)
        vertical_bar.config(command=self.canvas.yview)

        self.canvas.config(xscrollcommand=horizontal_bar.set, yscrollcommand=vertical_bar.set)
        self.canvas.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        self.elevator_system = ElevatorSystem.ElevatorSystem(self.canvas, config)

        self.canvas.config(width=min(500, self.elevator_system.number_of_elevators * 150 + 50),
                           height=min(850, self.elevator_system.heights_of_floors[-1] * 25 + 175))

        self.canvas.config(scrollregion=(0,
                                         0,
                                         self.elevator_system.number_of_elevators*150+50,
                                         self.elevator_system.heights_of_floors[-1]*25+175))

        self.canvas.pack(expand=tk.YES, fill=tk.BOTH)

        self.time = [8, 0, 0, 0]
        self.str_time = ["08", "00", "00", "000"]
        self.text_time = None

        self.canvas.create_text(20, 20, text="time:", anchor="w")
        self.text_time = self.canvas.create_text(50, 20, text=":".join(self.str_time), anchor="w")

        self.speeds = [1, 2, 5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000]
        self.current_speed = 1
        self.speed_scale = tk.Scale(self.window, from_=0, to=len(self.speeds)-1,
                                    command=self.update_value, showvalue=False, orient="horizontal", label="speed: 1")
        self.canvas.create_window(200, 30, window=self.speed_scale)

        self.update_time()

    def update_value(self, value):
        self.current_speed = self.speeds[int(value)]
        self.speed_scale.config(label="speed: " + str(self.current_speed))

    def update_time(self):
        for _ in range(self.current_speed):
            str_time = self.str_time[0]+":"+self.str_time[1]+":"+self.str_time[2]+"."+self.str_time[3]

            if str_time == "17:00:00.000":
                self.canvas.itemconfig(self.text_time, text=str_time)
                self.elevator_system.save_simulation_result()
                return

            self.elevator_system.tick(str_time)

            self.time[-1] += 10
            if self.time[-1] == 1000:
                self.time[-2] += self.time[-1] // 1000
                self.time[-1] = 0
                if self.time[-2] == 60:
                    self.time[-3] += self.time[-2] // 60
                    self.time[-2] = 0
                    if self.time[-3] == 60:
                        self.time[-4] += self.time[-3] // 60
                        self.time[-3] = 0
                        self.str_time[-4] = "{:02d}".format(self.time[-4])
                    self.str_time[-3] = "{:02d}".format(self.time[-3])
                self.str_time[-2] = "{:02d}".format(self.time[-2])

            self.str_time[-1] = "{:03d}".format(self.time[-1])

        self.canvas.itemconfig(self.text_time, text=str_time)
        self.window.after(10, self.update_time)  # update every 10ms
