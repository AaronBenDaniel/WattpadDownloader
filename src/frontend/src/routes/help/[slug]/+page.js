const modules = import.meta.glob("$lib/content/help/en/*.svx");

function slugFromPath(path) {
  return path.split("/").pop().replace(".svx", "");
}

export async function load({ params }) {
  const entry = Object.entries(modules).find(([path]) => slugFromPath(path) === params.slug);

  if (!entry) {
    throw new Error(`Article not found: ${params.slug}`);
  }

  const mod = await entry[1]();
  return {
    content: mod.default,
    meta: mod.metadata
  };
}

export function entries() {
  return Object.keys(modules).map((path) => ({ slug: slugFromPath(path) }));
}
