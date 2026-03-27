import { defineConfig } from 'vitepress'

export default defineConfig({
  title: 'AI创业资讯',
  description: '面向AI创业者的权威资讯聚合平台',

  head: [
    ['link', { rel: 'icon', href: '/favicon.ico' }],
    ['meta', { name: 'theme-color', content: '#5865F2' }],
    ['meta', { name: 'og:type', content: 'website' }],
    ['meta', { name: 'og:site_name', content: 'AI Startup News' }],
  ],

  // English locale temporarily disabled - will be enabled after backend migration
  // locales: { en: { ... } },

  lang: 'zh-CN',

  themeConfig: {
    logo: '/logo.svg',

    nav: [
      { text: '首页', link: '/' },
      { text: '信息来源', link: '/sources' }
    ],

    outline: {
      label: '页面导航'
    },

    lastUpdated: {
      text: '最后更新于'
    },

    docFooter: {
      prev: '上一篇',
      next: '下一篇'
    },

    socialLinks: [
      { icon: 'github', link: 'https://github.com' }
    ],

    footer: {
      message: '专注AI创业领域的权威资讯聚合',
      copyright: 'Copyright © 2025 AI Startup News'
    }
  },

  markdown: {
    lineNumbers: true
  },

  lastUpdated: true
})
