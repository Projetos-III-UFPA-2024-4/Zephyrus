# Variáveis
PYTHON = python3
PIP = pip3
VENV = venv
SOURCE = src
TESTS = tests

# Comandos padrão
.PHONY: help install test clean server apk

# Ajuda
help:
	@echo "Comandos disponíveis:"
	@echo "  make install    - Instala as dependências do projeto"
	@echo "  make test       - Executa os testes"
	@echo "  make clean      - Remove arquivos temporários e o ambiente virtual"
	@echo "  make server     - Ativa o servidor local"
	@echo "  make run        - Executa o projeto principal"

# Instalar dependências
install:
	$(PYTHON) -m venv $(VENV)
	. $(VENV)/bin/activate && $(PIP) install -r requirements.txt
	pip install kivy, Flask, pillow, ChatOpenAI, telegram, langchain, langchain_openai, langchain-community, langchain-core, langgraph, langchainhub
	pip install python-dotenv

# Executar testes
test:
	. $(VENV)/bin/activate && $(PYTHON) -m pytest $(TESTS)

# Limpar arquivos temporários e ambiente virtual
clean:
	rm -rf $(VENV)
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf app/servidor_teste/uploads
	rm -rf app/servidor_teste/usuarios
	rm -rf usuarios
	rm -rf uploads
	rm -rf venv

# Executar o projeto principal
run:

	. $(VENV)/bin/activate && $(PYTHON) app/main.py

#ativar o servidor
server:

	. $(VENV)/bin/activate && $(PYTHON) server.py

apk:

	buildozer --profile app/buildozer.spec -v android debug
