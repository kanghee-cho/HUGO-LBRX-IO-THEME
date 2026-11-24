const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const test = require('node:test');
const postcss = require('postcss');

const css = postcss.parse(fs.readFileSync(path.join(__dirname, '../assets/css/main.min.css'), 'utf8'));

function rulesFor(name) {
  const selector = '.' + name.replace(/[^a-zA-Z0-9_-]/g, '\\$&');
  const rules = [];
  css.walkRules(rule => {
    const index = rule.selector.indexOf(selector);
    if (index !== -1 && !/[a-zA-Z0-9_\\-]/.test(rule.selector.charAt(index + selector.length))) {
      rules.push(rule);
    }
  });
  assert.ok(rules.length > 0, `Missing generated utility: ${name}`);
  return rules;
}

function declarationsFor(rules, property) {
  return rules.flatMap(rule => rule.nodes
    .filter(node => node.type === 'decl' && node.prop === property)
    .map(node => node.value));
}

function lastValue(rules, property) {
  return declarationsFor(rules, property).at(-1);
}

function themeValue(property) {
  const values = [];
  css.walkDecls(property, declaration => values.push(declaration.value));
  assert.ok(values.length > 0, `Missing theme variable: ${property}`);
  return values.at(-1);
}

test('default favicon and manifest links resolve to correctly sized theme assets', () => {
  const staticDir = path.join(__dirname, '../static');
  const head = fs.readFileSync(path.join(__dirname, '../layouts/partials/head.html'), 'utf8');
  for (const name of ['favicon.ico', 'favicon.svg', 'apple-touch-icon.png', 'site.webmanifest']) {
    assert.ok(head.includes(`"${name}" | relURL`), `${name} must respect the site URL subpath`);
    assert.ok(fs.existsSync(path.join(staticDir, name)), `Missing default asset: ${name}`);
    assert.ok(!fs.existsSync(path.join(__dirname, '../exampleSite/static', name)),
      `The example site must not shadow the theme's default ${name}`);
  }
  const manifest = JSON.parse(fs.readFileSync(path.join(staticDir, 'site.webmanifest'), 'utf8'));
  for (const icon of [...manifest.icons, {src: 'apple-touch-icon.png', sizes: '180x180'}]) {
    assert.ok(!icon.src.startsWith('/'), 'Manifest icon URLs must be relative');
    const png = fs.readFileSync(path.join(staticDir, icon.src));
    assert.equal(png.subarray(0, 8).toString('hex'), '89504e470d0a1a0a');
    assert.equal(`${png.readUInt32BE(16)}x${png.readUInt32BE(20)}`, icon.sizes);
  }
  const ico = fs.readFileSync(path.join(staticDir, 'favicon.ico'));
  assert.equal(ico.readUInt16LE(2), 1);
  const sizes = [];
  for (let index = 0; index < ico.readUInt16LE(4); index++) {
    const entry = 6 + index * 16;
    const size = ico[entry];
    assert.equal(ico[entry + 1], size);
    const length = ico.readUInt32LE(entry + 8);
    const offset = ico.readUInt32LE(entry + 12);
    const frame = ico.subarray(offset, offset + length);
    assert.equal(frame.subarray(0, 8).toString('hex'), '89504e470d0a1a0a');
    assert.equal(frame.readUInt32BE(16), size);
    assert.equal(frame.readUInt32BE(20), size);
    sizes.push(size);
  }
  assert.deepEqual(sizes.sort((a, b) => a - b), [16, 32, 48]);
});

test('responsive book grids retain their column counts and breakpoints', () => {
  for (const [name, columns, breakpoint] of [
    ['grid-cols-3', 3, null],
    ['sm:grid-cols-4', 4, '(min-width:40rem)'],
    ['lg:grid-cols-6', 6, '(min-width:64rem)'],
  ]) {
    const rules = rulesFor(name);
    assert.deepEqual(declarationsFor(rules, 'grid-template-columns'), [
      `repeat(${columns},minmax(0,1fr))`,
    ]);
    if (breakpoint) {
      assert.equal(rules[0].parent.name, 'media');
      assert.equal(rules[0].parent.params, breakpoint);
    }
  }
});

test('grid, RSS and semantic status utilities survive compilation', () => {
  for (const name of [
    'grid-cols-2', 'grid-cols-3', 'grid-cols-4', 'grid-cols-5', 'grid-cols-6',
    'sm:grid-cols-4', 'lg:grid-cols-6',
    'text-brand-accent', 'hover:text-brand-accent',
    'bg-brand-surface', 'text-brand-success', 'border-brand-success',
    'text-brand-function', 'border-brand-function',
    'text-brand-warning', 'border-brand-warning',
    'text-brand-muted', 'border-brand-muted',
  ]) rulesFor(name);
});

