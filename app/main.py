from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivy.uix.textinput import TextInput
import requests
import json

# Classe base para as telas
class BaseScreen(Screen):
    def __init__(self, **kwargs):
        super(BaseScreen, self).__init__(**kwargs)

        # Layout principal da tela
        main_layout = BoxLayout(orientation='vertical')


        # Conteúdo da tela (será sobrescrito pelas classes filhas)
        self.content_layout = BoxLayout(orientation='vertical', size_hint=(1, 0.8))
        main_layout.add_widget(self.content_layout)

        # Barra de navegação inferior com 5 botões
        self.bottom_bar = BoxLayout(
            size_hint=(1, 0.1),  # Ocupa 10% da altura da tela
            padding=10,
            spacing=10
        )

        # Botões de navegação
        self.btn_tela_1 = Button(
            text="Foto",
            size_hint=(0.2, 1),  # Ocupa 20% da largura da barra
            background_color=get_color_from_hex("#FFFFFF"),  # Branco
            color=get_color_from_hex("#000000")  # Texto preto
        )
        self.btn_tela_1.bind(on_press=lambda x: self.go_to_screen("first_screen"))

        self.btn_tela_2 = Button(
            text="Tela 2",
            size_hint=(0.2, 1),
            background_color=get_color_from_hex("#FFFFFF"),  # Branco
            color=get_color_from_hex("#000000")
        )
        self.btn_tela_2.bind(on_press=lambda x: self.go_to_screen("second_screen"))

        self.btn_tela_3 = Button(
            text="Tela 3",
            size_hint=(0.2, 1),
            background_color=get_color_from_hex("#FFFFFF"),  # Branco
            color=get_color_from_hex("#000000")
        )
        self.btn_tela_3.bind(on_press=lambda x: self.go_to_screen("third_screen"))

        self.btn_tela_4 = Button(
            text="Tela 4",
            size_hint=(0.2, 1),
            background_color=get_color_from_hex("#FFFFFF"),  # Branco
            color=get_color_from_hex("#000000")
        )
        self.btn_tela_4.bind(on_press=lambda x: self.go_to_screen("fourth_screen"))

        self.btn_tela_5 = Button(
            text="Perfil",
            size_hint=(0.2, 1),
            background_color=get_color_from_hex("#FFFFFF"),  # Branco
            color=get_color_from_hex("#000000")
        )
        self.btn_tela_5.bind(on_press=lambda x: self.go_to_screen("fifth_screen"))

        # Adiciona os botões à barra de navegação
        self.bottom_bar.add_widget(self.btn_tela_2)
        self.bottom_bar.add_widget(self.btn_tela_3)
        self.bottom_bar.add_widget(self.btn_tela_1)
        self.bottom_bar.add_widget(self.btn_tela_4)
        self.bottom_bar.add_widget(self.btn_tela_5)

        # Adiciona a barra de navegação ao layout principal
        main_layout.add_widget(self.bottom_bar)

        # Adiciona o layout principal à tela
        self.add_widget(main_layout)

    def go_to_screen(self, screen_name):
        # Muda para a tela especificada
        self.manager.current = screen_name

    def update_button_colors(self, current_screen):
        # Atualiza as cores dos botões com base na tela atual
        buttons = {
            "first_screen": self.btn_tela_1,
            "second_screen": self.btn_tela_2,
            "third_screen": self.btn_tela_3,
            "fourth_screen": self.btn_tela_4,
            "fifth_screen": self.btn_tela_5,
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
    def __init__(self, **kwargs):
        super(TelaDafoto, self).__init__(**kwargs)

        # Botão para selecionar a imagem (parte superior)
        self.select_button = Button(
            text="Selecionar Imagem", 
            size_hint=(1, 0.1),
            background_color=get_color_from_hex("#8159EC"),  # Roxo
            color=get_color_from_hex("#FFFFFF")  # Texto branco
        )
        self.select_button.bind(on_press=self.show_file_chooser)

        # Conteúdo da tela (ScrollView e GridLayout para exibir o JSON)
        self.scroll_view = ScrollView(size_hint=(1, 0.7))
        self.grid_layout = GridLayout(cols=1, size_hint_y=None, spacing=10, padding=10)
        self.grid_layout.bind(minimum_height=self.grid_layout.setter('height'))
        self.scroll_view.add_widget(self.grid_layout)

        # Label para mostrar o status
        self.status_label = Label(text="Nenhuma imagem selecionada", size_hint=(1, 0.1))

        # Adiciona os widgets ao layout de conteúdo
        self.content_layout.add_widget(self.select_button)
        self.content_layout.add_widget(self.scroll_view)
        self.content_layout.add_widget(self.status_label)

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

# Telas adicionais (simples, apenas para exemplo)
class SecondScreen(BaseScreen):
    def __init__(self, **kwargs):
        super(SecondScreen, self).__init__(**kwargs)
        self.content_layout.add_widget(Label(text="Esta é a Tela 2", font_size=24))

class ThirdScreen(BaseScreen):
    def __init__(self, **kwargs):
        super(ThirdScreen, self).__init__(**kwargs)
        self.content_layout.add_widget(Label(text="Esta é a Tela 3", font_size=24))

class FourthScreen(BaseScreen):
    def __init__(self, **kwargs):
        super(FourthScreen, self).__init__(**kwargs)
        self.content_layout.add_widget(Label(text="Esta é a Tela 4", font_size=24))

# Tela 5 - Menu do Usuário
class FifthScreen(BaseScreen):
    def __init__(self, **kwargs):
        super(FifthScreen, self).__init__(**kwargs)

        # Layout principal da tela
        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=20)

        # Cabeçalho do perfil
        header_layout = BoxLayout(orientation='vertical', size_hint=(1, 0.3))
        profile_name = Label(
            text="Shambhavi Mishra",
            font_size=24,
            bold=True,
            size_hint=(1, 0.5),
            color=get_color_from_hex("#FFFFFF")
        )
        profile_role = Label(
            text="Food Blogger",
            font_size=18,
            size_hint=(1, 0.5),
            color=get_color_from_hex("#666666")
        )
        header_layout.add_widget(profile_name)
        header_layout.add_widget(profile_role)
        main_layout.add_widget(header_layout)

        # Opções do perfil (usando ScrollView para rolagem)
        options_scroll = ScrollView(size_hint=(1, 0.7))
        options_layout = GridLayout(cols=1, size_hint_y=None, spacing=10, padding=10)
        options_layout.bind(minimum_height=options_layout.setter('height'))

        # Função para criar um botão clicável
        def create_button(text):
            button = Button(
                text=text,
                size_hint_y=None,
                height=50,
                background_color=get_color_from_hex("#FFFFFF"),  # Fundo branco
                color=get_color_from_hex("#000000"),  # Texto preto
                background_normal="",  # Remove o fundo padrão
                border=(0, 0, 0, 0)  # Remove a borda
            )
            return button
            
        self.btn_perfil = Button(
            text="Editar perfil ➤",
            size_hint_y=None,
            height=50,
            background_color=get_color_from_hex("#FFFFFF"),  # Fundo branco
            color=get_color_from_hex("#000000"),  # Texto preto
            background_normal="",  # Remove o fundo padrão
            border=(0, 0, 0, 0)  # Remove a borda
        )
        self.btn_perfil.bind(on_press=lambda x: self.go_to_screen("profile_screen"))

        # Adiciona os botões ao layout
        options_layout.add_widget(self.btn_perfil)
        options_layout.add_widget(create_button("Planos de renovação ➤"))
        options_layout.add_widget(create_button("Configurações ➤"))
        options_layout.add_widget(create_button("Termos e política de privacidade ➤"))
        options_layout.add_widget(create_button("Sair ➤"))

        options_scroll.add_widget(options_layout)
        main_layout.add_widget(options_scroll)

        # Adiciona o layout principal à tela
        self.add_widget(main_layout)

