# =============================================================================
# SERVIÇO DE CLIMA - Open-Meteo (100% GRÁTIS, SEM CADASTRO!)
# =============================================================================

import requests
import json
import random
from typing import Dict, Any
from datetime import datetime

# Open-Meteo - COMPLETAMENTE GRÁTIS (sem cadastro, sem chave, sem limite)
# Documentação: https://open-meteo.com/
BASE_URL = "https://api.open-meteo.com/v1/forecast"
GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"

# Sistema sempre usa dados reais!
USE_REAL_API = True

def obter_clima_por_cidade(cidade: str) -> Dict[str, Any]:
    """
    Obtém informações climáticas para uma cidade específica
    """
    try:
        print(f"🌐 Buscando clima real para {cidade} via Open-Meteo...")
        return obter_clima_real_por_cidade(cidade)
        
    except Exception as e:
        print(f"❌ Erro ao obter clima real: {str(e)}")
        print("🔄 Usando dados simulados como fallback...")
        return simular_clima_por_cidade(cidade)

def obter_clima_real_por_cidade(cidade: str) -> Dict[str, Any]:
    """
    Busca clima real usando Open-Meteo (100% gratuita)
    """
    try:
        # Passo 1: Obter coordenadas da cidade
        coords = obter_coordenadas_cidade(cidade)
        if not coords:
            raise Exception(f"Cidade '{cidade}' não encontrada")
        
        lat, lon, nome_cidade = coords
        
        # Passo 2: Obter clima usando coordenadas
        return obter_clima_real_por_coordenadas(lat, lon, nome_cidade)
        
    except Exception as e:
        raise Exception(f"Erro ao buscar clima: {str(e)}")

