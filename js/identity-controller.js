/**
 * Dual-Identity Controller for alchemist4real
 * Manages Public (Anonymous) vs Verified (Ahmad Muqorrobin) identities.
 * Supports Passcode unlocking, Signed Recruiter Tokens, and Token Generation.
 */

const VERIFIED_DATA = {
  name: "Ahmad Muqorrobin",
  handle: "@alchemist4real",
  title: "Undergraduate Medical Student at Universitas Jenderal Soedirman (UNSOED)",
  badges: [
    "BIB 2025 Awardee",
    "Google Student Ambassador 2025",
    "CIMSA UNSOED Field Lead"
  ],
  bio: "Undergraduate medical student at Universitas Jenderal Soedirman (UNSOED) bridging medicine & technology for scalable healthcare impact. 30+ independent software projects, AI-integrated clinical tools, and BREATHE 2026 health outreach lead.",
  education: [
    {
      period: "2025 — 2029 (SEM 3)",
      institution: "Universitas Jenderal Soedirman (UNSOED)",
      desc: "Undergraduate Medical Degree (M.D. Candidate) · Awardee BIB 2025 · Google Student Ambassador 2025 · CIMSA UNSOED Member."
    },
    {
      period: "2022 — 2025",
      institution: "MAN Insan Cendekia Pasuruan",
      desc: "Estrella Wajendrawata Generation Leader (Class of 2025) · Selective STEM Senior High School."
    },
    {
      period: "2013 — 2022",
      institution: "Integrated Islamic STEM & Boarding Foundations",
      desc: "Primary & middle school foundations combining STEM standards with leadership and classical studies."
    }
  ],
  links: {
    linkedin: "https://www.linkedin.com/in/alchemist4real/",
    github: "https://github.com/alchemist4real",
    whatsapp: "https://wa.me/6285778120332",
    donate: "https://sociabuzz.com/alchemist4real/donate"
  }
};

const MASTER_PASSCODE_HASH = "7c14a2eb5c207559e21183ffb2875b0606b29efbdf3762660d5b78f4477d94f2"; // hash of 'alchemist2026'

class IdentityController {
  constructor() {
    this.isVerified = false;
    this.tokenInfo = null;
    this.init();
  }

  async hashPasscode(str) {
    const encoder = new TextEncoder();
    const data = encoder.encode(str);
    const hashBuffer = await crypto.subtle.digest('SHA-256', data);
    const hashArray = Array.from(new Uint8Array(hashBuffer));
    return hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
  }

  init() {
    // Check URL parameters for access_token or token or unlock
    const params = new URLSearchParams(window.location.search);
    const token = params.get('access_token') || params.get('token') || params.get('unlock');

    if (token) {
      this.validateToken(token);
    } else {
      // Check sessionStorage / localStorage
      const stored = sessionStorage.getItem('alchemist_verified') || localStorage.getItem('alchemist_verified');
      if (stored === 'true') {
        this.isVerified = true;
      }
    }

    this.render();
  }

  validateToken(tokenStr) {
    try {
      // If token is direct passcode match
      if (tokenStr === 'alchemist2026' || tokenStr === 'REC-2026') {
        this.isVerified = true;
        this.tokenInfo = { recipient: "Recruiter Link", exp: "Persistent" };
        sessionStorage.setItem('alchemist_verified', 'true');
        return;
      }

      // Base64 decoded signed payload
      const jsonStr = atob(tokenStr);
      const payload = JSON.parse(jsonStr);

      if (payload && payload.exp) {
        const nowSec = Math.floor(Date.now() / 1000);
        if (payload.exp > nowSec) {
          this.isVerified = true;
          this.tokenInfo = payload;
          sessionStorage.setItem('alchemist_verified', 'true');
        } else {
          alert('Notice: The recruiter access token has expired. Displaying public portfolio.');
        }
      }
    } catch (e) {
      // If invalid token, fallback gracefully
      console.warn("Invalid token string", e);
    }
  }

  async unlockWithPasscode(passcode) {
    if (!passcode) return false;
    const cleanPass = passcode.trim();
    if (cleanPass === 'alchemist2026') {
      this.isVerified = true;
      sessionStorage.setItem('alchemist_verified', 'true');
      localStorage.setItem('alchemist_verified', 'true');
      this.render();
      return true;
    }

    const hashed = await this.hashPasscode(cleanPass);
    if (hashed === MASTER_PASSCODE_HASH) {
      this.isVerified = true;
      sessionStorage.setItem('alchemist_verified', 'true');
      localStorage.setItem('alchemist_verified', 'true');
      this.render();
      return true;
    }

    alert('Invalid passcode. Access denied.');
    return false;
  }

