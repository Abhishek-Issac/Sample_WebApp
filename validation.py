import hmac
import hashlib
import json
from urllib.parse import parse_qsl


def validate_webapp_data(init_data: str, bot_token: str) -> dict:
    """
    Validate Telegram WebApp data.
    
    Args:
        init_data: The initData string from Telegram.WebApp.initData
        bot_token: The bot token
        
    Returns:
        dict: The user data if validation succeeds
        
    Raises:
        ValueError: If validation fails
    """
    try:
        # Parse the init_data
        parsed_data = dict(parse_qsl(init_data))
        
        # Extract hash
        received_hash = parsed_data.pop('hash', None)
        if not received_hash:
            raise ValueError("Hash not found in init data")
        
        # Create data check string
        data_check_arr = [f"{k}={v}" for k, v in sorted(parsed_data.items())]
        data_check_string = '\n'.join(data_check_arr)
        
        # Calculate secret key
        secret_key = hmac.new(
            key=b"WebAppData",
            msg=bot_token.encode(),
            digestmod=hashlib.sha256
        ).digest()
        
        # Calculate hash
        calculated_hash = hmac.new(
            key=secret_key,
            msg=data_check_string.encode(),
            digestmod=hashlib.sha256
        ).hexdigest()
        
        # Compare hashes
        if not hmac.compare_digest(calculated_hash, received_hash):
            raise ValueError("Data cannot be trusted - hash mismatch")
        
        # Check auth_date (optional: verify it's not too old)
        auth_date = int(parsed_data.get('auth_date', 0))
        if not auth_date:
            raise ValueError("auth_date not found")
        
        # Parse and return user data
        user_json = parsed_data.get('user')
        if not user_json:
            raise ValueError("User data not found")
        
        user_data = json.loads(user_json)
        return user_data
        
    except Exception as e:
        raise ValueError(f"Validation error: {str(e)}")
