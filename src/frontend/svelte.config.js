import adapter from "@sveltejs/adapter-static";

const config = {
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
