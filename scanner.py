import socket
import time
import platform

class WifiScanner:
    """فحص محلي محدود. لا ينفّذ تخمين كلمات مرور أو هجمات على الشبكات."""

    def scan_available_networks(self):
        # Android requires runtime permissions and OS services for Wi-Fi scans.
        # If pyjnius is unavailable (e.g. running on desktop), return a clear note.
        if platform.system().lower() != "linux":
            return [], "قراءة الشبكات الفعلية متاحة فقط داخل بناء Android المناسب."
        try:
            from jnius import autoclass
            PythonActivity = autoclass("org.kivy.android.PythonActivity")
            Context = autoclass("android.content.Context")
            activity = PythonActivity.mActivity
            wifi = activity.getApplicationContext().getSystemService(Context.WIFI_SERVICE)
            if wifi is None:
                return [], "لم يتمكن Android من إتاحة خدمة Wi-Fi."
            results = wifi.getScanResults()
            networks = []
            for item in results:
                caps = str(item.capabilities or "")
                security = self._security_from_caps(caps)
                networks.append({
                    "ssid": str(item.SSID or ""),
                    "bssid": str(item.BSSID or ""),
                    "signal_dbm": int(item.level),
                    "security": security,
                })
            if not networks:
                return [], (
                    "لم يُرجع Android أي شبكات. تحقق من أذونات الموقع/الأجهزة القريبة، "
                    "وتفعيل خدمات الموقع وWi-Fi. قد يقيّد النظام عمليات المسح المتكررة."
                )
            return networks, "النتائج من Android؛ قد تكون قديمة أو محدودة حسب الأذونات وإصدار النظام."
        except ImportError:
            return [], "واجهة Android غير متاحة في هذه البيئة. شغّل التطبيق بعد بنائه كـ APK."
        except Exception as exc:
            return [], (
                "تعذّر قراءة نتائج Wi-Fi من Android. تحقق من الأذونات وإعدادات النظام. "
                f"التفاصيل: {exc}"
            )

    @staticmethod
    def _security_from_caps(caps):
        c = caps.upper()
        if "WPA3" in c or "SAE" in c:
            return "WPA3 أو أحدث"
        if "WPA2" in c:
            return "WPA2"
        if "WPA" in c:
            return "WPA"
        if "WEP" in c:
            return "WEP"
        if not c or c == "[]":
            return "مفتوحة أو غير معروفة"
        return "غير معروف"

    def check_connectivity(self, host="1.1.1.1", port=53, timeout=3):
        start = time.perf_counter()
        try:
            with socket.create_connection((host, port), timeout=timeout):
                return round((time.perf_counter() - start) * 1000, 2)
        except OSError:
            return None
