# Gi 组件（gi-component）

> **适用范围**：`frontend/web/**/*.vue`  
> **工具无关**：Cursor、OpenCode、Codex 等 AI 编码助手均应遵循本文

`gi-component` 已在 `frontend/web/src/main.ts` 通过 `app.use(GiComponent)` **全局注册**，模板中可直接使用，**禁止**为组件本身编写 `import { GiXxx } from 'gi-component'`。

## 模板用法

**模板中统一使用 kebab-case 小写标签**，禁止 PascalCase（如 `<GiForm>`）。

```vue
<template>
  <gi-page-layout>
    <gi-form v-model="queryForm" :columns="formColumns" />
    <gi-table :data="tableData" :columns="tableColumns" />
    <gi-dialog v-model="visible" title="编辑">
      <gi-form v-model="form" :columns="dialogColumns" />
    </gi-dialog>
    <gi-card bordered title="标题">内容</gi-card>
  </gi-page-layout>
</template>
```

| PascalCase（script/类型） | 模板标签 |
|---------------------------|----------|
| `GiPageLayout` | `<gi-page-layout>` |
| `GiForm` | `<gi-form>` |
| `GiTable` | `<gi-table>` |
| `GiDialog` | `<gi-dialog>` |
| `GiCard` | `<gi-card>` |
| `GiButton` | `<gi-button>` |
| `GiDrawer` | `<gi-drawer>` |
| `GiFlex` / `GiGrid` | `<gi-flex>` / `<gi-grid>` |
| `GiTag` | `<gi-tag>` |

## script 中仅类型可 import

列配置、表单实例等 **TypeScript 类型** 仍从 `gi-component` 按需 `import type`：

```typescript
import type { FormColumnItem, TableColumnItem, FormInstance } from 'gi-component'
```

## 常用 Gi 组件

| 组件 | 用途 |
|------|------|
| `GiPageLayout` | 页面布局（列表页） |
| `GiForm` | 搜索/表单 |
| `GiTable` | 数据表格 |
| `GiDialog` | 弹窗 |
| `GiCard` | 卡片容器 |
| `GiDrawer` | 抽屉 |
| `GiFlex` / `GiGrid` | 布局 |
| `GiButton` / `GiTag` | 按钮、标签 |

Element Plus 组件（`el-row`、`el-col`、`el-statistic` 等）同样为全局注册，无需 import。

## 禁止

```typescript
// ❌ 不要为模板组件写值 import
import { GiCard, GiForm, GiTable, GiPageLayout, GiDialog } from 'gi-component'

// ✅ 仅类型
import type { FormColumnItem } from 'gi-component'
```

```vue
<!-- ❌ 模板中不要用 PascalCase -->
<GiForm v-model="form" />

<!-- ✅ 使用 kebab-case -->
<gi-form v-model="form" />
```
