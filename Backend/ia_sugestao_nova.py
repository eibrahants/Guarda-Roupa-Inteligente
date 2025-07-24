import random
from typing import List, Dict, Any, Tuple
from database import get_connection
from style_ai_avancado import style_ai
from feedback_learning import feedback_system

def gerar_sugestao_inteligente(clima_data: Dict[str, Any]) -> Dict[str, Any]:
    """Gera sugestão inteligente usando IA avançada que aprende com o tempo"""
    try:
        roupas_disponiveis = obter_roupas_disponiveis()
        
        if not roupas_disponiveis:
            return {
                'erro': 'Nenhuma roupa encontrada no guarda-roupa',
                'sugestao': None,
                'score': 0,
                'detalhes': {}
            }
        
        preferencias_usuario = feedback_system.obter_preferencias_usuario()
        padroes_aprendidos = feedback_system.obter_padroes_aprendidos(clima_data)
        
        melhores_combinacoes = []
        
        for padrao in padroes_aprendidos[:5]:
            combinacao = gerar_combinacao_por_padrao(roupas_disponiveis, padrao['pattern'], clima_data)
            if combinacao:
                score = style_ai.calcular_score_combinacao(combinacao, clima_data)
                score += padrao['score'] * 0.2 + padrao['frequencia'] * 0.1
                melhores_combinacoes.append((combinacao, score))
        
        for _ in range(45):
            combinacao = gerar_combinacao_aleatoria_inteligente(roupas_disponiveis, clima_data, preferencias_usuario)
            if combinacao:
                score = style_ai.calcular_score_combinacao(combinacao, clima_data)
                score += calcular_bonus_preferencias(combinacao, preferencias_usuario)
                melhores_combinacoes.append((combinacao, score))
        
        if not melhores_combinacoes:
            return gerar_sugestao_basica_fallback(roupas_disponiveis, clima_data)
        
        melhores_combinacoes.sort(key=lambda x: x[1], reverse=True)
        melhor_combinacao, melhor_score = melhores_combinacoes[0]
        
        detalhes_analise = analisar_combinacao_detalhada(melhor_combinacao, clima_data)
        
        detalhes_analise['aprendizado'] = {
            'padroes_usados': len(padroes_aprendidos),
            'preferencias_aplicadas': bool(preferencias_usuario),
            'score_ia': melhor_score
        }
        
        alternativas = []
        for combinacao, score in melhores_combinacoes[1:3]:
            alternativas.append({
                'roupas': combinacao,
                'score': round(score, 1),
                'descricao': gerar_descricao_combinacao(combinacao)
            })
        
        return {
            'sugestao': melhor_combinacao,
            'score': round(melhor_score, 1),
            'detalhes': detalhes_analise,
            'alternativas': alternativas,
            'clima': clima_data,
            'timestamp': obter_timestamp()
        }
        
    except Exception as e:
        print(f"Erro na sugestão inteligente: {e}")
        return gerar_sugestao_basica_fallback(obter_roupas_disponiveis(), clima_data)

def gerar_combinacao_aleatoria_inteligente(roupas: List[Dict], clima_data: Dict, preferencias: Dict[str, Dict[str, float]] = None) -> List[Dict]:
    """Gera uma combinação completa (superior, inferior, calçado) e adiciona casaco quando necessário"""
    temperatura = clima_data.get('temperatura', 20)
    condicao = clima_data.get('condicao', '').lower()
    
    roupas_adequadas = filtrar_roupas_por_clima(roupas, temperatura, condicao)
    
    if not roupas_adequadas:
        roupas_adequadas = roupas
    
    if preferencias:
        roupas_adequadas = aplicar_preferencias_selecao(roupas_adequadas, preferencias)
    
    categorias = categorizar_roupas(roupas_adequadas)
    
    combinacao = []
    
    if categorias['superior']:
        combinacao.append(random.choice(categorias['superior']))
    else:
        todas_categorias = categorizar_roupas(roupas)
        if todas_categorias['superior']:
            combinacao.append(random.choice(todas_categorias['superior']))
    
    if categorias['inferior']:
        combinacao.append(random.choice(categorias['inferior']))
    else:
        todas_categorias = categorizar_roupas(roupas)
        if todas_categorias['inferior']:
            combinacao.append(random.choice(todas_categorias['inferior']))
    
    if categorias['calçado']:
        combinacao.append(random.choice(categorias['calçado']))
    else:
        todas_categorias = categorizar_roupas(roupas)
        if todas_categorias['calçado']:
            combinacao.append(random.choice(todas_categorias['calçado']))
    
    if temperatura <= 25:
        if categorias['casaco']:
            combinacao.append(random.choice(categorias['casaco']))
        else:
            todas_categorias = categorizar_roupas(roupas)
            if todas_categorias['casaco']:
                combinacao.append(random.choice(todas_categorias['casaco']))
    
    if categorias['acessorios'] and random.random() < 0.2:
        combinacao.append(random.choice(categorias['acessorios']))
    
    return combinacao

