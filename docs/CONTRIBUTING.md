# Contributing to AI Analyst MVP

Thank you for your interest in contributing to the AI Analyst MVP! This document provides guidelines and instructions for contributors.

## 🚀 Getting Started

### Prerequisites
- Node.js 18+ and npm
- Python 3.9+
- Google Cloud SDK
- Git

### Development Setup

1. **Fork and Clone**
   ```bash
   git clone https://github.com/YOUR_USERNAME/ai-analyst.git
   cd ai-analyst
   ```

2. **Backend Setup**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   cp .env.example .env
   # Configure your environment variables
   ```

3. **Frontend Setup**
   ```bash
   cd frontend
   npm install
   cp .env.local.example .env.local
   # Configure your environment variables
   ```

4. **ML Pipeline Setup**
   ```bash
   cd ml
   pip install -r requirements.txt
   ```

## 📋 Development Workflow

### Branch Naming Convention
- Feature branches: `feature/short-description`
- Bug fixes: `fix/bug-description`
- Documentation: `docs/update-description`
- Refactoring: `refactor/component-name`

### Commit Messages
Follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
type(scope): short description

[optional body]

[optional footer]
```

Examples:
- `feat(backend): add OCR pipeline for PDF processing`
- `fix(frontend): resolve file upload validation issue`
- `docs(readme): update installation instructions`

## 🧪 Testing

### Backend Tests
```bash
cd backend
python -m pytest tests/ -v
python -m pytest tests/integration/ -v --slow
```

### Frontend Tests
```bash
cd frontend
npm test
npm run test:watch  # For development
```

### ML Pipeline Tests
```bash
cd ml
python -m pytest tests/ -v
```

### End-to-End Tests
```bash
# Run full integration tests
scripts/test-e2e.sh
```

## 📝 Code Style

### Python (Backend & ML)
- Use `black` for formatting: `black .`
- Use `isort` for imports: `isort .`
- Use `flake8` for linting: `flake8 .`
- Use `mypy` for type checking: `mypy .`

### TypeScript/JavaScript (Frontend)
- Use `prettier` for formatting: `npm run format`
- Use `eslint` for linting: `npm run lint`
- Use TypeScript strict mode

### Configuration Files
All formatter and linter configurations are included in the project.

## 🗂️ Project Structure

### Adding New Features

#### Backend Endpoints
1. Add route in `backend/app/routers/`
2. Add business logic in `backend/app/services/`
3. Add data models in `backend/app/models/`
4. Add tests in `backend/tests/`

#### Frontend Components
1. Add components in `frontend/src/components/`
2. Add pages in `frontend/src/pages/`
3. Add utilities in `frontend/src/utils/`
4. Add tests in `frontend/src/__tests__/`

#### ML Pipeline
1. Add processors in `ml/pipeline/`
2. Add prompts in `ml/prompts/`
3. Add models in `ml/models/`
4. Add tests in `ml/tests/`

## 🎯 Focus Areas

We're particularly looking for contributions in:

### High Priority
- **Document Processing**: Improve OCR accuracy and parsing
- **Risk Assessment**: Enhance risk detection algorithms
- **Benchmarking**: Expand peer comparison capabilities
- **UI/UX**: Improve user experience and accessibility

### Medium Priority
- **Performance**: Optimize processing speed and memory usage
- **Testing**: Increase test coverage and add edge cases
- **Documentation**: Improve guides and API documentation
- **Monitoring**: Add better observability and metrics

### Future Enhancements
- **Multi-language Support**: Support for non-English documents
- **Real-time Processing**: Streaming analysis capabilities
- **Advanced Analytics**: More sophisticated investment metrics
- **Integration**: APIs for external investment platforms

## 🐛 Bug Reports

When reporting bugs, please include:

1. **Description**: Clear description of the issue
2. **Reproduction Steps**: Step-by-step instructions
3. **Expected Behavior**: What should happen
4. **Actual Behavior**: What actually happens
5. **Environment**: OS, browser, versions
6. **Screenshots**: If applicable
7. **Logs**: Relevant error messages

Use the bug report template in `.github/ISSUE_TEMPLATE/bug_report.md`.

## 💡 Feature Requests

For feature requests, please:

1. **Search Existing Issues**: Check if it's already requested
2. **Use the Template**: Fill out the feature request template
3. **Provide Context**: Explain the use case and value
4. **Consider Scope**: Keep requests focused and actionable

## 📖 Documentation

### API Documentation
- Backend API docs are auto-generated with FastAPI
- Access at `http://localhost:8000/docs` when running locally
- Update docstrings and type hints for accuracy

### Code Documentation
- Use clear, descriptive variable and function names
- Add docstrings for all public functions and classes
- Include examples in docstrings where helpful
- Update README files when adding new components

## 🔍 Code Review Process

### Submitting PRs
1. **Create a branch** from `main`
2. **Make focused changes** that address one issue
3. **Write tests** for new functionality
4. **Update documentation** as needed
5. **Run all tests** before submitting
6. **Create PR** with descriptive title and description

### Review Criteria
- Code follows style guidelines
- Tests are included and passing
- Documentation is updated
- Changes are focused and minimal
- Performance impact is considered

### Review Process
- All PRs require at least one review
- Automated checks must pass
- Address feedback before merging
- Squash commits when merging

## 🌟 Recognition

Contributors will be:
- Listed in the README contributors section
- Mentioned in release notes for significant contributions
- Invited to join the core team for sustained contributions

## 📞 Getting Help

- **GitHub Discussions**: For questions and general discussion
- **GitHub Issues**: For bug reports and feature requests
- **Discord**: Join our community server (link in README)
- **Email**: Contact maintainers directly for sensitive issues

## 📄 Code of Conduct

This project follows the [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md). By participating, you agree to uphold this code.

## 📜 License

By contributing, you agree that your contributions will be licensed under the same license as the project (MIT License).

---

Thank you for contributing to AI Analyst MVP! 🚀