test('dark mode remains controlled by the dark class, not a media query', () => {
  for (const name of ['dark:bg-brand-background', 'dark:text-brand-text', 'dark:prose-invert']) {
    for (const rule of rulesFor(name)) {
      assert.ok(rule.selector.includes(':where(.dark,.dark *)'), rule.selector);
      for (let parent = rule.parent; parent; parent = parent.parent) {
        assert.ok(!parent.params?.includes('prefers-color-scheme'));
      }
    }
  }
});

test('semantic utilities resolve the reference palette in both modes', () => {
  for (const [selector, expected] of [
    [':root', {
      background: '#f3f4ec', surface: '#e8ede4', text: '#24362f',
      accent: '#246958', muted: '#52655b', 'on-accent': '#f3f4ec',
    }],
    ['.dark', {
      background: '#19231f', surface: '#25332c', text: '#dce6db',
      accent: '#84c7ac', muted: '#a3b5a9', 'on-accent': '#19231f',
    }],
  ]) {
    const rules = [];
    css.walkRules(rule => {
      if (rule.selector === selector) rules.push(rule);
    });
    for (const [role, color] of Object.entries(expected)) {
      assert.equal(lastValue(rules, `--brand-${role}`), color);
    }
  }
  for (const [utility, property, role] of [
    ['bg-brand-background', 'background-color', 'background'],
    ['dark:bg-brand-background', 'background-color', 'background'],
    ['text-brand-text', 'color', 'text'],
    ['dark:text-brand-text', 'color', 'text'],
    ['text-brand-accent', 'color', 'accent'],
    ['text-brand-on-accent', 'color', 'on-accent'],
  ]) {
    assert.equal(lastValue(rulesFor(utility), property), `var(--brand-${role})`);
  }
});

