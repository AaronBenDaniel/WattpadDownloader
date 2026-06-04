import { browser } from "$app/environment";

const STORAGE_KEY = "wpd-user-id";

let features = $state([]);
let externalIdentifier = $state("");
let loaded = $state(false);

export function getUserId() {
  if (!browser) return null;
  return localStorage.getItem(STORAGE_KEY);
}

export function setUserId(id) {
  if (!browser) return;
  localStorage.setItem(STORAGE_KEY, id);
}

export function clearUser() {
  if (!browser) return;
  localStorage.removeItem(STORAGE_KEY);
  features = [];
  externalIdentifier = "";
}

export function getFeatures() {
  return features;
}

export function getExternalIdentifier() {
  return externalIdentifier;
}

export function isLoaded() {
  return loaded;
}

export function hasFeature(name) {
  return features.includes(name);
}

export async function loadFeatures() {
  if (!browser) return;
  const userId = getUserId();
  if (!userId) {
    features = [];
    externalIdentifier = "";
    loaded = true;
    return;
  }
  try {
    const res = await fetch(`/user/features?user_id=${encodeURIComponent(userId)}`);
    if (res.ok) {
      const data = await res.json();
      features = data.features;
      externalIdentifier = data.external_identifier || "";
    }
  } catch {
    // network error — features stay empty
  }
  loaded = true;
}
