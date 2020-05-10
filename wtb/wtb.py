#!/usr/bin/env python3

"""
Perform traceroutes against a given list of targets via TCP, UDP,
HTTP, TCP, or HTTPS.
"""

import logging
import sys
from argparse import ArgumentParser

import coloredlogs

from classes.worker import Worker
from utils.get_url_list import main as get_url_list

logging.getLogger("scapy").setLevel(logging.ERROR)
logging.getLogger("requests").setLevel(logging.WARNING)

log = logging.getLogger(__name__)
coloredlogs.install(level="INFO", fmt="%(message)s")


if __name__ == "__main__":
    parser = ArgumentParser("Listen for targets to perform traceroutes.")

    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        default=False,
        help="Enable verbose logging.",
    )
    parser.add_argument(
        "-a", "--addr", default="0.0.0.0", help="Address to listen on for connections."
    )
    parser.add_argument(
        "-p",
        "--port",
        type=int,
        default=42075,
        help="Port for this worker to listen on for remote connections.",
    )
    parser.add_argument(
        "--get-url-list",
        type=str,
        metavar="COUNTRY CODE",
        help="Download a URL list for a given country code (ex: cn)",
    )

    args = parser.parse_args()

    # set log level to debug if verbose flag is passed
    if args.verbose:
        coloredlogs.install(
            level="DEBUG", fmt="%(asctime)s - %(levelname)s - %(message)s"
        )

    if args.get_url_list:
        get_url_list(args.get_url_list)
        sys.exit(0)

    worker = Worker(address=args.addr, port=args.port)
    if worker.bind():
        log.info(f"Worker is bound on {args.addr}:{args.port}.")

        try:
            worker.keep_alive()

        except KeyboardInterrupt:
            worker.shutdown()

    else:
        log.error(f"Unable to bind worker on {args.port}.")
