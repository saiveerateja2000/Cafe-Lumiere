# ☕ Café Lumière - System Architecture

## Overview

Café Lumière is a microservices-based café management application with three core services:
- **Frontend Service** - User interfaces (Customer, Kitchen, Display)
- **Order Service** - Order management and database operations
- **Kitchen Service** - Order processing workflow
- **PostgreSQL Database** - Persistent data storage

## System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                          USERS & CLIENTS                             │
│                                                                      │
│  👥 Customers      👨‍🍳 Kitchen Staff      📺 Display Monitor         │
└──────────┬────────────────┬─────────────────────┬────────────────────┘
           │                │                     │
           │                │                     │
           ▼                ▼                     ▼
┌──────────────────────────────────────────────────────────────────────┐
│                       FRONTEND SERVICE (Port 5000)                    │
│                          Flask + Jinja2                              │
│  ┌───────────────┐  ┌──────────────┐  ┌────────────────────────┐   │
│  │  Customer UI  │  │ Kitchen UI   │  │  Display Board UI      │   │
│  │  - Menu       │  │ - New Orders │  │  - Ready Orders        │   │
│  │  - Cart       │  │ - Preparing  │  │  - Preparing Orders    │   │
│  │  - Tracking   │  │ - Ready      │  │  - Auto-refresh        │   │
│  └───────────────┘  └──────────────┘  └────────────────────────┘   │
└──────────┬──────────────────────┬────────────────────────────────────┘
           │                      │
           │ HTTP/REST            │ HTTP/REST
           │                      │
           ▼                      ▼
┌──────────────────────┐  ┌──────────────────────────────────────┐
│  ORDER SERVICE       │  │  KITCHEN SERVICE                      │
│  (Port 5001)         │◄─┤  (Port 5002)                         │
│                      │  │                                       │
│  - Create Orders     │  │  - Fetch Active Orders               │
│  - Get Orders        │  │  - Update Status (Preparing)         │
│  - Update Status     │  │  - Update Status (Ready)             │
│  - Health Check      │  │  - Update Status (Served)            │
│                      │  │  - Kitchen Statistics                │
└──────────┬───────────┘  └───────────────────────────────────────┘
           │
           │ PostgreSQL Protocol
           │ (psycopg2)
           ▼
┌──────────────────────────────────────────────────────────────────────┐
│                    POSTGRESQL DATABASE (Port 5432)                    │
│                                                                       │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │  TABLE: orders                                              │    │
│  │  ┌────────────────┬────────────────┬─────────────────────┐ │    │
│  │  │ id             │ order_number   │ customer_name       │ │    │
│  │  │ items (JSONB)  │ total_price    │ status              │ │    │
│  │  │ created_at     │ updated_at     │                     │ │    │
│  │  └────────────────┴────────────────┴─────────────────────┘ │    │
│  └─────────────────────────────────────────────────────────────┘    │
└───────────────────────────────────────────────────────────────────────┘
```

## 🔄 Data Flow Diagram

### Order Creation Flow
```
Customer               Frontend              Order Service         Database
   │                      │                        │                  │
   │  1. Place Order      │                        │                  │
   ├─────────────────────►│                        │                  │
   │                      │  2. POST /orders       │                  │
   │                      ├───────────────────────►│                  │
   │                      │                        │  3. INSERT       │
   │                      │                        ├─────────────────►│
   │                      │                        │  4. Return Row   │
   │                      │                        │◄─────────────────┤
   │                      │  5. Order Created      │                  │
   │                      │◄───────────────────────┤                  │
   │  6. Show Order #     │                        │                  │
   │◄─────────────────────┤                        │                  │
   │  7. Poll Status      │                        │                  │
   ├─────────────────────►│  GET /orders/{id}     │                  │
   │      (every 3s)      ├───────────────────────►│  SELECT          │
   │                      │                        ├─────────────────►│
   │                      │  Return Status         │◄─────────────────┤
   │◄─────────────────────┤◄───────────────────────┤                  │
   │                      │                        │                  │
