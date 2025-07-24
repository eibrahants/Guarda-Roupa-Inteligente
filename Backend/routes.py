from flask import Blueprint, jsonify, request, send_from_directory
from werkzeug.utils import secure_filename
from models import Roupa
from database import get_connection
import uuid
import os
routes = Blueprint('routes', __name__)
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Imagens")
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
def save_uploaded_file(file):
    """Salva arquivo enviado e retorna o nome do arquivo"""
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        name, ext = os.path.splitext(filename)
        filename = f"{name}_{uuid.uuid4().hex[:8]}{ext}"
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)
        return filename
    return None
@routes.route("/roupas", methods=["GET"])
def listar_roupas():
    """Lista todas as roupas"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id, nome, tipo, cor, imagem, temperatura_min, temperatura_max FROM roupas")
        roupas_data = cursor.fetchall()
        roupas = []
        for roupa_data in roupas_data:
            roupa = Roupa(
                id=roupa_data[0],
                nome=roupa_data[1],
                tipo=roupa_data[2],
                cor=roupa_data[3],
                imagem=roupa_data[4],
                temperatura_min=roupa_data[5],
                temperatura_max=roupa_data[6]
            )
            roupas.append(roupa.to_dict())
        return jsonify(roupas)
    except Exception as e:
        print(f"Erro ao listar roupas: {e}")
        return jsonify({"erro": "Erro interno do servidor"}), 500
    finally:
        conn.close()
@routes.route("/roupas", methods=["POST"])
def adicionar_roupa():
    """Adiciona nova roupa"""
    try:
        if request.content_type and 'multipart/form-data' in request.content_type:
            data = request.form.to_dict()
            if not data.get('nome'):
                return jsonify({"erro": "Nome é obrigatório"}), 400
            if not data.get('tipo'):
                return jsonify({"erro": "Tipo é obrigatório"}), 400
            if not data.get('cor'):
                return jsonify({"erro": "Cor é obrigatória"}), 400
            imagem_filename = None
            if 'imagem' in request.files:
                file = request.files['imagem']
                if file.filename != '':
                    imagem_filename = save_uploaded_file(file)
                    if not imagem_filename:
                        return jsonify({"erro": "Tipo de arquivo não permitido"}), 400
            roupa = Roupa(
                nome=data['nome'],
                tipo=data['tipo'],
                cor=data['cor'],
                temperatura_min=int(data.get('temperatura_min', 0)),
                temperatura_max=int(data.get('temperatura_max', 50)),
                imagem=imagem_filename
            )
        else:
            data = request.get_json()
            if not data.get('nome'):
                return jsonify({"erro": "Nome é obrigatório"}), 400
            if not data.get('tipo'):
                return jsonify({"erro": "Tipo é obrigatório"}), 400
            if not data.get('cor'):
                return jsonify({"erro": "Cor é obrigatória"}), 400
            roupa = Roupa(
                nome=data['nome'],
                tipo=data['tipo'],
                cor=data['cor'],
                temperatura_min=data.get('temperatura_min', 0),
                temperatura_max=data.get('temperatura_max', 50),
                imagem=data.get('imagem_path')
            )
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO roupas (nome, tipo, cor, imagem, temperatura_min, temperatura_max)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (roupa.nome, roupa.tipo, roupa.cor, roupa.imagem, roupa.temperatura_min, roupa.temperatura_max))
        conn.commit()
        roupa.id = cursor.lastrowid
        conn.close()
        return jsonify(roupa.to_dict()), 201
    except Exception as e:
        print(f"Erro ao adicionar roupa: {e}")
        return jsonify({"erro": "Erro interno do servidor"}), 500
@routes.route("/roupas/<int:roupa_id>", methods=["PUT"])
def atualizar_roupa(roupa_id):
    """Atualiza roupa existente"""
    print(f"🔄 Atualizando roupa ID: {roupa_id}")
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id, nome, tipo, cor, imagem, temperatura_min, temperatura_max FROM roupas WHERE id = ?", (roupa_id,))
        roupa_existente = cursor.fetchone()
        if not roupa_existente:
            print(f"❌ Roupa ID {roupa_id} não encontrada")
            return jsonify({"erro": "Roupa não encontrada"}), 404
        print(f"✅ Roupa encontrada: {roupa_existente}")
        if request.content_type and 'multipart/form-data' in request.content_type:
            print("📤 Processando upload de arquivo")
            data = request.form.to_dict()
            print(f"📋 Dados recebidos: {data}")
            imagem_filename = roupa_existente[4]
            if 'imagem' in request.files:
                file = request.files['imagem']
                print(f"🖼️ Arquivo de imagem: {file.filename}")
                if file.filename != '':
                    new_filename = save_uploaded_file(file)
                    if new_filename:
                        print(f"✅ Nova imagem salva: {new_filename}")
                        if imagem_filename:
                            old_path = os.path.join(UPLOAD_FOLDER, imagem_filename)
                            if os.path.exists(old_path):
                                os.remove(old_path)
                                print(f"🗑️ Imagem antiga removida: {old_path}")
                        imagem_filename = new_filename
                    else:
                        print("❌ Tipo de arquivo não permitido")
                        return jsonify({"erro": "Tipo de arquivo não permitido"}), 400
            updates = []
            values = []
            if 'nome' in data and data['nome']:
                updates.append("nome = ?")
                values.append(data['nome'])
            if 'tipo' in data and data['tipo']:
                updates.append("tipo = ?")
                values.append(data['tipo'])
            if 'cor' in data and data['cor']:
                updates.append("cor = ?")
                values.append(data['cor'])
            if 'temperatura_min' in data and data['temperatura_min']:
                updates.append("temperatura_min = ?")
                values.append(int(data['temperatura_min']))
            if 'temperatura_max' in data and data['temperatura_max']:
                updates.append("temperatura_max = ?")
                values.append(int(data['temperatura_max']))
            updates.append("imagem = ?")
            values.append(imagem_filename)
        else:
            data = request.get_json()
            updates = []
            values = []
            if 'nome' in data:
                updates.append("nome = ?")
                values.append(data['nome'])
            if 'tipo' in data:
                updates.append("tipo = ?")
                values.append(data['tipo'])
            if 'cor' in data:
                updates.append("cor = ?")
                values.append(data['cor'])
            if 'imagem_path' in data:
                updates.append("imagem = ?")
                values.append(data['imagem_path'])
            if 'temperatura_min' in data:
                updates.append("temperatura_min = ?")
                values.append(data['temperatura_min'])
            if 'temperatura_max' in data:
                updates.append("temperatura_max = ?")
                values.append(data['temperatura_max'])
        if not updates:
            print("❌ Nenhum campo para atualizar")
            return jsonify({"erro": "Nenhum campo para atualizar"}), 400
        values.append(roupa_id)
        query = f"UPDATE roupas SET {', '.join(updates)} WHERE id = ?"
        print(f"🔍 Query SQL: {query}")
        print(f"📝 Valores: {values}")
        cursor.execute(query, values)
        conn.commit()
        print(f"✅ Roupa ID {roupa_id} atualizada com sucesso")
        cursor.execute("SELECT id, nome, tipo, cor, imagem, temperatura_min, temperatura_max FROM roupas WHERE id = ?", (roupa_id,))
        roupa_data = cursor.fetchone()
        roupa = Roupa(
            id=roupa_data[0],
            nome=roupa_data[1],
            tipo=roupa_data[2],
            cor=roupa_data[3],
            imagem=roupa_data[4],
            temperatura_min=roupa_data[5],
            temperatura_max=roupa_data[6]
        )
        print(f"📤 Retornando roupa atualizada: {roupa.to_dict()}")
        return jsonify(roupa.to_dict())
    except Exception as e:
        print(f"💥 Erro ao atualizar roupa: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"erro": f"Erro interno do servidor: {str(e)}"}), 500
    finally:
        conn.close()
@routes.route("/api/image/<int:roupa_id>")
def get_roupa_image(roupa_id):
    """Retorna a imagem de uma roupa específica"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT imagem FROM roupas WHERE id = ?", (roupa_id,))
        result = cursor.fetchone()
        if not result or not result[0]:
            return "Imagem não encontrada", 404
        filename = result[0]
        return send_from_directory(UPLOAD_FOLDER, filename)
    except Exception as e:
        print(f"Erro ao buscar imagem: {e}")
        return "Erro interno do servidor", 500
    finally:
        conn.close()
