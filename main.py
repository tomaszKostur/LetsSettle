from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button

class Scroller(BoxLayout):

    def add_member(self):
        self.ids.members.add_widget(Button(size_hint=(1, None), height=100))


class LetsSettleApp(App):
    def build(self):
        self.scroller = Scroller()
        return self.scroller


if __name__ == '__main__':
    LetsSettleApp().run()
