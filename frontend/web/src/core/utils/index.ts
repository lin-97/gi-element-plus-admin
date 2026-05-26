const LEADING_TRAILING_SLASHES_REGEX = /^\/+|\/+$/g
const WORD_SEPARATOR_REGEX = /[-_]+/

function toPascalCase(segment: string) {
  return segment
    .split(WORD_SEPARATOR_REGEX)
    .filter(Boolean)
    .map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
    .join('')
}

/**
 * 将路径转换为名称
 * @param path - 路径
 * @returns 名称
 * @example
 * transformPathToName('system/user/index') // 返回 'SystemUserIndex'
 */
export function transformPathToName(path: string) {
  return path
    .replace(LEADING_TRAILING_SLASHES_REGEX, '')
    .split('/')
    .filter(Boolean)
    .map(toPascalCase)
    .join('')
}
