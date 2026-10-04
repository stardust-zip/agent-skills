# GraphQL

## Spec format

The schema (SDL) is the reference. The docs live in the schema as descriptions: `"""block strings"""` on types, fields, arguments, enum values and input fields. Tools like GraphiQL, Apollo Studio and documentation generators read them from there.

## Where the truth lives in code

- **Schema-first** (SDL files with resolvers, gqlgen, graphql-tools): edit the `.graphql` files.
- **Code-first** (NestJS GraphQL, TypeGraphQL, Pothos, Strawberry, Graphene, graphql-java annotations): add descriptions in the code (`description:` options, docstrings, decorators). Print the schema with the project's own script to review the result.

Also read: the context builder and auth directives or guards (who may see which field), error formatting (`formatError`, error extensions), and complexity or depth limits.

## What complete docs cover

- Every type, field, argument and enum value has a description; arguments say defaults and constraints.
- Nullability is deliberate: say what `null` means for a nullable field.
- Deprecations use `@deprecated(reason: "Use X instead; removal planned <TODO(owner) if unknown>")`. Never remove a field without a deprecation period unless the owner says so.
- **Errors**: GraphQL returns HTTP 200 with an `errors` array for most failures. Document the `extensions.code` values the server actually sets, and any union or result types used for expected errors (for example `CreateOrderResult = Order | ValidationError`).
- **Pagination**: Relay connections (`edges`, `node`, `pageInfo`, `first`/`after`) or offset; the maximum page size.
- **Auth**: how the token is passed, and which fields or operations need which permission.
- **Limits**: query depth or complexity limits, persisted-query requirements, rate limits.
- **Subscriptions**: transport (graphql-ws, SSE), and what events trigger them.

## Lint

Prefer the project's config (for example a `graphql-schema-linter` config or ESLint `@graphql-eslint`). Otherwise:

```bash
npx --yes graphql-schema-linter <schema-files>
```

To check that the example operations are valid against the schema:

```bash
npx --yes @graphql-inspector/cli validate "<operations-glob>" <schema>
```

## Breaking-change check

```bash
npx --yes @graphql-inspector/cli diff <old-schema> <new-schema>
```

Get the old schema from the previous version with `git show`. For code-first schemas, print both versions with the project's schema-print script.

## Manual checklist (when lint is skipped)

- Every type, field, argument and enum value has a description.
- Every deprecation has a reason.
- No field returns a raw internal error message or stack trace.
- The example operations use only fields that exist with the right argument types.

## Examples

- curl: `curl -sS "$BASE_URL/graphql" -H "Authorization: Bearer $API_TOKEN" --json '{"query":"...","variables":{...}}'`.
- Show the operation as a readable GraphQL block with its variables, and the trimmed response, including one response with an `errors` array.
