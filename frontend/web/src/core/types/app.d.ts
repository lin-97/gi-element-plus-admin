declare namespace App {
  /** 系统配置 */
  interface SettingConfig {
    themeColor: string // 主题色
    isShowTabs: boolean // 是否显示页签
    isShowAnimation: boolean // 是否显示动画
    isMenuCollapse: boolean // 是否折叠菜单
    isMenuAccordion: boolean // 左侧菜单手风琴效果
    isMenuDark: boolean // 菜单深色模式
    menuWidth: number // 菜单宽度
    headerHeight: number // 顶栏高度
    layoutMode: 'left' | 'top' | 'mix' // 系统布局
  }
}
