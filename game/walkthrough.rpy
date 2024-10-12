init 1000 python:
    """
    Within this script is all the functions necessary to list, 
    extract and compare files.
    The main function here is the walthrough_dict' that returns the walkthrough data
    """
    import os

    use_archive_format = False

    def walkthrough_dict():
        green = "#0F0"
        blue = "#00F"
        yellow = "#FF0"
        red = "#F00"
        pink = "#F0F"

        _dech = "Dealers Choice"
        _goch = "Good Choice"
        _bach = "Bad Choice"
        _recc = "Recommended"
        _poss = "Possible"
        _ffch = "50/50 Choice"
        _bech = "Best Choice"

        return {
            ("game/script.rpy", 3440) : {
                "Say something" : {
                    "wt" : f"{_dech} {_recc}",
                    "hint" : [
                        "sadie_naked = True",
                        "More Dialogue"
                        ],
                    "color" : pink
                    },
                "Keep silent" : {
                    "wt" : f"{_dech}",
                    "hint" : [
                        "sadie_clothed = True"
                        ],
                    "color" : pink
                    },
                },
            ("game/script.rpy", 4230) : {
                "Hey guys, since you haven't made a big commotion yet, I think you might deserve a little reward..." : {
                    "wt" : f"{_dech} {_recc}",
                    "hint" : [
                        "More Dialogue"
                        ],
                    "color" : pink
                    },
                "Hmm, I'm gonna be late for my final if this keeps up..." : {
                    "wt" : f"{_dech}",
                    "hint" : [
                        ],
                    "color" : pink
                    },
                },
            ("game/script.rpy", 5894) : {
                "Go without underwear" : {
                    "wt" : f"{_dech} {_recc}",
                    "hint" : [
                        "without_underwear = True"
                        ],
                    "color" : pink
                    },
                "No, I should wear something" : {
                    "wt" : f"{_dech}",
                    "hint" : [
                        "with_underwear = True"
                        ],
                    "color" : pink
                    },
                },
            ("game/script.rpy", 5988) : {
                "Give panties to the boys?" : {
                    "wt" : f"{_dech} {_recc}",
                    "hint" : [
                        "with_underwear = False",
                        "without_underwear = True",
                        ],
                    "color" : pink
                    },
                "No...That's too much for today." : {
                    "wt" : f"{_dech}",
                    "hint" : [
                        ],
                    "color" : pink
                    },
                },
            ("game/script.rpy", 6074) : {
                "You can kiss me" : {
                    "wt" : f"{_dech} {_recc}",
                    "hint" : [
                        "reina_kiss = True",
                        ],
                    "color" : pink
                    },
                "No... I'm sorry..." : {
                    "wt" : f"{_dech}",
                    "hint" : [
                        "reina_rejected = True",
                        ],
                    "color" : pink
                    },
                },
            ("game/script.rpy", 7203) : {
                "Y-yes!" : {
                    "wt" : f"{_dech} {_recc}",
                    "hint" : [
                        "reina_foreplay = True",
                        ],
                    "color" : pink
                    },
                "It's... been a long day" : {
                    "wt" : f"{_dech}",
                    "hint" : [
                        ],
                    "color" : pink
                    },
                },
            ("game/script.rpy", 8301) : {
                "I should show more skin..." : {
                    "wt" : f"{_dech} {_recc}",
                    "hint" : [
                        "undershirtoff = True",
                        ],
                    "color" : pink
                    },
                "N-no... that's going too far...": {
                    "wt" : f"{_dech}",
                    "hint" : [
                        "undershirton = True"
                        ],
                    "color" : pink
                    },
                },
            ("game/script.rpy", 8367) : {
                "I've gone as far as I'm willing to go today..." : {
                    "wt" : f"{_dech} {_recc}",
                    "hint" : [
                        ],
                    "color" : pink
                    },
                "*gulp* What if I kept serving people like this..?": {
                    "wt" : f"{_dech}",
                    "hint" : [
                        ],
                    "color" : pink
                    },
                },
            ("game/script.rpy", 8734) : {
                "No... I just want to go to my room..." : {
                    "wt" : f"{_dech}",
                    "hint" : [
                        ],
                    "color" : pink
                    },
                "...too hot to resist...": {
                    "wt" : f"{_dech} {_recc}",
                    "hint" : [
                        "swimsuitshow = True"
                        ],
                    "color" : pink
                    },
                },
            ("game/script.rpy", 9427) : {
                "I agree with Hu..." : {
                    "wt" : f"{_dech}",
                    "hint" : [
                        "hubertsuit = True"
                        ],
                    "color" : pink
                    },
                "I Agree with Brandon...": {
                    "wt" : f"{_dech}",
                    "hint" : [
                        "brandonsuit = True"
                        ],
                    "color" : pink
                    },
                "I agree with Henry...": {
                    "wt" : f"{_dech}",
                    "hint" : [
                        "henrysuit = True"
                        ],
                    "color" : pink
                    },
                },
            ("game/script.rpy", 9465) : {
                "My body is drenched in sweat, so..." : {
                    "wt" : f"{_dech}",
                    "hint" : [
                        ],
                    "color" : pink
                    },
                "No, I want to change into something more comfortable...": {
                    "wt" : f"{_dech}",
                    "hint" : [
                        ],
                    "color" : pink
                    },
                },
            ("game/script.rpy", 9536) : {
                "I can't help myself..." : {
                    "wt" : f"{_dech} {_recc}",
                    "hint" : [
                        ],
                    "color" : pink
                    },
                "Let's put a stop to this." : {
                    "wt" : f"{_dech}",
                    "hint" : [
                        ],
                    "color" : pink
                    },
                },
            ("game/script.rpy", 10207) : {
                "I should talk to Reina." : {
                    "wt" : f"{_dech}",
                    "hint" : [
                        "reinatalk = True"
                        ],
                    "color" : pink
                    },
                "Honestly, Sadie may actually understand more than anyone..." : {
                    "wt" : f"{_dech}",
                    "hint" : [
                        "sadietalk = True"
                        ],
                    "color" : pink
                    },
                },
            ("game/script.rpy", 10598) : {
                "Check the park." : {
                    "wt" : f"{_dech}",
                    "hint" : [
                        "park = True"
                        ],
                    "color" : pink
                    },
                "Maybe... the mall?" : {
                    "wt" : f"{_dech}",
                    "hint" : [
                        "mall = True"
                        ],
                    "color" : pink
                    },
                },
            ("game/script.rpy", 11599) : {
                "It... kinda turned me on." : {
                    "wt" : f"{_dech} {_recc}",
                    "hint" : [
                        "ilikeporn = True"
                        ],
                    "color" : pink
                    },
                "I don't know if it was the porn, or the situation..." : {
                    "wt" : f"{_dech}",
                    "hint" : [
                        "ihateporn = True"
                        ],
                    "color" : pink
                    },
                },
            ("game/script.rpy", 11981) : {
                "Some of it was... pretty hot." : {
                    "wt" : f"{_dech} {_recc}",
                    "hint" : [
                        "ilikeporn = True"
                        ],
                    "color" : pink
                    },
                "It was all a bit weird to me..." : {
                    "wt" : f"{_dech}",
                    "hint" : [
                        "ihateporn = True"
                        ],
                    "color" : pink
                    },
                },
            }

    valid_dic_items = [#Changes Every Update
        ('game/script.rpy', 9465), ('game/script.rpy', 9536),
        ]

    script_ignore_lines = [#Changes Every Update
        ]

    event_ignore_lines = [#Changes Every Update
        ]

    student_ignore_lines = [#Changes Every Update
        ]
    
    ignore_list = [
        ]

    end_list = [
        ".flac", ".mp3", ".ogg", "opus", ".wav", #Audio Extensions
        ".webm", ".avi", ".mp4", ".mkv", ".ogv", #Video Extensions
        ".webp", ".png", ".jpg", #Image Extensions
        ".rpyc", ".rpa", #Renpy Extensions
        ".ttf", ".otf", #Font Extensions
        ".txt", #Other Extensions
        ]

    def read_rpy_file(file):
        try:
            with renpy.open_file(file, encoding="utf-8") as readfile:
                return readfile.readlines()
        except:
            with open(os.path.join(config.basedir, file), "r", encoding="utf-8") as readfile:
                return readfile.readlines()

    def extract_rpy(name):
        """
        Extract the rpy file within the basedir to folder extracted_files
        """
        folder = os.path.join(config.basedir, "extracted_files")
        path = os.path.join(folder, f"extracted_{name.replace('/', '_-_')}")

        if not os.path.exists(folder):
            os.mkdir(folder)

        f = read_rpy_file(name)

        with open(path, "w", encoding="utf-8") as d:
            d.writelines(f)

    def check_dic(current_dictionary, scripts, use_precise=True):
        """
        Generate a dictionary from 'scripts' containing
        'short_key', 'name' and 'path'
        This grabs the full .rpy file while busy

        Iterate over 'generated_dictionary' and 'current_dictionary'
        to do comparisons of files and lines

        Uses two functions to find the menu lines to see if they match 'current_dictionary'

        Function 'find_closest_menu_before_name' uses a range checker to match where 
        menu is found and searches backwards using a distance checker (Precise Search)

        Function 'find_menu_before_name' uses a range checker to match where
        menu is found and searches backwards no distance (Fuzzy Search)

        Outputs data to 'walkthrough_check.txt' to make corrections and check

        """

        counter = 0
        generated_dictionary = {}

        def find_closest_menu_before_name(lines, name, r_count, out=False):
            closest_menu_line = None
            min_distance = float('inf')

            for i, line in enumerate(lines):
                line = line.replace("\\","")
                # Check if the name, including double quotes, is in the line
                if name in line:
                    # Check if this `name` line is after `r_count`
                    if i >= r_count:
                        # Search backwards from the current line to find the nearest `menu`
                        for j in range(i, -1, -1):
                            if 'menu' in lines[j]:
                                # Calculate distance from `r_count` to the found `menu`
                                distance = abs(r_count - j)
                                if distance < min_distance:
                                    if out:
                                        print(f"Found {name} in {line.strip()} at {i+1}")
                                    min_distance = distance
                                    closest_menu_line = j + 1  # Convert to 1-indexed
                                break  # Stop searching backwards once we find the closest menu
            return closest_menu_line

        def find_menu_before_name(lines, name, out=False):
            for i, line in enumerate(lines):
                if name in line:
                    # Search backwards from the current line
                    for j in range(i, -1, -1):
                        if 'menu' in lines[j]:
                            if out:
                                print(f"Found {name} in {line.strip()} at {i+1}")
                            # Return the line number (1-indexed)
                            return j + 1
            return None
        
        def output(line):
            p = os.path.join(config.basedir, "walkthrough_check.txt")
            with open(p, 'a') as file:
                print(line)
                file.write("{}\n".format(line))

        for short_key, name, path in scripts:
            generated_dictionary[short_key] = [name, read_rpy_file(path), path]
            extract_rpy(path)

        # Iterate over the generated dictionary and the current walkthrough dictionary
        for key, value in generated_dictionary.items():
            for wt_key, wt_value in current_dictionary.items():
                r_count = wt_key[1]
                # Check if the name in value[0] is part of the current wt_key[0]
                if f"{value[0] if use_archive_format else f'game/{value[0]}'}" in wt_key[0]:
                    for name in wt_value:
                        # Find the closest menu line number
                        ln = find_closest_menu_before_name(value[1], f'"{name}"', r_count) #Precise Search
                        al = find_menu_before_name(value[1], f'"{name}"') #Fuzzy Search
                        # Create the tuple with the filename and the line number
                        if use_archive_format:
                            d = ("{}c".format(value[2]), ln) if use_precise else  ("{}c".format(value[2]), al) #Create the correct value .rpyc and line number
                        else:
                            d = ("game/{}".format(value[2]), ln) if use_precise else  ("game/{}".format(value[2]), al) #Create the correct value .rpyc and line number
                        # Print the result with the correct key and value
                        if wt_key != d and not wt_key in valid_dic_items:
                            counter += 1
                            output("Current: {}\nNew: {}\nLine: {}\nCould Be Mistaken For a Sub Menu\n".format(wt_key, d, name))
        return f"Total Items not matching correctly: {counter}"

    def filter_wt(fil):
        """

        'fil' needs to be the full path eg '"new scripts/Student Interaction.rpy"' or
        'script.rpy'

        It will match the lines from the file with the walkthrough dictionary
        """
       
        out = []

        for script, i in walkthrough_dict().keys():
            if fil in script:
                out.append(i)
       
        return out

    def get_rpy_files(ignore_list=ignore_list, end_list=end_list):
        """
        
        This Function Gets all the files mainly '.rpy'
        files.
        
        Add files to ignore in 'ignore_list'
        
        Add extensions to ignore in 'end_list'

        """
        for file in renpy.list_files():
            if file.startswith(("python-packages", "mod", "tl")):
                continue
            if not file in ignore_list:
                if not file.endswith(tuple(end_list)):
                    print(file)

    def get_menu_lines(filename, ignore_lines):
        """
        This Function will find all the menu lines in the script
        
        Function will output data to 'menu_finder.txt' in the base
        game dir

        Uses external Function 'read_rpy_file' to open the files within
        the archives

        """

        output_data = []
        data = read_rpy_file(filename)
        p = os.path.join(config.basedir, "menu_finder.txt")

        for i, line in enumerate(data, 1):
            if "menu:" in line and not i in ignore_lines:
                output_data.append((filename, i))
            elif "menu " in line and not i in ignore_lines:
                output_data.append((filename, i))
        if output_data:
            with open(p, "a") as file:
                for c, i in enumerate(output_data, 1):
                    file.write(f"{c} {str(i)}\n")
                file.write("\n")

    def update_check_walkthrough():
        """
        Use this to check if the lines match up after
        every update an get new menu items.

        Uses external function 'get_menu_lines'
        whilst checking to find current_lines using 'filter_wt' and ignore lists

        Uses external function 'check_dic'

        """
        get_menu_lines("game/script.rpy", filter_wt("game/script")+script_ignore_lines)
        return check_dic(walkthrough_dict(),[
            ("sc", "script", "script.rpy"),
            ])

    
#check_dic(walkthrough_dict(),[("sc", "script", "script.rpy")])