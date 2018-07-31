# untrustworthy (pwn 451p, 3 solved)

> Don't trust everything you see. There are secrets hidden in plain sight.

## Exploitation

1. Spawn `worker` by calling `server.exe` API exposed via Microsoft RPC

2. Copy pre-existing `fail_plugin.dll` to a temporary (writable) file

3. Send `auth::PluginBasedAuth` request over `worker` pipe using the temporary file as plugin

4. Attempt to modify the temporary file between `sha256` validation and `LoadLibraryA` by exploiting `worker` race-condition on plugin loading

   The modification is to return success from `auth` plugin API.

5. Receive `auth` response over `worker` pipe

The exploit repeats steps 2..5, to improve chance of winning the race-condition.
Without any tuning, the 100 iterations are sufficient to reliably receive the flag.

Full exploit is attached [here](exploit.c).
