/**
 * Inbox Scanner & Assistant Helper
 * Scansiona la cartella inbox-immagini, calcola gli hash MD5, confronta con l'archivio
 * esistente per prevenire duplicati e prepara la scheda di catalogazione.
 */

const fs = require("fs");
const path = require("path");
const crypto = require("crypto");

const inboxDir = path.join(__dirname, "../inbox-immagini");
const assetsDir = path.join(__dirname, "../content/assets/images");

function getHash(filePath) {
  const buf = fs.readFileSync(filePath);
  return crypto.createHash("md5").update(buf).digest("hex");
}

// 1. Mappiamo tutto l'archivio esistente
console.log("🔍 Mappatura dell'archivio immagini esistente...");
const existingHashes = new Map();

function scanExisting(dir) {
  if (!fs.existsSync(dir)) return;
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      scanExisting(full);
    } else if (/\.(jpg|jpeg|png|webp|gif|svg)$/i.test(entry.name)) {
      const hash = getHash(full);
      const rel = path.relative(path.join(__dirname, ".."), full).replace(/\\/g, "/");
      if (!existingHashes.has(hash)) existingHashes.set(hash, []);
      existingHashes.get(hash).push(rel);
    }
  }
}
scanExisting(assetsDir);

// 2. Scansioniamo l'inbox
const validExtensions = /\.(jpg|jpeg|png|webp|gif)$/i;
const filesInInbox = fs.existsSync(inboxDir) 
  ? fs.readdirSync(inboxDir).filter(f => validExtensions.test(f) && f !== "README.md")
  : [];

console.log(`\n======================================================`);
console.log(`📦 INBOX IMMAGINI — File in attesa di elaborazione: ${filesInInbox.length}`);
console.log(`======================================================\n`);

if (filesInInbox.length === 0) {
  console.log("ℹ️ Nessun file presente in 'inbox-immagini/'.");
  console.log("👉 Trascina qui dentro le tue foto e richiedimi di elaborarle!");
  process.exit(0);
}

filesInInbox.forEach((fileName, index) => {
  const fullPath = path.join(inboxDir, fileName);
  const stat = fs.statSync(fullPath);
  const hash = getHash(fullPath);
  const sizeKb = (stat.size / 1024).toFixed(1);
  const isDupe = existingHashes.has(hash);

  console.log(`[#${index + 1}] 📄 ${fileName}`);
  console.log(`    Dimensioni: ${sizeKb} KB | Hash: ${hash.slice(0, 10)}`);
  if (isDupe) {
    console.log(`    ⚠️ ATTENZIONE: Questo file è GIÀ PRESENTE nell'archivio:`);
    existingHashes.get(hash).forEach(p => console.log(`       -> ${p}`));
  } else {
    console.log(`    ✅ File NUOVO (nessun duplicato rilevato nell'archivio).`);
  }
  console.log("");
});
