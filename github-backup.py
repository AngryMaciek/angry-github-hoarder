"""
##############################################################################
#
#   AUTHOR: Maciek Bak
#
##############################################################################
"""

# imports
import os
import subprocess
import time
import logging
import logging.handlers
from argparse import ArgumentParser, RawTextHelpFormatter
from datetime import datetime
from github import Github


def parse_arguments():
    """Parser of the command-line arguments."""
    parser = ArgumentParser(description=__doc__, formatter_class=RawTextHelpFormatter)
    parser.add_argument(
        "-v",
        "--verbosity",
        dest="verbosity",
        choices=("DEBUG", "INFO", "WARN", "ERROR", "CRITICAL"),
        default="ERROR",
        help="Verbosity/Log level. Defaults to ERROR",
    )
    parser.add_argument(
        "-l", "--logfile", dest="logfile", help="Store log to this file."
    )
    parser.add_argument(
        "--username",
        dest="username",
        required=True,
        help="GitHub username.",
    )
    parser.add_argument(
        "--pat",
        dest="pat",
        required=True,
        help="GitHub PAT.",
    )
    return parser


##############################################################################


def main():
    """Main body of the script."""

    # get all repos a user has access to
    gh = Github(options.username, options.pat)
    user = gh.get_user()
    # filter for those under the user account
    userrepos = {
        repo.name : repo.git_url for repo in user.get_repos() \
            if repo.git_url.startswith("git://github.com/" + options.username)
    }
    # create a backup dir
    dirname = datetime.today().strftime("%Y%m%d-%H%M%S")
    os.makedirs("../" + dirname)
    # clone all user repos
    for k, v in userrepos.items():
        url = "https://" + options.pat + "@" + v.removeprefix("git://")
        subprocess.check_call([
            "git",
            "clone",
            url,
            "../" + dirname + "/" + k
        ])


##############################################################################

if __name__ == "__main__":

    try:
        # parse the command-line arguments
        options = parse_arguments().parse_args()

        # set up logging during the execution
        formatter = logging.Formatter(
            fmt="[%(asctime)s] %(levelname)s - %(message)s",
            datefmt="%d-%b-%Y %H:%M:%S",
        )
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger = logging.getLogger("logger")
        logger.setLevel(logging.getLevelName(options.verbosity))
        logger.addHandler(console_handler)
        if options.logfile is not None:
            logfile_handler = logging.handlers.RotatingFileHandler(
                options.logfile, maxBytes=50000, backupCount=2
            )
            logfile_handler.setFormatter(formatter)
            logger.addHandler(logfile_handler)

        # execute the body of the script
        start_time = time.time()
        logger.info("Starting script")
        main()
        seconds = time.time() - start_time

        # log the execution time
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        logger.info(
            "Successfully finished in {hours}h:{minutes}m:{seconds}s",
            hours=int(hours),
            minutes=int(minutes),
            seconds=int(seconds) if seconds > 1.0 else 1,
        )
    # log the exception in case it happens
    except Exception as e:
        logger.exception(str(e))
        raise e


'''
# Create the backup in the dir of a current date: YYYYMMDD
date=$(date "+%Y%m%d")
mkdir "$date"
cd "$date" || exit

# Inspect repos from page 1 | max repos per page is 100
curl "https://api.github.com/users/AngryMaciek/repos?page=1&per_page=100" |
grep -e "git_url*" |
cut -d \" -f 4 |
xargs -L1 git clone
'''
