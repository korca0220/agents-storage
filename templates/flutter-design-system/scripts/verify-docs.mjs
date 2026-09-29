// 디자인 시스템 패키지 정합성 검사 — 패키지 루트에서 `node scripts/verify-docs.mjs`.
//
// 1. Markdown 로컬 링크가 실제 파일을 가리키는가
// 2. 치환되지 않은 placeholder(`{{name}}`)가 남아 있지 않은가
// 3. docs/components/NN-*.md 와 components/00-INDEX.md 의 문서 칸이 서로 빠짐없이 대응하는가
// 4. INDEX에서 ✅ 인 행의 코드 폴더가 실제로 있는가
// 5. lib/src 의 public 파일이 배럴에서 export 되는가 (primitive 컬러·internal/·part 파일 제외)
// 6. test/semantics/coverage_matrix_test.dart 의 분류 수가 컴포넌트 문서 수와 같은가
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const ignored = new Set(['.dart_tool', 'build', '.git', 'node_modules', 'ios', 'android', 'macos', 'web', 'linux', 'windows']);
const textExtensions = new Set(['.md', '.dart', '.yaml', '.yml', '.json', '.mjs']);
const failures = [];

const rel = (file) => path.relative(root, file);
const read = (file) => fs.readFileSync(file, 'utf8');

function walk(directory, visit) {
  if (!fs.existsSync(directory)) return;
  for (const entry of fs.readdirSync(directory, { withFileTypes: true })) {
    if (ignored.has(entry.name)) continue;
    const entryPath = path.join(directory, entry.name);
    if (entry.isDirectory()) walk(entryPath, visit);
    else visit(entryPath);
  }
}

const files = [];
walk(root, (file) => files.push(file));

// 1. 로컬 링크
const linkPattern = /!?\[[^\]]*\]\((?:<([^>]+)>|([^ )]+))(?:\s+[^)]*)?\)/g;
for (const file of files.filter((f) => f.endsWith('.md'))) {
  const content = read(file).replace(/```[\s\S]*?```/g, '');
  for (const match of content.matchAll(linkPattern)) {
    const target = (match[1] ?? match[2] ?? '').split('#')[0];
    if (!target || /^(https?:|mailto:|tel:|data:)/.test(target) || target.includes('{{')) continue;
    if (!fs.existsSync(path.resolve(path.dirname(file), decodeURIComponent(target)))) {
      failures.push(`[link] ${rel(file)} -> ${target}`);
    }
  }
}

// 2. 잔여 placeholder — 템플릿 안내 파일(TEMPLATE.md)은 인스턴스화 때 지운다
for (const file of files.filter((f) => textExtensions.has(path.extname(f)) && path.basename(f) !== 'TEMPLATE.md')) {
  if (rel(file) === path.join('scripts', 'verify-docs.mjs')) continue;
  const names = new Set([...read(file).matchAll(/\{\{([A-Za-z_]+)\}\}/g)].map((m) => m[1]));
  if (names.size > 0) failures.push(`[placeholder] ${rel(file)}: ${[...names].join(', ')}`);
}
for (const file of files) {
  if (rel(file).includes('{{')) failures.push(`[placeholder] 경로 이름: ${rel(file)}`);
}

// 3·4. 컴포넌트 문서 ↔ INDEX
const componentsDir = path.join(root, 'docs', 'components');
const componentDocs = fs.existsSync(componentsDir)
  ? fs.readdirSync(componentsDir).filter((name) => /^\d{2}-.+\.md$/.test(name) && !name.startsWith('00-'))
  : [];
const indexPath = path.join(componentsDir, '00-INDEX.md');
if (fs.existsSync(indexPath)) {
  const rows = read(indexPath)
    .split('\n')
    .filter((line) => /^\|\s*\d{2}\s*\|/.test(line))
    .map((line) => line.split('|').map((cell) => cell.trim()));
  const indexedDocs = new Set();
  for (const cells of rows) {
    const docCell = cells.find((cell) => /\d{2}-[^`\s]+\.md/.test(cell)) ?? '';
    const doc = docCell.match(/\d{2}-[^`\s)\]]+\.md/)?.[0];
    if (!doc) {
      failures.push(`[index] 문서 칸을 읽을 수 없는 행: ${cells.join(' | ')}`);
      continue;
    }
    indexedDocs.add(doc);
    if (!componentDocs.includes(doc)) failures.push(`[index] INDEX에 있지만 문서가 없다: ${doc}`);
    if (cells.some((cell) => cell.startsWith('✅'))) {
      for (const folder of cells.join(' ').match(/src\/components\/[a-z0-9_]+\//g) ?? []) {
        if (!fs.existsSync(path.join(root, 'lib', folder))) failures.push(`[index] ✅인데 코드 폴더가 없다: ${doc} -> lib/${folder}`);
      }
    }
  }
  for (const doc of componentDocs) {
    if (!indexedDocs.has(doc)) failures.push(`[index] 문서가 INDEX에 없다: ${doc}`);
  }
}

// 5. 배럴 export
const libDir = path.join(root, 'lib');
const barrel = fs.existsSync(libDir)
  ? fs.readdirSync(libDir).find((name) => name.endsWith('.dart'))
  : undefined;
if (barrel) {
  const barrelContent = read(path.join(libDir, barrel));
  const exported = new Set([...barrelContent.matchAll(/^export\s+'([^']+)'/gm)].map((m) => m[1]));
  walk(path.join(libDir, 'src'), (file) => {
    if (!file.endsWith('.dart')) return;
    const relative = path.relative(libDir, file).split(path.sep).join('/');
    if (relative.includes('/internal/') || /_primitive_colors\.dart$/.test(relative)) return;
    if (/^part of\b/m.test(read(file))) return;
    if (!exported.has(relative)) failures.push(`[export] 배럴(${barrel})에 없다: lib/${relative}`);
  });
}

// 6. Semantics 커버리지 매트릭스
const matrixPath = path.join(root, 'test', 'semantics', 'coverage_matrix_test.dart');
if (fs.existsSync(matrixPath)) {
  const classified = [...read(matrixPath).matchAll(/^\s*(\d+):\s*_SemanticsDisposition\.\w+/gm)].length;
  if (classified !== componentDocs.length) {
    failures.push(`[semantics] 커버리지 매트릭스 ${classified}개 ≠ 컴포넌트 문서 ${componentDocs.length}개`);
  }
}

if (failures.length > 0) {
  console.error(failures.join('\n'));
  console.error(`\n${failures.length}건 실패`);
  process.exit(1);
}

console.log(`OK — Markdown ${files.filter((f) => f.endsWith('.md')).length}개, 컴포넌트 문서 ${componentDocs.length}개 검사 통과`);
