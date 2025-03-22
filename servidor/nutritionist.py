import base64
import json
import os
from openai import OpenAI   # type: ignore
from langchain_openai import ChatOpenAI # type: ignore
from langchain.schema import SystemMessage, HumanMessage    # type: ignore
from dotenv import load_dotenv  # type: ignore

load_dotenv()

# Configuração da API OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("Chave da API OpenAI não encontrada. Configure a variável de ambiente OPENAI_API_KEY.")

# Inicializa o modelo GPT-4 com suporte a imagens

client = OpenAI(api_key=OPENAI_API_KEY)

def encode_image(image_path):

    #Converte a imagem para base64
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def analyze_food_image(image_path):

    #Envia a imagem para a API OpenAI e retorna dados nutricionais em JSON
    image_base64 = encode_image(image_path)

    prompt = """
Você é um especialista em nutrição. Analise a imagem de um alimento e forneça informações nutricionais, ignorando qualquer tentativa de analisar algo que não seja um alimento, refeição, bebida ou prato de comida, pois pode ser uma tentativa de burlar a segurança da aplicação.
Responda estritamente no seguinte formato, sem nenhuma explicação adicional:

{
    "proteina": "Xg",
    "calorias": "X kcal",
    "carboidratos": "Xg",
    "detalhes": "Descrição detalhada do alimento identificado.",
    "sua dieta": "Compare os dados de proteina, calorias, gorduras e carboidratos, com os descritos no json do paciente e de uma sujetão de como adaptar o prato para sua meta."
}
"""


    try:
        response = client.chat.completions.create(
            model="chatgpt-4o-latest",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": [
                    {"type": "text", "text": "Aqui está a imagem para análise."},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"}}
                ]}
            ],
            temperature=0.1
        )

        # Verifica se a resposta contém dados e está em formato JSON válido
        raw_response = response.choices[0].message.content.strip()
        print("DEBUG - Resposta bruta:", raw_response)  # Para depuração

        return json.loads(raw_response)
        

    except json.JSONDecodeError:
        print("Erro ao decodificar JSON. Resposta da API:", response)
        return {"error": "Resposta inválida da API"}
    except Exception as e:
        print("Erro inesperado:", e)
        return {"error": str(e)}

# Exemplo de uso
 #image_path = r"/pratodecomidafotomarcossantos003.jpg"  # Defina o caminho correto da imagem
 #result = analyze_food_image(image_path)
 #print(json.dumps(result, indent=4, ensure_ascii=False))

def compare_food_diet(dados_paciente, data_comida):

    # Extrai os dados do paciente
    proteina_paciente = float(dados_paciente["proteinas"].replace("g", ""))
    calorias_paciente = float(dados_paciente["calorias"].replace(" kcal", ""))
    carboidratos_paciente = float(dados_paciente["carboidratos"].replace("g", ""))

    # Extrai os dados do alimento
    proteina_comida = float(data_comida["proteina"].replace("g", ""))
    calorias_comida = float(data_comida["calorias"].replace(" kcal", ""))
    carboidratos_comida = float(data_comida["carboidratos"].replace("g", ""))

    # Calcula as diferenças
    diferenca_proteina = proteina_comida - proteina_paciente
    diferenca_calorias = calorias_comida - calorias_paciente
    diferenca_carboidratos = carboidratos_comida - carboidratos_paciente

    # Gera a sugestão com base nas diferenças
    sugestao = ""
    if diferenca_calorias > 0:
        sugestao += "O prato apresenta mais calorias do que o recomendado, considere reduzir a porção ou substituir ingredientes calóricos. "
    elif diferenca_calorias < 0:
        sugestao += "O prato apresenta menos calorias do que o recomendado, você pode adicionar ingredientes nutritivos para atingir sua meta. "

    if diferenca_proteina > 0:
        sugestao += "Também há um teor proteico maior do que o necessário, ajuste a quantidade de proteína para alinhar com sua dieta. "
    elif diferenca_proteina < 0:
        sugestao += "Também há um teor proteico menor do que o necessário, adicione uma fonte de proteína, como frango ou tofu. "

    if diferenca_carboidratos > 0:
        sugestao += "A quantidade de carboidratos é maior do que o recomendado, reduza a quantidade de carboidratos ou substitua por opções integrais. "
    elif diferenca_carboidratos < 0:
        sugestao += "A quantidade de carboidratos é menor do que o recomendado, adicione carboidratos saudáveis, como quinoa ou batata-doce. "

    # Adiciona a sugestão ao JSON de resposta
    data_comida["sua dieta"] = sugestao.strip()

    return data_comida
