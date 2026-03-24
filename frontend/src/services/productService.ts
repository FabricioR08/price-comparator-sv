import axios from 'axios'
import type { PriceResult } from '../types/PriceResult'

const API_URL = 'http://localhost:8080/api'

export const searchProducts = async (keyword: string): Promise<PriceResult[]> => {
  const response = await axios.get<PriceResult[]>(`${API_URL}/products/search`, {
    params: { keyword }
  })
  return response.data
}