import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  base: './', // для использования относительных путей
  build: {
    outDir: 'dist',
  },
});
