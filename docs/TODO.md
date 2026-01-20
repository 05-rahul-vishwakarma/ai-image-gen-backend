# Pending Tasks

## Handlers (Business Logic) ❌

### `handlers/auth.py`

| Function | Status | Description |
|----------|--------|-------------|
| `login()` | ❌ TODO | Check if user exists, create if not, verify password, generate JWT |
| `logout()` | ❌ TODO | Invalidate session/token |
| `get_current_user()` | ❌ TODO | Fetch user from database by ID |

```python
# TODO: Implement in handlers/auth.py

async def login(data: UserLogin) -> TokenResponse:
    # 1. Check if user exists by email
    # 2. If not exists, create new user (hash password)
    # 3. If exists, verify password
    # 4. Generate JWT token
    # 5. Create session in database
    # 6. Return TokenResponse
    pass
```

---

### `handlers/generation.py`

| Function | Status | Description |
|----------|--------|-------------|
| `create_generation()` | ❌ TODO | Call AI API, save image, store in DB |
| `get_generations()` | ❌ TODO | Fetch all generations for user |
| `get_generation()` | ❌ TODO | Fetch single generation by ID |
| `delete_generation()` | ❌ TODO | Delete generation from DB |
| `clear_history()` | ❌ TODO | Delete all generations for user |

```python
# TODO: Implement in handlers/generation.py

async def create_generation(user_id: str, data: GenerationCreate) -> GenerationResponse:
    # 1. Call OpenAI DALL-E API with prompt
    # 2. Upload image to Cloudinary (optional)
    # 3. Save generation to database
    # 4. Return GenerationResponse
    pass
```

---

### `handlers/user.py`

| Function | Status | Description |
|----------|--------|-------------|
| `get_profile()` | ❌ TODO | Fetch user profile from DB |
| `update_profile()` | ❌ TODO | Update user name/avatar |

```python
# TODO: Implement in handlers/user.py

async def get_profile(user_id: str) -> UserResponse:
    # 1. Find user by ID
    # 2. Return UserResponse
    pass
```

---

## Middlewares ❌

### `middlewares/auth.py`

| Function | Status | Description |
|----------|--------|-------------|
| `get_current_user()` | ❌ TODO | Validate JWT, return user |

```python
# TODO: Implement in middlewares/auth.py

async def get_current_user(credentials) -> User:
    # 1. Extract token from Authorization header
    # 2. Decode JWT token
    # 3. Validate token (expiry, signature)
    # 4. Find user in database
    # 5. Return user or raise 401 error
    pass
```

---

## Utilities to Create ❌

| File | Status | Description |
|------|--------|-------------|
| `utils/security.py` | ❌ TODO | Password hashing, JWT encode/decode |
| `utils/openai.py` | ❌ TODO | OpenAI API client wrapper |
| `utils/cloudinary.py` | ❌ TODO | Image upload helper (optional) |

---

## Priority Order

1. **HIGH** - `utils/security.py` (needed for auth)
2. **HIGH** - `middlewares/auth.py` (needed for protected routes)
3. **HIGH** - `handlers/auth.py` (login/register)
4. **MEDIUM** - `handlers/generation.py` (core feature)
5. **LOW** - `handlers/user.py` (profile)
6. **LOW** - `utils/cloudinary.py` (optional)
