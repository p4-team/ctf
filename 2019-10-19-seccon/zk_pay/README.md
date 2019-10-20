# ZKPay (crypto?/web, 308p, 51 solved)

This turned out to be a rather confusing challenge.
We suspect that no-one actually solved it `the intended way`, which, we guess, involved some Zero-Knowledge Proofs.

In the task we can register on a webpage for money transfers.
We get initial transfer of 500 from the admin, and we need 1000000 to get the flag.
First obvious idea would be to simply register 20k accounts and transfer all the money to a single one, and judging by some organizers announcements, some teams tried that...

We guess that intended solution required figuring out how the signature for the transfer is generated, and forge a fake transfer of 1000000 from the admin.

However, the application had a major flaw with signed-unsigned comparison.
When doing a transfer the application did check if our account balance is `>=` of the value we want to send to someone.
But those values were signed!
It means we could simply transfer negative values and, of course, `500 > -1000000`, and the system would `deduct` this amount from our account via `500 - (-1000000)` effectively granting the money to us.

This way we get `SECCON{y0u_know_n07h1ng_3xcep7_7he_f4ct_th47_1_kn0w}`
