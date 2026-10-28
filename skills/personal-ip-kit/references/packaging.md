# 打包输入

脚本使用 Python 3 和 Pillow。优先选择环境已有的含 Pillow 的 Python；缺少时可用 `uv run --no-project --with pillow python`，无需向项目写入依赖。

所有文件路径都相对于 source，必须存在且不能越出 source。脚本不扫描整个项目，只收集资产、提示词、参考图和 documents 中列出的文档。不要把凭据或无关文件放入清单。

```json
{
  "name": "角色名",
  "version": "1.0",
  "assets": [
    {
      "id": "avatar",
      "title": "社交头像",
      "path": "images/avatar.png",
      "alpha": false,
      "promptFile": "prompts/avatar.txt",
      "references": ["reference/original.jpg", "reference/master.png"]
    }
  ],
  "documents": ["品牌手册.md", "验收记录.md"]
}
```

- assets 至少一项，id 和 path 不重复；alpha 必须是布尔值。
- alpha=true 的资产必须有真实透明像素，也有可见像素；有 RGBA 通道但全不透明不算透明素材。
- promptFile 和 references 必填，不能把没有用过的图列为已引用参考。引用至少一张实际参考图。
- 文档可省略，完整套装通常包含品牌手册、使用说明和视觉验收记录。
- 输入兼容已有角色素材 manifest 的这些字段；历史绝对路径 source 等字段不写入导出 manifest。
- 输出文件 index.html、manifest.json 保留给脚本，不能作为输入文件路径。
- 目标目录及其同名 .zip 都必须不存在。重做时使用新版本名。

```sh
python scripts/package_kit.py --source /absolute/source-kit --plan /absolute/asset-plan.json --output /absolute/deliverable-v1
```

输出为 deliverable-v1/index.html、manifest.json、所列素材与相邻 deliverable-v1.zip。
预览页可离线打开，支持背景切换、单图下载和文档下载。manifest 保存实际尺寸、颜色模式、透明范围与所有收录文件的哈希。打开页面检查可用性，脚本不会判断角色是否相像。
