# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is the Home-schooling-App repository - an educational application designed to support homeschooling workflows. The project is in its initial stages and will contain frontend, backend, and supporting infrastructure for educational content delivery and tracking.

## Project Structure

As the project grows, organize code by domain:
- Frontend: `/frontend`, `/client`, `/ui` (depending on framework choice)
- Backend: `/backend`, `/server`, `/api`
- Shared utilities: `/lib`, `/utils`, `/common`
- Tests: Co-located with source or `/tests`
- Documentation: `/docs`
- Configuration: Root level or `/config`

## Getting Started (Template for Future Development)

### Prerequisites
- Node.js/npm or Python/pip (depending on tech stack choice)
- Database client (if applicable)
- Git for version control

### Setup
When dependencies are added, include:
1. Installation instructions
2. Environment configuration (.env.example)
3. Database setup (if applicable)
4. Initial data seeding instructions

### Development Workflow

As features are implemented, document:
1. How to start the development server/environment
2. Frontend development server (if applicable)
3. Backend API server (if applicable)
4. How to run tests (unit, integration, e2e)
5. How to run a single test or test suite
6. Linting and code formatting commands
7. Database migration procedures

### Testing
Add testing framework details when implemented:
- Unit test command and file patterns
- Integration test setup
- E2E test procedures (if applicable)

### Linting & Code Style
Add code quality tools configuration when established:
- Linter commands
- Code formatter commands
- Pre-commit hook setup

## Key Conventions

- **Branch Strategy**: Feature branches from `main`, merged via pull requests
- **Commit Messages**: Clear, descriptive messages explaining changes
- **Feature Development**: Include tests and documentation with feature code
- **Component Organization**: Keep related components together; avoid deep nesting
- **Data Models**: Document data structures and relationships
- **API Design**: RESTful endpoints (if applicable) should be consistent and well-documented

## Git Workflow

1. Create a feature branch from `main` with descriptive name
2. Implement features with clear, atomic commits
3. Include tests with feature code
4. Push to remote and create pull request
5. Address review feedback
6. Merge after approval

## Architecture Notes

To be added as the project develops. Include:
- Frontend framework and key libraries
- Backend technology and main services
- Database schema and key entities
- Authentication/authorization approach
- Integration points between frontend and backend
- Deployment architecture

## Configuration

Configuration management:
- Environment variables: Document in `.env.example` with descriptions
- Feature flags: Document where and how they're used
- Secrets management: Document approach (never commit secrets)

## Database

When database is implemented, document:
- Setup and migration procedures
- Schema overview (link to schema documentation)
- Seed data procedures
- Backup/restore procedures

## Deployment

To be documented as deployment strategy is determined:
- Deployment process
- Environment setup (dev, staging, production)
- Environment-specific configurations
- CI/CD pipeline details

## Troubleshooting

Common development issues and solutions will be documented here.

## User Features Overview

When features are implemented, document:
- Key user workflows (student registration, course access, progress tracking, etc.)
- Admin capabilities
- Parent/guardian features (if applicable)

## Additional Resources

- GitHub repository: ocristaogamer-glitch/home-schooling-app
- Main branch: `main`
- Development branch pattern: `claude/claude-md-docs-*`
