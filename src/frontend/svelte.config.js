import adapter from "@sveltejs/adapter-static";
import { mdsvex } from "mdsvex";

const config = {
  extensions: [".svelte", ".svx"],
  preprocess: [mdsvex()],
  kit: {
    adapter: adapter({ strict: false }),
    prerender: {
      handleHttpError: ({ path, message }) => {
        if (path.startsWith("/auth/")) return;
        throw new Error(message);
      }
    }
  }
};

export default config;
