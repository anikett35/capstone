# User Story Template

## Story Title
[Brief title describing the capability or need]

### User Story Format
**As a** [role/user persona]  
**I need** [capability, action, or feature]  
**So that** [business value, benefit, or objective achieved]  

---

### Acceptance Criteria

```gherkin
Scenario: [Title of scenario 1 - Happy Path]
  Given [initial state or preconditions]
  When [action performed by the user or system]
  Then [expected outcome or assertion]

Scenario: [Title of scenario 2 - Error Handling / Edge Case]
  Given [preconditions]
  When [action performed that violates rules]
  Then [appropriate error code or message returned]
```

---

### Definition of Done (DoD)
- [ ] User story requirements fulfilled
- [ ] Automated unit test cases written with TDD
- [ ] Code passes linter checks (Flake8 and Pylint)
- [ ] Test coverage meets or exceeds 95% threshold
- [ ] Changes committed and pushed to GitHub
- [ ] CI pipeline runs and passes successfully
