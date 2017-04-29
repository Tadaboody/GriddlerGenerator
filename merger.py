import cv2
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import NumericProperty, ObjectProperty
from kivy.uix.gridlayout import GridLayout
import numpy
from kivy.uix.screenmanager import ScreenManager, Screen

import griddler

Builder.load_file("merger.kv")


class Merger(GridLayout):
    thresh_slider = ObjectProperty(None)
    size_slider = ObjectProperty(None)
    image = ObjectProperty(None)
    original_size = NumericProperty(10)

    def __init__(self,image_path="pics/awoo.jpg", **kwargs):
        super(Merger, self).__init__(**kwargs)
        self.image_name = image_path
        self.image_array = cv2.imread(self.image_name, 0)
        im = cv2.imread(self.image_name)
        self.original_size = len(self.image_array)
        # cv2.imshow("2", im)
        self.update()

    def update(self):
        ret, ima = cv2.threshold(self.image_array, self.thresh_slider.value, 255, cv2.THRESH_BINARY)
        ima = griddler.resize_maintaining_ratio(ima, int(self.size_slider.value))
        filter0 = [1] * 2
        ker = [filter0 for i in range(len(filter0))]
        kernel = numpy.array(ker)
        ima = cv2.filter2D(ima, -1, kernel)
        cv2.imwrite("pics/bin.png", ima)
        self.image.reload()
        print int(self.thresh_slider.value)
        print int(self.size_slider.value)

    def next(self):
        self.parent.parent.griddler = griddler.griddler_count(self.image)


class MyManager(ScreenManager):
    def __init__(self, **kwargs):
        super(MyManager, self).__init__(**kwargs)
        self.griddler = None


class GriddlerGame(GridLayout):
    def __init__(self, griddler, **kwargs):
        super(GriddlerGame, self).__init__(**kwargs)
        gridx, gridy = griddler
        self.rows = len(gridx) + 1

class GameScreen(Screen):
    def on_pre_enter(self, *args):
        self.add_widget(GriddlerGame(self.parent.griddler))
class MergeApp(App):
    def build(self):
        sm = MyManager()
        options_screen = Screen(name="options")
        options_screen.add_widget(Merger())
        sm.add_widget(options_screen)
        # game_screen = type("GameScreen", ((type(Screen)),
        #                                   {"name": "game", "on_pre_enter": lambda self: self.add_widget(
        #                                       GriddlerGame(self.parent.griddler))}))()
        game_screen = GameScreen(name="game")
        # game_screen.add_widget(GriddlerGame(sm.griddler))
        sm.add_widget(game_screen)
        return sm

        # def on_stop(self):
        #     cv2.destroyallwindows()


MergeApp().run()
