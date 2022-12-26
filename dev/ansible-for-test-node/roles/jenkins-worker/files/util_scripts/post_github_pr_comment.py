#!/usr/bin/env python3
"""Utility program to post a comment to a github PR"""
import argparse
import json
import os
import sys
import urllib.parse
from urllib.error import HTTPError, URLError
from urllib.request import urlopen, Request


def _parse_args():
    pr_link_var = "ghprbPullLink"
    pr_link_option = "--pr-link"
    github_oauth_key_var = "GITHUB_OAUTH_KEY"
    github_oauth_key_option = "--github-oauth-key"
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-pr",
        pr_link_option,
        default=os.environ.get(pr_link_var, ""),
        help="Specify pull request link",
    )
    parser.add_argument(
        github_oauth_key_option,
        default=os.environ.get(github_oauth_key_var, ""),
        help="Specify github oauth key",
    )
    args = parser.parse_args()
    if not args.pr_link:
        parser.error(
            f"Specify either environment variable {pr_link_var} or option {pr_link_option}"
        )
    if not args.github_oauth_key:
        parser.error(
            f"Specify either environment variable {github_oauth_key_var} or option {github_oauth_key_option}"
        )
    return args


def post_message_to_github(msg, github_oauth_key, pr_link):
    print("Attempting to post to Github...")

    ghprb_pull_id = os.environ["ghprbPullId"]
    api_url = os.getenv("GITHUB_API_BASE", "https://api.github.com/repos/apache/spark")
    url = f"{api_url}/issues/{ghprb_pull_id}/comments"

    posted_message = json.dumps({"body": msg})
    request = Request(
        url,
        headers={
            "Authorization": f"token {github_oauth_key}",
            "Content-Type": "application/json",
        },
        data=posted_message.encode("utf-8"),
    )
    try:
        response = urlopen(request)

        if response.getcode() == 201:
            print(" > Post successful.")
        else:
            print_err("Surprising post response.")
            print_err(f" > http_code: {response.getcode()}")
            print_err(f" > api_response: {response.read()}")
            print_err(f" > data: {posted_message}")
    except HTTPError as http_e:
        print_err("Failed to post message to Github.")
        print_err(f" > http_code: {http_e.code}")
        print_err(f" > api_response: {http_e.read()}")
        print_err(f" > data: {posted_message}")
    except URLError as url_e:
        print_err("Failed to post message to Github.")
        print_err(f" > urllib_status: {url_e.reason[1]}")
        print_err(f" > data: {posted_message}")


def print_err(msg):
    print(msg, file=sys.stderr)


def _main():
    args = _parse_args()
    msg = sys.stdin.read()
    post_message_to_github(msg, args.github_oauth_key, args.pr_link)
    return 0


if __name__ == "__main__":
    sys.exit(_main())
