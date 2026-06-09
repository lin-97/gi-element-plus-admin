import { clone, eachTree, mapTree, orderBy } from 'xe-utils'

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

const SORT_BY_META = [[(node: TreeNode) => node.meta?.sort ?? 0, 'asc']]

/**
 * 过滤并排序树形结构
 * @param array - 树形数组
 * @param predicate - 过滤函数
 */
export function filterSortTree<T extends TreeNode>(
  array: T[],
  predicate: (node: TreeNode) => boolean,
): T[] {
  const sorted = orderBy(filterTree(array, predicate) as T[], SORT_BY_META)
  eachTree(sorted, (item) => {
    if (item.children?.length)
      item.children = orderBy(item.children, SORT_BY_META)
  })
  return sorted
}

/** 深拷贝（基于 xe-utils clone） */
export function deepClone<T>(data: T): T {
  return clone(data, true) as T
}

/** 判断 path 是否为外链 */
export function isExternal(path: string) {
  return /^(?:https?:|mailto:|tel:)/.test(path)
}