test('local font stacks and weight mapping use only shipped Regular/Bold faces', () => {
  assert.deepEqual(declarationsFor(rulesFor('font-sans'), 'font-family'), [
    'var(--font-sans)',
  ]);
  assert.deepEqual(declarationsFor(rulesFor('font-mono'), 'font-family'), [
    'var(--font-mono)',
  ]);
  assert.equal(themeValue('--font-sans').replace(/["']/g, '').replace(/,\s*/g, ','),
    'LINE Seed Sans,LINE Seed Sans KR,LINE Seed JP_TTF,sans-serif');
  assert.equal(themeValue('--font-mono').replace(/["']/g, '').replace(/,\s*/g, ','),
    'D2Coding ligature,monospace');
  for (const [name, weight] of [['light', '400'], ['medium', '400'], ['semibold', '700']]) {
    assert.equal(themeValue(`--font-weight-${name}`), weight);
  }
  const faces = [];
  css.walkAtRules('font-face', rule => faces.push(rule));
  assert.equal(faces.length, 8);
  for (const family of ['LINE Seed Sans', 'LINE Seed Sans KR', 'LINE Seed JP_TTF', 'D2Coding ligature']) {
    const familyFaces = faces.filter(face =>
      lastValue([face], 'font-family').replace(/["']/g, '') === family);
    assert.deepEqual(familyFaces.map(face => lastValue([face], 'font-weight')).sort(), ['400', '700']);
  }
  for (const face of faces) {
    assert.equal(lastValue([face], 'font-display'), 'swap');
    const url = lastValue([face], 'src').match(/url\(["']?([^"')]+)["']?\)/)[1];
    const font = fs.readFileSync(path.join(__dirname, '../static', url.replace('../', '')));
    assert.equal(font.toString('ascii', 0, 4), 'wOF2');
  }
  const head = fs.readFileSync(path.join(__dirname, '../layouts/partials/head.html'), 'utf8');
  assert.doesNotMatch(head, /fonts\.googleapis\.com|fonts\.gstatic\.com|cdn\.jsdelivr\.net/);
});

test('arbitrary shelf grid tracks retain two valid space-separated columns', () => {
  for (const [name, value] of [
    ['grid-cols-[6rem_1fr]', '6rem 1fr'],
    ['lg:grid-cols-[14rem_1fr]', '14rem 1fr'],
  ]) {
    assert.deepEqual(declarationsFor(rulesFor(name), 'grid-template-columns'), [value]);
  }
});

test('renamed utilities retain v3 geometry and accessible focus outlines', () => {
  assert.equal(lastValue(rulesFor('rounded-xs'), 'border-radius'), 'var(--radius-xs)');
  assert.equal(themeValue('--radius-xs'), '.125rem');
  assert.equal(lastValue(rulesFor('sm:rounded-sm'), 'border-radius'), 'var(--radius-sm)');
  assert.equal(themeValue('--radius-sm'), '.25rem');
  assert.equal(themeValue('--blur-xs'), '4px');
  assert.ok(lastValue(rulesFor('shadow-xs'), '--tw-shadow').startsWith('0 1px 2px 0 '));
  assert.equal(lastValue(rulesFor('shrink-0'), 'flex-shrink'), '0');
  for (const name of ['outline-hidden', 'focus:outline-hidden']) {
    assert.equal(lastValue(rulesFor(name), 'outline-offset'), '2px');
    assert.ok(lastValue(rulesFor(name), 'outline').includes('2px solid'));
  }
});

test('Typography preserves prose width and follows semantic colors in both modes', () => {
  const rules = rulesFor('prose').filter(rule => rule.selector === '.prose');
  for (const [property, value] of [
    ['max-width', '70ch'],
    ['font-family', 'var(--font-sans)'],
    ['--tw-prose-body', 'var(--brand-text)'],
    ['--tw-prose-links', 'var(--brand-link)'],
    ['--tw-prose-code', 'var(--brand-inline-code)'],
    ['--tw-prose-invert-body', 'var(--brand-text)'],
    ['--tw-prose-invert-pre-bg', 'var(--brand-code-block-background)'],
  ]) {
    assert.equal(lastValue(rules, property), value);
  }
  const invert = rulesFor('dark:prose-invert');
  assert.deepEqual(declarationsFor(invert, '--tw-prose-body'), [
    'var(--tw-prose-invert-body)',
  ]);
  const orderedRules = [];
  css.walkRules(rule => orderedRules.push(rule));
  assert.ok(orderedRules.indexOf(invert[0]) > orderedRules.indexOf(
    rules.findLast(rule => rule.nodes.some(node => node.prop === '--tw-prose-body'))),
  'Dark Typography must follow the custom prose palette in the cascade');
  assert.ok(orderedRules.indexOf(rulesFor('max-w-none')[0]) > orderedRules.indexOf(
    rules.findLast(rule => rule.nodes.some(node => node.prop === 'max-width'))),
  'Explicit width utilities must override the default prose width');
});

test('prose code and syntax highlighting follow the brand typography and selection roles', () => {
  const codeRules = [];
  const selections = [];
  const keywords = [];
  css.walkRules(rule => {
    if (rule.selector === '.prose :where(pre,code,kbd,samp)') codeRules.push(rule);
    if (rule.selector === '::selection') selections.push(rule);
    if (rule.selector.split(',').includes('.chroma .k')) keywords.push(rule);
  });
  assert.equal(lastValue(codeRules, 'font-family'), 'var(--font-mono)');
  assert.equal(lastValue(codeRules, 'font-size'), '14px');
  assert.equal(lastValue(codeRules, 'line-height'), '1.45');
  assert.equal(lastValue(selections, 'background'), 'var(--brand-prose-selection-background)');
  assert.equal(lastValue(keywords, 'color'), 'var(--brand-keyword)');
});

test('interactive buttons keep their pointer affordance', () => {
  const buttons = [];
  css.walkRules(rule => {
    if (rule.selector.includes('button:not(:disabled)')) buttons.push(rule);
  });
  assert.ok(declarationsFor(buttons, 'cursor').includes('pointer'));
});

test('all twelve edition palettes include light, dark and hover utilities', () => {
  for (const color of [
    'rose', 'pink', 'fuchsia', 'violet', 'indigo', 'sky',
    'cyan', 'teal', 'emerald', 'lime', 'amber', 'orange',
  ]) {
    for (const name of [
      `bg-${color}-50`, `dark:bg-${color}-900`,
      `text-${color}-800`, `dark:text-${color}-200`,
      `border-${color}-200`, `dark:border-${color}-700`,
      `hover:bg-${color}-100`, `dark:hover:bg-${color}-900`,
    ]) rulesFor(name);
  }
});

test('JavaScript-generated search result utilities are included', () => {
  for (const name of [
    'line-clamp-1', 'line-clamp-2', 'tracking-wider',
    'group-hover:text-brand-accent', 'dark:group-hover:text-brand-accent',
  ]) rulesFor(name);
});

test('custom fiction ornaments and book cover effects remain compiled', () => {
  const ornaments = [];
  css.walkRules(rule => {
    if (/^(\.dark )?\.prose-fiction hr::?after$/.test(rule.selector)) ornaments.push(rule);
  });
  assert.equal(ornaments.length, 1);
  assert.deepEqual(declarationsFor(ornaments, 'color'), [
    'var(--brand-muted)',
  ]);
  assert.deepEqual(declarationsFor(rulesFor('book-3d'), 'transform'), [
    'perspective(700px)rotateY(0)',
    'perspective(700px)rotateY(-22deg)translateY(-8px)scale(1.03)',
  ]);
});
