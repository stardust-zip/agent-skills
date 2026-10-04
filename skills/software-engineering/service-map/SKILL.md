---
name: service-map
description: Finds another microservice's real contract (owning repo, API, what it wraps, URL per environment) via a local catalog, and records services it discovers. Use when work calls, integrates with or designs against another service.
---

# Service Map

The user works in a company with many microservices that call each other. Some are plain services; some are thin wrappers over middleware such as SeaweedFS or MLflow. Environments run local → DEV → SIT → UAT → PROD. The expensive part of cross-service work is finding the right other service and its real contract, so this skill keeps a catalog and knows how to search when the catalog is silent.

## The catalog

One YAML file, outside every repository:
- Work machine (`~/work-docs/` exists): `~/work-docs/service-map/services.yaml`
- Otherwise: `~/.local/share/service-map/services.yaml`

If it does not exist, create it from `{skill-root}/assets/services.example.yaml` and ask the user once for `clones_root` (the folder where they clone service repos).

Every value in an entry has a source: a file path with line (`deploy/values-dev.yaml:12`) or `user, <date>`. A value without a source is not written. Never store credentials, tokens or connection strings with secrets; store only the name of the variable or secret that holds them.

## Answering a question about another service

1. **Look it up** in the catalog, by name or alias.
2. **Read the source of truth**, even when the catalog has an entry: the catalog says where to look, the provider's repository says what is true. Open the provider's spec or routes in its local clone (`repo:`) and answer from there, citing `file:line`. If the clone is missing, say so and give the clone command from `git_url`.
3. **Check the consumer side** in the current repository: how this service already calls the provider (client code, generated clients, base-URL variables per environment). Report any mismatch between what the consumer sends and what the provider accepts.
4. **Answer** with the contract (endpoint or RPC, inputs, outputs, errors, auth), the URL per environment with its source, and a confidence level.

## Discovering a service the catalog does not know

Usually the user points you to the service. When they have not, or the pointer is not enough, search in this order and stop when the contract is found. Searching the current repository and `clones_root` needs no permission; anything beyond them needs the user's OK first.

1. **The current repository**: grep for the service name in config (`.env*`, Helm values, Kubernetes manifests, docker-compose, application config per environment) and client code. This usually gives the base URL per environment and the calls actually made.
2. **Local clones** under `clones_root`: find the repository by name, then its spec (`openapi.*`, `*.proto`, `schema.graphql`, `asyncapi.*`) or route definitions.
3. **The company Git host**, read-only, only after asking the user each time, and only if a CLI is installed and logged in (for GitLab, `glab`): search for the repository, then ask the user to clone it rather than reading code through the API.
4. **Ask the user**, with what was found so far and the exact gap.

Then propose a catalog entry as a diff and write it only after the user confirms.

## Wrappers over middleware

For a service that wraps middleware (`kind: wrapper`):
- The wrapper's own API is the contract. Callers use it, not the middleware directly, unless the design says otherwise.
- Record the middleware and its version (`wraps:`), from the wrapper's dependency or deployment files.
- Read upstream documentation for that version only for behaviour the wrapper passes through (for example SeaweedFS filer semantics, MLflow tracking calls). Note which middleware features the wrapper hides or changes.

## Environments

- URLs, hosts and topic names per environment come from config files, never from guesswork; the source is recorded per value.
- Only LOCAL, DEV and SIT are in scope. Do not record, look up or call UAT or PROD. If the user asks about them, say they are out of scope for now and add them only if the user explicitly asks to extend the catalog.
- Calling LOCAL, DEV or SIT to confirm a behaviour follows the live-call rules of the `api-docs` skill: the user approves each run, read-only calls first, and real data is scrubbed from anything written down.

## Keeping it fresh

When an answer contradicts the catalog (a moved spec, a changed URL), fix the entry, update `verified`, and tell the user what changed. Offer a refresh when an entry's `verified` date is older than about three months.
