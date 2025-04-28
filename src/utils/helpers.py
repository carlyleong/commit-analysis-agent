"""
Helper functions for consistent dictionary/object access.
"""

def safe_get(obj, key, default=None):
    """
    Safely get a value from either a dictionary or object.
    
    Args:
        obj: Dictionary or object to get value from
        key: Key or attribute name
        default: Default value if not found
    
    Returns:
        Value from dict/object or default
    """
    if isinstance(obj, dict):
        return obj.get(key, default)
    else:
        return getattr(obj, key, default)
