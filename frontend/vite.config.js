import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src')
    },
  },
  build: {
    outDir: './build',
    emptyOutDir: true,
    rollupOptions: {
      output: {
        assetFileNames: (assetInfo) => {
          if (assetInfo.name == 'style.css') {
            return 'css/style.css';
          }
          return 'assets/[name][extname]';
        },
      },
    },
  },
  base: './',
  // server: {
  //   proxy: {
  //     '^/api': {
  //       target: 'https://budget-application-hkvk.onrender.com:8000',
  //       changeOrigin: true
  //     }
  //   }
  // }
})
