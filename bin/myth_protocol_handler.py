#!/usr/bin/env python
#TODO: a generic myth protocol handler wouldn't just field requests for
# memoboard, so this could/should be moved into its own package/module
import sys
import memoboard

memoboard_client = memoboard.Client()
memo = memoboard_client.url2memo(sys.argv[1])

