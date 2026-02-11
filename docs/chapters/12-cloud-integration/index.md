# Chapter 12: Cloud Integration and APIs

## Learning Objectives

By the end of this chapter, you will be able to:

- Explain why integration eliminates data silos and creates connected systems
- Describe TankScan's open API architecture and partnership approach
- Apply REST API fundamentals to retrieve tank data programmatically
- Design cloud-to-cloud integrations between TankScan and enterprise systems
- Implement ERP, SCADA, and fleet management integrations
- Configure webhooks for real-time event-driven data streaming
- Apply security best practices including OAuth and API key management
- Build custom applications and dashboards on TankScan data

---

## 12.1 Why Integration Matters

Tank level data is valuable on its own, but its true power emerges when it flows seamlessly into the systems that drive business decisions. Without integration, tank data becomes a **data silo** -- isolated information that requires manual effort to extract and apply.

### Data Silos vs. Connected Systems

```mermaid
graph TD
    subgraph Siloed["Siloed Architecture"]
        A[TankScan Portal] --- X1[Manual Export]
        B[ERP System] --- X2[Manual Entry]
        C[Dispatch System] --- X3[Phone Calls]
        D[Billing System] --- X4[Spreadsheets]
        X1 -.- X2
        X2 -.- X3
        X3 -.- X4
    end

    subgraph Connected["Connected Architecture"]
        E[TankScan API] --> F[ERP System]
        E --> G[Dispatch System]
        E --> H[Billing System]
        E --> I[Analytics Platform]
        E --> J[Customer Portal]
    end

    style Siloed fill:#ffeeee,stroke:#cc0000
    style Connected fill:#eeffee,stroke:#00cc00
```

### The Cost of Manual Data Transfer

| Manual Process | Time per Occurrence | Frequency | Annual Cost (at $35/hr) |
|---|---|---|---|
| Export tank data, import to ERP | 30 minutes | Daily | $6,388 |
| Call dispatch with tank levels | 10 minutes | 50 tanks/day | $30,333 |
| Reconcile deliveries manually | 45 minutes | Per delivery | Varies widely |
| Create customer reports | 2 hours | Monthly per customer | $840/customer/year |
| **Total potential savings** | | | **$50,000 - $200,000/year** |

!!! tip "Integration ROI"
    For most TankScan customers, the ROI on API integration exceeds the ROI on the monitoring hardware itself. A distributor with 500 monitored tanks typically recovers their integration development cost within 3-6 months through labor savings alone.

### Integration Use Cases

1. **Automatic reorder triggering** -- When a tank drops below a threshold, an order is created in the ERP
2. **Route optimization** -- Dispatch system receives real-time levels to plan efficient delivery routes
3. **Automated billing** -- Consumption data flows directly into invoicing systems
4. **Customer self-service** -- Customers view their own tank levels on a branded portal
5. **Regulatory reporting** -- Tank data feeds compliance reports automatically
6. **Predictive analytics** -- Historical data streams into ML models for demand forecasting

---

## 12.2 TankScan's Open API Architecture

TankScan is built on an **open API architecture**, meaning that third-party systems can programmatically access tank data without proprietary middleware or vendor lock-in.

### Architectural Philosophy

TankScan follows three core principles in its API design:

1. **Open standards** -- RESTful APIs using JSON over HTTPS
2. **Partner-friendly** -- Documentation, sandbox environments, and support for integration partners
3. **Secure by default** -- Authentication required for all endpoints, data encrypted in transit

### System Architecture Overview

```mermaid
flowchart TD
    subgraph Field["Field Layer"]
        S1[Sensor 1] --> GW[TankScan Gateway]
        S2[Sensor 2] --> GW
        S3[Sensor N] --> GW
    end

    subgraph Cloud["TankScan Cloud"]
        GW -->|Cellular/WiFi| ING[Ingestion Service]
        ING --> DB[(Time-Series Database)]
        DB --> API[REST API Layer]
        DB --> WH[Webhook Engine]
        DB --> STREAM[Streaming Service]
        API --> AUTH[Auth Service]
    end

    subgraph Consumers["API Consumers"]
        API --> ERP[ERP Systems]
        API --> SCADA[SCADA Systems]
        API --> CUSTOM[Custom Apps]
        WH --> DISPATCH[Dispatch Systems]
        STREAM --> ANALYTICS[Analytics Platforms]
    end

    style Field fill:#e8f4fd,stroke:#2196F3
    style Cloud fill:#fff3e0,stroke:#FF9800
    style Consumers fill:#e8f5e9,stroke:#4CAF50
```

### Partnership Approach

TankScan maintains a **partner ecosystem** for integrations:

| Partner Tier | Access Level | Support | Examples |
|---|---|---|---|
| **Technology Partner** | Full API access, sandbox, early feature access | Dedicated integration engineer | ERP vendors, fleet management platforms |
| **Solution Partner** | Full API access, sandbox | Technical documentation, email support | System integrators, VARs |
| **Customer Developer** | API access for own account data | Documentation, community forums | In-house IT teams building custom dashboards |

---

## 12.3 REST API Fundamentals

To work effectively with TankScan's API, you need to understand the fundamentals of RESTful web services.

### What Is REST?

**REST** (Representational State Transfer) is an architectural style for designing networked applications. A RESTful API uses standard HTTP methods to perform operations on resources identified by URLs.

### HTTP Methods

| Method | Operation | Description | Example |
|---|---|---|---|
| `GET` | Read | Retrieve a resource or collection | Get current tank level |
| `POST` | Create | Create a new resource | Create a new alert rule |
| `PUT` | Update (full) | Replace a resource entirely | Update tank configuration |
| `PATCH` | Update (partial) | Modify specific fields of a resource | Change alert threshold |
| `DELETE` | Remove | Delete a resource | Remove an alert rule |

### Anatomy of an API Request

```
GET /api/v2/tanks/12345/readings?start=2025-01-01&end=2025-01-31 HTTP/1.1
Host: api.tankscan.com
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
Accept: application/json
Content-Type: application/json
```

