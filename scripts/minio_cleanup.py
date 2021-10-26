# Copyright (c) 2019, IRIS-HEP
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# * Neither the name of the copyright holder nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import argparse
import logging
import os
import sys

from servicex_storage import minio_storage_manager


def run_minio_cleaner():
    '''Run the minio cleaner
    '''
    logger = logging.getLogger()

    # Parse the command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--max-size', dest='max_size', action='store',
                        default='',
                        help='Max size allowed before pruning storage')

    args = parser.parse_args()
    logger.info("ServiceX Minio Cleaner starting up. "
                f"Max size for storage: {args.max_size}")

    env_vars = ['MINIO_URL', 'ACCESS_KEY', 'SECRET_KEY']
    error = False
    for var in env_vars:
        if var not in os.environ:
            logger.error(f"{var} not found in environment")
            error = True
    if error:
        logger.error("Exiting due to missing environment variables")
        sys.exit(1)

    try:
        store = servicex_storage.minio_storage_manager.MinioStore(minio_url=os.environ['MINIO_URL'],
                                                                  access_key=os.environ['ACCESS_KEY'],
                                                                  secret_key=os.environ['SECRET_KEY'])
        store.cleanup_storage()
    finally:
        logger.info('Done running minio storage cleanup')


if __name__ == "__main__":
    run_minio_cleaner()
