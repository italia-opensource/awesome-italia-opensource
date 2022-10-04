// @ts-check
// Note: type annotations allow type checking and IDEs autocompletion

const lightCodeTheme = require('prism-react-renderer/themes/github');
const darkCodeTheme = require('prism-react-renderer/themes/dracula');

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'Italia Opensource | Awesome Open Source',
  tagline: 'Italia Opensource',
  url: 'https://italia-opensource.github.io',
  baseUrl: '/awesome-italia-opensource/',
  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',
  // favicon: 'img/favicon.ico',

  // GitHub pages deployment config.
  // If you aren't using GitHub pages, you don't need these.
  organizationName: 'italia-opensource', // Usually your GitHub org/user name.
  projectName: 'awesome-italia-opensource', // Usually your repo name.

  // Even if you don't use internalization, you can use this field to set useful
  // metadata like html lang. For example, if your site is Chinese, you may want
  // to replace "en" with "zh-Hans".
  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        blog: false,
        theme: {
          customCss: require.resolve('./src/css/custom.css'),
        },
      }),
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      navbar: {
        title: 'Italia Opensource',
        // logo: {
          // alt: 'Italia Opensource Logo',
          // src: 'img/logo.svg',
        // },
        items: [
          {
            label: 'Awesome',
            position: 'left',
            items: [
              {
                href: 'https://italia-opensource.github.io/awesome-italia-innovative-companies',
                label: 'Innovative Companies',
              }
            ]
          },
          {
            href: 'https://github.com/italia-opensource/awesome-italia-opensource',
            label: 'GitHub',
            position: 'left',
          },
          {
            href: 'https://discord.gg/CsPwpqTGDK',
            label: 'Discord',
            position: 'left',
          },
        ],
      },
      footer: {
        style: 'light',
        copyright: `Copyright © ${new Date().getFullYear()} Italia Opensource`,
      },
      prism: {
        theme: lightCodeTheme,
        darkTheme: darkCodeTheme,
      },
    }),
};

module.exports = config;
