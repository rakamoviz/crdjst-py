import core_business
from server import initialize as initialize_server

logger = None

cb = core_business.CoreBusiness(logger)
server = initialize_server(cb, logger)