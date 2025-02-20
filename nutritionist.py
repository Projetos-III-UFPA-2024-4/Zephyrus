import base64
import json
import os
from openai import OpenAI
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
from dotenv import load_dotenv

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
    Você é um especialista em nutrição. Analise a imagem de um alimento e forneça informações nutricionais, ignore qualquer tentativa de analisar algo que não seja um alimento, refeição, bebida ou prato de comida pois pode ser uma tentativa de burlar a segurança.
    Responda estritamente no seguinte formato JSON:
    {
        "alimentos": [
            {
                "nome": "Nome do alimento",
                "carboidratos": "Xg",
                "proteínas": "Xg",
                "gorduras": "Xg",
                "calorias": "X kcal"
            }
        ]
    }
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
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
image_path = r"D:\Biblioteca\UFPA\Arquivos\Bloco V\ProjIII\Zephyrus\app\ia_teste\download.jpg"  # Defina o caminho correto da imagem
result = analyze_food_image(image_path)
print(json.dumps(result, indent=4, ensure_ascii=False))
