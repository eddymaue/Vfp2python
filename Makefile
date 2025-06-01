# Makefile pour PyFoxPro IDE

.PHONY: help install run test clean lint format

help:
	@echo "Commandes disponibles:"
	@echo "  make install    - Installer les dépendances"
	@echo "  make run       - Lancer l'application"
	@echo "  make test      - Lancer les tests"
	@echo "  make lint      - Vérifier le code"
	@echo "  make format    - Formater le code"
	@echo "  make clean     - Nettoyer les fichiers temporaires"

install:
	pip install -r requirements.txt
	pip install pytest flake8 black

run:
	python src/main.py

test:
	pytest tests/

lint:
	flake8 src/ --max-line-length=100 --exclude=__pycache__

format:
	black src/ tests/

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +