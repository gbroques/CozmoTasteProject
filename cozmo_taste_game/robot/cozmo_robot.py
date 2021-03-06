from .robot import Robot
from cozmo.util import degrees
from cozmo.world import EvtNewCameraImage
from random import randint, getrandbits
from cozmo.anim import Triggers


class CozmoRobot(Robot):
    """Wrapper class for a :class:`~cozmo.objects.robot`"""
    def __init__(self, cozmo, on_new_camera_image):
        self.cozmo = cozmo
        self.cozmo.add_event_handler(EvtNewCameraImage, on_new_camera_image)
        self.current_angle = 0

    def set_start_position(self) -> None:
        """Sets the start position.

        :return: None
        """
        self.cozmo.set_head_angle(degrees(10.0)).wait_for_completed()
        self.cozmo.set_lift_height(0.0).wait_for_completed()

    def speak(self, text: str) -> None:
        """Wrapper method for :meth:`~cozmo.robot.say_text`.

        :param text: The text to say
        :return: None
        """
        self.cozmo.say_text(str(text)).wait_for_completed()

    def turn_in_place(self) -> None:
        """Wrapper method for :meth:`~cozmo.robot.turn_in_place`.

        :return: None
        """
        rotation_amount = self.__get_rotation_amount()
        self.current_angle += rotation_amount
        self.cozmo.turn_in_place(degrees(rotation_amount)).wait_for_completed()

    def __get_rotation_amount(self) -> int:
        """Gets amount to rotate.

        :return: The amount to rotate
        """
        min_rotate_angle = -10
        max_rotate_angle = 10

        if self.current_angle <= min_rotate_angle:
            rotation_amount = 5 + randint(0, 7)

        elif self.current_angle >= max_rotate_angle:
            rotation_amount = -5 - randint(0, 7)

        else:
            rotation_amount = 5 if getrandbits(1) == 0 else -5

            if rotation_amount < 0:
                rotation_amount -= randint(0, 7)
            else:
                rotation_amount += randint(0, 7)

        return rotation_amount

    def react_positively(self) -> None:
        """Performs a positive reaction. Chooses a random number
            from 0 to 4 and plays reaction that is tied to that
            number
        :return: None
        """
        pos_reactions = [
            Triggers.MajorWin,
            Triggers.CodeLabHappy,
            Triggers.CodeLabYes,
            Triggers.CodeLabAmazed,
            Triggers.CodeLabCelebrate
        ]
        num = randint(0, 4)
        if num == 0:
            self.cozmo.say_text("That is Perfect!").wait_for_completed()
            self.cozmo.play_anim_trigger(pos_reactions[num], ignore_body_track=True).wait_for_completed()
        elif num == 1:
            self.cozmo.play_anim_trigger(pos_reactions[num], ignore_body_track=True).wait_for_completed()
            self.cozmo.say_text("Thank you!").wait_for_completed()
        elif num == 2:
            self.cozmo.play_anim_trigger(Triggers.CodeLabCurious).wait_for_completed()
            self.cozmo.play_anim_trigger(pos_reactions[num], ignore_body_track=True).wait_for_completed()
        elif num == 3:
            self.cozmo.play_anim_trigger(pos_reactions[num], ignore_body_track=True).wait_for_completed()
        else:
            self.cozmo.say_text("Yes, you got it!").wait_for_completed()
            self.cozmo.play_anim_trigger(pos_reactions[num], ignore_body_track=True).wait_for_completed()
        print('Cozmo reacts positively')

    def react_negatively(self) -> None:
        """Performs a negative reaction. Chooses a random number
            from 0 to 4 and plays reaction that is tied to that
            number
        :return: None
        """

        neg_reactions = [
            Triggers.MajorFail,
            Triggers.CubeMovedUpset,
            Triggers.CodeLabUnhappy,
            Triggers.PounceFail,
            Triggers.CodeLabBored
        ]
        num = randint(0, 4)
        if num == 0:
            self.cozmo.play_anim_trigger(neg_reactions[num], ignore_body_track=True).wait_for_completed()
            self.cozmo.say_text("I don't need that").wait_for_completed()
        elif num == 1:
            self.cozmo.play_anim_trigger(neg_reactions[num], ignore_body_track=True).wait_for_completed()
            self.cozmo.say_text("Try again please.").wait_for_completed()
        elif num == 2:
            self.cozmo.play_anim_trigger(Triggers.CodeLabCurious).wait_for_completed()
            self.cozmo.say_text("No").wait_for_completed()
            self.cozmo.play_anim_trigger(neg_reactions[num], ignore_body_track=True).wait_for_completed()
        elif num == 3:
            self.cozmo.say_text("That's not what I want.").wait_for_completed()
            self.cozmo.play_anim_trigger(neg_reactions[num], ignore_body_track=True).wait_for_completed()
        else:
            self.cozmo.play_anim_trigger(neg_reactions[num], ignore_body_track=True).wait_for_completed()



