import DefaultTheme from 'vitepress/theme'
import NewsTabs from './components/NewsTabs.vue'
import './custom.css'

export default {
  extends: DefaultTheme,
  enhanceApp({ app }) {
    app.component('NewsTabs', NewsTabs)
  }
}
