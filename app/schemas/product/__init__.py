# import os
# import importlib

# # Dynamically import all routers from the current directory
# current_dir = os.path.dirname(__file__)
# for filename in os.listdir(current_dir):
#     if filename.endswith("_schema.py") and not filename.startswith("__"):
#         module_name = filename[:-3]
#         module = importlib.import_module(
#             "." + module_name, package="app.schemas.product"
#         )
#         globals()[module_name] = module
