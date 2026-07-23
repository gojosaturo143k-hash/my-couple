import sqlite3
import logging

logger = logging.getLogger(__name__)

DB_NAME = "bot_database.db"

def get_connection():
    """Create and return a database connection."""
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA journal_mode=WAL")
    return conn

def init_db():
    """Initialize the database and create the members table if it doesn't exist."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS members (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                username TEXT,
                first_name TEXT,
                UNIQUE(chat_id, user_id)
            )
        """)
        conn.commit()
        logger.info("Database initialized successfully.")
    except sqlite3.Error as e:
        logger.error(f"Error initializing database: {e}")
    finally:
        conn.close()

def save_user(chat_id: int, user_id: int, username: str | None, first_name: str | None):
    """Save or update a user in the database."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO members (chat_id, user_id, username, first_name)
            VALUES (?, ?, ?, ?)
        """, (chat_id, user_id, username, first_name))
        conn.commit()
    except sqlite3.Error as e:
        logger.error(f"Error saving user {user_id}: {e}")
    finally:
        conn.close()

def get_user_by_id(chat_id: int, target_user_id: int) -> dict | None:
    """Get a specific user by their ID (Used for VIP/Fixed users)."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT user_id, username, first_name FROM members 
            WHERE chat_id = ? AND user_id = ? 
        """, (chat_id, target_user_id))
        row = cursor.fetchone()
        if row:
            return {"user_id": row[0], "username": row[1], "first_name": row[2]}
        return None
    except sqlite3.Error as e:
        logger.error(f"Error fetching user by ID: {e}")
        return None
    finally:
        conn.close()

def get_random_user(chat_id: int, exclude_user_id: int | None = None) -> dict | None:
    """Get a single random user from a specific chat, optionally excluding one user_id."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        if exclude_user_id:
            cursor.execute("""
                SELECT user_id, username, first_name FROM members 
                WHERE chat_id = ? AND user_id != ? 
                ORDER BY RANDOM() LIMIT 1
            """, (chat_id, exclude_user_id))
        else:
            cursor.execute("""
                SELECT user_id, username, first_name FROM members 
                WHERE chat_id = ? 
                ORDER BY RANDOM() LIMIT 1
            """, (chat_id,))
            
        row = cursor.fetchone()
        if row:
            return {"user_id": row[0], "username": row[1], "first_name": row[2]}
        return None
    except sqlite3.Error as e:
        logger.error(f"Error fetching random user: {e}")
        return None
    finally:
        conn.close()

def get_random_couple(chat_id: int, exclude_user_id: int | None = None) -> list[dict] | None:
    """Get two different random users from a specific chat."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        limit = 3 if exclude_user_id else 2
        
        if exclude_user_id:
            cursor.execute("""
                SELECT user_id, username, first_name FROM members 
                WHERE chat_id = ? AND user_id != ? 
                ORDER BY RANDOM() LIMIT ?
            """, (chat_id, exclude_user_id, limit))
        else:
            cursor.execute("""
                SELECT user_id, username, first_name FROM members 
                WHERE chat_id = ? 
                ORDER BY RANDOM() LIMIT ?
            """, (chat_id, limit))
            
        rows = cursor.fetchall()
        
        unique_users = []
        seen_ids = set()
        for row in rows:
            if row[0] not in seen_ids:
                unique_users.append({"user_id": row[0], "username": row[1], "first_name": row[2]})
                seen_ids.add(row[0])
                
        if len(unique_users) >= 2:
            return [unique_users[0], unique_users[1]]
        return None
    except sqlite3.Error as e:
        logger.error(f"Error fetching random couple: {e}")
        return None
    finally:
        conn.close()

def get_member_count(chat_id: int) -> int:
    """Return the total number of saved members in a chat."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM members WHERE chat_id = ?", (chat_id,))
        count = cursor.fetchone()[0]
        return count
    except sqlite3.Error as e:
        logger.error(f"Error getting member count: {e}")
        return 0
    finally:
        conn.close()