Breaking this down:

| Component | Value | Purpose |
|---|---|---|
| **Method** | `GET` | We want to retrieve data |
| **Path** | `/api/v2/tanks/12345/readings` | The specific resource (readings for tank 12345) |
| **Query Parameters** | `start=2025-01-01&end=2025-01-31` | Filter criteria |
| **Host** | `api.tankscan.com` | The API server |
| **Authorization** | `Bearer eyJ...` | Authentication token |
| **Accept** | `application/json` | We want JSON response format |

### HTTP Status Codes

Understanding response codes is essential for robust integration development:

| Code | Category | Meaning | Action Required |
|---|---|---|---|
| `200` | Success | Request succeeded | Process the response data |
| `201` | Success | Resource created | Store the new resource ID |
| `204` | Success | No content (successful delete) | Confirm deletion |
| `400` | Client Error | Bad request (malformed syntax) | Fix the request format |
| `401` | Client Error | Unauthorized (invalid/missing auth) | Refresh authentication token |
| `403` | Client Error | Forbidden (insufficient permissions) | Check API key permissions |
| `404` | Client Error | Resource not found | Verify the resource ID/path |
| `429` | Client Error | Too many requests (rate limited) | Implement backoff and retry |
| `500` | Server Error | Internal server error | Retry after delay; contact support if persistent |
| `503` | Server Error | Service unavailable | Retry with exponential backoff |

!!! warning "Error Handling Is Not Optional"
    Every API integration must handle error responses gracefully. A common mistake is only coding for the "happy path" (200 responses). Production integrations must handle authentication failures, rate limiting, network timeouts, and server errors with appropriate retry logic.

---

## 12.4 Retrieving Tank Data via API

The most common API operation is retrieving tank level data. Here are the key endpoints and usage patterns.

### Core Endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/api/v2/tanks` | GET | List all tanks in your account |
| `/api/v2/tanks/{id}` | GET | Get details for a specific tank |
| `/api/v2/tanks/{id}/readings` | GET | Get level readings for a tank |
| `/api/v2/tanks/{id}/readings/latest` | GET | Get the most recent reading |
| `/api/v2/tanks/{id}/alerts` | GET | Get alert history for a tank |
| `/api/v2/groups` | GET | List tank groups |
| `/api/v2/groups/{id}/tanks` | GET | List tanks in a group |

### Example: Get Current Tank Level

**Request:**

```bash
curl -X GET "https://api.tankscan.com/api/v2/tanks/12345/readings/latest" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Accept: application/json"
```

**Response:**

```json
{
  "tank_id": "12345",
  "tank_name": "Diesel Tank - Building A",
  "reading": {
    "timestamp": "2025-03-15T14:30:00Z",
    "level_percent": 67.4,
    "level_inches": 48.5,
    "volume_gallons": 3370,
    "temperature_f": 62.3,
    "signal_strength_dbm": -72,
    "battery_percent": 94
  },
  "tank": {
    "capacity_gallons": 5000,
    "product": "Diesel #2",
    "location": {
      "latitude": 41.8781,
      "longitude": -87.6298,
      "address": "123 Industrial Blvd, Chicago, IL"
    }
  }
}
```

### Example: Get Historical Readings

**Request:**

```bash
curl -X GET "https://api.tankscan.com/api/v2/tanks/12345/readings\
?start=2025-03-01T00:00:00Z\
&end=2025-03-15T23:59:59Z\
&interval=hourly" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Accept: application/json"
```

**Response (abbreviated):**

```json
{
  "tank_id": "12345",
  "period": {
    "start": "2025-03-01T00:00:00Z",
    "end": "2025-03-15T23:59:59Z"
  },
  "interval": "hourly",
  "readings": [
    {
      "timestamp": "2025-03-01T00:00:00Z",
      "level_percent": 82.1,
      "volume_gallons": 4105
    },
    {
      "timestamp": "2025-03-01T01:00:00Z",
      "level_percent": 82.0,
      "volume_gallons": 4100
    }
  ],
  "total_readings": 360,
  "pagination": {
    "page": 1,
    "per_page": 100,
    "total_pages": 4
  }
}
```

### Python SDK Example

```python
import tankscan

# Initialize client
client = tankscan.Client(api_key="YOUR_API_KEY")

# Get all tanks
tanks = client.tanks.list()

# Get latest reading for a specific tank
reading = client.tanks.get_latest_reading(tank_id="12345")
print(f"Tank level: {reading.level_percent}%")
print(f"Volume: {reading.volume_gallons} gallons")

# Get historical readings
from datetime import datetime, timedelta

readings = client.tanks.get_readings(
    tank_id="12345",
    start=datetime.now() - timedelta(days=30),
    end=datetime.now(),
    interval="daily"
)

# Convert to pandas DataFrame for analysis
import pandas as pd
df = pd.DataFrame([r.to_dict() for r in readings])
print(df.describe())
```

!!! note "SDK Availability"
    TankScan provides official SDKs for Python, JavaScript/Node.js, and C#/.NET. Community-maintained libraries are available for Java, Go, and Ruby. Check the developer portal for the latest versions.

---

## 12.5 Cloud-to-Cloud Integration

Cloud-to-cloud (C2C) integration connects TankScan's cloud platform directly to other cloud-based business systems without any on-premises middleware.

### Integration Patterns

```mermaid
flowchart LR
    subgraph Pattern1["Pattern 1: API Polling"]
        A1[External System] -->|Periodic GET requests| B1[TankScan API]
    end

    subgraph Pattern2["Pattern 2: Webhooks"]
        A2[TankScan Webhook] -->|Event-driven POST| B2[External Endpoint]
    end

    subgraph Pattern3["Pattern 3: Middleware"]
        A3[TankScan API] <-->|Bidirectional| C3[Integration Platform<br/>Zapier, MuleSoft, etc.]
        C3 <-->|Bidirectional| B3[External System]
    end

    subgraph Pattern4["Pattern 4: Data Lake"]
        A4[TankScan Export] -->|Batch or streaming| D4[(Data Lake<br/>S3, Azure Blob, GCS)]
        D4 --> B4[Analytics Platform]
    end
```

