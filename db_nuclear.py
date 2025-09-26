"""
Nuclear Database Adapter - Direct PostgreSQL
Bypasses Supabase client to avoid dependency hell
"""
import os
import asyncpg
import psycopg2
from typing import Dict, List, Any, Optional
import json
from urllib.parse import urlparse

class NuclearDB:
    """Direct PostgreSQL connection to Supabase database"""
    
    def __init__(self):
        # Parse Supabase URL to get PostgreSQL connection details
        supabase_url = os.environ.get('SUPABASE_URL')
        if not supabase_url:
            raise ValueError("SUPABASE_URL environment variable not set")
            
        # Convert Supabase URL to PostgreSQL connection string
        # Supabase URL format: https://abc.supabase.co
        # PostgreSQL format: postgresql://postgres:password@db.abc.supabase.co:5432/postgres
        
        parsed = urlparse(supabase_url)
        host = parsed.hostname.replace('.supabase.co', '') if parsed.hostname else ''
        
        self.db_config = {
            'host': f'db.{host}.supabase.co',
            'port': 5432,
            'database': 'postgres',
            'user': 'postgres',
            'password': os.environ.get('SUPABASE_SERVICE_ROLE_KEY', '')
        }
        
        print(f"🔥 NUCLEAR DB: Connecting to {self.db_config['host']}")
    
    async def get_async_connection(self):
        """Get async PostgreSQL connection"""
        return await asyncpg.connect(
            host=self.db_config['host'],
            port=self.db_config['port'],
            user=self.db_config['user'],
            password=self.db_config['password'],
            database=self.db_config['database']
        )
    
    def get_sync_connection(self):
        """Get sync PostgreSQL connection"""
        return psycopg2.connect(
            host=self.db_config['host'],
            port=self.db_config['port'],
            user=self.db_config['user'],
            password=self.db_config['password'],
            database=self.db_config['database']
        )
    
    async def execute_query(self, query: str, params: tuple = None) -> List[Dict]:
        """Execute SELECT query and return results"""
        conn = await self.get_async_connection()
        try:
            if params:
                rows = await conn.fetch(query, *params)
            else:
                rows = await conn.fetch(query)
            
            # Convert to list of dicts
            return [dict(row) for row in rows]
        finally:
            await conn.close()
    
    async def execute_mutation(self, query: str, params: tuple = None) -> str:
        """Execute INSERT/UPDATE/DELETE and return status"""
        conn = await self.get_async_connection()
        try:
            if params:
                result = await conn.execute(query, *params)
            else:
                result = await conn.execute(query)
            return result
        finally:
            await conn.close()
    
    # Common table operations
    async def get_users(self) -> List[Dict]:
        """Get all users"""
        return await self.execute_query("SELECT * FROM users ORDER BY created_at DESC")
    
    async def get_user_by_id(self, user_id: str) -> Optional[Dict]:
        """Get user by ID"""
        results = await self.execute_query("SELECT * FROM users WHERE id = $1", (user_id,))
        return results[0] if results else None
    
    async def create_user(self, user_data: Dict) -> str:
        """Create new user"""
        query = """
        INSERT INTO users (email, full_name, company_name, phone_number)
        VALUES ($1, $2, $3, $4)
        RETURNING id
        """
        conn = await self.get_async_connection()
        try:
            user_id = await conn.fetchval(
                query,
                user_data.get('email'),
                user_data.get('full_name'),
                user_data.get('company_name'),
                user_data.get('phone_number')
            )
            return str(user_id)
        finally:
            await conn.close()
    
    async def test_connection(self) -> bool:
        """Test database connection"""
        try:
            conn = await self.get_async_connection()
            await conn.fetchval("SELECT 1")
            await conn.close()
            print("✅ NUCLEAR DB: Connection successful")
            return True
        except Exception as e:
            print(f"❌ NUCLEAR DB: Connection failed - {e}")
            return False

# Global instance
nuclear_db = NuclearDB()
