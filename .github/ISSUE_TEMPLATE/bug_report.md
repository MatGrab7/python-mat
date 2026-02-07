name: Bug Report
description: Report a code quality or security issue
title: "[BUG] "
labels: ["bug", "needs-review"]
body:
  - type: markdown
    attributes:
      value: |
        Thanks for reporting an issue! Please provide as much detail as possible.
  - type: dropdown
    id: type
    attributes:
      label: Issue Type
      options:
        - Code Quality
        - Security/Secrets
        - Performance
        - Other
    validations:
      required: true
  - type: textarea
    id: description
    attributes:
      label: Description
      description: Describe the issue
      placeholder: Describe what needs to be fixed...
    validations:
      required: true
  - type: textarea
    id: location
    attributes:
      label: File Location
      description: Where is the issue located?
      placeholder: "File: src/module.py, Line: 42"
    validations:
      required: true
  - type: textarea
    id: reproduction
    attributes:
      label: How to Reproduce
      description: Steps to reproduce the issue
      placeholder: |
        1. Run the code quality scan
        2. Check the results
        3. See the issue
  - type: textarea
    id: suggested_fix
    attributes:
      label: Suggested Fix
      description: Any suggestions on how to fix this?
