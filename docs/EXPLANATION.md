# Project Structure Explanation

> For Node.js developers

---

## Folder Structure

```
python_project/
│
├── app/
│   ├── main.py              # Entry point (like index.js)
│   │
│   ├── models/              # Database schemas (like Mongoose models)
│   │   ├── user.py
│   │   ├── generation.py
│   │   └── session.py
│   │
│   ├── schemas/             # Request/Response validation (like Zod/Joi)
│   │   ├── user.py
│   │   ├── generation.py
│   │   └── auth.py
│   │
│   ├── routers/             # Route definitions (like Express routes)
│   │   ├── auth.py
│   │   ├── generation.py
│   │   └── user.py
│   │
│   ├── handlers/            # Business logic (like controllers)
│   │   ├── auth.py
│   │   ├── generation.py
│   │   └── user.py
│   │
│   ├── middlewares/         # Auth middleware (like Express middleware)
│   │   └── auth.py
│   │
│   └── core/                # Config & database
│       ├── config.py
│       └── database.py
│
├── docs/                    # Documentation
├── requirements.txt         # Dependencies (like package.json)
├── .env.example
└── .gitignore
```

---

## Node.js vs Python Mapping

### File Mapping

| Python (FastAPI) | Node.js (Express) |
|------------------|-------------------|
| `main.py` | `app.js` / `index.js` |
| `models/user.py` | `models/User.js` (Mongoose) |
| `schemas/user.py` | `validators/user.js` (Joi/Zod) |
| `routers/auth.py` | `routes/auth.js` |
| `handlers/auth.py` | `controllers/authController.js` |
| `middlewares/auth.py` | `middlewares/auth.js` |
| `core/config.py` | `config/index.js` |
| `core/database.py` | `config/db.js` |

### Package Mapping

| Python | Node.js | Purpose |
|--------|---------|---------|
| `fastapi` | `express` | Web framework |
| `uvicorn` | `nodemon` | Dev server |
| `beanie` | `mongoose` | MongoDB ODM |
| `motor` | `mongodb` | MongoDB driver |
| `pydantic` | `zod` / `joi` | Validation |
| `python-jose` | `jsonwebtoken` | JWT |
| `passlib` | `bcrypt` | Password hashing |

---

## How Each Layer Works

### 1. Models (Database Layer)

```
Node.js (Mongoose)                    Python (Beanie)
─────────────────                     ────────────────

const userSchema = new Schema({       class User(Document):
  email: String,                          email: EmailStr
  password: String,                       password: str
  name: String,                           name: str
});
                                          class Settings:
module.exports = mongoose.model(              name = "users"
  'User', userSchema
);
```

**What it does:** Defines the shape of data stored in MongoDB.

---

### 2. Schemas (Validation Layer)

```
Node.js (Zod)                         Python (Pydantic)
─────────────                         ─────────────────

const userSchema = z.object({         class UserCreate(BaseModel):
  email: z.string().email(),              email: EmailStr
  password: z.string().min(6),            password: str
  name: z.string(),                       name: str
});
```

**What it does:** Validates incoming request data before processing.

---

### 3. Routers (Route Layer)

```
Node.js (Express)                     Python (FastAPI)
─────────────────                     ────────────────

router.post('/login',                 @router.post("/login")
  async (req, res) => {               async def login(data: UserLogin):
    const result = await                  return await auth_handler.login(data)
      authController.login(req.body);
    res.json(result);
  }
);
```

**What it does:** Maps HTTP endpoints to handler functions.

---

### 4. Handlers (Business Logic Layer)

```
Node.js (Controller)                  Python (Handler)
────────────────────                  ─────────────────

exports.login = async (data) => {     async def login(data: UserLogin):
  // Find user                            # Find user
  // Verify password                      # Verify password
  // Generate token                       # Generate token
  // Return response                      # Return response
};
```

**What it does:** Contains the actual business logic.

---

### 5. Middlewares (Auth Layer)

```
Node.js                               Python
───────                               ──────

const auth = async (req, res, next)   async def get_current_user(
  => {                                    credentials
  const token = req.headers.auth;     ) -> User:
  const user = jwt.verify(token);         token = credentials.credentials
  req.user = user;                        user = decode_jwt(token)
  next();                                 return user
};
```

**What it does:** Validates JWT token and attaches user to request.

---

## Request Flow

```
                    ┌─────────────┐
                    │   Request   │
                    └──────┬──────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────────┐
│                      main.py (FastAPI App)                    │
│                                                              │
│   1. CORS Middleware                                         │
│   2. Route matching                                          │
└──────────────────────────┬───────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────────┐
│                    routers/auth.py                           │
│                                                              │
│   @router.post("/login")                                     │
│   async def login(data: UserLogin):  ◄── Schema validates    │
│       return await auth_handler.login(data)                  │
└──────────────────────────┬───────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────────┐
│                    handlers/auth.py                          │
│                                                              │
│   async def login(data):                                     │
│       user = await User.find_one(...)  ◄── Model query       │
│       token = create_jwt(...)                                │
│       return TokenResponse(...)        ◄── Schema response   │
└──────────────────────────┬───────────────────────────────────┘
                           │
                           ▼
                    ┌─────────────┐
                    │  Response   │
                    └─────────────┘
```

---

## Protected Route Flow

```
Request with Authorization: Bearer <token>
                           │
                           ▼
┌──────────────────────────────────────────────────────────────┐
│                  routers/generation.py                        │
│                                                              │
│   @router.get("/")                                           │
│   async def get_generations(                                 │
│       current_user: User = Depends(get_current_user)  ◄──┐   │
│   ):                                                      │   │
│       return await handler.get_generations(...)           │   │
└───────────────────────────────────────────────────────────┼───┘
                                                            │
                    ┌───────────────────────────────────────┘
                    │
                    ▼
┌──────────────────────────────────────────────────────────────┐
│                  middlewares/auth.py                          │
│                                                              │
│   async def get_current_user(credentials):                   │
│       token = credentials.credentials                        │
│       payload = decode_jwt(token)    ◄── Validate token      │
│       user = await User.get(payload["sub"])                  │
│       return user                    ◄── Return to route     │
└──────────────────────────────────────────────────────────────┘
```

---

## Key Differences from Node.js

| Concept | Node.js | Python |
|---------|---------|--------|
| **Async** | `async/await` | `async/await` (same) |
| **Exports** | `module.exports` | `from x import y` |
| **Package folder** | - | `__init__.py` required |
| **Type checking** | Optional (TypeScript) | Built-in (type hints) |
| **Validation** | Manual or Zod/Joi | Automatic with Pydantic |
| **API Docs** | Manual (Swagger) | Auto-generated at `/docs` |
| **Dependency injection** | Manual | `Depends()` function |

---

## Commands Comparison

| Task | Node.js | Python |
|------|---------|--------|
| Create venv | - | `python -m venv venv` |
| Activate venv | - | `source venv/bin/activate` |
| Install deps | `npm install` | `pip install -r requirements.txt` |
| Run dev | `npm run dev` | `uvicorn app.main:app --reload` |
| Run tests | `npm test` | `pytest` |

---

## Quick Start

```bash
# 1. Create virtual environment
python -m venv venv

# 2. Activate it
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Copy environment file
cp .env.example .env

# 5. Edit .env with your values
# - MONGODB_URI
# - JWT_SECRET
# - OPENAI_API_KEY

# 6. Run the server
uvicorn app.main:app --reload

# 7. Open API docs
# http://localhost:8000/docs
```
