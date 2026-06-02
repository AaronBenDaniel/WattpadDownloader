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
  <path d="M3 3l18 18" />
  <path d="M10.6 6.1A10.7 10.7 0 0 1 12 6c6.5 0 10 7 10 7a17.7 17.7 0 0 1-3.2 4" />
  <path d="M6.7 6.7C3.7 8.5 2 12 2 12s3.5 7 10 7c1.7 0 3.3-.4 4.6-1" />
  <path d="M9.5 9.6a3 3 0 0 0 4.2 4.2" />
</svg>
