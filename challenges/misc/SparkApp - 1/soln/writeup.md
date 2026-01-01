# Solution
Use `apktool` to decompile the APK file and find the AndroidManifest.xml file. You should be able to see something like this:

```xml
...
<activity android:exported="true" android:label="SPARK{P3rm15510n5_f0r_1yf3}" android:name="com.sparkctf.sparkapp.FinalActivity" android:parentActivityName="com.sparkctf.sparkapp.SecretActivity"/>
...
```

Not really difficult for this challenge, you should be able to see that flag :).