import { mapTree } from 'xe-utils'

interface TreeNode {
  children?: TreeNode[]
  [key: string]: any
}

/**
 * 过滤树形结构
 * @param array - 树形数组
 * @param predicate - 过滤函数
 * @returns 过滤后的树形数组
 */
export function filterTree(array: TreeNode[], predicate: (node: TreeNode) => boolean): TreeNode[] {
  const filtered = array.filter(predicate)
  return mapTree(filtered, (item) => {
    if (item.children?.length) {
      item.children = item.children.filter(predicate)
    }
    return item
  })
}

/** 判断 path 是否为外链 */
export function isExternal(path: string) {
  return /^(?:https?:|mailto:|tel:)/.test(path)
}
