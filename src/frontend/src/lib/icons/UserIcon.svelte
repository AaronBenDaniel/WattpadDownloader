<script>
  let { size = 16, ...rest } = $props();
</script>

<svg
  viewBox="0 0 24 24"
  width={size}
  height={size}
  fill="none"
  stroke="currentColor"
  stroke-width="1.8"
  stroke-linecap="round"
  stroke-linejoin="round"
  aria-hidden="true"
  {...rest}
>
  <circle cx="12" cy="8" r="4" />
  <path d="M4 21c1.5-4 5-6 8-6s6.5 2 8 6" />
</svg>
