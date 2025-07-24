# =============================================================================
# SISTEMA DE IA AVANÇADO - APRENDIZADO DE COMBINAÇÕES
# =============================================================================

from typing import Dict, List, Any, Tuple
from database import get_connection
import json
import math
from datetime import datetime, timedelta
import sqlite3

class StyleAI:
    """
    Sistema de IA que aprende as melhores combinações de roupas
    baseado em feedback do usuário, clima e regras de estilo
    """
    
    def __init__(self):
        self.inicializar_sistema_aprendizado()
        
    def inicializar_sistema_aprendizado(self):
        """Cria tabelas para armazenar dados de aprendizado"""
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            # Tabela para armazenar feedbacks de sugestões
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS sugestao_feedback (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    clima_data TEXT NOT NULL,
                    sugestao_data TEXT NOT NULL,
                    feedback_score INTEGER NOT NULL, -- 1-5 (1=péssimo, 5=excelente)
                    usado BOOLEAN DEFAULT FALSE,
                    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Tabela para armazenar combinações usadas
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS combinacoes_usadas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    roupa_ids TEXT NOT NULL, -- JSON array com IDs das roupas
                    clima_tipo TEXT NOT NULL,
                    temperatura INTEGER NOT NULL,
                    ocasiao TEXT DEFAULT 'casual',
                    satisfacao INTEGER DEFAULT 3, -- 1-5
                    data_uso TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Tabela para regras de harmonização de cores
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS harmonizacao_cores (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    cor1 TEXT NOT NULL,
                    cor2 TEXT NOT NULL,
                    compatibilidade REAL NOT NULL, -- 0.0-1.0
                    contexto TEXT DEFAULT 'geral', -- casual, formal, esportivo
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Tabela para preferências do usuário
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS preferencias_usuario (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    categoria TEXT NOT NULL, -- cor, estilo, tipo_roupa
                    item TEXT NOT NULL,
                    peso REAL DEFAULT 1.0, -- Importância da preferência
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(categoria, item)
                )
            """)
            
            conn.commit()
            self.inicializar_regras_base()
            
        except Exception as e:
            print(f"Erro ao inicializar sistema de aprendizado: {e}")
        finally:
            conn.close()
    
    def inicializar_regras_base(self):
        """Inicializa regras básicas de harmonização de cores e estilo"""
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            # Verificar se já existem regras
            cursor.execute("SELECT COUNT(*) FROM harmonizacao_cores")
            if cursor.fetchone()[0] > 0:
                return  # Já inicializado
            
            # Regras básicas de harmonização de cores
            regras_cores = [
                # Combinações clássicas
                ('preto', 'branco', 1.0, 'geral'),
                ('preto', 'cinza', 0.9, 'geral'),
                ('branco', 'azul', 0.9, 'geral'),
                ('branco', 'vermelho', 0.8, 'geral'),
                ('azul', 'branco', 0.9, 'geral'),
                ('azul', 'cinza', 0.8, 'geral'),
                ('azul', 'marrom', 0.7, 'casual'),
                
                # Tons neutros
                ('bege', 'marrom', 0.9, 'geral'),
                ('cinza', 'azul', 0.8, 'geral'),
                ('cinza', 'verde', 0.7, 'casual'),
                
                # Combinações arriscadas (menor compatibilidade)
                ('vermelho', 'verde', 0.3, 'geral'),
                ('laranja', 'rosa', 0.2, 'geral'),
                ('amarelo', 'roxo', 0.4, 'casual'),
                
                # Monocromáticas (sempre funcionam)
                ('azul', 'azul claro', 1.0, 'geral'),
                ('cinza', 'cinza claro', 1.0, 'geral'),
                ('verde', 'verde claro', 0.9, 'casual'),
            ]
            
            for cor1, cor2, compat, contexto in regras_cores:
                cursor.execute("""
                    INSERT INTO harmonizacao_cores (cor1, cor2, compatibilidade, contexto)
                    VALUES (?, ?, ?, ?)
                """, (cor1, cor2, compat, contexto))
                
                # Inserir também na ordem inversa
                cursor.execute("""
                    INSERT INTO harmonizacao_cores (cor1, cor2, compatibilidade, contexto)
                    VALUES (?, ?, ?, ?)
                """, (cor2, cor1, compat, contexto))
            
            conn.commit()
            
        except Exception as e:
            print(f"Erro ao inicializar regras base: {e}")
        finally:
            conn.close()
    
    def calcular_score_combinacao(self, roupas: List[Dict], clima_data: Dict) -> float:
        """
        Calcula um score de 0-100 para uma combinação de roupas
        considerando clima, cores, estilo e histórico
        """
        if not roupas:
            return 0.0
        
        scores = {
            'clima': self.score_adequacao_clima(roupas, clima_data),
            'cores': self.score_harmonizacao_cores(roupas),
            'estilo': self.score_coerencia_estilo(roupas),
            'historico': self.score_historico_uso(roupas, clima_data),
            'preferencias': self.score_preferencias_usuario(roupas)
        }
        
        # Pesos para cada componente
        pesos = {
            'clima': 0.35,      # Mais importante - adequação ao clima
            'cores': 0.25,      # Importante - harmonização visual
            'estilo': 0.20,     # Coerência do conjunto
            'historico': 0.15,  # Aprendizado com uso anterior
            'preferencias': 0.05 # Gostos pessoais
        }
        
        score_final = sum(scores[tipo] * peso for tipo, peso in pesos.items())
        return min(100.0, max(0.0, score_final))
    
    def score_adequacao_clima(self, roupas: List[Dict], clima_data: Dict) -> float:
        """Score baseado na adequação das roupas ao clima"""
        temperatura = clima_data.get('temperatura', 20)
        umidade = clima_data.get('umidade', 60)
        condicao = clima_data.get('condicao', '').lower()
        
        score = 0.0
        total_pecas = len(roupas)
        
        for roupa in roupas:
            clima_min = roupa.get('clima_min', 0)
            clima_max = roupa.get('clima_max', 50)
            tipo = roupa.get('tipo', '').lower()
            
            # Score básico por temperatura
            if clima_min <= temperatura <= clima_max:
                score += 25  # Dentro da faixa ideal
            else:
                diferenca = min(abs(temperatura - clima_min), abs(temperatura - clima_max))
                score += max(0, 25 - (diferenca * 2))
            
            # Bonus/penalty por tipo de peça vs clima
            if temperatura <= 15:  # Frio
                if any(t in tipo for t in ['jaqueta', 'casaco', 'moletom']):
                    score += 10
                elif any(t in tipo for t in ['shorts', 'regata']):
                    score -= 15
            elif temperatura >= 28:  # Quente
                if any(t in tipo for t in ['shorts', 'regata', 'camiseta']):
                    score += 10
                elif any(t in tipo for t in ['jaqueta', 'casaco']):
                    score -= 15
            
            # Considerações especiais para chuva
            if 'chuva' in condicao:
                if 'impermeável' in tipo or 'bota' in tipo:
                    score += 5
                elif 'sandália' in tipo or 'chinelo' in tipo:
                    score -= 10
        
        return score / total_pecas if total_pecas > 0 else 0.0
    
    def score_harmonizacao_cores(self, roupas: List[Dict]) -> float:
        """Score baseado na harmonização entre as cores das roupas"""
        if len(roupas) < 2:
            return 25.0  # Neutro para uma peça só
        
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            cores = [roupa.get('cor', '').lower() for roupa in roupas if roupa.get('cor')]
            
            if len(cores) < 2:
                return 20.0
            
            score_total = 0.0
            comparacoes = 0
            
            # Comparar todas as combinações de cores
            for i in range(len(cores)):
                for j in range(i + 1, len(cores)):
                    cor1, cor2 = cores[i], cores[j]
                    
                    # Buscar compatibilidade no banco
                    cursor.execute("""
                        SELECT compatibilidade FROM harmonizacao_cores
                        WHERE (cor1 = ? AND cor2 = ?) OR (cor1 = ? AND cor2 = ?)
                        ORDER BY compatibilidade DESC LIMIT 1
                    """, (cor1, cor2, cor2, cor1))
                    
                    result = cursor.fetchone()
                    if result:
                        score_total += result[0] * 25  # Converter para escala 0-25
                        comparacoes += 1
                    else:
                        # Heurística para cores não catalogadas
                        if cor1 == cor2:
                            score_total += 20  # Monocromático é seguro
                        elif any(cor in ['preto', 'branco', 'cinza'] for cor in [cor1, cor2]):
                            score_total += 18  # Neutros combinam com quase tudo
                        else:
                            score_total += 10  # Desconhecido = médio
                        comparacoes += 1
            
            return score_total / comparacoes if comparacoes > 0 else 15.0
            
        except Exception as e:
            print(f"Erro ao calcular score de cores: {e}")
            return 15.0
        finally:
            conn.close()
    
    def score_coerencia_estilo(self, roupas: List[Dict]) -> float:
        """Score baseado na coerência de estilo entre as peças"""
        if not roupas:
            return 0.0
        
        # Categorizar estilos por tipo de roupa
        estilos_formais = ['blazer', 'terno', 'camisa social', 'sapato social']
        estilos_casuais = ['camiseta', 'jeans', 'tênis', 'moletom']
        estilos_esportivos = ['shorts', 'regata', 'tênis', 'legging']
        
        formal_count = 0
        casual_count = 0
        esportivo_count = 0
        
        for roupa in roupas:
            tipo = roupa.get('tipo', '').lower()
            
            if any(estilo in tipo for estilo in estilos_formais):
                formal_count += 1
            elif any(estilo in tipo for estilo in estilos_casuais):
                casual_count += 1
            elif any(estilo in tipo for estilo in estilos_esportivos):
                esportivo_count += 1
        
        total_pecas = len(roupas)
        
        # Calcular dominância de um estilo
        dominancia_formal = formal_count / total_pecas
        dominancia_casual = casual_count / total_pecas
        dominancia_esportivo = esportivo_count / total_pecas
        
        # Quanto mais coerente (um estilo dominante), maior o score
        max_dominancia = max(dominancia_formal, dominancia_casual, dominancia_esportivo)
        
        # Penalty para misturas muito estranhas (formal + esportivo)
        if formal_count > 0 and esportivo_count > 0:
            max_dominancia *= 0.7
        
        return max_dominancia * 20  # Score de 0-20
    
    def score_historico_uso(self, roupas: List[Dict], clima_data: Dict) -> float:
        """Score baseado em combinações anteriores bem avaliadas"""
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            roupa_ids = [str(roupa.get('id', 0)) for roupa in roupas if roupa.get('id')]
            if not roupa_ids:
                return 10.0  # Neutro
            
            temperatura = clima_data.get('temperatura', 20)
            clima_tipo = self.classificar_clima_simples(clima_data)
            
            # Buscar combinações similares no histórico
            cursor.execute("""
                SELECT AVG(satisfacao) as media_satisfacao, COUNT(*) as total_usos
                FROM combinacoes_usadas
                WHERE clima_tipo = ? 
                AND ABS(temperatura - ?) <= 5
                AND (
                    json_extract(roupa_ids, '$') LIKE '%' || ? || '%'
                    OR json_extract(roupa_ids, '$') LIKE '%' || ? || '%'
                )
            """, (clima_tipo, temperatura, roupa_ids[0], roupa_ids[-1] if len(roupa_ids) > 1 else roupa_ids[0]))
            
            result = cursor.fetchone()
            if result and result[0]:
                media_satisfacao = result[0]
                total_usos = result[1]
                
                # Converter satisfação (1-5) para score (0-15) com peso por uso
                score_base = ((media_satisfacao - 3) / 2) * 15  # -15 a +15
                peso_experiencia = min(1.0, total_usos / 5)  # Mais peso com mais usos
                
                return score_base * peso_experiencia
            
            return 8.0  # Levemente positivo para encorajar experimentação
            
        except Exception as e:
            print(f"Erro ao calcular score de histórico: {e}")
            return 10.0
        finally:
            conn.close()
    
    def score_preferencias_usuario(self, roupas: List[Dict]) -> float:
        """Score baseado nas preferências do usuário"""
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT categoria, item, peso FROM preferencias_usuario")
            preferencias = cursor.fetchall()
            
            if not preferencias:
                return 2.5  # Neutro
            
            score = 0.0
            peso_total = 0.0
            
            for categoria, valor, peso in preferencias:
                peso_total += peso
                
                if categoria == 'cor':
                    for roupa in roupas:
                        if roupa.get('cor', '').lower() == valor.lower():
                            score += peso * 5
                
                elif categoria == 'tipo':
                    for roupa in roupas:
                        if valor.lower() in roupa.get('tipo', '').lower():
                            score += peso * 3
                
                elif categoria == 'cor_evitada':
                    for roupa in roupas:
                        if roupa.get('cor', '').lower() == valor.lower():
                            score -= peso * 3
            
            return score / peso_total if peso_total > 0 else 2.5
            
        except Exception as e:
            print(f"Erro ao calcular preferências: {e}")
            return 2.5
        finally:
            conn.close()
    
    def classificar_clima_simples(self, clima_data: Dict) -> str:
        """Classificação simples do clima para histórico"""
        temperatura = clima_data.get('temperatura', 20)
        
        if temperatura <= 15:
            return 'frio'
        elif temperatura <= 25:
            return 'ameno'
        else:
            return 'quente'
    
    def registrar_uso_combinacao(self, roupas: List[Dict], clima_data: Dict, satisfacao: int = 3):
        """Registra uma combinação usada para aprendizado futuro"""
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            roupa_ids = [roupa.get('id') for roupa in roupas if roupa.get('id')]
            clima_tipo = self.classificar_clima_simples(clima_data)
            temperatura = clima_data.get('temperatura', 20)
            
            cursor.execute("""
                INSERT INTO combinacoes_usadas (roupa_ids, clima_tipo, temperatura, satisfacao)
                VALUES (?, ?, ?, ?)
            """, (json.dumps(roupa_ids), clima_tipo, temperatura, satisfacao))
            
            conn.commit()
            
        except Exception as e:
            print(f"Erro ao registrar uso: {e}")
        finally:
            conn.close()
    
    def aprender_harmonizacao_cor(self, cor1: str, cor2: str, compatibilidade: float):
        """Aprende ou atualiza a compatibilidade entre duas cores"""
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            # Verificar se já existe
            cursor.execute("""
                SELECT compatibilidade FROM harmonizacao_cores
                WHERE cor1 = ? AND cor2 = ?
            """, (cor1.lower(), cor2.lower()))
            
            result = cursor.fetchone()
            
            if result:
                # Média ponderada: 70% do valor atual + 30% do novo
                nova_compatibilidade = result[0] * 0.7 + compatibilidade * 0.3
                cursor.execute("""
                    UPDATE harmonizacao_cores
                    SET compatibilidade = ?, updated_at = CURRENT_TIMESTAMP
                    WHERE cor1 = ? AND cor2 = ?
                """, (nova_compatibilidade, cor1.lower(), cor2.lower()))
            else:
                # Inserir nova regra
                cursor.execute("""
                    INSERT INTO harmonizacao_cores (cor1, cor2, compatibilidade)
                    VALUES (?, ?, ?)
                """, (cor1.lower(), cor2.lower(), compatibilidade))
            
            conn.commit()
            
        except Exception as e:
            print(f"Erro ao aprender harmonização: {e}")
        finally:
            conn.close()
    
    def definir_preferencia_usuario(self, tipo: str, valor: str, peso: float = 1.0):
        """Define uma preferência do usuário"""
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT OR REPLACE INTO preferencias_usuario (categoria, item, peso)
                VALUES (?, ?, ?)
            """, (tipo, valor.lower(), peso))
            
            conn.commit()
            
        except Exception as e:
            print(f"Erro ao definir preferência: {e}")
        finally:
            conn.close()

# Instância global da IA
style_ai = StyleAI()
