from itertools import cycle

import cv2
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import NumericProperty, ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooser
from kivy.uix.gridlayout import GridLayout
import numpy
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.stacklayout import StackLayout

import griddler

Builder.load_file("merger.kv")


class NavigationScreen(Screen):
    def __init__(self, prev_screen_name=None, next_screen_name=None, **kw):
        super(NavigationScreen, self).__init__(**kw)
        self.next_screen_name = next_screen_name
        self.prev_screen_name = prev_screen_name

    def next_screen(self):
        # if self.next_screen_name:
        self.manager.current = self.next_screen_name

    def prev_screen(self):
        # if self.prev_screen_name:
        self.manager.current = self.prev_screen_name


class Merger(GridLayout):
    thresh_slider = ObjectProperty(None)
    size_slider = ObjectProperty(None)
    blur_slider = ObjectProperty(None)
    image = ObjectProperty(None)
    original_size = NumericProperty(10)

    def __init__(self, image_path="pics/mass_awoo.jpg", **kwargs):
        super(Merger, self).__init__(**kwargs)
        self.image_name = image_path
        self.image_array = cv2.imread(self.image_name, 0)
        self.final_image_array = None
        self.original_size = len(self.image_array)
        self.update()

    def update(self):
        ret, ima = cv2.threshold(self.image_array, self.thresh_slider.value, 255, cv2.THRESH_BINARY)
        ima = griddler.resize_maintaining_ratio(ima, int(self.size_slider.value))
        # ima = griddler.blur_by(ima, self.blur_slider.value)
        self.final_image_array = ima
        cv2.imwrite("pics/bin.png", ima)
        self.image.reload()
        print int(self.thresh_slider.value)
        print int(self.size_slider.value)

    def previous_screen(self):
        self.parent.current = "files"


class MyManager(ScreenManager):
    def __init__(self, **kwargs):
        super(MyManager, self).__init__(**kwargs)
        self.griddler = None
        self.image = None

    def switch_to_options(self, image):
        self.image = image[0]
        self.current = "options"


class GriddlerButton(Button):
    def __init__(self, color_changer, number=None, **kwargs):
        super(GriddlerButton, self).__init__(**kwargs)
        self.color_changer = color_changer

        if number:
            self.text = str(number)
            # self.colors = cycle([(1, 1, 1, 1), (0, 0, 0, 1), (0.5, 0.5, 0.5, 1)])
            # self.background_color = next(self.colors)

    def on_touch_move(self, touch):
        if self.collide_point(*touch.pos):
            self.background_color = self.color_changer.color


class NumStack(BoxLayout):
    def __init__(self, data, color_changer, **kwargs):
        super(NumStack, self).__init__(**kwargs)
        if not data:
            self.add_widget(GriddlerButton(color_changer))
        for i in data:
            self.add_widget(GriddlerButton(color_changer, i))


class ColorChanger(Button):
    def __init__(self, **kwargs):
        super(ColorChanger, self).__init__(**kwargs)
        self.colors = cycle([(1, 1, 1, 1), (0.5, 0.5, 0.5, 1), (0.1, 0.1, 0.5, 1)])
        self.color = next(self.colors)

    def on_press(self):
        self.color = next(self.colors)
        self.background_color = self.color


class GriddlerGame(GridLayout):
    def __init__(self, griddler_data, **kwargs):
        super(GriddlerGame, self).__init__(**kwargs)
        gridx, gridy = griddler_data
        self.rows = len(gridx) + 1
        self.cols = len(gridy) + 1
        self.padding = [2, 2, 2, 2]
        color_changer = ColorChanger()
        self.add_widget(color_changer)
        for i in gridy:
            self.add_widget(NumStack(i, color_changer, orientation="vertical"))
        for j in gridx:
            self.add_widget(NumStack(j, color_changer, orientation="horizontal"))
            for i in xrange(len(gridy)):
                self.add_widget(GriddlerButton(color_changer))


class GameScreen(NavigationScreen):
    def on_pre_enter(self, *args):
        self.add_widget(GriddlerGame(self.manager.griddler))


class OptionScreen(NavigationScreen):
    def on_pre_enter(self, *args):
        print self.parent.image
        self.add_widget(Merger(self.manager.image))

    def next_screen(self):
        self.manager.griddler = griddler.griddler_count(self.children[0].final_image_array)  # TODO (quickfix)
        super(OptionScreen, self).next_screen()


class FileScreen(Screen):
    pass


class MergeApp(App):
    def build(self):
        sm = MyManager()
        file_screen = FileScreen(name="file")
        file_screen.add_widget(FileChooser())
        sm.add_widget(file_screen)
        options_screen = OptionScreen(name="options", next_screen_name="game")
        sm.add_widget(options_screen)
        # game_screen = type("GameScreen", ((type(Screen)),
        #                                   {"name": "game", "on_pre_enter": lambda self: self.add_widget(
        #                                       GriddlerGame(self.parent.griddler))}))()
        game_screen = GameScreen(name="game", prev_screen_name="options")
        # game_screen.add_widget(GriddlerGame(sm.griddler))
        sm.add_widget(game_screen)
        return sm

        # def on_stop(self):
        #     cv2.destroyallwindows()


MergeApp().run()
