---
name: api-docs
description: Writes API docs for REST, GraphQL, gRPC or event APIs - reference spec, usage guide, verified examples and change notes, linted with real tools. Use for API docs, OpenAPI/proto/GraphQL/AsyncAPI specs, integration guides or API contracts.
---

# API Docs

The user is a fullstack engineer at a large tech company, fairly new in the role. They work across microservices, and each one may expose a different kind of API. Their docs are read by engineers who will integrate without talking to them, so the test of a good result is simple: **another engineer can call the API correctly from the docs alone.**

## Conventions

- `{skill-root}` is the folder containing this SKILL.md. If your tool did not say where that is, find this skill's folder by name under `.claude/skills` in the current repository, `~/.claude/skills`, `~/.codex/skills`, `~/.agents/skills`, `~/.gemini/antigravity-cli/skills` or `~/.config/opencode/skills/software-engineering`.
- `{service-root}` is the Git root of the service that owns the API. If the current directory is an umbrella repo that only aggregates services, ask which service to document.
- Style references, loaded only for the styles actually present:
  - REST / HTTP: `references/rest-openapi.md`
  - GraphQL: `references/graphql.md`
  - gRPC / protobuf: `references/grpc.md`
  - Events, message queues, webhooks: `references/events.md`
- Usage guide template: `assets/usage-guide.md`.
- Local `AGENTS.md`, `CLAUDE.md`, and the repo's own doc and lint conventions take precedence over this skill's defaults.
- Reply to the user in the language they write in. Write the docs in English unless the user says their team documents in another language.

## Work machine: no Markdown in the repository

Check whether `~/work-docs/` exists. If it does, this is a work machine, and company policy forbids pushing Markdown files to the work Git host. Then:
- Every `.md` file (the usage guide, the changelog) goes to `~/work-docs/<repo-name>/` plus the path it would have had in the repository, for example `~/work-docs/<repo-name>/docs/api/README.md`. Never write a `.md` file inside the repository.
- Spec files (`openapi.yaml`, `.proto`, `schema.graphql`, `asyncapi.yaml`) and descriptions in code annotations are not Markdown. They stay in the repository as usual.
- Links from the guide to the spec use the spec's path in the repository, written as text, since the guide no longer sits next to it.

## Must not invent

Docs that are wrong are worse than docs that are missing, because consumers build on them. Never make up any of these. Take them from code, config or the user, or mark them:

- Auth schemes, scopes, roles and who may call what.
- Rate limits, quotas, timeouts, payload size limits, SLAs.
- Error codes, error shapes or status codes the code does not produce.
- The meaning of a field, when the name and code do not make it clear.
- Base URLs, hostnames, topic names, environment names.
- Delivery guarantees, ordering, retention, idempotency behaviour.
- Version numbers, deprecation dates, sunset dates.

Mark an unknown inline as `TODO(owner): <what is missing>`, and list every TODO in the end-of-run report. A field described as "The user ID" because it is called `userId` is fine. A field called `status` with no visible enum or comment gets a TODO, not a guess.

## Workflow

### 1. Survey the service

Read before asking. Work out three things.

**Which API styles exist.** A service often has more than one: a REST API plus the events it publishes is common. Look for:
- REST: `openapi.*`, `swagger.*`, route or controller definitions, framework annotations.
- GraphQL: `*.graphql`, `*.gql`, `schema.*`, resolver modules, a GraphQL server dependency.
- gRPC: `*.proto`, `buf.yaml`, `buf.gen.yaml`, generated stubs.
- Events: `asyncapi.*`, producer or consumer code, topic or queue config, schema-registry config (Avro, Protobuf, JSON Schema), outgoing webhook senders.

Load the reference file for each style found.

**Which starting case applies,** per style:
- **Spec exists**: improve and complete it. Check it against the code; where they disagree, the code is what consumers actually get, so flag every mismatch rather than silently picking one.
- **Spec generated from code** (FastAPI, NestJS, springdoc and similar; see the reference file): document in the code annotations and docstrings, not in a hand-written spec that will drift. The generated spec is the output.
- **Code only**: reverse-engineer the spec from the code.
- **Nothing built yet**: this is a spec-first contract. The spec is a proposal for the consuming team to agree. Mark it `Status: Draft contract`. If the contract hides real design choices (sync or async, which service owns the data), say so and suggest the `design-doc` skill first.

**House conventions.** Existing docs location and format, a developer portal config (for example `catalog-info.yaml`, `mkdocs.yml`, a docs site), lint configs (`.redocly.yaml`, `.spectral.yaml`, `buf.yaml`, GraphQL lint config), and package scripts that lint or generate specs. Use them over this skill's defaults.

**Consumers and providers.** When the API calls other services or is called by them, use the `service-map` skill to find their real contracts. After documenting, offer to update this service's catalog entry (spec path, environments).

### 2. Interview the user

One round, two to five questions in a single message, after the survey. Use a structured question tool if available; otherwise a numbered list. Always allow "I don't know".

