const LOADING_ID = 'app-loading'

/** 移除系统初次加载占位层（淡出后从 DOM 删除） */
export function removeAppLoading() {
  const el = document.getElementById(LOADING_ID)
  if (!el)
    return

  el.classList.add('is-hide')
  el.addEventListener(
    'transitionend',
    () => el.remove(),
    { once: true },
  )
}
