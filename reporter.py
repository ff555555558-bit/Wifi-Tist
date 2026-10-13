import json
from datetime import datetime
from pathlib import Path

def _report_dir():
    # Use app-private storage, avoiding broad storage permissions on Android.
    try:
        from kivy.app import App
        app = App.get_running_app()
        if app and app.user_data_dir:
            path = Path(app.user_data_dir) / "reports"
            path.mkdir(parents=True, exist_ok=True)
            return path
    except Exception:
        pass
    path = Path.home() / "WifiAuditTool_reports"
    path.mkdir(parents=True, exist_ok=True)
    return path

def save_report(data):
    folder = _report_dir()
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    json_path = folder / f"wifi_audit_{stamp}.json"
    txt_path = folder / f"wifi_audit_{stamp}.txt"

    json_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        "Wi-Fi Audit Tool — تقرير فحص محلي",
        f"وقت التقرير: {data.get('generated_at', 'غير متاح')}",
        f"زمن الاتصال (ms): {data.get('connectivity_ms', 'لم يُختبر')}",
        "",
        "الشبكات:",
    ]
    networks = data.get("networks") or []
    if not networks:
        lines.append("لم تُسجّل شبكات. راجع رسالة حالة الفحص والأذونات.")
    for i, net in enumerate(networks, 1):
        lines.extend([
            f"{i}. SSID: {net.get('ssid') or '(اسم مخفي)'}",
            f"   BSSID: {net.get('bssid') or 'غير متاح'}",
            f"   الإشارة: {net.get('signal_dbm', 'غير متاح')} dBm",
            f"   الأمان: {net.get('security') or 'غير معروف'}",
        ])
    lines.extend(["", "ملاحظات:"])
    lines.extend(f"- {note}" for note in data.get("notes", []))
    txt_path.write_text("\n".join(lines), encoding="utf-8")
    return [str(json_path), str(txt_path)]
