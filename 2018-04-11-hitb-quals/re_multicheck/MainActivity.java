package com.p020a.multicheck;

import android.os.Bundle;
import android.support.v7.app.C0326c;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.EditText;
import android.widget.Toast;
import com.a.multicheck.R;
import dalvik.system.DexClassLoader;
import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;

public class MainActivity extends C0326c {
    private String f1763l;

    static {
        System.loadLibrary("check");
    }

    private void m2541i() {
        FileOutputStream fileOutputStream;
        InputStream inputStream = null;
        File file = new File(getFilesDir().getAbsolutePath());
        if (!file.exists()) {
            file.mkdirs();
        }
        File file2 = new File(file, "claz.dex");
        try {
            InputStream open = getAssets().open("claz.dex");
            try {
                fileOutputStream = new FileOutputStream(file2);
                try {
                    byte[] bArr = new byte[1024];
                    while (true) {
                        int read = open.read(bArr);
                        if (read <= 0) {
                            break;
                        }
                        fileOutputStream.write(bArr, 0, read);
                    }
                    open.close();
                    fileOutputStream.close();
                } catch (Exception e) {
                    inputStream = open;
                    if (inputStream != null) {
                        try {
                            inputStream.close();
                        } catch (IOException e2) {
                            e2.printStackTrace();
                        }
                    }
                    if (fileOutputStream != null) {
                        try {
                            fileOutputStream.close();
                        } catch (IOException e3) {
                            e3.printStackTrace();
                        }
                    }
                    this.f1763l = file2.getAbsolutePath();
                }
            } catch (Exception e4) {
                fileOutputStream = null;
                inputStream = open;
                if (inputStream != null) {
                    inputStream.close();
                }
                if (fileOutputStream != null) {
                    fileOutputStream.close();
                }
                this.f1763l = file2.getAbsolutePath();
            }
        } catch (Exception e5) {
            fileOutputStream = null;
            if (inputStream != null) {
                inputStream.close();
            }
            if (fileOutputStream != null) {
                fileOutputStream.close();
            }
            this.f1763l = file2.getAbsolutePath();
        }
        this.f1763l = file2.getAbsolutePath();
    }

    protected void onCreate(Bundle bundle) {
        ReflectiveOperationException e;
        final EditText editText;
        Method method = null;
        super.onCreate(bundle);
        setContentView((int) R.layout.activity_main);
        m2541i();
        String str = getFilesDir().getAbsolutePath() + File.separator + "out";
        File file = new File(str);
        if (!file.exists()) {
            file.mkdirs();
        }
        DexClassLoader dexClassLoader = new DexClassLoader(this.f1763l, str, null, getClassLoader());
        new File(this.f1763l).delete();
        try {
            method = dexClassLoader.loadClass("com.a.Check").getMethod("check", new Class[]{String.class});
        } catch (ClassNotFoundException e2) {
            e = e2;
            e.printStackTrace();
            editText = (EditText) findViewById(R.id.edit_text);
            findViewById(R.id.button).setOnClickListener(new OnClickListener(this) {
                final /* synthetic */ MainActivity f1762d;

                public void onClick(View view) {
                    try {
                        if (((Boolean) method.invoke(null, new Object[]{editText.getText().toString()})).booleanValue()) {
                            Toast.makeText(this, "YES, you get it~", 0).show();
                            return;
                        }
                    } catch (IllegalAccessException e) {
                    } catch (InvocationTargetException e2) {
                    }
                    Toast.makeText(this, "Sorry, you are wrong", 0).show();
                }
            });
        } catch (NoSuchMethodException e3) {
            e = e3;
            e.printStackTrace();
            editText = (EditText) findViewById(R.id.edit_text);
            findViewById(R.id.button).setOnClickListener(/* anonymous class already generated */);
        }
        editText = (EditText) findViewById(R.id.edit_text);
        findViewById(R.id.button).setOnClickListener(/* anonymous class already generated */);
    }
}
