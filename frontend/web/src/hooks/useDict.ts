import type { DictOption } from '@/apis/dict'
import { getDictByCodeApi } from '@/apis/dict'

const dictCache = reactive<Record<string, DictOption[]>>({})
const loadingCodes = new Set<string>()

/**
 * 将字符串数组转换为对象类型
 * @example
 * ArrayToObject<['STATUS', 'GENDER']> // { STATUS: DictOption[], GENDER: DictOption[] }
 */
type ArrayToObject<T extends readonly string[]> = {
  [K in T[number]]: DictOption[]
}

async function loadDict(code: string) {
  if (dictCache[code]?.length)
    return dictCache[code]

  if (loadingCodes.has(code))
    return dictCache[code] ?? []

  loadingCodes.add(code)
  try {
    const data = await getDictByCodeApi(code)
    dictCache[code] = data
    return data
  }
  finally {
    loadingCodes.delete(code)
  }
}

/**
 * 字典数据 Hook
 * @description 根据传入的字典代码数组，返回对应的字典数据对象
 * @param codes - 字典代码数组，会自动推断字面量类型以提供类型提示
 * @returns 返回包含字典数据的响应式对象，对象的键为 codes 中的元素
 * @example
 * const { dictData } = useDict(['STATUS', 'GENDER'] as const)
 * // dictData.value.STATUS ✅ 有类型提示
 * // dictData.value.GENDER ✅ 有类型提示
 */
export function useDict<const T extends readonly string[]>(codes: T) {
  const loading = ref(false)

  async function load() {
    const pending = codes.filter(code => !dictCache[code]?.length)
    if (!pending.length)
      return

    loading.value = true
    try {
      await Promise.all(pending.map(code => loadDict(code)))
    }
    finally {
      loading.value = false
    }
  }

  onMounted(load)

  const dictData = computed<ArrayToObject<T>>(() => {
    const result = {} as ArrayToObject<T>
    for (const code of codes) {
      result[code as T[number]] = dictCache[code] || []
    }
    return result
  })

  return { dictData, loading, load }
}

/** 根据字典选项解析展示文案 */
export function getDictLabel(options: DictOption[], value: string | undefined) {
  if (!value)
    return ''
  return options.find(o => o.value === value)?.label ?? value
}

/** 清除字典缓存（不传 code 则清空全部） */
export function clearDictCache(code?: string) {
  if (code) {
    delete dictCache[code]
    return
  }
  Object.keys(dictCache).forEach(key => delete dictCache[key])
}
