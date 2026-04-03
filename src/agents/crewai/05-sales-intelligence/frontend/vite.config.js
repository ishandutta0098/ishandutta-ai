import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3004,
    proxy: {
      '/process-lead': 'http://localhost:8004',
      '/leads': 'http://localhost:8004',
      '/approve': 'http://localhost:8004',
      '/reject': 'http://localhost:8004',
      '/health': 'http://localhost:8004',
    },
  },
})
