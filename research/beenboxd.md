<div align="center">

# 🎦 beenboxd
**a sleek, ai-powered logger to bulk export movies to letterboxd.**

[![Built with HTML](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)](#)
[![Styled with Tailwind](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)](#)
[![Powered by Gemini](https://img.shields.io/badge/Gemini_AI-8E75B2?style=for-the-badge&logo=googlebard&logoColor=white)](#)

</div>

<br>

> **beenboxd** is a hyper-modern, glassmorphic web tool designed to make logging your movies effortless. utilizing the gemini ai api, it auto-fetches movie metadata, builds an elegant queue, and exports a clean csv perfectly formatted for letterboxd imports.

---

## ✦ features

- 🧠 **ai-driven auto-complete:** punch in a movie title, click auto, and gemini fetches the exact letterboxd slug, release year, and genres instantly.
- ⚡ **smart bulk processing:** paste a raw list of movie titles and watch the ai digest them in batches, generating rich metadata for your entire backlog.
- 💾 **persistent queue:** uses `localStorage` to safely hold onto your logged movies across sessions. don't lose your progress.
- 🎨 **glassmorphic aesthetic:** built with pure tailwind css, featuring a dark noise texture, watermorphism containers, and slick animated marquees.
- 📤 **letterboxd-ready export:** one-click download generates the perfect `.csv` schema (`Title, Year, Rating10, WatchedDate, Review, Tags`) to import straight into letterboxd.

## ✦ how to use

1. **add movies**: type a movie title and hit **auto** to fetch details. add your rating, review, and watch date.
2. **bulk import**: switch to the ai tab, drop a giant list of films, and let the system process them in batches.
3. **export**: hit the download button to generate your `letterboxd-import-*.csv` file.
4. **import to letterboxd**: head over to the [letterboxd import page](https://letterboxd.com/import/) and upload your newly created csv.

## ✦ tech stack

- **frontend:** HTML5, Tailwind CSS
- **ai integration:** Google Gemini API
- **data storage:** LocalStorage API
- **export logic:** Vanilla JavaScript Blob/CSV creation

<br>

<div align="center">
    <i>created for the love of cinema. keep your logs pristine.</i>
</div>