| Pattern | Best For | Latency | Complexity | Cost |
|---|---|---|---|---|
| **API Polling** | Periodic data sync, batch updates | Minutes to hours | Low | Low (API calls) |
| **Webhooks** | Real-time alerts, event-driven workflows | Seconds | Medium | Low (event-based) |
| **Middleware/iPaaS** | Complex transformations, multi-system orchestration | Seconds to minutes | Medium-High | Medium (platform fees) |
| **Data Lake** | Historical analytics, ML training, regulatory archives | Minutes to hours | High | Medium-High (storage + compute) |

### Pre-Built Connectors

TankScan maintains pre-built connectors for popular integration platforms:

| Platform | Type | Supported Operations |
|---|---|---|
| **Zapier** | No-code iPaaS | Triggers: new reading, alert fired. Actions: get tank data |
| **Microsoft Power Automate** | Low-code iPaaS | Triggers: level threshold, alert. Actions: read tank data |
| **MuleSoft** | Enterprise iPaaS | Full bidirectional API connector |
| **Dell Boomi** | Enterprise iPaaS | Full bidirectional API connector |
| **Workato** | Enterprise iPaaS | Full bidirectional API connector |

!!! example "Example: Zapier Integration"
    A common no-code integration using Zapier:

    **Trigger:** TankScan alert fires (tank below 20%)

    **Actions:**
    1. Create a new order in QuickBooks for product replenishment
    2. Send a Slack notification to the dispatch channel
    3. Add a row to a Google Sheet for tracking
    4. Send an email to the customer

    This entire workflow can be configured in 30 minutes without writing any code.

---

## 12.6 ERP Integration

Enterprise Resource Planning (ERP) integration is the highest-value integration for most TankScan customers because it connects physical tank data to financial and operational processes.

### Common ERP Integration Points

| ERP Process | TankScan Data Input | Resulting Action |
|---|---|---|
| **Inventory Management** | Current tank levels, volumes | Real-time inventory quantities |
| **Purchase Orders** | Low-level alerts | Automatic PO generation |
| **Sales Orders** | Consumption rate data | Proactive customer replenishment |
| **Billing/Invoicing** | Delivery volumes (before/after) | Accurate usage-based billing |
| **Financial Reporting** | Inventory valuation | Mark-to-market commodity accounting |
| **Demand Planning** | Historical consumption patterns | Forecast accuracy improvement |

### SAP Integration Architecture

```mermaid
flowchart LR
    A[TankScan Cloud API] -->|REST/JSON| B[SAP Integration Suite<br/>or SAP CPI]
    B -->|IDoc/BAPI/RFC| C[SAP S/4HANA]

    C --> D[MM Module<br/>Materials Management]
    C --> E[SD Module<br/>Sales & Distribution]
    C --> F[PP Module<br/>Production Planning]
    C --> G[FI Module<br/>Financial Accounting]

    D -->|Stock levels| H[Inventory Dashboard]
    E -->|Delivery orders| I[Route Planning]
    F -->|Supply signals| J[Production Schedule]
    G -->|Valuation| K[Financial Reports]
```

**Key SAP integration scenarios:**

1. **Material Document Creation** -- Each tank reading updates the material stock quantity in SAP MM
2. **Purchase Requisition Trigger** -- When tank level drops below reorder point, SAP creates a PR automatically
3. **Delivery Confirmation** -- Post-delivery tank reading confirms the quantity received, creating a Goods Receipt
4. **Consumption Posting** -- Period-over-period level decreases generate consumption postings in SAP

### Oracle Integration

For Oracle ERP Cloud or Oracle E-Business Suite:

```python
# Example: Oracle ERP Cloud integration using REST
import requests

# Step 1: Get tank data from TankScan
ts_response = requests.get(
    "https://api.tankscan.com/api/v2/tanks/12345/readings/latest",
    headers={"Authorization": "Bearer TS_API_KEY"}
)
tank_data = ts_response.json()

# Step 2: Create inventory transaction in Oracle
oracle_payload = {
    "OrganizationCode": "M1",
    "ItemNumber": "DIESEL-2",
    "TransactionTypeName": "Miscellaneous receipt",
    "TransactionQuantity": tank_data["reading"]["volume_gallons"],
    "TransactionUnitOfMeasure": "GAL",
    "TransactionDate": tank_data["reading"]["timestamp"]
}

oracle_response = requests.post(
    "https://your-oracle.oraclecloud.com/fscmRestApi/resources/v1/inventoryTransactions",
    json=oracle_payload,
    headers={
        "Authorization": "Bearer ORACLE_TOKEN",
        "Content-Type": "application/json"
    }
)
```

### NetSuite Integration

NetSuite integrations commonly use SuiteTalk (SOAP) or RESTlet (REST) interfaces:

| Integration Method | Best For | Complexity |
|---|---|---|
| **SuiteTalk SOAP API** | Complex, high-volume transactions | High |
| **RESTlet** | Custom endpoints for specific use cases | Medium |
| **SuiteScript Scheduled** | Periodic data sync (polling TankScan API) | Medium |
| **Celigo/Dell Boomi** | Middleware-based, pre-built connectors | Low-Medium |

---

## 12.7 SCADA System Integration

Supervisory Control and Data Acquisition (SCADA) systems are the backbone of industrial process control. Integrating TankScan with SCADA provides a unified operational view.

### Why SCADA Integration Matters

Traditional SCADA systems monitor **wired** sensors in local facilities. TankScan adds **wireless** monitoring of remote tanks. Integration creates a single pane of glass:

