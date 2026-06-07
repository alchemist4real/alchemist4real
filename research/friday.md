<div align="center">
  <h1>🌌 F.R.I.D.A.Y.</h1>
  <p><em>Your dark, sleek, and intelligent personal AI assistant at the edge.</em></p>

  <p>
    <img src="https://img.shields.io/badge/Cloudflare-F38020?style=for-the-badge&logo=Cloudflare&logoColor=white" alt="Cloudflare Workers" />
    <img src="https://img.shields.io/badge/AI-Black?style=for-the-badge&logo=openai&logoColor=white" alt="Workers AI" />
    <img src="https://img.shields.io/badge/esbuild-FFCF00?style=for-the-badge&logo=esbuild&logoColor=black" alt="Esbuild" />
  </p>
</div>

---

## ⚡ Overview

**FRIDAY** is an aesthetic, dark-themed AI assistant web application powered by **Cloudflare Workers AI**. Built with a sleek interface designed for modern web interactions, it effortlessly toggles between dynamic Chat and Call modes.

## 🌑 Features

- **Aesthetic Dark Mode:** A stunning, deep-dark UI optimized for visual comfort and high contrast.
- **Edge AI Powered:** Seamless integration with `@cloudflare/ai` to bring rapid, serverless ML inference.
- **Dual Interface Modes:** Swap intuitively between interactive **Chat Mode** and immersive **Call Mode**.
- **Lightning Fast:** Bundled perfectly with `esbuild` to deliver an ultra-lightweight edge worker.

## 🛠️ Tech Stack

- **Frontend:** HTML, CSS (Custom Properties), Vanilla JavaScript
- **Backend/Edge:** Cloudflare Workers (`public/_worker.js`)
- **Bundler:** ESBuild

## 🚀 Getting Started

### Prerequisites

- Node.js & npm
- Wrangler (Cloudflare CLI)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/alchemist4real/friday.git
   cd friday
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Build the worker**
   ```bash
   npm run build
   ```
   > This compiles `src/api.js` into `public/_worker.js` via `esbuild`.

4. **Deploy to Edge**
   ```bash
   wrangler deploy
   ```

## 📜 License

This project is entirely private. All rights reserved.
