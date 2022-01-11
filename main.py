import os

#os.environ['DISPLAY'] = ":0.0"
#os.environ['KIVY_WINDOW'] = 'egl_rpi'

from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from pidev.MixPanel import MixPanel
from pidev.kivy.PassCodeScreen import PassCodeScreen
from pidev.kivy.PauseScreen import PauseScreen
from kivy.animation import Animation, AnimationTransition
from pidev.Joystick import Joystick
joy = Joystick(0, False)
from threading import Thread
from time import sleep
from pidev.kivy import DPEAButton
from pidev.kivy import ImageButton
from pidev.kivy.selfupdatinglabel import SelfUpdatingLabel
from kivy.uix.slider import Slider

from datetime import datetime

time = datetime

MIXPANEL_TOKEN = "x"
MIXPANEL = MixPanel("Project Name", MIXPANEL_TOKEN)

SCREEN_MANAGER = ScreenManager()
MAIN_SCREEN_NAME = 'main'
ADMIN_SCREEN_NAME = 'admin'
SINGLE_BUTTON_SCREEN_NAME = 'SingleButtonScreen'

class ProjectNameGUI(App):
    """
    Class to handle running the GUI Application
    """

    def build(self):
        """
        Build the application
        :return: Kivy Screen Manager instance
        """
        return SCREEN_MANAGER


Window.clearcolor = (1, 1, 1, 1)  # White

class MainScreen(Screen):
    """
    Class to handle the main screen and its associated touch events
    """
    value = 0
    stepp = 0

    shared = ObjectProperty()

    def start_joy_thread(self):  # This should be inside the MainScreen Class
        Thread(target=self.joy_update, daemon=True).start()

    def counter(self):
        self.value = self.value + 1
        self.counter_button.text = str(self.value)
        print("Callback from MainScreen.counter()")

    # the below pocket of code (2 lines) creates the counter
    # self.value = self.value +1
    # self.counter_button.text = str(self.value) #you need the self to refer to the instance of main screen. The counter_button tells us which button, and the .text tells us to change .text

    def other_button_text_conversion(self):
        if self.changed_text.text == "Yeah, right.":
            self.changed_text.text = "Nooooooooooooooo!"
        elif self.changed_text.text == "Nooooooooooooooo!":
            self.changed_text.text = "You're mean."
        elif self.changed_text.text == "You're mean.":
            self.changed_text.text = "Ughhhhh"
        elif self.changed_text.text == "Ughhhhh":
            self.changed_text.text = "Ugh"
        elif self.changed_text.text == "Ugh!":
            self.changed_text.text = "Ugh"
        else:
            self.changed_text.text = "Ugh!"


    def pressed(self):
        """
        Function called on button touch event for button with id: testButton
        :return: None
        """
        print("Callback from MainScreen.pressed()")

    def transition_to_single_button_screen(self):
        SCREEN_MANAGER.current = SINGLE_BUTTON_SCREEN_NAME

    def admin_action(self):
        """
        Hidden admin button touch event. Transitions to passCodeScreen.
        This method is called from pidev/kivy/PassCodeScreen.kv
        :return: None
        """
        SCREEN_MANAGER.current = 'passCode'

    def animate_alvaro(self):
        print("Called animate")
        if self.stepp%3 == 0:
            anim = Animation(x=350) + Animation(size=(200, 200), duration=2.)
            anim.start(self.alvaro)
            print("Called alvaro animation (1)")
        elif self.stepp%3 == 1:
            SCREEN_MANAGER.current = SINGLE_BUTTON_SCREEN_NAME
            print("Called screen change (2)")
        elif self.stepp%3 == 2:
            anim = Animation(x=490, y=30, duration=0.) + Animation(size=(90, 90), duration=0.)
            anim.start(self.alvaro)
            print("Called alvaro back to normal (3)")
        self.stepp += 1

    def joy_update(self):  # This should be inside the MainScreen Class
       while True:
           self.joy_label.center_x += joy.get_axis('x')
           self.joy_label.center_y += joy.get_axis('y')
           print("X:" ,joy.get_axis('x'), ", Y:", joy.get_axis('y'))
           self.melanie.x += joy.get_axis('x')
           self.shared = joy.get_axis('x'), joy.get_axis('y')
           self.melanie.y += joy.get_axis('y')
           sleep(.1)

class SingleButtonScreen(Screen):
    def __init__(self, **kwargs):
        Builder.load_file('SingleButtonScreen.kv')

        #PassCodeScreen.set_admin_events_screen(ADMIN_SCREEN_NAME)  # Specify screen name to transition to after correct password
        #PassCodeScreen.set_transition_back_screen(MAIN_SCREEN_NAME)  # set screen name to transition to if "Back to Game is pressed"

        super(SingleButtonScreen, self).__init__(**kwargs)

    @staticmethod
    def transition_back():
        """
        Transition back to the main screen
        :return:
        """
        SCREEN_MANAGER.current = MAIN_SCREEN_NAME

    def animate_cesar_harlow(self):
        anim = Animation(x=200, duration=0.5) + Animation(size=(400, 400), duration=0.5)
        anim.start(self.cesarharlow)

    def get_axis(self):
        print('X:', joy.get_axis('x'))
        print('Y:', joy.get_axis('y'))

class AdminScreen(Screen):
    """
    Class to handle the AdminScreen and its functionality
    """

    def __init__(self, **kwargs):
        """
        Load the AdminScreen.kv file. Set the necessary names of the screens for the PassCodeScreen to transition to.
        Lastly super Screen's __init__
        :param kwargs: Normal kivy.uix.screenmanager.Screen attributes
        """
        Builder.load_file('AdminScreen.kv')

        PassCodeScreen.set_admin_events_screen(ADMIN_SCREEN_NAME)  # Specify screen name to transition to after correct password
        PassCodeScreen.set_transition_back_screen(MAIN_SCREEN_NAME)  # set screen name to transition to if "Back to Game is pressed"

        super(AdminScreen, self).__init__(**kwargs)

    @staticmethod
    def transition_back():
        """
        Transition back to the main screen
        :return:
        """
        SCREEN_MANAGER.current = MAIN_SCREEN_NAME

    @staticmethod
    def shutdown():
        """
        Shutdown the system. This should free all steppers and do any cleanup necessary
        :return: None
        """
        os.system("sudo shutdown now")

    @staticmethod
    def exit_program():
        """
        Quit the program. This should free all steppers and do any cleanup necessary
        :return: None
        """
        quit()


"""
Widget additions
"""

Builder.load_file('main.kv')
SCREEN_MANAGER.add_widget(MainScreen(name=MAIN_SCREEN_NAME))
SCREEN_MANAGER.add_widget(PassCodeScreen(name='passCode'))
SCREEN_MANAGER.add_widget(PauseScreen(name='pauseScene'))
SCREEN_MANAGER.add_widget(AdminScreen(name=ADMIN_SCREEN_NAME))
SCREEN_MANAGER.add_widget(SingleButtonScreen(name=SINGLE_BUTTON_SCREEN_NAME))

"""
MixPanel
"""


def send_event(event_name):
    """
    Send an event to MixPanel without properties
    :param event_name: Name of the event
    :return: None
    """
    global MIXPANEL

    MIXPANEL.set_event_name(event_name)
    MIXPANEL.send_event()


if __name__ == "__main__":
    # send_event("Project Initialized")
    # Window.fullscreen = 'auto'
    ProjectNameGUI().run()