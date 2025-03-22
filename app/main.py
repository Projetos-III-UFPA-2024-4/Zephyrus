from kivy.app import App  # type: ignore
from kivy.uix.button import Button  # type: ignore
from kivy.uix.screenmanager import Screen, ScreenManager  # type: ignore
from kivy.uix.boxlayout import BoxLayout  # type: ignore
from kivy.uix.label import Label  # type: ignore
from kivy.uix.filechooser import FileChooserListView  # type: ignore
from kivy.uix.popup import Popup  # type: ignore
from kivy.uix.scrollview import ScrollView  # type: ignore
from kivy.uix.gridlayout import GridLayout  # type: ignore
from kivy.core.window import Window  # type: ignore
from kivy.utils import get_color_from_hex  # type: ignore
from kivy.uix.textinput import TextInput  # type: ignore
from kivy.storage.jsonstore import JsonStore  # Adicionado
import requests  # type: ignore
import json
import os  # Adicionado

class SubScreen(Screen):
    def go_to_screen(self, screen_name):
        self.manager.current = screen_name

    def get_color_from_hex(self, hex_color):
        return get_color_from_hex(hex_color)

# Classe base para as telas
class BaseScreen(SubScreen):
    def update_button_colors(self, current_screen):
        buttons = {
            "first_screen": self.ids.btn_tela_1,
            "second_screen": self.ids.btn_tela_2,
            "third_screen": self.ids.btn_tela_3,
            "fourth_screen": self.ids.btn_tela_4,
            "fifth_screen": self.ids.btn_tela_5,
        }

        for screen_name, button in buttons.items():
            if screen_name == current_screen:
                button.background_color = get_color_from_hex("#8159EC")  # Roxo
                button.color = get_color_from_hex("#FFFFFF")  # Texto branco
            else:
                button.background_color = get_color_from_hex("#FFFFFF")  # Branco
                button.color = get_color_from_hex("#000000")  # Texto preto

# Primeira tela
class TelaDafoto(BaseScreen):
    def show_file_chooser(self):
        self.file_chooser = FileChooserListView(path='.', filters=['*.png', '*.jpg', '*.jpeg'])
        self.file_chooser.bind(on_submit=self.select_image)

        self.popup = Popup(title="Selecione uma imagem", content=self.file_chooser, size_hint=(0.9, 0.9))
        self.popup.open()

    def select_image(self, instance, selection, *args):
        if selection:
            self.selected_image = selection[0]
            self.ids.status_label.text = f"Imagem selecionada: {self.selected_image}"
            self.popup.dismiss()
            self.upload_image(self.selected_image)

    def upload_image(self, image_path):
        try:
            user_id = self.get_user_id()  # Obtém o ID do usuário salvo
            if not user_id:
                self.ids.status_label.text = "Erro: ID do usuário não encontrado"
                return

            with open(image_path, 'rb') as file:
                files = {'file': file}
                data = {
                    'user_id': user_id,  # ID do usuário obtido dinamicamente
                    'filename': os.path.basename(image_path)
                }
                response = requests.post('http://3.214.4.114:8080/upload', files=files, data=data)

            if response.status_code == 200:
                self.display_json(response.json())
                self.ids.status_label.text = "Imagem enviada com sucesso!"
            else:
                self.ids.status_label.text = f"Erro ao enviar imagem: {response.json().get('error')}"
        except Exception as e:
            self.ids.status_label.text = f"Erro: {str(e)}"

    def get_user_id(self):
        # Carrega o ID do usuário do armazenamento
        store = JsonStore('usuario.json')
        if store.exists('user'):
            return store.get('user')['id']
        return None

    def display_json(self, json_data):
        self.ids.grid_layout.clear_widgets()
        self.add_label("**Informações Nutricionais**", font_size=32, bold=True)
        self.add_label(f"Proteína: {json_data.get('proteina', 'N/A')}")
        self.add_label(f"Calorias: {json_data.get('calorias', 'N/A')}")
        self.add_label(f"Carboidratos: {json_data.get('carboidratos', 'N/A')}")
        self.add_label("**Detalhes**", font_size=32, bold=True)
        self.add_label(json_data.get('detalhes', 'N/A'))
        self.add_label("**Sua Dieta**", font_size=32, bold=True)
        self.add_label(json_data.get('sua dieta', 'N/A'))

    def add_label(self, text, font_size=14, bold=False):
        label = Label(
            text=text,
            size_hint_y=None,
            height=40,
            font_size=font_size,
            bold=bold,
            halign='left',
            valign='middle'
        )
        label.bind(size=label.setter('text_size'))
        self.ids.grid_layout.add_widget(label)

# Telas adicionais (simples, apenas para exemplo)
class SecondScreen(BaseScreen):
    pass

class ThirdScreen(BaseScreen):
    pass

class FourthScreen(BaseScreen):
    pass

# Tela 5 - Menu do Usuário
class FifthScreen(BaseScreen):
    pass

# Tela de Perfil
class ProfileScreen(SubScreen):
    def __init__(self, **kwargs):
        super(ProfileScreen, self).__init__(**kwargs)
        self.store = JsonStore('usuario.json')  # Armazenamento do ID do usuário

    def go_to_screen(self, screen_name):
        self.manager.current = screen_name

    def confirmar_dados(self):
        dados = {
            "name": self.ids.name_input.text,
            "email": self.ids.email_input.text,
            "senha": self.ids.senha_input.text,
            "calorias": self.ids.calorias_input.text,
            "carboidratos": self.ids.carboidratos_input.text,
            "proteina": self.ids.proteina_input.text,
        }

        try:
            response = requests.post(
                "http://3.214.4.114:8080/salvar_usuario",
                json=dados,
                headers={"Content-Type": "application/json"}
            )
            if response.status_code == 200:
                # Salva o ID retornado pelo servidor
                user_id = response.json().get('user_id')
                if user_id:
                    self.store.put('user', id=user_id)
                    print(f"ID do usuário salvo: {user_id}")
                print("Dados enviados com sucesso!")
            else:
                print(f"Erro ao enviar dados: {response.text}")
        except Exception as e:
            print(f"Erro: {str(e)}")

# App principal
class ZephApp(App):
    def build(self):
        sm = ScreenManager()

        sm.add_widget(TelaDafoto(name="first_screen"))
        sm.add_widget(SecondScreen(name="second_screen"))
        sm.add_widget(ThirdScreen(name="third_screen"))
        sm.add_widget(FourthScreen(name="fourth_screen"))
        sm.add_widget(FifthScreen(name="fifth_screen"))
        sm.add_widget(ProfileScreen(name="profile_screen"))

        sm.current = "first_screen"

        for screen in sm.screens:
            if isinstance(screen, BaseScreen):
                screen.update_button_colors(sm.current)

        sm.bind(current=self.on_screen_change)

        return sm

    def on_screen_change(self, instance, value):
        for screen in instance.screens:
            if isinstance(screen, BaseScreen):
                screen.update_button_colors(value)

if __name__ == '__main__':
    ZephApp().run()
