<script>
  let { size = 20, ...rest } = $props();
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
  <rect x="3" y="4" width="4" height="16" rx="1" />
  <rect x="9" y="4" width="4" height="16" rx="1" />
  <path d="M16 5l4 1-3 14-4-1z" />
</svg>
