import { defineConfig, loadEnv } from 'vite';
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default ({ mode }) => {
  process.env = {...process.env, ...loadEnv(mode, process.cwd())};
  
  console.log('--------------------')
  console.log('Mode:', mode)
  console.log('Base path:', process.env.VITE_APP_BASE_PATH)
  console.log('API base URL:', process.env.VITE_API_BASE_URL)
  console.log('--------------------')

  return defineConfig({
    plugins: [vue()],
    base: process.env.VITE_APP_BASE_PATH,
    emptyOutDir: true,
    // envDir: '../',
  })
}