def filtrar_roupas_por_clima(roupas: List[Dict], temperatura: int, condicao: str) -> List[Dict]:
    """Filtra roupas apropriadas para o clima atual"""
    roupas_adequadas = []
    
    for roupa in roupas:
        clima_min = roupa.get('clima_min', 0)
        clima_max = roupa.get('clima_max', 50)
        tipo = roupa.get('tipo', '').lower()
        
        if clima_min <= temperatura <= clima_max:
            roupas_adequadas.append(roupa)
            continue
        
        if abs(temperatura - clima_min) <= 8 or abs(temperatura - clima_max) <= 8:
            roupas_adequadas.append(roupa)
            continue
        
        if 'chuva' in condicao:
            if any(palavra in tipo for palavra in ['impermeável', 'bota', 'jaqueta']):
                roupas_adequadas.append(roupa)
    
    return roupas_adequadas

def categorizar_roupas(roupas: List[Dict]) -> Dict[str, List[Dict]]:
    """Categoriza roupas por tipo para montagem inteligente"""
    categorias = {
        'superior': [],
        'inferior': [],
        'calçado': [],
        'casaco': [],
        'acessorios': []
    }
    
    for roupa in roupas:
        tipo = roupa.get('tipo', '').lower()
        
        if tipo == 'superior':
            categorias['superior'].append(roupa)
        elif tipo == 'inferior':
            categorias['inferior'].append(roupa)
        elif tipo == 'calçado':
            categorias['calçado'].append(roupa)
        elif tipo == 'casaco':
            categorias['casaco'].append(roupa)
        elif any(palavra in tipo for palavra in ['camiseta', 'camisa', 'blusa', 'regata', 'top']):
            categorias['superior'].append(roupa)
        elif any(palavra in tipo for palavra in ['calça', 'short', 'bermuda', 'saia', 'vestido']):
            categorias['inferior'].append(roupa)
        elif any(palavra in tipo for palavra in ['sapato', 'tênis', 'sandália', 'chinelo', 'bota']):
            categorias['calçado'].append(roupa)
        elif any(palavra in tipo for palavra in ['jaqueta', 'moletom', 'blazer', 'cardigã']):
            categorias['casaco'].append(roupa)
        elif any(palavra in tipo for palavra in ['chapéu', 'boné', 'cinto', 'bolsa', 'óculos']):
            categorias['acessorios'].append(roupa)
        else:
            categorias['superior'].append(roupa)
    
    return categorias

def analisar_combinacao_detalhada(combinacao: List[Dict], clima_data: Dict) -> Dict:
    """Análise detalhada da combinação escolhida"""
    cores = [roupa.get('cor', 'indefinida') for roupa in combinacao]
    tipos = [roupa.get('tipo', 'indefinido') for roupa in combinacao]
    
    temp = clima_data.get('temperatura', 20)
    if temp <= 15:
        clima_desc = "frio - casaco obrigatório"
    elif temp <= 25:
        clima_desc = "ameno - casaco recomendado"
    else:
        clima_desc = "quente - sem necessidade de casaco"
    
    cores_unicas = list(set(cores))
    if len(cores_unicas) <= 2:
        harmonia_cor = "Excelente"
    elif len(cores_unicas) == 3:
        harmonia_cor = "Boa"
    else:
        harmonia_cor = "Arriscada"
    
    formal_count = sum(1 for tipo in tipos if any(formal in tipo.lower() for formal in ['blazer', 'social', 'terno']))
    casual_count = sum(1 for tipo in tipos if any(casual in tipo.lower() for casual in ['camiseta', 'jeans', 'tênis']))
    
    if formal_count > casual_count:
        estilo_dominante = "Formal"
    elif casual_count > 0:
        estilo_dominante = "Casual"
    else:
        estilo_dominante = "Neutro"
    
    return {
        'clima_adequacao': clima_desc,
        'harmonia_cores': harmonia_cor,
        'estilo_dominante': estilo_dominante,
        'cores_usadas': cores_unicas,
        'total_pecas': len(combinacao),
        'recomendacao': gerar_recomendacao_textual(combinacao, clima_data)
    }

