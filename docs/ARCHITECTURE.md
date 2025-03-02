# Globetrotter System Architecture

## System Overview

Globetrotter is a real-time multiplayer geography quiz game built with a modern, scalable architecture. The system uses FastAPI for the backend, PostgreSQL for data persistence, and React with TanStack Query for the frontend.

```mermaid
graph TB
    subgraph "Frontend Layer"
        UI[React UI]
        RQ[TanStack Query]
        UI --> RQ
    end

    subgraph "API Gateway"
        API[FastAPI Server]
        Cache[Redis Cache]
        RQ --> API
        API <--> Cache
    end

    subgraph "Data Layer"
        DB[(PostgreSQL)]
        API <--> DB
    end
```

## Core Components

### 1. Frontend Architecture

- **React with TypeScript**: Type-safe client implementation
- **TanStack Query**: Efficient data fetching and caching
- **Real-time Updates**: Optimistic UI updates with background synchronization
- **State Management**: Distributed state management through React Query

### 2. Backend Architecture

- **FastAPI**: High-performance async API framework
- **PostgreSQL**: Primary data store
- **Redis**: Caching and real-time features
- **Pydantic**: Type validation and serialization

## Data Flow

```mermaid
sequenceDiagram
    participant User
    participant Frontend
    participant API
    participant Cache
    participant Database

    User->>Frontend: Start Game
    Frontend->>API: Create User
    API->>Database: Store User
    Database-->>API: User Created
    API-->>Frontend: User Details

    loop Game Play
        Frontend->>API: Get Question
        API->>Cache: Check Cache
        alt Cache Hit
            Cache-->>API: Return Cached Question
        else Cache Miss
            API->>Database: Fetch Question
            Database-->>API: Question Data
            API->>Cache: Store in Cache
        end
        API-->>Frontend: Question Data

        User->>Frontend: Submit Answer
        Frontend->>API: Post Answer
        API->>Database: Update Score
        API->>Cache: Invalidate Cache
        API-->>Frontend: Result
    end
```

## Scalability Features

1. **Horizontal Scaling**
   - Stateless API servers can be scaled horizontally
   - Load balancer distributes traffic across API instances
   - Database read replicas for scaling read operations

2. **Caching Strategy**

   ```mermaid
   graph LR
       A[API Request] --> B{Cache?}
       B -->|Yes| C[Return Cached]
       B -->|No| D[Database Query]
       D --> E[Cache Result]
       E --> F[Return Response]
   ```

3. **Performance Optimizations**
   - Question caching with 5-minute stale time
   - Batch database operations
   - Efficient indexing on frequently queried fields
   - Connection pooling for database connections

## Multiplayer Implementation

### Concurrent User Management

- Each user has an independent game session
- Questions are randomly selected from a large pool
- User scores and stats are updated atomically
- Real-time leaderboard updates through Redis pub/sub

### Data Consistency

```mermaid
graph TB
    A[User Action] --> B{Valid Session?}
    B -->|Yes| C[Process Action]
    B -->|No| D[Error Response]
    C --> E{Update Required?}
    E -->|Yes| F[Atomic Update]
    E -->|No| G[Return Response]
    F --> H[Publish Event]
    H --> I[Update Cache]
```

## Security Measures

1. **Rate Limiting**
   - Per-user request limits
   - IP-based rate limiting
   - Concurrent session limits

2. **Data Validation**
   - Input validation using Pydantic models
   - Request size limits
   - SQL injection prevention through ORM

## Monitoring and Observability

1. **Key Metrics**
   - Request latency
   - Cache hit rates
   - Database connection pool status
   - Active user sessions

2. **Logging**
   - Structured JSON logs
   - Error tracking
   - User activity monitoring

## Database Schema

```mermaid
erDiagram
    Users ||--o{ GameSessions : has
    Users {
        int id
        string username
        float score
        int total_attempts
        int correct_answers
        timestamp created_at
    }
    GameSessions {
        int id
        int user_id
        string question_alias
        string answer
        boolean is_correct
        timestamp created_at
    }
    Questions {
        int id
        string alias
        string[] clues
        string[] options
        string correct_answer
        string fun_fact
        timestamp created_at
    }
```

## API Endpoints

### Game Flow

1. `POST /api/v1/users`
   - Create new user
   - Returns user details and session token

2. `GET /api/v1/game/question`
   - Fetch random question
   - Cached for 5 minutes
   - Different users may get different questions

3. `POST /api/v1/game/answer`
   - Submit answer
   - Updates user score
   - Returns result with fun fact

4. `GET /api/v1/users/{username}/stats`
   - Fetch user statistics
   - Cached with automatic invalidation on score updates

## Deployment Architecture

```mermaid
graph TB
    subgraph "Load Balancer"
        LB[NGINX]
    end

    subgraph "Application Tier"
        API1[API Server 1]
        API2[API Server 2]
        API3[API Server 3]
    end

    subgraph "Cache Layer"
        RC1[Redis Primary]
        RC2[Redis Replica]
    end

    subgraph "Database Tier"
        DB1[(PostgreSQL Primary)]
        DB2[(Read Replica 1)]
        DB3[(Read Replica 2)]
    end

    LB --> API1
    LB --> API2
    LB --> API3

    API1 --> RC1
    API2 --> RC1
    API3 --> RC1
    RC1 --> RC2

    API1 --> DB1
    API2 --> DB1
    API3 --> DB1
    DB1 --> DB2
    DB1 --> DB3
```

## Performance Considerations

1. **Database Optimization**
   - Indexed queries
   - Connection pooling
   - Prepared statements
   - Regular vacuum and maintenance

2. **Caching Strategy**
   - Multi-level caching
   - Cache warming
   - Smart invalidation
   - Cache stampede prevention

3. **API Performance**
   - Async operations
   - Batch processing
   - Response compression
   - CDN integration for static assets

## Future Improvements

1. **Real-time Features**
   - WebSocket integration for live updates
   - Multiplayer rooms
   - Live leaderboards
   - Chat functionality

2. **Game Features**
   - Different difficulty levels
   - Category-based questions
   - Time-based scoring
   - Achievement system

3. **Technical Enhancements**
   - GraphQL API
   - Event sourcing
   - Microservices architecture
   - AI-powered question generation
