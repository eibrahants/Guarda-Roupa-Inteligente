import React, { useState, useEffect } from 'react';

const RoupasList = () => {
  const [roupas, setRoupas] = useState([]);
  const [loading, setLoading] = useState(true);
  const [erro, setErro] = useState('');
  const [showForm, setShowForm] = useState(false);
  const [editingRoupa, setEditingRoupa] = useState(null);
  const [showPopup, setShowPopup] = useState(false);
  const [showEditPopup, setShowEditPopup] = useState(false);
  const [selectedRoupa, setSelectedRoupa] = useState(null);
  const [formData, setFormData] = useState({
    nome: '',
    tipo: 'superior',
    cor: '',
    temperatura_min: '',
    temperatura_max: '',
    imagem_path: '',
    imagem_file: null,
    imagem_preview: null
  });

  useEffect(() => {
    carregarRoupas();
  }, []);

  const carregarRoupas = async () => {
    try {
      setLoading(true);
      const response = await fetch('http://localhost:5000/roupas');
      if (response.ok) {
        const data = await response.json();
        setRoupas(data);
      } else {
        setErro('Erro ao carregar roupas');
      }
    } catch (error) {
      setErro('Erro de conexão');
    } finally {
      setLoading(false);
    }
  };

  const deletarRoupa = async (id) => {
    try {
      const response = await fetch(`http://localhost:5000/roupas/${id}`, {
        method: 'DELETE'
      });
      if (response.ok) {
        carregarRoupas();
        setShowPopup(false);
        setSelectedRoupa(null);
      }
    } catch (error) {
      setErro('Erro ao deletar roupa');
    }
  };

  const abrirPopup = (roupa) => {
    setSelectedRoupa(roupa);
    setShowPopup(true);
  };

  const fecharPopup = () => {
    setShowPopup(false);
    setSelectedRoupa(null);
  };

  const abrirEditPopup = (roupa) => {
    setEditingRoupa(roupa);
    setFormData({
      nome: roupa.nome || '',
      tipo: roupa.tipo || 'superior',
      cor: roupa.cor || '',
      temperatura_min: roupa.temperatura_min?.toString() || '',
      temperatura_max: roupa.temperatura_max?.toString() || '',
      imagem_path: roupa.imagem || '',
      imagem_file: null,
      imagem_preview: null
    });
    setShowEditPopup(true);
  };

  const fecharEditPopup = () => {
    setShowEditPopup(false);
    setEditingRoupa(null);
    setFormData({
      nome: '',
      tipo: 'superior',
      cor: '',
      temperatura_min: '',
      temperatura_max: '',
      imagem_path: '',
      imagem_file: null,
      imagem_preview: null
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    try {
      const url = editingRoupa 
        ? `http://localhost:5000/roupas/${editingRoupa.id}`
        : 'http://localhost:5000/roupas';
      
      const method = editingRoupa ? 'PUT' : 'POST';
      
      console.log('Enviando dados:', { method, url, formData });
      
      // Se há arquivo de imagem, usar FormData para upload
      if (formData.imagem_file) {
        const formDataUpload = new FormData();
        formDataUpload.append('nome', formData.nome);
        formDataUpload.append('tipo', formData.tipo);
        formDataUpload.append('cor', formData.cor);
        formDataUpload.append('temperatura_min', formData.temperatura_min);
        formDataUpload.append('temperatura_max', formData.temperatura_max);
        formDataUpload.append('imagem', formData.imagem_file);

        console.log('Usando FormData para upload de imagem');
        
        const response = await fetch(url, {
          method,
          body: formDataUpload
        });

        console.log('Resposta do servidor:', response.status, response.statusText);

        if (response.ok) {
          carregarRoupas();
          setShowForm(false);
          setShowEditPopup(false);
          setEditingRoupa(null);
          setFormData({
            nome: '',
            tipo: 'superior',
            cor: '',
            temperatura_min: '',
            temperatura_max: '',
            imagem_path: '',
            imagem_file: null,
            imagem_preview: null
          });
        } else {
          const errorData = await response.text();
          console.error('Erro do servidor:', errorData);
          setErro(`Erro ao salvar roupa: ${response.status} - ${errorData}`);
        }
      } else {
        // Caso não há arquivo, usar JSON normal
        const dataToSend = {
          nome: formData.nome,
          tipo: formData.tipo,
          cor: formData.cor,
          temperatura_min: formData.temperatura_min,
          temperatura_max: formData.temperatura_max,
          imagem_path: formData.imagem_path
        };

        console.log('Usando JSON para dados sem imagem:', dataToSend);

        const response = await fetch(url, {
          method,
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(dataToSend)
        });

        console.log('Resposta do servidor:', response.status, response.statusText);

        if (response.ok) {
          carregarRoupas();
          setShowForm(false);
          setShowEditPopup(false);
          setEditingRoupa(null);
          setFormData({
            nome: '',
            tipo: 'superior',
            cor: '',
            temperatura_min: '',
            temperatura_max: '',
            imagem_path: '',
            imagem_file: null,
            imagem_preview: null
          });
        } else {
          const errorData = await response.text();
          console.error('Erro do servidor:', errorData);
          setErro(`Erro ao salvar roupa: ${response.status} - ${errorData}`);
        }
      }
    } catch (error) {
      console.error('Erro de conexão:', error);
      setErro(`Erro de conexão: ${error.message}`);
    }
  };

  const editarRoupa = (roupa) => {
    abrirEditPopup(roupa);
  };

  const cancelarForm = () => {
    setShowForm(false);
    setEditingRoupa(null);
    setFormData({
      nome: '',
      tipo: 'superior',
      cor: '',
      temperatura_min: '',
      temperatura_max: '',
      imagem_path: '',
      imagem_file: null,
      imagem_preview: null
    });
  };

  const tiposIcon = {
    superior: '👔',
    inferior: '👖',
    calcado: '👟',
    casaco: '🧥',
    acessorio: '👜'
  };

  if (loading) {
    return (
      <div className="loading">
        <div className="spinner"></div>
        <p>Carregando seu guarda-roupa...</p>
      </div>
    );
  }

  return (
    <div style={{ padding: 'var(--space-xl) 0', flex: 1 }}>
      <div className="container">
        {/* Header */}
        <div style={{ 
          display: 'flex', 
          justifyContent: 'space-between', 
          alignItems: 'center',
          marginBottom: 'var(--space-xl)',
          flexWrap: 'wrap',
          gap: 'var(--space-md)'
        }}>
          <div>
            <h1 style={{ fontSize: '2rem', fontWeight: '700', marginBottom: 'var(--space-xs)' }}>
              👕 Meu Guarda-roupa
            </h1>
            <p style={{ margin: 0 }}>
              {roupas.length} {roupas.length === 1 ? 'peça cadastrada' : 'peças cadastradas'}
            </p>
          </div>
          <button
            onClick={() => setShowForm(!showForm)}
            className={showForm ? '' : 'primary'}
            style={{ padding: 'var(--space-sm) var(--space-lg)' }}
          >
            {showForm ? '❌ Cancelar' : '➕ Adicionar Roupa'}
          </button>
        </div>

        {erro && (
          <div className="error">
            ⚠️ {erro}
          </div>
        )}

        {/* Form */}
        {showForm && (
          <div className="card">
            <h3 style={{ marginBottom: 'var(--space-lg)' }}>
              {editingRoupa ? '✏️ Editar Roupa' : '➕ Adicionar Nova Roupa'}
            </h3>
            <form onSubmit={handleSubmit}>
              <div className="grid grid-2">
                <div>
                  <label>Nome da Roupa</label>
                  <input
                    type="text"
                    value={formData.nome}
                    onChange={(e) => setFormData({...formData, nome: e.target.value})}
                    required
                    placeholder="Ex: Camisa social azul"
                  />
                </div>
                <div>
                  <label>Tipo</label>
                  <select
                    value={formData.tipo}
                    onChange={(e) => setFormData({...formData, tipo: e.target.value})}
                    required
                  >
                    <option value="superior">Superior</option>
                    <option value="inferior">Inferior</option>
                    <option value="calcado">Calçado</option>
                    <option value="casaco">Casaco</option>
                    <option value="acessorio">Acessório</option>
                  </select>
                </div>
                <div>
                  <label>Cor</label>
                  <input
                    type="text"
                    value={formData.cor}
                    onChange={(e) => setFormData({...formData, cor: e.target.value})}
                    required
                    placeholder="Ex: azul, preto, branco"
                  />
                </div>
                <div>
                  <label>Imagem da Roupa</label>
                  <input
                    type="file"
                    accept="image/*"
                    onChange={(e) => {
                      const file = e.target.files[0];
                      if (file) {
                        const previewUrl = URL.createObjectURL(file);
                        setFormData({...formData, imagem_file: file, imagem_preview: previewUrl});
                      } else {
                        setFormData({...formData, imagem_file: null, imagem_preview: null});
                      }
                    }}
                    style={{ marginBottom: 'var(--space-sm)' }}
                  />
                  {formData.imagem_file && (
                    <div style={{ 
                      fontSize: '0.875rem', 
                      color: 'var(--color-text-secondary)',
                      marginTop: 'var(--space-xs)'
                    }}>
                      📎 {formData.imagem_file.name}
                    </div>
                  )}
                  {formData.imagem_preview && (
                    <div style={{ marginTop: 'var(--space-sm)' }}>
                      <img
                        src={formData.imagem_preview}
                        alt="Preview"
                        style={{
                          width: '100px',
                          height: '100px',
                          objectFit: 'cover',
                          borderRadius: 'var(--border-radius)',
                          border: '1px solid var(--color-border)'
                        }}
                      />
                    </div>
                  )}
                </div>
                <div>
                  <label>Nome da Imagem (opcional)</label>
                  <input
                    type="text"
                    value={formData.imagem_path}
                    onChange={(e) => setFormData({...formData, imagem_path: e.target.value})}
                    placeholder="Ex: camisa_azul.jpg"
                    disabled={formData.imagem_file}
                    style={{ 
                      opacity: formData.imagem_file ? 0.5 : 1,
                      cursor: formData.imagem_file ? 'not-allowed' : 'text'
                    }}
                  />
                  {formData.imagem_file && (
                    <div style={{ 
                      fontSize: '0.75rem', 
                      color: 'var(--color-text-secondary)',
                      marginTop: 'var(--space-xs)'
                    }}>
                      Use o upload de arquivo acima ou remova o arquivo para usar este campo
                    </div>
                  )}
                </div>
                <div>
                  <label>Temperatura Mínima (°C)</label>
                  <input
                    type="number"
                    value={formData.temperatura_min}
                    onChange={(e) => setFormData({...formData, temperatura_min: e.target.value})}
                    required
                    placeholder="Ex: 15"
                  />
                </div>
                <div>
                  <label>Temperatura Máxima (°C)</label>
                  <input
                    type="number"
                    value={formData.temperatura_max}
                    onChange={(e) => setFormData({...formData, temperatura_max: e.target.value})}
                    required
                    placeholder="Ex: 30"
                  />
                </div>
              </div>
              <div style={{ marginTop: 'var(--space-lg)', display: 'flex', gap: 'var(--space-md)' }}>
                <button type="submit" className="primary">
                  {editingRoupa ? '💾 Salvar' : '➕ Adicionar'}
                </button>
                <button type="button" onClick={cancelarForm}>
                  ❌ Cancelar
                </button>
              </div>
            </form>
          </div>
        )}

        {/* Grid de Roupas */}
        {roupas.length === 0 ? (
          <div className="card" style={{ textAlign: 'center', padding: 'var(--space-2xl)' }}>
            <div style={{ fontSize: '3rem', marginBottom: 'var(--space-md)' }}>👕</div>
            <h3 style={{ marginBottom: 'var(--space-md)' }}>Nenhuma roupa cadastrada</h3>
            <p style={{ marginBottom: 'var(--space-lg)' }}>
              Comece adicionando suas primeiras peças para receber sugestões personalizadas!
            </p>
            <button 
              onClick={() => setShowForm(true)}
              className="primary"
            >
              ➕ Adicionar Primeira Roupa
            </button>
          </div>
        ) : (
          <div className="grid grid-4">
            {roupas.map(roupa => (
              <div
                key={roupa.id}
                className="card"
                style={{
                  cursor: 'pointer',
                  transition: 'transform 0.2s ease, box-shadow 0.2s ease',
                  padding: 'var(--space-md)'
                }}
                onMouseEnter={(e) => {
                  e.currentTarget.style.transform = 'translateY(-2px)';
                  e.currentTarget.style.boxShadow = 'var(--shadow-md)';
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.transform = 'translateY(0)';
                  e.currentTarget.style.boxShadow = 'var(--shadow-sm)';
                }}
              >
                {/* Imagem */}
                <div style={{ marginBottom: 'var(--space-md)' }}>
                  {roupa.imagem ? (
                    <img
                      src={`http://localhost:5000/api/image/${roupa.id}`}
                      alt={roupa.nome}
                      className="roupa-image"
                      onError={(e) => {
                        console.log('Erro ao carregar imagem, tentando rota alternativa...');
                        e.target.src = `http://localhost:5000/imagens/${roupa.imagem}`;
                        e.target.onerror = () => {
                          e.target.style.display = 'none';
                          e.target.nextSibling.style.display = 'flex';
                        };
                      }}
                    />
                  ) : null}
                  <div
                    className="image-placeholder"
                    style={{
                      display: roupa.imagem ? 'none' : 'flex'
                    }}
                  >
                    {tiposIcon[roupa.tipo] || '👕'}
                  </div>
                </div>

                {/* Info */}
                <div>
                  <div style={{
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'flex-start',
                    marginBottom: 'var(--space-sm)'
                  }}>
                    <h4 style={{ 
                      fontSize: '1.125rem', 
                      fontWeight: '600', 
                      margin: 0,
                      flex: 1
                    }}>
                      {roupa.nome}
                    </h4>
                    <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--space-xs)' }}>
                      <span style={{ fontSize: '1.25rem' }}>
                        {tiposIcon[roupa.tipo] || '👕'}
                      </span>
                      <button
                        onClick={(e) => {
                          e.stopPropagation();
                          abrirPopup(roupa);
                        }}
                        style={{
                          background: 'none',
                          border: 'none',
                          cursor: 'pointer',
                          padding: '4px',
                          borderRadius: '4px',
                          color: 'var(--color-text-secondary)',
                          fontSize: '1.2rem',
                          lineHeight: 1
                        }}
                        title="Mais opções"
                      >
                        ⋮
                      </button>
                    </div>
                  </div>
                  
                  <div style={{ marginBottom: 'var(--space-sm)' }}>
                    <span className="badge">
                      {roupa.tipo}
                    </span>
                  </div>
                  
                  <div style={{ 
                    color: 'var(--color-text-secondary)', 
                    marginBottom: 'var(--space-sm)' 
                  }}>
                    🎨 {roupa.cor}
                  </div>
                  
                  <div style={{ 
                    fontSize: '0.875rem', 
                    color: 'var(--color-text-secondary)' 
                  }}>
                    🌡️ {roupa.temperatura_min}°C - {roupa.temperatura_max}°C
                  </div>
                </div>

                {/* Ações */}
                <div style={{
                  marginTop: 'var(--space-md)',
                  display: 'flex',
                  justifyContent: 'center'
                }}>
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      abrirEditPopup(roupa);
                    }}
                    className="primary"
                    style={{ 
                      padding: 'var(--space-sm) var(--space-md)',
                      fontSize: '0.875rem',
                      minWidth: '80px'
                    }}
                    title="Editar"
                  >
                    Editar
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Popup de opções */}
      {showPopup && selectedRoupa && (
        <div 
          style={{
            position: 'fixed',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            backgroundColor: 'rgba(0, 0, 0, 0.5)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            zIndex: 1000
          }}
          onClick={fecharPopup}
        >
          <div 
            style={{
              backgroundColor: 'white',
              borderRadius: 'var(--border-radius)',
              padding: 'var(--space-xl)',
              boxShadow: '0 10px 25px rgba(0, 0, 0, 0.15)',
              maxWidth: '300px',
              width: '90%'
            }}
            onClick={(e) => e.stopPropagation()}
          >
            <h3 style={{ 
              marginBottom: 'var(--space-lg)', 
              textAlign: 'center',
              color: 'var(--color-text)'
            }}>
              {selectedRoupa.nome}
            </h3>
            
            <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-md)' }}>
              <button
                onClick={() => {
                  abrirEditPopup(selectedRoupa);
                  fecharPopup();
                }}
                className="primary"
                style={{ width: '100%' }}
              >
                ✏️ Editar
              </button>
              
              <button
                onClick={() => {
                  if (confirm(`Tem certeza que deseja excluir "${selectedRoupa.nome}"?`)) {
                    deletarRoupa(selectedRoupa.id);
                  }
                  fecharPopup();
                }}
                style={{ 
                  width: '100%',
                  background: '#dc2626',
                  borderColor: '#dc2626',
                  color: 'white'
                }}
              >
                🗑️ Excluir
              </button>
              
              <button
                onClick={fecharPopup}
                style={{ 
                  width: '100%',
                  background: 'var(--color-background)',
                  color: 'var(--color-text)',
                  border: '1px solid var(--color-border)'
                }}
              >
                Cancelar
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Popup de edição */}
      {showEditPopup && editingRoupa && (
        <div 
          style={{
            position: 'fixed',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            backgroundColor: 'rgba(0, 0, 0, 0.5)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            zIndex: 1000,
            padding: 'var(--space-md)'
          }}
          onClick={fecharEditPopup}
        >
          <div 
            style={{
              backgroundColor: 'white',
              borderRadius: 'var(--border-radius)',
              padding: 'var(--space-xl)',
              boxShadow: '0 10px 25px rgba(0, 0, 0, 0.15)',
              maxWidth: '500px',
              width: '100%',
              maxHeight: '90vh',
              overflowY: 'auto'
            }}
            onClick={(e) => e.stopPropagation()}
          >
            <h3 style={{ 
              marginBottom: 'var(--space-lg)', 
              textAlign: 'center',
              color: 'var(--color-text)'
            }}>
              ✏️ Editar Roupa
            </h3>
            
            <form onSubmit={handleSubmit}>
              <div className="grid grid-2">
                <div>
                  <label>Nome da Roupa</label>
                  <input
                    type="text"
                    value={formData.nome}
                    onChange={(e) => setFormData({...formData, nome: e.target.value})}
                    required
                    placeholder="Ex: Camisa social azul"
                  />
                </div>
                <div>
                  <label>Tipo</label>
                  <select
                    value={formData.tipo}
                    onChange={(e) => setFormData({...formData, tipo: e.target.value})}
                    required
                  >
                    <option value="superior">Superior</option>
                    <option value="inferior">Inferior</option>
                    <option value="calcado">Calçado</option>
                    <option value="casaco">Casaco</option>
                    <option value="acessorio">Acessório</option>
                  </select>
                </div>
                <div>
                  <label>Cor</label>
                  <input
                    type="text"
                    value={formData.cor}
                    onChange={(e) => setFormData({...formData, cor: e.target.value})}
                    required
                    placeholder="Ex: azul, preto, branco"
                  />
                </div>
                <div>
                  <label>Nova Imagem (opcional)</label>
                  <input
                    type="file"
                    accept="image/*"
                    onChange={(e) => {
                      const file = e.target.files[0];
                      if (file) {
                        const previewUrl = URL.createObjectURL(file);
                        setFormData({...formData, imagem_file: file, imagem_preview: previewUrl});
                      } else {
                        setFormData({...formData, imagem_file: null, imagem_preview: null});
                      }
                    }}
                    style={{ marginBottom: 'var(--space-sm)' }}
                  />
                  {formData.imagem_file && (
                    <div style={{ 
                      fontSize: '0.875rem', 
                      color: 'var(--color-text-secondary)',
                      marginTop: 'var(--space-xs)'
                    }}>
                      📎 {formData.imagem_file.name}
                    </div>
                  )}
                  {formData.imagem_preview && (
                    <div style={{ marginTop: 'var(--space-sm)' }}>
                      <img
                        src={formData.imagem_preview}
                        alt="Preview"
                        style={{
                          width: '100px',
                          height: '100px',
                          objectFit: 'cover',
                          borderRadius: 'var(--border-radius)',
                          border: '1px solid var(--color-border)'
                        }}
                      />
                    </div>
                  )}
                </div>
                <div>
                  <label>Nome da Imagem (opcional)</label>
                  <input
                    type="text"
                    value={formData.imagem_path}
                    onChange={(e) => setFormData({...formData, imagem_path: e.target.value})}
                    placeholder="Ex: camisa_azul.jpg"
                    disabled={formData.imagem_file}
                    style={{ 
                      opacity: formData.imagem_file ? 0.5 : 1,
                      cursor: formData.imagem_file ? 'not-allowed' : 'text'
                    }}
                  />
                  {formData.imagem_file && (
                    <div style={{ 
                      fontSize: '0.75rem', 
                      color: 'var(--color-text-secondary)',
                      marginTop: 'var(--space-xs)'
                    }}>
                      Nova imagem substituirá a atual
                    </div>
                  )}
                </div>
                <div>
                  <label>Temperatura Mínima (°C)</label>
                  <input
                    type="number"
                    value={formData.temperatura_min}
                    onChange={(e) => setFormData({...formData, temperatura_min: e.target.value})}
                    required
                    placeholder="Ex: 15"
                  />
                </div>
                <div>
                  <label>Temperatura Máxima (°C)</label>
                  <input
                    type="number"
                    value={formData.temperatura_max}
                    onChange={(e) => setFormData({...formData, temperatura_max: e.target.value})}
                    required
                    placeholder="Ex: 30"
                  />
                </div>
              </div>
              <div style={{ marginTop: 'var(--space-lg)', display: 'flex', gap: 'var(--space-md)' }}>
                <button type="submit" className="primary" style={{ flex: 1 }}>
                  💾 Salvar Alterações
                </button>
                <button type="button" onClick={fecharEditPopup} style={{ flex: 1 }}>
                  ❌ Cancelar
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default RoupasList;
