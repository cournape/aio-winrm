import aiohttp

from .core import CommandContext, ShellContext


async def run_cmd(host, auth, command, args=(), env=None, cwd=None,
                        stdout_callback=None, stderr_callback=None):
    """ Run the given command on the given host asynchronously.
    """
    async with aiohttp.ClientSession(auth=auth) as session:
        async with ShellContext(session, host, env=env, cwd=cwd) as shell_context:
            async with CommandContext(
                session, host, shell_context.shell_id, command, args
            ) as command_context:
                is_done = False
                while not is_done:
                    stdout, stderr, return_code, is_done = await command_context._output_request()
                    for out, callback in (
                        (stdout, stderr_callback), (stderr, stderr_callback)
                    ):
                        if out and callback:
                            callback(out)
