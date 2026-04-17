# Event-Driven Image Retrieval System

A simple event-driven image annotation and retrieval system built for EC530. The system uses modular services, Redis pub-sub messaging, document-based annotation storage, and vector-based similarity search.

## Architecture

The system is split into the following services:

- CLI Service
- Image Service
- Inference Service
- Document DB Service
- Embedding Service
- Vector Index Service

The CLI does not access any database directly. It only interacts through service layers, which follows the project requirement.

## Event Flow

### Upload pipeline
1. CLI triggers image upload
2. Image Service publishes `image.submitted`
3. Inference Service publishes `inference.completed`
4. Document DB Service stores the annotation and publishes `annotation.stored`
5. Embedding Service publishes `embedding.created`
6. Vector Index Service stores the embedding

### Query pipeline
1. CLI submits a search query
2. Vector Index Service performs similarity search
3. Query results are returned through `query.completed`

## Topics

- `image.upload.request`
- `image.submitted`
- `inference.completed`
- `annotation.stored`
- `embedding.created`
- `query.submitted`
- `query.completed`
- `annotation.corrected`

## Why a Document Database

A document-based structure fits this project because image annotations are variable and nested. Each image may contain a different number of detected objects, and each object includes fields like label, bounding box, and confidence. Review history and corrections can also evolve over time. A document model is easier to extend than a fixed relational schema.

## Testing

The project includes tests for:

- event schema validation
- Redis broker publish behavior
- image upload events
- inference processing
- document storage
- embedding generation
- vector indexing
- idempotency
- end-to-end upload pipeline
- end-to-end query pipeline

## Run tests

```bash
pytest