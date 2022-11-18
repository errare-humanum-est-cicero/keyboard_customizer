#!/usr/bin/env python3
import subprocess, platform, sys, json

if platform.system() != "Linux": exit()

def check_color(color):
    if color[0] == "#" and len(str(color)) == 7:
        return color[1:]
    elif len(str(color)) != 6:
        raise ValueError
    return color

def apply_loop():
    while True:
        for zone in zone_list:
            print(f"Nr. {zone[0]} is the {zone[1]} zone")

        user_zone = input("which zone do you wan to modify? > ")

        user_color = input("what hex color value do you want to assign? > ")

        try: 
            user_color = check_color(user_color)
        except ValueError:
            print("not a valid color")
            continue

        do_for = []
        if not len(str(user_zone)) > 1:
            apply_arr([[user_zone, user_color]])
            return
            
        getmemyzone = user_zone.split(" ")

        for idx, val in enumerate(getmemyzone):
            if val == "..":            
                zone_from = int(getmemyzone[idx - 1])
                zone_to = int(getmemyzone[idx + 1])

                while zone_from <= zone_to:
                    do_for.append([zone_from, user_color])
                    
                    zone_from += 1

        apply_arr(do_for)

def write_layouts_to_file():
    with open("/home/errare/programming/python/keyboard_customizer/layouts.json", "w") as file:
        file.write(json.dumps(layouts))

#"openrgb -d 0 -z 0 -c ffac1c -m direct"

def apply_arr(values):
    for set in values:
        yay = subprocess.run(["g213-led", "-r", f"{set[0]}", f"{set[1]}"], capture_output=True, text=True)
        if yay.stdout != "":
            print(yay.stdout)
        
    print("layout applied sucessfully")


def print_hex_colored(r, g, b, background=False):
    return f'\033[{48 if background else 38};2;{int(r, 16)};{int(g, 16)};{int(b, 16)}m'

def print_layout(name, arr):
        print(f"Layout: {name}")
        for set in arr:
            print(f"{set[0]}: ", print_hex_colored(set[1][:2], set[1][2:4], set[1][4:]), set[1], '\033[0m')

        print("")

def print_all_layouts():
    for layout_key in layouts:
            print_layout(layout_key, layouts[layout_key])


zone_list =  [
#    [
        [1, "left"],
        [2, "middle"],
        [3, "right"],
        [4, "arrow and homekeys"],
        [5, "numpad"]
#    ],
    
#    [
#        [1, "mouse-main"],
#        [2, "mouse-logo"]
#    ]
]

args = sys.argv

with open("/home/errare/programming/python/keyboard_customizer/layouts.json", "r") as file:
    layouts = json.loads(file.read())


if len(args) == 1:
    apply_loop()
    exit()

match args[1]:
    case "--list":
        if not len(args) > 2:
            args[2] = str(input("do you want to print available zones, layouts or the defauilt layout?> "))
            
        match args[2]:
            case "zones":
                for zone in zone_list:
                    print(f"Nr. {zone[0]} is the {zone[1]} zone")

            case "layouts":
                print_all_layouts()        
            
            case _:
                print("fuck you then")
                
    case "--add-layout":
        new_sets = []
        layout_name = str(input("Name: "))
        
        if layout_name in layouts:
            print("this existing layout will be modified.")
            print_layout(layout_name, layouts[layout_name])
        
        for zone in zone_list:
            user_color = str(input(f"color for {zone[1]}> "))
            
            try: 
                user_color = check_color(user_color)
            except ValueError:
                print("not a valid color")
                exit()
            
            new_sets.append([zone[0], user_color])
        
        layouts[layout_name] = new_sets
        
        print_layout(layout_name, layouts[layout_name])
        write_layouts_to_file()
        
        apply_now = str(input("do you want to apply it right now? (y/N)> "))
        
        if not "y" in apply_now:
            apply_arr(layouts[layout_name])            

    case "--remove-layout":
        if not len(args) > 2:
            print_all_layouts()
            to_remove = input("which layout do you want to remove?> ")
        
        else:
            to_remove = args[2]
        
        if to_remove in layouts:
            del(layouts[to_remove])
            write_layouts_to_file()
            print("layout removed successfully!")
        
        elif to_remove == "default":
            print("cannot remove the default layout")
        
        else:
            print("layout does not exist!")
        
    case "--apply-layout":
        if not len(args) > 2:
            print_all_layouts()
            to_apply = str(input("what layout do you want to apply?> "))
        
        else: 
            to_apply = args[2]
        
        if to_apply in layouts:
            apply_arr(layouts[to_apply])
    
    case _:
        pass