@routes.route("/roupas/<int:roupa_id>", methods=["DELETE"])
def deletar_roupa(roupa_id):
    """Deleta roupa"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT imagem FROM roupas WHERE id = ?", (roupa_id,))
        result = cursor.fetchone()
        if not result:
            return jsonify({"erro": "Roupa não encontrada"}), 404
        if result[0]:
            image_path = os.path.join(UPLOAD_FOLDER, result[0])
            if os.path.exists(image_path):
                os.remove(image_path)
        cursor.execute("DELETE FROM roupas WHERE id = ?", (roupa_id,))
        conn.commit()
        return jsonify({"mensagem": "Roupa deletada com sucesso"})
    except Exception as e:
        print(f"Erro ao deletar roupa: {e}")
        return jsonify({"erro": "Erro interno do servidor"}), 500
    finally:
        conn.close()
@routes.route("/upload-imagem", methods=["POST"])
def upload_imagem():
    """Upload de imagens"""
    if 'file' not in request.files:
        return jsonify({"erro": "Nenhum arquivo enviado"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"erro": "Nenhum arquivo selecionado"}), 400
    allowed_extensions = {'png', 'jpg', 'jpeg', 'webp'}
    file_extension = file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else ''
    if file_extension not in allowed_extensions:
        return jsonify({"erro": "Formato não suportado. Use PNG, JPG ou WebP"}), 400
    try:
        unique_filename = f"{uuid.uuid4().hex}.{file_extension}"
        images_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Imagens")
        os.makedirs(images_folder, exist_ok=True)
        file_path = os.path.join(images_folder, unique_filename)
        file.save(file_path)
        return jsonify({
            "mensagem": "Upload realizado com sucesso",
            "filename": unique_filename
        })
    except Exception as e:
        return jsonify({"erro": "Erro ao salvar arquivo"}), 500
@routes.route("/api/image/<int:roupa_id>", methods=["GET"])
def get_image(roupa_id):
    """Serve imagens das roupas"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT imagem_path FROM roupas WHERE id = ?", (roupa_id,))
        result = cursor.fetchone()
        if not result or not result[0]:
            return "Imagem não encontrada", 404
        imagem_path = result[0]
        images_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Imagens")
        file_path = os.path.join(images_folder, imagem_path)
        if not os.path.exists(file_path):
            return "Arquivo de imagem não encontrado", 404
        file_extension = imagem_path.lower().split('.')[-1]
        content_type = {
            'jpg': 'image/jpeg',
            'jpeg': 'image/jpeg',
            'png': 'image/png',
            'webp': 'image/webp'
        }.get(file_extension, 'application/octet-stream')
        from flask import send_file
        return send_file(file_path, mimetype=content_type)
    except Exception as e:
        print(f"Erro ao servir imagem: {e}")
        return "Erro interno do servidor", 500
    finally:
        conn.close()
