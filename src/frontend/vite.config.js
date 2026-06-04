import tailwindcss from "@tailwindcss/vite";
import { sveltekit } from "@sveltejs/kit/vite";
import { defineConfig } from "vite";

export default defineConfig({
  plugins: [tailwindcss(), sveltekit()],
  server: {
    allowedHosts: true,
    proxy: {
      "/download": "http://localhost:5042",
      "/activate": "http://localhost:5042",
      "/admin": "http://localhost:5042",
      "/user": "http://localhost:5042"
    }
  }
});
