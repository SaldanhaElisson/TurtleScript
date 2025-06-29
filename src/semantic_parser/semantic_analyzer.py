from ..syntatic_tree import BinaryExpression, Literal, VariableReference, Assignment, Command, RepeatLoop
from ..symbols_table import SymbolTable

def infer_expression_type(expr, symbol_table):
    if isinstance(expr, Literal):
        return expr.type_
    elif isinstance(expr, VariableReference):
        return symbol_table.lookup(expr.name)
    if isinstance(expr, BinaryExpression):
        left_type = infer_expression_type(expr.left, symbol_table)
        right_type = infer_expression_type(expr.right, symbol_table)

        if expr.operator in ['+', '-', '*', '/', '%']:
            if expr.operator == '/':
                return 'real'
            
            if expr.operator == '%':
                return 'inteiro'
            
            if left_type == 'inteiro' and right_type == 'inteiro':
                return 'inteiro'
            
            if (left_type == 'real' or left_type == 'inteiro') and \
                (right_type == 'real' or right_type == 'inteiro') and not \
                (left_type == 'inteiro' and right_type == 'inteiro'):

                return 'real'
            else:
                raise Exception(f"Erro: Operador '{expr.operator}' só aceita inteiros.")
            


        if expr.operator in ['>', '<', '==']:
            if left_type == right_type:
                return 'logico'
            else:
                raise Exception(f"Erro: Comparação inválida entre '{left_type}' e '{right_type}'.")

    else:
        raise Exception("Erro: Tipo de expressão desconhecida.")
    
command_signature = {
    "avancar": ["inteiro"],
    "recuar": ["inteiro"],
    "girar_direita": ["inteiro"],
    "girar_esquerda": ["inteiro"],
    "ir_para": ["inteiro", "inteiro"],
    "levantar_caneta": [],
    "abaixar_caneta": [],
    "definir_cor": ["texto"],
    "definir_espessura": ["inteiro"],
    "limpar_tela": [],
    "cor_de_fundo": ["texto"],
}

def analyze_command(cmd, symbol_table):
    if isinstance(cmd, Assignment):
        var_type = symbol_table.lookup(cmd.var_name)
        expr_type = infer_expression_type(cmd.expression, symbol_table)
        if var_type != expr_type:
            raise Exception(f"Erro: Atribuição: variável '{cmd.var_name}' é do tipo '{var_type}' mas recebeu '{expr_type}'.")

    elif isinstance(cmd, Command):
        if cmd.name not in command_signature:
            raise Exception(f"Erro: Comando '{cmd.name}' não existe.")

        expected_args = command_signature[cmd.name]
        if len(expected_args) != len(cmd.args):
            raise Exception(f"Erro: Comando '{cmd.name}' espera {len(expected_args)} argumento(s).")

        for expected_type, arg in zip(expected_args, cmd.args):
            actual_type = infer_expression_type(arg, symbol_table)
            if actual_type != expected_type:
                raise Exception(f"Erro: Comando '{cmd.name}' esperava argumento '{expected_type}' mas recebeu '{actual_type}'.")

    elif isinstance(cmd, RepeatLoop):
        if not isinstance(cmd.count, Literal) or cmd.count.type_ != 'inteiro':
            raise Exception("Erro: O 'repita' deve receber um inteiro como número de repetições.")
        for inner_cmd in cmd.body:
            analyze_command(inner_cmd, symbol_table)

def analyze_program(program):
    symbol_table = SymbolTable()

    for decl in program.declarations:
        for name in decl.names:
            symbol_table.declare(name, decl.var_type)

    for cmd in program.commands:
        analyze_command(cmd, symbol_table)