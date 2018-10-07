# Who knows john dows? (web, 416p, 24 solved)

In the challenge we get link to github repo: https://github.com/h18johndoe/user_repository/blob/master/user_repo.rb

And link to page where we can test this login form.
It's clear that there is SQLinjection in the code, but in order to use it, we need to first get past the check for existing users.

We do this by checking emails of the people who contributed to the github repo, and we get a matching email: `john_doe@flow.go` which is recognized by the page.

Now we can provide password.
The trick is to notice that password we provide is "hashed" be simply reversing it, and only then pasted into the query.
This means we can use classic `dupa' or '1'='1` but we need to invert it to `1'='1' ro 'aa` so that after "hashing" it forms a proper injection query.

Once we do this we get logged in and flag is there: ` hackover18{I_KN0W_H4W_70_STALK_2018}`
