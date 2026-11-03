const sharp = require('sharp');
const fs = require('fs');
const path = require('path');

const TARGET_DIRS = [
  path.join(__dirname, '..', 'quartz', 'static', 'images'),
  path.join(__dirname, '..', 'content', 'assets', 'images')
];

function getAllFiles(dir, allFilesList = []) {
  if (!fs.existsSync(dir)) return allFilesList;
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  for (const entry of entries) {
    const fullPath = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      getAllFiles(fullPath, allFilesList);
    } else if (entry.isFile()) {
      const ext = path.extname(entry.name).toLowerCase();
      if (['.jpg', '.jpeg', '.png'].includes(ext)) {
        allFilesList.push(fullPath);
      }
    }
  }
  return allFilesList;
}

async function optimizeImages() {
  let totalSavedBytes = 0;
  let optimizedCount = 0;

  for (const dir of TARGET_DIRS) {
    const files = getAllFiles(dir);
    console.log(`Scanning ${files.length} images in ${path.basename(dir)}...`);

    for (const file of files) {
      const stat = fs.statSync(file);
      // Optimize if file > 120 KB
      if (stat.size < 120 * 1024) continue;

      try {
        const ext = path.extname(file).toLowerCase();
        const inputBuffer = fs.readFileSync(file);
        let pipeline = sharp(inputBuffer).resize({ width: 1200, withoutEnlargement: true });

        let buffer;
        if (ext === '.jpg' || ext === '.jpeg') {
          buffer = await pipeline.jpeg({ quality: 80, mozjpeg: true }).toBuffer();
        } else if (ext === '.png') {
          buffer = await pipeline.png({ compressionLevel: 9, effort: 7 }).toBuffer();
        }

        if (buffer && buffer.length < stat.size) {
          const saved = stat.size - buffer.length;
          totalSavedBytes += saved;
          optimizedCount++;
          fs.writeFileSync(file, buffer);
          console.log(`[Optimized] ${path.basename(file)}: ${(stat.size/1024).toFixed(0)}KB -> ${(buffer.length/1024).toFixed(0)}KB (saved ${(saved/1024).toFixed(0)}KB)`);
        }
      } catch (err) {
        console.warn(`[Skip] ${path.basename(file)}: ${err.message}`);
      }
    }
  }

  console.log(`\nOptimization finished!`);
  console.log(`Optimized ${optimizedCount} images.`);
  console.log(`Total data saved: ${(totalSavedBytes / (1024 * 1024)).toFixed(2)} MB.`);
}

optimizeImages();
