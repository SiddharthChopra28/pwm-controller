import  serial, serial.tools.list_ports

import json, sys, time, threading

import pynput

ser = serial.Serial()
ports = serial.tools.list_ports.comports()
            
class Controller:
    def __init__(self, baud_rate):
        self.ard = None
        self.supported_keys = {'a': 'a', 'b': 'b', 'c': 'c', 'd': 'd', 'e': 'e', 'f': 'f', 'g': 'g', 'h': 'h', 'i': 'i', 'j': 'j', 'k': 'k', 'l': 'l', 'm': 'm', 'n': 'n', 'o': 'o', 'p': 'p', 'q': 'q', 'r': 'r', 's': 's', 't': 't', 'u': 'u', 'v': 'v', 'w': 'w', 'x': 'x', 'y': 'y', 'z': 'z', '0': '0', '1': '1', '2': '2', '3': '3', '4': '4', '5': '5', '6': '6', '7': '7', '8': '8', '9': '9', 'enter': pynput.keyboard.Key.enter, 'space': pynput.keyboard.Key.space, 'backspace': pynput.keyboard.Key.backspace, 'esc': pynput.keyboard.Key.esc, 'shift': pynput.keyboard.Key.shift, 'ctrl': pynput.keyboard.Key.ctrl, 'alt': pynput.keyboard.Key.alt, 'cmd': pynput.keyboard.Key.cmd, 'tab': pynput.keyboard.Key.tab, 'up': pynput.keyboard.Key.up, 'down': pynput.keyboard.Key.down, 'left': pynput.keyboard.Key.left, 'right': pynput.keyboard.Key.right, 'delete': pynput.keyboard.Key.delete, 'home': pynput.keyboard.Key.home, 'end': pynput.keyboard.Key.end, 'page_up': pynput.keyboard.Key.page_up, 'page_down': pynput.keyboard.Key.page_down, 'f1': pynput.keyboard.Key.f1, 'f2': pynput.keyboard.Key.f2, 'f3': pynput.keyboard.Key.f3, 'f4': pynput.keyboard.Key.f4, 'f5': pynput.keyboard.Key.f5, 'f6': pynput.keyboard.Key.f6, 'f7': pynput.keyboard.Key.f7, 'f8': pynput.keyboard.Key.f8, 'f9': pynput.keyboard.Key.f9, 'f10': pynput.keyboard.Key.f10, 'f11': pynput.keyboard.Key.f11, 'f12': pynput.keyboard.Key.f12}
        self.accepted_kv_pairs = {"joystick": ["wasd", "mouse"], "bj": self.supported_keys, "b1": self.supported_keys, "b2": self.supported_keys, "b3": self.supported_keys}
        self.readings = {
            "x": 0,
            "y": 0,
            "bj": 0,
            "b1": 0,
            "b2": 0,
            "b3": 0
        }
        self.maxmousespeed = None
        self.mouseFPS = None
        self.pwmfreq = None
        self.deadzone = 100
            
        self.getConfig()
        
        
        self.setport(baud_rate)
        
        
    def getConfig(self):
        try:
            with open('config.json', 'r') as f:
                settings = json.load(f)
                
            self.maxmousespeed = float(settings["mouse_max_speed"])
            self.mouseFPS = int(settings["mouse_FPS"])
            self.pwmfreq = int(settings["analogKeysFrequency"])
            
            if self.maxmousespeed <0:
                raise(ValueError)
            elif self.mouseFPS <= 0:
                raise(ValueError)
            elif self.pwmfreq <= 0:
                raise(ValueError)
            
        except FileNotFoundError:
            print("Please create config.json first")
            sys.exit()
        except (ValueError, TypeError): 
            print("Incorrect values detected in config")
            sys.exit()
            
    
    def setport(self, baud_rate):
        for port in ports:
            
            if 'Arduino' in port.description or (port.vid, port.pid) == (9025, 1):
                
                try:
                    self.ard = serial.Serial(port.device, baudrate=baud_rate)
                    return
                except Exception as e:
                    print(e)
                    print("couldn't connect to arduino")
                    sys.exit()
                
        print("No connected controller found")
        sys.exit()
    def verifY_mapping(self, mapping):
        for i in self.accepted_kv_pairs.keys():
            if i not in mapping.keys():
                print("Incorrect keys present in json mapping. Please refer to github readme for documentation")
                sys.exit()

        for k,v in mapping.items():
            if v not in self.accepted_kv_pairs[k]:
                print("Incorrect values present in json mapping. Please refer to github readme for documentation")
                sys.exit()
                

    def get_map(self):
        with open('maps.json', 'r') as f:
            maps_dict = json.load(f)
            available_maps = maps_dict.keys()
        print("List of available mappings: ")
        for n, m in enumerate(available_maps):
            print(f"{n+1}. {m}")
        while True:
            try:
                x = int(input("Enter the number of keymap to use: "))

                if x <= 0 or x>len(available_maps):
                    raise(Exception)
                else:
                    break
            except:
                print("Please enter a valid map number")
                continue
            
        self.verifY_mapping(maps_dict[list(available_maps)[x-1]])
        self.map = maps_dict[list(available_maps)[x-1]]
        
    def get_serial_values(self):
        while 1:
            json_str = self.ard.readline()
            # print(json_str)
            try:
                datadict = json.loads(json_str)
                x_raw = datadict["x"] # reading of analogRead - 0 to 1023
                y_raw = datadict["y"]
                
                bj = not bool(datadict["bj"])
                b1 = not bool(datadict["b1"])
                b2 = not bool(datadict["b2"])
                b3 = not bool(datadict["b3"])
                
                x = (x_raw-512) / 1023
                y = -(y_raw-512) / 1023
                
                if abs(x_raw-512) < self.deadzone:
                    x = 0
                if abs(y_raw-512) < self.deadzone:
                    y = 0

                
                self.readings = {
                    "x": x,
                    "y": y,
                    "bj": bj,
                    "b1": b1,
                    "b2": b2,
                    "b3": b3
                }
                
            except:
                print("error")
                continue
                
        
            
    def mainloop(self):
        if self.map["joystick"] == "wasd":
            pwm_keys = ['w', 'a', 's', 'd']
        elif self.map["joystick"] == "arrows":
            pwm_keys = ['up', 'left', 'down', 'right']
            
        clickbinds = {"leftclick": pynput.mouse.Button.left, "rightclick": pynput.mouse.Button.right, "middleclick": pynput.mouse.Button.middle}
        
        prev_time = time.time()
        prev_time2 = time.time()
        
        onebyfps = 1/self.mouseFPS
        timeperiod = 1/self.pwmfreq
        
        state_x = 0
        state_y = 0
        
        mouse = pynput.mouse.Controller()
        keyboard = pynput.keyboard.Controller()
        y = 0
        a = time.time()
        
        t = threading.Thread(target= self.get_serial_values, daemon=True)
        t.start()
        
        keystohold = []
        while True:
            # if not self.get_serial_values():
            #     # print('[[]]')
            #     continue

            if self.map["joystick"] == "mouse":
                
                newtime = time.time()
                if newtime - prev_time >= onebyfps:
                    # print('ye')
                    mouse.move(2*self.maxmousespeed * self.readings["x"] * onebyfps, 2*self.maxmousespeed * self.readings["y"] * onebyfps)

                    prev_time = newtime
            
            elif self.map["joystick"] in ["wasd", "arrows"]:
                
                for key in pwm_keys:
                    if key not in keystohold:
                        keyboard.release(key)
                
                for key in keystohold:
                    keyboard.press(key)
                
                x_ratio = self.readings["x"]*2
                y_ratio = self.readings["y"]*2
                
                # print(f"{x_ratio=}")
                # print(f"{y_ratio=}")

                uptime_x = abs(x_ratio) * timeperiod
                downtime_x = (1 - abs(x_ratio)) * timeperiod
                
                uptime_y = abs(y_ratio) * timeperiod
                downtime_y = (1 - abs(y_ratio)) * timeperiod

                # print(f"{uptime_x=}")
                # print(f"{downtime_x=}")
                # print(f"{uptime_y=}")
                # print(f"{downtime_y=}")
                # print(f"{state_x=}")
                # print(f"{state_y=}")
                
                newtime2 = time.time()

                if state_y == 0:
                    if newtime2 - prev_time2 >= downtime_y:
                        if y_ratio < 0:
                            keystohold.append(pwm_keys[2])
                        elif y_ratio > 0:
                            keystohold.append(pwm_keys[0])
                        prev_time2 = newtime2
                        state_y = 1
                elif state_y == 1:
                    if newtime2 - prev_time2 >= uptime_y:
                        try:
                            keystohold.remove(pwm_keys[2])
                        except:
                            pass
                        try:
                            keystohold.remove(pwm_keys[0])
                        except:
                            pass
                        prev_time2 = newtime2
                        state_y = 0
                
                newtime = time.time()

                if state_x == 0:
                    if newtime - prev_time >= downtime_x:
                        if x_ratio < 0:
                            keystohold.append(pwm_keys[1])
                        elif x_ratio > 0:
                            keystohold.append(pwm_keys[3])
                        prev_time = newtime
                        state_x = 1
                elif state_x == 1:
                    if newtime - prev_time >= uptime_x:
                        try:
                            keystohold.remove(pwm_keys[1])
                        except:
                            pass
                        try:
                            keystohold.remove(pwm_keys[3])
                        except:
                            pass
                        prev_time = newtime
                        state_x = 0

            # print(f"{downtime_y=}")
            # print(f"{downtime_x=}")
            # print(f"{newtime=}")
            # print(f"{newtime2=}")
            for b in ["bj", "b1", "b2", "b3"]:
                if self.map[b] in ["leftclick", "rightclick","middleclick"]:
                    if self.readings[b]:
                        mouse.press(clickbinds[self.map[b]])
                    else:
                        mouse.release(clickbinds[self.map[b]])
                        
                else:
                    if self.readings[b]:
                        keyboard.press(self.supported_keys[self.map[b]])
                    else:
                        keyboard.release(self.supported_keys[self.map[b]])
                

            time.sleep(0.01)
                
                
        
        

if __name__ == '__main__':
    controller = Controller(9600)
    controller.get_map()
    controller.mainloop()
