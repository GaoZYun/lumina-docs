# Contributing to Lumina Docs

[中文](CONTRIBUTING.zh.md) | **English**

We love your input! We want to make contributing to Lumina Docs as easy and transparent as possible, whether it's:

- Reporting a bug
- Discussing the current state of the code
- Submitting a fix
- Proposing new features
- Becoming a maintainer

## Development Process

We use GitHub to host code, to track issues and feature requests, as well as accept pull requests.

## Pull Requests

Pull requests are the best way to propose changes to the codebase. We actively welcome your pull requests:

1. Fork the repo and create your branch from `main`.
2. If you've added code that should be tested, add tests.
3. If you've changed APIs, update the documentation.
4. Ensure the test suite passes.
5. Make sure your code lints.
6. Issue that pull request!

## Any contributions you make will be under the MIT Software License

In short, when you submit code changes, your submissions are understood to be under the same [MIT License](http://choosealicense.com/licenses/mit/) that covers the project. Feel free to contact the maintainers if that's a concern.

## Report bugs using Github's [issues](https://github.com/username/lumina-docs/issues)

We use GitHub issues to track public bugs. Report a bug by [opening a new issue](https://github.com/username/lumina-docs/issues/new); it's that easy!

## Write bug reports with detail, background, and sample code

**Great Bug Reports** tend to have:

- A quick summary and/or background
- Steps to reproduce
  - Be specific!
  - Give sample code if you can
- What you expected would happen
- What actually happens
- Notes (possibly including why you think this might be happening, or stuff you tried that didn't work)

People *love* thorough bug reports. I'm not even kidding.

## Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/username/lumina-docs.git
   cd lumina-docs
   ```

2. Install dependencies:
   ```bash
   pip install -e .
   ```

3. Create sample data:
   ```bash
   cd examples
   python sample_data.py
   ```

4. Run the server:
   ```bash
   python -m doc_manager
   ```

## Code Style

- We use Python 3.8+ features
- Follow PEP 8 style guidelines
- Use type hints where appropriate
- Write docstrings for all public functions and classes
- Keep functions focused and small

## Testing

- Add tests for any new functionality
- Run existing tests to ensure nothing breaks:
  ```bash
  python -m pytest tests/
  ```

## Documentation

- Update README.md if you change functionality
- Update both English and Chinese versions if applicable
- Include code examples in docstrings
- Update configuration examples if needed

## Feature Requests

We welcome feature requests! Please:

1. Check if the feature already exists or is planned
2. Open an issue with the "enhancement" label
3. Describe the feature and its use case
4. Discuss implementation approaches

## Code Review Process

The core team looks at Pull Requests on a regular basis. We'll provide feedback and work with you to get your changes merged.

## Community

- Be respectful and inclusive
- Help others learn and grow
- Share knowledge and best practices
- Welcome newcomers

## Recognition

Contributors will be recognized in our README and release notes. Significant contributors may be invited to join the core team.

## Getting Help

- Check the [documentation](README.md)
- Search [existing issues](https://github.com/username/lumina-docs/issues)
- Ask questions in [discussions](https://github.com/username/lumina-docs/discussions)

## License

By contributing, you agree that your contributions will be licensed under its MIT License.

## References

This document was adapted from the open-source contribution guidelines for [Facebook's Draft](https://github.com/facebook/draft-js/blob/a9316a723f9e918afde44dea68b5f9f39b7d9b00/CONTRIBUTING.md)