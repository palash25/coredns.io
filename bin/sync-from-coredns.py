#!/usr/bin/python

# Copy the <plugin>/README.md to plugins/<mddleware>.md, add
# some Hugo meta data to let Hugo render it.

import datetime
import os
import re
import sys

def header(plugin, title, description, weight):
  h = """+++
title = "%(title)s"
description = "%(description)s"
weight = %(weight)s
tags = [ "plugin", "%(plugin)s" ]
categories = [ "plugin" ]
date = "%(date)s"
+++
""" % {'title': title, 'description': description,
      'weight': weight, 'plugin': plugin,
      'date': str(datetime.datetime.utcnow().isoformat()) }
  return h

def parse(readme, plugin):
  file = open(readme)

  description, title, rest = '', '', ''
  
  state = 'TITLE'
  line = file.readline()
  while line:
    if state == 'TITLE':
      title = re.sub('# ?', '', line).rstrip()
      state = 'SKIP'
      line = file.readline()
      continue

    if state == 'SKIP':
      if line.strip() == '':
        line = file.readline()
        continue
      state = 'DESCRIPTION'

    if state == 'DESCRIPTION':
      if line.strip() == '':
        state = 'REST'
      else:
        description += line.rstrip() + " "

    if state == 'REST':
      rest += line

    line = file.readline()

  file.close()
  h = header(plugin, title, description.rstrip(), weight)
  return h + rest

weight=0
tags='plugin'
content='../content/plugin'

if not os.path.isdir(content):
  sys.exit("%s: Need to be run from the site's bin directory" % sys.argv[0])

if len(sys.argv) < 2:
  sys.exit("%s: Need containing directory of CoreDNS plugins" % sys.argv[0])


for plugin in sorted(os.listdir(sys.argv[1])):
  dir = os.path.join(sys.argv[1], plugin)
  readme = os.path.join(dir, "README.md")
  page = os.path.join(content, plugin) + ".md"
  if os.path.isdir(dir) and os.path.exists(readme):
    weight+=1
    print >> sys.stderr, readme + " --> " + page
    p = parse(readme, plugin)
    filep = open(page, 'w')
    filep.write(p)
    filep.close()
