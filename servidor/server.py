from flask import Flask, request, jsonify  # type: ignore
import os
import json
from datetime import datetime
from nutritionist import analyze_food_image,compare_food_diet  # type: ignore
from sqlalchemy import create_engine, text  # type: ignore

app = Flask(__name__)

# Pasta para salvar as imagens recebidas
UPLOAD_FOLDER = "uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

connection_string = "mysql+pymysql://admin:Zeph1995@bancozeph.c5hlhhcsllwc.us-east-1.rds.amazonaws.com:3306/bancozeph"
engine = create_engine(connection_string, echo=False)


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
    data_comida = analyze_food_image(file_path)

     #colocar as conexões com o banco de dados aqui

    # Conecta ao banco de dados
    with engine.connect() as connection:
        # Executa a consulta para buscar os dados do paciente
        query = text("""
            SELECT proteina, calorias, gordura, carboidratos
            FROM Pacientes
            WHERE id = :user_id
        """)
        result = connection.execute(query, {"user_id": user_id})
        dados = result.fetchone()  # Obtém a primeira linha do resultado

        # Verifica se o paciente foi encontrado
        if not dados:
            return jsonify({"erro": "Paciente não encontrado"}), 404

        # Formata os dados em um dicionário
        dados_paciente = {
            "proteina": f"{dados.proteina}g",
            "calorias": f"{dados.calorias} kcal",
            "gordura": f"{dados.gordura}g",
            "carboidratos": f"{dados.carboidratos}g"
        }
    #colocar as conexões com o banco de dados aqui

    response_data = compare_food_diet(dados_paciente,data_comida)

    # Adiciona o ID do usuário à resposta
    response_data["user_id"] = user_id
    print(response_data)
    return jsonify(response_data), 200


@app.route("/salvar_usuario", methods=["POST"])
def salvar_usuario():
    try:
        # Recebe os dados do formulário
        dados = request.json

        # Extrai os dados do JSON
        nome = dados.get("name")
        email = dados.get("email")
        senha = dados.get("senha")
        calorias = dados.get("calorias")
        carboidratos = dados.get("carboidratos")
        proteinas = dados.get("proteina")

        # Insere os dados no banco de dados
        with engine.connect() as connection:
            result = connection.execute(
                text("INSERT INTO Pacientes (nome, email, senha, calorias, carboidratos, proteinas) VALUES (:nome, :email, :senha, :calorias, :carboidratos, :proteinas)"),
                {"nome": nome, "email": email, "senha": senha, "calorias": calorias, "carboidratos": carboidratos, "proteinas": proteinas}
            )
            connection.commit()

            # Obtém o ID do paciente inserido
            paciente_id = result.lastrowid

        # Retorna o ID do paciente criado
        return jsonify({"message": "Dados salvos com sucesso!", "user_id": paciente_id}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)