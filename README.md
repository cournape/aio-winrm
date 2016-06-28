Python 3.5+ library implementing the WinRM protocol on top of asyncio. Work in
progress.

Sync API:

    from aiowinrm.sync import run_cmd

    host = "192.168.1.1"
    auth = ("user", "password")
    response = run_cmd(host, auth, "ipconfig", ("/all",))
