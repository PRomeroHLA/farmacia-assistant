/**
 * Configuración del cliente API (base URL). Si VITE_API_BASE_URL no está definida,
 * se usa la URL por defecto en desarrollo o "" para decidir uso de mock.
 */
const DEFAULT_API_BASE_URL = "http://localhost:8000"

export function getApiBaseUrl(): string {
  const url = import.meta.env.VITE_API_BASE_URL
  return url !== undefined && url !== "" ? url : DEFAULT_API_BASE_URL
}

/**
 * True si hay una URL de API configurada (permite elegir cliente real vs mock).
 */
export function hasApiBaseUrl(): boolean {
  const url = import.meta.env.VITE_API_BASE_URL
  return url !== undefined && url !== ""
}
