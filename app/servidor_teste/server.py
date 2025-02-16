from flask import Flask, request, jsonify
import os
from datetime import datetime

app = Flask(__name__)

# Pasta para salvar as imagens recebidas
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

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
    response_data = {
        "message": "Imagem recebida com sucesso!",
        "proteina": "450g",
        "calorias": "220kcal",
        "gordura": "100g",
        "carboidratos": "49g",
        "detalhes": "Um hambúrguer é um sanduíche composto por um ou ",
        "sua dieta": "A quantidade de carboidratos excede os limites de sua prescrição",
        
    }

    return jsonify(response_data), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)