# Test Suite

Professional test organization for the Automaton Auditor.

## Structure

```
tests/
├── unit/              # Fast, isolated component tests
│   ├── test_state.py
│   ├── test_rubric_loader.py
│   ├── test_detectives.py
│   └── test_judges.py
├── integration/       # Multi-component workflow tests
│   └── test_integration.py
└── manual/           # Manual validation scripts
    ├── test_phase2_manual.py
    ├── test_phase3_manual.py
    └── test_vision_setup.py
```

## Running Tests

### All Unit Tests
```bash
pytest tests/unit/ -v
```

### Specific Test File
```bash
pytest tests/unit/test_state.py -v
```

### Integration Tests
```bash
pytest tests/integration/ -v
```

### Manual Tests (require API keys)
```bash
python tests/manual/test_phase2_manual.py
python tests/manual/test_phase3_manual.py
```

### All Tests
```bash
pytest tests/ -v
```

## Test Categories

### Unit Tests
- **Fast**: < 1 second per test
- **Isolated**: No external dependencies
- **Focused**: Single component/function
- **Examples**: State models, rubric parsing, AST tools

### Integration Tests
- **Moderate**: 1-10 seconds per test
- **Connected**: Multiple components
- **Workflow**: End-to-end scenarios
- **Examples**: Detective → Judge pipeline

### Manual Tests
- **Slow**: 10+ seconds
- **External**: Requires API keys, network
- **Validation**: Real-world scenarios
- **Examples**: GitHub repo analysis, LLM evaluation

## Coverage

Run with coverage report:
```bash
pytest tests/unit/ --cov=src --cov-report=html
```

View report: `open htmlcov/index.html`

## Best Practices

1. **Unit tests**: Mock external dependencies
2. **Integration tests**: Use test fixtures
3. **Manual tests**: Document expected behavior
4. **All tests**: Clear assertions and error messages