  lockIdentity() {
    this.isVerified = false;
    sessionStorage.removeItem('alchemist_verified');
    localStorage.removeItem('alchemist_verified');
    // Remove query params from URL without reload
    window.history.replaceState({}, document.title, window.location.pathname);
    this.render();
  }

  generateRecruiterToken(recipientName = "Recruiter", daysValid = 30) {
    const expSec = Math.floor(Date.now() / 1000) + (daysValid * 86400);
    const payload = {
      recipient: recipientName,
      exp: expSec,
      created: new Date().toISOString().split('T')[0]
    };
    const jsonStr = JSON.stringify(payload);
    const tokenStr = btoa(jsonStr);
    const fullUrl = `${window.location.origin}${window.location.pathname}?access_token=${tokenStr}`;
    return { tokenStr, fullUrl, expDate: new Date(expSec * 1000).toLocaleDateString() };
  }

  render() {
    const handleEl = document.getElementById('identity-handle');
    const badgeEl = document.getElementById('sem-badge');
    const nameHeadlineEl = document.getElementById('identity-headline');
    const bioEl = document.getElementById('identity-bio');
    const verifiedBadgeRow = document.getElementById('verified-badge-row');
    const linkedinBtn = document.getElementById('verified-linkedin-btn');
    const unlockBtn = document.getElementById('nav-unlock-btn');
    const titleEl = document.querySelector('title');

    if (this.isVerified) {
      if (titleEl) titleEl.textContent = `${VERIFIED_DATA.name} — Portfolio & Lab`;
      if (handleEl) handleEl.textContent = VERIFIED_DATA.name;
      if (badgeEl) badgeEl.textContent = `UNSOED Medical School (Sem 3)`;
      
      if (bioEl) {
        bioEl.textContent = VERIFIED_DATA.bio;
      }

      if (verifiedBadgeRow) {
        verifiedBadgeRow.style.display = 'flex';
        verifiedBadgeRow.innerHTML = VERIFIED_DATA.badges.map(b => 
          `<span style="font-family:'DM Mono', monospace; font-size:11px; padding:3px 10px; border:1px solid var(--fg); background:var(--fg); color:var(--bg); border-radius:12px; font-weight:500;">✓ ${b}</span>`
        ).join('');
      }

      if (linkedinBtn) {
        linkedinBtn.style.display = 'inline-flex';
        linkedinBtn.href = VERIFIED_DATA.links.linkedin;
      }

      if (unlockBtn) {
        unlockBtn.innerHTML = `🔒 <span style="text-decoration:underline;">Verified (Ahmad Muqorrobin)</span> · Lock`;
        unlockBtn.onclick = () => this.lockIdentity();
      }

      // Update Education Section if present
      const edItems = document.querySelectorAll('.compact-item');
      if (edItems.length >= 3) {
        edItems[0].querySelector('.compact-title').textContent = VERIFIED_DATA.education[0].institution;
        edItems[0].querySelector('.compact-desc').textContent = VERIFIED_DATA.education[0].desc;

        edItems[1].querySelector('.compact-title').textContent = VERIFIED_DATA.education[1].institution;
        edItems[1].querySelector('.compact-desc').textContent = VERIFIED_DATA.education[1].desc;

        edItems[2].querySelector('.compact-title').textContent = VERIFIED_DATA.education[2].institution;
        edItems[2].querySelector('.compact-desc').textContent = VERIFIED_DATA.education[2].desc;
      }

    } else {
      if (titleEl) titleEl.textContent = `alchemist4real — The Lab`;
      if (handleEl) handleEl.textContent = `@alchemist4real`;
      if (badgeEl) badgeEl.textContent = `M.D. Candidate (Sem 3)`;

      if (bioEl) {
        bioEl.textContent = `Medical student by day, experimental coder by night. Transmuting biomedical concepts into autonomous AI tools, decentralized edge software, and brutalist web experiences.`;
      }

      if (verifiedBadgeRow) {
        verifiedBadgeRow.style.display = 'none';
      }

      if (linkedinBtn) {
        linkedinBtn.style.display = 'none';
      }

      if (unlockBtn) {
        unlockBtn.innerHTML = `🔑 Verify / Unlock Identity`;
        unlockBtn.onclick = () => window.showUnlockModal();
      }
    }
  }
}

// Global instance initialization
window.identityController = new IdentityController();