```

### Order Status Update Flow
```
Kitchen Staff        Frontend         Kitchen Service     Order Service    Database
     │                  │                    │                  │             │
     │ 1. Click         │                    │                  │             │
     │  "Start"         │                    │                  │             │
     ├─────────────────►│                    │                  │             │
     │                  │ 2. POST            │                  │             │
     │                  │ /kitchen/orders/   │                  │             │
     │                  │  {id}/start        │                  │             │
     │                  ├───────────────────►│                  │             │
     │                  │                    │ 3. PUT /orders/  │             │
     │                  │                    │  {id}            │             │
     │                  │                    │ {status:         │             │
     │                  │                    │  "preparing"}    │             │
     │                  │                    ├─────────────────►│             │
     │                  │                    │                  │ 4. UPDATE   │
     │                  │                    │                  ├────────────►│
     │                  │                    │                  │◄────────────┤
     │                  │                    │ 5. Updated Order │             │
     │                  │                    │◄─────────────────┤             │
     │                  │ 6. Success         │                  │             │
     │                  │◄───────────────────┤                  │             │
     │ 7. UI Update     │                    │                  │             │
     │◄─────────────────┤                    │                  │             │
     │                  │                    │                  │             │
```

## 🏗️ Microservices Architecture

### Service Responsibilities

#### 1. **Frontend Service** (Port 5000)
```
┌─────────────────────────────────────┐
│         Frontend Service            │
├─────────────────────────────────────┤
│ Technology: Flask + Jinja2 + JS    │
│ Purpose: User Interface Layer      │
├─────────────────────────────────────┤
│ Responsibilities:                   │
│ • Serve HTML templates             │
│ • Handle user interactions         │
│ • Proxy API requests               │
│ • Real-time status polling         │
│ • Static asset serving             │
├─────────────────────────────────────┤
│ Endpoints:                          │
│ • GET  /                           │
│ • GET  /kitchen                    │
│ • GET  /display                    │
│ • GET  /api/menu                   │
│ • POST /api/orders                 │
│ • GET  /api/orders                 │
│ • POST /api/kitchen/orders/{id}/*  │
└─────────────────────────────────────┘
```

#### 2. **Order Service** (Port 5001)
```
┌─────────────────────────────────────┐
│         Order Service               │
├─────────────────────────────────────┤
│ Technology: Flask + PostgreSQL     │
│ Purpose: Order Management          │
├─────────────────────────────────────┤
│ Responsibilities:                   │
│ • Create new orders                │
│ • Store order data                 │
│ • Retrieve orders                  │
│ • Update order status              │
│ • Database schema management       │
│ • Data validation                  │
├─────────────────────────────────────┤
│ API Endpoints:                      │
│ • GET    /health                   │
│ • POST   /orders                   │
│ • GET    /orders                   │
│ • GET    /orders/{order_number}    │
│ • PUT    /orders/{order_number}    │
├─────────────────────────────────────┤
│ Database: PostgreSQL               │
│ • Connection pooling               │
│ • Retry logic (10 attempts)        │
│ • Auto-reconnect                   │
└─────────────────────────────────────┘
```

#### 3. **Kitchen Service** (Port 5002)
```
┌─────────────────────────────────────┐
│        Kitchen Service              │
├─────────────────────────────────────┤
│ Technology: Flask + Requests       │
│ Purpose: Workflow Management       │
├─────────────────────────────────────┤
│ Responsibilities:                   │
│ • Filter kitchen orders            │
│ • Coordinate status updates        │
│ • Provide kitchen statistics       │
│ • Service communication            │
│ • Retry failed requests            │
├─────────────────────────────────────┤
│ API Endpoints:                      │
│ • GET  /health                     │
│ • GET  /kitchen/orders             │
│ • POST /kitchen/orders/{id}/start  │
│ • POST /kitchen/orders/{id}/ready  │
│ • POST /kitchen/orders/{id}/serve  │
│ • GET  /kitchen/stats              │
├─────────────────────────────────────┤
│ Upstream: Order Service            │
│ • HTTP retry (3 attempts)          │
│ • Timeout: 5 seconds               │
│ • Backoff: exponential             │
└─────────────────────────────────────┘
```

## 🗄️ Database Schema

### Orders Table
```sql
CREATE TABLE orders (
    id              SERIAL PRIMARY KEY,
    order_number    VARCHAR(20) UNIQUE NOT NULL,
    customer_name   VARCHAR(100) NOT NULL,
    items           JSONB NOT NULL,
    total_price     DECIMAL(10, 2) NOT NULL,
    status          VARCHAR(20) DEFAULT 'ordered',
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX idx_orders_order_number ON orders(order_number);
CREATE INDEX idx_orders_status ON orders(status);
CREATE INDEX idx_orders_created_at ON orders(created_at DESC);

-- Trigger for auto-updating updated_at
CREATE TRIGGER update_orders_updated_at
    BEFORE UPDATE ON orders
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
```

### Items JSONB Structure
```json
[
  {
    "id": 1,
    "name": "Cappuccino",
    "price": 4.50,
    "quantity": 2
  }
]
```

## 🔄 Order Status Lifecycle

```
┌──────────┐
│ ordered  │  Customer places order
└────┬─────┘
     │ Chef clicks "Start Preparing"
     ▼
┌──────────┐
│preparing │  Order is being cooked
└────┬─────┘
     │ Chef clicks "Mark Ready"
     ▼
┌──────────┐
│  ready   │  Order ready for pickup
└────┬─────┘
     │ Staff clicks "Serve Order"
     ▼
┌──────────┐
│  served  │  Order delivered (final state)
└──────────┘
```

## 🐳 Docker Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Docker Network: cafe-lumiere-network         │
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │  frontend    │  │   kitchen    │  │    order     │         │
│  │  container   │  │   service    │  │   service    │         │
│  │              │  │  container   │  │  container   │         │
│  │  Port: 5000  │  │  Port: 5002  │  │  Port: 5001  │         │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘         │
│         │                 │                  │                 │
│         └─────────────────┴──────────────────┘                 │
│                           │                                    │
│                           │                                    │
│                  ┌────────▼─────────┐                          │
│                  │    postgres      │                          │
│                  │    container     │                          │
│                  │                  │                          │
│                  │    Port: 5432    │                          │
│                  └──────────────────┘                          │
│                           │                                    │
│                  ┌────────▼─────────┐                          │
│                  │  Volume:         │                          │
│                  │  postgres-data   │                          │
│                  └──────────────────┘                          │
└─────────────────────────────────────────────────────────────────┘

Host Machine:
  localhost:5000  →  frontend
  localhost:5001  →  order-service
  localhost:5002  →  kitchen-service
  localhost:5432  →  postgres
```

## ☸️ Kubernetes Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                  Namespace: cafe-lumiere                         │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ Ingress / LoadBalancer                                      ││
│  │ External Access → Frontend Service                          ││
│  └───────────────────┬─────────────────────────────────────────┘│
│                      │                                           │
│  ┌───────────────────▼──────────────┐                           │
│  │ Service: frontend (LoadBalancer) │                           │
│  │ Port: 80 → 5000                  │                           │
│  └───────────────────┬──────────────┘                           │
│                      │                                           │
│  ┌───────────────────▼──────────────┐                           │
│  │ Deployment: frontend             │                           │
│  │ Replicas: 2                      │                           │
│  │ ┌──────────┐  ┌──────────┐      │                           │
│  │ │ Pod 1    │  │ Pod 2    │      │                           │
│  │ └──────────┘  └──────────┘      │                           │
│  └──────────────────────────────────┘                           │
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ Services: order-service, kitchen-service (ClusterIP)       │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
│  ┌──────────────────┐  ┌──────────────────┐                    │
│  │ Deployment:      │  │ Deployment:      │                    │
│  │ order-service    │  │ kitchen-service  │                    │
│  │ Replicas: 2      │  │ Replicas: 2      │                    │
│  └────────┬─────────┘  └──────────────────┘                    │
│           │                                                     │
│  ┌────────▼───────────────────────────────────────────────────┐│
│  │ Service: cafe-lumiere-postgresql (ClusterIP)              ││
│  │ Port: 5432                                                 ││
│  └────────┬───────────────────────────────────────────────────┘│
│           │                                                     │
│  ┌────────▼───────────────────────────────────────────────────┐│
│  │ StatefulSet: cafe-lumiere-postgresql                       ││
│  │ Replicas: 1                                                ││
│  │ ┌────────────┐                                             ││
│  │ │ Pod        │                                             ││
│  │ │ PostgreSQL │                                             ││
│  │ └─────┬──────┘                                             ││
│  │       │                                                     ││
│  │ ┌─────▼──────────────┐                                     ││
│  │ │ PVC: 1Gi           │                                     ││
│  │ └────────────────────┘                                     ││
│  └────────────────────────────────────────────────────────────┘│
│                                                                  │
│  ConfigMap: cafe-config    Secret: cafe-secrets                 │
└──────────────────────────────────────────────────────────────────┘
```

## 📡 API Communication Matrix

| From | To | Method | Endpoint | Purpose |
|------|------|--------|----------|---------|
| Frontend | Order Service | POST | /orders | Create new order |
| Frontend | Order Service | GET | /orders | Get all orders |
| Frontend | Order Service | GET | /orders/{id} | Get specific order |
| Kitchen Service | Order Service | GET | /orders | Fetch all orders |
| Kitchen Service | Order Service | PUT | /orders/{id} | Update order status |
| Order Service | PostgreSQL | SQL | - | Database operations |

## 🔐 Security Considerations

### Current Setup (Development)
- ⚠️ Default PostgreSQL credentials
- ⚠️ No authentication on endpoints
- ⚠️ No HTTPS/TLS
- ⚠️ Debug mode enabled
- ⚠️ CORS wide open

### Production Requirements
- ✅ Strong database passwords
- ✅ API authentication (JWT/OAuth)
- ✅ HTTPS with valid certificates
- ✅ Production mode (debug off)
- ✅ Restricted CORS origins
- ✅ Rate limiting
- ✅ Input validation & sanitization
- ✅ SQL injection prevention (using parameterized queries ✓)

## 📊 Technology Stack Summary

| Layer | Technology | Version | Purpose |
|-------|-----------|---------|---------|
| **Language** | Python | 3.11 | All services |
| **Web Framework** | Flask | 3.0.2 | HTTP services |
| **Database** | PostgreSQL | 15 | Data persistence |
| **DB Driver** | psycopg2-binary | 2.9.9 | PostgreSQL connection |
| **HTTP Client** | requests | 2.31.0 | Service communication |
| **CORS** | flask-cors | 4.0.0 | Cross-origin requests |
| **Template Engine** | Jinja2 | (with Flask) | HTML rendering |
| **Container** | Docker | - | Application packaging |
| **Orchestration** | Kubernetes | - | Container management |
| **Package Manager** | Helm | 3.x | Database deployment |
| **WSGI Server** | Gunicorn | 21.2.0 | Production server |

## 🔄 Communication Patterns

### Synchronous REST
- Frontend ↔ Order Service
- Frontend ↔ Kitchen Service
- Kitchen Service ↔ Order Service

### Database Connection
- Order Service → PostgreSQL (psycopg2 with connection pooling)

### Retry Mechanisms
- **Kitchen Service → Order Service**: 3 retries with exponential backoff
- **Order Service → PostgreSQL**: 10 retries with 3s delay

### Health Checks
- All services expose `/health` endpoint
- Order Service checks database connectivity
- Kitchen Service checks Order Service connectivity
- Docker health checks every 10s
- Kubernetes liveness/readiness probes

## 📈 Scalability Design

### Horizontal Scaling
```
Load Balancer
      │
      ├─────► Frontend Pod 1
      ├─────► Frontend Pod 2
      │
      ├─────► Order Service Pod 1
      ├─────► Order Service Pod 2
      │
      ├─────► Kitchen Service Pod 1
      └─────► Kitchen Service Pod 2
```

### Stateless Services
- ✅ Frontend: No session storage
- ✅ Order Service: State in database only
- ✅ Kitchen Service: Fully stateless

### Database Scaling (Future)
- Read replicas for query load
- Connection pooling (pgbouncer)
- Partitioning by date

## 🎯 Performance Characteristics

| Metric | Target | Notes |
|--------|--------|-------|
| Order Creation | <100ms | Includes DB write |
| Order Retrieval | <50ms | Single order lookup |
| List All Orders | <200ms | Full table scan |
| Status Update | <100ms | Update + commit |
| Frontend Load | <500ms | Initial page load |
| Health Check | <10ms | Simple query |

## 🛠️ Development vs Production

| Aspect | Development | Production |
|--------|-------------|------------|
| Database | Docker container | Managed service (RDS/Cloud SQL) |
| Secrets | Environment variables | Secrets manager |
| Scaling | Single instance | Auto-scaling groups |
| Logging | stdout | Centralized (ELK/CloudWatch) |
| Monitoring | None | Prometheus + Grafana |
| SSL/TLS | No | Yes (Let's Encrypt/ACM) |
| Load Balancer | None | ALB/GKE Ingress |

---

## 📚 Further Reading

- [GETTING_STARTED.md](GETTING_STARTED.md) - Quick start guide
- [DATABASE_SETUP.md](DATABASE_SETUP.md) - Database configuration
- [DEPLOYMENT.md](DEPLOYMENT.md) - Deployment instructions
- [README.md](README.md) - Project overview

---

**Built with ❤️ for DevOps learning** • **Café Lumière** ☕✨
