from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.post("/verify-token")
def verify_token_endpoint(id_token: str):
    try:
        # Call the function that uses Firebase Admin SDK
        user_info = verify_id_token(id_token)
        # Perform operations with the verified user info
        return {"user_id": user_info['uid']}
    except HTTPException as exc:
        # Handle authentication error
        raise exc
