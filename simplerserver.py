#!/usr/bin/python
import sys, os
import SimpleHTTPServer
import SocketServer

import upload_measurements as um
#import sc_final_report as sc
#import check_upload as c
#import delete_entities as d

PORT = 8005

Handler = SimpleHTTPServer.SimpleHTTPRequestHandler

httpd = SocketServer.TCPServer(("localhost", PORT), Handler)

print "serving at port", PORT

# print sc.list_entities(sys.argv[1], sys.argv[2])
# sc.write_report(sys.argv[1], sys.argv[2])

# print "CSV written!"

um.post_measurements("45f93880-df89-4565-acd1-6a1d6c22792c", "d434ec0e-210f-4937-9873-6c42eddd3936", sys.argv[1], sys.argv[2])


####################
#c.find_entities_by_code("after_delete.csv", "eleonore@mastodonc.com", "Mastodonc")

#d.delete_properties(d.test_properties, sys.argv[1], sys.argv[2])
###################

httpd.serve_forever()
