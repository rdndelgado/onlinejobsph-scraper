from services.mapper_workflow import run_mapper
from services.parser_workflow import run_parser
from utils.logger import get_logger

logger = get_logger(__name__)

if __name__ == "__main__":
    mapper_result = run_mapper()
    logger.info("mapper result=%s", mapper_result)

    parser_result = run_parser()
    logger.info("parser result=%s", parser_result)
