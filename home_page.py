from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, RoundedRectangle, Rectangle

class ColoredButton(Button):
    def __init__(self, color, **kwargs):
        super(ColoredButton, self).__init__(**kwargs)
        self.background_color = color
        self.bind(pos=self.update_rect, size=self.update_rect)
        with self.canvas.before:
            Color(*color)
            self.rect = RoundedRectangle(size=self.size, pos=self.pos, radius=[20])
        self.update_rect()

    def update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

class MyntraApp(App):
    def build(self):
        layout = FloatLayout()

        button1 = ColoredButton(text='Mood Analysis', size_hint=(None, None), size=(300, 50), pos_hint={'center_x': 0.5, 'center_y': 0.6}, color=(0.953, 0.643, 0.827, 1))  # #F3A4D3
        button2 = ColoredButton(text=' vr Try On', size_hint=(None, None), size=(300, 50), pos_hint={'center_x': 0.5, 'center_y': 0.5}, color=(0.957, 0.498, 0.533, 1))  # #F47F88
        button3 = ColoredButton(text='Design Your Own Dress & \n Show Your Graceful Walk (VR Contests)', size_hint=(None, None), size=(300, 50), pos_hint={'center_x': 0.5, 'center_y': 0.4}, color=(0.992, 0.780, 0.549, 1))  # #FDC78C
        button4 = ColoredButton(text='pre-book before release ', size_hint=(None, None), size=(300, 50), pos_hint={'center_x': 0.5, 'center_y': 0.3}, color=(0.957, 0.639, 0.443, 1))  # #F4A371

        layout.add_widget(button1)
        layout.add_widget(button2)
        layout.add_widget(button3)
        layout.add_widget(button4)

        root = FloatLayout()
        with root.canvas.before:
            self.bg = Rectangle(source='background.png', size=root.size, pos=root.pos)
            root.bind(size=self.update_rect, pos=self.update_rect)
        root.add_widget(layout)
        return root

    def update_rect(self, *args):
        self.bg.size = self.root.size
        self.bg.pos = self.root.pos

if __name__ == '__main__':
    MyntraApp().run()