```mermaid
flowchart TD
    subgraph Local["Local Plant (SCADA)"]
        A[Wired Level Sensors] --> B[PLC/RTU]
        C[Flow Meters] --> B
        D[Pressure Sensors] --> B
        B --> E[SCADA Server]
    end

    subgraph Remote["Remote Tanks (TankScan)"]
        F[Wireless Sensors] --> G[TankScan Gateway]
        G --> H[TankScan Cloud]
    end

    H -->|OPC UA / API / MQTT| E

    E --> I[Unified HMI Dashboard]

    style Local fill:#e8f4fd,stroke:#2196F3
    style Remote fill:#fff3e0,stroke:#FF9800
```

### Integration Protocols for SCADA

| Protocol | Description | Use Case | Direction |
|---|---|---|---|
| **OPC UA** | Open Platform Communications Unified Architecture | Modern SCADA systems | TankScan to SCADA |
| **Modbus TCP** | Simple, widely supported industrial protocol | Legacy SCADA systems | TankScan to SCADA |
| **MQTT** | Lightweight pub/sub messaging | IoT-native SCADA, edge systems | Bidirectional |
| **REST API** | HTTP-based data retrieval | IT/OT convergence platforms | TankScan to SCADA |
| **DNP3** | Distributed Network Protocol | Utility SCADA systems | TankScan to SCADA |

### OPC UA Integration Example

OPC UA (Open Platform Communications Unified Architecture) is the modern standard for industrial interoperability:

```
OPC UA Address Space Mapping:

Root
└── Objects
    └── TankScan
        ├── Tank_12345
        │   ├── LevelPercent    (Float, ReadOnly)  = 67.4
        │   ├── VolumeGallons   (Float, ReadOnly)  = 3370
        │   ├── TemperatureF    (Float, ReadOnly)  = 62.3
        │   ├── LastUpdate      (DateTime, ReadOnly) = 2025-03-15T14:30:00Z
        │   ├── BatteryPercent  (Int, ReadOnly)    = 94
        │   └── Alarms
        │       ├── HighLevel   (Boolean, ReadOnly) = false
        │       └── LowLevel    (Boolean, ReadOnly) = false
        ├── Tank_12346
        │   └── ...
        └── Gateway_001
            ├── Status          (String, ReadOnly)  = "Online"
            └── LastHeartbeat   (DateTime, ReadOnly) = 2025-03-15T14:29:00Z
```

### MQTT Integration Pattern

MQTT is increasingly popular for IoT-SCADA convergence:

```python
# MQTT subscriber for TankScan data
import paho.mqtt.client as mqtt
import json

def on_message(client, userdata, msg):
    data = json.loads(msg.payload)
    tank_id = data["tank_id"]
    level = data["level_percent"]

    # Forward to local SCADA/PLC
    update_scada_point(tank_id, level)

    # Check for alarm conditions
    if level > 95:
        trigger_high_level_alarm(tank_id)
    elif level < 15:
        trigger_low_level_alarm(tank_id)

client = mqtt.Client()
client.username_pw_set("tankscan_user", "password")
client.tls_set()
client.on_message = on_message
client.connect("mqtt.tankscan.com", 8883)

# Subscribe to all tank readings
client.subscribe("tankscan/readings/#")
client.loop_forever()
```

!!! note "IT/OT Convergence"
    The integration of TankScan (an IT/cloud system) with SCADA (an OT/operational system) is an example of **IT/OT convergence**. This convergence is a major trend in industrial operations, and security must be carefully managed at the boundary between IT and OT networks.

---

## 12.8 Fleet Management System Integration

For distributors who deliver bulk products to monitored tanks, fleet management integration closes the loop between tank data and delivery operations.

### Integration Flow

```mermaid
sequenceDiagram
    participant TS as TankScan Cloud
    participant FM as Fleet Management
    participant DR as Driver Mobile App
    participant TR as Delivery Truck

    TS->>FM: Tank 456 at 18% (low-level alert)
    FM->>FM: Generate delivery order
    FM->>FM: Optimize route with other deliveries
    FM->>DR: Assign delivery to route
    DR->>TR: Navigate to customer site
    TR->>TR: Deliver product
    DR->>FM: Confirm delivery (gallons pumped)
    FM->>TS: Delivery confirmed
    TS->>TS: Verify level increase matches delivery
    TS->>FM: Delivery reconciliation complete
```

### Common Fleet Management Integrations

| System | Integration Method | Key Data Exchanged |
|---|---|---|
| **Lytx/Omnitracs** | REST API | Tank locations, delivery requirements, route suggestions |
| **Trimble TMT** | API + File exchange | Work orders, delivery confirmations |
| **Descartes** | API | Route optimization inputs, delivery windows |
| **Samsara** | REST API | Vehicle location, tank locations, delivery status |
| **Custom Dispatch** | TankScan API | Tank levels, alerts, delivery history |

### Data Fields for Fleet Integration

| Field | Source | Used For |
|---|---|---|
| Tank ID | TankScan | Unique identifier for delivery location |
| Current level (%) | TankScan | Delivery urgency prioritization |
| Estimated days until empty | TankScan (calculated) | Delivery scheduling window |
| Tank capacity | TankScan | Maximum delivery volume calculation |
| Delivery volume needed | TankScan (calculated) | $V_{needed} = V_{capacity} \times (Target\% - Current\%) / 100$ |
| GPS coordinates | TankScan | Route optimization |
| Access hours | Customer data | Delivery time window constraints |
| Product type | TankScan | Truck/compartment assignment |

---

## 12.9 Data Export Formats

Not all integrations require real-time API calls. TankScan supports multiple export formats for batch processing, reporting, and archival.

### Supported Formats

| Format | Best For | Structure | Human Readable |
|---|---|---|---|
| **JSON** | API responses, web apps, modern systems | Hierarchical | Moderate |
| **CSV** | Spreadsheets, simple imports, legacy systems | Tabular | High |
| **XML** | Enterprise systems, SOAP services, EDI | Hierarchical | Low-Moderate |
| **Excel (XLSX)** | Business reporting, ad-hoc analysis | Tabular with formatting | High |
| **PDF** | Compliance reports, customer deliverables | Formatted document | High |

