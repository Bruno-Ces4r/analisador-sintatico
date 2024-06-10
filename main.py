import re

# Definição das palavras reservadas com tokens associados
reserved_words = {
    "if": 1,
    "else": 2,
    "while": 3,
    "return": 4,
    "int": 5,
    "float": 6,
    "void": 7,
    "char": 8
}

# Inicialização das tabelas de símbolos
reserved_words_table = {k: v for k, v in reserved_words.items()}
identifiers_table = {}
literals_table = {}

# Definição dos padrões de tokens
token_patterns = [
    (r'[ \t\n]+', None),  # Espaços em branco e tabulações (ignorar)
    (r'/\*.*?\*/', None),  # Comentários de múltiplas linhas (ignorar)
    (r'//.*', None),  # Comentários de uma linha (ignorar)
    (r'\d+\.\d*', 'NUM-FLOAT'),
    (r'\d+', 'NUM-INT'),
    (r'\".*?\"', 'STRING'),
    (r'[a-zA-Z_][a-zA-Z0-9_]*', 'ID'),
    (r'\+\+|\-\-|\+|\-|\*|\/|<=|>=|==|!=|<|>|&&|\|\||!|=|;|,|\(|\)|\{|\}|\[|\]', 'SYMBOL'),
]

# Função para converter símbolos específicos em tokens com nomes específicos
def get_symbol_token(symbol):
    symbols = {
        '(': 'LPARENT',
        ')': 'RPARENT',
        '{': 'LBRACE',
        '}': 'RBRACE',
        '[': 'LBRACKET',
        ']': 'RBRACKET',
        ';': 'SEMICOLON',
        ',': 'COMMA',
        '=': 'ASSIGN',
        '==': 'RELATIONALEQ',
        '!=': 'RELATIONALNEQ',
        '<': 'RELATIONALLT',
        '>': 'RELATIONALGT',
        '<=': 'RELATIONALLTE',
        '>=': 'RELATIONALGTE',
        '&&': 'LOGICALAND',
        '||': 'LOGICALOR',
        '!': 'LOGICALNOT',
        '+': 'PLUS',
        '-': 'MINUS',
        '*': 'TIMES',
        '/': 'DIVIDE'
    }
    return symbols.get(symbol, 'SYMBOL')

# Função para tokenizar o código-fonte
def tokenize(source_code):
    tokens = []
    position = 0
    line = 1
    
    while position < len(source_code):
        match = None
        for token_pattern in token_patterns:
            pattern, tag = token_pattern
            regex = re.compile(pattern)
            match = regex.match(source_code, position)
            if match:
                text = match.group(0)
                if tag:
                    if tag == 'ID':
                        if text in reserved_words:
                            tag = 'RESERVED'
                            reserved_words_table[text] = reserved_words[text]
                        else:
                            tag = f'ID.{text}'
                            if text not in identifiers_table:
                                identifiers_table[text] = len(identifiers_table) + 1
                    elif tag == 'NUM-FLOAT' or tag == 'NUM-INT':
                        tag = f'{tag}.{text}'
                        if text not in literals_table:
                            literals_table[text] = len(literals_table) + 1
                    elif tag == 'STRING':
                        tag = f'STRING.{text}'
                        if text not in literals_table:
                            literals_table[text] = len(literals_table) + 1
                    elif tag == 'SYMBOL':
                        tag = get_symbol_token(text)
                    tokens.append((tag, text, line))
                break
        if not match:
            print(f'Unexpected character {source_code[position]} at line {line}')
            position += 1
            continue
        position = match.end(0)
        line += text.count('\n')
    tokens.append(('EOF', 'EOF', line))
    return tokens

# Função para imprimir as tabelas de símbolos
def print_symbol_tables():
    print("\nReserved Words Table:")
    for word, token in reserved_words_table.items():
        print(f"{word}: {token}")

    print("\nIdentifiers Table:")
    for identifier, token in identifiers_table.items():
        print(f"{identifier}: {token}")

    print("\nLiterals Table:")
    for literal, token in literals_table.items():
        print(f"{literal}: {token}")

# Código fonte exemplo
source_code = '''
if (x1 <= 32) {
    b = 10;
}
'''

# Tokenizar o código fonte
tokens = tokenize(source_code)

# Imprimir os tokens
for token in tokens:
    print(token[0])

# Imprimir as tabelas de símbolos
print_symbol_tables()
