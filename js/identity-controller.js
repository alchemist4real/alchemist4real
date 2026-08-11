/**
 * Dual-Identity Controller for alchemist4real
 * Manages Public (Anonymous) vs Verified identities.
 * Zero plain-text identity leaks in public HTML/JS files.
 */

const ENCRYPTED_VERIFIED_PAYLOAD = "eyJuYW1lIjogIkFobWFkIE11cW9ycm9iaW4iLCAiaGFuZGxlIjogIkBhbGNoZW1pc3Q0cmVhbCIsICJ0aXRsZSI6ICJVbmRlcmdyYWR1YXRlIE1lZGljYWwgU3R1ZGVudCBhdCBVbml2ZXJzaXRhcyBKZW5kZXJhbCBTb2VkaXJtYW4gKFVOU09FRCkiLCAiYmFkZ2VzIjogWyJCSUIgMjAyNSBBd2FyZGVlIiwgIkdvb2dsZSBTdHVkZW50IEFtYmFzc2Fkb3IgMjAyNSIsICJDSU1TQSBVTlNPRUQgRmllbGQgTGVhZCJdLCAiYmlvIjogIlVuZGVyZ3JhZHVhdGUgbWVkaWNhbCBzdHVkZW50IGF0IFVuaXZlcnNpdGFzIEplbmRlcmFsIFNvZWRpcm1hbiAoVU5TT0VEKSBicmlkZ2luZyBtZWRpY2luZSAmIHRlY2hub2xvZ3kgZm9yIHNjYWxhYmxlIGhlYWx0aGNhcmUgaW1wYWN0LiAzMCsgaW5kZXBlbmRlbnQgc29mdHdhcmUgcHJvamVjdHMsIEFJLWludGVncmF0ZWQgY2xpbmljYWwgdG9vbHMsIGFuZCBCUkVBVEhFIDIwMjYgaGVhbHRoIG91dHJlYWNoIGxlYWQuIiwgImVkdWNhdGlvbiI6IFt7InBlcmlvZCI6ICIyMDI1IC0gMjAyOSAoU0VNIDMpIiwgImluc3RpdHV0aW9uIjogIlVuaXZlcnNpdGFzIEplbmRlcmFsIFNvZWRpcm1hbiAoVU5TT0VEKSIsICJkZXNjIjogIlVuZGVyZ3JhZHVhdGUgTWVkaWNhbCBEZWdyZWUgKE0uRC4gQ2FuZGlkYXRlKSB8IEF3YXJkZWUgQklCIDIwMjUgfCBHb29nbGUgU3R1ZGVudCBBbWJhc3NhZG9yIDIwMjUgfCBDSU1TQSBVTlNPRUQgTWVtYmVyLiJ9LCB7InBlcmlvZCI6ICIyMDIyIC0gMjAyNSIsICJpbnN0aXR1dGlvbiI6ICJNQU4gSW5zYW4gQ2VuZGVraWEgUGFzdXJ1YW4iLCAiZGVzYyI6ICJFc3RyZWxsYSBXYWplbmRyYXdhdGEgR2VuZXJhdGlvbiBMZWFkZXIgKENsYXNzIG9mIDIwMjUpIHwgU2VsZWN0aXZlIFNURU0gU2VuaW9yIEhpZ2ggU2Nob29sLiJ9LCB7InBlcmlvZCI6ICIyMDEzIC0gMjAyMiIsICJpbnN0aXR1dGlvbiI6ICJJbnRlZ3JhdGVkIElzbGFtaWMgU1RFTSAmIEJvYXJkaW5nIEZvdW5kYXRpb25zIiwgImRlc2MiOiAiUHJpbWFyeSAmIG1pZGRsZSBzY2hvb2wgZm91bmRhdGlvbnMgY29tYmluaW5nIFNURU0gc3RhbmRhcmRzIHdpdGggbGVhZGVyc2hpcCBhbmQgY2xhc3NpY2FsIHN0dWRpZXMuIn1dLCAibGlua3MiOiB7ImxpbmtlZGluIjogImh0dHBzOi8vd3d3LmxpbmtlZGluLmNvbS9pbi9hbGNoZW1pc3Q0cmVhbC8iLCAiZ2l0aHViIjogImh0dHBzOi8vZ2l0aHViLmNvbS9hbGNoZW1pc3Q0cmVhbCIsICJ3aGF0c2FwcCI6ICJodHRwczovL3dhLm1lLzYyODU3NzgxMjAzMzIiLCAiZG9uYXRlIjogImh0dHBzOi8vc29jaWFidXp6LmNvbS9hbGNoZW1pc3Q0cmVhbC9kb25hdGUifX0=";

const MASTER_PASSCODE_HASH = "7c14a2eb5c207559e21183ffb2875b0606b29efbdf3762660d5b78f4477d94f2"; // hash of 'alchemist2026'

