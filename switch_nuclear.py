"""
Nuclear Switch Script
Modifies main.py to use direct PostgreSQL instead of Supabase client
"""
import os
import shutil

def switch_to_nuclear():
    """Switch main.py to use nuclear database adapter"""
    
    # Read current main.py
    with open('api/main.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Create backup
    shutil.copy('api/main.py', 'api/main.py.backup')
    print("✅ Backed up api/main.py")
    
    # Replace Supabase imports with nuclear DB
    modifications = [
        # Comment out Supabase import
        ('from supabase import create_client', '# from supabase import create_client  # NUCLEAR: DISABLED'),
        
        # Comment out Supabase client imports
        ('from .db_client import supabase_service_client, get_supabase_anon_client', 
         '# from .db_client import supabase_service_client, get_supabase_anon_client  # NUCLEAR: DISABLED'),
        
        # Add nuclear DB import
        ('from .config import BaseModel, get_user_id_from_token',
         'from .config import BaseModel, get_user_id_from_token\nfrom ..db_nuclear import nuclear_db  # NUCLEAR: ADDED'),
    ]
    
    for old, new in modifications:
        content = content.replace(old, new)
    
    # Write modified content
    with open('api/main.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Switched main.py to nuclear mode")

def restore_original():
    """Restore original main.py from backup"""
    if os.path.exists('api/main.py.backup'):
        shutil.copy('api/main.py.backup', 'api/main.py')
        os.remove('api/main.py.backup')
        print("✅ Restored original main.py")
    else:
        print("❌ No backup found")

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == 'restore':
        restore_original()
    else:
        switch_to_nuclear()
