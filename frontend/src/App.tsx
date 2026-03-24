import { useState } from 'react'
import { searchProducts } from './services/productService'
import type { PriceResult } from './types/PriceResult'
import './App.css'

function App() {
  const [keyword, setKeyword] = useState('')
  const [results, setResults] = useState<PriceResult[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleSearch = async () => {
    if (!keyword.trim()) return
    setLoading(true)
    setError('')
    try {
      const data = await searchProducts(keyword)
      setResults(data)
    } catch {
      setError('No se encontraron productos o hubo un error.')
      setResults([])
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={{ maxWidth: '800px', margin: '0 auto', padding: '2rem' }}>
      <h1>🛒 Comparador de Precios</h1>
      <p>Encuentra el precio más bajo entre tiendas de El Salvador</p>

      <div style={{ display: 'flex', gap: '1rem', marginBottom: '2rem' }}>
        <input
          type="text"
          placeholder="Buscar producto... ej: arroz"
          value={keyword}
          onChange={(e) => setKeyword(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
          style={{ flex: 1, padding: '0.5rem', fontSize: '1rem' }}
        />
        <button onClick={handleSearch} style={{ padding: '0.5rem 1.5rem', fontSize: '1rem' }}>
          Buscar
        </button>
      </div>

      {loading && <p>Buscando...</p>}
      {error && <p style={{ color: 'red' }}>{error}</p>}

      {results.length > 0 && (
        <table style={{ width: '100%', borderCollapse: 'collapse' }}>
          <thead>
            <tr style={{ backgroundColor: '#f0f0f0' }}>
              <th style={{ padding: '0.75rem', textAlign: 'left' }}>#</th>
              <th style={{ padding: '0.75rem', textAlign: 'left' }}>Producto</th>
              <th style={{ padding: '0.75rem', textAlign: 'left' }}>Tienda</th>
              <th style={{ padding: '0.75rem', textAlign: 'right' }}>Precio</th>
              <th style={{ padding: '0.75rem', textAlign: 'center' }}>Ver</th>
            </tr>
          </thead>
          <tbody>
            {results.map((r, i) => (
              <tr key={i} style={{ borderBottom: '1px solid #ddd', backgroundColor: i === 0 ? '#f0fff0' : 'white' }}>
                <td style={{ padding: '0.75rem' }}>{i === 0 ? '🥇' : i + 1}</td>
                <td style={{ padding: '0.75rem' }}>{r.productName}</td>
                <td style={{ padding: '0.75rem' }}>{r.storeName}</td>
                <td style={{ padding: '0.75rem', textAlign: 'right', fontWeight: 'bold' }}>
                  ${r.price.toFixed(2)}
                </td>
                <td style={{ padding: '0.75rem', textAlign: 'center' }}>
                  <a href={r.productUrl} target="_blank" rel="noreferrer">🔗</a>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  )
}

export default App