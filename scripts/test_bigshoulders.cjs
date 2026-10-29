const fs = require('fs');
const sharp = require('sharp');

const fontBase64 = fs.readFileSync('quartz/static/fonts/big-shoulders-display-latin-11.woff2').toString('base64');

// 1. Opzione A: Bordo nero, fondo bianco, W nera, C rossa, C azzurra con Big Shoulders Display
const svgA = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
  <defs>
    <style>
      @font-face {
        font-family: 'Big Shoulders Display';
        font-style: normal;
        font-weight: 900;
        src: url(data:font/woff2;charset=utf-8;base64,${fontBase64}) format('woff2');
      }
      .wcc-letter {
        font-family: 'Big Shoulders Display', Impact, sans-serif;
        font-weight: 900;
        text-anchor: middle;
        dominant-baseline: central;
      }
    </style>
  </defs>
  <rect x="28" y="76" width="456" height="360" rx="32" fill="#ffffff" stroke="#111111" stroke-width="44" />
  <g font-size="285" class="wcc-letter">
    <text x="145" y="250" fill="#111111">W</text>
    <text x="285" y="250" fill="#d11317">C</text>
    <text x="395" y="250" fill="#0055a5">C</text>
  </g>
</svg>`;

// 2. Opzione B: Sfondo nero solido, W bianca, C rossa, C azzurra con Big Shoulders Display
const svgB = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
  <defs>
    <style>
      @font-face {
        font-family: 'Big Shoulders Display';
        font-style: normal;
        font-weight: 900;
        src: url(data:font/woff2;charset=utf-8;base64,${fontBase64}) format('woff2');
      }
      .wcc-letter {
        font-family: 'Big Shoulders Display', Impact, sans-serif;
        font-weight: 900;
        text-anchor: middle;
        dominant-baseline: central;
      }
    </style>
  </defs>
  <rect x="28" y="76" width="456" height="360" rx="32" fill="#111111" stroke="#333333" stroke-width="16" />
  <g font-size="285" class="wcc-letter">
    <text x="145" y="250" fill="#ffffff">W</text>
    <text x="285" y="250" fill="#d11317">C</text>
    <text x="395" y="250" fill="#0cb2d9">C</text>
  </g>
</svg>`;

fs.writeFileSync('quartz/static/favicon_bs_a.svg', svgA);
fs.writeFileSync('quartz/static/favicon_bs_b.svg', svgB);

Promise.all([
  sharp(Buffer.from(svgA)).resize(512, 512).png().toFile('quartz/static/favicon_bs_a.png'),
  sharp(Buffer.from(svgB)).resize(512, 512).png().toFile('quartz/static/favicon_bs_b.png'),
]).then(() => {
  console.log('Generated Big Shoulders Display favicons A & B!');
});
