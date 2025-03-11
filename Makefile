# Variáveis
PYTHON = python3
PIP = pip3
VENV = venv
SOURCE = src
TESTS = tests

# Comandos padrão
<<<<<<< HEAD
.PHONY: help install test clean apk
=======
.PHONY: help install test clean server
>>>>>>> 4d734eca2dfc864100122ae88583ce95fc102de3

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

<<<<<<< HEAD
#	. $(VENV)/bin/activate && $(PYTHON) servidor_teste/server.py
	$(PYTHON) app/main.py

apk:

	buildozer android clean
	buildozer -v android debug
=======
	. $(VENV)/bin/activate && $(PYTHON) app/main.py

#ativar o servidor
server:

	. $(VENV)/bin/activate && $(PYTHON) servidor_teste/server.py
>>>>>>> 4d734eca2dfc864100122ae88583ce95fc102de3
