import React, { useState, useEffect } from 'react';

const SugestaoRoupa = () => {
  const [cidade, setCidade] = useState('Juiz de Fora');
  const [clima, setClima] = useState(null);
  const [sugestao, setSugestao] = useState(null);
  const [loading, setLoading] = useState(false);
  const [erro, setErro] = useState('');
  const [feedback, setFeedback] = useState(null);

  const buscarSugestao = async () => {
    if (!cidade.trim()) {
      setErro('Por favor, digite o nome de uma cidade.');
      return;
    }

    setLoading(true);
    setErro('');
    setFeedback(null);

    try {
      const response = await fetch('http://localhost:5000/api/sugestao', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ cidade })
      });

      const data = await response.json();

      if (response.ok) {
        setClima(data.clima);
        const sugestaoProcessada = {
          sugestao_principal: `Outfit perfeito para ${data.clima.temperatura}°C em ${data.clima.cidade}`,
          explicacao: data.detalhes?.recomendacao || 'Sugestão baseada no clima atual',
          confianca: Math.round(data.score * 5),
          outfit: {}
        };
        
        if (data.sugestao && Array.isArray(data.sugestao)) {
          data.sugestao.forEach(peca => {
            sugestaoProcessada.outfit[peca.tipo] = {
              id: peca.id,
              nome: peca.nome,
              cor: peca.cor,
              imagem: peca.imagem_path
            };
          });
        }
        
        setSugestao(sugestaoProcessada);
      } else {
        setErro(data.erro || 'Erro ao buscar sugestão');
      }
    } catch (error) {
      setErro('Erro de conexão com o servidor');
    } finally {
      setLoading(false);
    }
  };

  const enviarFeedback = async (tipo) => {
    try {
      await fetch('http://localhost:5000/api/feedback', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          cidade,
          temperatura: clima?.temperatura,
          tipo_feedback: tipo
        })
      });
      setFeedback(tipo);
    } catch (error) {
      console.error('Erro ao enviar feedback:', error);
    }
  };

  useEffect(() => {
    buscarSugestao();
  }, []);

  return (
    <div style={{ padding: 'var(--space-xl) 0', flex: 1 }}>
      <div className="container">
        {/* Header */}
        <div style={{ textAlign: 'center', marginBottom: 'var(--space-2xl)' }}>
          <h1 style={{ fontSize: '2.5rem', fontWeight: '700', marginBottom: 'var(--space-md)' }}>
            🤖 Sugestão IA
          </h1>
          <p style={{ fontSize: '1.125rem', maxWidth: '600px', margin: '0 auto' }}>
            Descubra o outfit perfeito baseado no clima atual
          </p>
        </div>

        {/* Search */}
        <div className="card">
          <div style={{ display: 'flex', gap: 'var(--space-md)', flexWrap: 'wrap' }}>
            <input
              type="text"
              value={cidade}
              onChange={(e) => setCidade(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && buscarSugestao()}
              placeholder="Digite o nome da cidade..."
              style={{ flex: 1, minWidth: '300px' }}
            />
            <button
              onClick={buscarSugestao}
              disabled={loading}
              className="primary"
              style={{ padding: 'var(--space-sm) var(--space-lg)' }}
            >
              {loading ? '⏳ Analisando...' : '🔍 Buscar'}
            </button>
          </div>
          
          {erro && (
            <div className="error">
              ⚠️ {erro}
            </div>
          )}
        </div>

        {/* Loading */}
        {loading && (
          <div className="loading">
            <div className="spinner"></div>
            <p>Analisando clima e gerando sugestão...</p>
          </div>
        )}

        {/* Results */}
        {clima && !loading && (
          <div style={{ display: 'grid', gap: 'var(--space-xl)' }}>
            {/* Weather */}
            <div className="card">
              <h3 style={{ marginBottom: 'var(--space-lg)' }}>🌤️ Clima em {clima.cidade}</h3>
              <div className="weather-info">
                <div className="weather-temp">
                  {clima.temperatura}°C
                </div>
                <div className="weather-details">
                  <div className="weather-detail">
                    <div className="weather-detail-value">{clima.umidade}%</div>
                    <div className="weather-detail-label">Umidade</div>
                  </div>
                  <div className="weather-detail">
                    <div className="weather-detail-value">{clima.vento} km/h</div>
                    <div className="weather-detail-label">Vento</div>
                  </div>
                  <div className="weather-detail">
                    <div className="weather-detail-value">{clima.condicao}</div>
                    <div className="weather-detail-label">Condição</div>
                  </div>
                  <div className="weather-detail">
                    <div className="weather-detail-value">{clima.visibilidade} km</div>
                    <div className="weather-detail-label">Visibilidade</div>
                  </div>
                </div>
              </div>
            </div>

            {/* Suggestion */}
            {sugestao && (
              <div className="card">
                <div style={{ 
                  display: 'flex', 
                  justifyContent: 'space-between', 
                  alignItems: 'flex-start',
                  marginBottom: 'var(--space-lg)',
                  flexWrap: 'wrap',
                  gap: 'var(--space-md)'
                }}>
                  <h3>✨ Sua Sugestão Personalizada</h3>
                  <div className="badge badge-primary">
                    {sugestao.confianca}% confiança
                  </div>
                </div>

                <div style={{ marginBottom: 'var(--space-lg)' }}>
                  <p style={{ fontSize: '1.125rem', fontWeight: '500', marginBottom: 'var(--space-sm)' }}>
                    {sugestao.sugestao_principal}
                  </p>
                  <p>{sugestao.explicacao}</p>
                </div>

                {/* Outfit */}
                {sugestao.outfit && Object.keys(sugestao.outfit).length > 0 && (
                  <div>
                    <h4 style={{ marginBottom: 'var(--space-md)' }}>👕 Seu Outfit Completo</h4>
                    <div className="outfit-grid">
                      {Object.entries(sugestao.outfit).map(([tipo, item]) => (
                        <div key={tipo} className="outfit-item">
                          <div className="outfit-type">{tipo}</div>
                          
                          {item.id ? (
                            <img
                              src={`http://localhost:5000/api/image/${item.id}`}
                              alt={item.nome}
                              className="roupa-image"
                              onError={(e) => {
                                e.target.style.display = 'none';
                                e.target.nextSibling.style.display = 'flex';
                              }}
                            />
                          ) : item.imagem ? (
                            <img
                              src={`http://localhost:5000/imagens/${item.imagem}`}
                              alt={item.nome}
                              className="roupa-image"
                              onError={(e) => {
                                e.target.style.display = 'none';
                                e.target.nextSibling.style.display = 'flex';
                              }}
                            />
                          ) : null}
                          
                          <div className="image-placeholder" style={{ display: 'none' }}>
                            {tipo === 'superior' ? '👔' : 
                             tipo === 'inferior' ? '👖' : 
                             tipo === 'calcado' ? '👟' : 
                             tipo === 'casaco' ? '🧥' : '👕'}
                          </div>
                          
                          <div className="outfit-name">{item.nome}</div>
                          <div className="outfit-color">{item.cor}</div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Feedback */}
                {!feedback && (
                  <div style={{
                    borderTop: '1px solid var(--color-border)',
                    paddingTop: 'var(--space-lg)',
                    marginTop: 'var(--space-lg)'
                  }}>
                    <p style={{ marginBottom: 'var(--space-md)', textAlign: 'center' }}>
                      Esta sugestão foi útil?
                    </p>
                    <div style={{ display: 'flex', justifyContent: 'center', gap: 'var(--space-md)' }}>
                      <button onClick={() => enviarFeedback('positivo')} className="primary">
                        👍 Sim
                      </button>
                      <button onClick={() => enviarFeedback('negativo')}>
                        👎 Não
                      </button>
                    </div>
                  </div>
                )}

                {feedback && (
                  <div className="success">
                    ✅ Obrigado pelo seu feedback!
                  </div>
                )}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default SugestaoRoupa;
