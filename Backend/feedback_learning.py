# =============================================================================
# SISTEMA DE APRENDIZADO POR FEEDBACK - IA ADAPTATIVA
# =============================================================================

import sqlite3
import json
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from database import get_connection

class FeedbackLearningSystem:
    """Sistema de aprendizado que coleta feedback do usuário e adapta as sugestões"""
    
    def __init__(self):
        self.criar_tabelas_feedback()
    
    def criar_tabelas_feedback(self):
        """Cria tabelas necessárias para armazenar feedback e aprendizado"""
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            # Verificar se tabela preferencias_usuario existe e tem estrutura correta
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='preferencias_usuario'")
            tabela_existe = cursor.fetchone()
            
            if tabela_existe:
                # Verificar se tem a coluna categoria
                cursor.execute("PRAGMA table_info(preferencias_usuario)")
                colunas = [col[1] for col in cursor.fetchall()]
                if 'categoria' not in colunas:
                    # Recriar a tabela com estrutura correta
                    cursor.execute('DROP TABLE IF EXISTS preferencias_usuario')
            
            # Tabela de feedback das sugestões
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS feedback_sugestoes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    data_sugestao DATETIME NOT NULL,
                    clima_data TEXT NOT NULL,  -- JSON do clima
                    combinacao_sugerida TEXT NOT NULL,  -- JSON da combinação
                    score_original REAL NOT NULL,
                    feedback_usuario INTEGER CHECK(feedback_usuario IN (1, 2, 3, 4, 5)) NOT NULL,
                    comentario TEXT,
                    usado BOOLEAN DEFAULT FALSE,
                    data_feedback DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Tabela de padrões aprendidos
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS padroes_aprendidos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    tipo_clima TEXT NOT NULL,  -- sol, chuva, frio, etc.
                    temperatura_faixa TEXT NOT NULL,  -- quente, morno, frio
                    combinacao_pattern TEXT NOT NULL,  -- JSON do padrão
                    score_medio REAL NOT NULL,
                    frequencia_uso INTEGER DEFAULT 1,
                    ultima_atualizacao DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Tabela de preferências do usuário
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS preferencias_usuario (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    categoria TEXT NOT NULL,  -- cor, estilo, tipo_roupa
                    item TEXT NOT NULL,  -- azul, casual, camisa, etc.
                    peso REAL DEFAULT 1.0,  -- peso da preferência (-1 a 1)
                    ultima_atualizacao DATETIME DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(categoria, item)
                )
            ''')
            
            # Tabela de histórico de uso
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS historico_uso (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    roupa_id INTEGER NOT NULL,
                    data_uso DATE NOT NULL,
                    clima_data TEXT NOT NULL,
                    satisfacao INTEGER CHECK(satisfacao IN (1, 2, 3, 4, 5)),
                    FOREIGN KEY (roupa_id) REFERENCES roupas (id)
                )
            ''')
            
            conn.commit()
            conn.close()
            print("✅ Tabelas de feedback criadas/verificadas com sucesso")
            
        except Exception as e:
            print(f"❌ Erro ao criar tabelas de feedback: {e}")
            # Se der erro, podemos continuar sem o sistema de aprendizado
            pass
    
    def registrar_feedback(self, sugestao_id: str, feedback: Dict[str, Any]) -> bool:
        """
        Registra feedback do usuário sobre uma sugestão
        
        Args:
            sugestao_id: ID da sugestão
            feedback: {
                'rating': int (1-5),
                'usado': bool,
                'comentario': str (opcional),
                'clima_data': dict,
                'combinacao': dict
            }
        """
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO feedback_sugestoes 
                (data_sugestao, clima_data, combinacao_sugerida, score_original, 
                 feedback_usuario, comentario, usado)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                datetime.now(),
                json.dumps(feedback['clima_data']),
                json.dumps(feedback['combinacao']),
                feedback.get('score_original', 0),
                feedback['rating'],
                feedback.get('comentario', ''),
                feedback.get('usado', False)
            ))
            
            # Atualizar padrões aprendidos
            self._atualizar_padroes_aprendidos(feedback)
            
            # Atualizar preferências do usuário
            self._atualizar_preferencias_usuario(feedback)
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            print(f"Erro ao registrar feedback: {e}")
            return False
    
    def _atualizar_padroes_aprendidos(self, feedback: Dict[str, Any]):
        """Atualiza padrões aprendidos baseado no feedback"""
        try:
            clima = feedback['clima_data']
            combinacao = feedback['combinacao']
            rating = feedback['rating']
            
            # Classificar tipo de clima
            tipo_clima = self._classificar_clima(clima)
            temperatura_faixa = self._classificar_temperatura(clima.get('temperatura', 20))
            
            # Criar padrão da combinação
            pattern = self._extrair_pattern_combinacao(combinacao)
            
            conn = get_connection()
            cursor = conn.cursor()
            
            # Verificar se padrão já existe
            cursor.execute('''
                SELECT id, score_medio, frequencia_uso 
                FROM padroes_aprendidos 
                WHERE tipo_clima = ? AND temperatura_faixa = ? AND combinacao_pattern = ?
            ''', (tipo_clima, temperatura_faixa, json.dumps(pattern)))
            
            existing = cursor.fetchone()
            
            if existing:
                # Atualizar padrão existente
                id_pattern, score_atual, freq_atual = existing
                novo_score = (score_atual * freq_atual + rating) / (freq_atual + 1)
                
                cursor.execute('''
                    UPDATE padroes_aprendidos 
                    SET score_medio = ?, frequencia_uso = ?, ultima_atualizacao = ?
                    WHERE id = ?
                ''', (novo_score, freq_atual + 1, datetime.now(), id_pattern))
            else:
                # Criar novo padrão
                cursor.execute('''
                    INSERT INTO padroes_aprendidos 
                    (tipo_clima, temperatura_faixa, combinacao_pattern, score_medio)
                    VALUES (?, ?, ?, ?)
                ''', (tipo_clima, temperatura_faixa, json.dumps(pattern), rating))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"Erro ao atualizar padrões: {e}")
    
    def _atualizar_preferencias_usuario(self, feedback: Dict[str, Any]):
        """Atualiza preferências do usuário baseado no feedback"""
        try:
            combinacao = feedback['combinacao']
            rating = feedback['rating']
            
            # Extrair cores, estilos e tipos de roupa
            preferencias = self._extrair_preferencias_combinacao(combinacao)
            
            conn = get_connection()
            cursor = conn.cursor()
            
            for categoria, items in preferencias.items():
                for item in items:
                    # Calcular novo peso da preferência
                    peso_feedback = (rating - 3) * 0.2  # Rating 1-5 -> peso -0.4 a 0.4
                    
                    cursor.execute('''
                        INSERT OR REPLACE INTO preferencias_usuario 
                        (categoria, item, peso, ultima_atualizacao)
                        VALUES (?, ?, 
                            COALESCE((SELECT peso FROM preferencias_usuario WHERE categoria = ? AND item = ?), 0) + ?,
                            ?)
                    ''', (categoria, item, categoria, item, peso_feedback, datetime.now()))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"Erro ao atualizar preferências: {e}")
    
    def obter_preferencias_usuario(self) -> Dict[str, Dict[str, float]]:
        """Obtém preferências atuais do usuário"""
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT categoria, item, peso 
                FROM preferencias_usuario 
                ORDER BY categoria, peso DESC
            ''')
            
            preferencias = {}
            for categoria, item, peso in cursor.fetchall():
                if categoria not in preferencias:
                    preferencias[categoria] = {}
                preferencias[categoria][item] = peso
            
            conn.close()
            return preferencias
            
        except Exception as e:
            print(f"Erro ao obter preferências: {e}")
            return {}
    
    def obter_padroes_aprendidos(self, clima_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Obtém padrões aprendidos relevantes para o clima atual"""
        try:
            tipo_clima = self._classificar_clima(clima_data)
            temperatura_faixa = self._classificar_temperatura(clima_data.get('temperatura', 20))
            
            conn = get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT combinacao_pattern, score_medio, frequencia_uso
                FROM padroes_aprendidos 
                WHERE tipo_clima = ? AND temperatura_faixa = ?
                ORDER BY score_medio DESC, frequencia_uso DESC
                LIMIT 10
            ''', (tipo_clima, temperatura_faixa))
            
            padroes = []
            for pattern_json, score, freq in cursor.fetchall():
                padroes.append({
                    'pattern': json.loads(pattern_json),
                    'score': score,
                    'frequencia': freq
                })
            
            conn.close()
            return padroes
            
        except Exception as e:
            print(f"Erro ao obter padrões: {e}")
            return []
    
    def _classificar_clima(self, clima_data: Dict[str, Any]) -> str:
        """Classifica o tipo de clima em categorias"""
        condicao = clima_data.get('condicao', '').lower()
        
        if any(word in condicao for word in ['chuva', 'chuvisco', 'tempest']):
            return 'chuva'
        elif any(word in condicao for word in ['nuvem', 'nublado', 'encoberto']):
            return 'nublado'
        elif any(word in condicao for word in ['sol', 'limpo', 'claro']):
            return 'sol'
        elif any(word in condicao for word in ['vento', 'ventania']):
            return 'ventoso'
        else:
            return 'normal'
    
    def _classificar_temperatura(self, temperatura: float) -> str:
        """Classifica a temperatura em faixas"""
        if temperatura < 15:
            return 'frio'
        elif temperatura < 25:
            return 'morno'
        else:
            return 'quente'
    
    def _extrair_pattern_combinacao(self, combinacao: Dict[str, Any]) -> Dict[str, Any]:
        """Extrai padrão da combinação para aprendizado"""
        pattern = {}
        
        for categoria, roupa in combinacao.items():
            if roupa:
                pattern[categoria] = {
                    'tipo': roupa.get('tipo', ''),
                    'cor': roupa.get('cor', ''),
                    'estilo': roupa.get('estilo', '')
                }
        
        return pattern
    
    def _extrair_preferencias_combinacao(self, combinacao: Dict[str, Any]) -> Dict[str, List[str]]:
        """Extrai preferências da combinação (cores, estilos, tipos)"""
        preferencias = {
            'cor': [],
            'estilo': [],
            'tipo_roupa': []
        }
        
        for categoria, roupa in combinacao.items():
            if roupa:
                if roupa.get('cor'):
                    preferencias['cor'].append(roupa['cor'])
                if roupa.get('estilo'):
                    preferencias['estilo'].append(roupa['estilo'])
                if roupa.get('tipo'):
                    preferencias['tipo_roupa'].append(roupa['tipo'])
        
        return preferencias

# Instância global do sistema de aprendizado
feedback_system = FeedbackLearningSystem()
