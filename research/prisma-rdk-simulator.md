<div align="center">

# 🪐 PRISMA

### *Pengawasan Distribusi Antibiotik Berbasis Blockchain & SATUSEHAT*

[![React](https://img.shields.io/badge/React-18.3-20232a?style=for-the-badge&logo=react)](https://react.dev/)
[![Vite](https://img.shields.io/badge/Vite-5.4-646cff?style=for-the-badge&logo=vite)](https://vite.dev/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.5-3178c6?style=for-the-badge&logo=typescript)](https://www.typescriptlang.org/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-3.4-38bdf8?style=for-the-badge&logo=tailwindcss)](https://tailwindcss.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-teal?style=for-the-badge)](https://opensource.org/licenses/MIT)

</div>

---

### 📌 Overview

**PRISMA** (Sistem Pengawasan Antibiotik Nasional) is a simulation platform designed to address **Antimicrobial Resistance (AMR)** in Indonesia. By combining **blockchain technology** with **SATUSEHAT** standards, it introduces transparency, immutability, and smart-contract verification to the national antibiotic supply chain and prescription dispensing workflow.

This simulator models a multi-role web application where pharmaceutical manufacturers, logistics distributors, doctors, and pharmacists interact with a distributed ledger to track antibiotics from factory production to patient dispensing.

---

### 🛡️ Core Pillars

#### 1. ⛓️ Immutable Ledger (On-Chain)
A simulation of a national, tamper-proof blockchain ledger. Every state modification—from batch production and logistics transfer to prescription creation and drug dispensing—is cryptographically chained using `previousHash` references, establishing an audit trail that cannot be modified retrospectively.

#### 2. 🔒 Privacy-Preserving Storage (Off-Chain)
To comply with medical privacy regulations, sensitive patient health records (such as names, NIKs, and clinical diagnoses) are kept off-chain. Instead, they are stored on a simulated decentralized storage network (IPFS/node local) and linked to the public ledger via secure cryptographic pointers (e.g., `IPFS-QmW2X9`). Only authorized entities (e.g., Doctors, Pharmacists) hold the keys to decrypt and resolve these pointers.

#### 3. 📶 Offline-First Synchronization
Designed for remote clinics and rural healthcare facilities with intermittent internet connectivity. Transactions can be queued locally when the system detects an offline state, maintaining clinical operations. Once connectivity is restored, the system auto-resolves and synchronizes local transactions to the main national ledger, recalculating the cryptographic chain securely.

#### 4. 📜 Smart Contract Verification
Preventing illicit double-spending of medical prescriptions. The dispenser module enforces a three-step smart contract:
1. **Digital Signature Verification** — confirming the physician's credentials.
2. **Double-Spending Verification** — ensuring the prescription ID has not been previously redeemed.
3. **Transaction Finalization** — locking the state to prevent future redemption.

---

### 👥 Simulation Roles

| Role | Responsibility | Action in Simulator |
| :--- | :--- | :--- |
| **🏭 Manufacturer** | Register antibiotic batches at source | Generate unique batch hashes, drug codes (DIN), and log initial quantities. |
| **🚚 Distributor** | Manage cold-chain & transport log | Update transit states and location metadata along the supply route. |
| **🩺 Doctor / Nakes** | Issue digital prescriptions | Encrypt patient identities off-chain and mint prescription blocks. |
| **🏪 Pharmacist** | Validate & dispense antibiotics | Scan and resolve prescription IDs, trigger smart contract validation, and execute dispensing. |
| **🔍 Auditor / Developer**| System health & ledger audit | Inspect full cryptographic payloads, block indices, and decode decrypted off-chain records. |

---

### ⚙️ Architecture & Tech Stack

The platform is designed as a modern, lightweight, client-side simulation app:
* **Frontend Library:** [React 18](https://react.dev/) (functional components with React Hooks)
* **Build Tool:** [Vite](https://vite.dev/) for sub-second hot module replacement
* **Programming Language:** [TypeScript](https://www.typescriptlang.org/) for robust static type checking
* **Styling:** [Tailwind CSS](https://tailwindcss.com/) for fluid, modern utility classes
* **Iconography:** [Lucide React](https://lucide.dev/) for crisp, scalable vectors
* **Cryptographic Engine:** Custom client-side string hashing algorithm simulating a blockchain miner and chain state ledger.

---

### 📂 Repository Structure

```
prisma-rdk-simulator/
├── src/
│   ├── PrismaAdvanced.tsx  # Core simulator logic, role dashboards, and blockchain engine
│   ├── main.jsx            # React application entrypoint
│   └── index.css           # Tailwind directives and custom fonts
├── index.html              # HTML shell
├── tailwind.config.js      # Styling configuration
├── vite.config.js          # Build configuration
└── package.json            # Application dependencies and script definitions
```

---

### 🚀 Getting Started

To spin up the simulator locally, follow these simple commands:

1. **Clone & Navigate:**
   ```bash
   git clone https://github.com/alchemist4real/prisma-rdk-simulator.git
   cd prisma-rdk-simulator
   ```

2. **Install Dependencies:**
   ```bash
   npm install
   ```

3. **Run Development Server:**
   ```bash
   npm run dev
   ```

4. **Build for Production:**
   ```bash
   npm run build
   ```

---

### 💡 Interactive Demo Controls

* **Toggle Online/Offline Mode:** Simulates connectivity failure to test local queue stacking and subsequent database synchronization.
* **Auto-Simulation Mode (Zap Button):** Toggles background bots simulating real-time batch productions and physician prescription minting.
* **Smart Contract Inspector:** Try dispensing the same prescription twice in the Pharmacist view to watch the smart contract automatically flag and reject double-spending attempts.
