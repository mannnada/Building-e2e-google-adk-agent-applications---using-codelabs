# Example Output - Advanced Tool Agent

This document shows real examples of what the agent produces for different types of requests.

## Example 1: REST API Generation

### Input
```
Generate a Python REST API with authentication using FastAPI
```

### Output
```
✅ Code Generated Successfully

Language: python
Complexity: medium

Generated Code:
```python
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import Optional
import jwt
from datetime import datetime, timedelta

app = FastAPI(title="Authenticated API")
security = HTTPBearer()

# Secret key for JWT (use environment variable in production)
SECRET_KEY = "your-secret-key-here"
ALGORITHM = "HS256"

# Models
class User(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class UserResponse(BaseModel):
    username: str
    message: str

# Mock user database
users_db = {
    "admin": "password123"
}

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verify JWT token"""
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials"
            )
        return username
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )

@app.post("/login", response_model=Token)
async def login(user: User):
    """Login endpoint - returns JWT token"""
    if user.username not in users_db or users_db[user.username] != user.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=timedelta(hours=1)
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/protected", response_model=UserResponse)
async def protected_route(username: str = Depends(verify_token)):
    """Protected endpoint - requires valid JWT token"""
    return {
        "username": username,
        "message": f"Hello {username}! This is a protected route."
    }

@app.get("/")
async def root():
    """Public endpoint"""
    return {"message": "Welcome to the Authenticated API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```
```

---

## Example 2: Security Analysis

### Input
```
Analyze this code for security vulnerabilities:

import os
import pickle

def process_user_input(user_data):
    # Dangerous: using eval
    result = eval(user_data)
    
    # Dangerous: command injection
    os.system(f"echo {user_data}")
    
    # Dangerous: insecure deserialization
    data = pickle.loads(user_data)
    
    return result
```

### Output
```
✅ Code Analysis Complete

Analysis Type: security

Results:
{
  "severity": "high",
  "vulnerabilities": [
    {
      "type": "Arbitrary Code Execution",
      "line": "7",
      "description": "Use of eval() allows execution of arbitrary Python code from user input. This is extremely dangerous and can lead to complete system compromise.",
      "recommendation": "Never use eval() with user input. Use ast.literal_eval() for safe evaluation of literals, or implement proper parsing logic."
    },
    {
      "type": "Command Injection",
      "line": "10",
      "description": "Direct use of user input in os.system() allows command injection. An attacker could execute arbitrary system commands.",
      "recommendation": "Use subprocess.run() with a list of arguments instead of shell commands. Never interpolate user input directly into shell commands."
    },
    {
      "type": "Insecure Deserialization",
      "line": "13",
      "description": "pickle.loads() with user input can execute arbitrary code during deserialization. This is a critical vulnerability.",
      "recommendation": "Use JSON for data serialization instead of pickle. If pickle is necessary, implement signature verification and only deserialize trusted data."
    }
  ],
  "summary": "This code contains three critical security vulnerabilities that could lead to complete system compromise. All three issues involve executing or deserializing untrusted user input. Immediate remediation is required before deploying this code."
}
```

---

## Example 3: Combined Workflow (Generate + Analyze)

### Input
```
Generate a Python data processing script and analyze it for performance
```

### Output
```
============================================================
🤖 ADVANCED TOOL AGENT - COMPLETE WORKFLOW
============================================================

📝 STEP 1: CODE GENERATION
------------------------------------------------------------
✅ Successfully generated python code

```python
import pandas as pd
from typing import List, Dict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataProcessor:
    """
    A data processing class that handles CSV file operations
    with error handling and logging.
    """
    
    def __init__(self, file_path: str):
        """
        Initialize the data processor.
        
        Args:
            file_path: Path to the CSV file to process
        """
        self.file_path = file_path
        self.data = None
    
    def load_data(self) -> bool:
        """
        Load data from CSV file.
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            logger.info(f"Loading data from {self.file_path}")
            self.data = pd.read_csv(self.file_path)
            logger.info(f"Successfully loaded {len(self.data)} rows")
            return True
        except FileNotFoundError:
            logger.error(f"File not found: {self.file_path}")
            return False
        except pd.errors.EmptyDataError:
            logger.error("CSV file is empty")
            return False
        except Exception as e:
            logger.error(f"Error loading data: {str(e)}")
            return False
    
    def clean_data(self) -> None:
        """Remove null values and duplicates."""
        if self.data is None:
            logger.warning("No data loaded")
            return
        
        initial_rows = len(self.data)
        
        # Remove null values
        self.data = self.data.dropna()
        
        # Remove duplicates
        self.data = self.data.drop_duplicates()
        
        final_rows = len(self.data)
        logger.info(f"Cleaned data: {initial_rows} → {final_rows} rows")
    
    def filter_data(self, column: str, value: any) -> pd.DataFrame:
        """
        Filter data by column value.
        
        Args:
            column: Column name to filter on
            value: Value to filter for
            
        Returns:
            Filtered DataFrame
        """
        if self.data is None:
            logger.warning("No data loaded")
            return pd.DataFrame()
        
        if column not in self.data.columns:
            logger.error(f"Column '{column}' not found")
            return pd.DataFrame()
        
        filtered = self.data[self.data[column] == value]
        logger.info(f"Filtered to {len(filtered)} rows")
        return filtered
    
    def aggregate_data(self, group_by: str, agg_column: str, 
                      agg_func: str = 'sum') -> Dict:
        """
        Aggregate data by grouping.
        
        Args:
            group_by: Column to group by
            agg_column: Column to aggregate
            agg_func: Aggregation function (sum, mean, count)
            
        Returns:
            Dictionary of aggregated results
        """
        if self.data is None:
            logger.warning("No data loaded")
            return {}
        
        try:
            grouped = self.data.groupby(group_by)[agg_column].agg(agg_func)
            result = grouped.to_dict()
            logger.info(f"Aggregated {len(result)} groups")
            return result
        except KeyError as e:
            logger.error(f"Column not found: {str(e)}")
            return {}
        except Exception as e:
            logger.error(f"Aggregation error: {str(e)}")
            return {}
    
    def save_data(self, output_path: str) -> bool:
        """
        Save processed data to CSV.
        
        Args:
            output_path: Path to save the file
            
        Returns:
            bool: True if successful, False otherwise
        """
        if self.data is None:
            logger.warning("No data to save")
            return False
        
        try:
            self.data.to_csv(output_path, index=False)
            logger.info(f"Data saved to {output_path}")
            return True
        except Exception as e:
            logger.error(f"Error saving data: {str(e)}")
            return False

# Example usage
if __name__ == "__main__":
    processor = DataProcessor("input_data.csv")
    
    if processor.load_data():
        processor.clean_data()
        filtered = processor.filter_data("status", "active")
        aggregated = processor.aggregate_data("category", "amount", "sum")
        processor.save_data("output_data.csv")
        
        print("Data processing complete!")
        print(f"Aggregated results: {aggregated}")
```

🔍 STEP 2: CODE ANALYSIS
------------------------------------------------------------
✅ Analysis complete (performance)

{
  "performance_score": "7",
  "issues": [
    {
      "type": "Potential Memory Issue",
      "line": "Multiple operations",
      "description": "The code loads the entire CSV file into memory using pandas. For very large files, this could cause memory issues.",
      "recommendation": "Consider using chunked reading with pd.read_csv(chunksize=...) for large files, or use dask for out-of-core processing."
    },
    {
      "type": "Inefficient Filtering",
      "line": "78",
      "description": "The filter_data method creates a new DataFrame copy. Multiple filters could be inefficient.",
      "recommendation": "Consider chaining filters or using query() method for better performance: df.query('column == value')"
    },
    {
      "type": "Logging Overhead",
      "line": "Throughout",
      "description": "Logging on every operation could add overhead for high-frequency processing.",
      "recommendation": "Consider using logging levels appropriately and reducing log frequency for production use."
    }
  ],
  "summary": "Overall performance is good (7/10). The code uses pandas efficiently for most operations. Main concerns are memory usage for large files and potential overhead from excessive logging. The code is well-structured and maintainable. For production use with large datasets, consider implementing chunked processing and optimizing the logging strategy."
}

============================================================
```

---

## Example 4: JavaScript API Generation

### Input
```
Create a Node.js Express API with user registration and login endpoints
```

### Output
```
✅ Code Generated Successfully

Language: javascript
Complexity: medium

Generated Code:
```javascript
const express = require('express');
const bcrypt = require('bcrypt');
const jwt = require('jsonwebtoken');
const { body, validationResult } = require('express-validator');

const app = express();
const PORT = process.env.PORT || 3000;
const JWT_SECRET = process.env.JWT_SECRET || 'your-secret-key';

// Middleware
app.use(express.json());

// In-memory user storage (use database in production)
const users = [];

/**
 * Middleware to verify JWT token
 */
const authenticateToken = (req, res, next) => {
    const authHeader = req.headers['authorization'];
    const token = authHeader && authHeader.split(' ')[1];

    if (!token) {
        return res.status(401).json({ error: 'Access token required' });
    }

    jwt.verify(token, JWT_SECRET, (err, user) => {
        if (err) {
            return res.status(403).json({ error: 'Invalid or expired token' });
        }
        req.user = user;
        next();
    });
};

/**
 * POST /register - Register a new user
 */
app.post('/register',
    // Validation middleware
    body('email').isEmail().normalizeEmail(),
    body('password').isLength({ min: 6 }),
    body('username').isLength({ min: 3 }).trim(),
    async (req, res) => {
        try {
            // Check validation errors
            const errors = validationResult(req);
            if (!errors.isEmpty()) {
                return res.status(400).json({ errors: errors.array() });
            }

            const { email, password, username } = req.body;

            // Check if user already exists
            const existingUser = users.find(u => u.email === email);
            if (existingUser) {
                return res.status(409).json({ error: 'User already exists' });
            }

            // Hash password
            const saltRounds = 10;
            const hashedPassword = await bcrypt.hash(password, saltRounds);

            // Create user
            const user = {
                id: users.length + 1,
                email,
                username,
                password: hashedPassword,
                createdAt: new Date()
            };

            users.push(user);

            // Return user without password
            const { password: _, ...userWithoutPassword } = user;
            res.status(201).json({
                message: 'User registered successfully',
                user: userWithoutPassword
            });

        } catch (error) {
            console.error('Registration error:', error);
            res.status(500).json({ error: 'Internal server error' });
        }
    }
);

/**
 * POST /login - Authenticate user and return JWT
 */
app.post('/login',
    body('email').isEmail().normalizeEmail(),
    body('password').notEmpty(),
    async (req, res) => {
        try {
            // Check validation errors
            const errors = validationResult(req);
            if (!errors.isEmpty()) {
                return res.status(400).json({ errors: errors.array() });
            }

            const { email, password } = req.body;

            // Find user
            const user = users.find(u => u.email === email);
            if (!user) {
                return res.status(401).json({ error: 'Invalid credentials' });
            }

            // Verify password
            const isValidPassword = await bcrypt.compare(password, user.password);
            if (!isValidPassword) {
                return res.status(401).json({ error: 'Invalid credentials' });
            }

            // Generate JWT
            const token = jwt.sign(
                { id: user.id, email: user.email },
                JWT_SECRET,
                { expiresIn: '24h' }
            );

            res.json({
                message: 'Login successful',
                token,
                user: {
                    id: user.id,
                    email: user.email,
                    username: user.username
                }
            });

        } catch (error) {
            console.error('Login error:', error);
            res.status(500).json({ error: 'Internal server error' });
        }
    }
);

/**
 * GET /profile - Get user profile (protected route)
 */
app.get('/profile', authenticateToken, (req, res) => {
    const user = users.find(u => u.id === req.user.id);
    if (!user) {
        return res.status(404).json({ error: 'User not found' });
    }

    const { password: _, ...userWithoutPassword } = user;
    res.json({ user: userWithoutPassword });
});

/**
 * GET / - Health check
 */
app.get('/', (req, res) => {
    res.json({ message: 'API is running', version: '1.0.0' });
});

// Error handling middleware
app.use((err, req, res, next) => {
    console.error(err.stack);
    res.status(500).json({ error: 'Something went wrong!' });
});

// Start server
app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});