### JSON Export Example

```json
{
  "export_metadata": {
    "generated_at": "2025-03-15T15:00:00Z",
    "format_version": "2.1",
    "tank_count": 3,
    "reading_count": 2160
  },
  "tanks": [
    {
      "id": "12345",
      "name": "Diesel Tank A",
      "readings": [
        {"timestamp": "2025-03-01T00:00:00Z", "level_pct": 82.1, "vol_gal": 4105},
        {"timestamp": "2025-03-01T01:00:00Z", "level_pct": 82.0, "vol_gal": 4100}
      ]
    }
  ]
}
```

### CSV Export Example

```csv
tank_id,tank_name,timestamp,level_percent,volume_gallons,temperature_f
12345,Diesel Tank A,2025-03-01T00:00:00Z,82.1,4105,58.2
12345,Diesel Tank A,2025-03-01T01:00:00Z,82.0,4100,57.9
12346,Gasoline Tank B,2025-03-01T00:00:00Z,45.3,2265,59.1
```

### XML Export Example

```xml
<?xml version="1.0" encoding="UTF-8"?>
<TankScanExport version="2.1" generated="2025-03-15T15:00:00Z">
  <Tanks>
    <Tank id="12345" name="Diesel Tank A" capacity="5000" unit="gallons">
      <Reading timestamp="2025-03-01T00:00:00Z">
        <LevelPercent>82.1</LevelPercent>
        <VolumeGallons>4105</VolumeGallons>
        <TemperatureF>58.2</TemperatureF>
      </Reading>
    </Tank>
  </Tanks>
</TankScanExport>
```

!!! tip "Choosing the Right Format"
    - Use **JSON** for modern software integrations and web applications
    - Use **CSV** when the consumer is a spreadsheet, database import, or legacy system
    - Use **XML** when required by enterprise systems (SAP IDocs, EDI, etc.)
    - Use **Excel** for business stakeholders who need formatted, ready-to-use reports
    - Use **PDF** for formal compliance submissions and customer deliverables

---

## 12.10 Webhooks and Real-Time Data Streaming

While polling the API on a schedule works for many use cases, some scenarios demand immediate notification when events occur. Webhooks and streaming address this need.

### What Are Webhooks?

A **webhook** is a user-defined HTTP callback. Instead of your system asking TankScan "has anything changed?" repeatedly (polling), TankScan tells your system "something just happened" the moment it occurs (push).

```mermaid
sequenceDiagram
    participant TS as TankScan Cloud
    participant YS as Your System

    Note over TS,YS: Polling Pattern (Inefficient)
    loop Every 5 minutes
        YS->>TS: GET /tanks/12345/readings/latest
        TS->>YS: 200 OK (same data, no change)
    end

    Note over TS,YS: Webhook Pattern (Efficient)
    TS->>YS: POST /your-webhook-endpoint<br/>{"event": "level_alert", "tank_id": "12345", "level": 18.5}
    YS->>TS: 200 OK (acknowledged)
```

### Configuring Webhooks

```bash
# Register a webhook endpoint
curl -X POST "https://api.tankscan.com/api/v2/webhooks" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://your-system.com/tankscan/events",
    "events": ["level.alert", "level.reading", "sensor.offline", "delivery.detected"],
    "secret": "your_webhook_signing_secret",
    "active": true
  }'
```

### Webhook Event Types

| Event | Trigger | Typical Use |
|---|---|---|
| `level.alert` | Tank level crosses a configured threshold | Trigger reorders, dispatch alerts |
| `level.reading` | New reading received from sensor | Real-time dashboard updates |
| `sensor.offline` | Sensor stops reporting | Maintenance dispatch |
| `sensor.battery_low` | Battery below threshold | Preventive maintenance |
| `delivery.detected` | Significant level increase detected | Delivery reconciliation |
| `consumption.anomaly` | Unusual consumption pattern detected | Theft/leak investigation |
| `gateway.offline` | Gateway stops communicating | Network troubleshooting |

### Webhook Security

!!! warning "Verify Webhook Signatures"
    Always verify that incoming webhook requests genuinely originate from TankScan. Every webhook request includes a signature header that you must validate:

```python
import hmac
import hashlib

def verify_webhook(payload_body, signature_header, secret):
    """Verify TankScan webhook signature."""
    expected_signature = hmac.new(
        key=secret.encode('utf-8'),
        msg=payload_body,
        digestmod=hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(
        f"sha256={expected_signature}",
        signature_header
    )

# In your webhook handler
from flask import Flask, request, abort

app = Flask(__name__)

@app.route('/tankscan/events', methods=['POST'])
def handle_webhook():
    signature = request.headers.get('X-TankScan-Signature')

    if not verify_webhook(request.data, signature, WEBHOOK_SECRET):
        abort(401)  # Reject unsigned/invalid requests

    event = request.json
    process_event(event)
    return '', 200
```

### Real-Time Streaming

For applications that need continuous data streams (dashboards, analytics), TankScan supports Server-Sent Events (SSE):

```javascript
// Browser-side JavaScript for real-time dashboard
const eventSource = new EventSource(
    'https://api.tankscan.com/api/v2/stream/readings?token=YOUR_TOKEN'
);

eventSource.onmessage = function(event) {
    const data = JSON.parse(event.data);
    updateDashboard(data.tank_id, data.level_percent);
};

eventSource.onerror = function(err) {
    console.error('Stream error:', err);
    // Implement reconnection logic
};
```

---

## 12.11 Building Custom Applications on TankScan Data

The TankScan API enables building entirely custom applications tailored to specific business needs.

### Common Custom Application Types

| Application | Description | Primary Users |
|---|---|---|
| **Customer Portal** | White-labeled dashboard showing customers their own tank levels | End customers |
| **Dispatch Dashboard** | Real-time map of all tanks with delivery urgency indicators | Dispatch operators |
| **Executive KPI Board** | Aggregate metrics: fill rates, service levels, consumption trends | Management |
| **Field Technician App** | Mobile app for sensor installation, diagnostics, maintenance | Field technicians |
| **Consumption Analytics** | Deep analysis of usage patterns, forecasting | Analysts |

