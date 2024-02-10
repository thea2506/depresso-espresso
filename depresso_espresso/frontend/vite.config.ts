import { defineConfig } from "vite";
import react from "@vitejs/plugin-react-swc";

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],

  build: {
    rollupOptions: {
      output: {
        assetFileNames: () => {
          return `static/[name]-[hash][extname]`;
        },
        chunkFileNames: "static/[name]-[hash].js",
        entryFileNames: "static/[name]-[hash].js",
      },
    },
  },
});