def gerar_recomendacao_textual(combinacao: List[Dict], clima_data: Dict) -> str:
    """Gera uma recomendação em texto natural"""
    temp = clima_data.get('temperatura', 20)
    condicao = clima_data.get('condicao', '')
    
    recomendacoes = []
    
    if temp <= 15:
        recomendacoes.append("Perfeito para o clima frio de hoje! Use casaco.")
    elif temp <= 25:
        recomendacoes.append("Ideal para o clima ameno! Casaco incluído para conforto.")
    else:
        recomendacoes.append("Combinação fresca e ideal para se manter confortável no calor!")
    
    if 'chuva' in condicao.lower():
        recomendacoes.append("Lembre-se de levar um guarda-chuva!")
    
    # Análise de cores
    cores = [r.get('cor', '') for r in combinacao if r.get('cor')]
    if len(set(cores)) <= 2:
        recomendacoes.append("As cores harmonizam perfeitamente.")
    
    return " ".join(recomendacoes)

def gerar_descricao_combinacao(combinacao: List[Dict]) -> str:
    """Gera descrição curta da combinação"""
    if not combinacao:
        return "Combinação vazia"
    
    tipos = [roupa.get('tipo', 'peça') for roupa in combinacao]
    cores = [roupa.get('cor', '') for roupa in combinacao if roupa.get('cor')]
    
    descricao = f"{len(combinacao)} peças"
    if cores:
        cores_principais = list(set(cores))[:2]  # Máximo 2 cores na descrição
        descricao += f" em {', '.join(cores_principais)}"
    
    return descricao

def gerar_sugestao_basica_fallback(roupas: List[Dict], clima_data: Dict) -> Dict:
    """Fallback para quando a IA avançada falha - garante combinação completa"""
    if not roupas:
        return {
            'erro': 'Nenhuma roupa disponível',
            'sugestao': [],
            'score': 0,
            'detalhes': {}
        }
    
    categorias = categorizar_roupas(roupas)
    sugestao_simples = []
    temperatura = clima_data.get('temperatura', 20)
    
    if categorias['superior']:
        sugestao_simples.append(random.choice(categorias['superior']))
    
    if categorias['inferior']:
        sugestao_simples.append(random.choice(categorias['inferior']))
    
    if categorias['calçado']:
        sugestao_simples.append(random.choice(categorias['calçado']))
    
    if temperatura <= 18 and categorias['casaco']:
        sugestao_simples.append(random.choice(categorias['casaco']))
    
    if len(sugestao_simples) < 2:
        num_roupas = min(3, len(roupas))
        sugestao_simples = random.sample(roupas, num_roupas)
    
    return {
        'sugestao': sugestao_simples,
        'score': 50.0,
        'detalhes': {
            'clima_adequacao': 'básica',
            'harmonia_cores': 'indefinida',
            'estilo_dominante': 'Misto',
            'recomendacao': 'Combinação básica com peças essenciais.',
            'total_pecas': len(sugestao_simples)
        },
        'alternativas': [],
        'clima': clima_data,
        'timestamp': obter_timestamp()
    }

