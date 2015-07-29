#!/usr/bin/python
import sys, os
import SimpleHTTPServer
import SocketServer

import sc_final_report as sc
#import check_upload as c
#import delete_entities as d

PORT = 8005

Handler = SimpleHTTPServer.SimpleHTTPRequestHandler

httpd = SocketServer.TCPServer(("localhost", PORT), Handler)

print "serving at port", PORT

#print sc.list_entities(sys.argv[1], sys.argv[2])
sc.write_report(sys.argv[1], sys.argv[2])

print "CSV written!"

####################
#c.find_entities_by_code("after_delete.csv", "eleonore@mastodonc.com", "Mastodonc")

#d.delete_properties(d.test_properties, sys.argv[1], sys.argv[2])
###################

httpd.serve_forever()
