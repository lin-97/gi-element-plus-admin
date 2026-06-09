# 前端强制规范

> **适用范围**：`frontend/web/**`  
> **工具无关**：Cursor、OpenCode、Codex 等 AI 编码助手均应遵循本文

## 通用要求

- 始终使用**简体中文**与用户沟通。
- 未经用户明确要求，**不要**创建说明文档（README、*.md 等）。
- 未经用户明确要求，**不要**执行 git commit / push。
- 改动范围最小化：只改与任务直接相关的代码，不顺手重构无关模块。
- 优先复用项目已有抽象与约定，禁止凭空引入新架构或重复造轮子。

## 项目路径

- 前端根目录：`frontend/web/`
- 路径别名：`@/` → `frontend/web/src/`

## 技术栈

- Vue 3 **Composition API** + `<script setup lang="ts">`
- 每个 SFC 必须 `defineOptions({ name: 'Xxx' })`
- UI 组件库：优先使用 `gi-component`（GiPageLayout、GiForm、GiTable、GiDialog、GiCard 等）；**模板中统一使用 kebab-case 小写标签**（如 `<gi-form>`），无需 import（详见 `agents/rules/gi-component-vue.md`）；`script` 中仅 `import type` 类型
- 状态：Pinia；路由：Vue Router 4
- HTTP：`@/apis/request`，统一响应类型 `ApiResponse<T>`

## 目录约定

```
src/views/{module}/index.vue      # 列表页
src/views/{module}/FormDialog.vue # 新增/编辑弹窗（有表单时必建）
src/apis/{module}.ts              # 类型定义 + CRUD API
```

路由组件路径与 `views` 目录一致，例如 `crud/index` → `views/crud/index.vue`。

## CRUD 列表页（强制遵循）

新建/修改表格页时，**必须**参考并遵循：

- 参考实现：`frontend/web/src/views/crud/index.vue`、`FormDialog.vue`
- Hook：`@/hooks/useTable`
- API 模板：`frontend/web/src/apis/student.ts`
- 详细步骤：读取并遵循 `agents/skills/table-page/SKILL.md`

核心结构：

1. `queryForm`（reactive）+ `formColumns`（FormColumnItem[]）搜索区
2. `tableColumns`（TableColumnItem[]），操作列 `slotName: 'action'`
3. `useTable` 绑定列表 API 与 `deleteAPI`
4. `FormDialog` ref，`@success="refresh"`

分页类型：`PageResult<T>`（`list` + `total`）。

## API 层模板

```typescript
import { request } from './request'

export function getXxxListApi(params: XxxListQuery) {
  return request<PageResult<XxxInfo>>({ url: '/xxx/list', method: 'get', params })
}
```

## 代码风格

- 遵循 `@antfu/eslint-config`（`eslint.config.js`）
- 优先使用 auto-import 已注册 API（ref、reactive、computed 等无需手动 import）
- 布局组件放 `layouts/`，通用组件放 `components/`，业务逻辑 Hook 放 `hooks/` 或 `core/hooks/`

## dayjs

- 默认导入变量名必须为 **`Dayjs`**（大写开头），禁止小写 `dayjs`

```typescript
import Dayjs from 'dayjs'

const today = Dayjs().format('YYYY-MM-DD')
```

## 模板 Ref

- 获取**子组件实例**或 **DOM 元素实例**时，必须使用 **`useTemplateRef`**，禁止用 `ref()` + 模板 `ref` 属性
- `useTemplateRef` 的参数与模板上的 `ref="Xxx"` 保持一致（字符串字面量）
- `useTemplateRef` 已 auto-import，无需手动 import

```vue
<script setup lang="ts">
const FormDialogRef = useTemplateRef('FormDialogRef')
const formRef = useTemplateRef<FormInstance>('formRef')

function handleAdd() {
  FormDialogRef.value?.openAdd()
}
</script>

<template>
  <FormDialog ref="FormDialogRef" />
  <el-form ref="formRef" />
</template>
```

## Gi 组件模板写法

- **模板中** Gi 组件标签统一使用 **kebab-case 小写**，禁止 PascalCase
- 组件名对照：`GiPageLayout` → `<gi-page-layout>`，`GiForm` → `<gi-form>`，`GiTable` → `<gi-table>`，`GiDialog` → `<gi-dialog>`，`GiCard` → `<gi-card>`，`GiButton` → `<gi-button>`

