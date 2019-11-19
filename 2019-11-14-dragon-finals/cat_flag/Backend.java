import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.io.OutputStream;
import java.net.InetSocketAddress;
import java.util.List;
import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpHandler;
import com.sun.net.httpserver.HttpServer;
import com.sun.net.httpserver.Headers;

public class Backend {

    public static void main(String[] args) throws Exception {
        HttpServer server = HttpServer.create(new InetSocketAddress(8085), 0);
        server.createContext("/cat", new CatHandler());
        server.createContext("/flag", new FlagHandler());
        server.setExecutor(null);
        server.start();
    }

    public static String readFlag() throws Exception {
        BufferedReader reader = new BufferedReader(new FileReader("flag.txt"));
        String flag = reader.readLine();

        reader.close();

        return flag;
    }

    static class CatHandler implements HttpHandler {

        @Override
        public void handle(HttpExchange t) throws IOException {
            try {
                String response = getCat(getName(t)).toString();
                setHeaders(t);
                writeResponse(t, response);
            } catch (Exception e) {
                System.out.println(e);
                t.sendResponseHeaders(500, 0);
            } finally {
                t.close();
            }
        }

        private String getName(HttpExchange t) {
            String path = t.getRequestURI().getPath();
            return path.replaceFirst("^/cat", "");
        }

        private Integer getCat(String name) {
            return Math.abs(name.hashCode()) % 9;
        }
    }

    static class FlagHandler implements HttpHandler {

        @Override
        public void handle(HttpExchange t) throws IOException {
            try {
                String response = readFlag();
                setHeaders(t);
                writeResponse(t, response);
            } catch (Exception e) {
                System.out.println(e);
                t.sendResponseHeaders(500, 0);
            } finally {
                t.close();
            }
        }
    }

    private static void writeResponse(HttpExchange t, String response) throws IOException {
        t.sendResponseHeaders(200, response.length());
        OutputStream os = t.getResponseBody();
        os.write(response.getBytes());
        os.close();
    }

    private static void setHeaders(HttpExchange t) {
        if (canCloseConn(t)) {
            t.getResponseHeaders().set("Connection", "close");
        }
        t.getResponseHeaders().set("Content-Type", "text/plain");
    }

    private static boolean canCloseConn(HttpExchange t) {
        List<String> connectionHeaders = t.getRequestHeaders().get("Connection");
        if (connectionHeaders == null || (connectionHeaders.size() == 1 && connectionHeaders.get(0).toLowerCase() == "close")) {
            return true;
        }
        return false;
    }

}
