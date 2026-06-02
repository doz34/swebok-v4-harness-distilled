# Database Schema Design Recipe
> Compiled from 15+ canonical works (SQL Antipatterns, Refactoring Databases, Designing Data-Intensive Applications)

## When to use
Designing any new relational schema. Steps apply to SQL databases (Postgres, MySQL, SQLite, etc.).

## Steps

### 1. Identify entities and relationships
- Nouns in your domain = entities (User, Order, Product)
- Verbs = relationships (User PLACES Order, Order CONTAINS Product)
- Cardinality: 1:1, 1:N, N:M

### 2. Normalize first (3NF minimum)
- 1NF: No repeating groups; atomic values per cell
- 2NF: 1NF + no partial dependencies (every non-key column depends on the whole PK)
- 3NF: 2NF + no transitive dependencies (non-key columns don't depend on other non-key columns)
- BCNF: 3NF + every determinant is a candidate key
- Denormalize later for performance, with explicit justification

### 3. Choose primary keys
- **Prefer synthetic (surrogate) keys**: `BIGSERIAL`, `UUID v4`, or `UUID v7`
- Avoid natural keys as primary (they change, they're not stable)
- Composite keys OK for junction tables in many-to-many
- UUID v7 > UUID v4 (time-ordered, better index locality)

### 4. Foreign keys and referential integrity
- ALWAYS declare foreign keys. `REFERENCES other_table(id)`.
- `ON DELETE` strategy:
  - `CASCADE` — child rows deleted with parent (use for owned children)
  - `SET NULL` — child's FK becomes null (use when child is independent)
  - `RESTRICT` — default, parent can't be deleted if children exist (use for safety)
  - `NO ACTION` — same as RESTRICT but deferrable

### 5. Indexes
- Every primary key (automatic in most DBs)
- Every foreign key (often forgotten, causes slow JOINs)
- Columns in WHERE clauses that are queried often
- Columns in ORDER BY (for sorting without filesort)
- Composite indexes: order matters; leftmost prefix rule
- Don't over-index: every index slows writes

### 6. Constraints
- `NOT NULL` for required fields (default to NOT NULL, allow null explicitly when needed)
- `UNIQUE` for natural unique constraints (email, slug, etc.)
- `CHECK` for value constraints (`age > 0`, `status IN (...)`)
- `DEFAULT` for sensible defaults (`created_at`, `status='active'`)
- Use enums via `CHECK` or `CREATE TYPE` (Postgres), not text fields

### 7. Timestamps
- Always `created_at TIMESTAMP NOT NULL DEFAULT NOW()`
- Always `updated_at TIMESTAMP NOT NULL DEFAULT NOW()`
- Use `TIMESTAMPTZ` (with time zone), never `TIMESTAMP` (Postgres specific advice)
- For audit: `created_by`, `updated_by` (user_id references)
- For soft delete: `deleted_at TIMESTAMPTZ NULL` + partial index `WHERE deleted_at IS NULL`

### 8. Naming conventions
- Tables: `snake_case`, plural (`users`, `order_items`)
- Columns: `snake_case`, singular (`first_name`, `created_at`)
- Primary key: `id` (always, never `user_id` in the users table)
- Foreign keys: `<singular_referenced_table>_id` (`user_id`, `order_id`)
- Timestamps: `<verb>_at` (`created_at`, `deleted_at`, `published_at`)
- Booleans: `is_<adjective>` or `has_<noun>` (`is_active`, `has_children`)
- Indexes: `idx_<table>_<columns>` (`idx_users_email`)
- Unique constraints: `uniq_<table>_<columns>` (`uniq_users_email`)

### 9. Money / numerics
- NEVER use FLOAT or DOUBLE for money (rounding errors)
- Use `NUMERIC(precision, scale)` or `DECIMAL` (Postgres: `NUMERIC(10, 2)` for typical money)
- Store in smallest unit (cents, not dollars) to avoid decimals
- Or use a dedicated money type (if available)

### 10. Migrations
- Migrations are code — versioned, reviewed, tested
- Forward AND backward (down) migrations
- Never edit a deployed migration — add a new one
- For destructive changes (column drop): expand-contract pattern
  1. Add new column
  2. Backfill
  3. Switch code to use new column
  4. Drop old column (separate migration)

### 11. Common patterns
- **Audit log**: separate `audit_log` table with trigger or app-level writes
- **Soft delete**: `deleted_at` + filter in queries (don't use `is_deleted` boolean)
- **Multi-tenancy**: row-level security (RLS) or schema-per-tenant or DB-per-tenant
- **Polymorphic associations**: avoid. Use separate FKs or a junction table.
- **Tags**: separate `tags` table + `taggings` junction with `(tag_id, taggable_id, taggable_type)`
- **Hierarchies**: adjacency list (parent_id) for simple trees; nested set or ltree for complex queries

### 12. Verification
- Test the schema with realistic data volumes
- Run `EXPLAIN ANALYZE` on your key queries
- Check that the slow queries match the indexes
- Verify constraints with negative test data
- Check that backups and restores work

## Anti-patterns (from SQL Antipatterns)
- **EAV (Entity-Attribute-Value)**: lose type safety, indexing, query power
- **Polymorphic associations**: see above
- **Floating-point money**: see above
- **Naive trees**: adjacency list is fine for shallow trees; use nested set for deep
- **DELETE without WHERE**: see the famous xkcd
- **Using OR in queries**: usually kills indexes
- **SELECT * in production**: column changes break callers
- **Implicit type conversions**: `WHERE varchar_col = 123` skips index
- **Not using CHECK constraints**: bad data is forever

## Related
- See `comparisons/sql-vs-nosql.json` for when to use relational at all
- See `risks/data-risks.md` for the failure modes
- See `decision-trees/choose-database.json` for picking the database
