from fastapi import HTTPException, Depends, status, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.users import User
from app.database import get_async_session
from app.routers.users import auth_handler


router = APIRouter()

@router.post("/subscriptions", status_code=status.HTTP_201_CREATED)
async def create_user_subscription(
    # subscription_data: SubscriptionCreate = Body(...),  # Define this Pydantic model
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(auth_handler.get_current_user),
):
    """
    Creates a new subscription for the current user.

    Requires Authentication (JWT).

    Request Body:
        - subscription_data (SubscriptionCreate): Details of the new subscription.

    Response (Success - 201 Created):
        - SubscriptionRead (schema): The newly created subscription object in JSON format.

    Error Codes:
        - 400 Bad Request: If the user already has an active subscription.
    """
    # TODO: Implement subscription creation logic here.
    # This would likely involve checking for an existing active subscription,
    # processing payment, creating the subscription entry, and returning
    # a representation of the newly created subscription.
    pass


@router.put("/subscriptions", status_code=status.HTTP_200_OK)
async def update_user_subscription(
    # subscription_data: SubscriptionUpdate = Body(...),  # Define this Pydantic model
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(auth_handler.get_current_user),
):
    """
    Updates the current user's subscription.

    Requires Authentication (JWT).

    Request Body:
        - subscription_data (SubscriptionUpdate): Updated subscription details.

    Response (Success - 200 OK):
        - SubscriptionRead (schema): The updated subscription object as JSON.
    """
    # TODO: Implement subscription update logic here, ensuring proper
    # validation and handling of potential errors (e.g., invalid subscription ID).
    pass


@router.delete("/subscriptions", status_code=status.HTTP_204_NO_CONTENT)
async def cancel_user_subscription(
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(auth_handler.get_current_user),
):
    """
    Cancels the current user's subscription.

    Requires Authentication (JWT).

    Response (Success - 204 No Content): Indicates successful cancellation.
    """
    # TODO: Implement subscription cancellation logic here, handling
    # potential errors (e.g., no active subscription to cancel).
    pass
