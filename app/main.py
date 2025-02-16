from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
import requests
import json

class ZephApp(App):
    def build(self):
        # Define o tamanho da janela
        Window.size = (400, 600)

        # Layout principal
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Botão para selecionar a imagem
        self.select_button = Button(text="Selecionar Imagem", size_hint=(1, 0.1))
        self.select_button.bind(on_press=self.show_file_chooser)

        # Label para mostrar o status
        self.status_label = Label(text="Nenhuma imagem selecionada", size_hint=(1, 0.1))

        # ScrollView para exibir o JSON de resposta
        self.scroll_view = ScrollView(size_hint=(1, 0.8))
        self.grid_layout = GridLayout(cols=1, size_hint_y=None, spacing=10, padding=10)
        self.grid_layout.bind(minimum_height=self.grid_layout.setter('height'))

        # Adiciona os widgets ao layout
        self.scroll_view.add_widget(self.grid_layout)
        self.layout.add_widget(self.select_button)
        self.layout.add_widget(self.status_label)
        self.layout.add_widget(self.scroll_view)

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
                # Exibe o JSON de resposta de forma bonita
                self.display_json(response.json())
                self.status_label.text = "Imagem enviada com sucesso!"
            else:
                self.status_label.text = f"Erro ao enviar imagem: {response.json().get('error')}"
        except Exception as e:
            self.status_label.text = f"Erro: {str(e)}"

    def display_json(self, json_data):
        # Limpa o grid layout antes de adicionar novos widgets
        self.grid_layout.clear_widgets()

        # Adiciona cada campo do JSON ao grid layout
        self.add_label("**Informações Nutricionais**", font_size=18, bold=True)
        self.add_label(f"Proteína: {json_data.get('proteina', 'N/A')}")
        self.add_label(f"Calorias: {json_data.get('calorias', 'N/A')}")
        self.add_label(f"Gordura: {json_data.get('gordura', 'N/A')}")
        self.add_label(f"Carboidratos: {json_data.get('carboidratos', 'N/A')}")
        self.add_label("**Detalhes**", font_size=18, bold=True)
        self.add_label(json_data.get('detalhes', 'N/A'))
        self.add_label("**Sua Dieta**", font_size=18, bold=True)
        self.add_label(json_data.get('sua dieta', 'N/A'))

    def add_label(self, text, font_size=14, bold=False):
        # Cria um label com o texto fornecido
        label = Label(
            text=text,
            size_hint_y=None,
            height=40,
            font_size=font_size,
            bold=bold,
            halign='left',
            valign='middle'
        )
        label.bind(size=label.setter('text_size'))  # Ajusta o tamanho do texto
        self.grid_layout.add_widget(label)

if __name__ == '__main__':
 ZephApp().run()