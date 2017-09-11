#!/usr/local/bin/python
##
## cloudfront_invalidate.py - A simple ansible module for making Cloudfront invalidation requests
##
## Copyright (C) 2016 KISS IT Consulting <http://www.kissitconsulting.com/>

## Redistribution and use in source and binary forms, with or without
## modification, are permitted provided that the following conditions
## are met:
##
## 1. Redistributions of source code must retain the above copyright
##    notice, this list of conditions and the following disclaimer.
## 2. Redistributions in binary form must reproduce the above
##    copyright notice, this list of conditions and the following
##    disclaimer in the documentation and/or other materials
##    provided with the distribution.
##
## THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
## "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
## LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
## A PARTICULAR PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL ANY
## CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
## EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
## PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
## PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY
## OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
## NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
## SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
DOCUMENTATION = '''
---
module: cloudfront_invalidate
short_description: Make Cloudfront invalidation requests.
description:
    - Makes Cloudfront invalidation requests.  The Cloudfront distribution id is referenced by its id. It is designed to be used for tasks such as code deployments where static assets are updated on a Cloudfront distribution and need to have their cache cleared.  This module has a dependency on python-boto.
version_added: "1.0"
options:
  aws_access_key:
    description:
      - The AWS Access Key.
    required: true
    default: null
    aliases: []
  aws_secret_key:
    description:
      - The AWS Secret Key.
    required: true
    default: null
    aliases: []
  distribution_id:
    description:
      - The Cloudfront Distribution ID.
    required: true
    default: null
    aliases: []
  path:
    description:
      - a path in the corresponding distribution to schedule an invalidation request for
    required: true
    default: null
    aliases: []

author: "Viktor Bonev (https://github.com/vpbonev)"
extends_documentation_fragment:
    - aws
    - ec2
'''

try:
    import boto
    import boto.ec2
    from boto import cloudfront
    from boto.cloudfront import CloudFrontConnection
    from boto3 import Session
    HAS_BOTO = True
except ImportError:
    HAS_BOTO = False


def main():
    argument_spec = aws_common_argument_spec()

    argument_spec.update(dict(
            aws_access_key = dict(required=True),
            aws_secret_key = dict(required=True),
            distribution_id = dict(required=True),
            path = dict(required=True),
        )
    )
    module = AnsibleModule(argument_spec=argument_spec)

    if not HAS_BOTO:
        module.fail_json(msg='boto 2/3 required for this module')

    distribution_id = module.params.get('distribution_id')
    path = module.params.get('path')
    aws_access_key = module.params.get('aws_access_key')
    aws_secret_key = module.params.get('aws_secret_key')

    # connect to Cloudfront
    try:
        conn = CloudFrontConnection(aws_access_key_id = aws_access_key, aws_secret_access_key = aws_secret_key)
    except boto.exception.BotoServerError as e:
        module.fail_json(msg = e.error_message)

    # Make the invalidation request
    invalidation = [path];
    conn.create_invalidation_request(distribution_id, invalidation)
    module.exit_json(msg="Path %s scheduled for invalidation." % (distribution_id), changed=True)

# import module snippets
from ansible.module_utils.basic import *
from ansible.module_utils.ec2 import *

if __name__ == '__main__':
    main()
