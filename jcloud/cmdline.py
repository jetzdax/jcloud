import argparse
import sys
import logging
from argparse import RawTextHelpFormatter
from jcloud.core import JCloudCore
from jcloud.errors import ParamError, UsageError, TemplateError, ClientError, CloudError

logger = logging.getLogger(__package__)


def main():
    """ Entrypoint to jcloud CLI as defined in setup.py """
    parser = argparse.ArgumentParser(formatter_class=RawTextHelpFormatter,
                                     description="Combines the power of jinja2 and cloudformation templates")
    parser.add_argument("-i", "--input", help="The input jinja2 file.", required=True)
    parser.add_argument("-e", "--execute", required=True, choices=JCloudCore.help("command"),
                        help="The command to execute:\n" + '\n'.join(JCloudCore.help("help")))
    parser.add_argument("-p", "--params", help="The input parameters files, comma separated.")
    parser.add_argument("-c", "--config", help="The configuration file.", default="jcloud.cfg")
    parser.add_argument("-v", "--verbose", action="store_true", help="Turn on verbose logging.")
    # parser.add_argument("-V", "--version", help="Show the version number.")
    parser.add_argument("--params-dir", help="The directory where the params files reside.")

    # Future
    # parser.add_argument("--profile", help="The AWS profile to use.")
    # parser.add_argument("--region", help="The AWS region.")
    # parser.add_argument("--use-changeset", help="Use changeset to deploy instead of directly (prompts user).")
    # parser.add_argument("-y", "--yes", help="Automatically select 'yes' when prompted")

    args = parser.parse_args()
    if args.verbose:
        logger.setLevel(logging.INFO)
        log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        log_handler = logging.StreamHandler()
        log_handler.setFormatter(log_formatter)
        logger.addHandler(log_handler)

    try:
        jcloud_core = JCloudCore(args)
        jcloud_core.execute()
    except UsageError as e:
        logger.error(e)
        parser.print_help()
        sys.exit(1)
    except ParamError as e:
        logger.error(e)
        sys.exit(1)
    except TemplateError as e:
        logger.error(e)
        sys.exit(1)
    except ClientError as e:
        logger.error(e)
        sys.exit(2)
    except CloudError as e:
        logger.error(e)
        sys.exit(2)
    # except BotoCoreError as e:
    #     logger.error(e)
    #     sys.exit(2)
    except Exception as e:
        logger.error(e)
        sys.exit(2)
