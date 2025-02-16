from kivy.app import App
from kivy.uix.button import Button

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.popup import Popup
import requests

class ImageUploaderApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Botão para selecionar a imagem
        self.select_button = Button(text="Selecionar Imagem", size_hint=(1, 0.1))
        self.select_button.bind(on_press=self.show_file_chooser)

        # Label para mostrar o status
        self.status_label = Label(text="Nenhuma imagem selecionada", size_hint=(1, 0.1))

        # Adiciona os widgets ao layout
        self.layout.add_widget(self.select_button)
        self.layout.add_widget(self.status_label)

        return self.layout

    def show_file_chooser(self, instance):
        # Cria um FileChooser para selecionar a imagem
        self.file_chooser = FileChooserListView(path='.', filters=['*.png', '*.jpg', '*.jpeg'])
        self.file_chooser.bind(on_submit=self.select_image)

        # Cria um Popup para exibir o FileChooser
        self.popup = Popup(title="Selecione uma imagem", content=self.file_chooser, size_hint=(0.9, 0.9))
        self.popup.open()

    def select_image(self, instance, selection, *args):
        if selection:
            self.selected_image = selection[0]
            self.status_label.text = f"Imagem selecionada: {self.selected_image}"
            self.popup.dismiss()

            # Envia a imagem para o servidor Flask
            self.upload_image(self.selected_image)

    def upload_image(self, image_path):
        try:
            with open(image_path, 'rb') as file:
                files = {'file': file}
                response = requests.post('http://127.0.0.1:5000/upload', files=files)

            if response.status_code == 200:
                self.status_label.text = "Imagem enviada com sucesso!"
            else:
                self.status_label.text = f"Erro ao enviar imagem: {response.json().get('error')}"
        except Exception as e:
            self.status_label.text = f"Erro: {str(e)}"

if __name__ == '__main__':
    ImageUploaderApp().run()