# Yifei Dong — Academic Homepage

响应式英文个人学术主页，可直接部署到 GitHub Pages。使用 HTML、CSS 和少量原生 JavaScript，无需安装依赖或构建；关闭 JavaScript 时仍可阅读全部内容。

## 本地运行

在仓库根目录执行：

```bash
python3 -m http.server 8000 --bind 0.0.0.0
```

然后通过本地浏览器访问服务器的 8000 端口。相对路径同时兼容个人域名、GitHub Pages 根站点和 `/yifei/` 项目站点。

## 文件与维护

- `index.html`：简介、动态、10 项精选成果（9 篇论文及 1 篇预印本）、独立的 Technical Reports 栏目、经历、教育、奖项与学术服务。
- `assets/styles.css`：桌面、手机与打印样式。
- `assets/main.js`：论文主题筛选；使用原生按钮和无障碍状态提示。
- `assets/images/`：旧主页头像与研究项目配图，均保存在本地。
- `assets/documents/Yifei_Dong_CV.pdf`：用户提供的最新 CV 原文件。
- `SOURCES.md`：内容与图片来源、维护注意事项。

直接修改 HTML 即可更新内容。新增论文时同步更新筛选结果计数；`data-category` 使用 `navigation` 或 `vision-language`。新增第一/共同第一作者论文时添加 `first-author` 类。没有可靠公开链接的成果仅显示文字，不使用占位链接。

## 部署

1. 将网站文件推送到 GitHub 仓库。
2. 在 **Settings → Pages → Build and deployment** 中选择 **Deploy from a branch**。
3. 选择包含这些文件的分支以及 **/ (root)**，保存。

仓库包含 `.nojekyll`，无需 Jekyll、Node.js、API 密钥、第三方统计脚本或外部字体服务。本次交付仅准备源码，不会自动推送或发布网站。

## 验证

```bash
python3 scripts/check_site.py
```

该检查验证 HTML 内部链接、本地资源、页面标识、论文数量与分类、必要个人资料和本地 CV。浏览器验证还应覆盖手机宽度、分类按钮、动态折叠、键盘访问、图片加载与 CV 下载。
