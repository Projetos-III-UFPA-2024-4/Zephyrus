# Variáveis
PYTHON = python3
PIP = pip3
VENV = venv
SOURCE = src
TESTS = tests

# Comandos padrão
.PHONY: help install test clean apk

# Ajuda
help:
	@echo "Comandos disponíveis:"
	@echo "  make install    - Instala as dependências do projeto"
	@echo "  make test       - Executa os testes"
	@echo "  make clean      - Remove arquivos temporários e o ambiente virtual"
	@echo "  make run        - Executa o projeto principal"

# Instalar dependências
install:
	$(PYTHON) -m venv $(VENV)
	. $(VENV)/bin/activate && $(PIP) install -r requirements.txt

# Executar testes
test:
	. $(VENV)/bin/activate && $(PYTHON) -m pytest $(TESTS)

# Limpar arquivos temporários e ambiente virtual
clean:
	rm -rf $(VENV)
	buildozer android clean
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf app/servidor_teste/uploads
	rm -rf app/servidor_teste/usuarios
	rm -rf usuarios
	rm -rf uploads
	rm -rf venv

# Executar o projeto principal
run:

#	. $(VENV)/bin/activate && $(PYTHON) servidor_teste/server.py
	$(PYTHON) app/main.py

apk:

	buildozer android clean
	buildozer -v android debug
