import java.io.*;
import java.net.URLEncoder;
import java.nio.file.Files;
import java.net.InetSocketAddress;
import java.net.URI;
import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpHandler;
import com.sun.net.httpserver.HttpServer;
import org.apache.http.HttpEntity;
import org.apache.http.HttpResponse;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.ResponseHandler;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.impl.client.CloseableHttpClient;
import org.apache.http.impl.client.HttpClients;
import org.apache.http.util.EntityUtils;
import com.google.gson.Gson;

public class Frontend {

    private static Gson gson = new Gson();

    public static void main(String[] args) throws IOException {
        HttpServer server = HttpServer.create(new InetSocketAddress(8080), 0);
        server.createContext("/", new IndexHandler());
        server.createContext("/cats", new CatsHandler());
        server.createContext("/static", new StaticHandler());
        server.setExecutor(null);
        server.start();
    }

    static class CatsHandler implements HttpHandler {
        private class Req {
            public String[] names;
        }

        @Override
        public void handle(HttpExchange t) throws IOException {
            try {
                String body = getBody(t);
                Req req = gson.fromJson(body, Req.class);
                if (req.names.length > 5) {
                    t.sendResponseHeaders(400, 0);
                    return;
                }

                String traceId = getTraceId(t);
                String[] cats = getCats(req.names, traceId);

                String response = gson.toJson(cats);
                t.getResponseHeaders().set("Content-Type", "application/json");
                t.sendResponseHeaders(200, response.length());
                OutputStream os = t.getResponseBody();
                os.write(response.getBytes());
                os.close();
            } catch (Exception e) {
                System.out.println(e);
                t.sendResponseHeaders(500, 0);
            } finally {
                t.close();
            }
        }

        private String getBody(HttpExchange t) throws IOException {
            StringBuilder sb = new StringBuilder();
            InputStream ios = t.getRequestBody();
            int i;
            while ((i = ios.read()) != -1) {
                sb.append((char) i);
            }
            return sb.toString();
        }

        private String getTraceId(HttpExchange t) {
            String query = t.getRequestURI().getQuery();
            return query.replaceFirst("^traceId=", "");
        }

        private String[] getCats(String[] names, String trace) throws Exception {
            CloseableHttpClient httpclient = HttpClients.createDefault();
            ResponseHandler<String> responseHandler = new ResponseHandler<String>() {
                @Override
                public String handleResponse(final HttpResponse response) throws IOException {
                    return EntityUtils.toString(response.getEntity());
                }
            };
            try {
                String[] cats = new String[names.length];
                for (int i = 0; i < names.length; i++) {
                    String name = names[i].trim();
                    URI url = new URI("http://localhost:8085/cat/" + URLEncoder.encode(name, "UTF-8"));
                    HttpGet httpget = new HttpGet(url);
                    httpget.setHeader("X-Trace", trace);
                    String response = httpclient.execute(httpget, responseHandler);
                    cats[i] = response;
                }
                return cats;
            } finally {
                httpclient.close();
            }
        }
    }

    static class IndexHandler implements HttpHandler {

        @Override
        public void handle(HttpExchange t) throws IOException {
            try {
                File file = new File("index.html");
                t.getResponseHeaders().set("Content-Type", "text/html");
                t.sendResponseHeaders(200, file.length());
                OutputStream os = t.getResponseBody();
                Files.copy(file.toPath(), os);
                os.close();
            } catch (Exception e) {
                System.out.println(e);
                t.sendResponseHeaders(500, 0);
            } finally {
                t.close();
            }
        }
    }

    static class StaticHandler implements HttpHandler {
        @Override
        public void handle(HttpExchange t) throws IOException {
            try {
                Integer catNumber = getCatNumber(t);
                String filePath = "static/" + catNumber.toString() + ".jpg";
                File file = new File(filePath);
                t.getResponseHeaders().set("Content-Type", "image/jpeg");
                t.sendResponseHeaders(200, file.length());
                OutputStream os = t.getResponseBody();
                Files.copy(file.toPath(), os);
                os.close();
            } catch (Exception e) {
                System.out.println(e);
                t.sendResponseHeaders(500, 0);
            } finally {
                t.close();
            }
        }
        private Integer getCatNumber(HttpExchange t) throws Exception {
            String path = t.getRequestURI().getPath();
            Integer n = Integer.valueOf(path.replaceFirst("^/static/", ""));
            if (n < 0 || n > 8) {
                throw new Exception("out of catnip");
            }
            return n;
        }

    }


}
