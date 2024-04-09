import path from "node:path"

import react from "@vitejs/plugin-react"
import { defineConfig, loadEnv } from "vite"

// https://vitejs.dev/config/
export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, path.join(process.cwd(), "../"), "")

  const host = env.HOST || "127.0.0.1"
  const port = env.PORT || "8000"

  return {
    plugins: [react()],
    server: {
      proxy: {
        "/api": {
          target: `http://${host}:${port}`,
          changeOrigin: true,
          rewrite: (path) => path.replace(/^\/api/, ""),
        },
      },
    },
    envDir: "../",
  }
})
