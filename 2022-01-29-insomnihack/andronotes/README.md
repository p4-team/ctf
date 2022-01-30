# AndroNotes

> Our Forensic experts dumped the mobile device of a criminal, can you identify what the thugs are up to...

We get a 3.5GB dump of a flash memory of an Android device with a task of retrieving an encrypted note. After a while of
looking at installed applications we take an even closer look at the "Safe Notes - Secure Ad-free notepad"
(com.protectedtext.android) app and, especially, it's stored data at
`/dump/data/data/com.protectedtext.android/`:
```
./databases
./databases/notes_db_name-journal
./databases/google_app_measurement_local.db-journal
./databases/google_app_measurement_local.db
./databases/notes_db_name
./shared_prefs
./shared_prefs/com.google.android.gms.appid.xml
./shared_prefs/com.protectedtext.n2.xml
./shared_prefs/com.google.android.gms.measurement.prefs.xml
./shared_prefs/com.protectedtext.lon.xml
./shared_prefs/com.crashlytics.sdk.android:answers:settings.xml
./shared_prefs/remoteConfigPrefs.xml
./shared_prefs/com.google.firebase.remoteconfig_legacy_settings.xml
./shared_prefs/frc_1:169956459094:android:8d67c78e1c4facc6_firebase_settings.xml
./shared_prefs/com.protectedtext.android_preferences.xml
./shared_prefs/TwitterAdvertisingInfoPreferences.xml
./shared_prefs/com.crashlytics.prefs.xml
```

At first, we looked into the `./databases/notes_db_name` file, which is a sqlite database.

```
$ sqlite3 ./databases/notes_db_name
SQLite version 3.31.1 2020-01-27 19:55:54
Enter ".help" for usage hints.
sqlite> .schema
CREATE TABLE android_metadata (locale TEXT);
CREATE TABLE Notes (ID_COLUMN integer primary key autoincrement, NOTE_CONTENT_COLUMN text, LAST_TIME_MODIFIED_COLUMN integer, IS_ENCRYPTED_COLUMN integer, INIT_CONTENT_HASH_COLUMN text, EXPECTED_DB_VERSION_COLUMN integer, LAST_SELECTED_TAB_INDEX_COLUMN integer, PASSWORD_COLUMN text, URL_COLUMN text );
CREATE TABLE sqlite_sequence(name,seq);
```

It's schema was very promising, but...

```
sqlite> select * from Notes;
sqlite> 
```

... the database was empty.

Then we looked at shared_prefs and especially the `./shared_prefs/com.protectedtext.n2.xml` file that turned out
to have a base64-encoded high-entropy data, possibly an encrypted note.
```
$ cat shared_prefs/com.protectedtext.n2.xml 
<?xml version='1.0' encoding='utf-8' standalone='yes' ?>
<map>
    <string name="a">U2FsdGVkX19c/zcgG/UScI+1bKvOvunZUy6Ck1FB/dxMD+BGQLAAkEVufV1+skdK5cyCFqnw2WTY546XgOGnD11WLjg1N0RbbeotynkRGGKFZ3XAMQQUk7v08mBs8IYVISRxSzktd9HgT4cCAjtvWgpYytz9y7Tb4hF1x8plEb114yaWfNspk4XmLqUyssVnyIhqBXDmmIEFVudV+EQsOkYcBW5S1GINEBLqV6lxLKHSTlwWej2Y+TpC1mOAScmIs6NAyquw7ow2oYpqDBC6SB5dslgHYeV9YoCv+evP+lQdmCTf+88VvT001MnUHtgTFnsRcZR1rCmZp2EXNQArCH/onRSAE2ehGPv2NIfsnljeSfg7jO12zkRqf1q22SLtFpHL8OLKjrfvpcY5yRIm1H1vkYRDewYlku6r/WoESpBfAvl8/VKmkrsPfp1JjKLuO3mDOuv5CmE7HBmT3etR5b1WEL78nizxtkj4wFKyY2I4SuHmsNFANZdxMsdpZImYpB6pG0i5ifMGiesjThvTQU8pblQ2XQSrNuqpTtjwXvk=</string>
</map>
```

Now's the time to finally look into the application itself. We've downloaded an APK and decompiled its code.

We started with `com.protectedtext.android` package and quickly ran into the `a.c.b()` method with a string suggesting
it might deal with the aforementioned shared prefs file:
```java
public JSONObject b(long j) {
    Context applicationContext = PtApplication.b().getApplicationContext();
    String string = applicationContext.getSharedPreferences("com.protectedtext.n" + j, 0).getString("a", (String) null);
    if (string == null) {
        f.a((Throwable) new IllegalStateException("Note xml file exists, but no keys inside!"));
    }
    try {
        return new JSONObject(e.a(string, f3128b + j));
    } catch (JSONException e) {
        f.a((Throwable) e);
        throw new RuntimeException(e);
    }
}
```

The `e.a` method it invokes when creating the JSONObject looks like a decryption function:

```java
public static String a(String str, String str2) {
    try {
        byte[] decode = Base64.decode(str, 0);
        byte[] bArr = new byte[8];
        byte[] bArr2 = new byte[(decode.length - 16)];
        System.arraycopy(decode, 8, bArr, 0, 8);
        System.arraycopy(decode, 16, bArr2, 0, bArr2.length);
        MessageDigest instance = MessageDigest.getInstance("MD5");
        byte[] a2 = a(str2.getBytes(), bArr);
        byte[] digest = instance.digest(a2);
        byte[] digest2 = instance.digest(a(digest, a2));
        byte[] digest3 = instance.digest(a(digest2, a2));
        SecretKeySpec secretKeySpec = new SecretKeySpec(a(digest, digest2), "AES");
        IvParameterSpec ivParameterSpec = new IvParameterSpec(digest3);
        Cipher instance2 = Cipher.getInstance("AES/CBC/PKCS5Padding");
        instance2.init(2, secretKeySpec, ivParameterSpec);
        return new String(instance2.doFinal(bArr2), "UTF-8");
    } catch {
        ... error handling ...
    }
}
```

It takes base64-encoded data and a key. Conveniently it's just a static key constructed from a few strings:
```java
StringBuilder sb = new StringBuilder();
sb.append("7igb2h048io6fyv");
sb.append(Math.random() > -1.0d ? "8h92q3ruag" : "98hasdfil");
sb.append("09g8h");
f3128b = sb.toString();
```

Copying all that code into a new Java project and passing the base64-encoded data we've found in the shared prefs
along with the static key to the decryption function gives us the note contents and the flag:

```json
{"id":2,"content":"Operation Secret:\nINS{P1n_L0c4l_AuTh3nT1c4t10N_1s_4asY}\nf47c13a09bfcad9eb1f81fbf12c04516e0d900e409a74c660f933e69cf93914e16bc9facc7d379a036fe71468bd4504f2a388a0a28a9b727a38ab7843203488c♻ Reload this website to hide mobile app metadata! ♻{\"version\":1,\"color\":-1118482}","ordering_time":1640170640052,"is_encrypted":false,"expected_db_ver":2,"selected_tab_index":0}
```

The application description on Google Play also suggests that the app uses a user-provided PIN to protect user's data,
but we guess it only blocks the UI.