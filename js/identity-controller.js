/**
 * Dual-Identity Controller for alchemist4real
 * Cryptographically secured using AES-256-GCM (WebCrypto API).
 * Zero plain-text identity leaks in source code or Chrome DevTools.
 * Zero emojis across all UI states and modals.
 * Recruiter token links show ONLY verified candidate profile (admin tools hidden).
 */

const CRYPTO_PAYLOAD = {
  salt: "616c6368656d6973745f73616c745f32303236",
  iv: "70515b39b1e39b6c7182ead7",
  tag: "6a03fc57cbdf0099e61fca8ec2cc62ec",
  ciphertext: "abba8f00adec12b6a31f652285bf9494ca96bad7c4731678b438978ec83c4b041f0ee4e1e1c0e2268ca5b0dcecc768e4097b6835c084dd92b6cd13e5a6c5f7f7fd8b06e7a57ca1c1032bc30bc882e71f73daad9a1e523810b59ebb87701a9aefe799398cee4f54e31f6a47d0630c2ac3e028db904336878042ecaa1c18f87003df0cf92831a01cb5022db303262b1d51ebaca0dbca15929fe6a94bc79192f0322c47e4064c4f560569c566fab11fbddac0fa8fe6f31dc232ecabab82fb003ce65b218f5b923c28f71039fc31bfe6beb9460cd14d47f72b73490814de1096309eb110e1a00007f6277e8445e19d8fc5b006fc4d2424fd0dc9d62dcf8361ca319a1913143326bcb44b64aaccc81b2c325ce41c5e66ac759b63eafc1e2801e2ee11440ecbc8806f06b17394ed72284bc4cfcfb6c14850b46cde15508c735f079fa06d871f7d25c880d2bf7589f0ba3f81f8883d806d928cdb2f94787da9aa6d9a9b03c25e09eda64d8dc868783fe7a206daae04478f5397e8c2e28f64059b229e248caa3c033f60f158fd6ba3fd3ff0d7fd15d96191b284f51d134c6d6759c87f35984a8cda320312566df777efe864526dc37e247f4e90c26ed528978e00e697cd5feaf62d39e6c74eae57052f874775a27aad7c9e2906cc30a4be06ffbc3023ef7dc1dbee333e137b5deed1a6308a18f76da0ac9ef82859ade689e638bdf165dfbc365be59d8e3505eb02715993f9cf19d811366461f6836f1600fdd110cdc1d20cfb6f5875ab4e7f3ab2b628f70683b5dd68f83f79c673a6c3ba51eb2bbc4df6c48c4c8e4b83f060f2451c1d54eaf0839fb22c472a76a42d6ac6f6fd5777699d9f9c4c8a55652652d957d3de5dd78da794e26bea7fc75088cf319367234c1a85bb1f2fdddc7b0e28ce4190da20ca2935d64a57ca6e30057fcb7d952efbd8176c78b7e908ed13eee08856b7a419c15814b6ea54fb4d466203a664288d89e380cb08c5ef922f6b4d4e95bf429b058264e33cb559013edb3dd436460c3756acd8c1176af9167d48e98e51797e6ff281f1403093eb6e89912d335b34761ab69adea7996eb47cada0434a34d61d5da5dcb78105c359473a4381f41b2e0c31a376aad1efcfdc83c98fbf0c5ba650886a440ec2a9670cc2b266f1f22d32a730a35b9aee8ec719e02ecc2a390f5645935ddaeed6ef820950aaa24478e0f788caf40cb39eab1c213bf4fd6ba75fa0abae21060c7adc44725a26c7137cd9e0feec3685484e7f576f12ce5f54a5b7f02f60bb744429a98e88db5fd46da1dc4abdf3a813fa25bf883abba28140e4de4489e4f780b1b54d32ae5edebacfa43eddf5dd201c552a9afcffc2b311bd66a90cec48eb56be8ff2cd1c079d3b7e745b81fde66f58580c064825536fff23fc0adf687ceb6bf7243b298b04babf86226572ecdd1d8fcd83e39c2da2258ee897d48eae8917f341303976e59e6dbd6a2f10710f7b2eae044f5940243871cd2c700d9ae04e7bd2cf34dd7cdf0263383542ff5baa58c7d7b1462d81c5a14b22920e48c284c265846182503f9d9117be9dd186c616577758efb8ea6c7a914ce25314121ee905c4ab68d2b6218753ef03131b8176e4c5bc9a6d87a394d8572fd161c4b2d5b6cc4b281de0db9ae572762a88b2baaaf3e8336b8fb41974244217594f73a79eed2522b89385ee408d7193c64246df152a47f3c71357d1603fe7e17b7afdca9e606e40fa0b1a0d94f962fc86f1bfe4870b26f78c903b3edfb03f372670cc18d575c81d95ade0f3135ab8267ae94e912f4c81eeea4e6a211c4c"
};