### Architecture for a Custom Web Application

```mermaid
flowchart TD
    A[TankScan API] --> B[Backend Server<br/>Node.js / Python / .NET]
    B --> C[Application Database<br/>PostgreSQL / MongoDB]
    B --> D[Frontend Application<br/>React / Vue / Angular]

    B --> E[Authentication<br/>Your user accounts]
    B --> F[Business Logic<br/>Custom rules, calculations]
    B --> G[Notification Service<br/>Email, SMS, Push]

    D --> H[Map View<br/>Tank locations]
    D --> I[Charts<br/>Level trends]
    D --> J[Tables<br/>Tank inventory]
    D --> K[Alerts Panel<br/>Active alarms]

    style A fill:#FF9800,color:#fff
    style B fill:#2196F3,color:#fff
    style D fill:#4CAF50,color:#fff
```

### Example: Simple Python Dashboard

```python
"""
Simple TankScan Dashboard using Streamlit
"""
import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta

# Configuration
API_BASE = "https://api.tankscan.com/api/v2"
API_KEY = st.secrets["tankscan_api_key"]
headers = {"Authorization": f"Bearer {API_KEY}"}

# Page setup
st.title("Tank Monitoring Dashboard")

# Fetch all tanks
tanks = requests.get(f"{API_BASE}/tanks", headers=headers).json()

# Display summary metrics
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Tanks", len(tanks))
col2.metric("Low Level", sum(1 for t in tanks if t["latest_level"] < 20))
col3.metric("High Level", sum(1 for t in tanks if t["latest_level"] > 90))
col4.metric("Offline", sum(1 for t in tanks if not t["online"]))

# Tank level chart for selected tank
selected_tank = st.selectbox(
    "Select Tank",
    [(t["id"], t["name"]) for t in tanks],
    format_func=lambda x: x[1]
)

if selected_tank:
    readings = requests.get(
        f"{API_BASE}/tanks/{selected_tank[0]}/readings",
        headers=headers,
        params={
            "start": (datetime.now() - timedelta(days=30)).isoformat(),
            "end": datetime.now().isoformat()
        }
    ).json()

    df = pd.DataFrame(readings["readings"])
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    st.line_chart(df.set_index("timestamp")["level_percent"])
```

!!! tip "Development Best Practice"
    Cache TankScan API responses in your application database to reduce API calls and improve response times. Tank levels typically update every 15-60 minutes, so caching for 5-10 minutes is perfectly acceptable for dashboard applications.

---

## 12.12 API Rate Limits and Best Practices

To ensure fair usage and system stability, TankScan enforces rate limits on API access.

### Rate Limit Tiers

| Tier | Requests/Minute | Requests/Hour | Requests/Day | Typical Use Case |
|---|---|---|---|---|
| **Standard** | 60 | 1,000 | 10,000 | Single-system integration |
| **Professional** | 300 | 5,000 | 50,000 | Multi-system integration |
| **Enterprise** | 1,000 | 20,000 | 200,000 | High-volume, real-time applications |
| **Custom** | Negotiable | Negotiable | Negotiable | Special requirements |

### Rate Limit Headers

Every API response includes headers indicating your current rate limit status:

```
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 45
X-RateLimit-Reset: 1710512460
```

### Implementing Exponential Backoff

When rate limited (HTTP 429), implement exponential backoff:

```python
import time
import requests

def api_request_with_retry(url, headers, max_retries=5):
    """Make API request with exponential backoff on rate limiting."""
    for attempt in range(max_retries):
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return response.json()
        elif response.status_code == 429:
            # Rate limited - back off exponentially
            wait_time = (2 ** attempt) + (random.random() * 0.5)
            retry_after = response.headers.get('Retry-After')
            if retry_after:
                wait_time = max(wait_time, int(retry_after))

            print(f"Rate limited. Retrying in {wait_time:.1f}s...")
            time.sleep(wait_time)
        elif response.status_code >= 500:
            # Server error - retry with backoff
            wait_time = (2 ** attempt) + (random.random() * 0.5)
            time.sleep(wait_time)
        else:
            # Client error - don't retry
            response.raise_for_status()

    raise Exception(f"Max retries ({max_retries}) exceeded")
```

### Best Practices Summary

| Practice | Description | Impact |
|---|---|---|
| **Cache responses** | Store data locally; re-fetch only when stale | Reduces API calls by 80-90% |
| **Use webhooks** | Subscribe to events instead of polling | Eliminates unnecessary polling |
| **Batch requests** | Fetch multiple tanks in one call where possible | Fewer total requests |
| **Request only needed fields** | Use field selection parameters | Smaller payloads, faster responses |
| **Implement backoff** | Exponential backoff on 429/5xx responses | Prevents cascading failures |
| **Monitor usage** | Track your API consumption against limits | Avoid unexpected rate limiting |
| **Use compression** | Set `Accept-Encoding: gzip` | Reduces bandwidth by 60-80% |

---

## 12.13 Security and Authentication

API security is non-negotiable. Tank level data can reveal sensitive business information including inventory levels, consumption patterns, and customer locations.

### Authentication Methods

| Method | Security Level | Use Case | Token Lifetime |
|---|---|---|---|
| **API Key** | Good | Server-to-server integrations | Long-lived (rotate quarterly) |
| **OAuth 2.0** | Better | User-authorized applications | Short-lived (1 hour typical) |
| **OAuth 2.0 + PKCE** | Best | Single-page and mobile applications | Short-lived with refresh |

### API Key Authentication

The simplest method -- suitable for server-to-server integrations where the key can be securely stored:

```bash
# API Key in Authorization header
curl -H "Authorization: Bearer ts_live_abc123def456" \
     https://api.tankscan.com/api/v2/tanks
```

