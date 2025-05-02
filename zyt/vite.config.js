import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { fileURLToPath, URL } from 'node:url'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  server: {
    host: '0.0.0.0',   // <== 必须添加，让 Vite 监听所有地址
    port: 8080,
    proxy: {
      // 代理API请求到Django后端
      '/api': {
        target: 'http://118.178.232.89:8000',
        changeOrigin: true,
        secure: false
      },
      // 代理媒体文件
      '/media': {
        target: 'http://118.178.232.89:8000',
        changeOrigin: true,
        secure: false
      }
    }
  }
})
