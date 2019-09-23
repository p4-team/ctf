# rms, Web / Pwning, 365p
> Difficulty: medium (13 solvers)
>
> I generally do not connect to web sites from my own machine, aside from a few sites I have some special relationship with. I usually fetch web pages from other sites by sending mail to a program that fetches them, much like wget, and then mails them back to me.
> ~ Richard Stallman
>
> Flag is at http://127.0.0.1:8000/flag

In this task we are given a binary and IP running this service. 
When connected, we can ask it to connect to any HTTP domain and port, and get the response - localhost, where flag is hosted,
is filtered though.

The binary uses `gethostbyname2` function to resolve domains, which is not thread safe - and the app uses multiple threads to queue the requests.
The lack of thread safety comes from the fact that there is only one single global variable for the results.
Every time you call `gethostbyname2` the returned pointer points to the same memory location.
This means any time you call this function it will overwrite the previous results!

The important function to look at is `fetch`:

```c
  uVar2 = htons(local_11c);
  phVar4 = gethostbyname2(local_118,10);
  lVar7 = 0x10;
  puVar8 = &local_98;
  while (lVar7 != 0) {
    lVar7 = lVar7 + -1;
    *puVar8 = 0;
    puVar8 = puVar8 + (ulong)bVar9 * 0x1ffffffffffffffe + 1;
  }
  if (phVar4 != (hostent *)0x0) {
    if (phVar4->h_addrtype != 10) {
                /* WARNING: Subroutine does not return */
      __assert_fail("hent6->h_addrtype == AF_INET6","task/main.c",0x95,"fetch");
    }
    local_98 = 10;
    uStack136 = *(undefined8 *)(*phVar4->h_addr_list + 1);
    uStack144 = *(undefined8 *)*phVar4->h_addr_list;
    uStack150 = uVar2;
    iVar3 = memcmp(&uStack144,in6addr_loopback,0x10);
    if ((iVar3 == 0) || ((char)uStack144 == 0)) {
      local_b0 = "localhost not allowed";
      goto LAB_00101de7;
    }
  }
  phVar5 = gethostbyname2(local_118,2);
  if (phVar5 != (hostent *)0x0) {
    if (phVar5->h_addrtype != 2) {
                /* WARNING: Subroutine does not return */
      __assert_fail("hent4->h_addrtype == AF_INET","task/main.c",0xa0,"fetch");
    }
    if ((**phVar5->h_addr_list == 0x7f) || (**phVar5->h_addr_list == 0)) {
      local_b0 = "localhost not allowed";
      goto LAB_00101de7;
    }
  }
  if ((phVar4 != (hostent *)0x0) &&
     (cVar1 = make_request(&local_98,0x80,local_118,local_108,&local_b0,&local_a8), cVar1 !=0))
  goto LAB_00101e07;
  if (phVar5 == (hostent *)0x0) {
    piVar6 = __h_errno_location();
    local_b0 = hstrerror(*piVar6);
  }
  else {
    local_98 = 2;
    uStack148 = *(undefined4 *)*phVar5->h_addr_list;
    uStack150 = uVar2;
    cVar1 = make_request(&local_98,0x80,local_118,local_108,&local_b0,&local_a8);
    if (cVar1 != 0) goto LAB_00101e07;
  }
```

The flow for each thread is as follows:

1. Use `gethostbyname2` on given domain asking for IPv6 address. If we got response and it is in fact IPv6 then check if it's not localhost and fail if it is. The pointer from 
2. Use `gethostbyname2` on given domain asking for IPv4 address. If we got response and it is in fact IPv4 then check if it's not localhost and fail if it is.
3. If address check for IPv6 succeeded then make request to returned address.
4. If the request to IPv6 failed then check the result from IPv4 address check.
5. If IPv4 check succeeded then make IPv4 request to the returned address.

This creates a race condition between the threads, because they will overwrite the results of `gethostbyname2`.
Initially we were trying to win the race after `if ((**phVar5->h_addr_list == 0x7f) || (**phVar5->h_addr_list == 0))` with one thread passing this condition and another thread requesting localhost, before the first thread reaches `make_request` call.
However, this proved to be difficult to actually trigger.

Fortunately one of our players noticed an easier way to do this, with a nice synchronized approach.
He noticed that we can block one of the threads on the request, and thus give the necessary time for the second thread to request localhost, and overwrite the data, before the first thread moves further to making IPv4 request.

The idea is:

* Thread 1: request http://foo.com:8000/flag (where this domain record has IPv6 and IPv4 non localhost address) wait for it to connect through IPv6
* Thread 2: request http://localhost:8000/flag, and fail
* Thread 1: IPv6 times out or does not connect, connects to IPv4 which is overwritten by thread 1 to point to localhost. 

The connection timeout was set to 10s, so we have plenty of time before the first thread fails the IPv6 connection and proceeds to make IPv4 request.

Once we do this in the results of Thread 1 we have the flag: `DrgnS{e9759caf4f2d2b69773c}`
