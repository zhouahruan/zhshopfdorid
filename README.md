# iApp M3UI F-Droid Store (清华源镜像 F-Droid 应用商店)

基于 iApp (裕语言) 框架与 Material 3 (M3UI) 设计规范打造的独立 F-Droid 应用商店客户端，原生接入清华大学开源软件镜像站（TUNA）F-Droid 软件仓库协议。

---

## 一、 项目架构与目录结构

```text
.
├── README.md                # 项目架构与集成使用说明文档
└── src/
    ├── config.json          # 全局配置文件（默认清华源 URL、签名指纹、M3 色彩规范）
    ├── fdroid/
    │   └── fdroid.myu       # F-Droid 协议引擎（索引拉取、SQLite 数据库缓存、网络下载）
    ├── m3ui/
    │   └── m3ui.myu         # Material 3 UI 样式引擎（动态配色、圆角 Drawable、卡片阴影）
    └── views/
        ├── detail.iyu       # 应用详情页布局及逻辑
        ├── item_app.iyu     # 应用列表项 (M3 CardView Item) 组件
        ├── item_category.iyu# M3 Filter Chip 分类标签组件
        ├── m.iyu            # 主界面（顶部 M3 搜索框、分类 Chip 栏、应用列表）
        └── settings.iyu     # 软件源管理与设置页
```

---

## 二、 核心原理与 F-Droid 协议对接

### 1. 软件源与签名指纹
* **默认镜像源**: 清华大学开源软件镜像站 (TUNA)
  * `https://mirrors.tuna.tsinghua.edu.cn/fdroid/repo/`
* **公钥签名指纹 (Fingerprint)**: `43238D512C1E5EB2D6569F4A3AFBF5523418B82E0A3ED1552770ABB9A9C9CCAB`

### 2. 索引拉取与 SQLite 本地缓存机制
由于 F-Droid 源索引文件（`index-v1.json` 或 `index-v2.json`）解压后体积较大，客户端采取以下优化策略：
1. **压缩包拉取**: 下载并解压 `index-v1.jar`。
2. **签名校验**: 校验 JAR 包内的证书指纹是否与配置的指纹匹配，防范中间人篡改。
3. **SQLite 本地化**: 解析 JSON 后增量写入本地 SQLite 数据库 (`fdroid_store.db`)。
4. **高效查询**: 分页、分类过滤与搜索全部在本地数据库通过 SQL 快速响应，避免重复请求大文件。

---

## 三、 Material 3 (M3UI) 视觉规范

本项目全面引入 Android Material 3 视觉标准：
* **动态色彩 (Color Palette)**:
  * Primary: `#0061A4` / Primary Container: `#D1E4FF`
  * Surface: `#FDFCFF` / Surface Variant: `#DFE2EB`
* **形状与组件 (Shapes & Components)**:
  * **搜索框**: 28dp 全圆角 Pill Shape 悬浮搜索栏。
  * **卡片**: 16dp 圆角 M3 Surface Elevated Card。
  * **分类 Chip**: 24dp 交互式 M3 Filter Chip。
  * **按钮**: 30dp M3 Filled & Tonal Button。

---

## 四、 iApp 项目导入与编译指南

1. 打开 **iApp** 软件。
2. 创建或导入项目，将 `src/` 下的 `.myu` 函数库放入项目 `myu` 目录，将 `src/views/` 下的 `.iyu` 界面布局放入 `iyu` 目录。
3. 确保项目权限声明中开启以下 Android 权限：
   * `android.permission.INTERNET` (网络访问)
   * `android.permission.WRITE_EXTERNAL_STORAGE` (存储 APK 及缓存)
   * `android.permission.REQUEST_INSTALL_PACKAGES` (安装应用程序)
4. 运行或打包 APK。
