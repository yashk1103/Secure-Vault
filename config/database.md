# Database Configuration

## SQLite Implementation

The application uses SQLite for data persistence with the following schema:

### Tables

**users**
- Primary key: `id`
- Unique constraint: `username`
- Indexed: `username`

**vault_entries**
- Primary key: `id`
- Foreign key: `user_id` references `users(id)`
- Indexed: `user_id`

### Security Features

1. **Data Encryption**: All sensitive fields encrypted before storage
2. **Foreign Keys**: Cascading deletes for data integrity
3. **Indexes**: Optimized queries with proper indexing
4. **Prepared Statements**: SQL injection prevention

### Production Considerations

For production deployment, consider:
- PostgreSQL or MySQL for better concurrency
- Database connection pooling
- Regular automated backups
- Database-level encryption
- Read replicas for scaling
