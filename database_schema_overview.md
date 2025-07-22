

---

### **Application Database Schema: An Overview**

We will design a simple but powerful relational schema with three core tables. Think of them as the three pillars of your application's data.

#### **1. The `users` Table**

*   **Purpose:** This table stores all information related to a user's account. It is the central point for authentication and user identity.
*   **Key Columns:**
    *   `id` (Integer, **Primary Key**): A unique, auto-incrementing number for each user (e.g., 1, 2, 3...). This is the most efficient way to link this user to other tables.
    *   `email` (String, **Unique**): The user's email address. We'll enforce that it must be unique to prevent duplicate accounts. This will also serve as their login username.
    *   `hashed_password` (String): The user's password after it has been securely hashed. **We will never, ever store plain-text passwords.**
    *   `created_at` (Timestamp): The date and time the user account was created. This is great for analytics.
    *   `is_active` (Boolean): A flag to indicate if the account is active. Useful for implementing account deactivation features later.

**Example Row:**
| id  | email               | hashed_password                        | created_at          | is_active |
|-----|---------------------|----------------------------------------|---------------------|-----------|
| 1   | user@example.com    | `$2b$12$D...` (a long, hashed string)  | 2023-10-27 10:00:00 | true      |

---

#### **2. The `movies` Table**

*   **Purpose:** This table will be a local, fast-access copy of the essential metadata for all the movies in our system. We will populate this table once from the `movies_df.pkl` file we created. This is much more efficient than reading from a large file every time.
*   **Key Columns:**
    *   `id` (Integer, **Primary Key**): A unique, auto-incrementing internal ID for our database.
    *   `tconst` (String, **Unique**, **Indexed**): The IMDb constant (e.g., `tt15398776`). This is the "universal ID" that links back to our model and external data sources. We'll make it unique and add an index for very fast lookups.
    *   `primaryTitle` (String): The main title of the movie.
    *   `startYear` (Integer): The release year.
    *   `genres` (String): A comma-separated string of genres (e.g., "Biography,Drama,History").

**Example Row:**
| id  | tconst      | primaryTitle | startYear | genres                    |
|-----|-------------|--------------|-----------|---------------------------|
| 1   | tt15398776  | Oppenheimer  | 2023      | Biography,Drama,History   |

---

#### **3. The `interactions` Table**

*   **Purpose:** This is the most important table for our long-term goal of building a Collaborative Filtering model. It's a "log book" of every meaningful action a user takes.
*   **Key Columns:**
    *   `id` (Integer, **Primary Key**): A unique ID for the interaction event itself.
    *   `user_id` (Integer, **Foreign Key -> `users.id`**): This links the interaction directly to a specific user.
    *   `movie_id` (Integer, **Foreign Key -> `movies.id`**): This links the interaction directly to a specific movie in our database.
    *   `interaction_type` (String or Integer): The type of action taken. We can use strings like `'like'`, `'dislike'`, `'superlike'`, or integers (`1`, `-1`, `2`) for efficiency.
    *   `timestamp` (Timestamp): The exact time the interaction occurred.

**Example Rows:**
| id  | user_id | movie_id | interaction_type | timestamp           |
|-----|---------|----------|------------------|---------------------|
| 1   | 1       | 1        | 'like'           | 2023-10-27 10:05:12 |
| 2   | 1       | 23       | 'dislike'        | 2023-10-27 10:06:45 |

---

### **Visualizing the Relationships**

Here's how they all connect:

```
+-------------+      +------------------+      +-------------+
|    users    |      |   interactions   |      |   movies    |
+-------------+      +------------------+      +-------------+
| id (PK)     |----<| user_id (FK)     |      | id (PK)     |
| email       |      | movie_id (FK)    |----->| tconst      |
| hashed_pass |      | interaction_type |      | primaryTitle|
| ...         |      | timestamp        |      | ...         |
+-------------+      +------------------+      +-------------+
```

*   A **User** can have many **Interactions**.
*   A **Movie** can have many **Interactions**.
*   This creates a **many-to-many** relationship between `users` and `movies`, with the `interactions` table acting as the "join" or "through" table that connects them.

Using a UUID as your primary key is the best path forward.