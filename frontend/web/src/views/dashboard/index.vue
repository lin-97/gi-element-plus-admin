<script setup lang="ts">
import dayjs from 'dayjs'
import { GiCard } from 'gi-component'
import VChart from 'vue-echarts'
import { useChart } from '@/hooks/useChart'

defineOptions({ name: 'Dashboard' })

/** 统计卡片数据 */
const stats = shallowRef([
  { title: '访问量', value: 12846, trend: '+12%', color: '#165dff' },
  { title: '用户数', value: 3256, trend: '+8%', color: '#00b42a' },
  { title: '订单量', value: 1892, trend: '+5%', color: '#ff7d00' },
  { title: '收入', value: 86420, trend: '+18%', color: '#f53f3f', prefix: '¥' },
])

const { option: lineOption, theme: lineTheme } = useChart(() => ({
  tooltip: { trigger: 'axis' },
  grid: { left: 40, right: 20, top: 30, bottom: 30 },
  xAxis: {
    type: 'category',
    data: ['周一', '周二', '周三', '周四', '周五', '周六', '周日'],
  },
  yAxis: { type: 'value' },
  series: [
    {
      name: '访问量',
      type: 'line',
      smooth: true,
      data: [120, 200, 150, 280, 220, 310, 260],
      areaStyle: { color: 'rgba(22, 93, 255, 0.15)' },
      itemStyle: { color: '#165dff' },
    },
  ],
}))

const { option: pieOption, theme: pieTheme } = useChart(() => ({
  tooltip: { trigger: 'item' },
  legend: { bottom: 0 },
  series: [
    {
      type: 'pie',
      radius: ['40%', '70%'],
      data: [
        { value: 1048, name: '直接访问' },
        { value: 735, name: '邮件营销' },
        { value: 580, name: '联盟广告' },
        { value: 484, name: '视频广告' },
      ],
    },
  ],
}))

const updateTime = dayjs(new Date()).format('YYYY-MM-DD HH:mm:ss')
</script>

<template>
  <div class="dashboard">
    <el-row :gutter="16">
      <el-col v-for="item in stats" :key="item.title" :xs="24" :sm="12" :lg="6">
        <GiCard class="dashboard__stat" bordered>
          <el-statistic
            :title="item.title"
            :value="item.value"
            :prefix="item.prefix"
            group-separator=","
            :value-style="{ color: item.color, fontWeight: 600 }"
          >
            <template #suffix>
              <el-tag size="small" type="success" class="dashboard__stat-trend">
                {{ item.trend }}
              </el-tag>
            </template>
          </el-statistic>
        </GiCard>
      </el-col>
    </el-row>

    <el-row :gutter="16" class="dashboard__charts">
      <el-col :xs="24" :lg="14">
        <GiCard bordered title="访问趋势">
          <template #extra>
            <span class="dashboard__time">{{ updateTime }}</span>
          </template>
          <VChart
            :key="lineTheme"
            class="dashboard__chart"
            :option="lineOption"
            :theme="lineTheme"
            autoresize
          />
        </GiCard>
      </el-col>
      <el-col :xs="24" :lg="10">
        <GiCard bordered title="流量来源">
          <VChart
            :key="pieTheme"
            class="dashboard__chart"
            :option="pieOption"
            :theme="pieTheme"
            autoresize
          />
        </GiCard>
      </el-col>
    </el-row>
  </div>
</template>

<style lang="scss" scoped>
.dashboard {
  height: 100%;
  padding: 16px;
  overflow: hidden;
  overflow-y: auto;
  &__stat {
    margin-bottom: 16px;

    :deep(.gi-card-header) {
      display: none;
    }

    :deep(.el-statistic__content) {
      flex-wrap: wrap;
      gap: 8px;
    }

    &-trend {
      margin-left: 4px;
    }
  }

  &__charts {
    margin-top: 8px;
  }

  &__chart {
    width: 100%;
    height: 360px;
  }

  &__time {
    font-size: 12px;
    color: var(--el-text-color-regular);
  }
}
</style>
