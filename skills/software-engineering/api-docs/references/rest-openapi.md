# REST / HTTP with OpenAPI

## Spec format

- New specs: OpenAPI 3.1. Existing specs: keep their version (3.0 or 2.0/Swagger) unless the user asks to upgrade.
- YAML unless the repo uses JSON.

## Where the truth lives in code

Code-first frameworks generate the spec. Document in the code, then export the spec with the project's own command or script if it has one. Do not start the server just to fetch the spec unless the user agrees.

| Framework | Where docs go | How the spec is produced |
|---|---|---|
| FastAPI | Pydantic model `Field(description=..., examples=...)`, route `summary`, `description`, `responses=`, `response_model` | `app.openapi()`; often an export script |
| NestJS | `@ApiProperty`, `@ApiOperation`, `@ApiResponse`, `@ApiTags` from `@nestjs/swagger` | `SwaggerModule.createDocument` |
| Spring Boot | springdoc `@Operation`, `@ApiResponse`, `@Schema`, `@Parameter` | springdoc at build or runtime |
| Django REST Framework | drf-spectacular `@extend_schema`, serializer `help_text` | `manage.py spectacular --file openapi.yaml` |
| Go | swaggo comment annotations, or a hand-written spec with oapi-codegen | `swag init`, or the spec is the source |
| Express / Fastify / Hono | Usually none built in; look for zod-openapi, tsoa, fastify-swagger | Varies; check package scripts |

If none applies, the spec is hand-written and lives in the repo.

When reading code without generated docs, check: the router, request validation (schemas, DTOs, validators), auth middleware, the global error handler, and serializers for the response shape.

## What a complete operation has

- `operationId` (stable, camelCase verb plus noun, e.g. `listOrders`), `summary` (one line), `description` (behaviour, side effects, permissions), `tags`.
- Parameters with `required`, `schema`, `description`, and `example`.
- Request body with a schema in `components/schemas` and at least one example.
- Every response the code can return: success codes, validation errors (usually 400 or 422), 401, 403, 404, 409, 429 if rate limited, 5xx only if the API documents it. Each with a schema.
- `security` naming a scheme from `components/securitySchemes`.

## Conventions to check

- **Error model**: document the shape the error handler really returns. If it is RFC 9457 (`application/problem+json`), say so.
- **Pagination**: cursor or offset, parameter names, the max page size, how the caller knows there are more results.
- **Idempotency**: whether retries are safe; an `Idempotency-Key` header if supported.
- **Dates and money**: format (RFC 3339 timestamps, timezone), currency and units.
- **Nullability and optionality**: `required` lists and `nullable`/`type: [x, "null"]` must match what the serializer does.
- **Enums**: list values, and say whether consumers must tolerate unknown future values.
- **Servers**: use `{baseUrl}`-style server variables or placeholders; never hardcode internal hostnames in external docs.

Public design guidelines worth matching when the team has none: Google AIP (aip.dev), Microsoft REST API Guidelines, Zalando RESTful API Guidelines.

## Lint

Prefer the project's config. Otherwise:

```bash
npx --yes @redocly/cli@latest lint <spec>
```

Spectral if the repo has a `.spectral.yaml`:

```bash
npx --yes @stoplight/spectral-cli lint <spec>
```

## Breaking-change check

Get the previous version, for example `git show main:<spec-path> > /tmp/old-spec.yaml` (use the scratchpad directory if one exists). Then, if installed:

```bash
oasdiff breaking <old-spec> <new-spec>
oasdiff changelog <old-spec> <new-spec>
```

`breaking` only reports error and warning levels. Removing an optional response property is `info` level, so `breaking` stays silent, yet consumers reading that field will break. Always read the `changelog` output as well, and treat every `*-removed` entry as potentially breaking in the change notes.

oasdiff is a standalone binary, not on npm. If it is not installed, compare by hand: removed paths or operations, removed or renamed fields, new required request fields, narrowed types or enums, changed status codes or auth.

## Manual checklist (when lint is skipped)

- Every `$ref` resolves.
- Every operation has a unique `operationId`, a summary, a tag, and at least one 2xx and one 4xx response.
- Every schema property has a type and a description.
- Examples validate against their schemas.
- No secrets, internal hostnames or real customer data anywhere.

## Examples

- curl with `-sS`, `-H "Authorization: Bearer $API_TOKEN"`, `$BASE_URL`, and `--json` or `-H 'Content-Type: application/json' -d`.
- Show the response body, trimmed to the relevant fields.