module.exports = app;
```
```

---

## Example 5: Style Analysis

### Input
```
Analyze this code for style and best practices:

def calc(x,y,op):
    if op=="add":
        return x+y
    elif op=="sub":
        return x-y
    else:
        return None
```

### Output
```
✅ Code Analysis Complete

Analysis Type: style

Results:
{
  "style_score": "4",
  "issues": [
    {
      "type": "Naming Convention",
      "line": "1",
      "description": "Function name 'calc' is too abbreviated. Python style guide (PEP 8) recommends descriptive names.",
      "recommendation": "Rename to 'calculate' or 'perform_calculation' for better clarity."
    },
    {
      "type": "Missing Whitespace",
      "line": "1",
      "description": "Missing spaces around parameters and operators. PEP 8 requires spaces after commas.",
      "recommendation": "Change 'calc(x,y,op)' to 'calc(x, y, op)' and add spaces around operators."
    },
    {
      "type": "Missing Documentation",
      "line": "1",
      "description": "Function lacks a docstring explaining its purpose, parameters, and return value.",
      "recommendation": "Add a docstring: '''Perform arithmetic operation on two numbers.'''"
    },
    {
      "type": "String Comparison",
      "line": "2-4",
      "description": "Using string literals for operation type is error-prone. Consider using an enum or constants.",
      "recommendation": "Define constants: ADD = 'add', SUB = 'sub', or use an Enum class."
    },
    {
      "type": "Limited Functionality",
      "line": "6",
      "description": "Function only supports two operations. Consider making it more extensible.",
      "recommendation": "Use a dictionary mapping operations to functions, or implement a strategy pattern."
    },
    {
      "type": "Return Type Inconsistency",
      "line": "6",
      "description": "Function returns None for invalid operations, which could cause errors. Should raise an exception or return a default value.",
      "recommendation": "Raise ValueError('Invalid operation') for unsupported operations."
    }
  ],
  "summary": "Code has significant style issues (4/10). Main problems are poor naming, missing documentation, lack of whitespace, and inconsistent return types. The code works but doesn't follow Python best practices. Refactoring recommended for production use."
}
```

