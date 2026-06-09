import { breakpointsTailwind, useBreakpoints } from '@vueuse/core'

/**
 * 统一响应式断点 Hook
 */
export function useResponsive() {
  const breakpoints = useBreakpoints(breakpointsTailwind)

  return {
    /** 视口宽度 < 640px */
    isXs: breakpoints.smaller('sm'),
    /** 视口宽度 < 768px */
    isMobile: breakpoints.smaller('md'),
  }
}
