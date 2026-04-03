import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
export default defineConfig({
  plugins: [react()],
  server: {
    port: 3003,
    proxy: {
      '/research': 'http://localhost:8003',
      '/health': 'http://localhost:8003',
      '/logs': 'http://localhost:8003',
    }
  }
})