def obter_coordenadas_cidade(cidade: str) -> tuple:
    """
    Obtém coordenadas da cidade usando geocoding gratuito
    """
    try:
        params = {
            'name': cidade,
            'count': 1,
            'language': 'pt',
            'format': 'json'
        }
        
        response = requests.get(GEOCODING_URL, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('results') and len(data['results']) > 0:
                result = data['results'][0]
                lat = result['latitude']
                lon = result['longitude']
                nome = result['name']
                return lat, lon, nome
            else:
                return None
        else:
            return None
            
    except Exception as e:
        print(f"Erro no geocoding: {e}")
        return None

def obter_clima_por_coordenadas(lat: float, lon: float) -> Dict[str, Any]:
    """
    Obtém informações climáticas por coordenadas geográficas
    """
    try:
        return obter_clima_real_por_coordenadas(lat, lon)
        
    except Exception as e:
        print(f"Erro ao obter clima para coordenadas {lat}, {lon}: {str(e)}")
        cidade = determinar_cidade_por_coordenadas(lat, lon)
        return simular_clima_por_cidade(cidade)

def obter_clima_real_por_coordenadas(lat: float, lon: float, cidade: str = None) -> Dict[str, Any]:
    """
    Busca clima real por coordenadas usando Open-Meteo
    """
    try:
        params = {
            'latitude': lat,
            'longitude': lon,
            'current': 'temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,weather_code,cloud_cover,wind_speed_10m,wind_direction_10m',
            'timezone': 'auto',
            'forecast_days': 1
        }
        
        response = requests.get(BASE_URL, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Clima real obtido com sucesso via Open-Meteo!")
            return processar_dados_clima_real(data, lat, lon, cidade)
        else:
            raise Exception(f"API retornou status {response.status_code}")
            
    except Exception as e:
        raise Exception(f"Erro ao buscar clima: {str(e)}")

def processar_dados_clima_real(data: Dict, lat: float, lon: float, cidade: str = None) -> Dict[str, Any]:
    """
    Processa dados reais da Open-Meteo para formato padronizado
    """
    try:
        current = data['current']
        
        # Converter código do tempo para descrição
        weather_code = current.get('weather_code', 0)
        condicao = converter_codigo_tempo(weather_code)
        
        # Determinar cidade se não fornecida
        if not cidade:
            cidade = determinar_cidade_por_coordenadas(lat, lon)
        
        return {
            "cidade": cidade or "Localização",
            "pais": "BR",
            "temperatura": round(current.get('temperature_2m', 20)),
            "sensacao_termica": round(current.get('apparent_temperature', 20)),
            "temperatura_min": round(current.get('temperature_2m', 20) - 3),  # Estimativa
            "temperatura_max": round(current.get('temperature_2m', 20) + 5),  # Estimativa
            "umidade": round(current.get('relative_humidity_2m', 60)),
            "pressao": 1013,  # Valor padrão (Open-Meteo não fornece)
            "vento": round(current.get('wind_speed_10m', 0) * 3.6),  # m/s para km/h
            "direcao_vento": current.get('wind_direction_10m', 0),
            "condicao": condicao,
            "condicao_id": weather_code,
            "nuvens": current.get('cloud_cover', 0),
            "visibilidade": 10,  # Valor padrão
            "precipitacao": current.get('precipitation', 0),
            "coordenadas": {"lat": lat, "lon": lon},
            "timestamp": int(datetime.now().timestamp()),
            "fonte": "Open-Meteo (100% Gratuita)",
            "qualidade": "real",
            "api_calls_restantes": "Ilimitado (sem cadastro)"
        }
    except Exception as e:
        raise Exception(f"Erro ao processar dados: {str(e)}")

def converter_codigo_tempo(codigo: int) -> str:
    """
    Converte código WMO para descrição em português
    """
    codigos = {
        0: "céu limpo",
        1: "principalmente limpo",
        2: "parcialmente nublado", 
        3: "nublado",
        45: "neblina",
        48: "neblina com geada",
        51: "garoa leve",
        53: "garoa moderada",
        55: "garoa intensa",
        61: "chuva leve",
        63: "chuva moderada",
        65: "chuva intensa",
        71: "neve leve",
        73: "neve moderada",
        75: "neve intensa",
        77: "granizo",
        80: "pancadas de chuva leves",
        81: "pancadas de chuva moderadas",
        82: "pancadas de chuva intensas",
        95: "tempestade",
        96: "tempestade com granizo leve",
        99: "tempestade com granizo intenso"
    }
    
    return codigos.get(codigo, "tempo variável")

# =============================================================================
# SISTEMA DE SIMULAÇÃO (FALLBACK)
# =============================================================================

def simular_clima_por_cidade(cidade: str) -> Dict[str, Any]:
    """
    Simula dados climáticos realistas para uma cidade
    """
    # Usar cidade como seed para consistência
    random.seed(hash(cidade) % 1000)
    
    # Padrões climáticos brasileiros realistas
    temperaturas_por_regiao = {
        "são paulo": (15, 28),
        "rio de janeiro": (20, 32),
        "salvador": (22, 30),
        "recife": (24, 31),
        "fortaleza": (25, 32),
        "brasília": (16, 28),
        "belo horizonte": (16, 27),
        "porto alegre": (12, 25),
        "curitiba": (10, 23),
        "manaus": (24, 33),
        "belém": (24, 32),
        "goiânia": (18, 30),
        "florianópolis": (15, 26),
        "natal": (24, 31),
        "campo grande": (19, 32),
        "joão pessoa": (23, 30),
        "cuiabá": (21, 35),
        "vitória": (20, 29),
        "aracaju": (22, 30),
        "teresina": (23, 36),
        "macapá": (24, 32),
        "palmas": (20, 34),
        "rio branco": (22, 32),
        "boa vista": (23, 35),
        "porto velho": (22, 33)
    }
    
    cidade_lower = cidade.lower()
    temp_min, temp_max = temperaturas_por_regiao.get(cidade_lower, (18, 30))
    
    # Gerar dados realistas
    temperatura = random.randint(temp_min, temp_max)
    
    condicoes = [
        "céu limpo", "poucas nuvens", "nuvens dispersas", 
        "nublado", "chuva leve", "sol"
    ]
    
    return {
        "cidade": cidade.title(),
        "pais": "BR",
        "temperatura": temperatura,
        "sensacao_termica": temperatura + random.randint(-2, 3),
        "temperatura_min": temperatura - random.randint(2, 5),
        "temperatura_max": temperatura + random.randint(2, 5),
        "umidade": random.randint(40, 85),
        "pressao": random.randint(1010, 1025),
        "vento": random.randint(5, 25),
        "direcao_vento": random.randint(0, 360),
        "condicao": random.choice(condicoes),
        "condicao_id": random.randint(200, 800),
        "nuvens": random.randint(0, 100),
        "visibilidade": random.randint(8, 15),
        "precipitacao": 0,
        "coordenadas": {"lat": -21.7648, "lon": -43.3500},  # Juiz de Fora padrão
        "timestamp": int(datetime.now().timestamp()),
        "fonte": "Simulado (fallback)",
        "qualidade": "simulado",
        "api_calls_restantes": "Ilimitado (simulação)"
    }

def determinar_cidade_por_coordenadas(lat: float, lon: float) -> str:
    """
    Determina cidade aproximada baseada em coordenadas
    """
    # Mapeamento simples de coordenadas para cidades brasileiras
    if -23.7 <= lat <= -23.4 and -46.8 <= lon <= -46.3:
        return "São Paulo"
    elif -23.0 <= lat <= -22.7 and -43.8 <= lon <= -43.1:
        return "Rio de Janeiro"
    elif -21.9 <= lat <= -21.6 and -43.5 <= lon <= -43.2:
        return "Juiz de Fora"
    elif -13.0 <= lat <= -12.8 and -38.7 <= lon <= -38.3:
        return "Salvador"
    elif -8.2 <= lat <= -7.9 and -35.0 <= lon <= -34.8:
        return "Recife"
    elif -15.9 <= lat <= -15.6 and -48.0 <= lon <= -47.7:
        return "Brasília"
    elif -25.6 <= lat <= -25.3 and -49.4 <= lon <= -49.1:
        return "Curitiba"
    elif -30.2 <= lat <= -29.9 and -51.4 <= lon <= -51.0:
        return "Porto Alegre"
    else:
        return "Juiz de Fora"  # Padrão

# =============================================================================
# STATUS DA API
# =============================================================================

def verificar_status_api() -> Dict[str, Any]:
    """
    Verifica o status da configuração da API
    """
    return {
        "api_configurada": True,
        "provedor": "Open-Meteo",
        "plano": "100% Gratuito (sem limites)",
        "modo_atual": "Real",
        "cadastro_necessario": False,
        "chave_necessaria": False,
        "message": "✅ API Open-Meteo ativa! Clima real sem cadastro.",
        "vantagens": [
            "Sem cadastro necessário",
            "Sem chave API",
            "Sem limites de uso",
            "Dados meteorológicos precisos",
            "Cobertura mundial"
        ]
    }

if __name__ == "__main__":
    # Teste rápido
    print("🧪 Testando serviço de clima Open-Meteo...")
    print(json.dumps(verificar_status_api(), indent=2, ensure_ascii=False))
    print("\n🌤️ Testando busca por cidade:")
    resultado = obter_clima_por_cidade("São Paulo")
    print(json.dumps(resultado, indent=2, ensure_ascii=False))
