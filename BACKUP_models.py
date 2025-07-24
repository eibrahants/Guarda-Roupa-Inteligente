# Modelo de dados para o sistema de roupas
class Roupa:
    def __init__(self, id=None, nome=None, tipo=None, cor=None, ocasiao=None, 
                 temperatura_min=None, temperatura_max=None, imagem=None):
        self.id = id
        self.nome = nome
        self.tipo = tipo
        self.cor = cor
        self.ocasiao = ocasiao
        self.temperatura_min = temperatura_min
        self.temperatura_max = temperatura_max
        self.imagem = imagem
    
    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'tipo': self.tipo,
            'cor': self.cor,
            'ocasiao': self.ocasiao,
            'temperatura_min': self.temperatura_min,
            'temperatura_max': self.temperatura_max,
            'imagem': self.imagem
        }

def create_table(conn):
    """Cria a tabela 'roupas' no banco de dados se ela não existir"""
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS roupas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            tipo TEXT,
            cor TEXT,
            categoria TEXT,
            imagem_path TEXT,
            clima_min INTEGER,
            clima_max INTEGER
        )
    """)
    conn.commit()
    print("✅ Tabela 'roupas' criada/verificada com sucesso")