!!! warning "API Key Security Rules"
    - **Never** embed API keys in client-side code (JavaScript, mobile apps)
    - **Never** commit API keys to version control (Git)
    - **Always** use environment variables or secure key management services
    - **Always** use different keys for development and production
    - **Rotate** keys quarterly and immediately if compromised
    - **Scope** keys to minimum required permissions (read-only if write not needed)

### OAuth 2.0 Authorization Code Flow

For applications where users authorize access to their TankScan data:

```mermaid
sequenceDiagram
    participant U as User
    participant App as Your Application
    participant TS as TankScan Auth Server
    participant API as TankScan API

    U->>App: Click "Connect TankScan"
    App->>TS: Redirect to authorization URL
    TS->>U: Show login & consent screen
    U->>TS: Approve access
    TS->>App: Redirect with authorization code
    App->>TS: Exchange code for access token
    TS->>App: Return access_token + refresh_token
    App->>API: GET /tanks (with access_token)
    API->>App: Return tank data

    Note over App,TS: When access_token expires:
    App->>TS: POST /token (refresh_token)
    TS->>App: New access_token
```

### OAuth 2.0 Implementation Example

```python
from authlib.integrations.requests_client import OAuth2Session

# OAuth2 configuration
client_id = "your_client_id"
client_secret = "your_client_secret"
authorization_url = "https://auth.tankscan.com/authorize"
token_url = "https://auth.tankscan.com/token"
redirect_uri = "https://your-app.com/callback"

# Step 1: Redirect user to authorization
session = OAuth2Session(client_id, client_secret, redirect_uri=redirect_uri)
uri, state = session.create_authorization_url(authorization_url)
# Redirect user to `uri`

# Step 2: Handle callback and exchange code for token
token = session.fetch_token(
    token_url,
    authorization_response=callback_url
)

# Step 3: Make authenticated API calls
response = session.get("https://api.tankscan.com/api/v2/tanks")
tanks = response.json()
```

### Security Best Practices

| Layer | Practice | Implementation |
|---|---|---|
| **Transport** | HTTPS only (TLS 1.2+) | API rejects HTTP connections |
| **Authentication** | OAuth 2.0 or API keys | Required for all endpoints |
| **Authorization** | Role-based access control | Scope tokens to specific permissions |
| **Input Validation** | Validate all API inputs | Prevents injection attacks |
| **Rate Limiting** | Throttle excessive requests | Prevents abuse and DDoS |
| **Logging** | Audit all API access | Detect unauthorized access patterns |
| **Encryption at Rest** | Encrypt stored data | Protects against data breach |
| **IP Allowlisting** | Optional IP-based access control | Additional layer for enterprise |

---

## 12.14 Integration Case Studies

### Case Study 1: Fuel Distributor -- ERP Integration

**Company:** Regional fuel distributor with 800 monitored tanks across 400 customer sites

**Integration:** TankScan API to SAP Business One

**Architecture:**

- Custom middleware running on Azure Functions
- Polls TankScan API every 15 minutes for all tank readings
- Creates inventory adjustments in SAP for each customer's tank
- Generates purchase orders when tanks fall below 25%
- Reconciles deliveries by comparing pre/post delivery levels

**Results:**

| Metric | Before Integration | After Integration | Improvement |
|---|---|---|---|
| Order processing time | 45 minutes manual | 2 minutes automated | 96% reduction |
| Delivery accuracy | 82% on-time | 97% on-time | 18% improvement |
| Billing disputes | 12 per month | 1 per month | 92% reduction |
| Staff time on data entry | 4 FTE | 0.5 FTE | 87% reduction |

### Case Study 2: Chemical Company -- SCADA Integration

**Company:** Specialty chemical manufacturer with 150 tanks across 3 plants

**Integration:** TankScan API to Ignition SCADA via OPC UA

**Architecture:**

- Ignition OPC UA client connects to TankScan's OPC UA endpoint
- Remote tank levels displayed alongside local process variables
- Alarm integration with Ignition's alarm pipeline
- Historical data stored in Ignition's historian alongside process data

**Results:**

- Unified view of all tanks (local wired + remote wireless) in one SCADA display
- Reduced operator training time (one system to learn instead of two)
- Faster response to remote tank issues (alarm latency reduced from 30 minutes to 30 seconds)
- Historical analysis spans both local and remote data

### Case Study 3: Convenience Store Chain -- Custom Application

**Company:** 250-location convenience store chain with underground fuel tanks

**Integration:** TankScan API to custom mobile application

**Architecture:**

- React Native mobile app for store managers
- Node.js backend with PostgreSQL database
- TankScan webhooks for real-time alert forwarding
- Push notifications for critical alerts

**Key Features Built:**

1. Store managers see their location's tank levels on their phone
2. Regional managers see aggregate dashboard of all locations
3. Automatic notification when delivery truck is needed
4. Weekly consumption reports by location and product type
5. Exception alerts: unusual overnight consumption (potential theft)

---

## Chapter 12 Summary

This chapter covered the full spectrum of TankScan cloud integration capabilities:

- **Integration eliminates data silos** and enables automated workflows that save significant labor costs
- **TankScan's REST API** follows open standards (JSON over HTTPS) with robust authentication
- **Core API operations** include retrieving tank lists, current readings, and historical data
- **Cloud-to-cloud integration** patterns include polling, webhooks, middleware, and data lake approaches
- **ERP integration** with SAP, Oracle, and NetSuite automates inventory, ordering, and billing
- **SCADA integration** via OPC UA, MQTT, and Modbus unifies local and remote monitoring
- **Fleet management integration** connects tank data to dispatch and route optimization
- **Multiple export formats** (JSON, CSV, XML, Excel, PDF) serve different consumer needs
- **Webhooks** provide real-time, event-driven data push instead of inefficient polling
- **Custom applications** can be built on the API for tailored business needs
- **Rate limiting and best practices** ensure reliable, sustainable API usage
- **Security** through OAuth 2.0, API keys, HTTPS, and access controls protects sensitive data

