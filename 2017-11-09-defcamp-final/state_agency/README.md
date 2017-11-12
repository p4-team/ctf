# State agency (Web)

We get access to a webpage for reporting security vulnerabilities.
It seems basically nothing there works, apart from reading two existing reports.
Once we click on them we get a link with same GET parameters (which are ignored), but the interesting part is that the link is for example `http://5889.state-agency.tux.ro/` where `5589` is the ID of article we want to read.
If we change it to some random value we get information that our SQL is wrong.

Upon further inspection we figure out that in reality we simply need to change `Host` header to manipulate this value.
We guessed that there will be some SQL injection via the ID, but it seemed a lot of stuff was blacklisted by internal WAF and not knowing the query layout made this hard.
Eventually we managed to get some working injections.
Initally a blind one, based on 1 or 2 articles in the result, but eventually we noticed that `union select` is not blacklisted in WAF, so we could get a full echo of the query.

We could use the payload: `5880') union select 1,2,3,4,5 -- a` to get the union result.
The problem was that the injection point we had was already after the condition to select only the "public" vulnerabilities, and we could not change this condition any more.
We needed to make a new query using `union select`, but we don't know the table name.
The `information schema` was blacklisted in WAF, so were any other useful things.
Finally we found out that `procedure analyse` is not in the blacklist!

We could then send `5880') procedure analyse() -- a` and get back information that we're interested in the table `agency.articles` and the column most likely `content`.
But when sending `5880') union select 1,2,3,4,content from articles -- a` we get back `Private data exfiltration attempt blocked` so it seems the WAF checks if flag is in the response.
But this is not a problem, we can do: `5880') union select 1,2,3,4,to_base64(content) from articles -- a` to encode the flag and bypass the WAF.

Whole solver [here](sql.py)
