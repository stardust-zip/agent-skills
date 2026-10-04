# gRPC / protobuf

## Spec format

The `.proto` files are the reference. The docs are the comments: a leading `//` comment directly above each service, rpc, message, field and enum value. Documentation generators (protoc-gen-doc, buf's registry, IDE tooltips) read them from there.

Keep protos where they already live. Do not add a new docs generator plugin to `buf.gen.yaml` unless the user asks; if the repo already has one, run it.

## Where the truth lives in code

- The `.proto` files define the contract. The server implementation defines the behaviour: which status codes each rpc returns, validation, auth.
- Read: service implementations, interceptors or middleware (auth, logging, deadlines), validation (protovalidate / `buf.validate` annotations, or hand-written checks), and how errors are converted to status codes.

## What complete docs cover

- **Every rpc**: what it does, side effects, permissions, and every status code it returns with when (`INVALID_ARGUMENT`, `NOT_FOUND`, `ALREADY_EXISTS`, `PERMISSION_DENIED`, `UNAUTHENTICATED`, `FAILED_PRECONDITION`, `RESOURCE_EXHAUSTED`, `UNAVAILABLE`), plus any rich error details (`google.rpc.ErrorInfo`, `BadRequest`) the server attaches.
- **Every field**: meaning, units, format, whether it is required in practice (proto3 fields are all optional on the wire), and the default-value trap: `0`, `""` and `false` are indistinguishable from unset unless the field uses `optional` or a wrapper type.
- **Field behaviour**: if the project uses `google.api.field_behavior` (`REQUIRED`, `OUTPUT_ONLY`, `IMMUTABLE`), apply it consistently.
- **Enums**: the `_UNSPECIFIED = 0` value and what it means; consumers must tolerate unknown values.
- **Streaming**: for client, server or bidirectional streaming, the message order, who closes the stream, and how errors surface mid-stream.
- **Deadlines and retries**: recommended deadline, which rpcs are safe to retry, idempotency.
- **Auth**: which metadata key carries credentials.
- **HTTP transcoding**: if rpcs have `google.api.http` options, document the REST view too, using `rest-openapi.md`.

Public design guidance worth matching when the team has none: Google AIP (aip.dev) and the buf style guide.

## Lint

Prefer the project's `buf.yaml`. Otherwise:

```bash
npx --yes @bufbuild/buf lint
```

If the repo has no `buf.yaml`, buf uses its defaults, which may flag existing naming conventions; report those rather than renaming fields, since renames break consumers.

## Breaking-change check

```bash
npx --yes @bufbuild/buf breaking --against '.git#branch=main'
```

Use the module's subdirectory with `,subdir=<path>` if the protos are not at the repo root, or `#tag=<tag>` for a release tag. Changing a field number, type or name, or removing a field without `reserved`, breaks consumers.

## Manual checklist (when lint is skipped)

- Every service, rpc, message, field and enum value has a leading comment.
- Removed fields are `reserved` by number and name.
- Every enum has a zero `_UNSPECIFIED` value.
- Request and response messages are named `<Rpc>Request` / `<Rpc>Response` (or the project's convention), not shared across rpcs.

## Examples

grpcurl, with reflection if the server enables it, otherwise with `-proto`:

```bash
grpcurl -H "authorization: Bearer $API_TOKEN" -d '{"order_id": "<order-id>"}' \
  "$GRPC_HOST:443" acme.orders.v1.OrderService/GetOrder
```

Show the JSON form of the response, and one error response with its status code and details. Add client snippets in the consumers' languages using the generated stubs.
