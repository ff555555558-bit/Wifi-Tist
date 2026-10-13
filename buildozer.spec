[app]
title = Wi-Fi Audit Tool
package.name = wifiaudittool
package.domain = org.xabur
source.dir = .
source.include_exts = py,kv,txt,md
version = 1.0.0
requirements = python3,kivy,pyjnius
orientation = portrait
fullscreen = 0

# Android permissions needed for displaying nearby Wi-Fi scan results.
android.permissions = INTERNET,ACCESS_WIFI_STATE,CHANGE_WIFI_STATE,ACCESS_FINE_LOCATION,ACCESS_COARSE_LOCATION,NEARBY_WIFI_DEVICES
android.api = 35
android.minapi = 23
android.archs = arm64-v8a
android.allow_backup = False

[buildozer]
log_level = 2
warn_on_root = 1
