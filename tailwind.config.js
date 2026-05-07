/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: 'class',
  content: [
    './layouts/**/*.html',
    './assets/**/*.js',
  ],
  safelist: [
    // Grid column classes used dynamically — must survive CSS purge
    'grid-cols-2', 'grid-cols-3', 'grid-cols-4', 'grid-cols-5', 'grid-cols-6',
    'sm:grid-cols-4', 'lg:grid-cols-6',
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Pretendard Variable', 'Noto Sans JP', 'ui-sans-serif', 'system-ui', 'sans-serif'],
        mono: ['JetBrains Mono', 'ui-monospace', 'monospace'],
      },
      colors: {
        olive: {
          50:  '#fafaf5',
          100: '#f0f2dc',
          200: '#dde3b0',
          300: '#c4cf7e',
          400: '#aab853',
          500: '#8a9e3a',
          600: '#6b7c2d',
          700: '#526022',
          800: '#3d4a1a',
          900: '#2c3612',
          950: '#1a1a0d',
        },
      },
      typography: ({ theme }) => ({
        DEFAULT: {
          css: {
            maxWidth: '70ch',
            fontFamily: theme('fontFamily.sans').join(', '),
            '--tw-prose-body': theme('colors.olive[800]'),
            '--tw-prose-headings': theme('colors.olive[900]'),
            '--tw-prose-links': theme('colors.olive[600]'),
            '--tw-prose-bold': theme('colors.olive[800]'),
            '--tw-prose-counters': theme('colors.olive[500]'),
            '--tw-prose-bullets': theme('colors.olive[400]'),
            '--tw-prose-hr': theme('colors.olive[200]'),
            '--tw-prose-quotes': theme('colors.olive[700]'),
            '--tw-prose-quote-borders': theme('colors.olive[300]'),
            '--tw-prose-captions': theme('colors.olive[600]'),
            '--tw-prose-code': theme('colors.olive[800]'),
            '--tw-prose-pre-bg': theme('colors.olive[50]'),
            '--tw-prose-th-borders': theme('colors.olive[200]'),
            '--tw-prose-td-borders': theme('colors.olive[100]'),
            '--tw-prose-invert-body': theme('colors.olive[200]'),
            '--tw-prose-invert-headings': theme('colors.olive[100]'),
            '--tw-prose-invert-links': theme('colors.olive[400]'),
            '--tw-prose-invert-bold': theme('colors.olive[200]'),
            '--tw-prose-invert-counters': theme('colors.olive[400]'),
            '--tw-prose-invert-bullets': theme('colors.olive[500]'),
            '--tw-prose-invert-hr': theme('colors.olive[700]'),
            '--tw-prose-invert-quotes': theme('colors.olive[300]'),
            '--tw-prose-invert-quote-borders': theme('colors.olive[600]'),
            '--tw-prose-invert-captions': theme('colors.olive[400]'),
            '--tw-prose-invert-code': theme('colors.olive[200]'),
            '--tw-prose-invert-pre-bg': theme('colors.olive[950]'),
            '--tw-prose-invert-th-borders': theme('colors.olive[700]'),
            '--tw-prose-invert-td-borders': theme('colors.olive[800]'),
          },
        },
      }),
    },
  },
  plugins: [
    require('@tailwindcss/typography'),
  ],
}

