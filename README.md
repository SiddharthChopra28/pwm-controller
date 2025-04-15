##  mappable controls

####  edit the maps.json file to add new keymaps

```
{
	"name of map 1": {
	"joystick": "mouse",
	"bj": "space",
	"b1": "A",
	"b2": "W",
	"b3": "D"
	}
}
```
#### The 5 keys remain constant, whereas the list of supported values for the keys are given below:
```
{
    "joystick": ["mouse", "wasd", "arrows"],
    "all buttons": [
        "a", "b", "c", "d", "e", "f", "g", "h", "i", "j",
        "k", "l", "m", "n", "o", "p", "q", "r", "s", "t",
        "u", "v", "w", "x", "y", "z",
        "0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
        "enter", "space", "backspace", "esc",
        "shift", "ctrl", "alt", "cmd", "tab",
        "up", "down", "left", "right",
        "delete", "home", "end", "page_up", "page_down",
        "f1", "f2", "f3", "f4", "f5", "f6",
        "f7", "f8", "f9", "f10", "f11", "f12",
        "leftclick", "rightclick","middleclick"
    ]
}

```


## For general configurations, edit config.json
#### params:
```
{
    "mouse_max_speed": float, // enter max speed of mouse in pixel per second, defaults to 50
    "mouse_FPS": int, //  enter number of times to update mouse position per second, higher is smoother
    "analogKeysFrequency": int // pulse frequency of PWM during analog key control (higher the smoother)
}
```