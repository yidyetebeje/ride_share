### **README.md**

# Analytics and Reporting Service

This project implements **Analytics** and **Reports** services for a ride-sharing application. It provides endpoints for analytics (ride volumes, user stats, and driver stats) and reporting (summaries and exports). The system uses dynamically generated dummy data for testing and prototyping.

---

## **API Endpoints**

### **1. Analytics Service**

#### **Get Overall Analytics**

- **Endpoint**: `GET /analytics`
- **Description**: Provides overall ride-sharing analytics, including ride volume, total revenue, and user/driver stats.
- **Response Example**:
  ```json
  {
    "rideVolume": 1000,
    "revenue": 52340,
    "userStats": [{ "userId": 1, "totalRides": 12, "totalSpent": 850 }],
    "driverStats": [{ "driverId": 1, "totalRides": 15, "totalEarnings": 980 }]
  }
  ```

#### **Get Analytics for a Specific User**

- **Endpoint**: `GET /analytics/user/:id`
- **Description**: Provides stats for a specific user.
- **Path Parameter**:
  - `id` (number): User ID.
- **Response Example**:
  ```json
  {
    "userId": 1,
    "totalRides": 12,
    "totalSpent": 850
  }
  ```

#### **Get All Users' Analytics**

- **Endpoint**: `GET /analytics/user`
- **Description**: Retrieves stats for all users.
- **Response Example**:
  ```json
  [
    { "userId": 1, "totalRides": 12, "totalSpent": 850 },
    { "userId": 2, "totalRides": 9, "totalSpent": 430 }
  ]
  ```

#### **Get Analytics for a Specific Driver**

- **Endpoint**: `GET /analytics/driver/:id`
- **Description**: Provides stats for a specific driver.
- **Path Parameter**:
  - `id` (number): Driver ID.
- **Response Example**:
  ```json
  {
    "driverId": 1,
    "totalRides": 15,
    "totalEarnings": 980
  }
  ```

#### **Get All Drivers' Analytics**

- **Endpoint**: `GET /analytics/driver`
- **Description**: Retrieves stats for all drivers.
- **Response Example**:
  ```json
  [
    { "driverId": 1, "totalRides": 15, "totalEarnings": 980 },
    { "driverId": 2, "totalRides": 10, "totalEarnings": 670 }
  ]
  ```

---

### **2. Reports Service**

#### **Get Summary Report**

- **Endpoint**: `GET /reports/summary`
- **Description**: Provides a summary report of ride-sharing metrics.
- **Response Example**:
  ```json
  {
    "totalRides": 1000,
    "totalRevenue": 52340,
    "activeUsers": 250,
    "activeDrivers": 120
  }
  ```

#### **Get Date Range Report**

- **Endpoint**: `GET /reports/date-range`
- **Description**: Retrieves analytics for a specific date range.
- **Query Parameters**:
  - `start` (string): Start date in `YYYY-MM-DD` format.
  - `end` (string): End date in `YYYY-MM-DD` format.
- **Example**: `/reports/date-range?start=2024-01-01&end=2024-01-31`
- **Response Example**:
  ```json
  [
    { "date": "2024-01-01", "rides": 25, "revenue": 1250 },
    { "date": "2024-01-02", "rides": 30, "revenue": 1400 }
  ]
  ```

#### **Export Report**

- **Endpoint**: `GET /reports/export`
- **Description**: Exports reports in JSON or CSV format.
- **Query Parameters**:
  - `format` (string): Format of the export (`json` or `csv`).
  - `type` (string): Type of report (`summary` or `date-range`).
  - `start` (string, optional): Start date for date range (required if `type` is `date-range`).
  - `end` (string, optional): End date for date range (required if `type` is `date-range`).
- **Examples**:
  - `/reports/export?format=json&type=summary`
  - `/reports/export?format=json&type=date-range&start=2024-01-01&end=2024-01-31`
  - `/reports/export?format=csv&type=summary`
  - `/reports/export?format=csv&type=date-range&start=2024-01-01&end=2024-01-31`
- **Response Example (JSON)**:
  ```json
  {
    "format": "json",
    "data": [{ "date": "2024-01-01", "rides": 25, "revenue": 1250 }]
  }
  ```
- **Response Example (CSV)**:
  ```csv
  date,rides,revenue
  2024-01-01,25,1250
  2024-01-02,30,1400
  ```

---

## **Testing and Setup**

1. Install dependencies:

   ```bash
   npm install
   ```

2. Run the server:

   ```bash
   npm run start
   ```

3. Access the endpoints using:

   - Postman
   - cURL
   - Any HTTP client

4. Example cURL commands:
   - Fetch summary report:
     ```bash
     curl -X GET "http://localhost:3000/reports/summary"
     ```
   - Fetch date-range report:
     ```bash
     curl -X GET "http://localhost:3000/reports/date-range?start=2024-01-01&end=2024-01-31"
     ```
   - Export as JSON:
     ```bash
     curl -X GET "http://localhost:3000/reports/export?format=json&type=summary"
     ```
   - Export as CSV:
     ```bash
     curl -X GET "http://localhost:3000/reports/export?format=csv&type=date-range&start=2024-01-01&end=2024-01-31"
     ```

---
