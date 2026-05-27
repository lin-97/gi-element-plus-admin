import type { DictOption } from '@/apis/dict'
import { getDictByCodeApi } from '@/apis/dict'

const dictCache = new Map<string, DictOption[]>()

export function useDict(code: string) {
  const options = ref<DictOption[]>([])
  const loading = ref(false)

  async function load() {
    const cached = dictCache.get(code)
    if (cached) {
      options.value = cached
      return
    }
    loading.value = true
    try {
      const data = await getDictByCodeApi(code)
      dictCache.set(code, data)
      options.value = data
    }
    finally {
      loading.value = false
    }
  }

  function getLabel(value: string | undefined) {
    if (!value)
      return ''
    return options.value.find(o => o.value === value)?.label ?? value
  }

  onMounted(load)

  return { options, loading, load, getLabel }
}

export function clearDictCache(code?: string) {
  if (code)
    dictCache.delete(code)
  else
    dictCache.clear()
}