Always ask, unless already stated:
- **Who reads these docs: internal teams, or external partners or public developers?** External docs need more on auth, onboarding, rate limits and errors, and must not expose internal hostnames, internal service names or internal-only endpoints.
- **Besides curl (or grpcurl, or a raw GraphQL request), which languages do the consumers use?** Write client snippets only for those.

Then pick from:
- **Scope**: the whole API, or specific endpoints, operations or topics?
- **Previous version for change notes**: default is the spec on the main branch, or the latest release tag if the repo tags releases.
- **Verification environment**: is there an environment where examples may be checked (see step 5)? Which credentials, passed how?
- **For a spec-first contract**: what has the consuming team already asked for or agreed?

### 3. Extract the facts

For each operation, query, RPC or message, collect from the code: name, inputs and their types and constraints, outputs, every success and error outcome the code can produce, auth requirements, pagination, idempotency, and side effects. Follow the code paths, including middleware, interceptors, validators and error handlers; that is where auth, validation errors and error shapes usually live.

Note file paths as you go. Anything you could not confirm becomes a `TODO(owner)`.

### 4. Write the reference spec

Follow the reference file for the style. Rules for every style:
- Every operation and every field has a description a consumer can act on: what it is, units, format, allowed values, and what happens at the edges (empty, missing, too large).
- Every error outcome is documented with when it happens and what the caller should do about it.
- Reuse shared definitions instead of repeating them.
- Use the spec format version the repo already uses. For a new spec, use the current major version named in the reference file.

### 5. Write examples, and verify them if allowed

Write examples for the main flows: at least the most common call, an error case, and a paginated or streaming call if the API has one. Always curl (grpcurl for gRPC, a raw HTTP POST for GraphQL, a sample payload for events), plus the languages from the interview.

Use placeholders for anything secret or environment-specific: `$API_TOKEN`, `$BASE_URL`, `<order-id>`.

Verification is optional and needs the user's approval for each run, naming the environment. When approved:
- Start with read-only calls. A call that creates, changes or deletes anything needs its own explicit approval, listed as the exact call before it runs.
- Never make a creating, changing or deleting call against production, even if approved in general. Say so and verify it elsewhere or leave it unverified.
- Never publish events to a shared topic or queue. Consuming to verify a payload shape is allowed only with approval, and without committing offsets for an existing consumer group.
- Take credentials from environment variables the user names. Never ask for a secret in the chat, and never write one into a file.
- Before an actual response goes into the docs, replace real IDs, names, emails, tokens and any other personal or customer data with realistic fake values.
- Label every example `verified against <environment> on <date>` or `unverified (written from code)`.

### 6. Write the usage guide

Fill `{skill-root}/assets/usage-guide.md`. Drop sections that do not apply; for internal audiences keep it short. The guide explains the things a spec cannot: how to get access, which call to make first, how the calls fit together in the common flows, and how to handle errors and retries.

### 7. Write the change notes

If a previous version exists:
- Run the style's breaking-change check from its reference file against the previous version.
- Write a changelog entry: added, changed, deprecated, removed, each with what consumers must do.
- Call out every breaking change at the top. A breaking change with no versioning or deprecation plan is a `Watch out` item for the user to raise with the owner; do not invent a plan.

If there is no previous version, write a first entry ("Initial version") and skip the check.

### 8. Lint and fix

Run the style's linter from its reference file, in this order of preference:
1. The project's own lint script or config.
2. The `npx` command in the reference file, if Node is available.
3. If neither is possible, work through the reference file's checklist by hand, and report linting as `SKIPPED (<reason>)`. Never describe unlinted docs as linted.

Fix every error. Fix warnings unless the fix would contradict the code's real behaviour; report the ones you leave and why. Rerun until clean.

Do not install tools globally or add dependencies to the project. `npx` downloads a tool for one run; if the network blocks it, treat it as unavailable.

### 9. Where the output goes

Follow the repo's convention. Otherwise:
- Spec next to the code it describes, where tools expect it: `openapi.yaml` at `{service-root}` or `{service-root}/api/`, `.proto` files where they already live, `schema.graphql` at the schema module, `asyncapi.yaml` at `{service-root}`.
- Guide and changelog in `{service-root}/docs/api/` (`README.md`, `CHANGELOG.md`), or under `~/work-docs/<repo-name>/docs/api/` on a work machine.

Write the files; do not commit them.

## End of every run

Stop there. Do not change API behaviour to match the docs; if the code looks wrong, report it. End with:

```
State: DONE | DONE_WITH_TODOS | OWNER_INPUT_REQUIRED
Produced: [files written or changed]
Lint: PASS (<tool>) | SKIPPED (<reason>)
Examples: [n verified against <env>, m unverified]
Breaking changes: [list, or "none" or "no previous version"]
Spec vs code mismatches: [list, or "none"]
TODO(owner): [each one, with who can likely answer]
Watch out: [only real issues: an undocumented auth path, an error leaking internals, a breaking change with no plan]
```

Use `OWNER_INPUT_REQUIRED` when the docs cannot be useful without an answer, such as unknown auth on an external API, or a spec-first contract with no agreed requirements.