def obter_roupas_disponiveis() -> List[Dict[str, Any]]:
    """Busca todas as roupas disponíveis no banco de dados"""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT id, nome, tipo, cor, imagem_path, clima_min, clima_max
            FROM roupas 
            ORDER BY id
        """)
        
        roupas = []
        
        for linha in cursor.fetchall():
            roupa = {
                'id': linha[0],
                'nome': linha[1],
                'tipo': linha[2],
                'cor': linha[3],
                'imagem_path': linha[4],
                'clima_min': linha[5],
                'clima_max': linha[6]
            }
            roupas.append(roupa)
        
        return roupas
        
    except Exception as e:
        print(f"Erro ao buscar roupas: {e}")
        return []
    finally:
        conn.close()

def obter_timestamp() -> str:
    """Retorna timestamp atual"""
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def registrar_feedback_sugestao(sugestao_id: str, feedback_score: int, usado: bool = False):
    """Registra feedback de uma sugestão para aprendizado"""
    try:
        print(f"Feedback registrado: ID={sugestao_id}, Score={feedback_score}, Usado={usado}")
    except Exception as e:
        print(f"Erro ao registrar feedback: {e}")

def aprender_com_uso(roupas_usadas: List[Dict], clima_data: Dict, satisfacao: int):
    """Registra uma combinação usada para aprendizado futuro"""
    try:
        style_ai.registrar_uso_combinacao(roupas_usadas, clima_data, satisfacao)
        print(f"Aprendizado registrado: {len(roupas_usadas)} roupas, satisfação={satisfacao}")
    except Exception as e:
        print(f"Erro ao registrar aprendizado: {e}")

def gerar_combinacao_por_padrao(roupas: List[Dict], padrao: Dict[str, Any], clima_data: Dict) -> List[Dict]:
    """Gera uma combinação baseada em um padrão aprendido"""
    try:
        combinacao = []
        
        for categoria, pattern_info in padrao.items():
            roupas_categoria = [
                roupa for roupa in roupas
                if (roupa.get('tipo', '').lower() == pattern_info.get('tipo', '').lower() or
                    roupa.get('categoria', '').lower() == categoria.lower())
            ]
            
            if roupas_categoria:
                roupas_filtradas = roupas_categoria
                
                if pattern_info.get('cor'):
                    roupas_cor = [r for r in roupas_categoria if r.get('cor', '').lower() == pattern_info['cor'].lower()]
                    if roupas_cor:
                        roupas_filtradas = roupas_cor
                
                if pattern_info.get('estilo'):
                    roupas_estilo = [r for r in roupas_filtradas if r.get('estilo', '').lower() == pattern_info['estilo'].lower()]
                    if roupas_estilo:
                        roupas_filtradas = roupas_estilo
                
                if roupas_filtradas:
                    combinacao.append(random.choice(roupas_filtradas))
        
        return combinacao if len(combinacao) >= 2 else None
        
    except Exception as e:
        print(f"Erro ao gerar combinação por padrão: {e}")
        return None

def calcular_bonus_preferencias(combinacao: List[Dict], preferencias: Dict[str, Dict[str, float]]) -> float:
    """Calcula bonus baseado nas preferências do usuário"""
    try:
        bonus = 0.0
        
        for roupa in combinacao:
            if not roupa:
                continue
                
            cor = roupa.get('cor', '').lower()
            if cor and 'cor' in preferencias and cor in preferencias['cor']:
                bonus += preferencias['cor'][cor] * 0.3
            
            estilo = roupa.get('estilo', '').lower()
            if estilo and 'estilo' in preferencias and estilo in preferencias['estilo']:
                bonus += preferencias['estilo'][estilo] * 0.2
            
            tipo = roupa.get('tipo', '').lower()
            if tipo and 'tipo_roupa' in preferencias and tipo in preferencias['tipo_roupa']:
                bonus += preferencias['tipo_roupa'][tipo] * 0.2
        
        return min(bonus, 2.0)
        
    except Exception as e:
        print(f"Erro ao calcular bonus de preferências: {e}")
        return 0.0

def aplicar_preferencias_selecao(roupas: List[Dict], preferencias: Dict[str, Dict[str, float]]) -> List[Dict]:
    """Aplica preferências do usuário na seleção de roupas, favorecendo itens preferidos"""
    try:
        if not preferencias:
            return roupas
        
        roupas_com_score = []
        
        for roupa in roupas:
            score_preferencia = 0.0
            
            cor = roupa.get('cor', '').lower()
            if cor and 'cor' in preferencias and cor in preferencias['cor']:
                score_preferencia += preferencias['cor'][cor]
            
            estilo = roupa.get('estilo', '').lower()
            if estilo and 'estilo' in preferencias and estilo in preferencias['estilo']:
                score_preferencia += preferencias['estilo'][estilo]
            
            tipo = roupa.get('tipo', '').lower()
            if tipo and 'tipo_roupa' in preferencias and tipo in preferencias['tipo_roupa']:
                score_preferencia += preferencias['tipo_roupa'][tipo]
            
            roupas_com_score.append((roupa, score_preferencia))
        
        roupas_com_score.sort(key=lambda x: x[1], reverse=True)
        
        limite = max(1, int(len(roupas_com_score) * 0.7))
        return [roupa for roupa, score in roupas_com_score[:limite]]
        
    except Exception as e:
        print(f"Erro ao aplicar preferências: {e}")
        return roupas

def gerar_sugestao_roupa(clima_data: Dict[str, Any]) -> Dict[str, Any]:
    """Função de compatibilidade - redireciona para versão inteligente"""
    resultado = gerar_sugestao_inteligente(clima_data)
    
    if 'sugestao' in resultado and resultado['sugestao']:
        return {
            'sugestao': resultado['sugestao'],
            'explicacao': resultado.get('detalhes', {}).get('recomendacao', 'Sugestão da IA'),
            'clima': resultado.get('clima', clima_data),
            'score': resultado.get('score', 0),
            'total_roupas_analisadas': len(obter_roupas_disponiveis()),
            'detalhes': resultado.get('detalhes', {})
        }
    else:
        return resultado
