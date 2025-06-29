import sys
import os

# Adiciona o diretório 'src' ao PATH do Python
SRC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "src")
sys.path.append(SRC_DIR)

# Agora os imports funcionarão SEM precisar do prefixo 'src.'
from src.syntatic_tree import Program, Command  # Remove 'src.'
from src.semantic_parser.semantic_analyzer import analyze_program  # Remove 'src.'


print("Caminho do src:", SRC_DIR)  # Deve mostrar: .../Compiladores/src
print("Arquivos em src:", os.listdir(SRC_DIR))  # Deve listar syntatic_tree.py, semantic_parser/, etc.