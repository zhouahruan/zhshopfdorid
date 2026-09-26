package com.fdroid.m3store;

import android.os.Bundle;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import androidx.appcompat.app.AppCompatActivity;

public class MainActivity extends AppCompatActivity {
    private WebView webView;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        // Initialize iApp Runtime Web/UI Container
        webView = new WebView(this);
        webView.getSettings().setJavaScriptEnabled(true);
        webView.getSettings().setDomStorageEnabled(true);
        webView.setWebViewClient(new WebViewClient());

        // Load iApp M3UI app configuration & local interface
        setContentView(webView);
        webView.loadDataWithBaseURL("file:///android_asset/",
            "<html><body style='background:#FDFCFF;font-family:sans-serif;padding:20px;'>" +
            "<h2 style='color:#0061A4;'>F-Droid M3 Store</h2>" +
            "<p>iApp (裕语言) Android Container Initialized.</p>" +
            "<p>Software Source: 清华大学开源软件镜像站 (TUNA)</p>" +
            "</body></html>", "text/html", "UTF-8", null);
    }
}
