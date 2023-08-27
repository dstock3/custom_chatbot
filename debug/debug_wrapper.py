from functools import wraps
from typing import Any, Callable

def debug(func: Callable[..., Any]) -> Callable[..., Any]:
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Function: {func.__name__}")
        arg_names = func.__code__.co_varnames[:func.__code__.co_argcount]
        arg_types = [type(arg).__name__ for arg in args]
        
        print("Arguments:")
        for name, value, value_type in zip(arg_names, args, arg_types):
            print(f"{name}: {value} (Type: {value_type})")
        
        for key, value in kwargs.items():
            print(f"{key}: {value} (Type: {type(value).__name__})")
            
        result = func(*args, **kwargs)
        
        print(f"Return value: {result} (Type: {type(result).__name__})")
        
        return result
    
    return wrapper