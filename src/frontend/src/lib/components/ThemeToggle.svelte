<script>
  import { browser } from "$app/environment";
  import SunIcon from "$lib/icons/SunIcon.svelte";
  import MoonIcon from "$lib/icons/MoonIcon.svelte";

  const LIGHT = "bumblebee";
  const DARK = "abyss";
  const STORAGE_KEY = "wpd-theme";

  let dark = $state(false);

  if (browser) {
    const saved = localStorage.getItem(STORAGE_KEY);
    if (saved) {
      dark = saved === DARK;
    } else {
      dark = window.matchMedia("(prefers-color-scheme: dark)").matches;
    }
  }

  let initialized = false;

  function apply(isDark) {
    if (!browser) return;
    const theme = isDark ? DARK : LIGHT;
    localStorage.setItem(STORAGE_KEY, theme);
    if (!initialized) {
      document.documentElement.setAttribute("data-theme", theme);
      initialized = true;
      return;
    }
    const el = document.documentElement;
    el.classList.add("theme-transitioning");
    void el.offsetHeight;
    el.setAttribute("data-theme", theme);
    setTimeout(() => el.classList.remove("theme-transitioning"), 350);
  }

  $effect(() => {
    apply(dark);
  });
</script>

<label class="swap swap-rotate" aria-label="Toggle dark mode">
  <input type="checkbox" bind:checked={dark} />
  <SunIcon class="swap-off size-5 fill-current" />
  <MoonIcon class="swap-on size-5 fill-current" />
</label>
