# Hashing@Home (pwn, 231+10 pts, 14 solved)

The server uses the memory addresses of `hash_rpc_context` structures as request ids to track work delegated to its clients.
However the verification of any request ids received by the server in client responses is insufficient and the clients may abuse this to overwrite any memory locations that pass simple check for valid `hash_rpc_context` structure header.

Further, it is possible for the clients to sent arbitrary response data to be stored as `data_to_hash` member of existing `hash_rpc_context` structures in server memory.
This allows the clients to craft fake `hash_rpc_context` structures that pass server checks.

The above may be used to read arbitrary server memory by overwriting `hash_rpc_context` structure of `first_context` and next triggering `hash_together_the_first_two`.
This xors arbitrary memory location with known bytes and sends result as new request to the client.

My [exploit](exploit.py) uses this to extract content of `key_bytes` containing the flag.
