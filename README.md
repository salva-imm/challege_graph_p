## comparing the three main approaches to solving the challenge:

## 1. Insert-Only Approach
Description: Every incoming mention is inserted as a new row in an events table (i.e., an append-only log).

Pros:

- Fast write operations because no lookup or update is required.
- Simple to implement and fits well with an event-sourcing pattern, preserving full historical details.

Cons:

- Aggregation and querying shift the burden to the read side; you must sum or roll up many rows to compute current weights.
- The table size can grow very quickly, potentially affecting read performance.

Optimization:

- Use batch processing to periodically aggregate mentions and prune historical data.
- Leverage PostgreSQL’s materialized views to cache aggregated results for faster access.

## 2. Two-Table Normalized Approach
   Description: Use one table for users (nodes) and a separate table for mentions (edges). For example:
- Table 1: Users (columns: id, username)
- Table 2: Mentions (columns: id, source_id, target_id, weight) where source_id and target_id are foreign keys referencing the Users table.

Pros:

- Enforces data integrity and normalization through foreign keys.
- Saves storage space by avoiding duplicate username storage, which is especially beneficial when user metadata is enriched.
- Improves maintainability and scalability in the long run.

Cons:

- Slightly slower write performance because each operation may require creating or looking up user records and then performing joins or multiple inserts/updates.

Optimization:

- Improve performance with proper indexing and potentially caching of user IDs to avoid repetitive lookups.

## 3. Single-Table Aggregated Approach
Description: Store both users and mention relationships within a single table. For instance, one table with columns (source_username, target_username, weight) keeps a unique row per user pair.

Pros:

- Uses an UPSERT (ON CONFLICT) operation to either insert a new record or update an existing one, which can be efficient.
- Results in a smaller overall storage size compared to the insert-only approach because redundant mentions are aggregated into a single row.
- Avoids the extra join overhead seen in a two-table design.

Cons:

- While insertion is efficient, lookups are required to detect conflicts, although this is mitigated by database-level optimizations.

Optimization:

- Ensure appropriate indexing (e.g., a composite key on source and target) to maximize performance for UPSERTs and queries.

## In summary I choose approach 3, as it's more suitable for small/medium systems—especially for this challenge.

NOTE: for `Old mentions decay over time` we could use pg_cron/kafka. I'll not implement it in this challenge.
