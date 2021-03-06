import threading
import traceback
import requests
import cozmo
import os
import shutil
from sys import argv, exit

from random import choice

from cozmo_taste_game import Robot, FakeRobot, CozmoRobot
from cozmo_taste_game import ColorfulPlate, get_food
from cozmo_taste_game import ResponseAnalyzer

# Globals
DEBUG_MODE = False
camera_lock = threading.Lock()
food_analyzer = ResponseAnalyzer(.65, 2, DEBUG_MODE)
endpoint_url = None
discovered_object = False
latest_picture = None

if len(argv) != 2:
    print("Error: please supply endpoint url")
    exit(-1)
else:
    if argv[1] == "-g":
        DEBUG_MODE = True
    else:
        endpoint_url = argv[1]


def cozmo_program(robot: Robot):
    global food_analyzer
    global camera_lock

    foods = ['hotdog', 'lemon', 'saltshaker', 'broccoli', 'watermelon']

    create_photo_directory()
    plate = ColorfulPlate()

    robot.speak('I''m hungry')
    robot.set_start_position()

    while not plate.is_full:

        if DEBUG_MODE:
            input('Press enter to have Cozmo find a food')
            random_food = choice(foods)
            food_analyzer.force_input(random_food)

        # Check to see if critical section is open
        if not food_analyzer.has_been_checked and (DEBUG_MODE or camera_lock.acquire(False)):

            if food_analyzer.has_found_food():
                # Cozmo found a food
                food_string = food_analyzer.get_found_food()
                food = get_food(food_string)

                robot.speak(str(food))

                if plate.can_place_food(food):
                    robot.react_positively()
                    plate.add_food(food)
                else:
                    print('cannot place the food')
                    robot.react_negatively()

                print(plate)
                print()

            else:
                robot.turn_in_place()

            if not DEBUG_MODE:
                camera_lock.release()

        else:
            pass  # Picture currently being taken or processing


def on_new_camera_image(evt, **kwargs):
    global food_analyzer
    global camera_lock
    global endpoint_url

    if food_analyzer.has_been_checked and camera_lock.acquire(False):
        pil_image = kwargs['image'].raw_image
        photo_location = f"photos/fromcozmo-{kwargs['image'].image_number}.jpeg"
        print(f"photo_location is {photo_location}")
        pil_image.save(photo_location, "JPEG")

        with open(photo_location, 'rb') as f:
            # TODO: automate model mounting
            response = requests.post(endpoint_url, files={'file': f})
            if response.status_code == 200:
                food_analyzer.analyze_response(response.json())

        camera_lock.release()


def create_photo_directory():
    if os.path.exists('photos'):
        shutil.rmtree('photos')
    if not os.path.exists('photos'):
        os.makedirs('photos')


if not DEBUG_MODE:
    cozmo.run_program(CozmoRobot(cozmo_program, on_new_camera_image), use_viewer=True, force_viewer_on_top=True)
else:
    try:
        cozmo_program(FakeRobot())
    except AttributeError as ae:

        print(traceback.format_exc())
        if str(ae)[1:10] == "FakeRobot":
            print(f"\nThe function '{str(ae)[-5:-1]}' hasn't been added to the dummy class")
            print("or you're trying to reference a variable that doesn't exist")
            print(f"Add the following lines to cozmo_taste_game/fake_robot.py:")
            print(f"def {str(ae)[-5:-1]}(a*):")
            print(f"\tprint('#Give helpful input here#')")
            print(f"\treturn FakeAction()")
