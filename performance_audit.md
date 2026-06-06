# Performance Audit: `alchemist4real/index.html`

## Overview
Overall, the portfolio site uses a lightweight vanilla HTML/CSS/JS stack which inherently offers great baseline performance. However, there are a few bottlenecks specifically related to asset loading and CSS rendering complexity.

## 1. Asset Loading
- **Render-Blocking CSS**: 
  - Font Awesome is loaded synchronously in the `<head>` (`<link href="https://cdnjs.cloudflare.com/.../all.min.css" rel="stylesheet">`). This blocks initial page rendering. Consider adding `media="print" onload="this.media='all'"` to defer its loading if icons aren't critical for the initial paint, or at least add `preconnect` to `cdnjs.cloudflare.com`.
- **Font Optimization**:
  - The `Inter` font lacks a `<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>` tag. Adding this will speed up the TCP/TLS handshake for the font download.
  - **Critical Issue**: The `Silkscreen` font is loaded using `@import` inside the `<style>` block. This causes a sequential dependency (browser must parse HTML -> parse CSS -> discover `@import` -> fetch font CSS -> fetch font). Move this to a `<link>` tag in the `<head>` to allow parallel downloading.
- **Network Requests**:
  - The GitHub API stats fetch (`api.github.com/users/...`) runs immediately when the JavaScript executes. Since the "Connect" section is at the bottom of the page, consider wrapping these `fetch` calls in an `IntersectionObserver` so they only execute when the user scrolls near the footer, saving initial network bandwidth.

## 2. Rendering Speed & UI Performance
- **Expensive CSS Properties**:
  - The `backdrop-filter: blur(16px)` applied to the `<nav>` and `.icon-wrap` elements is computationally expensive and can cause stuttering/jank on low-end mobile devices, especially during scrolling. 
  - The `box-shadow` animations (e.g., the `.dot` pulse animation and the `.project-card:hover` glow) cause repaints. While visually appealing, animating `box-shadow` is not as performant as animating `transform` or `opacity`.
- **Scanline Overlay**:
  - The `body::after` fixed scanline effect (`repeating-linear-gradient`) covers the entire viewport and pointer events are set to `none`. While visually striking, large fixed overlays with gradients can force the browser into heavy composite operations during scrolling.
- **Scroll Performance**:
  - Using `IntersectionObserver` for the `.fade-in` elements is excellent for performance. It avoids the common trap of binding expensive layout calculations to the `scroll` event.
  - The inline CSS strategy (all styles in `<style>`) eliminates an extra network request for the stylesheet, ensuring the First Meaningful Paint (FMP) is as fast as possible for this single-page structure.

## Summary Recommendations
1. Replace `@import` with `<link>` for the Silkscreen font.
2. Add `<link rel="preconnect">` for Google Fonts and Font Awesome.
3. Lazy-load the GitHub API fetch requests using `IntersectionObserver`.
4. Be cautious with `backdrop-filter` and animated `box-shadow` if targeting lower-end devices.
