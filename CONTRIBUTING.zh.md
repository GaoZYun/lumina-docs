# 为 Lumina Docs 贡献代码

**中文** | [English](CONTRIBUTING.md)

我们欢迎你的贡献！我们希望让为 Lumina Docs 贡献代码变得尽可能简单和透明，无论是：

- 报告 bug
- 讨论当前代码状态
- 提交修复
- 提议新功能
- 成为维护者

## 开发流程

我们使用 GitHub 来托管代码、跟踪问题和功能请求，以及接受 pull request。

## Pull Requests

Pull request 是提议代码更改的最佳方式。我们积极欢迎你的 pull request：

1. Fork 仓库并从 `main` 分支创建你的分支。
2. 如果你添加了需要测试的代码，请添加测试。
3. 如果你更改了 API，请更新文档。
4. 确保测试套件通过。
5. 确保你的代码符合规范。
6. 提交 pull request！

## 你的贡献将遵循 MIT 软件许可证

简而言之，当你提交代码更改时，你的提交被理解为遵循覆盖项目的同一个 [MIT 许可证](http://choosealicense.com/licenses/mit/)。如果有疑虑，请随时联系维护者。

## 使用 GitHub 的 [issues](https://github.com/username/lumina-docs/issues) 报告 bug

我们使用 GitHub issues 来跟踪公开的 bug。通过[开启新 issue](https://github.com/username/lumina-docs/issues/new) 来报告 bug，就这么简单！

## 写详细的、有背景的、有示例代码的 bug 报告

**优秀的 Bug 报告** 通常包含：

- 快速摘要和/或背景
- 重现步骤
  - 要具体！
  - 尽可能提供示例代码
- 你期望发生什么
- 实际发生了什么
- 注释（可能包括你认为可能发生这种情况的原因，或你尝试过但没有用的方法）

人们*喜欢*详尽的 bug 报告。我不是在开玩笑。

## 开发环境设置

1. 克隆仓库：
   ```bash
   git clone https://github.com/username/lumina-docs.git
   cd lumina-docs
   ```

2. 安装依赖：
   ```bash
   pip install -e .
   ```

3. 创建示例数据：
   ```bash
   cd examples
   python sample_data.py
   ```

4. 运行服务器：
   ```bash
   python -m doc_manager
   ```

## 代码风格

- 我们使用 Python 3.8+ 特性
- 遵循 PEP 8 风格指南
- 在适当的地方使用类型提示
- 为所有公共函数和类编写文档字符串
- 保持函数专注和小巧

## 测试

- 为任何新功能添加测试
- 运行现有测试以确保没有破坏：
  ```bash
  python -m pytest tests/
  ```

## 文档

- 如果你更改了功能，请更新 README.md
- 如果适用，请更新英文和中文版本
- 在文档字符串中包含代码示例
- 如果需要，请更新配置示例

## 功能请求

我们欢迎功能请求！请：

1. 检查功能是否已经存在或已计划
2. 开启带有 "enhancement" 标签的 issue
3. 描述功能及其用例
4. 讨论实现方法

## 代码审查流程

核心团队定期查看 Pull Request。我们会提供反馈并与你合作将你的更改合并。

## 社区

- 保持尊重和包容
- 帮助他人学习和成长
- 分享知识和最佳实践
- 欢迎新手

## 认可

贡献者将在我们的 README 和发布说明中得到认可。重要贡献者可能会被邀请加入核心团队。

## 获取帮助

- 查看[文档](README.md)
- 搜索[现有 issues](https://github.com/username/lumina-docs/issues)
- 在[讨论区](https://github.com/username/lumina-docs/discussions)提问

## 许可证

通过贡献，你同意你的贡献将在其 MIT 许可证下获得许可。

## 参考

本文档改编自 [Facebook's Draft](https://github.com/facebook/draft-js/blob/a9316a723f9e918afde44dea68b5f9f39b7d9b00/CONTRIBUTING.md) 的开源贡献指南