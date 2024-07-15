from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.core.window import Window

class TryOnApp(App):
    def build(self):
        # Set the background image
        self.root = RelativeLayout()
        background = Image(source='background.png', allow_stretch=True, keep_ratio=False)
        self.root.add_widget(background)

        # Main layout
        root_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.root.add_widget(root_layout)

        # Title
        title = Label(text='Pre-Launch: Start a Trend for Another Friend', font_size=24, size_hint=(1, 0.1))
        root_layout.add_widget(title)

        # Main layout for products
        products_layout = BoxLayout(orientation='horizontal', spacing=10)

        # Product 1
        product1_layout = self.create_product_layout('blackglasses-removebg-preview (3).png')
        products_layout.add_widget(product1_layout)

        # Product 2
        product2_layout = self.create_product_layout('nailback.png')
        products_layout.add_widget(product2_layout)

        root_layout.add_widget(products_layout)

        return self.root

    def create_product_layout(self, image_path):
        layout = RelativeLayout(size_hint=(1, 1))

        # Adding an image
        img = Image(source=image_path, size_hint=(None, None), size=(300, 400), pos_hint={'center_x': 0.5, 'center_y': 0.6})
        layout.add_widget(img)

        # Creating a vertical box layout for the buttons
        button_layout = BoxLayout(orientation='vertical', spacing=10, size_hint=(None, None), size=(200, 150), pos_hint={'center_x': 0.5, 'y': 0})

        # Adding VR Try-On button
        vr_tryon_button = Button(text='VR Try-On', size_hint=(None, None), size=(200, 50))
        vr_tryon_button.bind(on_press=self.on_vr_tryon_button_press)

        # Adding Pre-Book button
        prebook_button = Button(text='Pre-Book', size_hint=(None, None), size=(200, 50))
        prebook_button.bind(on_press=self.on_prebook_button_press)

        # Adding buttons to the button layout
        button_layout.add_widget(vr_tryon_button)
        button_layout.add_widget(prebook_button)

        # Adding button layout to the main layout
        layout.add_widget(button_layout)

        return layout

    def on_vr_tryon_button_press(self, instance):
        print('VR Try-On clicked!')

    def on_prebook_button_press(self, instance):
        print('Pre-Book clicked!')

if __name__ == '__main__':
    TryOnApp().run()