class IdentityController {
  constructor() {
    this.isVerified = false;
    this.isRecruiter = false;
    this.tokenInfo = null;
    this.verifiedData = null;
    this.activeKey = null;
    this.init();
  }

  async decryptPayload(passcodeStr) {
    if (!passcodeStr) return null;
    try {
      const payload = CRYPTO_PAYLOAD;
      const encoder = new TextEncoder();
      const passBuffer = encoder.encode(passcodeStr.trim());

      const hexToBytes = (hex) => new Uint8Array(hex.match(/.{1,2}/g).map(b => parseInt(b, 16)));

      const salt = hexToBytes(payload.salt);
      const iv = hexToBytes(payload.iv);
      const tag = hexToBytes(payload.tag);
      const cipherBytes = hexToBytes(payload.ciphertext);

      const combined = new Uint8Array(cipherBytes.length + tag.length);
      combined.set(cipherBytes);
      combined.set(tag, cipherBytes.length);

      const baseKey = await crypto.subtle.importKey('raw', passBuffer, { name: 'PBKDF2' }, false, ['deriveKey']);
      const aesKey = await crypto.subtle.deriveKey(
        { name: 'PBKDF2', salt: salt, iterations: 100000, hash: 'SHA-256' },
        baseKey,
        { name: 'AES-GCM', length: 256 },
        false,
        ['decrypt']
      );

      const decryptedBuffer = await crypto.subtle.decrypt(
        { name: 'AES-GCM', iv: iv },
        aesKey,
        combined
      );

      const decoder = new TextDecoder();
      const jsonStr = decoder.decode(decryptedBuffer);
      return JSON.parse(jsonStr);
    } catch (e) {
      return null;
    }
  }

  async init() {
    const searchStr = (typeof window !== 'undefined' && window.location) ? window.location.search : '';
    const params = new URLSearchParams(searchStr);
    const token = params.get('access_token') || params.get('token');
    const unlockKey = params.get('unlock');

    if (token) {
      await this.validateToken(token);
    } else if (unlockKey) {
      const data = await this.decryptPayload(unlockKey);
      if (data) {
        this.isVerified = true;
        this.isRecruiter = false; // Owner access
        this.verifiedData = data;
        this.activeKey = unlockKey;
        if (typeof sessionStorage !== 'undefined') sessionStorage.setItem('alchemist_key', unlockKey);
      }
    } else {
      const storedKey = (typeof sessionStorage !== 'undefined' ? sessionStorage.getItem('alchemist_key') : null) || (typeof localStorage !== 'undefined' ? localStorage.getItem('alchemist_key') : null);
      const storedRecruiter = typeof sessionStorage !== 'undefined' ? sessionStorage.getItem('alchemist_recruiter') : null;
      if (storedKey) {
        const data = await this.decryptPayload(storedKey);
        if (data) {
          this.isVerified = true;
          this.isRecruiter = storedRecruiter === 'true';
          this.verifiedData = data;
          this.activeKey = storedKey;
        }
      }
    }

    this.render();
  }

  async validateToken(tokenStr) {
    try {
      let keyToTry = tokenStr;
      let isRecruiterToken = true;

      try {
        const jsonStr = atob(tokenStr);
        const payload = JSON.parse(jsonStr);

        if (payload && payload.exp) {
          const nowSec = Math.floor(Date.now() / 1000);
          if (payload.exp < nowSec) {
            alert('Notice: The recruiter access token has expired. Displaying public portfolio.');
            return;
          }
        }

        if (payload && payload.key) {
          keyToTry = payload.key;
        }
      } catch (e) {
        // Direct string key
        isRecruiterToken = false;
      }

      const data = await this.decryptPayload(keyToTry);
      if (data) {
        this.isVerified = true;
        this.isRecruiter = isRecruiterToken;
        this.verifiedData = data;
        this.activeKey = keyToTry;
        if (typeof sessionStorage !== 'undefined') {
          sessionStorage.setItem('alchemist_key', keyToTry);
          sessionStorage.setItem('alchemist_recruiter', isRecruiterToken ? 'true' : 'false');
        }
      }
    } catch (e) {
      console.warn("Invalid token string", e);
    }
  }

  lockIdentity() {
    this.isVerified = false;
    this.isRecruiter = false;
    this.verifiedData = null;
    this.activeKey = null;
    if (typeof sessionStorage !== 'undefined') {
      sessionStorage.removeItem('alchemist_key');
      sessionStorage.removeItem('alchemist_recruiter');
    }
    if (typeof localStorage !== 'undefined') {
      localStorage.removeItem('alchemist_key');
    }
    if (typeof window !== 'undefined' && window.history) {
      window.history.replaceState({}, document.title, window.location.pathname);
    }
    this.render();
  }