```vue
<template>
  <gi-page-layout>
    <gi-form v-model="queryForm" :columns="formColumns" />
    <gi-table :data="tableData" :columns="tableColumns" />
    <gi-dialog v-model="visible" title="编辑">
      <gi-form v-model="form" :columns="dialogColumns" />
    </gi-dialog>
  </gi-page-layout>
</template>
```

## 组件 Emits

- `defineEmits` 必须使用**基于类型的函数调用签名**，禁止数组/tuple 形式
- 无参事件写 `(e: 'eventName'): void`；有参事件将参数写在 `e` 之后

```typescript
// ✅ 函数调用签名
const emit = defineEmits<{
  (e: 'success'): void
  (e: 'select', type?: DictTypeItem): void
  (e: 'change', id: number): void
}>()

// ❌ 数组/tuple 形式
const emit = defineEmits<{ success: [] }>()
const emit = defineEmits<{ select: [type?: DictTypeItem] }>()
```

## CSS 类名（BEM）

Vue SFC 中**自定义** CSS 类名必须采用 **BEM**（Block Element Modifier）命名，并在 `<style scoped>` 中与模板保持一致。

### 结构

| 类型 | 格式 | 示例 |
|------|------|------|
| Block（块） | `block` | `login-page`、`project-card` |
| Element（元素） | `block__element` | `login-page__brand`、`project-card__item` |
| Modifier（修饰符） | `block--modifier` 或 `block__element--modifier` | `login-page__illus-line--short` |

### 约定

- **Block** 名使用 **kebab-case**，通常对应当前组件语义（如 `login-page`、`user-form-dialog`），一个组件只设一个 Block
- **Element** 用双下划线 `__` 连接 Block，多级语义继续用 `-` 连接（如 `login-page__illus-line`），**禁止** `block__a__b` 链式元素写法
- **Modifier** 用双连字符 `--` 表示状态或变体（如 `--active`、`--disabled`、`--short`）
- 样式写在 `<style lang="scss" scoped>`，优先用 SCSS 嵌套表达 BEM 层级（`&__element`、`&--modifier`）
- **第三方组件**自带类名（如 `el-button`、`gi-table`）及 Tailwind/工具类不在此限；仅约束本组件新增的自定义 class

```vue
<template>
  <div class="login-page">
    <aside class="login-page__brand">
      <span class="login-page__badge">企业级中后台</span>
      <span class="login-page__illus-line login-page__illus-line--short" />
    </aside>
    <main class="login-page__panel login-page__panel--compact" />
  </div>
</template>

<style lang="scss" scoped>
.login-page {
  display: flex;

  &__brand {
    flex: 1;
  }

  &__badge {
    font-size: 13px;
  }

  &__illus-line {
    display: block;

    &--short {
      width: 70%;
    }
  }

  &__panel--compact {
    padding: 24px;
  }
}
</style>
```

## 禁止事项

- ❌ 使用 Options API 编写新组件
- ❌ 绕过 `@/apis/request` 直接裸用 axios
- ❌ 表格页自行实现分页/删除逻辑，而不使用 `useTable`
- ❌ 表格页使用原生 el-table 替代 GiTable（除非用户明确要求）
- ❌ `import { GiForm, GiTable, GiCard, ... } from 'gi-component'`（Gi 组件已全局注册）
- ❌ 模板中使用 PascalCase 写 Gi 组件（如 `<GiForm>`，应使用 `<gi-form>`）
- ❌ `import dayjs from 'dayjs'`（应使用 `import Dayjs from 'dayjs'`）
- ❌ 用 `const xxxRef = ref()` 绑定模板 ref 获取组件/元素实例（应使用 `useTemplateRef`）
- ❌ `defineEmits` 使用数组/tuple 形式（如 `{ success: [] }`，应使用 `(e: 'success'): void`）
- ❌ 自定义 class 使用非 BEM 命名（如 `.headerTitle`、`.card-body-item`、`.active-btn`）
- ❌ BEM 元素链式嵌套（如 `block__a__b`，应扁平为 `block__a-b`）
- ❌ 使用 `JSON.parse(JSON.stringify())` 做深拷贝（应使用 `@/utils` 的 `deepClone`）
- ❌ 在用户未要求时添加测试、文档或无关注释
