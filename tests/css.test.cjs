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

test('all safelisted grid, RSS and status utilities survive compilation', () => {
  for (const name of [
    'grid-cols-2', 'grid-cols-3', 'grid-cols-4', 'grid-cols-5', 'grid-cols-6',
    'sm:grid-cols-4', 'lg:grid-cols-6',
    'text-orange-400', 'hover:text-orange-500', 'dark:text-orange-400', 'dark:hover:text-orange-300',
    'border-neutral-700', 'border-neutral-300', 'bg-neutral-200', 'bg-neutral-700',
    'text-neutral-600', 'text-neutral-200',
    'bg-sky-100', 'border-sky-400', 'text-sky-700',
    'bg-sky-900/50', 'border-sky-600', 'text-sky-300',
    'bg-amber-50', 'border-amber-400', 'text-amber-700',
    'bg-amber-900/40', 'border-amber-600', 'text-amber-300',
  ]) rulesFor(name);
});

test('dark mode remains controlled by the dark class, not a media query', () => {
  for (const name of ['dark:bg-olive-950', 'dark:text-olive-100', 'dark:prose-invert']) {
    for (const rule of rulesFor(name)) {
      assert.ok(rule.selector.includes(':where(.dark,.dark *)'), rule.selector);
      for (let parent = rule.parent; parent; parent = parent.parent) {
        assert.ok(!parent.params?.includes('prefers-color-scheme'));
      }
    }
  }
});

test('CSS-first theme preserves all olive colors and both font stacks', () => {
  for (const [shade, color] of Object.entries({
    50: '#fafaf5', 100: '#f0f2dc', 200: '#dde3b0', 300: '#c4cf7e',
    400: '#aab853', 500: '#8a9e3a', 600: '#6b7c2d', 700: '#526022',
    800: '#3d4a1a', 900: '#2c3612', 950: '#1a1a0d',
  })) assert.equal(themeValue(`--color-olive-${shade}`), color);
  assert.deepEqual(declarationsFor(rulesFor('text-olive-600'), 'color'), [
    'var(--color-olive-600)',
  ]);
  assert.deepEqual(declarationsFor(rulesFor('font-sans'), 'font-family'), [
    'var(--font-sans)',
  ]);
  assert.deepEqual(declarationsFor(rulesFor('font-mono'), 'font-family'), [
    'var(--font-mono)',
  ]);
  assert.equal(themeValue('--font-sans').replace(/["']/g, '').replace(/,\s*/g, ','),
    'Pretendard Variable,Noto Sans JP,ui-sans-serif,system-ui,sans-serif');
  assert.equal(themeValue('--font-mono').replace(/["']/g, '').replace(/,\s*/g, ','),
    'JetBrains Mono,ui-monospace,monospace');
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

test('Typography preserves the prose width and light/dark olive palette', () => {
  const rules = rulesFor('prose');
  for (const [property, value] of [
    ['max-width', '70ch'],
    ['font-family', 'var(--font-sans)'],
    ['--tw-prose-body', 'var(--color-olive-800)'],
    ['--tw-prose-links', 'var(--color-olive-600)'],
    ['--tw-prose-invert-body', 'var(--color-olive-200)'],
    ['--tw-prose-invert-pre-bg', 'var(--color-olive-950)'],
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
    'group-hover:text-olive-700', 'dark:group-hover:text-olive-300',
  ]) rulesFor(name);
});

test('custom fiction ornaments and book cover effects remain compiled', () => {
  const ornaments = [];
  css.walkRules(rule => {
    if (/^(\.dark )?\.prose-fiction hr::?after$/.test(rule.selector)) ornaments.push(rule);
  });
  assert.equal(ornaments.length, 2);
  assert.deepEqual(declarationsFor(ornaments, 'color'), [
    'var(--color-olive-400)', 'var(--color-olive-600)',
  ]);
  assert.deepEqual(declarationsFor(rulesFor('book-3d'), 'transform'), [
    'perspective(700px)rotateY(0)',
    'perspective(700px)rotateY(-22deg)translateY(-8px)scale(1.03)',
  ]);
});
