const fs = require('fs');
const sharp = require('sharp');

let svg = fs.readFileSync('quartz/static/images/photos/logo-catania-fc.svg', 'utf8');
// Adjust viewBox to square: -150 0 900 900
svg = svg.replace('viewBox="0.00 0.00 600.00 900.00"', 'viewBox="-150 0 900 900"');
fs.writeFileSync('quartz/static/favicon.svg', svg, 'utf8');

sharp(Buffer.from(svg))
  .resize(512, 512)
  .png()
  .toFile('quartz/static/icon.png')
  .then(info => {
    console.log('Generated quartz/static/icon.png (512x512):', info);
    return sharp(Buffer.from(svg)).resize(48, 48).toFormat('png').toFile('public/favicon.ico');
  })
  .then(info => console.log('Generated public/favicon.ico:', info))
  .catch(err => console.error(err));