---

## Review Questions

!!! question "Question 1 -- Knowledge (Remember)"
    List the five standard HTTP methods used in REST APIs and describe what operation each performs.

    ??? success "Answer"
        1. **GET** -- Read: Retrieves a resource or collection of resources
        2. **POST** -- Create: Creates a new resource
        3. **PUT** -- Update (full): Replaces a resource entirely with the provided data
        4. **PATCH** -- Update (partial): Modifies specific fields of an existing resource
        5. **DELETE** -- Remove: Deletes a resource

!!! question "Question 2 -- Comprehension (Understand)"
    Explain the difference between API polling and webhooks. Why would you choose webhooks over polling for a real-time dispatch dashboard?

    ??? success "Answer"
        **Polling** is when the client repeatedly sends requests to the API at regular intervals (e.g., every 5 minutes) asking "has anything changed?" This is simple but wasteful because most requests return the same data with no changes.

        **Webhooks** are the reverse: the server sends a request to the client only when an event actually occurs. The client registers a callback URL, and TankScan pushes event data to that URL in real-time.

        For a real-time dispatch dashboard, webhooks are superior because: (1) they provide **immediate notification** -- dispatchers see alerts within seconds, not up to 5 minutes later; (2) they are **more efficient** -- no wasted API calls when nothing has changed; (3) they **scale better** -- monitoring 1,000 tanks via polling requires 1,000 requests per interval, while webhooks only fire when events actually occur.

!!! question "Question 3 -- Application (Apply)"
    A distributor wants to automatically create a delivery order in their ERP system when any tank drops below 25% full. The delivery volume should fill the tank to 90%. Write pseudocode for this integration, including the TankScan API call and the ERP order creation.

    ??? success "Answer"
        ```
        # Webhook handler for low-level alerts
        function handle_tankscan_webhook(event):
            if event.type != "level.alert":
                return

            if event.level_percent > 25:
                return  # Not below threshold

            # Get tank details from TankScan API
            tank = GET /api/v2/tanks/{event.tank_id}

            # Calculate delivery volume needed
            target_level = 0.90  # Fill to 90%
            current_level = event.level_percent / 100
            capacity = tank.capacity_gallons
            volume_needed = capacity * (target_level - current_level)

            # Create order in ERP
            order = ERP.create_sales_order(
                customer_id = tank.customer_id,
                product = tank.product_type,
                quantity = round(volume_needed),
                unit = "gallons",
                delivery_address = tank.location.address,
                priority = "normal" if event.level_percent > 15 else "urgent",
                notes = f"Auto-generated from TankScan alert. Current level: {event.level_percent}%"
            )

            # Log the automated order
            log(f"Created order {order.id} for {volume_needed} gal to tank {event.tank_id}")
        ```

!!! question "Question 4 -- Analysis (Analyze)"
    Compare the four cloud-to-cloud integration patterns (API Polling, Webhooks, Middleware/iPaaS, Data Lake) for a scenario where a chemical company needs to: (a) trigger immediate safety alerts, (b) sync daily inventory to SAP, and (c) run quarterly consumption analytics. Which pattern would you recommend for each need, and why?

    ??? success "Answer"
        **(a) Immediate safety alerts -- Webhooks**
        Safety alerts require the lowest possible latency. Webhooks deliver events within seconds of occurrence, making them ideal. Polling could introduce up to a 5-minute delay (depending on polling interval), which is unacceptable for safety. Neither middleware nor data lake patterns are optimal for urgent, real-time alerts.

        **(b) Daily inventory sync to SAP -- Middleware/iPaaS (or API Polling)**
        Daily inventory synchronization involves data transformation (TankScan JSON to SAP IDoc format) and error handling. A middleware platform like MuleSoft or Dell Boomi excels here because it can: transform data formats, handle retries on failures, log transactions for audit, and manage the SAP-specific protocols (BAPI, RFC). Simple API polling on a daily schedule could also work for simpler implementations.

        **(c) Quarterly consumption analytics -- Data Lake**
        Analytics on three months of data across hundreds of tanks requires a data lake approach. TankScan data should be exported (via API or batch export) into a data lake (S3, Azure Blob, BigQuery), where it can be joined with other data sources and processed using analytics tools (Spark, Tableau, Python). The data lake provides the storage capacity and query performance needed for large-scale historical analysis.

!!! question "Question 5 -- Evaluation (Evaluate)"
    A developer proposes embedding the TankScan API key directly in a React frontend application's JavaScript code, arguing that "it's only a read-only key and the data isn't that sensitive." Evaluate this approach and recommend a secure alternative.

    ??? success "Answer"
        This approach is **fundamentally insecure** and should be rejected, even for a read-only key:

        1. **API key exposure**: Any JavaScript code sent to a browser is visible to users via browser developer tools. The API key would be trivially extractable.
        2. **Data sensitivity**: Tank level data reveals customer inventory levels, consumption patterns, delivery schedules, and site locations. Competitors, thieves, or bad actors could exploit this information.
        3. **Abuse potential**: Even a read-only key, once exposed, can be used to poll the API at high rates, potentially exhausting rate limits and disrupting legitimate operations.
        4. **Key rotation burden**: If the key is compromised, every deployed instance of the frontend must be updated simultaneously.
        5. **Compliance risk**: Many regulatory frameworks (SOC 2, ISO 27001) explicitly prohibit embedding credentials in client-side code.

        **Secure alternative:** Implement a **Backend-for-Frontend (BFF)** pattern:
        - The React app authenticates users through your own authentication system (e.g., OAuth2)
        - Authenticated requests go to your backend server (Node.js, Python, etc.)
        - Your backend server holds the TankScan API key securely (in environment variables or a secrets manager)
        - Your backend makes API calls to TankScan on behalf of the user, returning only the data that user is authorized to see
        - This also enables you to implement additional authorization logic (e.g., customer A can only see their own tanks)
