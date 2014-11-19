# Copyright (c) 2013-2014 Marin Atanasov Nikolov <dnaeon@gmail.com>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer
#    in this position and unchanged.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR(S) ``AS IS'' AND ANY EXPRESS OR
# IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
# OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE AUTHOR(S) BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
# NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
# THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""
vSphere Agent Session Tasks

"""

import logging

import pyVmomi

from vpoller.agent.core import task

@task(name='session.get', required=['hostname'])
def session_get(agent, msg):
    """
    Get the established vSphere sessions

    Example client message would be:

    {
        "method":   "session.get",
        "hostname": "vc01.example.org",
    }

    Returns:
        The established vSphere sessions in JSON format

    """
    logging.info('[%s] Retrieving established sessions', agent.host)

    try:
        sm = agent.si.content.sessionManager
        session_list = sm.sessionList
    except pyVmomi.vim.NoPermission:
        return {
            'msg': 'No permissions to view established sessions',
            'success': 1
        }

    props = [
        'key',
        'userName',
        'fullName',
        'loginTime',
        'lastActiveTime',
        'ipAddress',
        'userAgent',
        'callCount'
    ]

    sessions = []
    for session in session_list:
        s = {k: str(getattr(session, k)) for k in props}
        sessions.append(s)

    result = {
        'msg': 'Successfully retrieved sessions',
        'success': 0,
        'result': sessions,
    }

    logging.debug(
        '[%s] Returning result from operation: %s',
        agent.host,
        result
    )

    return result