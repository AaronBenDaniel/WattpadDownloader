<script>
  let { size = 16, ...rest } = $props();
</script>

<svg
  style="display: inline; vertical-align: center"
  viewBox="0 0 24 24"
  width={size}
  height={size}
  fill="none"
  stroke="currentColor"
  stroke-width="2"
  stroke-linecap="round"
  stroke-linejoin="round"
  aria-hidden="true"
  {...rest}
>
  <path d="M12 4v12" />
  <path d="M7 11l5 5 5-5" />
  <path d="M5 20h14" />
</svg>
