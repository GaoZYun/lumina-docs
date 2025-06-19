# 项目重命名总结 / Project Rename Summary

## 项目名称变更 / Project Name Change

**旧名称 / Old Name**: Document Manager  
**新名称 / New Name**: **Lumina Docs**

## 主要变更 / Major Changes

### 1. 配置文件更新 / Configuration Updates

- 默认服务器名称：`document-manager` → `lumina-docs`
- 默认数据目录：`~/.doc-manager` → `~/.lumina-docs`
- 环境变量：`DOC_MANAGER_SERVER_NAME` → `LUMINA_DOCS_SERVER_NAME`

### 2. 文档更新 / Documentation Updates

- ✅ 创建了英文版 README (`README.en.md`)
- ✅ 中文版 README 添加语言切换链接
- ✅ 更新了所有配置示例文件
- ✅ 更新了安装脚本和说明

### 3. 配置模板文件 / Configuration Templates

所有 Claude Desktop 配置模板都已更新：
- `claude_desktop_config.example.json`
- `claude_desktop_config.macos.json`
- `claude_desktop_config.conda.json`
- `claude_desktop_config.multi.json`

### 4. 脚本文件更新 / Script Updates

- `install_to_claude_desktop.sh` - 安装脚本
- `run_server.sh` - 启动脚本
- `docker-compose.example.yml` - Docker 配置

### 5. 代码更新 / Code Updates

- `src/doc_manager/config.py` - 配置管理
- `src/doc_manager/simple_server.py` - 服务器描述
- `.env.example` - 环境变量模板

## 向后兼容性 / Backward Compatibility

为了保持兼容性，以下环境变量仍然有效：
- `DOC_MANAGER_DB_PATH`
- `DOC_MANAGER_EXPORT_DIR`
- `DOC_MANAGER_DATA_DIR`
- `DOC_MANAGER_DEBUG`
- `DOC_MANAGER_LOG_LEVEL`

只有服务器名称相关的变量发生了变化：
- `DOC_MANAGER_SERVER_NAME` → `LUMINA_DOCS_SERVER_NAME`

## 升级指南 / Upgrade Guide

### 对于现有用户 / For Existing Users

1. **更新 Claude Desktop 配置**：
   ```bash
   # 备份现有配置
   cp ~/Library/Application\ Support/Claude/claude_desktop_config.json ~/Library/Application\ Support/Claude/claude_desktop_config.json.backup
   
   # 更新服务器名称（可选）
   # 将 "document-manager" 改为 "lumina-docs"
   ```

2. **更新环境变量（可选）**：
   ```bash
   # 如果使用了自定义服务器名称，更新环境变量
   # DOC_MANAGER_SERVER_NAME → LUMINA_DOCS_SERVER_NAME
   ```

3. **数据迁移**：
   ```bash
   # 如果想要使用新的默认数据目录
   mv ~/.doc-manager ~/.lumina-docs
   ```

### 对于新用户 / For New Users

直接使用新的配置模板和文档即可，无需额外操作。

## 语言支持 / Language Support

现在项目支持中英文双语：

- **中文文档**: `README.md`
- **English Documentation**: `README.en.md`

每个 README 顶部都有语言切换链接。

## 下一步 / Next Steps

1. 测试新配置是否正常工作
2. 更新 GitHub 仓库名称（如果需要）
3. 发布新版本
4. 通知用户进行升级

---

**Note**: 这个文件是为了记录重命名过程，在正式发布时可以删除。  
**注意**: 此文件用于记录重命名过程，正式发布时可删除此文件。