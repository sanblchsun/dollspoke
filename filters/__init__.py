from loader import dp
from .admin_filter import AdminFilter


if __name__ == "filters":
    dp.filters_factory.bind(AdminFilter)
    # dp.filters_factory.bind(MyFilter)

