def object_to_dict(obj):
    if isinstance(obj, list):
        # Recursively handle lists
        return [object_to_dict(item) for item in obj]
    elif hasattr(obj, "__dict__"):
        # Convert objects with __dict__ attribute (typical Python objects)
        return {key: object_to_dict(value) for key, value in obj.__dict__.items()}
    else:
        # Return primitive types as-is
        return obj

