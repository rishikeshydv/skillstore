---
name: direct-readable-code
description: Write, edit, refactor, test, and review code in a direct human-readable style optimized for first-pass understanding. Use for implementation, bug fixes, refactors, code review, examples, tests, configuration, scripts, and application code in any language. Favor meaningful domain abstractions, explicit contracts, cohesive workflows, declarative mappings, guard clauses, typed data models, short docstrings, and readable pure collection transformations; avoid robotic over-engineering, generic layers, fragmented micro-functions, stateless utility classes, speculative architecture, custom result wrappers, hidden control flow, and unrelated rewrites.
---

# Direct Readable Code

## Goal

Write code that a competent developer can understand on the first pass.

Use the simplest structure that makes the domain, state, operation, contract, control flow, and side effects clear. Do not equate simplicity with avoiding every abstraction. Introduce an abstraction when it gives a real concept a useful name or establishes a meaningful boundary. Reject abstractions that only move obvious code elsewhere or make the reader navigate more files and layers.

Treat the user's rated examples as the highest-authority style evidence. Read [references/preferred-examples.md](references/preferred-examples.md) and [references/avoid-examples.md](references/avoid-examples.md) when choosing between plausible structures, performing a style-focused refactor, or reviewing the final implementation.

## Operating priorities

Apply these priorities in order:

1. Preserve correctness, security, required behavior, and public compatibility.
2. Follow the repository's established architecture, naming, formatting, dependency, and error-handling conventions.
3. Make the requested change with the smallest coherent diff.
4. Apply this skill's style to new and directly modified code.
5. Optimize only for a stated requirement or a measured bottleneck.
6. Prefer clarity over cleverness and brevity when they conflict.

Do not rewrite unrelated code merely to impose this style. When an existing repository convention materially conflicts with this skill, preserve repository consistency unless the user explicitly requests a broader style migration.

## Work process

1. Inspect the relevant code, tests, types, and nearby conventions before editing.
2. Identify the smallest coherent behavior change.
3. Decide whether each proposed function, class, interface, model, mapping, or wrapper earns its place.
4. Implement the behavior with visible control flow and localized side effects.
5. Run the relevant formatter, linter, type checker, and tests when available.
6. Review the result against the final checklist before presenting it.

## Abstraction decision test

Before adding a layer, ask whether it does at least one of these jobs:

- Name a real domain concept or policy.
- Own meaningful state, identity, lifecycle, or invariants.
- Define a useful contract at a dependency or module boundary.
- Encapsulate a recognizable operation that deserves a stable name.
- Centralize behavior that is conceptually the same, not merely textually similar.
- Represent uniform cases more clearly as data or dispatch.
- Reduce cognitive load without hiding important behavior.

If none applies, keep the logic local and direct.

## Functions and cohesive workflows

- Keep a short, linear, single-purpose workflow together when reading it top to bottom is easier than jumping among helpers.
- Extract a function when its name communicates a meaningful operation, domain rule, or reusable policy.
- Prefer a domain-specific helper such as `fetch_user_settings` over a generic configurable helper such as `request_json` when only the domain operation is needed.
- Permit a focused helper even at one call site when it cleanly encapsulates a recognizable operation, such as fetching and validating JSON.
- Extract repeated logic such as email normalization when the repetitions represent the same concept.
- Avoid predicate and accessor micro-functions that merely replace obvious expressions and make a simple transformation harder to scan.
- Avoid splitting one clear workflow into `build`, `ensure`, and `save_and_notify` helpers unless those operations are independently complex, reused, or tested as distinct domain behavior.
- Use meaningful names. Avoid vague names such as `process_data`, `handle_item`, `manager`, `utils`, `temp`, or `result` when a more specific name is available.

## Classes, data models, and contracts

