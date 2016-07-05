Python 3.5+ library implementing the WinRM protocol on top of asyncio. Work in
progress: no TLS (plain text only), API not stable.

Sync API:

    from aiowinrm.sync import run_cmd

    host = "192.168.1.1"
    auth = ("user", "password")
    response = run_cmd(host, auth, "ipconfig", ("/all",))

Tentative async API:

    import asyncio
    from aiowinrm import winrm_command

    def callback_factory(host):
        """ Returns a callback that prefix every output line by host.
        """
        def callback(s):
            output = "\n".join(
                host + ":" + line
                for line in s.splitlines()
            )
            print(output)

        return callback

    host = "172.17.5.2"
    auth = ("vagrant", "vagrant")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        run_cmd(
            host, auth, "ipconfig", ("/All",),
            stdout_callback=callback_factory(host),
            stderr_callback=callback_factory(host),
        )
    )
    loop.close()
