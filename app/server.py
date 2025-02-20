from flask import Flask, request, jsonify
import os
import json
from datetime import datetime
import nutritionist

app = Flask(__name__)

# Pasta para salvar as imagens recebidas
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Pasta para armazenar os dados dos usuários
USUARIOS_DIR = "usuarios"
if not os.path.exists(USUARIOS_DIR):
    os.makedirs(USUARIOS_DIR)

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({"erro": "Nenhum arquivo enviado"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"erro": "Nome de arquivo inválido"}), 400

    # Salva a imagem na pasta "uploads"
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    # JSON fake para testes
    response_data = analyze_food_image(image_path)

    return jsonify(response_data), 200

@app.route("/salvar_usuario", methods=["POST"])
def salvar_usuario():
    try:
        # Recebe os dados do formulário
        dados = request.json

        # Salva os dados em um arquivo JSON
        usuario_id = len(os.listdir(USUARIOS_DIR)) + 1  # Gera um ID
        arquivo_usuario = os.path.join(USUARIOS_DIR, f"usuario_{usuario_id}.json")
        with open(arquivo_usuario, "w") as f:
            json.dump(dados, f, indent=4)

        return jsonify({"message": "Dados salvos com sucesso!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)