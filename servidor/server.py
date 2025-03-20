from flask import Flask, request, jsonify  # type: ignore
import os
import json
from datetime import datetime
from servidor_.nutritionist import analyze_food_image  # type: ignore

app = Flask(__name__)

# Pasta para salvar as imagens recebidas
UPLOAD_FOLDER = "uploads"
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

    # Obtém o ID do usuário da requisição
    user_id = request.form.get('user_id')
    if not user_id:
        return jsonify({"erro": "ID do usuário não fornecido"}), 400

    # Cria uma pasta para o usuário, se não existir
    user_folder = os.path.join(UPLOAD_FOLDER, f"user_{user_id}")
    if not os.path.exists(user_folder):
        os.makedirs(user_folder)

    # Salva a imagem na pasta do usuário
    file_path = os.path.join(user_folder, file.filename)
    file.save(file_path)

    # Analisa a imagem
    response_data = analyze_food_image(file_path)

    # Adiciona o ID do usuário à resposta
    response_data["user_id"] = user_id

    return jsonify(response_data), 200

@app.route("/salvar_usuario", methods=["POST"])
def salvar_usuario():
    try:
        # Recebe os dados do formulário
        dados = request.json

        # Gera um ID único para o usuário
        usuario_id = len(os.listdir(USUARIOS_DIR)) + 1

        # Salva os dados em um arquivo JSON
        arquivo_usuario = os.path.join(USUARIOS_DIR, f"usuario_{usuario_id}.json")
        with open(arquivo_usuario, "w") as f:
            json.dump(dados, f, indent=4)

        # Retorna o ID do usuário
        return jsonify({"message": "Dados salvos com sucesso!", "user_id": usuario_id}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)