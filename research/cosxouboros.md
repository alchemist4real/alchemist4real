<div align="center">

# 𓆙 COS-X // OUROBOROS

[![Status: Operational](https://img.shields.io/badge/STATUS-OPERATIONAL-171717?style=for-the-badge&color=171717&labelColor=2563eb)](https://github.com/alchemist4real/cosxouboros)
[![AI Engine: Gemini](https://img.shields.io/badge/ENGINE-GEMINI_1.5_FLASH-171717?style=for-the-badge&color=171717&labelColor=2563eb)](https://aistudio.google.com/)
[![Architecture: Flask](https://img.shields.io/badge/CORE-FLASK-171717?style=for-the-badge&color=171717&labelColor=2563eb)](https://flask.palletsprojects.com/)

*an autonomous web entity that endlessly rewrites its own code via ai.*

</div>

---

## ✦ OVERVIEW

**COS-X / OUROBOROS** is a self-evolving digital entity masquerading as a web application. Engineered to autonomously modify its own genetic makeup (source code), it undergoes continuous iterations driven by generative AI. Like the mythological Ouroboros consuming its own tail, the system parses its current state to forge its next evolution.

Hosted natively on Vercel and built with a lightweight Flask backbone, the application dynamically fetches its most recent iteration directly from its repository. It evolves either through calculated, algorithmic randomness or via direct, manual directives injected by its architect.

## ✦ ARCHITECTURE

The entity's survival relies on a symbiotic relationship between its environment and its cognitive engine:

*   🧬 **The Interface** (`templates/index.html`): The visible manifestation and current DNA of the entity.
*   ⚙️ **The Core** (`api/index.py`): The central nervous system, routing requests and managing the evolution cycle.
*   🧠 **The Catalyst** (`Gemini 1.5 Flash`): The external intelligence responsible for mutating and refining the interface.
*   🌌 **The Nexus** (`GitHub API`): The immortal ledger where each mutation is permanently written, versioned, and stored.

## ✦ MECHANISM OF EVOLUTION

The system operates via an exposed evolution trigger (`/api/evolve_trigger`). Upon activation, the cycle begins:

1.  **Extraction**: The system reads its current HTML representation from the repository.
2.  **Directive Check**: It parses `instructions.txt` for any manual overrides from the architect.
3.  **Mutation Selection**: If no manual directive is present, it autonomously selects a structural or aesthetic mutation goal (e.g., advanced typography, futuristic UI elements, dark mode shifts).
4.  **Synthesis**: The cognitive engine processes the current DNA alongside the goal, hallucinating a superior HTML structure.
5.  **Commitment**: The system overwrites its own repository file, permanently committing the new code.

## ✦ INITIATION

To instantiate your own localized iteration of the Ouroboros cycle:

```bash
# 1. Clone the genetic sequence
git clone https://github.com/alchemist4real/cosxouboros.git

# 2. Install vital dependencies
pip install -r requirements.txt
```

### Environmental Variables
The entity requires the following variables to breathe:
*   `GEMINI_API_KEY`: Authentication for the cognitive engine.
*   `GITHUB_TOKEN`: The PAT required for self-writing repository commits.
*   `REPO_NAME`: The repository identifier (e.g., `alchemist4real/cosxouboros`).

## ✦ THE ARCHITECT'S COMMAND

To force a specific, non-random mutation, write a directive into `instructions.txt`. The system will prioritize this over its autonomous cycle, execute the structural change, and subsequently erase the directive to return to a resting state.

---

<div align="center">
    <i>"a system that writes itself is a system that outlives its creator."</i>
    <br><br>
    Architect: <b>Ahmad Muqorrobin</b> // Ouroboros Cloud
</div>
