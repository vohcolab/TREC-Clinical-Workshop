import sys
import requests
import xml
import xml.etree.ElementTree as ET
from optparse import OptionParser

op = OptionParser()
op.add_option("-o",
              dest="output", type="str",
              help="Specify output file path for the xml topics")

# +
topics_url = 'http://www.trec-cds.org/topics2021.xml'

res = requests.get(topics_url, headers={"User-Agent": "XY"})
assert res.status_code == 200, "Oops, couldn't download the topics"

# +
argv = sys.argv[1:]
(opts, args) = op.parse_args(argv)

output = opts.output

# add .xml extension if not already there
if output[-4:] != '.xml':
    output += '.xml'
    
# save contents
with open(output,'w') as f:
    f.write(res.text)
print('Done!')
# -