- Use a class when it represents a real domain concept or owns meaningful state and behavior.
- Use a data class, record, struct, schema, or typed object when named fields make the data model easier to understand, even in a small script.
- Use an interface, protocol, trait, or abstract contract at a meaningful dependency boundary when it clarifies what a caller requires or improves substitution and testing. A single current implementation does not automatically make the contract unnecessary.
- Keep contracts small and shaped around the consumer's actual needs.
- Use a plain function for a stateless operation.
- Do not create a class only to hold static methods or to provide a namespace.
- Do not add factories, adapters, service layers, wrappers, registries, or plugin systems for hypothetical future variation.

## Control flow and side effects

- Prefer guard clauses when they keep the main path visible and avoid deep nesting.
- Use explicit branches for absence, invalid input, and important business conditions.
- Introduce intermediate variables when they expose an important step or give a value a meaningful name.
- Avoid ternaries, chained calls, and one-liners that hide branches or failure cases.
- Keep database writes, network calls, file operations, notifications, and other side effects visible in the workflow.
- Use lookup tables for uniform value selection and dispatch maps for uniform behavior selection when they make supported cases visible in one place.
- Raise an explicit error for unsupported dispatch keys instead of failing later or silently doing nothing.

## Collection transformations

- Prefer an idiomatic comprehension or equivalent language construct for a pure filtering and mapping pipeline.
- Format comprehensions across multiple lines when that improves scanning.
- Permit multiple `for` and `if` clauses when the expression still reads as one linear, side-effect-free transformation and the produced value is obvious.
- Do not replace a readable comprehension with a longer imperative loop merely because it has several clauses.
- Use an explicit loop when the operation has side effects, mutable state beyond accumulation, early exits, retries, exception handling, complex branching, or an opaque expression.
- Avoid `map` or `filter` combined with trivial helper functions when a direct loop or comprehension communicates the transformation more clearly.

## Error handling and validation

- Use the repository's normal exception or error mechanism.
- Raise ordinary, specific exceptions when failure should stop the operation.
- Do not introduce a custom generic `Result` wrapper unless the surrounding API intentionally models recoverable outcomes that way.
- Validate untrusted data at system boundaries, not repeatedly at every internal call.
- Do not swallow errors or add defensive checks for states the architecture already prevents.
- Preserve error causes when translating exceptions.

## Tests

- Write tests as readable behavior statements.
- Prefer separate, specifically named tests for distinct behaviors, including fallback and error behavior.
- Keep each test's setup and assertion close enough to understand without decoding a data table.
- Use parameterization only when many cases exercise exactly the same behavior and the individual intent remains obvious.
- Test meaningful behavior, not implementation trivia or coverage numbers alone.

## Documentation and comments

- Add a short one-sentence docstring to public functions, reusable helpers, domain operations, and small functions whose purpose benefits from being stated explicitly.
- Keep docstrings concise; do not repeat every implementation detail.
- Use comments to explain business rules, constraints, compatibility decisions, security concerns, workarounds, or surprising choices.
- Do not comment obvious syntax line by line.
- Explain a meaningful implementation trade-off briefly; do not justify routine choices at length.

## Scope and maintenance

- Preserve backward compatibility unless the task explicitly changes it.
- Reuse trusted language and framework features before adding dependencies.
- Avoid speculative configuration and extension points.
- Keep related logic localized so a future change does not require tracing behavior through many layers.
- Do not rename, reformat, move, or refactor unrelated code during a focused task.
- Prefer a boring implementation that is easy to debug over a sophisticated implementation that only looks impressive.

## Final review checklist

Before presenting code, verify all of the following:

- Can a developer understand the main behavior on the first read?
- Are domain concepts and data shapes named explicitly?
- Does every helper, class, interface, and wrapper have a concrete present purpose?
- Is a cohesive workflow kept together rather than fragmented into micro-functions?
- Are pure collection transformations concise and free of side effects?
- Are control flow, errors, and side effects visible?
- Are classes used for state or domain modeling rather than namespacing?
- Are interfaces limited to meaningful boundaries and actual consumer needs?
- Are tests written as distinct behavior stories?
- Are docstrings short and useful, and are comments about why rather than what?
- Does the diff avoid unrelated changes and hypothetical architecture?
- Were relevant checks and tests run?

If an important answer is no, simplify or improve the implementation before presenting it.