---

## Interactive Mode Example Session

```
============================================================
🤖 ADVANCED TOOL AGENT - Interactive Mode
============================================================

Capabilities:
  • Generate code (REST APIs, scripts, pipelines)
  • Analyze code (security, performance, style)
  • Combined workflows (generate + analyze)

Examples:
  - 'Generate a Python REST API with authentication'
  - 'Analyze this code for security issues: <code>'
  - 'Create and analyze a data pipeline in Python'

Type 'quit' or 'exit' to stop

============================================================

💬 You: Generate a simple Python function to validate email addresses

🤖 Processing your request...

✅ Code Generated Successfully

Language: python
Complexity: simple

Generated Code:
```python
import re

def validate_email(email: str) -> bool:
    """
    Validate email address format.
    
    Args:
        email: Email address string to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    # Email regex pattern
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if not email or not isinstance(email, str):
        return False
    
    return bool(re.match(pattern, email))

# Example usage
if __name__ == "__main__":
    test_emails = [
        "user@example.com",
        "invalid.email",
        "test@domain.co.uk",
        "@invalid.com"
    ]
    
    for email in test_emails:
        result = validate_email(email)
        print(f"{email}: {'Valid' if result else 'Invalid'}")
```

------------------------------------------------------------

💬 You: quit

👋 Goodbye!
```

---

These examples demonstrate the agent's capabilities across different scenarios and show the quality and format of outputs users can expect.
