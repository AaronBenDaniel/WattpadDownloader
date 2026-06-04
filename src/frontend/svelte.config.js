import adapter from "@sveltejs/adapter-static";

const config = { kit: { adapter: adapter({ strict: false, fallback: "200.html" }) } };

export default config;
