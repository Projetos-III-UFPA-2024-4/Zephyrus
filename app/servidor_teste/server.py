from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# Pasta para salvar as imagens recebidas
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({"error": "Nenhum arquivo enviado"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "Nome de arquivo inválido"}), 400

    # Salva a imagem na pasta "uploads"
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    return jsonify({"message": "Imagem recebida com sucesso!", "path": file_path}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)