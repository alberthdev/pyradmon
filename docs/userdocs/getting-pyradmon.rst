Getting PyRadmon
***********************************************************************

You can grab the latest source code
`here <https://github.com/alberthdev/pyradmon>`_.

Stable Release
--------------

To get a stable release, go to the
`releases page <https://github.com/alberthdev/pyradmon/releases>`_
and grab your preferred release. Beta and alpha versions of PyRadmon
are also available on this page.

Latest Git
----------

.. warning:: 

   The latest Git code is bleeding-edge. Code from Git changes
   frequently, and may be unstable. Do not attempt to use live Git code
   in a production environment!

Downloading from Git
++++++++++++++++++++

To get the latest code, run the following command::

    git clone https://github.com/alberthdev/pyradmon.git

If your version of Git is old, you may receive errors like these::

    error: The requested URL returned error: 401 while accessing
    # https://github.com/user/repo.git/info/refs?service=git-receive-pack
    # fatal: HTTP request failed

::

    Error: The requested URL returned error: 403 while accessing
    # https://github.com/user/repo.git/info/refs
    # fatal: HTTP request failed

::

    Error: https://github.com/user/repo.git/info/refs not found: did you run git
    # update-server-info on the server?

If you get any of these errors, try updating your Git to the latest
version.

If you are unable to update your Git for whatever reason, you can alternatively try::

    svn co https://github.com/alberthdev/pyradmon

Updating Git Source
+++++++++++++++++++

If you're using Git, you can update from Git! From within the PyRadmon directory root, run::

    git pull

If you're using SVN, you can still update! From within the trunk directory root, run::

    svn update


