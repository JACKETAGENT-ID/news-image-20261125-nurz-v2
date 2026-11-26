// Entry program for make.fun news-image-20261125 (nurz v2).
// Copies the pre-drawn entry.png (1024x1024, drawn by gen.py) next to this
// script into the output directory. Node 22, standard library only.
import { copyFileSync, mkdirSync, readFileSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const scriptDir = dirname(fileURLToPath(import.meta.url));
const src = join(scriptDir, "entry.png");

// Validate the PNG before copying: signature, dimensions, size cap.
const bytes = readFileSync(src);
const PNG_SIG = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
if (!bytes.subarray(0, 8).equals(PNG_SIG)) throw new Error("not a PNG");
const width = bytes.readUInt32BE(16);
const height = bytes.readUInt32BE(20);
if (width > 1024 || height > 1024) {
  throw new Error(`image too large: ${width}x${height}`);
}
if (statSync(src).size > 1048576) throw new Error("image over 1 MiB");

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });
copyFileSync(src, join(outDir, "entry.png"));
console.log(`wrote ${width}x${height} entry.png to`, outDir);
