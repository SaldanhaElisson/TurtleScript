
from src import syntatic_tree

def main():
    # Exemplo da input 1
    syntatic_tree.Program(
        declarations=[
            syntatic_tree.Command("avancar", 150),
            syntatic_tree.Command("girar_direta", 90),
            syntatic_tree.Command("avancar", 150),
            syntatic_tree.Command("girar_direita", 90),
            syntatic_tree.Command("avancar", 150),
            syntatic_tree.Command("girar_direta", 90),
            syntatic_tree.Command("avancar", 150),
            syntatic_tree.Command("girar_direta", 90),
        ]
    )

    # Exemplo da input 2
    syntatic_tree.Program(
        declarations=[]
    )