# Tela de Perfil
class ProfileScreen(Screen):
    def __init__(self, **kwargs):
        super(ProfileScreen, self).__init__(**kwargs)

        # Layout principal da tela
        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=20)

        # Título da tela
        title_label = Label(
            text="Editar Perfil",
            font_size=24,
            bold=True,
            size_hint=(1, 0.1),
            color=get_color_from_hex("#000000")
        )
        main_layout.add_widget(title_label)

        # Formulário (usando ScrollView para rolagem)
        form_scroll = ScrollView(size_hint=(1, 0.8))
        self.form_layout = GridLayout(cols=1, size_hint_y=None, spacing=10, padding=10)
        self.form_layout.bind(minimum_height=self.form_layout.setter('height'))

        def create_form_field(label_text, input_type="text", placeholder=""):
            field_layout = BoxLayout(orientation='vertical', size_hint_y=None, height=80)
            label = Label(
                text=label_text,
                size_hint=(1, 0.4),
                halign='left',
                valign='middle',
                color=get_color_from_hex("#000000")
            )
            label.bind(size=label.setter('text_size'))  # Ajusta o tamanho do texto
            input_field = TextInput(
                size_hint=(1, 0.6),
                multiline=False,
                hint_text=placeholder,
                password=(input_type == "password")  # Oculta o texto se for uma senha
            )
            field_layout.add_widget(label)
            field_layout.add_widget(input_field)
            return field_layout, input_field

        # Adiciona os campos ao formulário e armazena os campos em uma lista
        self.fields = {}
        field, input_field = create_form_field("Name", placeholder="Name")
        self.fields["name"] = input_field
        self.form_layout.add_widget(field)

        field, input_field = create_form_field("E-mail", placeholder="E-mail")
        self.fields["email"] = input_field
        self.form_layout.add_widget(field)

        field, input_field = create_form_field("Senha", input_type="password", placeholder="Senha")
        self.fields["senha"] = input_field
        self.form_layout.add_widget(field)

        field, input_field = create_form_field("Calorias diárias", placeholder="Kcal")
        self.fields["calorias"] = input_field
        self.form_layout.add_widget(field)

        field, input_field = create_form_field("Carboidratos diários", placeholder="carbo")
        self.fields["carboidratos"] = input_field
        self.form_layout.add_widget(field)

        field, input_field = create_form_field("Proteína diária", placeholder="protein")
        self.fields["proteina"] = input_field
        self.form_layout.add_widget(field)

        form_scroll.add_widget(self.form_layout)
        main_layout.add_widget(form_scroll)

        # Botão "Confirme"
        confirm_button = Button(
            text="Confirme",
            size_hint=(1, 0.1),
            background_color=get_color_from_hex("#8159EC"),  # Roxo
            color=get_color_from_hex("#FFFFFF")  # Texto branco
        )
        confirm_button.bind(on_press=self.confirmar_dados)  # Vincula a função ao botão
        main_layout.add_widget(confirm_button)

        # Adiciona o layout principal à tela
        self.add_widget(main_layout)

    def confirmar_dados(self, instance):
        # Coleta os dados do formulário
        dados = {
            "name": self.fields["name"].text,
            "email": self.fields["email"].text,
            "senha": self.fields["senha"].text,
            "calorias": self.fields["calorias"].text,
            "carboidratos": self.fields["carboidratos"].text,
            "proteina": self.fields["proteina"].text,
        }

        # Converte os dados para JSON
        dados_json = json.dumps(dados, indent=4)

        # Envia os dados para o servidor Flask
        try:
            response = requests.post(
                "http://127.0.0.1:5000/salvar_usuario",
                json=dados,
                headers={"Content-Type": "application/json"}
            )
            if response.status_code == 200:
                print("Dados enviados com sucesso!")
            else:
                print(f"Erro ao enviar dados: {response.text}")
        except Exception as e:
            print(f"Erro: {str(e)}")


# App principal
class ZephApp(App):
    def build(self):
        # Cria o gerenciador de telas
        sm = ScreenManager()

        # Adiciona as telas ao gerenciador
        sm.add_widget(TelaDafoto(name="first_screen"))
        sm.add_widget(SecondScreen(name="second_screen"))
        sm.add_widget(ThirdScreen(name="third_screen"))
        sm.add_widget(FourthScreen(name="fourth_screen"))
        sm.add_widget(FifthScreen(name="fifth_screen"))
        sm.add_widget(ProfileScreen(name="profile_screen"))

        # Define a tela inicial
        sm.current = "first_screen"

        # Atualiza as cores dos botões na tela inicial
        for screen in sm.screens:
            if isinstance(screen, BaseScreen):
                screen.update_button_colors(sm.current)

        # Monitora a mudança de tela para atualizar as cores dos botões
        sm.bind(current=self.on_screen_change)

        return sm

    def on_screen_change(self, instance, value):
        # Atualiza as cores dos botões sempre que a tela muda
        for screen in instance.screens:
            if isinstance(screen, BaseScreen):
                screen.update_button_colors(value)

if __name__ == '__main__':
    ZephApp().run()