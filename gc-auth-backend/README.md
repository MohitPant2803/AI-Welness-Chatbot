# Authentication API Documentation

## Endpoints

### 1. User Signup
**Endpoint:** `POST /api/v1/emp/auth/signup`

**Description:** Creates a new user account.

**Request Body:**
```json
{
  "empid": "EMP12345",
  "password": "securepassword"
}
```

**Response:**
- **201 Created**
- **400 Bad Request** (User already exists)
- **500 Internal Server Error**

---

### 2. User Sign-in
**Endpoint:** `POST /api/v1/emp/auth/signin`

**Description:** Authenticates a user and provides a JWT token.

**Request Body:**
```json
{
  "empid": "EMP12345",
  "password": "securepassword"
}
```

**Response:**
- **200 OK** (Successful login)
- **401 Unauthorized** (User does not exist)
- **403 Forbidden** (Invalid password)
- **500 Internal Server Error**

---
---

<br/>
<br/>

---
---

# User Profile API Documentation

## Endpoints

### 1. Get User Details
**Endpoint:** `GET /api/v1/emp/details/user`

**Description:** Retrieves details of the authenticated user.

**Headers:**
```
Authorization: Bearer <JWT_TOKEN>
```

**Response:**
- **200 OK** (User details retrieved successfully)
  
- **401 Unauthorized** (Invalid or missing token)
- **404 Not Found** (User does not exist)
- **500 Internal Server Error**

**Errors:** (Token is invalid: expired and Token is invalid: invalid)
---
---

<br/>
<br/>

---
---

# Admin Authentication API

## Endpoints

### 1. Admin Signup
**Endpoint:** `POST /api/v1/admin/auth/signup`

**Description:** Creates a new admin account.

**Request Body:**
```json
{
  "adminid": "ADM1234",
  "password": "securepassword"
}
```

**Response:**
- **201 Created**
- **400 Bad Request** (User already exists)
- **500 Internal Server Error**

---

### 2. Admin Sign-in
**Endpoint:** `POST /api/v1/admin/auth/signin`

**Description:** Authenticates an admin and provides a JWT token.

**Request Body:**
```json
{
  "adminid": "ADM1234",
  "password": "securepassword"
}
```

**Response:**
- **200 OK** (Successful login)
- **401 Unauthorized** (User does not exist)
- **403 Forbidden** (Invalid password)
- **500 Internal Server Error**
---
---
<br/>
<br/>

---
---

# Admin Dashboard API

### Routes

#### **Get AdminDB Details**
`GET /api/v1/admin/details/db`

- **Description**: Fetches admin database details.
- **Headers:**
```
Authorization: Bearer <JWT_TOKEN>
```
- **Responses**:
  - `200 OK`: Returns database details.
  - `404 Not Found`: Data not found.

#### **Get All Users in AdminDB**
`GET /api/v1/admin/details/db/all`

- **Description**: Fetches all user records in AdminDB.
- **Headers:**
```
Authorization: Bearer <JWT_TOKEN>
```
- **Responses**:
  - `200 OK`: Returns list of all users.
  - `404 Not Found`: Data not found.

#### **Get Specific Employee Data**
`GET /api/v1/admin/details/db/emp/{empid}`

- **Description**: Fetches specific employee data using `empid`.
- **Headers:**
```
Authorization: Bearer <JWT_TOKEN>
```
- **Path Parameters**:
  - `empid`: Employee ID (String)
- **Responses**:
  - `200 OK`: Returns employee details.
  - `404 Not Found`: Employee not found.

---