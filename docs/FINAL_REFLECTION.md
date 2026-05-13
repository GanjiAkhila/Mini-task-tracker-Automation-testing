# Final Reflection

## 1. What did AI do well?

AI generated a complete project structure quickly, kept the layers separated, and covered the requested CRUD, search, filter, and validation features in one pass.

## 2. Where did AI fail?

AI could not fully prove GUI runtime behavior without a local PySide6 runtime already installed in the environment, so the final verification depended partly on static checks and test coverage.

## 3. What bugs did AI introduce?

No confirmed bugs were found during the code review and validation test run. Any future issues are most likely to be UI polish or environment-specific Qt behavior rather than architectural mistakes.

## 4. Did AI follow MVC properly?

Yes. The `Task` dataclass is isolated in the model, Qt widgets stay in the views, user-flow coordination sits in the controller, SQLite access stays in the repository, and validation stays in the service layer.

## 5. What did humans need to correct?

Humans mainly needed to review naming, UX choices, and environment setup expectations. No major structural correction was required in the generated code.

## 6. Which prompt worked best?

The most effective prompt was the one that explicitly defined the required features, the MVC rules, the exact folder structure, and the documentation/test expectations in the same instruction.

## 7. What would you do differently next time?

Next time, I would add repository unit tests with a temporary SQLite database and a small controller integration test plan so verification goes beyond validation-only tests.
