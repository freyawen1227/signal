<script setup>
import { ref, computed, onMounted } from 'vue'
import newsData from '../../../data/news.json'

const activeTab = ref('ai-news')
const isEn = ref(false)

onMounted(() => {
  isEn.value = window.location.pathname.startsWith('/en')
})

const tabs = computed(() => [
  { id: 'ai-news', label: isEn.value ? 'AI News' : 'AI 动态' },
  { id: 'investment', label: isEn.value ? 'Investment' : '投资市场' }
])

const getLocalizedText = (item, field) => {
  if (typeof item[field] === 'object') {
    return isEn.value ? item[field].en : item[field].zh
  }
  return item[field]
}

const getLocalizedLink = (item) => {
  if (typeof item.link === 'object') {
    return isEn.value ? item.link.en : item.link.zh
  }
  return item.link
}

const setActiveTab = (tabId) => {
  activeTab.value = tabId
}
</script>

<template>
  <ClientOnly>
    <div class="news-tabs">
      <div class="tabs-header">
        <button
          v-for="tab in tabs"
          :key="tab.id"
          :class="['tab-btn', { active: activeTab === tab.id }]"
          @click="setActiveTab(tab.id)"
        >
          {{ tab.label }}
        </button>
      </div>

      <div class="tabs-content">
        <div v-for="tab in tabs" :key="tab.id" v-show="activeTab === tab.id" class="tab-panel">
          <div v-for="item in newsData[tab.id]" :key="item.date + getLocalizedText(item, 'title')" class="news-card">
            <div class="news-meta">
              <span class="news-date">{{ item.date }}</span>
              <span class="news-source">{{ getLocalizedText(item, 'source') }}</span>
            </div>
            <h3 class="news-title">
              <a :href="getLocalizedLink(item)">{{ getLocalizedText(item, 'title') }}</a>
            </h3>
            <p class="news-summary">{{ getLocalizedText(item, 'summary') }}</p>
            <div class="news-tags">
              <span v-for="tag in getLocalizedText(item, 'tags')" :key="tag" class="tag">{{ tag }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </ClientOnly>
</template>

<style scoped>
.news-tabs {
  margin: 2rem 0;
}

.tabs-header {
  display: flex;
  gap: 0.5rem;
  border-bottom: 2px solid #E0E7D0;
  padding-bottom: 0;
  margin-bottom: 1.5rem;
}

.tab-btn {
  padding: 0.75rem 1.5rem;
  border: none;
  background: none;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 500;
  font-family: 'YouWare Sans', sans-serif;
  color: rgba(0, 0, 0, 0.6);
  border-bottom: 2px solid transparent;
  margin-bottom: -2px;
  transition: all 0.2s ease;
}

.tab-btn:hover {
  color: #55644A;
}

.tab-btn.active {
  color: #55644A;
  border-bottom-color: #55644A;
}

.tabs-content {
  min-height: 400px;
}

.tab-panel {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.news-card {
  padding: 1.25rem;
  border: 1px solid #E0E7D0;
  border-radius: 12px;
  transition: all 0.2s ease;
  background: #FFFFFF;
}

.news-card:hover {
  border-color: #55644A;
  box-shadow: 0 4px 16px rgba(85, 100, 74, 0.1);
}

.news-meta {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 0.5rem;
}

.news-date {
  color: rgba(0, 0, 0, 0.5);
  font-size: 0.875rem;
}

.news-source {
  padding: 0.125rem 0.5rem;
  background: #E0E7D0;
  color: #2E4226;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 500;
}

.news-title {
  margin: 0 0 0.5rem 0;
  font-size: 1.125rem;
  line-height: 1.4;
  font-family: 'YouWare Sans', sans-serif;
}

.news-title a {
  color: #000000;
  text-decoration: none;
}

.news-title a:hover {
  color: #55644A;
}

.news-summary {
  color: rgba(0, 0, 0, 0.7);
  font-size: 0.9375rem;
  line-height: 1.6;
  margin: 0 0 0.75rem 0;
}

.news-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.375rem;
}

.tag {
  padding: 0.125rem 0.5rem;
  background: #F6F4F1;
  color: rgba(0, 0, 0, 0.6);
  border-radius: 4px;
  font-size: 0.75rem;
}

/* 深色模式 */
.dark .tabs-header {
  border-bottom-color: #2E4226;
}

.dark .tab-btn {
  color: rgba(246, 244, 241, 0.6);
}

.dark .tab-btn:hover,
.dark .tab-btn.active {
  color: #7A8B6E;
}

.dark .tab-btn.active {
  border-bottom-color: #7A8B6E;
}

.dark .news-card {
  background: #242424;
  border-color: #2E4226;
}

.dark .news-card:hover {
  border-color: #55644A;
}

.dark .news-source {
  background: rgba(85, 100, 74, 0.3);
  color: #E0E7D0;
}

.dark .news-title a {
  color: #F6F4F1;
}

.dark .news-title a:hover {
  color: #7A8B6E;
}

.dark .news-summary {
  color: rgba(246, 244, 241, 0.7);
}

.dark .tag {
  background: #2E4226;
  color: rgba(246, 244, 241, 0.6);
}

@media (max-width: 640px) {
  .tabs-header {
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
  }

  .tab-btn {
    padding: 0.625rem 1rem;
    font-size: 0.9375rem;
    white-space: nowrap;
  }

  .news-card {
    padding: 1rem;
  }
}
</style>
