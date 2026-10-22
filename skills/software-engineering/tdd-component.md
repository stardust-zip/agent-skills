---
name: tdd-component
description: Use this when the user asks to create a new UI component, function, or service class.
---

## The Procedure

When asked to build a new feature or component, you must strictly follow this order of operations:

1. **Write the Interface/Type definition first.** Define the inputs and outputs clearly. Do not write implementation logic yet.
2. **Write the Unit Test.** Create a test file that imports the interface and mocks the inputs. Write assertions for the expected outputs and edge cases.
3. **Wait for user review.** Present the interface and the test. Ask the user if the contract looks correct.
4. **Implement the logic.** Only after the test is approved, write the actual code to make the test pass.

## Constraints

- Ensure the component has a single responsibility.
- Inject any external dependencies (API calls, state management) rather than hardcoding them.
