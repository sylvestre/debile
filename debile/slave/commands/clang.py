# Copyright (c) 2012-2013 Paul Tagliamonte <paultag@debian.org>
# Copyright (c) 2013 Leo Cavaille <leo@cavaille.net>
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

from debile.slave.runners.sbuild import sbuild, version
import glob


def run(dsc, package, job, firehose):
    build_arch = job['arch'] != "all"
    build_indep = job['arch'] == "all" or job['do_indep']
    maintainer = package['config'].get('sbuild', {}).get('maintainer')
    firehose, out, ftbfs, changes, = \
        sbuild(dsc, maintainer, package['suite'], package['affinity'], build_arch, build_indep, firehose, True)

    if not changes and not ftbfs:
        print(out)
        print(changes)
        print(list(glob.glob("*")))
        raise Exception("Um. No changes but no FTBFS.")

    if not ftbfs:
        changes = changes[0]
    else:
        changes = None

    return (firehose, out, ftbfs, changes, None)


def get_version():
    return version()
