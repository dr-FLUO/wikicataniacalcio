const fs = require('fs');
const sharp = require('sharp');

// 1. Design A: Bordo rettangolare nero netto, fondo bianco, W (nero), C (rosso), C (azzurro)
// Ispirato esattamente al box editoriale brutalista del brand
const svgA = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
  <rect x="24" y="64" width="464" height="384" rx="28" fill="#ffffff" stroke="#111111" stroke-width="36" />
  <g font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Arial Black', Impact, sans-serif" font-weight="900" font-size="210" letter-spacing="-4">
    <text x="68" y="330" fill="#111111">W</text>
    <text x="255" y="330" fill="#d11317">C</text>
    <text x="368" y="330" fill="#0cb2d9">C</text>
  </g>
</svg>`;

// 2. Design B: Sfondo nero solido, con W in riquadro bianco o contrastata
// E se il rettangolo nero ha W bianca, C rossa, C azzurra?
const svgB = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
  <rect x="24" y="64" width="464" height="384" rx="28" fill="#111111" stroke="#333333" stroke-width="12" />
  <g font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Arial Black', Impact, sans-serif" font-weight="900" font-size="210" letter-spacing="-4">
    <text x="68" y="330" fill="#ffffff">W</text>
    <text x="255" y="330" fill="#d11317">C</text>
    <text x="368" y="330" fill="#0cb2d9">C</text>
  </g>
</svg>`;

// 3. Design C: Badge split orizzontale/verticale ispirato al split-badge del sito
// Rettangolo nero di base con tab W nera su bianco, C rossa su rosso/nero, C azzurra su azzurro
const svgC = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
  <rect x="24" y="64" width="464" height="384" rx="28" fill="#111111" />
  <rect x="36" y="76" width="140" height="360" rx="16" fill="#ffffff" />
  <g font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Arial Black', Impact, sans-serif" font-weight="900" font-size="210">
    <text x="56" y="330" fill="#111111">W</text>
    <text x="240" y="330" fill="#d11317">C</text>
    <text x="360" y="330" fill="#0cb2d9">C</text>
  </g>
</svg>`;

fs.writeFileSync('quartz/static/favicon_a.svg', svgA);
fs.writeFileSync('quartz/static/favicon_b.svg', svgB);
fs.writeFileSync('quartz/static/favicon_c.svg', svgC);

Promise.all([
  sharp(Buffer.from(svgA)).resize(512, 512).png().toFile('quartz/static/favicon_a.png'),
  sharp(Buffer.from(svgB)).resize(512, 512).png().toFile('quartz/static/favicon_b.png'),
  sharp(Buffer.from(svgC)).resize(512, 512).png().toFile('quartz/static/favicon_c.png'),
]).then(() => console.log('Generated favicons A, B, C successfully!'));
