import lxml.etree as etree

from .soap.protocol import (
    cleanup_command, close_shell_payload, command_output, create_command,
    create_shell_payload, parse_create_shell_response,
    parse_create_command_response, parse_command_output
)


class ShellContext:
    def __init__(self, session, host, env=None, cwd=None):
        self._session = session

        self.host = host
        self.env = env
        self.cwd = cwd

        self._shell_id = None

    def __enter__(self):
        payload = etree.tostring(create_shell_payload(self.env, self.cwd))
        resp = self._session.post(self.host, data=payload)
        resp.raise_for_status()

        self._shell_id = parse_create_shell_response(resp.text)

        return self

    def __exit__(self, *a, **kw):
        payload = etree.tostring(close_shell_payload(self._shell_id))
        resp = self._session.post(self.host, data=payload)
        resp.raise_for_status()


class CommandContext:
    @classmethod
    def from_shell_context(cls, shell_context, command, args=()):
        return cls(
            shell_context._session, shell_context.host,
            shell_context._shell_id, command, args
        )

    def __init__(self, session, host, shell_id, command, args=()):
        self._session = session
        self._shell_id = shell_id

        self.host = host
        self.command = command
        self.args = args

        self._command_id = None

    def __enter__(self):
        payload = etree.tostring(
            create_command(self._shell_id, self.command, self.args)
        )
        resp = self._session.post(self.host, data=payload)
        resp.raise_for_status()

        self._command_id = parse_create_command_response(resp.text)

        return self

    def __exit__(self, *a, **kw):
        payload = etree.tostring(
            cleanup_command(self._shell_id, self._command_id)
        )
        resp = self._session.post(self.host, data=payload)
        resp.raise_for_status()

    def _output_request(self):
        payload = etree.tostring(command_output(self._shell_id, self._command_id))
        resp = self._session.post(self.host, data=payload)
        resp.raise_for_status()

        stdout, stderr, return_code, is_done = parse_command_output(resp.text)

        return (
            stdout.decode("utf8"), stderr.decode("utf8"), return_code, is_done
        )

    def get_output(self):
        out_buffer = []
        err_buffer = []

        is_done = False

        while not is_done:
            out, err, return_code, is_done = self._output_request()

            if out:
                out_buffer.append(out)
            if err:
                err_buffer.append(err)

        return "\n".join(out_buffer), "\n".join(err_buffer)
