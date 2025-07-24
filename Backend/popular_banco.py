#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import sqlite3
import os

def popular_banco_de_dados():
    """Popula o banco de dados com as roupas do CSV"""
    print("🔧 Populando banco de dados com roupas...")
    
    # Caminhos dos arquivos
    csv_path = r'C:\Users\pedro\OneDrive\Desktop\Projeto_Roupa\Database\csv certo.csv'
    db_path = r'C:\Users\pedro\OneDrive\Desktop\Projeto_Roupa\Database\roupas.db'
    
    try:
        # Ler o CSV (separado por ponto e vírgula)
        print("📄 Lendo CSV...")
        df = pd.read_csv(csv_path, sep=';')
        print(f"✅ CSV lido com {len(df)} roupas")
        print(f"📋 Colunas: {list(df.columns)}")
        
        # Conectar ao banco
        print("🔗 Conectando ao banco...")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Verificar se a tabela existe
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='roupas'")
        tabela_existe = cursor.fetchone()
        
        if not tabela_existe:
            print("📝 Criando tabela de roupas...")
            cursor.execute('''
                CREATE TABLE roupas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    tipo TEXT NOT NULL,
                    cor TEXT NOT NULL,
                    imagem_path TEXT,
                    clima_min REAL DEFAULT 10.0,
                    clima_max REAL DEFAULT 30.0
                )
            ''')
        
        # Limpar dados existentes
        cursor.execute("DELETE FROM roupas")
        print("🧹 Dados antigos removidos")
        
        # Inserir dados do CSV
        print("📥 Inserindo roupas...")
        roupas_inseridas = 0
        
        for index, row in df.iterrows():
            cursor.execute('''
                INSERT INTO roupas (nome, tipo, cor, imagem_path, clima_min, clima_max)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                row['nome'],
                row['tipo'],
                row['cor'], 
                row['imagem_path'],
                float(row.get('clima_min', 10.0)),
                float(row.get('clima_max', 30.0))
            ))
            roupas_inseridas += 1
        
        # Salvar mudanças
        conn.commit()
        print(f"✅ {roupas_inseridas} roupas inseridas com sucesso!")
        
        # Verificar inserção
        cursor.execute("SELECT COUNT(*) FROM roupas")
        total = cursor.fetchone()[0]
        print(f"📊 Total de roupas no banco: {total}")
        
        # Mostrar algumas roupas de exemplo
        print("\n🔍 Primeiras 5 roupas inseridas:")
        cursor.execute("SELECT id, nome, tipo, cor FROM roupas LIMIT 5")
        for row in cursor.fetchall():
            print(f"  ID: {row[0]}, Nome: {row[1]}, Tipo: {row[2]}, Cor: {row[3]}")
        
        conn.close()
        print("\n🎉 Banco de dados populado com sucesso!")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao popular banco: {e}")
        return False

if __name__ == "__main__":
    popular_banco_de_dados()
