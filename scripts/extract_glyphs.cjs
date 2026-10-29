const fs = require('fs');
const opentype = require('opentype.js');
const sharp = require('sharp');

const buffer = fs.readFileSync('quartz/static/fonts/BigShouldersDisplay-900.ttf');
const font = opentype.parse(buffer.buffer.slice(buffer.byteOffset, buffer.byteOffset + buffer.byteLength));

const glyphW = font.charToGlyph('W');
const glyphC = font.charToGlyph('C');

const fontSize = 240;
const baselineY = 354;

// Coordinate calcolate per centratura ottica millimetrica
const xW = 46;
const xC1 = 238;
const xC2 = 348;

const pathW = glyphW.getPath(xW, baselineY, fontSize);
const pathC1 = glyphC.getPath(xC1, baselineY, fontSize);
const pathC2 = glyphC.getPath(xC2, baselineY, fontSize);

const dW = pathW.toPathData(2);
const dC1 = pathC1.toPathData(2);
const dC2 = pathC2.toPathData(2);

// Rossi e azzurri ufficiali Catania
const RED = "#d11317";
const BLUE_DARK = "#0055a5";
const BLUE_CYAN = "#0cb2d9";
const BLACK = "#111111";

// OPZIONE 1: Cornice rettangolare nera (brutalista), fondo bianco, W nera, C rossa, C azzurra
const svg1 = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
  <rect x="20" y="86" width="472" height="340" rx="44" fill="#ffffff" stroke="${BLACK}" stroke-width="40" stroke-linejoin="round" />
  <path d="${dW}" fill="${BLACK}" />
  <path d="${dC1}" fill="${RED}" />
  <path d="${dC2}" fill="${BLUE_DARK}" />
</svg>`;

// OPZIONE 2: Badge quadrato arrotondato con bordo nero spesso, fondo bianco, W nera, C rossa, C azzurra
const svg2 = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
  <rect x="24" y="24" width="464" height="464" rx="90" fill="#ffffff" stroke="${BLACK}" stroke-width="44" stroke-linejoin="round" />
  <path d="${dW}" fill="${BLACK}" />
  <path d="${dC1}" fill="${RED}" />
  <path d="${dC2}" fill="${BLUE_DARK}" />
</svg>`;

// OPZIONE 3: Rettangolo nero pieno, W bianca ad altissima leggibilità, C rossa, C azzurro vivace
const svg3 = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
  <rect x="20" y="86" width="472" height="340" rx="44" fill="${BLACK}" stroke="#333333" stroke-width="8" />
  <path d="${dW}" fill="#ffffff" />
  <path d="${dC1}" fill="${RED}" />
  <path d="${dC2}" fill="${BLUE_CYAN}" />
</svg>`;

// OPZIONE 4: Rettangolo nero pieno, W nera con bordo bianco netto, C rossa, C azzurro vivace
const svg4 = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
  <rect x="20" y="86" width="472" height="340" rx="44" fill="${BLACK}" stroke="#333333" stroke-width="8" />
  <path d="${dW}" fill="${BLACK}" stroke="#ffffff" stroke-width="14" stroke-linejoin="round" />
  <path d="${dC1}" fill="${RED}" />
  <path d="${dC2}" fill="${BLUE_CYAN}" />
</svg>`;

const brainDir = 'C:/Users/sim0n/.gemini/antigravity/brain/ab57b6c7-4214-45ec-97bd-6ac4c09dfd66';

fs.writeFileSync('quartz/static/favicon_opt1.svg', svg1, 'utf8');
fs.writeFileSync('quartz/static/favicon_opt2.svg', svg2, 'utf8');
fs.writeFileSync('quartz/static/favicon_opt3.svg', svg3, 'utf8');
fs.writeFileSync('quartz/static/favicon_opt4.svg', svg4, 'utf8');

Promise.all([
  sharp(Buffer.from(svg1)).resize(512, 512).png().toFile(`${brainDir}/favicon_opt1.png`),
  sharp(Buffer.from(svg2)).resize(512, 512).png().toFile(`${brainDir}/favicon_opt2.png`),
  sharp(Buffer.from(svg3)).resize(512, 512).png().toFile(`${brainDir}/favicon_opt3.png`),
  sharp(Buffer.from(svg4)).resize(512, 512).png().toFile(`${brainDir}/favicon_opt4.png`),
]).then(() => {
  console.log('Optically centered favicons 1, 2, 3, 4 generated successfully!');
}).catch(console.error);
