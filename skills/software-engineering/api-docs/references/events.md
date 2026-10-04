# Events, message queues and webhooks

## Spec format

- **Message brokers** (Kafka, Pub/Sub, SQS/SNS, RabbitMQ, NATS): AsyncAPI. New specs use AsyncAPI 3.0; keep the version an existing spec uses.
- **Schema registry**: if messages are registered (Avro, Protobuf or JSON Schema in Confluent Schema Registry, Glue, Apicurio), the registered schema is the source of truth for the payload. The AsyncAPI document references it and adds what a schema cannot say.
- **Outgoing webhooks**: OpenAPI 3.1 `webhooks` if the service already has an OpenAPI spec; otherwise AsyncAPI.

## Where the truth lives in code

Read: producer code (what is published, when, with which key and headers), consumer code (what is expected, retries, dead-letter handling), topic or queue configuration (infrastructure-as-code, Helm values, broker config), and schema files or registry config. Behaviour like ordering and retention lives in config, not in the payload schema.

## What complete docs cover

- **Each channel**: topic or queue name (placeholder per environment if names differ), who produces, who consumes, and the business event it represents.
- **Each message**: payload schema with field descriptions, headers, the message key and why it was chosen (it decides partitioning and ordering), content type, and a sample payload.
- **When it is emitted**: the exact trigger, and whether it is emitted once per change or can repeat.
- **Delivery semantics**: at-most-once, at-least-once or effectively-once. At-least-once means consumers must be idempotent; say how to deduplicate (an event ID).
- **Ordering**: guaranteed per key, per partition, or not at all.
- **Retention and replay**: how long messages are kept, and whether consumers can replay.
- **Schema evolution**: the registry compatibility mode (BACKWARD, FORWARD, FULL) or the team's rule, and how breaking changes are versioned (new topic, version field, new event type).
- **Errors**: retries, dead-letter topic or queue, what consumers should do with a message they cannot process.
- **Webhooks**: the HTTP request sent, signature verification (header, algorithm, how to verify), retry schedule, which responses count as success, and timeouts.

Delivery semantics, ordering, retention and compatibility mode are on the must-not-invent list: take them from config or mark `TODO(owner)`.

## Lint

Prefer the project's setup. Otherwise:

```bash
npx --yes @asyncapi/cli validate <asyncapi-file>
```

For a webhooks section in OpenAPI, lint with `rest-openapi.md`. For registered schemas, use the registry's compatibility check if the project has a script for it; do not register schemas yourself.

## Breaking-change check

```bash
npx --yes @asyncapi/cli diff <old-asyncapi-file> <new-asyncapi-file>
```

For Protobuf payloads, `buf breaking` from `grpc.md` also applies. Removing a field, renaming it, changing its type, or adding a required field breaks existing consumers.

## Manual checklist (when lint is skipped)

- Every channel has producers, consumers and a description.
- Every message has a schema, a key description and a sample payload that validates against the schema.
- Delivery semantics, ordering and retention are stated or marked `TODO(owner)`.
- Sample payloads contain no real customer data.

## Examples

- A sample payload for each message, with headers and key.
- Consumer snippets in the consumers' languages showing deserialisation and idempotent handling.
- For verification, never produce to a shared topic or queue. Reading to check a payload shape needs approval, and must not commit offsets for an existing consumer group: use a fresh, uniquely named group or read without a group (for Kafka, `kcat -C -b "$BROKER" -t <topic> -o -5 -e`).
- For webhooks: a sample request with headers and signature, and a snippet that verifies the signature.
