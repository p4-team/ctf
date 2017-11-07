# Data and Mining (Forensics, 137p)

In the task we get a rather large pcapng file (230 MB!), but the task was actually rather trivial because the flag was written in plaintext.
Since we didn't expect it to be so, we first did load the file into Network Miner and Wireshark to see what exactly we have there.

Most of is was some strange and random packets but looking around available TCP streams we finally find:

```
{"method":"login","params":{"login":"45duiDz79Y2AtSZH2pw9uV8YXmvtAT8tVNAYrfKTUnYiQZT5BMdRrGD4hbipmZ5DoaQXLak9ENEwYNC7kVk3ivDyMHyZCVV","pass":"hitcon{BTC_is_so_expensive_$$$$$$$}","agent":"xmr-stak-cpu/1.3.0-1.5.0"},"id":1}
{"id":1,"jsonrpc":"2.0","error":null,"result":{"id":"862725926260463","job":{"blob":"0606f0caedcf05fdd86cbe0f15bc3348d604fe35830c579edf14293facd6ea0ccfe3eee4333da700000000fcbc11627100084072bdf490f984a780283662579715458b5b7cc79241b9916813","job_id":"505683845491148","target":"711b0d00"},"status":"OK"}}
{"jsonrpc":"2.0","method":"job","params":{"blob":"0606f0caedcf05fdd86cbe0f15bc3348d604fe35830c579edf14293facd6ea0ccfe3eee4333da700000000cfe1acb5536f58c031d3d283f6b28c6a5ec623199fc3c1a0566452af58c4ccfb13","job_id":"246228154539130","target":"4a861b00"}}
{"method":"submit","params":{"id":"862725926260463","job_id":"246228154539130","nonce":"88030000","result":"193736d498976952b64024ec0a331fbb4cb25b70b3f049ebfdb1b8a49d670f00"},"id":1}
{"id":1,"jsonrpc":"2.0","error":null,"result":{"status":"OK"}}
{"method":"submit","params":{"id":"862725926260463","job_id":"246228154539130","nonce":"c6050000","result":"2d88e73d77d30a2433bc278c0e95ccd201072fd8228bdf1549128d4eddde0a00"},"id":1}
{"id":1,"jsonrpc":"2.0","error":null,"result":{"status":"OK"}}
{"jsonrpc":"2.0","method":"job","params":{"blob":"0606f0caedcf05fdd86cbe0f15bc3348d604fe35830c579edf14293facd6ea0ccfe3eee4333da70000000080b6cf10161e3dbeae53526958001e18e799232b1c5497829f922e772d2a76f713","job_id":"543452732195146","target":"e3380e00"}}
{"method":"submit","params":{"id":"862725926260463","job_id":"543452732195146","nonce":"17010000","result":"edc5c13d93b28620561c5a8f969fc0df30f8f4b6dafd11e749fe531aa6300200"},"id":1}
{"id":1,"jsonrpc":"2.0","error":null,"result":{"status":"OK"}}
{"jsonrpc":"2.0","method":"job","params":{"blob":"0606f0caedcf05fdd86cbe0f15bc3348d604fe35830c579edf14293facd6ea0ccfe3eee4333da700000000feb1a807a7690bfc5207eb5ab80741d918aadab53d2293237ce25f61c994dbc213","job_id":"148255726112984","target":"ce950700"}}
{"jsonrpc":"2.0","method":"job","params":{"blob":"0606a1ccedcf05ffcd054c320a4110c7468c4829f34dd84159522c9ba5e29cb9b1db57d855dde300000000b9978dcdfc7e40c8a7fa8305bb120b5c02e7eca365b2604fc70bc099f119112504","job_id":"753287914698012","target":"ce950700"}}
```

Which contains the flag in plaintext.
It turns out we could have just done `cat inputfile.pcapng | grep hitcon`.

`hitcon{BTC_is_so_expensive_$$$$$$$}`
