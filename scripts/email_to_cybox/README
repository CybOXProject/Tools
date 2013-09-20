# Copyright (c) 2013, The MITRE Corporation. All rights reserved.
# See LICENSE.txt for complete terms.

Email to CybOX v2.0.1 Translator
Converts raw email to CybOX representation

2013 - Bryan Worrell & Greg Back - The MITRE Corporation
Version 2.0.1

usage: email_to_cybox.py [-h] [-v] [--exclude-attachments]
                         [--exclude-raw-body] [--exclude-raw-headers]
                         [--exclude-urls] [--exclude-domain-objs]
                         [--exclude-url-objs] [--whois] [--http-whois] [--dns]
                         [--use-dns-server DNS-SERVER] [--headers HEADERS]
                         input

positional arguments:
  input                 message data (can be either a file or '-' for STDIN)

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         verbose output
  --exclude-attachments
                        exclude attachments from cybox email message object
  --exclude-raw-body    exclude raw body from email message object
  --exclude-raw-headers
                        exclude raw headers from email message object
  --exclude-urls        do not attempt to parse urls from input
  --exclude-domain-objs
                        do not create URI domain objects for found URLS
  --exclude-url-objs    do not create URI objects for found URLs
  --whois               attempt to perform s WHOIS lookup of domains found
                        within the email and create a WHOIS record object
  --http-whois          Use a HTTP WHOIS service that operates on port 80
                        (useful if port 43 is blocked by a firewall)
  --dns                 attempt to perform a dns lookup for domains within the
                        email and create a DNS record object
  --use-dns-server DNS-SERVER
                        use this DNS server for DNS lookup of domains
  --headers HEADERS     comma-separated list of header fields to be included
                        in the in the CybOX EmailMessage output. DO NOT
                        INCLUDE SPACES. Allowed fields: to, cc, bcc, from,
                        subject, in-reply-to, date, message-id, sender, reply-
                        to, errors-to, boundary, content-type, mime-version,
                        precedence, user-agent, x-mailer, x-originating-ip,
                        x-priority. If not specified, all of these headers
                        will be included if present.

Examples:
`python email_to_cybox.py foobar.txt > output.xml`
`cat email.txt | python email_to_cybox.py - > output.xml`
`python email_to_cybox.py --headers to,from,cc --exclude-urls foobar.txt > output.xml`

Requirements
============
The Email-to-CybOX script requires Python 2.7 and depends on the following
modules, which can be installed using "pip" (i.e. `pip install cybox dnspython
python-whois`).

* [[cybox]] (https://pypi.python.org/pypi/cybox)
* [[dnspython]] (https://pypi.python.org/pypi/dnspython)
* [[python-whois]] (https://pypi.python.org/pypi/python-whois)

The script may also work with Python 2.6, but requires the "argparse" package
to be installed separately. However, this has not been tested.
