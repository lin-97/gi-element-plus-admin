import { pascalCase } from 'es-toolkit/string'

/**
 * 将路径转换为名称
 * @param path - 路径
 * @returns 名称
 * @example
 * transformPathToName('system/user/index') // 返回 'SystemUserIndex'
 */
export function transformPathToName(path: string) {
  return pascalCase(path)
}
