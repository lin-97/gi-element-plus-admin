/** 动态路由是否已为当前会话加载（切换用户须重置） */
let isRoutesLoaded = false

export function isRoutesLoadedState() {
  return isRoutesLoaded
}

export function markRoutesLoaded() {
  isRoutesLoaded = true
}

export function resetRoutesLoadedFlag() {
  isRoutesLoaded = false
}
