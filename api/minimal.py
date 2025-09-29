"""
ABSOLUTE MINIMAL TEST - No external dependencies
Tests if basic Python function works on Vercel
"""

def handler(event, context):
    """Pure Python handler - no FastAPI, no Mangum, no imports"""
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
        },
        'body': '{"message": "✅ Pure Python handler working!", "test": "minimal"}'
    }
