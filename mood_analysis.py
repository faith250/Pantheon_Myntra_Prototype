import os
import random
import csv
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

class ImageSelectionScreen(Screen):
    def __init__(self, image_paths, used_images, **kwargs):
        super().__init__(**kwargs)
        self.image_paths = image_paths
        self.used_images = used_images
        self.layout = GridLayout(cols=2, spacing=10, padding=10)
        self.add_widget(self.layout)
        self.display_random_images()

    def display_random_images(self):
        self.layout.clear_widgets()
        self.current_images = []
        categories = list(self.image_paths.keys())
        for _ in range(4):
            while True:
                category = random.choice(categories)
                image_path = random.choice(self.image_paths[category])
                if image_path not in self.used_images:
                    break
            self.used_images.add(image_path)
            btn = Button(background_normal=image_path, size=(300, 370), size_hint=(None, None))
            btn.image_data = (image_path, category)
            btn.bind(on_press=self.select_image)
            self.layout.add_widget(btn)
            self.current_images.append(btn)

    def select_image(self, instance):
        self.manager.selected_images.append(instance.image_data)
        self.write_to_csv(instance.image_data)
        instance.disabled = True  # Disable the button to indicate selection
        if len(self.manager.selected_images) < 12:
            self.manager.current = self.manager.next()
        else:
            self.manager.current = 'recommendation'

    def write_to_csv(self, image_data):
        with open('selected_images.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(image_data)


class ClothesRecommendationScreen(Screen):
    def __init__(self, cloth_paths, **kwargs):
        super().__init__(**kwargs)
        self.cloth_paths = cloth_paths
        self.layout = GridLayout(cols=2, spacing=10, padding=10)
        self.add_widget(self.layout)

    def on_enter(self):
        self.display_clothes()

    def display_clothes(self):
        self.layout.clear_widgets()
        selected_categories = [category for _, category in self.manager.selected_images]
        suggested_clothes = []
        for category in selected_categories:
            clothes = random.sample(self.cloth_paths[category], 1)
            suggested_clothes.extend(clothes)
        for cloth in suggested_clothes:
            btn = Button(background_normal=cloth, size=(300, 370), size_hint=(None, None))
            btn.cloth_data = cloth
            btn.bind(on_press=self.show_cloth_details)
            self.layout.add_widget(btn)

        # Add heartwarming message
        message_label = Label(text="We hope these outfits make your day brighter!",
                              size_hint_y=None, height=50, font_size='20sp',
                              halign='right', valign='middle', padding=(10, 10),
                              color=(1, 1, 1, 1))  # White color
        self.layout.add_widget(message_label)

        btn = Button(text='Restart', size_hint_y=None, height=50)
        btn.bind(on_press=self.restart)
        self.layout.add_widget(btn)

    def show_cloth_details(self, instance):
        self.manager.current = 'cloth_detail'
        self.manager.get_screen('cloth_detail').display_cloth(instance.cloth_data)

    def restart(self, instance):
        self.manager.selected_images = []
        self.manager.current = 'screen1'


class ClothDetailScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        self.add_widget(self.layout)

    def display_cloth(self, cloth_path):
        self.layout.clear_widgets()

        # Centered BoxLayout for the image
        image_box = BoxLayout(orientation='vertical', size_hint=(None, None), size=(300, 437))
        img = Button(background_normal=cloth_path, size_hint=(None, None), size=(300, 437))
        image_box.add_widget(img)
        self.layout.add_widget(image_box)

        # BoxLayout for the buttons with padding
        button_box = BoxLayout(orientation='horizontal', size_hint=(1, None), height=50, spacing=10,
                               padding=(0, 10, 0, 0))
        btn_tryon = Button(text='Virtual Try-On')
        btn_tryon.bind(on_press=self.virtual_tryon)
        button_box.add_widget(btn_tryon)

        btn_purchase = Button(text='Purchase')
        btn_purchase.bind(on_press=self.purchase)
        button_box.add_widget(btn_purchase)

        self.layout.add_widget(button_box)

    def virtual_tryon(self, instance):
        # Placeholder for virtual try-on functionality
        print("Virtual Try-On feature coming soon!")

    def purchase(self, instance):
        # Placeholder for purchase functionality
        print("Purchase feature coming soon!")


class ImageSelectorApp(App):
    def build(self):
        Window.size = (900, 1100)  # Set window size to fit images
        self.image_paths = {
            'beach': self.load_images('images/beach'),
            'mountain': self.load_images('images/mountain'),
            'galaxy': self.load_images('images/galaxy'),
            'forest': self.load_images('images/forest'),
        }
        self.cloth_paths = {
            'beach': self.load_images('clothes/beach'),
            'mountain': self.load_images('clothes/mountain'),
            'galaxy': self.load_images('clothes/galaxy'),
            'forest': self.load_images('clothes/forest'),
        }

        sm = ScreenManager(transition=SlideTransition())
        sm.selected_images = []
        sm.used_images = set()

        sm.add_widget(ImageSelectionScreen(name='screen1', image_paths=self.image_paths, used_images=sm.used_images))
        sm.add_widget(ImageSelectionScreen(name='screen2', image_paths=self.image_paths, used_images=sm.used_images))
        sm.add_widget(ImageSelectionScreen(name='screen3', image_paths=self.image_paths, used_images=sm.used_images))
        sm.add_widget(ClothesRecommendationScreen(name='recommendation', cloth_paths=self.cloth_paths))
        sm.add_widget(ClothDetailScreen(name='cloth_detail'))

        # Initialize the CSV file with headers
        with open('selected_images.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Image Path', 'Category'])

        return sm

    def load_images(self, directory):
        return [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith(('png', 'jpg', 'jpeg'))]


if __name__ == '__main__':
    ImageSelectorApp().run()
