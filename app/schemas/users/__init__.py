from .activity.user_activity_schema import UserActivityBase, UserActivityRead
from .activity.user_reviews_and_ratings_schema import (
    UserReviewRatingBase,
    UserReviewRatingCreate,
    UserReviewRatingRead,
)
from .activity.user_saved_items_schema import (
    UserSavedItemBase,
    UserSavedItemCreate,
    UserSavedItemRead,
)
from .core.data_privacy_consents_schema import (
    DataPrivacyConsentBase,
    DataPrivacyConsentCreate,
    DataPrivacyConsentRead,
)
from .core.user_info_schema import UserInfoBase, UserInfoCreate, UserInfoUpdate
from .core.users_schema import (
    UsersBase,
    UsersCreate,
    UsersDelete,
    UsersRead,
    UsersUpdate,
)
from .profile.user_addresses_schema import (
    AddressType,
    UserAddressBase,
    UserAddressCreate,
    UserAddressUpdate,
)
from .profile.user_photos_schema import UserPhotoBase, UserPhotoCreate, UserPhotoRead
from .roles.roles_schema import RoleAssign, RoleBase, RoleRead

__all__ = [
    "UserActivityBase",
    "UserActivityRead",
    "UserReviewRatingBase",
    "UserReviewRatingCreate",
    "UserReviewRatingRead",
    "UserSavedItemBase",
    "UserSavedItemCreate",
    "UserSavedItemRead",
    "AddressType",
    "RoleAssign",
    "RoleBase",
    "RoleRead",
    "UserAddressBase",
    "UserAddressCreate",
    "UserAddressUpdate",
    "UserInfoBase",
    "UserInfoCreate",
    "UserInfoUpdate",
    "UserPhotoBase",
    "UserPhotoCreate",
    "UserPhotoRead",
    "UsersBase",
    "UsersCreate",
    "UsersDelete",
    "UsersRead",
    "UsersUpdate",
    "DataPrivacyConsentBase",
    "DataPrivacyConsentCreate",
    "DataPrivacyConsentRead",
]
