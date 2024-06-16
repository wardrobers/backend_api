from .core.products_schema import ProductBase, ProductCreate, ProductRead, ProductUpdate
from .core.variants_schema import VariantBase, VariantCreate, VariantRead, VariantUpdate
from .core.articles_schema import ArticleBase, ArticleCreate, ArticleRead, ArticleUpdate
from .inventorization.categories_schema import (
    CategoryBase,
    CategoryCreate,
    CategoryRead,
    CategoryUpdate,
)
from .inventorization.product_status_schema import (
    ProductStatusBase,
    ProductStatusCreate,
    ProductStatusRead,
    ProductStatusUpdate,
)
from .inventorization.stock_keeping_units_schema import (
    StockKeepingUnitBase,
    StockKeepingUnitCreate,
    StockKeepingUnitRead,
    StockKeepingUnitUpdate,
)
from .product_details.brand_schema import BrandBase, BrandCreate, BrandRead, BrandUpdate
from .product_details.colors_schema import (
    ColorBase,
    ColorCreate,
    ColorRead,
    ColorUpdate,
)
from .product_details.materials_schema import (
    MaterialBase,
    MaterialCreate,
    MaterialRead,
    MaterialUpdate,
)
from .sizing.size_systems_schema import (
    SizeSystemBase,
    SizeSystemCreate,
    SizeSystemRead,
    SizeSystemUpdate,
)
from .sizing.sizing_schema import SizingBase, SizingCreate, SizingRead, SizingUpdate

__all__ = [
    "ArticleBase",
    "ArticleCreate",
    "ArticleRead",
    "ArticleUpdate",
    "ProductStatusBase",
    "ProductStatusCreate",
    "ProductStatusRead",
    "ProductStatusUpdate",
    "StockKeepingUnitBase",
    "StockKeepingUnitCreate",
    "StockKeepingUnitRead",
    "StockKeepingUnitUpdate",
    "ProductBase",
    "ProductCreate",
    "ProductUpdate",
    "ProductRead",
    "VariantBase",
    "VariantCreate",
    "VariantUpdate",
    "VariantRead",
    "SizingBase",
    "SizingCreate",
    "SizingUpdate",
    "SizingRead",
    "SizeSystemBase",
    "SizeSystemCreate",
    "SizeSystemUpdate",
    "SizeSystemRead",
    "CategoryBase",
    "CategoryCreate",
    "CategoryUpdate",
    "CategoryRead",
    "BrandBase",
    "BrandCreate",
    "BrandUpdate",
    "BrandRead",
    "ColorBase",
    "ColorCreate",
    "ColorUpdate",
    "ColorRead",
    "MaterialBase",
    "MaterialCreate",
    "MaterialUpdate",
    "MaterialRead",
]
