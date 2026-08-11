const fs = require('fs');
const crypto = require('crypto');

const privB64 = fs.readFileSync('assets/priv_b64.txt', 'utf8').trim();

const fullPayload = {
  name: 'Ahmad Muqorrobin',
  role: 'Undergraduate Medical Student',
  status: 'BIB 2025 Awardee -- Sem 3',
  bio: 'Undergraduate Medical Student at Universitas Jenderal Soedirman (UNSOED) | Awardee BIB 2025 | Google Student Ambassador 2025 | CIMSA UNSOED Field Lead. Transmuting biomedical research and autonomous AI systems.',
  badges: ['BIB 2025 Awardee', 'Google Student Ambassador 2025', 'CIMSA UNSOED Field Lead'],
  links: {
    linkedin: 'https://www.linkedin.com/in/alchemist4real/'
  },
  education: [
    {
      institution: 'Universitas Jenderal Soedirman (UNSOED)',
      degree: 'Undergraduate Medical Student (M.D. Candidate)',
      period: 'Jul 2025 – Aug 2029',
      desc: 'Pursuing M.D. degree. Active in biomedical research, clinical skills development, and CIMSA community health outreach.'
    },
    {
      institution: 'MAN Insan Cendekia Pasuruan',
      degree: 'High School Diploma (Estrella Wajendrawata Generation Lead)',
      period: 'Jul 2022 – Jun 2025',
      desc: 'Leader of Class of 2025 (Estrella Wajendrawata). Specialized in natural sciences and academic competitions.'
    },
    {
      institution: 'BIB 2025 Awardee & Google Ambassador',
      degree: 'National Honors & Tech Leadership',
      period: '2025 – Present',
      desc: 'Awardee Beasiswa Indonesia Bangkit 2025 and Google Student Ambassador 2025 representing UNSOED.'
    }
  ],
  photo: privB64
};

const jsonStr = JSON.stringify(fullPayload);

// PBKDF2 derive key from 'alchemist2026'
const salt = Buffer.from('alchemist_salt_2026', 'utf8');
const pass = Buffer.from('alchemist2026', 'utf8');
const key = crypto.pbkdf2Sync(pass, salt, 100000, 32, 'sha256');

const iv = crypto.randomBytes(12);
const cipher = crypto.createCipheriv('aes-256-gcm', key, iv);
let encrypted = cipher.update(jsonStr, 'utf8');
encrypted = Buffer.concat([encrypted, cipher.final()]);
const tag = cipher.getAuthTag();

const code = `const CRYPTO_PAYLOAD = {
  salt: "${salt.toString('hex')}",
  iv: "${iv.toString('hex')}",
  tag: "${tag.toString('hex')}",
  ciphertext: "${encrypted.toString('hex')}"
};`;

fs.writeFileSync('assets/crypto_payload.js', code, 'utf8');
console.log('Encrypted payload successfully written to assets/crypto_payload.js');
