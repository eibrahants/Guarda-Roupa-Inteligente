#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script para corrigir os caminhos das imagens no banco de dados
"""

import pandas as pd
import sqlite3
import os
from database import get_connection

def corrigir_caminhos_imagens():
    """Corrige os caminhos das imagens no banco de dados"""
    try:
        print("🔧 Corrigindo caminhos de imagens...")
        
        # Conectar ao banco
        conn = get_connection()
        cursor = conn.cursor()
        
        # Buscar todas as roupas
        cursor.execute("SELECT id, nome, imagem_path FROM roupas")
        roupas = cursor.fetchall()
        
        # Mapear nomes para imagens corretas
        nome_para_imagem = {
            'Moletom Branco': 'moletom_branco.jpg',
            'Moletom st cruz': 'moletom_branco.jpg',  # fallback
            'Moletom nike': 'moletom_branco.jpg',     # fallback 
            'Moletom wcm': 'moletom_branco.jpg',      # fallback
            'Moletom class': 'moletom_class.jpg',
            'Moletom lepre': 'moletom_lepre.jpg',
            'Camisa cahartt': 'camisa_cahartt.jpg',
            'Camisa carnan preta': 'camisa_marrom.jpg',  # fallback
            'Camisa marrom': 'camisa_marrom.jpg',
            'Camisa pace': 'camisa_marrom.jpg',          # fallback
            'Camisa high branca': 'camisa_high.jpg',
            'Camisa high preta': 'camisa_high.jpg',
            'Camisa piet c rosa': 'camisa_pietr.jpg',
            'Camisa piet c verde': 'camisa_pietv.jpg',
            'Camisa branca midas': 'camisa_midas.jpg',
            'Camisa preta barra': 'camisa_marrom.jpg',   # fallback
            'Camisa branca stussy': 'camisa_marrom.jpg', # fallback
            'camisa leordre': 'camisa_leordre.jpg',
            'Camisa preta stussy': 'camisa_marrom.jpg',  # fallback
            'Camisa botão': 'camisa_marrom.jpg',         # fallback
            'Short branco': 'short_branco.jpg',
            'short sopro': 'short_sopro.jpg',
            'short barra': 'short_barra.jpg',
            'jorts': 'jort.jpg',
            'Calça Jeans clara': 'calça_jeans_clara.jpg',
            'Calça Jeans preta': 'calça_jeans_preta.jpg',
            'Calça jeans cinza': 'calça_jeans_cinza.jpg',
            'Calça moletom cinza': 'calça_moletom_cinza.jpg',
            'Nb 550': 'Nb_550.jpg',
            'Nike blazer': 'blazer.jpg',
            'Superstar bape': 'superxbape.jpg',
            'Chinelo rider': 'rider.jpg',
            'Havaianas branco': 'havaianas.jpg',
            'Vans Preto': 'vans.jpg'
        }
        
        # Atualizar cada roupa
        atualizadas = 0
        for id_roupa, nome, caminho_atual in roupas:
            if nome in nome_para_imagem:
                novo_caminho = nome_para_imagem[nome]
                cursor.execute(
                    "UPDATE roupas SET imagem_path = ? WHERE id = ?",
                    (novo_caminho, id_roupa)
                )
                atualizadas += 1
                print(f"  ✅ {nome}: {novo_caminho}")
        
        conn.commit()
        conn.close()
        
        print(f"🎉 {atualizadas} imagens corrigidas!")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao corrigir imagens: {e}")
        return False

if __name__ == "__main__":
    corrigir_caminhos_imagens()
