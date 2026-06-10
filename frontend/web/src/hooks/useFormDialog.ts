import type { FormInstance } from 'gi-component'
import type { Ref, ShallowRef } from 'vue'

export interface UseFormDialogSubmitContext<TForm> {
  isEdit: boolean
  id: string
  data: TForm
}

export interface UseFormDialogOptions<TForm, TRow> {
  formRef: Ref<FormInstance | null | undefined> | ShallowRef<FormInstance | null | undefined>
  createEmptyForm: () => TForm
  toFormData: (row: TRow) => TForm
  getRowId?: (row: TRow) => string
  submit: (ctx: UseFormDialogSubmitContext<TForm>) => Promise<void>
  onSuccess?: () => void
  titles: { add: string, edit: string }
}

export function useFormDialog<TForm, TRow extends { id?: string }>(
  options: UseFormDialogOptions<TForm, TRow>,
) {
  const visible = ref(false)
  const isEdit = ref(false)
  const currentId = ref('')
  const formData = ref(options.createEmptyForm()) as Ref<TForm>

  const dialogTitle = computed(() => (isEdit.value ? options.titles.edit : options.titles.add))

  function openAdd() {
    isEdit.value = false
    currentId.value = ''
    formData.value = options.createEmptyForm()
    visible.value = true
  }

  function openEdit(row: TRow) {
    isEdit.value = true
    currentId.value = options.getRowId?.(row) ?? row.id ?? ''
    formData.value = options.toFormData(row)
    visible.value = true
  }

  async function handleBeforeOk() {
    try {
      await options.formRef.value?.formRef?.validate()
      await options.submit({
        isEdit: isEdit.value,
        id: currentId.value,
        data: formData.value,
      })
      options.onSuccess?.()
      return true
    }
    catch {
      return false
    }
  }

  return {
    visible,
    isEdit,
    currentId,
    formData,
    dialogTitle,
    openAdd,
    openEdit,
    handleBeforeOk,
  }
}
