# 前端静态文件目录

请将前端构建产物( dist 文件夹)放置于此目录。

当前 nginx 配置读取 `docker/nginx/web/dist`，构建后应包含：
- index.html
- js/、css/、img/ 等静态资源目录

示例：

```bash
cd frontend/web
pnpm install
pnpm run build
cd ../..
mkdir -p docker/nginx/web
# cp -r 你的前端项目/dist ./
cp -R frontend/web/dist docker/nginx/web/

最终目录结构应为:
```
docker/nginx/web/
└── dist/
    ├── index.html
    ├── static/
    └── ...

```
