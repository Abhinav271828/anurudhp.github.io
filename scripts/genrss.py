#!/bin/python3

import yaml
from pathlib import Path, PosixPath
from feedgen.feed import FeedGenerator
import argparse
import sh
import logging

# Generate the feed
def make_feed(feed: FeedGenerator, blogs: [PosixPath]):
    feed.title("Anurudh's Blog")
    feed.description("Navigating the manifold of computing")
    feed.author(name='Anurudh Peduri')
    feed.language('en')

    SITE_PATH = "https://anurudhp.github.io/"
    feed.link(href=SITE_PATH)
    feed.id(SITE_PATH)

    for blog in blogs:
        metadata = read_metadata(blog)
        if metadata is not None:
            logging.info(f'Adding: {metadata["title"]}')
            entry = feed.add_entry()
            loc = SITE_PATH+str(blog)
            entry.id(loc)
            entry.title(metadata['title'])
            entry.link(href=loc)
            pubDate = sh.date('-R', '-d', metadata['created']).strip()
            entry.pubDate(pubDate)

def read_metadata(src: PosixPath):
    try:
        yml_started, yml_ended = False, False
        yml_front = ''
        title = None

        with open(src) as f:
            prev_line = None
            for line in f:
                if line[:3] == '---' and yml_started: yml_ended = True
                if yml_started and not yml_ended: yml_front += line
                if line[:3] == '---' and not yml_started: yml_started = True
                if line[:3] == '===':
                    title = prev_line
                    break
                if line[:2] == '# ':
                    title = line[2:].strip()
                    break
                prev_line = line.strip()

        metadata = yaml.safe_load(yml_front)
        if metadata['layout'] != 'blog': return None
        metadata['title'] = title
        return metadata
    except Exception as e:
        logging.warning(f'Warning: ignoring file {src}, failed loading YML metadata')
        return None

def main():
    parser = argparse.ArgumentParser(description='Site RSS feed generator')
    parser.add_argument('-b', metavar='blogs_dir', help='Directory containing blogs', required=True, dest='blogs_dir')
    parser.add_argument('-o', metavar='rss_file', help='Output file (defaults to ./feed.xml)', default='feed.xml', dest='output')
    parser.add_argument('-a', metavar='atom_file', help='Output file (defaults to ./feed.xml)', dest='atom_output')
    parser.add_argument('-v', action='store_true', help='verbose mode, show info/warnings')
    args = parser.parse_args()

    if args.v:
        logging.basicConfig(level=logging.INFO)

    blogs = Path(args.blogs_dir).glob('*.md')
    feed = FeedGenerator()
    make_feed(feed, blogs)
    feed.rss_file(args.output, pretty=True)
    if args.atom_output:
        feed.atom_file(args.atom_output, pretty=True)

if __name__ == "__main__":
    main()

