import path from 'node:path'
import { fileURLToPath, URL } from 'node:url'
import vue from '@vitejs/plugin-vue'
import vueJsx from '@vitejs/plugin-vue-jsx'
import AutoImport from 'unplugin-auto-import/vite'
import IconsResolver from 'unplugin-icons/resolver'
import Icons from 'unplugin-icons/vite'
import { ElementPlusResolver } from 'unplugin-vue-components/resolvers'
import Components from 'unplugin-vue-components/vite'
import { defineConfig, loadEnv } from 'vite'
import vitePluginCompression from 'vite-plugin-compression'
import { createSvgIconsPlugin } from 'vite-plugin-svg-icons'
import VueDevTools from 'vite-plugin-vue-devtools'

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd()) as ImportMetaEnv

  return {
    base: env.VITE_BASE,
    resolve: {
      alias: {
        '~': fileURLToPath(new URL('./', import.meta.url)),
        '@': fileURLToPath(new URL('./src', import.meta.url)),
        // 使 echarts/theme/*.js 在按需引入时也能注册到 echarts/core
        'echarts/lib/echarts': 'echarts/core',
      },
      dedupe: ['vue', 'element-plus'],
    },
    css: {
      preprocessorOptions: {
        scss: {
          additionalData: `@use "@/styles/var.scss" as *;`,
        },
      },
    },
    server: {
      open: false,
      port: 5050,
      proxy: {
        '/api': {
          target: 'http://localhost:8000',
          changeOrigin: true,
          secure: false,
        },
      },
    },
    plugins: [
      vue(),
      vueJsx(),
      VueDevTools(),
      AutoImport({
        imports: [
          'vue',
          'vue-router',
          'pinia',
          '@vueuse/core',
          {
            vue: ['useTemplateRef', 'onWatcherCleanup', 'useId'],
          },
        ],
        dirs: ['src/stores', 'src/utils', 'src/hooks'],
        dts: 'src/auto-import.d.ts',
        resolvers: [ElementPlusResolver()],
      }),
      Components({
        dirs: ['src/components'],
        extensions: ['vue', 'tsx'],
        dts: 'src/components.d.ts',
        resolvers: [
          ElementPlusResolver({ importStyle: 'sass' }),
          IconsResolver({
            prefix: 'icon',
            enabledCollections: ['ep'],
          }),
        ],
      }),
      Icons({
        compiler: 'vue3',
        autoInstall: true,
        defaultClass: 'iconify-icon',
      }),
      createSvgIconsPlugin({
        iconDirs: [path.resolve(process.cwd(), 'src/assets/icons')],
        symbolId: 'icon-[dir]-[name]',
      }),
      vitePluginCompression({
        verbose: true,
        disable: false,
        deleteOriginFile: false,
        threshold: 10240,
        algorithm: 'gzip',
        ext: '.gz',
      }),
    ],
    build: {
      chunkSizeWarningLimit: 2000,
      rollupOptions: {
        output: {
          manualChunks: {
            vue: ['vue', 'vue-router', 'pinia'],
            elementPlus: ['element-plus'],
            echarts: ['echarts', 'vue-echarts'],
            utils: ['axios', 'dayjs', 'xe-utils', 'lodash-es'],
          },
        },
      },
    },
    esbuild:
      mode === 'development'
        ? undefined
        : {
            pure: ['console.log'],
            drop: ['debugger'],
            legalComments: 'none',
          },
  }
})