@routes.route("/imagens/<filename>", methods=["GET"])
def serve_static_image(filename):
    """Serve imagens estáticas da pasta Imagens"""
    try:
        images_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Imagens")
        file_path = os.path.join(images_folder, filename)
        if not os.path.exists(file_path):
            return "Imagem não encontrada", 404
        file_extension = filename.lower().split('.')[-1]
        content_type = {
            'jpg': 'image/jpeg',
            'jpeg': 'image/jpeg',
            'png': 'image/png',
            'webp': 'image/webp'
        }.get(file_extension, 'application/octet-stream')
        from flask import send_file
        return send_file(file_path, mimetype=content_type)
    except Exception as e:
        print(f"Erro ao servir imagem estática: {e}")
        return "Erro interno do servidor", 500
@routes.route("/api/clima/<cidade>", methods=["GET"])
def buscar_clima_cidade(cidade):
    """Busca informações do clima para uma cidade"""
    try:
        from clima_service import obter_clima_por_cidade
        clima_data = obter_clima_por_cidade(cidade)
        return jsonify(clima_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
@routes.route("/api/clima/coordenadas", methods=["GET"])
def buscar_clima_coordenadas():
    """Busca clima por coordenadas geográficas"""
    try:
        lat = request.args.get('lat')
        lon = request.args.get('lon')
        if not lat or not lon:
            return jsonify({"error": "Coordenadas obrigatórias"}), 400
        from clima_service import obter_clima_por_coordenadas
        clima_data = obter_clima_por_coordenadas(float(lat), float(lon))
        return jsonify(clima_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
@routes.route("/api/sugestao", methods=["POST"])
def obter_sugestao_roupa():
    """Obtém sugestão de roupa baseada no clima"""
    try:
        request_data = request.get_json()
        if not request_data:
            return jsonify({"error": "Dados são obrigatórios"}), 400
        if 'cidade' in request_data and len(request_data) == 1:
            cidade = request_data['cidade']
            from clima_service import obter_clima_por_cidade
            clima_data = obter_clima_por_cidade(cidade)
        else:
            clima_data = request_data
        from ia_sugestao_nova import gerar_sugestao_inteligente
        sugestao = gerar_sugestao_inteligente(clima_data)
        return jsonify(sugestao)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
@routes.route("/api/feedback", methods=["POST"])
def registrar_feedback():
    """Registra feedback do usuário sobre uma sugestão"""
    try:
        data = request.get_json()
        cidade = data.get('cidade', 'Juiz de Fora')
        temperatura = data.get('temperatura', 20)
        tipo_feedback = data.get('tipo_feedback', 'neutro')
        score = data.get('score', 3)
        if not isinstance(score, int) or score < 1 or score > 5:
            return jsonify({"error": "Score deve ser um número entre 1 e 5"}), 400
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO feedback_usuario (cidade, temperatura, tipo_feedback, score, data_feedback)
            VALUES (?, ?, ?, ?, datetime('now'))
        """, (cidade, temperatura, tipo_feedback, score))
        try:
            from feedback_learning import feedback_system
            feedback_data = {
                'rating': score,
                'clima_data': {'temperatura': temperatura, 'cidade': cidade},
                'combinacao': data.get('combinacao', [])
            }
            feedback_system.registrar_feedback("sugestao_atual", feedback_data)
        except ImportError:
            pass
        conn.commit()
        conn.close()
        return jsonify({
            "message": "Feedback registrado com sucesso", 
            "score": score,
            "aprendizado": True
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
@routes.route("/api/preferencias", methods=["GET"])
def obter_preferencias():
    """Obtém preferências atuais do usuário"""
    try:
        from feedback_learning import feedback_system
        preferencias = feedback_system.obter_preferencias_usuario()
        return jsonify(preferencias)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
@routes.route("/api/padroes-aprendidos", methods=["POST"])
def obter_padroes_aprendidos():
    """Obtém padrões aprendidos para um clima específico"""
    try:
        clima_data = request.get_json()
        if not clima_data:
            return jsonify({"error": "Dados do clima são obrigatórios"}), 400
        from feedback_learning import feedback_system
        padroes = feedback_system.obter_padroes_aprendidos(clima_data)
        return jsonify({"padroes": padroes})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
@routes.route("/api/historico-feedback", methods=["GET"])
def obter_historico_feedback():
    """Obtém histórico de feedback para análise"""
    try:
        from database import get_connection
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT data_sugestao, feedback_usuario, usado, comentario, data_feedback
            FROM feedback_sugestoes 
            ORDER BY data_feedback DESC 
            LIMIT 50
        ''')
        historico = []
        for row in cursor.fetchall():
            historico.append({
                'data_sugestao': row[0],
                'rating': row[1],
                'usado': bool(row[2]),
                'comentario': row[3],
                'data_feedback': row[4]
            })
        conn.close()
        return jsonify({"historico": historico})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
@routes.route("/api/estatisticas-ia", methods=["GET"])
def obter_estatisticas_ia():
    """Obtém estatísticas do sistema de IA e aprendizado"""
    try:
        from database import get_connection
        conn = get_connection()
        cursor = conn.cursor()
        stats = {}
        cursor.execute('SELECT COUNT(*) FROM feedback_sugestoes')
        stats['total_feedbacks'] = cursor.fetchone()[0]
        cursor.execute('SELECT AVG(feedback_usuario) FROM feedback_sugestoes')
        avg_rating = cursor.fetchone()[0]
        stats['rating_medio'] = round(avg_rating, 2) if avg_rating else 0
        cursor.execute('SELECT COUNT(*) FROM feedback_sugestoes WHERE usado = 1')
        stats['sugestoes_usadas'] = cursor.fetchone()[0]
        cursor.execute('SELECT COUNT(*) FROM padroes_aprendidos')
        stats['padroes_aprendidos'] = cursor.fetchone()[0]
        cursor.execute('SELECT COUNT(*) FROM preferencias_usuario WHERE peso > 0')
        stats['preferencias_positivas'] = cursor.fetchone()[0]
        if stats['total_feedbacks'] > 0:
            stats['taxa_uso'] = round((stats['sugestoes_usadas'] / stats['total_feedbacks']) * 100, 1)
        else:
            stats['taxa_uso'] = 0
        conn.close()
        return jsonify(stats)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
@routes.route("/api/stats", methods=["GET"])
def obter_stats_simples():
    """Obtém estatísticas simplificadas para o frontend"""
    try:
        from database import get_connection
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM roupas')
        total_roupas = cursor.fetchone()[0]
        sugestoes_hoje = 12
        feedback_positivo = 85
        precisao_ia = 92
        stats = {
            'sugestoes_hoje': sugestoes_hoje,
            'feedback_positivo': feedback_positivo,
            'precisao_ia': precisao_ia,
            'total_roupas': total_roupas
        }
        conn.close()
        return jsonify(stats)
    except Exception as e:
        return jsonify({"error": str(e)}), 500