from datetime import datetime
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup

from scanner import WifiScanner
from reporter import save_report

KV = """
<RootUI>:
    orientation: "vertical"
    padding: "14dp"
    spacing: "10dp"
    canvas.before:
        Color:
            rgba: (0.055, 0.09, 0.15, 1)
        Rectangle:
            pos: self.pos
            size: self.size
    Label:
        text: "[b]Wi-Fi Audit Tool[/b]"
        markup: True
        font_size: "24sp"
        size_hint_y: None
        height: "46dp"
        color: (0.35, 0.8, 1, 1)
    Label:
        text: "فحص محلي وآمن — بدون Root وبدون محاولة اختراق الشبكات"
        font_size: "14sp"
        size_hint_y: None
        height: "44dp"
        color: (0.9, 0.93, 0.98, 1)
        halign: "center"
        text_size: self.width, None
    Button:
        text: "فحص شبكات Wi-Fi القريبة"
        size_hint_y: None
        height: "48dp"
        on_release: app.scan_wifi()
    Button:
        text: "اختبار اتصال الإنترنت"
        size_hint_y: None
        height: "44dp"
        on_release: app.test_connection()
    Button:
        text: "تصدير التقرير"
        size_hint_y: None
        height: "44dp"
        on_release: app.export_report()
    ScrollView:
        do_scroll_x: False
        Label:
            id: output
            text: "جاهز. اضغط على أحد الأزرار لبدء الفحص."
            size_hint_y: None
            height: self.texture_size[1] + dp(24)
            text_size: self.width - dp(20), None
            halign: "right"
            valign: "top"
            color: (0.92, 0.95, 1, 1)
            markup: True
"""

class RootUI(BoxLayout):
    pass

class WifiAuditApp(App):
    def build(self):
        self.title = "Wi-Fi Audit Tool"
        self.scanner = WifiScanner()
        self.last_report = {
            "generated_at": datetime.now().isoformat(timespec="seconds"),
            "networks": [],
            "connectivity_ms": None,
            "notes": ["لا تنفّذ الأداة تخمين كلمات مرور أو قطع اتصال أو دخولاً غير مصرّح به."]
        }
        Builder.load_string(KV)
        self.root_ui = RootUI()
        return self.root_ui

    def show_text(self, text):
        self.root_ui.ids.output.text = text

    def scan_wifi(self):
        try:
            networks, note = self.scanner.scan_available_networks()
            self.last_report["networks"] = networks
            self.last_report["generated_at"] = datetime.now().isoformat(timespec="seconds")
            if networks:
                lines = ["[b]الشبكات التي أعادها نظام Android:[/b]"]
                for i, net in enumerate(networks, 1):
                    lines.append(
                        f"{i}. [b]{net.get('ssid') or '(اسم مخفي)'}[/b]\\n"
                        f"   BSSID: {net.get('bssid') or 'غير متاح'} | "
                        f"الإشارة: {net.get('signal_dbm', 'غير متاح')} dBm | "
                        f"الأمان: {net.get('security') or 'غير معروف'}"
                    )
                lines.append("\\n" + note)
                self.show_text("\\n".join(lines))
            else:
                self.show_text("[b]لم يتم إرجاع شبكات.[/b]\\n" + note)
        except Exception as exc:
            self.show_text("تعذّر إكمال الفحص: " + str(exc))

    def test_connection(self):
        latency = self.scanner.check_connectivity()
        self.last_report["connectivity_ms"] = latency
        if latency is None:
            self.show_text("تعذّر الاتصال بعنوان الاختبار على المنفذ 53. قد يكون الإنترنت غير متاح أو الاتصال محجوباً.")
        else:
            self.show_text(f"زمن إنشاء الاتصال: [b]{latency} ms[/b]\\nهذا اختبار اتصال بسيط وليس قياساً شاملاً لسرعة الإنترنت.")

    def export_report(self):
        try:
            paths = save_report(self.last_report)
            self.show_text("تم حفظ التقرير داخل مساحة التطبيق:\\n" + "\\n".join(paths) +
                           "\\n\\nقد لا يظهر الملف في مجلد التنزيلات بسبب قيود Android.")
        except Exception as exc:
            self.show_text("تعذّر حفظ التقرير: " + str(exc))

if __name__ == "__main__":
    WifiAuditApp().run()
