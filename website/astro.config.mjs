import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';
import sitemap from '@astrojs/sitemap';
import tailwindcss from '@tailwindcss/vite';
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const __dirname = dirname(fileURLToPath(import.meta.url));
const sodlGrammar = JSON.parse(
  readFileSync(join(__dirname, 'src/sodl.tmLanguage.json'), 'utf-8')
);

export default defineConfig({
  site: 'https://sodlspace.github.io',
  base: '/sodl-impl-v1/',
  vite: {
    plugins: [tailwindcss()],
  },
  markdown: {
    shikiConfig: {
      langs: [sodlGrammar],
    },
  },
  integrations: [
    sitemap(),
    starlight({
      title: 'SODL',
      description:
        'Specification Orchestration Definition Language — turn AI code generation from guesswork into engineering.',
      social: {
        github: 'https://github.com/sodlspace/sodl-impl-v1',
      },
      head: [
        {
          tag: 'meta',
          attrs: { property: 'og:image', content: 'https://sodl.space/og-card.png' },
        },
        {
          tag: 'meta',
          attrs: { name: 'twitter:card', content: 'summary_large_image' },
        },
      ],
      sidebar: [
        { label: 'Getting Started', link: '/getting-started/' },
        { label: 'Why SODL', link: '/why-sodl/' },
        { label: 'Use Cases', link: '/use-cases/' },
        {
          label: 'Language Reference',
          items: [
            { label: 'Overview', link: '/language/' },
            { label: 'Syntax', link: '/language/syntax/' },
            { label: 'Constructs', link: '/language/constructs/' },
            { label: 'Compiler & Output', link: '/language/compiler-output/' },
          ],
        },
        {
          label: 'Examples',
          autogenerate: { directory: 'examples' },
        },
        { label: 'Best Practices', link: '/best-practices/' },
        { label: 'Contact', link: '/contact/' },
      ],
      components: {
        Footer: './src/layouts/StarlightOverride.astro',
      },
      customCss: ['./src/styles/global.css'],
      expressiveCode: {
        shiki: {
          langs: [sodlGrammar],
        },
      },
    }),
  ],
});
