# -*- mode: python, coding: utf-8 -*-
# shell.py: Shell entrypoint
# (C) 2014 Takahiro Yoshimura <altakey@gmail.com>.  All rights reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import csv
import re
import sys
import urllib3
from bs4 import BeautifulSoup

http = urllib3.PoolManager()

class KnownLinksParser:
  def __init__(self, f):
    self.f = f

  def parse(self):
    out = dict()
    for content,url in csv.reader(self.f, csv.excel_tab):
      out[content] = url
    return out

class TitleFetcher:
  def __init__(self):
    self.cache = dict()

  def fetch(self, url):
    try:
      return self.cache[url]
    except KeyError:
      self.cache[url] = self.resolve(url)
      return self.cache[url]

  def resolve(self, url):
    r = http.request('GET', url)
    try:
      return BeautifulSoup(r.data).title.string.strip()
    except AttributeError:
      return None

class TagFormatter:
  def __init__(self, known_links):
    self.fetcher = TitleFetcher()
    self.formatter = self.format_normal
    self.known_links = known_links

  def format(self, l):
    if self.formatter is None:
      return self.format_normal(l)
    else:
      return self.formatter(l)

  def resolve_link(self, m):
    maybe_relic = m.group(1)
    if '|' in maybe_relic:
      content, url = maybe_relic.split('|')
      if content not in self.known_links:
        self.known_links[content] = url
      return r'<a href="%s" title="%s">%s</a>' % (url, self.fetcher.fetch(url), content)
    else:
      url, content = self.known_links[maybe_relic], maybe_relic
      return r'<a href="%s" title="%s">%s</a>' % (url, self.fetcher.fetch(url), content)

  def format_pre(self, l):
    if self.look(l, ['/pre']):
      self.formatter = None
    return l.rstrip('\n')

  def format_normal(self, l):
    if self.look(l, ['pre']):
      self.formatter = self.format_pre
      return self.format(l)
    else:
      l = l.strip()
      l = re.sub(r'^h([0-9]). (.*)$', r'<h\1>\2</h\1>', l)
      l = re.sub(r'^<p></p>$', '<br />', re.sub(r'^((?!<).*(?<!>))$', r'<p>\1</p>', l))
      l = re.sub(r'\[(.+?)\]', self.resolve_link, l)
      return l

  def look(self, l, scopes):
    m = re.match('<(/?(?:%s))>' % '|'.join(scopes), l)
    if m:
      return m.group(1)
    else:
      return None
