/// <reference types="vite/client" />

interface ImportMetaEnv {
  /** URL base del API del backend (ej. http://localhost:8000). Si no está definida, se usa mock. */
  readonly VITE_API_BASE_URL?: string
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}
