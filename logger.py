import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - \
%(levelname)s - %(funcName)s [%(lineno)d] - \
%(message)s')
LOGGER = logging.getLogger(__name__)
