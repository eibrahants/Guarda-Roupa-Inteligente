from flask import Flask, send_from_directory
from flask_cors import CORS
from routes import routes
from models import create_table
from database import get_connection
import os
app = Flask(__name__)
CORS(app)
print("🔧 Inicializando banco de dados...")
conn = get_connection()
create_table(conn)
conn.close()
print("✅ Banco de dados inicializado")
app.register_blueprint(routes)
@app.route('/imagens/<filename>')
def serve_image(filename):
    """Serve imagens da pasta Imagens"""
    try:
        image_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Imagens")
        return send_from_directory(image_path, filename)
    except FileNotFoundError:
        return "Imagem não encontrada", 404
@app.route('/debug/imagens')
def debug_images():
    """Endpoint de debug para listar imagens disponíveis"""
    try:
        image_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Imagens")
        files = os.listdir(image_path) if os.path.exists(image_path) else []
        return {"pasta": image_path, "arquivos": files, "total": len(files)}
    except Exception as e:
        return {"erro": str(e)}, 500
if __name__ == "__main__":
    print("🚀 Iniciando servidor Flask...")
    print("📋 API disponível em: http://localhost:5000")
    try:
        from database import get_connection
        conn = get_connection()
        conn.close()
        print("✅ Conexão com banco OK")
    except Exception as e:
        print(f"❌ Erro na conexão: {e}")
    app.run(debug=True, host="0.0.0.0", port=5000)