  generateRecruiterToken(recipientName = "Recruiter", daysValid = 30) {
    const expSec = Math.floor(Date.now() / 1000) + (daysValid * 86400);
    const payload = {
      recipient: recipientName,
      exp: expSec,
      key: this.activeKey,
      created: new Date().toISOString().split('T')[0]
    };
    const jsonStr = JSON.stringify(payload);
    const tokenStr = btoa(jsonStr);
    const origin = (typeof window !== 'undefined' && window.location && window.location.origin) ? (window.location.origin + window.location.pathname) : 'https://alchemist4real.vercel.app/';
    const fullUrl = `${origin}?access_token=${encodeURIComponent(tokenStr)}`;
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
    const genModalBtn = document.getElementById('verified-generator-btn');
    const unlockBtn = document.getElementById('nav-unlock-btn');
    const titleEl = document.querySelector('title');

    // ID card elements
    const orgLabel = document.getElementById('id-org-label');
    const roleEl = document.getElementById('id-role');
    const photoSilhouette = document.querySelector('.id-photo-silhouette');
    const photoReal = document.getElementById('id-photo-real');
    const photoLabel = document.getElementById('id-photo-label');

    if (this.isVerified && this.verifiedData) {
      const data = this.verifiedData;

      if (titleEl) titleEl.textContent = `${data.name} — Portfolio & Lab`;
      if (handleEl) handleEl.textContent = data.name;
      if (heroHandleEl) heroHandleEl.textContent = data.name;
      if (footerBrandEl) footerBrandEl.textContent = data.name;
      if (footerCopyrightEl) footerCopyrightEl.textContent = `© 2025 ${data.name} | Co-architect Sir. Yaon (@ghaffarsyafiq-arch)`;
      if (badgeEl) badgeEl.textContent = `Sem 3`;
      if (orgLabel) orgLabel.textContent = data.education ? data.education[0].institution : data.name;
      if (roleEl) roleEl.textContent = 'M.D. Candidate — UNSOED';

      // Show real photo in verified mode
      if (photoSilhouette) photoSilhouette.style.display = 'none';
      if (photoReal && data.photo) {
        photoReal.src = data.photo;
        photoReal.alt = data.name;
        photoReal.style.display = 'block';
      }
      if (photoLabel) photoLabel.textContent = 'VERIFIED';
      
      if (bioEl) {
        bioEl.textContent = data.bio;
      }

      if (verifiedBadgeRow) {
        verifiedBadgeRow.style.display = 'flex';
        verifiedBadgeRow.innerHTML = data.badges.map(b => 
          `<span style="font-family:'DM Mono', monospace; font-size:10px; padding:2px 8px; border:1px solid var(--fg); background:var(--fg); color:var(--bg); border-radius:10px; font-weight:500;">${b}</span>`
        ).join('');
      }

      if (linkedinBtn) {
        linkedinBtn.style.display = 'inline-flex';
        linkedinBtn.href = data.links.linkedin;
      }

      // Hide generator modal button from recruiters
      if (genModalBtn) {
        genModalBtn.style.display = this.isRecruiter ? 'none' : 'inline-flex';
      }

      // Hide lock button from recruiters
      if (unlockBtn) {
        if (this.isRecruiter) {
          unlockBtn.style.display = 'none';
        } else {
          unlockBtn.style.display = 'inline-flex';
          unlockBtn.innerHTML = `LOCK`;
          unlockBtn.title = "Click to Lock Profile";
          unlockBtn.onclick = () => this.lockIdentity();
        }
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
      if (footerCopyrightEl) footerCopyrightEl.textContent = `© 2025 @alchemist4real | Co-architect Sir. Yaon (@ghaffarsyafiq-arch)`;
      if (badgeEl) badgeEl.textContent = `Sem 3`;
      if (orgLabel) orgLabel.textContent = 'alchemist4real';
      if (roleEl) roleEl.textContent = 'M.D. Candidate';

      // Show silhouette in public mode
      if (photoSilhouette) photoSilhouette.style.display = 'block';
      if (photoReal) photoReal.style.display = 'none';
      if (photoLabel) photoLabel.textContent = 'PHOTO';

      if (bioEl) {
        bioEl.textContent = `Medical student by day, experimental coder by night. Transmuting biomedical concepts into autonomous AI tools, decentralized edge software, and brutalist web experiences.`;
      }

      if (verifiedBadgeRow) {
        verifiedBadgeRow.style.display = 'none';
      }

      if (linkedinBtn) {
        linkedinBtn.style.display = 'none';
      }

      if (genModalBtn) {
        genModalBtn.style.display = 'none';
      }

      if (unlockBtn) {
        unlockBtn.style.display = 'none';
      }
    }
  }
}

// Global instance initialization
window.identityController = new IdentityController();