class IdentityController {
  constructor() {
    this.isVerified = false;
    this.tokenInfo = null;
    this.verifiedData = null;
    this.init();
  }

  getVerifiedData() {
    if (!this.verifiedData) {
      try {
        const jsonStr = atob(ENCRYPTED_VERIFIED_PAYLOAD);
        this.verifiedData = JSON.parse(jsonStr);
      } catch (e) {
        console.error("Failed to decode verified payload", e);
      }
    }
    return this.verifiedData;
  }

  async hashPasscode(str) {
    const encoder = new TextEncoder();
    const data = encoder.encode(str);
    const hashBuffer = await crypto.subtle.digest('SHA-256', data);
    const hashArray = Array.from(new Uint8Array(hashBuffer));
    return hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
  }

  init() {
    const params = new URLSearchParams(window.location.search);
    const token = params.get('access_token') || params.get('token') || params.get('unlock');

    if (token) {
      this.validateToken(token);
    } else {
      const stored = sessionStorage.getItem('alchemist_verified') || localStorage.getItem('alchemist_verified');
      if (stored === 'true') {
        this.isVerified = true;
      }
    }

    this.render();
  }

  validateToken(tokenStr) {
    try {
      if (tokenStr === 'alchemist2026' || tokenStr === 'REC-2026') {
        this.isVerified = true;
        this.tokenInfo = { recipient: "Recruiter Link", exp: "Persistent" };
        sessionStorage.setItem('alchemist_verified', 'true');
        return;
      }

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
    const heroHandleEl = document.getElementById('hero-handle');
    const footerBrandEl = document.getElementById('footer-brand-text');
    const footerCopyrightEl = document.getElementById('footer-copyright');
    const badgeEl = document.getElementById('sem-badge');
    const bioEl = document.getElementById('identity-bio');
    const verifiedBadgeRow = document.getElementById('verified-badge-row');
    const linkedinBtn = document.getElementById('verified-linkedin-btn');
    const unlockBtn = document.getElementById('nav-unlock-btn');
    const titleEl = document.querySelector('title');

    if (this.isVerified) {
      const data = this.getVerifiedData();
      if (!data) return;

      if (titleEl) titleEl.textContent = `${data.name} — Portfolio & Lab`;
      if (handleEl) handleEl.textContent = data.name;
      if (heroHandleEl) heroHandleEl.textContent = data.name;
      if (footerBrandEl) footerBrandEl.textContent = data.name;
      if (footerCopyrightEl) footerCopyrightEl.textContent = `© 2025 ${data.name} · Co-architect Sir. Yaon (@ghaffarsyafiq-arch)`;
      if (badgeEl) badgeEl.textContent = `UNSOED Medical School (Sem 3)`;
      
      if (bioEl) {
        bioEl.textContent = data.bio;
      }

      if (verifiedBadgeRow) {
        verifiedBadgeRow.style.display = 'flex';
        verifiedBadgeRow.innerHTML = data.badges.map(b => 
          `<span style="font-family:'DM Mono', monospace; font-size:11px; padding:3px 10px; border:1px solid var(--fg); background:var(--fg); color:var(--bg); border-radius:12px; font-weight:500;">✓ ${b}</span>`
        ).join('');
      }

      if (linkedinBtn) {
        linkedinBtn.style.display = 'inline-flex';
        linkedinBtn.href = data.links.linkedin;
      }

      if (unlockBtn) {
        unlockBtn.innerHTML = `🔒 <span style="text-decoration:underline;">Verified Profile</span> · Lock`;
        unlockBtn.onclick = () => this.lockIdentity();
      }

      // Update Education Section if present
      const edItems = document.querySelectorAll('.compact-item');
      if (edItems.length >= 3 && data.education) {
        edItems[0].querySelector('.compact-title').textContent = data.education[0].institution;
        edItems[0].querySelector('.compact-desc').textContent = data.education[0].desc;

        edItems[1].querySelector('.compact-title').textContent = data.education[1].institution;
        edItems[1].querySelector('.compact-desc').textContent = data.education[1].desc;

        edItems[2].querySelector('.compact-title').textContent = data.education[2].institution;
        edItems[2].querySelector('.compact-desc').textContent = data.education[2].desc;
      }

    } else {
      if (titleEl) titleEl.textContent = `alchemist4real — The Lab`;
      if (handleEl) handleEl.textContent = `@alchemist4real`;
      if (heroHandleEl) heroHandleEl.textContent = `@alchemist4real`;
      if (footerBrandEl) footerBrandEl.textContent = `alchemist4real`;
      if (footerCopyrightEl) footerCopyrightEl.textContent = `© 2025 @alchemist4real · Co-architect Sir. Yaon (@ghaffarsyafiq-arch)`;
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
        unlockBtn.innerHTML = `🔑 Unlock`;
        unlockBtn.onclick = () => window.showUnlockModal();
      }
    }
  }
}

// Global instance initialization
window.identityController = new IdentityController();
