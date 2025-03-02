# Contributing to Globetrotter

Thank you for your interest in contributing to Globetrotter! This document provides guidelines and instructions for contributing to the project.

## Code of Conduct

By participating in this project, you agree to abide by our Code of Conduct. Please read it before contributing.

- Be respectful and inclusive
- Focus on constructive feedback
- Maintain a harassment-free environment
- Show empathy towards others

## Getting Started

1. Fork the repository
2. Clone your fork locally
3. Set up the development environment following the README instructions
4. Create a new branch for your feature/fix

```bash
git checkout -b feature/your-feature-name
```

## Development Process

### Environment Setup

1. Install dependencies for both frontend and backend
2. Set up the database and Redis using Docker
3. Configure environment variables
4. Run the development servers

### Code Style

#### Frontend (TypeScript/React)

- Use TypeScript for all new code
- Follow the existing code style
- Use functional components and hooks
- Write meaningful component and function names
- Add proper TypeScript types
- Use proper error handling

#### Backend (Python/FastAPI)

- Follow PEP 8 style guide
- Use type hints
- Document functions and classes
- Handle errors appropriately
- Write meaningful variable and function names

### Testing

- Write tests for new features
- Ensure existing tests pass
- Run the test suite before submitting PR
- Add both unit and integration tests where appropriate

### Commit Guidelines

Follow the conventional commits specification:

- `feat:` New features
- `fix:` Bug fixes
- `docs:` Documentation changes
- `style:` Code style changes (formatting, etc)
- `refactor:` Code refactoring
- `test:` Test updates
- `chore:` Routine tasks, maintenance

Example:

```bash
git commit -m "feat: add user achievement system"
```

## Pull Request Process

1. Update documentation for any new features
2. Add or update tests as needed
3. Ensure all tests pass
4. Update the README if necessary
5. Create a detailed PR description

### PR Title Format

Use the same format as commit messages:

```
feat: add user authentication system
```

### PR Description Template

```markdown
## Description
Brief description of the changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## How Has This Been Tested?
Describe the tests you ran

## Checklist
- [ ] My code follows the style guidelines
- [ ] I have performed a self-review
- [ ] I have commented my code where needed
- [ ] I have updated the documentation
- [ ] My changes generate no new warnings
- [ ] I have added tests that prove my fix/feature works
- [ ] New and existing tests pass
```

## Review Process

1. Maintainers will review your PR
2. Address any requested changes
3. Once approved, your PR will be merged

## Development Guidelines

### Frontend

1. Component Structure
   - Keep components small and focused
   - Use proper file naming conventions
   - Place shared components in appropriate directories

2. State Management
   - Use React Query for server state
   - Use React hooks for local state
   - Avoid prop drilling

3. Styling
   - Use Tailwind CSS
   - Follow the existing design system
   - Maintain responsive design

### Backend

1. API Design
   - Follow RESTful principles
   - Use proper HTTP methods
   - Implement proper error handling
   - Document all endpoints

2. Database
   - Write clean SQL/ORM queries
   - Handle migrations properly
   - Consider performance implications

3. Security
   - Validate all inputs
   - Implement proper authentication
   - Follow security best practices

## Questions?

If you have questions, please:

1. Check existing issues
2. Create a new issue with the question
3. Tag it with the 'question' label

## License

By contributing, you agree that your contributions will be licensed under the project's MIT License.
