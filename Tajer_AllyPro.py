# ba_meta require api 9
# BSLIFE Ally Manager — v11.1 STABLE
# Made with Tajer · @Tajerbetbot · api 9 · Free

from __future__ import annotations

import babase
import bauiv1 as bui
import bascenev1 as bs
from bauiv1lib import party

import colorsys
import http.cookiejar
import json
import math
import os
import random
import ssl
import threading
import time
import urllib.error
import urllib.request

# ═══════════════════════════════════════════════════════════════
# CONFIG
# ═══════════════════════════════════════════════════════════════

BASE_URL = "https://bslife.ir"
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".bslife_ally")
os.makedirs(DATA_DIR, exist_ok=True)
SESSION_FILE = os.path.join(DATA_DIR, "session.json")
LOG_FILE = os.path.join(DATA_DIR, "bslife_debug.log")

CHANNEL_NAME = "Tajer"
CHANNEL_HANDLE = "@Tajerbetbot"
CHANNEL_URL = "https://t.me/Tajerbetbot"

MyCall = getattr(bui, 'CallPartial', bui.Call)

def _safe_timer(delay, call, repeat=False):
    """Reliable timer that works on all BombSquad versions."""
    try:
        if repeat:
            return bs.AppTimer(delay, call, repeat=True)
        return bs.AppTimer(delay, call)
    except Exception:
        try:
            if repeat:
                return bui.apptimer(delay, call, repeat=True)
            return bui.apptimer(delay, call)
        except Exception:
            try:
                call()
            except Exception:
                pass
            return None


# ═══════════════════════════════════════════════════════════════
# LANGUAGE
# ═══════════════════════════════════════════════════════════════

def _is_fa():
    try:
        return bui.app.lang.language in ("Persian", "fa", "Farsi")
    except Exception:
        return False

IS_FA = _is_fa()

T = {
    "login": {"fa": "ورود", "en": "Login"},
    "logout": {"fa": "خروج", "en": "Logout"},
    "cancel": {"fa": "انصراف", "en": "Cancel"},
    "overview": {"fa": "مرور", "en": "Overview"},
    "members": {"fa": "اعضا", "en": "Members"},
    "requests": {"fa": "درخواست‌ها", "en": "Requests"},
    "vault": {"fa": "خزانه", "en": "Vault"},
    "settings": {"fa": "تنظیمات", "en": "Settings"},
    "ranking": {"fa": "رنکینگ", "en": "Ranking"},
    "chat": {"fa": "چت", "en": "Chat"},
    "news": {"fa": "اخبار", "en": "News"},
    "channels": {"fa": "کانال", "en": "Channel"},
    "manage": {"fa": "مدیریت", "en": "Manage"},
    "title": {"fa": "عنوان", "en": "Title"},
    "color": {"fa": "رنگ", "en": "Color"},
    "apply_title": {"fa": "اعمال عنوان", "en": "Apply Title"},
    "role": {"fa": "نقش", "en": "Role"},
    "change_role": {"fa": "تغییر نقش", "en": "Change Role"},
    "mute": {"fa": "سکوت", "en": "Mute"},
    "unmute": {"fa": "رفع سکوت", "en": "Unmute"},
    "kick": {"fa": "اخراج", "en": "Kick"},
    "leader": {"fa": "لیدر", "en": "Leader"},
    "general": {"fa": "جنرال", "en": "General"},
    "spy": {"fa": "جاسوس", "en": "Spy"},
    "member": {"fa": "عضو", "en": "Member"},
    "deposit": {"fa": "واریز", "en": "Deposit"},
    "split": {"fa": "تقسیم", "en": "Split"},
    "capacity": {"fa": "ظرفیت", "en": "Capacity"},
    "buy": {"fa": "خرید", "en": "Buy"},
    "new": {"fa": "جدید", "en": "New"},
    "accepted": {"fa": "تایید", "en": "Accepted"},
    "rejected": {"fa": "رد", "en": "Rejected"},
    "yes": {"fa": "بله", "en": "Yes"},
    "no": {"fa": "نه", "en": "No"},
    "ready": {"fa": "آماده", "en": "Ready"},
    "loading": {"fa": "در حال لود", "en": "Loading"},
    "expired": {"fa": "سشن منقضی", "en": "Session expired"},
    "recovering": {"fa": "در حال بازیابی", "en": "Recovering"},
    "not_ranked": {"fa": "رتبه‌بندی نشده", "en": "Not ranked"},
    "ally_name": {"fa": "نام اتحاد", "en": "Alliance"},
    "your_role": {"fa": "نقش شما", "en": "Your Role"},
    "members_count": {"fa": "تعداد اعضا", "en": "Members"},
    "coins": {"fa": "سکه", "en": "Coins"},
    "message": {"fa": "پیام", "en": "Message"},
    "send": {"fa": "ارسال", "en": "Send"},
    "fill_all": {"fa": "همه فیلدها را پر کنید", "en": "Fill all fields"},
    "logging_in": {"fa": "ورود", "en": "Logging in"},
    "success_load": {"fa": "موفق", "en": "Success"},
    "error": {"fa": "خطا", "en": "Error"},
    "hub": {"fa": "مرکز اتحاد", "en": "Alliance Hub"},
    "no_ally": {"fa": "بدون اتحاد", "en": "Not in ally"},
    "create": {"fa": "ساخت", "en": "Create"},
    "join": {"fa": "پیوستن", "en": "Join"},
    "search": {"fa": "جستجو", "en": "Search"},
    "cost": {"fa": "هزینه", "en": "Cost"},
    "user": {"fa": "کاربر", "en": "User"},
    "req_sent": {"fa": "درخواست ارسال شد", "en": "Request sent"},
    "ok": {"fa": "باشه", "en": "OK"},
    "request": {"fa": "درخواست", "en": "Request"},
    "confirm": {"fa": "تایید", "en": "Confirm"},
    "success": {"fa": "موفق", "en": "Success"},
    "fail": {"fa": "ناموفق", "en": "Failed"},
    "enter_amount": {"fa": "مقدار", "en": "Amount"},
    "equal_all": {"fa": "مساوی همه", "en": "Equal all"},
    "equal_top": {"fa": "مساوی ۲۰ برتر", "en": "Equal top 20"},
    "by_points": {"fa": "با امتیاز", "en": "By points"},
    "remove_role": {"fa": "حذف نقش", "en": "Remove role"},
    "already_ally": {"fa": "در اتحادی", "en": "Already in ally"},
    "no_coins": {"fa": "سکه کم", "en": "Not enough"},
    "select": {"fa": "انتخاب", "en": "Select"},
    "vault_ok": {"fa": "خزانه تقسیم شد", "en": "Split OK"},
    "deposit_ok": {"fa": "واریز شد", "en": "Deposited"},
    "role_changed": {"fa": "نقش تغییر کرد", "en": "Role changed"},
    "leave": {"fa": "خروج از اتحاد", "en": "Leave Ally"},
    "leave_confirm": {"fa": "مطمئنید؟", "en": "Are you sure?"},
    "vault_hist": {"fa": "تاریخچه خزانه", "en": "Vault History"},
    "shares": {"fa": "سهام", "en": "Shares"},
    "history": {"fa": "تاریخچه", "en": "History"},
    "more": {"fa": "بیشتر", "en": "More"},
    "no_news": {"fa": "خبری نیست", "en": "No news"},
    "gkick": {"fa": "حد جنرال", "en": "General Kick Limit"},
    "spynet": {"fa": "بودجه Spynet", "en": "Spynet Budget"},
    "tag": {"fa": "وضعیت تگ", "en": "Tag Status"},
    "active": {"fa": "فعال", "en": "Active"},
    "inactive": {"fa": "غیرفعال", "en": "Inactive"},
    "price": {"fa": "قیمت فروش", "en": "Sale Price"},
    "enrol": {"fa": "تنظیمات عضوگیری", "en": "Enrolment"},
    "direct": {"fa": "مستقیم", "en": "Direct"},
    "reqmode": {"fa": "درخواستی", "en": "Request"},
    "closed": {"fa": "بسته", "en": "Closed"},
    "min_coin": {"fa": "حداقل سکه", "en": "Min Coins"},
    "top": {"fa": "رتبه تاپ", "en": "Required Top"},
    "score": {"fa": "حداقل امتیاز", "en": "Min Score"},
    "saved": {"fa": "ذخیره شد", "en": "Saved"},
    "rank_by": {"fa": "رتبه", "en": "Rank"},
    "newest": {"fa": "جدیدترین", "en": "Newest"},
    "oldest": {"fa": "قدیمی‌ترین", "en": "Oldest"},
    "most": {"fa": "بیشترین", "en": "Most"},
    "style": {"fa": "تم", "en": "Style"},
    "set": {"fa": "تنظیم", "en": "Set"},
    "change": {"fa": "تغییر", "en": "Change"},
    "forced": {"fa": "اجباری", "en": "Forced"},
    "off": {"fa": "خاموش", "en": "Off"},
    "bot": {"fa": "ربات تلگرام", "en": "Telegram Bot"},
    "join_mode": {"fa": "حالت ورود", "en": "Join Mode"},
    "not_set": {"fa": "تنظیم نشده", "en": "Not set"},
    "role_full": {"fa": "ظرفیت نقش پر", "en": "Role full"},
    "no_bot": {"fa": "بدون بات", "en": "No bot"},
    "empty": {"fa": "خالی", "en": "Empty"},
    "username": {"fa": "اسم خاص", "en": "Username"},
    "otp": {"fa": "کد لاگین", "en": "OTP"},
    "login_h1": {"fa": "• در چت بازی تایپ کنید: login", "en": "• In-game chat: login"},
    "login_h2": {"fa": "• یا در @BslifeBot: login", "en": "• Or @BslifeBot: login"},
    "login_sub": {"fa": "مدیریت اتحاد در بازی", "en": "Manage your ally in-game"},
    "no_data": {"fa": "داده‌ای نیست", "en": "No data"},
    "amount_hint": {"fa": "مقدار سکه...", "en": "Coins amount..."},
    "search_hint": {"fa": "جستجوی اتحاد...", "en": "Search ally..."},
    "name_hint": {"fa": "نام اتحاد...", "en": "Ally name..."},
    "msg_hint": {"fa": "پیام...", "en": "Message..."},
    "left_recent": {"fa": "اخیراً خارج شده‌اید", "en": "Recently left"},
    "pending": {"fa": "در انتظار", "en": "Pending"},
    "req_rejected": {"fa": "قبلاً رد شده", "en": "Previously rejected"},
    "no_req": {"fa": "شرایط را ندارید", "en": "Requirements not met"},
    "needed": {"fa": "نیازمندی‌ها", "en": "Requirements"},
    "open": {"fa": "باز کردن", "en": "Open"},
    "closing": {"fa": "در حال بستن", "en": "Closing"},
}

def L(key):
    return T.get(key, {}).get("fa" if IS_FA else "en", key)


# ═══════════════════════════════════════════════════════════════
# LOGGING
# ═══════════════════════════════════════════════════════════════

def log(msg):
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {msg}\n")
    except Exception:
        pass

def fmt(n):
    try:
        return f"{int(n):,}"
    except Exception:
        return str(n)

def role_name(rid):
    return L({1: "leader", 2: "general", 3: "spy"}.get(rid, "member"))


# ═══════════════════════════════════════════════════════════════
# THEMES
# ═══════════════════════════════════════════════════════════════

THEMES = {
    'Aurora':   dict(a=(0.20, 0.45, 1.00), b=(0.15, 0.85, 0.60), icon='✦'),
    'Midnight': dict(a=(0.15, 0.15, 0.45), b=(0.40, 0.15, 0.65), icon='☾'),
    'Lava':     dict(a=(1.00, 0.35, 0.10), b=(0.85, 0.10, 0.20), icon='🔥'),
    'Ocean':    dict(a=(0.05, 0.45, 0.95), b=(0.05, 0.85, 0.85), icon='🌊'),
    'Galaxy':   dict(a=(0.55, 0.20, 0.95), b=(0.25, 0.10, 0.60), icon='✧'),
    'Gold':     dict(a=(1.00, 0.82, 0.25), b=(0.95, 0.55, 0.10), icon='★'),
    'Emerald':  dict(a=(0.15, 0.90, 0.45), b=(0.05, 0.60, 0.30), icon='❦'),
    'Rose':     dict(a=(1.00, 0.45, 0.70), b=(0.85, 0.20, 0.55), icon='❀'),
    'Frost':    dict(a=(0.65, 0.90, 1.00), b=(0.85, 0.95, 1.00), icon='❄'),
    'Neon':     dict(a=(1.00, 0.15, 0.85), b=(0.15, 0.85, 1.00), icon='⚡'),
}
THEME_ORDER = list(THEMES.keys())
_CFG_THEME = 'BSLIFE_Theme'
_FX_T0 = time.time()


def _theme_current():
    try:
        name = babase.app.config.get(_CFG_THEME, 'Aurora')
        if name not in THEMES:
            name = 'Aurora'
        return name, THEMES[name]
    except Exception:
        return 'Aurora', THEMES['Aurora']


def _theme_rgb(theme, elapsed):
    period = 5.0
    phase = (elapsed % period) / period
    t = (1 - math.cos(phase * math.pi * 2)) / 2
    ha, sa, va = colorsys.rgb_to_hsv(*theme['a'])
    hb, sb, vb = colorsys.rgb_to_hsv(*theme['b'])
    dh = hb - ha
    if dh > 0.5:
        dh -= 1.0
    elif dh < -0.5:
        dh += 1.0
    h = (ha + dh * t) % 1.0
    s = sa + (sb - sa) * t
    v = va + (vb - va) * t
    v = min(1.0, v * (0.93 + 0.07 * math.sin(elapsed * 2.3)))
    return colorsys.hsv_to_rgb(h, s, v)


# ═══════════════════════════════════════════════════════════════
# COLORS
# ═══════════════════════════════════════════════════════════════

def hsv(h, s, v):
    return colorsys.hsv_to_rgb(h % 1.0, max(0.0, min(1.0, s)), max(0.0, min(1.0, v)))


def _palette(base_rgb):
    h, s, _v = colorsys.rgb_to_hsv(*base_rgb)
    s = min(1.0, 0.20 + s * 0.75)
    return {
        'bg_top': hsv(h, s * 0.85, 0.10),
        'bg_bot': hsv(h, s * 0.85, 0.06),
        'surface': hsv(h, s * 0.75, 0.18),
        'surface_hi': hsv(h, s * 0.75, 0.24),
        'surface_lo': hsv(h, s * 0.75, 0.13),
        'header': hsv(h, s * 0.80, 0.28),
        'border': hsv(h, s * 0.55, 0.55),
        'border_hi': hsv(h, s * 0.65, 0.78),
        'field': hsv(h, s * 0.75, 0.08),
        'accent': hsv(h, min(1.0, 0.30 + s * 0.55), 0.95),
        'accent_hi': hsv(h, min(1.0, 0.25 + s * 0.50), 1.0),
        'text': hsv(h, s * 0.15, 0.98),
        'dim': hsv(h, s * 0.35, 0.70),
        'muted': hsv(h, s * 0.45, 0.50),
        'success': (0.35, 1.00, 0.55),
        'danger': (1.00, 0.42, 0.50),
        'gold': (1.00, 0.82, 0.30),
        'silver': (0.85, 0.90, 0.95),
        'bronze': (0.90, 0.55, 0.30),
    }


def role_color(rid, pal):
    return {1: pal['gold'], 2: pal['accent'], 3: hsv(0.75, 0.75, 0.95)}.get(rid, pal['dim'])


# ═══════════════════════════════════════════════════════════════
# SCALE
# ═══════════════════════════════════════════════════════════════

def ui_scale():
    try:
        s = bui.app.ui_v1.uiscale
        if s is babase.UIScale.SMALL:
            return 1.75
        if s is babase.UIScale.MEDIUM:
            return 1.30
        return 1.0
    except Exception:
        return 1.0


def win_h():
    try:
        s = bui.app.ui_v1.uiscale
        if s is babase.UIScale.SMALL:
            return 380
        if s is babase.UIScale.MEDIUM:
            return 460
        return 560
    except Exception:
        return 560


# ═══════════════════════════════════════════════════════════════
# API
# ═══════════════════════════════════════════════════════════════

class BslifeAPI:
    def __init__(self):
        self.jar = http.cookiejar.CookieJar()
        try:
            ctx = ssl.create_default_context()
        except Exception:
            try:
                ctx = ssl._create_unverified_context()
            except Exception:
                ctx = None
        handlers = [urllib.request.HTTPCookieProcessor(self.jar)]
        try:
            handlers.append(urllib.request.HTTPSHandler(context=ctx))
        except Exception:
            pass
        self.opener = urllib.request.build_opener(*handlers)
        self.headers = {
            "User-Agent": "BombSquad/1.7.x (BSLIFE v11.1)",
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
        self.user = None
        self.ally = None
        self.roleid = None
        self.memberid = None
        self._load()

    def _load(self):
        if not os.path.exists(SESSION_FILE):
            return
        try:
            with open(SESSION_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            for k, v in data.get("cookies", {}).items():
                c = http.cookiejar.Cookie(
                    version=0, name=k, value=v, port=None, port_specified=False,
                    domain="bslife.ir", domain_specified=True, domain_initial_dot=False,
                    path="/", path_specified=True, secure=True,
                    expires=None, discard=True, comment=None, comment_url=None,
                    rest={"HttpOnly": None}, rfc2109=False,
                )
                self.jar.set_cookie(c)
            self.user = data.get("user")
            log(f"Session loaded: {self.user}")
        except Exception as e:
            log(f"Load cookies: {e}")

    def _save(self):
        data = {"cookies": {c.name: c.value for c in self.jar}, "user": self.user}
        try:
            with open(SESSION_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            log(f"Save cookies: {e}")

    def post(self, path, payload):
        url = BASE_URL + path
        try:
            data = json.dumps(payload).encode("utf-8")
            ck = self.jar._cookies
            ck_s = "".join(f"{n}={ck[d][p][n].value}; "
                          for d in ck for p in ck[d] for n in ck[d][p])
            h = self.headers.copy()
            if ck_s:
                h["Cookie"] = ck_s
            req = urllib.request.Request(url, data=data, headers=h, method="POST")
            with self.opener.open(req, timeout=20) as resp:
                result = resp.read().decode("utf-8", errors="replace").strip()
                self._save()
                return result
        except urllib.error.HTTPError as e:
            return f"__HTTPERROR__:{e.code}"
        except Exception as e:
            return f"__ERROR__:{e}"

    def post_json(self, path, payload):
        t = self.post(path, payload)
        if t in ("3", "", "-1"):
            return t
        if t.startswith("__"):
            return {"error": t}
        try:
            return json.loads(t)
        except Exception:
            return t

    def login(self, name, otp):
        r = self.post("/Head.php", {"fu": "login", "n": name, "p": otp})
        if r == "1":
            self.user = name
            self._save()
            return True, L("success_load")
        return False, {"0": "Wrong OTP", "ban": "Banned", "-1": "Server Error"}.get(r, "Unknown")

    def whoami(self):
        r = self.post("/Head.php", {"fu": "load"})
        return None if r in ("3", "") else r

    def logout(self):
        try:
            self.post("/Head.php", {"fu": "account_logout"})
        except Exception:
            pass
        self.jar.clear()
        if os.path.exists(SESSION_FILE):
            try:
                os.remove(SESSION_FILE)
            except Exception:
                pass
        self.user = None
        self.ally = None
        self.roleid = None
        self.memberid = None

    def ally_status(self): return self.post_json("/post/Ally.php", {"fu": "status"})
    def ally_members(self): return self.post_json("/post/Ally.php", {"fu": "members"})
    def ally_leave(self): return self.post("/post/Ally.php", {"fu": "leave_ally"})
    def ally_requests(self, t="new"): return self.post_json("/post/Ally.php", {"fu": "get_requests", "type": t, "offset": None})
    def ally_handle_request(self, rid, mode): return self.post("/post/Ally.php", {"fu": "handle_request", "request": rid, "mode": mode})
    def ally_change_role(self, mid, rid): return self.post("/post/Ally.php", {"fu": "change_role", "id": mid, "roleid": rid})
    def ally_change_title(self, mid, t, c): return self.post("/post/Ally.php", {"fu": "change_title", "id": mid, "title": t, "color": c})
    def ally_mute(self, target, typ): return self.post("/post/Ally.php", {"fu": "mute_unmute", "target": target, "type": typ})
    def ally_kick(self, mid): return self.post("/post/Ally.php", {"fu": "delete_member", "id": mid})
    def ally_settings(self): return self.post_json("/post/Ally.php", {"fu": "settings"})
    def ally_save_setting(self, k, v): return self.post_json("/post/Ally.php", {"fu": "settings", "key": k, "val": v})
    def ally_capacity(self): return self.post("/post/Ally.php", {"fu": "capacity"})
    def ally_chat_history(self, off=None): return self.post_json("/post/Ally.php", {"fu": "chat_history", "offset": off})
    def ally_chat_send(self, t): return self.post("/post/Ally.php", {"fu": "chat_send", "chat": t})
    def ally_ranking(self, d=None): return self.post_json("/post/Ally.php", {"fu": "ranking_info", "date": d})
    def ally_vault_status(self): return self.post_json("/post/Ally.php", {"fu": "vault_status"})
    def ally_vault_add(self, a): return self.post("/post/Ally.php", {"fu": "vault_add", "amount": a})
    def ally_vault_clear(self, t): return self.post("/post/Ally.php", {"fu": "vault_clear", "type": t})
    def ally_vault_news(self, off=None): return self.post_json("/post/Ally.php", {"fu": "vault_news", "offset": off})
    def ally_vault_shares(self, tid): return self.post_json("/post/Ally.php", {"fu": "vault_shares", "id": tid})
    def ally_enrol(self): return self.post_json("/post/Ally.php", {"fu": "enrol_settings"})
    def ally_set_enrol(self, k, v): return self.post_json("/post/Ally.php", {"fu": "enrol_settings", "key": k, "val": v})
    def ally_news(self, off=None): return self.post_json("/post/Ally.php", {"fu": "news", "offset": off})
    def create_status(self): return self.post_json("/post/AllyCreate.php", {"fu": "status"})
    def create_ally(self, n, c=0): return self.post_json("/post/AllyCreate.php", {"fu": "create", "name": n, "confirm": c})
    def list_allies(self, s="", o="rank"): return self.post_json("/post/AllyList.php", {"fu": "get_allys", "offset": None, "order": o, "search": s, "filter": "[]"})
    def join_ally(self, aid): return self.post("/post/AllyList.php", {"fu": "join_ally", "ally": aid})


class Net:
    @classmethod
    def fetch(cls, api, m, args=(), cb=None):
        def worker():
            try:
                r = getattr(api, m)(*args)
            except Exception as e:
                r = {"error": str(e)}
            if cb:
                try:
                    bui.pushcall(MyCall(cb, r), from_other_thread=True)
                except Exception as e:
                    log(f"Pushcall: {e}")
        threading.Thread(target=worker, daemon=True).start()


# ═══════════════════════════════════════════════════════════════
# UI PRIMITIVES
# ═══════════════════════════════════════════════════════════════

class RoundedRect:
    def __init__(self, parent, x, y, w, h, r, color):
        r = max(1.0, min(r, w / 2.0, h / 2.0))
        white = bui.gettexture('white')
        disc = bui.gettexture('circle')
        self.parts = []
        def add(px, py, pw, ph, tex):
            try:
                p = bui.imagewidget(
                    parent=parent, position=(px, py), size=(pw, ph),
                    texture=tex, color=color, opacity=1.0,
                )
                self.parts.append(p)
            except Exception:
                pass
        add(x + r, y, w - 2 * r, h, white)
        add(x, y + r, r, h - 2 * r, white)
        add(x + w - r, y + r, r, h - 2 * r, white)
        tile = 2 * r / 0.97
        for cx, cy in ((x + r, y + r), (x + w - r, y + r),
                       (x + r, y + h - r), (x + w - r, y + h - r)):
            add(cx - tile / 2, cy - tile / 2, tile, tile, disc)

    def recolor(self, color):
        for p in self.parts:
            try:
                bui.imagewidget(edit=p, color=color)
            except Exception:
                pass

    def delete(self):
        for p in self.parts:
            try:
                p.delete()
            except Exception:
                pass


class Card:
    def __init__(self, parent, x, y, w, h, r, bw=2.0):
        self.edge = RoundedRect(parent, x, y, w, h, r, (0, 0, 0))
        self.fill = RoundedRect(parent, x + bw, y + bw,
                                w - 2 * bw, h - 2 * bw, max(1.0, r - bw), (0, 0, 0))

    def recolor(self, edge, fill):
        self.edge.recolor(edge)
        self.fill.recolor(fill)

    def delete(self):
        self.edge.delete()
        self.fill.delete()


class Gradient:
    def __init__(self, parent, x, y, w, h, c_top, c_bot, layers=8):
        self.parts = []
        for i in range(layers):
            t = i / max(1, layers - 1)
            c = tuple(c_top[j] + (c_bot[j] - c_top[j]) * t for j in range(3))
            try:
                p = bui.imagewidget(
                    parent=parent, position=(x, y + i * h / layers),
                    size=(w, h / layers + 1),
                    texture=bui.gettexture('white'), color=c, opacity=1.0,
                )
                self.parts.append(p)
            except Exception:
                pass

    def recolor(self, c_top, c_bot):
        n = len(self.parts)
        for i, p in enumerate(self.parts):
            t = i / max(1, n - 1)
            c = tuple(c_top[j] + (c_bot[j] - c_top[j]) * t for j in range(3))
            try:
                bui.imagewidget(edit=p, color=c)
            except Exception:
                pass

    def delete(self):
        for p in self.parts:
            try:
                p.delete()
            except Exception:
                pass


# ═══════════════════════════════════════════════════════════════
# PARTICLE FIELD (behind everything)
# ═══════════════════════════════════════════════════════════════

class ParticleField:
    def __init__(self, parent, W, H):
        self.W, self.H = W, H
        self._active = True
        rnd = random.Random(3)
        soft = bui.gettexture('circleSoft')
        star = bui.gettexture('star')
        self.orbs = []
        for i in range(4):
            try:
                w = bui.imagewidget(
                    parent=parent, position=(0, 0),
                    size=(60, 60), texture=soft, color=(1, 1, 1), opacity=0.0,
                )
                self.orbs.append({
                    'w': w,
                    'x': rnd.uniform(0.15, 0.85) * W,
                    'y': rnd.uniform(0.20, 0.80) * H,
                    'r': rnd.uniform(50, 90),
                    'fx': rnd.uniform(0.10, 0.25),
                    'fy': rnd.uniform(0.08, 0.18),
                    'ph': rnd.uniform(0, 6.28),
                })
            except Exception:
                pass
        self.stars = []
        for i in range(10):
            try:
                w = bui.imagewidget(
                    parent=parent, position=(0, 0),
                    size=(6, 6), texture=star, color=(1, 1, 1), opacity=0.0,
                )
                self.stars.append({
                    'w': w,
                    'x': rnd.uniform(0.05, 0.95) * W,
                    'y': rnd.uniform(0.05, 0.95) * H,
                    's': rnd.uniform(4, 7),
                    'f': rnd.uniform(0.5, 1.5),
                    'ph': rnd.uniform(0, 6.28),
                    'last_op': -1.0,
                })
            except Exception:
                pass

    def tick(self, elapsed, pal):
        if not self._active:
            return
        # Orbs
        for o in self.orbs:
            try:
                x = o['x'] + math.sin(elapsed * o['fx'] + o['ph']) * 35
                y = o['y'] + math.cos(elapsed * o['fy'] + o['ph']) * 22
                sz = o['r'] * (1 + 0.06 * math.sin(elapsed * 0.9 + o['ph']))
                op = 0.04 + 0.04 * (1 + math.sin(elapsed * 0.6 + o['ph'])) / 2
                bui.imagewidget(
                    edit=o['w'], position=(x - sz / 2, y - sz / 2),
                    size=(sz, sz), color=pal['accent'], opacity=op,
                )
            except Exception:
                pass
        # Stars
        for s in self.stars:
            try:
                k = max(0.0, math.sin(elapsed * s['f'] + s['ph'])) ** 3
                op = 0.04 + 0.55 * k
                if abs(op - s['last_op']) > 0.08:
                    sz = s['s'] * (0.7 + 0.4 * k)
                    bui.imagewidget(
                        edit=s['w'], position=(s['x'] - sz / 2, s['y'] - sz / 2),
                        size=(sz, sz), color=pal['accent'], opacity=op,
                    )
                    s['last_op'] = op
            except Exception:
                pass

    def recolor(self, pal):
        pass

    def delete(self):
        self._active = False
        for o in self.orbs:
            try:
                o['w'].delete()
            except Exception:
                pass
        for s in self.stars:
            try:
                s['w'].delete()
            except Exception:
                pass


# ═══════════════════════════════════════════════════════════════
# TOASTS (fixed stacking)
# ═══════════════════════════════════════════════════════════════

class ToastStack:
    _toasts = []

    @classmethod
    def push(cls, text, kind='info', duration=2.4):
        color_map = {
            'info': (0.30, 0.70, 1.00),
            'success': (0.30, 0.95, 0.55),
            'error': (1.00, 0.35, 0.40),
            'warn': (1.00, 0.75, 0.20),
        }
        color = color_map.get(kind, color_map['info'])
        icon_map = {'info': 'i', 'success': '+', 'error': 'x', 'warn': '!'}
        icon = icon_map.get(kind, 'i')
        try:
            stack = bui.get_special_widget('overlay_stack')
            try:
                sz = stack.get_size()
                screen_h = sz[1]
                screen_w = sz[0]
            except Exception:
                screen_h, screen_w = 720, 1280

            sw, sh = 320, 48
            # FIX: use a global counter to position toasts
            idx = len(cls._toasts)
            x = (screen_w - sw) / 2
            y = screen_h - 80 - idx * 58

            root = bui.containerwidget(
                parent=stack, size=(sw, sh),
                transition='in_scale', scale=ui_scale(), color=color,
            )
            try:
                bui.containerwidget(edit=root, position=(x, y))
            except Exception:
                pass
            # Icon circle
            try:
                bui.imagewidget(
                    parent=root, position=(8, 8), size=(32, 32),
                    texture=bui.gettexture('circleSoft'),
                    color=(1, 1, 1), opacity=0.30,
                )
            except Exception:
                pass
            bui.textwidget(
                parent=root, position=(24, 24), size=(0, 0),
                text=icon, scale=1.1, color=(1, 1, 1),
                h_align='center', v_align='center',
            )
            bui.textwidget(
                parent=root, position=(50, 24), size=(0, 0),
                text=str(text), scale=0.7, color=(1, 1, 1),
                h_align='left', v_align='center', maxwidth=sw - 60,
            )
            cls._toasts.append(root)

            def _dismiss():
                try:
                    if root.exists():
                        bui.containerwidget(edit=root, transition='out_scale')
                except Exception:
                    pass
                try:
                    if root in cls._toasts:
                        cls._toasts.remove(root)
                except Exception:
                    pass
                try:
                    if root.exists():
                        root.delete()
                except Exception:
                    pass

            _safe_timer(duration, _dismiss)
        except Exception as e:
            log(f"Toast error: {e}")


# ═══════════════════════════════════════════════════════════════
# STATE
# ═══════════════════════════════════════════════════════════════

_top_win = None
_api_singleton = None
_opening = False
_open_dialogs = []
_router_lock = threading.Lock()


def _later(delay, call):
    _safe_timer(delay, call)


def _close_all_dialogs():
    for d in list(_open_dialogs):
        try:
            d.close()
        except Exception:
            pass
    _open_dialogs.clear()


# ═══════════════════════════════════════════════════════════════
# BASE WINDOW
# ═══════════════════════════════════════════════════════════════

class BaseWindow:
    def __init__(self, W, H):
        global _top_win
        self.W, self.H = W, H
        self._theme_name, self._theme = _theme_current()
        self._t0 = time.time()
        self._alive_flag = True
        self._btns = []
        self._cards = []
        self._tick_h = None

        base_color = _theme_rgb(self._theme, 0.0)
        self.pal = _palette(base_color)

        self.root = bui.containerwidget(
            parent=bui.get_special_widget('overlay_stack'),
            size=(W, H), transition='in_scale', scale=ui_scale(),
            color=self.pal['bg_top'],
        )
        _top_win = self

        # Gradient background
        self._grad = Gradient(self.root, 0, 0, W, H,
                              self.pal['bg_top'], self.pal['bg_bot'], layers=10)

        # Particles
        self._particles = ParticleField(self.root, W, H)

        # Start render loop
        self._loop()

    def _loop(self):
        if not self._alive_flag:
            self._tick_h = None
            return
        try:
            if not self.root.exists():
                self._tick_h = None
                self._alive_flag = False
                return
            elapsed = time.time() - _FX_T0
            color = _theme_rgb(self._theme, elapsed)
            pal = _palette(color)
            self.pal = pal

            if self._grad:
                self._grad.recolor(pal['bg_top'], pal['bg_bot'])

            if self._particles:
                self._particles.tick(elapsed, pal)

            self._on_tick(elapsed, pal)

            self._tick_h = _safe_timer(0.06, MyCall(self._loop))
        except Exception as e:
            log(f"Loop error: {e}")
            self._tick_h = None

    def _on_tick(self, elapsed, pal):
        pass

    def make_card(self, x, y, w, h, r=14, kind='surface'):
        if w <= 0 or h <= 0:
            return None
        card = Card(self.root, x, y, w, h, r, bw=1.8)
        edge, fill = self._card_colors(kind)
        card.recolor(edge, fill)
        self._cards.append((card, kind))
        return card

    def _card_colors(self, kind):
        p = self.pal
        if kind == 'surface_hi':
            return p['border_hi'], p['surface_hi']
        if kind == 'header':
            return p['border_hi'], p['header']
        if kind == 'field':
            return p['border'], p['field']
        return p['border'], p['surface']

    def button(self, parent, pos, size, label, call,
               kind='accent', text_scale=0.75):
        p = self.pal
        if kind == 'accent':
            c, t = p['accent'], (1, 1, 1)
        elif kind == 'danger':
            c, t = p['danger'], (1, 1, 1)
        elif kind == 'success':
            c, t = p['success'], (1, 1, 1)
        elif kind == 'surface':
            c, t = p['surface_hi'], p['text']
        elif kind == 'ghost':
            c, t = p['surface_lo'], p['dim']
        else:
            c, t = p['accent'], (1, 1, 1)

        try:
            btn = bui.buttonwidget(
                parent=parent, position=pos, size=size,
                label=label, color=c, textcolor=t,
                button_type='square', autoselect=True,
                text_scale=text_scale,
                on_activate_call=call,
                texture=bui.gettexture('buttonSquare'),
            )
            self._btns.append((btn, kind))
            return btn
        except Exception as e:
            log(f"Button error: {e}")
            return None

    def label(self, parent, pos, text, scale=0.7, color=None,
              h='left', maxwidth=None, v='center'):
        if color is None:
            color = self.pal['text']
        kw = dict(
            parent=parent, position=pos, size=(0, 0),
            text=str(text) if text is not None else '',
            scale=scale, color=color, h_align=h, v_align=v,
        )
        if maxwidth:
            kw['maxwidth'] = maxwidth
        try:
            return bui.textwidget(**kw)
        except Exception as e:
            log(f"Label error: {e}")
            return None

    def field(self, parent, pos, size, text='', max_chars=60, desc=''):
        x, y = pos
        w, h = size
        self.make_card(x, y, w, h, r=8, kind='field')
        try:
            return bui.textwidget(
                parent=parent, position=(x + 10, y), size=(w - 20, h),
                editable=True, text=str(text), autoselect=True,
                h_align='left', v_align='center',
                maxwidth=w - 26, max_chars=max_chars,
                description=desc, color=self.pal['text'],
                shadow=0.3,
            )
        except Exception as e:
            log(f"Field error: {e}")
            return None

    def divider(self, parent, x, y, w, color=None):
        if color is None:
            color = self.pal['border']
        if w <= 0:
            return None
        try:
            return bui.imagewidget(
                parent=parent, position=(x, y), size=(w, 1),
                texture=bui.gettexture('white'), color=color, opacity=0.6,
            )
        except Exception:
            return None

    def close(self):
        global _top_win
        self._alive_flag = False
        self._tick_h = None
        if _top_win is self:
            _top_win = None
        _close_all_dialogs()
        # Clear tracked cards & buttons
        for card, _k in self._cards:
            try:
                card.delete()
            except Exception:
                pass
        self._cards = []
        try:
            if self.root.exists():
                bui.containerwidget(edit=self.root, transition='out_scale')
                _safe_timer(0.2, self.root.delete)
        except Exception:
            pass

    def close_sound(self):
        try:
            bui.getsound('swish').play()
        except Exception:
            pass
        self.close()

    def cycle_theme(self):
        try:
            cfg = babase.app.config
            cur = self._theme_name
            i = (THEME_ORDER.index(cur) + 1) % len(THEME_ORDER) if cur in THEME_ORDER else 0
            new_name = THEME_ORDER[i]
            cfg[_CFG_THEME] = new_name
            try:
                cfg.commit()
            except Exception:
                pass
            self._theme_name = new_name
            self._theme = THEMES[new_name]
            try:
                bui.getsound('ding').play()
            except Exception:
                pass
            ToastStack.push(f"{L('style')}: {new_name} {THEMES[new_name]['icon']}", 'info')
        except Exception as e:
            log(f"Cycle theme: {e}")


# ═══════════════════════════════════════════════════════════════
# DIALOG
# ═══════════════════════════════════════════════════════════════

class Dialog(BaseWindow):
    def __init__(self, W, H, title, tcolor=None):
        super().__init__(W, H)
        _open_dialogs.append(self)
        self._closed = False

        # Header
        self.make_card(12, H - 58, W - 24, 46, r=12, kind='header')
        self._title_w = self.label(
            self.root, (W / 2 + 12, H - 35), title,
            scale=0.95, color=tcolor or self.pal['text'],
            h='center', maxwidth=W - 130,
        )
        self._title_color_fixed = tcolor

        # Close button
        try:
            self.close_btn = bui.buttonwidget(
                parent=self.root, position=(18, H - 52), size=(38, 38),
                label=bui.charstr(bui.SpecialChar.CLOSE),
                color=self.pal['danger'], textcolor=(1, 1, 1),
                button_type='square', text_scale=0.9,
                on_activate_call=MyCall(self.close_sound),
                texture=bui.gettexture('buttonSquare'),
            )
            bui.containerwidget(edit=self.root, cancel_button=self.close_btn)
        except Exception:
            self.close_btn = None

    def _on_tick(self, elapsed, pal):
        if not self._title_color_fixed and self._title_w:
            try:
                bui.textwidget(edit=self._title_w, color=pal['text'])
            except Exception:
                pass

    def close(self):
        if self._closed:
            return
        self._closed = True
        try:
            _open_dialogs.remove(self)
        except Exception:
            pass
        BaseWindow.close(self)


class AlertDialog(Dialog):
    def __init__(self, title, text, kind='info', on_ok=None):
        color_map = {'success': (0.30, 0.95, 0.55),
                     'error': (1.0, 0.35, 0.40),
                     'warn': (1.0, 0.75, 0.20),
                     'info': (0.30, 0.70, 1.0)}
        tcolor = color_map.get(kind, color_map['info'])
        lines = str(text).split('\n')
        W, H = 400, 160 + 22 * max(1, min(len(lines), 8))
        super().__init__(W, H, title, tcolor=tcolor)
        self._on_ok = on_ok

        self.make_card(12, 76, W - 24, H - 148, r=12, kind='surface')
        y = H - 70 - 20
        for ln in lines[:8]:
            self.label(self.root, (W / 2, y), ln, scale=0.65,
                       color=self.pal['text'], h='center', maxwidth=W - 60)
            y -= 22

        ok = self.button(self.root, (W / 2 - 70, 20), (140, 42),
                         L('ok'), MyCall(self._ok), kind='success')
        if ok:
            try:
                bui.containerwidget(edit=self.root, start_button=ok)
            except Exception:
                pass

    def _ok(self):
        self.close()
        if self._on_ok:
            _later(0.22, MyCall(self._on_ok))


class ConfirmDialog(Dialog):
    def __init__(self, title, text, on_yes, danger=True):
        W, H = 420, 220
        super().__init__(W, H, title,
                         tcolor=(1.0, 0.35, 0.40) if danger else (1.0, 0.78, 0.30))
        self._on_yes = on_yes

        self.make_card(12, 74, W - 24, H - 148, r=12, kind='surface')
        self.label(self.root, (W / 2, H - 110), text, scale=0.7,
                   color=self.pal['text'], h='center', maxwidth=W - 60)

        self.button(self.root, (24, 20), (170, 42), L('yes'),
                    MyCall(self._yes), kind='danger' if danger else 'success')
        self.button(self.root, (W - 194, 20), (170, 42), L('no'),
                    MyCall(self.close_sound), kind='surface')

    def _yes(self):
        self.close()
        if self._on_yes:
            _later(0.22, MyCall(self._on_yes))


class NumberInputDialog(Dialog):
    def __init__(self, title, initial, on_ok):
        W, H = 400, 230
        super().__init__(W, H, title)
        self._on_ok = on_ok

        self.make_card(12, 74, W - 24, H - 148, r=12, kind='surface')
        self.inp = self.field(self.root, (40, 100), (W - 80, 42),
                              str(initial) if initial is not None else "",
                              max_chars=12, desc=L('amount_hint'))

        self.button(self.root, (24, 20), (170, 42), L('confirm'),
                    MyCall(self._confirm), kind='success')
        self.button(self.root, (W - 194, 20), (170, 42), L('cancel'),
                    MyCall(self.close_sound), kind='surface')

    def _confirm(self):
        if not self.inp:
            return
        try:
            txt = (bui.textwidget(query=self.inp) or '').strip()
        except Exception:
            return
        if not txt:
            val = None
        else:
            try:
                val = int(txt)
            except Exception:
                try:
                    bui.getsound('error').play()
                except Exception:
                    pass
                return
        self.close()
        if self._on_ok:
            _later(0.22, MyCall(self._on_ok, val))


class SelectDialog(Dialog):
    def __init__(self, title, options, on_ok):
        n = max(1, len(options))
        W = 400
        H = 150 + n * 48
        super().__init__(W, H, title)
        self._on_ok = on_ok
        self._sel = None
        self._sel_key = None
        self._keys = []
        self._choices = []

        y = H - 76
        for i, (val, label) in enumerate(options):
            y -= 46
            key = f"opt{i}"
            self._keys.append((key, val))
            b = self.button(self.root, (24, y), (W - 48, 40),
                            label, MyCall(self._pick, key, val),
                            kind='surface', text_scale=0.85)
            self._choices.append((key, val, b))

        self.button(self.root, (24, 20), (170, 42), L('confirm'),
                    MyCall(self._confirm), kind='success')
        self.button(self.root, (W - 194, 20), (170, 42), L('cancel'),
                    MyCall(self.close_sound), kind='surface')

    def _pick(self, key, val):
        self._sel = val
        self._sel_key = key
        p = self.pal
        for k, _v, b in self._choices:
            if b is None:
                continue
            c = p['accent'] if k == key else p['surface_hi']
            try:
                bui.buttonwidget(edit=b, color=c)
            except Exception:
                pass

    def _confirm(self):
        if self._sel_key is None:
            try:
                bui.getsound('error').play()
            except Exception:
                pass
            return
        self.close()
        if self._on_ok:
            _later(0.22, MyCall(self._on_ok, self._sel))


# ═══════════════════════════════════════════════════════════════
# LOGIN
# ═══════════════════════════════════════════════════════════════

class LoginWindow(BaseWindow):
    def __init__(self, api, on_success):
        W, H = 520, 380
        super().__init__(W, H)
        self.api = api
        self.on_success = on_success
        self._busy = False

        # Header
        self.make_card(12, H - 74, W - 24, 62, r=16, kind='header')
        self._title = self.label(
            self.root, (W / 2, H - 43), u"\ue010  BSLIFE ALLY",
            scale=1.05, color=self.pal['gold'], h='center', maxwidth=W - 120,
        )
        self.label(self.root, (W / 2, H - 62), L('login_sub'),
                   scale=0.48, color=self.pal['dim'], h='center')

        # Close
        try:
            cb = bui.buttonwidget(
                parent=self.root, position=(22, H - 66), size=(42, 42),
                label=bui.charstr(bui.SpecialChar.CLOSE),
                color=self.pal['danger'], textcolor=(1, 1, 1),
                button_type='square', text_scale=0.9,
                on_activate_call=MyCall(self.close_sound),
                texture=bui.gettexture('buttonSquare'),
            )
            bui.containerwidget(edit=self.root, cancel_button=cb)
        except Exception:
            pass

        # Info card
        self.make_card(30, 250, W - 60, 78, r=14, kind='surface_hi')
        self.label(self.root, (W / 2, 302), L('login'),
                   scale=0.62, color=self.pal['accent'], h='center')
        self.label(self.root, (W / 2, 280), L('login_h1'),
                   scale=0.55, color=self.pal['text'], h='center', maxwidth=W - 80)
        self.label(self.root, (W / 2, 262), L('login_h2'),
                   scale=0.55, color=self.pal['text'], h='center', maxwidth=W - 80)

        # Username
        self.label(self.root, (46, 218), L('username') + ":",
                   scale=0.62, color=self.pal['dim'])
        self.inp_user = self.field(self.root, (46, 176), (W - 92, 36),
                                   "", max_chars=30, desc=L('username'))

        # OTP
        self.label(self.root, (46, 148), L('otp') + ":",
                   scale=0.62, color=self.pal['dim'])
        self.inp_otp = self.field(self.root, (46, 106), (W - 92, 36),
                                  "", max_chars=8, desc=L('otp'))

        # Status
        self._status = self.label(
            self.root, (W / 2, 76), "", scale=0.6,
            color=self.pal['dim'], h='center', maxwidth=W - 60,
        )

        # Login button
        b = self.button(self.root, (46, 20), (W - 92, 46),
                        L('login'), MyCall(self._do_login),
                        kind='accent', text_scale=0.85)
        if b:
            try:
                bui.containerwidget(edit=self.root, start_button=b)
            except Exception:
                pass

        # Theme cycle
        self.button(self.root, (W - 60, 20), (44, 46),
                    "o", MyCall(self.cycle_theme), kind='surface')

    def _on_tick(self, elapsed, pal):
        try:
            if self._title:
                bui.textwidget(edit=self._title, color=pal['gold'])
            if self._status:
                bui.textwidget(edit=self._status, color=pal['dim'])
        except Exception:
            pass

    def _status_msg(self, text, color):
        if self._status:
            try:
                bui.textwidget(edit=self._status, text=text, color=color)
            except Exception:
                pass

    def _do_login(self):
        if self._busy:
            return
        if not self.inp_user or not self.inp_otp:
            return
        try:
            name = (bui.textwidget(query=self.inp_user) or '').strip()
            otp = (bui.textwidget(query=self.inp_otp) or '').strip()
        except Exception:
            return
        if not name or not otp:
            self._status_msg(L('fill_all'), self.pal['danger'])
            try:
                bui.getsound('error').play()
            except Exception:
                pass
            return

        self._busy = True
        self._status_msg(L('logging_in') + "...", self.pal['dim'])

        def worker():
            try:
                ok, msg = self.api.login(name, otp)
            except Exception as e:
                ok, msg = False, str(e)
            try:
                bui.pushcall(MyCall(self._done, ok, msg), from_other_thread=True)
            except Exception as e:
                log(f"Login pushcall: {e}")
        threading.Thread(target=worker, daemon=True).start()

    def _done(self, ok, msg):
        self._busy = False
        if not self._alive_flag or not self.root.exists():
            return
        if ok:
            self._status_msg(L('success_load'), self.pal['success'])
            _later(0.5, MyCall(self._go_next))
        else:
            self._status_msg(L('error') + ": " + str(msg), self.pal['danger'])
            try:
                bui.getsound('error').play()
            except Exception:
                pass

    def _go_next(self):
        self.close()
        _later(0.28, MyCall(self.on_success))


# ═══════════════════════════════════════════════════════════════
# MAIN WINDOW
# ═══════════════════════════════════════════════════════════════

TAB_ICONS = {
    "overview": "[]",
    "members": "()",
    "requests": "<>",
    "vault": "$$",
    "settings": "**",
    "ranking": "##",
    "news": "!!",
    "chat": "..",
    "channels": "^^",
}


class MainWindow(BaseWindow):
    TABS = ["overview", "members", "requests", "vault",
            "settings", "ranking", "news", "chat", "channels"]

    def __init__(self, api):
        W, H = 680, win_h()
        super().__init__(W, H)
        self.api = api
        self.tab = "overview"
        self._tab_btns = {}
        self._req_filter = "new"
        self._tok = 0
        self._news = []
        self._chat_sig = None
        self._chat_scroll = None
        self._chat_cont = None

        self._header_h = 64
        self._footer_h = 44
        self._sidebar_w = 140
        self._content_x = 16 + self._sidebar_w + 12
        self._content_w = W - 16 - self._content_x - 16
        self._content_y = 16 + self._footer_h
        self._content_h = H - self._header_h - 24 - self._content_y

        # Header
        self.make_card(12, H - 76, W - 24, 64, r=16, kind='header')
        self._title = self.label(
            self.root, (32, H - 48), u"\ue010  BSLIFE",
            scale=1.0, color=self.pal['gold'], maxwidth=400,
        )
        self._subtitle = self.label(
            self.root, (32, H - 66), L('loading') + "...",
            scale=0.5, color=self.pal['dim'], maxwidth=400,
        )
        self.button(self.root, (W - 206, H - 62), (60, 38), "o",
                    MyCall(self.cycle_theme), kind='surface')
        self.button(self.root, (W - 138, H - 62), (54, 38), L('style'),
                    MyCall(self.cycle_theme), kind='surface', text_scale=0.55)
        self.button(self.root, (W - 76, H - 62), (60, 38), L('logout'),
                    MyCall(self._logout), kind='danger', text_scale=0.55)

        try:
            cb = bui.buttonwidget(
                parent=self.root, position=(16, H - 66), size=(46, 46),
                label=bui.charstr(bui.SpecialChar.CLOSE),
                color=self.pal['danger'], textcolor=(1, 1, 1),
                button_type='square', text_scale=0.9,
                on_activate_call=MyCall(self.close_sound),
                texture=bui.gettexture('buttonSquare'),
            )
            bui.containerwidget(edit=self.root, cancel_button=cb)
        except Exception:
            pass

        # Sidebar
        self.make_card(12, self._content_y, self._sidebar_w, self._content_h,
                       r=14, kind='surface')
        self._build_sidebar()

        # Content
        self.make_card(self._content_x - 8, self._content_y,
                       self._content_w + 16, self._content_h,
                       r=14, kind='surface')
        self._content = None
        self._new_content()

        # Footer status
        self._status = self.label(
            self.root, (W / 2, 22), "", scale=0.6,
            color=self.pal['dim'], h='center', maxwidth=W - 60,
        )

        self._refresh()

    def _on_tick(self, elapsed, pal):
        try:
            if self._title:
                bui.textwidget(edit=self._title, color=pal['gold'])
            if self._subtitle:
                bui.textwidget(edit=self._subtitle, color=pal['dim'])
            if self._status:
                bui.textwidget(edit=self._status, color=pal['dim'])
        except Exception:
            pass

    def _set_status(self, text, color=None):
        if self._status:
            try:
                bui.textwidget(
                    edit=self._status, text=text,
                    color=color or self.pal['dim'],
                )
            except Exception:
                pass

    def _new_content(self):
        if self._content is not None:
            try:
                self._content.delete()
            except Exception:
                pass
        self._content = bui.containerwidget(
            parent=self.root,
            position=(self._content_x, self._content_y),
            size=(self._content_w, self._content_h),
            background=False,
        )
        self._tok += 1
        return self._content

    def _reload(self, *_a):
        if not self._alive_flag or not self.root.exists():
            return
        self._new_content()
        self._render()

    def _alive(self, tok):
        try:
            return (self._alive_flag) and tok == self._tok and self.root.exists()
        except Exception:
            return False

    def _build_sidebar(self):
        for b in self._tab_btns.values():
            try:
                b.delete()
            except Exception:
                pass
        self._tab_btns = {}

        tabs = [k for k in self.TABS
                if not (k in ("requests", "settings") and self.api.roleid not in (1, 2))]

        n = max(1, len(tabs))
        gap = 3
        avail = self._content_h - 16
        th = min(38, max(20, (avail - (n - 1) * gap) / n))
        y = self._content_y + self._content_h - 8 - th

        for key in tabs:
            icon = TAB_ICONS.get(key, "?")
            label = f"{icon}  {L(key)}"
            c, t = (self.pal['accent'], (1, 1, 1)) if key == self.tab \
                   else (self.pal['surface_hi'], self.pal['text'])
            try:
                btn = bui.buttonwidget(
                    parent=self.root,
                    position=(12 + 6, y),
                    size=(self._sidebar_w - 12, th),
                    label=label, color=c, textcolor=t,
                    button_type='square', autoselect=True,
                    text_scale=0.65,
                    on_activate_call=MyCall(self._switch_tab, key),
                    texture=bui.gettexture('buttonSquare'),
                )
                self._tab_btns[key] = btn
            except Exception as e:
                log(f"Sidebar btn: {e}")
            y -= th + gap

    def _switch_tab(self, key):
        if not self._alive_flag:
            return
        self.tab = key
        for k, b in self._tab_btns.items():
            c = self.pal['accent'] if k == key else self.pal['surface_hi']
            t = (1, 1, 1) if k == key else self.pal['text']
            try:
                bui.buttonwidget(edit=b, color=c, textcolor=t)
            except Exception:
                pass
        self._reload()

    def _refresh(self):
        self._set_status(L('loading') + "...")
        Net.fetch(self.api, "ally_status", cb=self._on_status)

    def _on_status(self, st):
        if not self._alive_flag or not self.root.exists():
            return
        if st in ("3", "0", "", None):
            self._set_status(L('recovering') + "...")
            def check(who):
                if who:
                    self._refresh()
                else:
                    self._set_status(L('expired'), self.pal['danger'])
                    self._logout()
            Net.fetch(self.api, "whoami", cb=check)
            return
        if not isinstance(st, dict):
            self.close()
            HubWindow(self.api)
            return
        if "error" in st and "name" not in st:
            self._set_status(L('error') + ": " + str(st['error']),
                             self.pal['danger'])
            return
        self.api.ally = st.get("name")
        self.api.roleid = st.get("roleid")
        self.api.memberid = st.get("memberid")
        try:
            if self._title:
                bui.textwidget(
                    edit=self._title,
                    text=u"\ue010  " + f"{st.get('name') or L('no_ally')}",
                )
            if self._subtitle:
                bui.textwidget(
                    edit=self._subtitle,
                    text=f"{L('user')}: {self.api.user or '?'}  -  {role_name(st.get('roleid'))}",
                )
        except Exception:
            pass
        self._set_status(L('ready'), self.pal['success'])
        self._build_sidebar()
        self._reload()

    def _render(self):
        handler = getattr(self, "_tab_" + self.tab, None)
        if handler:
            try:
                handler()
            except Exception as e:
                log(f"Render {self.tab}: {e}")

    def _logout(self):
        self._alive_flag = False
        self._tok += 1
        self.api.logout()
        self.close()
        _later(0.3, MyCall(LoginWindow, self.api, _route))

    # ═══════════════════════ TABS ═══════════════════════

    def _tab_overview(self):
        c, tok = self._content, self._tok
        CW, CH = self._content_w, self._content_h
        if not c or CW <= 0 or CH <= 0:
            return

        def cb(st):
            if not self._alive(tok) or not isinstance(st, dict):
                return
            if not c.exists():
                return
            self.label(c, (CW / 2, CH - 24), L('overview'),
                       scale=1.05, color=self.pal['gold'], h='center')
            self.divider(c, 20, CH - 40, CW - 40)

            cards = [
                (L('ally_name'), st.get('name') or '-', self.pal['text']),
                (L('your_role'), role_name(st.get('roleid')),
                 role_color(st.get('roleid'), self.pal)),
                (L('members_count'), str(st.get('count', '?')), self.pal['text']),
            ]
            y = CH - 68
            for k, v, col in cards:
                y -= 60
                if y < 60:
                    break
                self.make_card(20, y, CW - 40, 52, r=10, kind='surface_hi')
                self.label(c, (40, y + 26), k, scale=0.7,
                           color=self.pal['dim'])
                self.label(c, (CW - 40, y + 26), str(v), scale=0.8,
                           color=col, h='right', maxwidth=CW / 2)

            if self.api.roleid != 1 and y > 80:
                self.button(c, (CW / 2 - 100, 10), (200, 42),
                            L('leave'), MyCall(self._confirm_leave),
                            kind='danger', text_scale=0.75)

        Net.fetch(self.api, "ally_status", cb=cb)

    def _confirm_leave(self):
        def do_leave():
            def cb(r):
                if r == "1":
                    ToastStack.push(L('leave'), 'warn')
                    self.close()
                    _later(0.5, MyCall(_route))
                else:
                    ToastStack.push(L('fail'), 'error')
            Net.fetch(self.api, "ally_leave", cb=cb)
        ConfirmDialog(L('leave'), L('leave_confirm'), do_leave, danger=True)

    def _tab_members(self):
        c, tok = self._content, self._tok
        CW, CH = self._content_w, self._content_h
        if not c or CW <= 0 or CH <= 0:
            return

        def cb(members):
            if not self._alive(tok):
                return
            if not c.exists():
                return
            if not isinstance(members, list):
                if members in ("3", "", "-1"):
                    self._on_status("3")
                return
            if not members:
                self.label(c, (CW / 2, CH / 2), L('empty'),
                           scale=0.9, color=self.pal['dim'], h='center')
                return

            self.label(c, (CW / 2, CH - 24),
                       f"{L('members')} ({len(members)})",
                       scale=1.0, color=self.pal['gold'], h='center')
            self.divider(c, 20, CH - 40, CW - 40)

            scroll_h = max(50, CH - 50)
            try:
                sc = bui.scrollwidget(
                    parent=c, position=(0, 0),
                    size=(CW, scroll_h),
                    color=(0.4, 0.6, 0.3), border_opacity=0.0,
                )
                rh = 38
                hh = max(rh * len(members) + 10, scroll_h)
                cont = bui.containerwidget(parent=sc, size=(max(50, CW - 12), hh), background=False)
                rw = CW - 12
                y = hh

                for m in members:
                    y -= rh
                    is_me = m.get('id') == self.api.memberid
                    rid = m.get('roleid')
                    role_c = role_color(rid, self.pal)
                    bg_col = self.pal['surface_hi'] if is_me else self.pal['surface']

                    try:
                        bui.imagewidget(
                            parent=cont, position=(0, y + 2),
                            size=(rw, rh - 4),
                            texture=bui.gettexture('white'),
                            color=bg_col, opacity=0.5,
                        )
                    except Exception:
                        pass

                    try:
                        bui.imagewidget(
                            parent=cont, position=(8, y + (rh - 22) / 2),
                            size=(60, 22),
                            texture=bui.gettexture('circleSoft'),
                            color=role_c, opacity=0.85,
                        )
                    except Exception:
                        pass
                    self.label(cont, (8 + 30, y + rh / 2), role_name(rid),
                               scale=0.5, color=(1, 1, 1), h='center', maxwidth=54)

                    self.label(cont, (78, y + rh / 2), m.get('name', '?'),
                               scale=0.65, color=self.pal['text'],
                               maxwidth=rw - 200)

                    if m.get('muted'):
                        self.label(cont, (rw - 120, y + rh / 2), "M",
                                   scale=0.6, color=self.pal['danger'], h='right')

                    if self.api.roleid in (1, 2) and not is_me:
                        self.button(cont, (rw - 50, y + 6), (42, 26),
                                    "...", MyCall(self._open_member, m),
                                    kind='accent', text_scale=0.6)
            except Exception as e:
                log(f"Members scroll: {e}")

        Net.fetch(self.api, "ally_members", cb=cb)

    def _open_member(self, m):
        MemberActionWindow(self.api, m, self._reload)

    def _tab_requests(self):
        c, tok = self._content, self._tok
        CW, CH = self._content_w, self._content_h
        if not c or CW <= 0 or CH <= 0:
            return

        self.label(c, (CW / 2, CH - 24), L('requests'),
                   scale=1.0, color=self.pal['gold'], h='center')
        self.divider(c, 20, CH - 40, CW - 40)

        bw = max(50, (CW - 20) / 3)
        for i, key in enumerate(["new", "accepted", "rejected"]):
            kind = 'accent' if key == self._req_filter else 'surface'
            self.button(c, (10 + i * bw, CH - 84), (bw - 6, 30),
                        L(key), MyCall(self._set_filter, key),
                        kind=kind, text_scale=0.6)

        def cb(reqs):
            if not self._alive(tok):
                return
            if not c.exists():
                return
            if not isinstance(reqs, list):
                return
            if not reqs:
                self.label(c, (CW / 2, (CH - 100) / 2), L('empty'),
                           scale=0.9, color=self.pal['dim'], h='center')
                return

            scroll_h = max(50, CH - 100)
            try:
                sc = bui.scrollwidget(
                    parent=c, position=(0, 0),
                    size=(CW, scroll_h),
                    color=(0.4, 0.6, 0.3), border_opacity=0.0,
                )
                rh = 40
                hh = max(rh * len(reqs) + 10, scroll_h)
                cont = bui.containerwidget(parent=sc, size=(max(50, CW - 12), hh), background=False)
                rw = CW - 12
                y = hh

                for r in reqs:
                    y -= rh
                    try:
                        bui.imagewidget(
                            parent=cont, position=(0, y + 2),
                            size=(rw, rh - 4),
                            texture=bui.gettexture('white'),
                            color=self.pal['surface'], opacity=0.5,
                        )
                    except Exception:
                        pass
                    self.label(cont, (10, y + rh / 2), r.get('name', '?'),
                               scale=0.65, color=self.pal['text'],
                               maxwidth=rw - 200)
                    if self._req_filter == "new":
                        self.button(cont, (rw - 150, y + 8), (68, 26),
                                    "+", MyCall(self._handle_req, r, "accept"),
                                    kind='success', text_scale=0.7)
                        self.button(cont, (rw - 78, y + 8), (68, 26),
                                    "x", MyCall(self._handle_req, r, "reject"),
                                    kind='danger', text_scale=0.7)
            except Exception as e:
                log(f"Requests scroll: {e}")

        Net.fetch(self.api, "ally_requests", (self._req_filter,), cb=cb)

    def _set_filter(self, key):
        self._req_filter = key
        self._reload()

    def _handle_req(self, r, mode):
        Net.fetch(self.api, "ally_handle_request",
                  (r.get('id'), mode), cb=lambda res: self._reload())

    # ═══════════════════════ VAULT ═══════════════════════

    def _tab_vault(self):
        c, tok = self._content, self._tok
        CW, CH = self._content_w, self._content_h
        if not c or CW <= 0 or CH <= 0:
            return

        self.label(c, (CW / 2, CH - 24), L('vault'),
                   scale=1.0, color=self.pal['gold'], h='center')
        self.divider(c, 20, CH - 40, CW - 40)

        loading = self.label(c, (CW / 2, CH / 2), L('loading') + "...",
                             scale=0.85, color=self.pal['dim'], h='center')

        def cb(v):
            if not self._alive(tok):
                return
            if not c.exists():
                return
            try:
                if loading:
                    loading.delete()
            except Exception:
                pass
            if not isinstance(v, dict):
                self.label(c, (CW / 2, CH / 2), str(v),
                           scale=0.75, color=self.pal['danger'], h='center')
                return

            coins = v.get('coin', 0)

            # Hero card
            self.make_card(20, CH - 190, CW - 40, 130, r=16, kind='surface_hi')
            self.label(c, (CW / 2, CH - 78), "$",
                       scale=2.5, color=self.pal['gold'], h='center')
            self.label(c, (CW / 2, CH - 116), fmt(coins),
                       scale=2.0, color=self.pal['gold'], h='center',
                       maxwidth=CW - 80)
            self.label(c, (CW / 2, CH - 148), L('coins'),
                       scale=0.65, color=self.pal['dim'], h='center')

            # Action buttons
            btns = [
                (L('deposit'), self._vault_deposit, 'success'),
                (L('history'), self._vault_history, 'accent'),
            ]
            if self.api.roleid in (1, 2):
                btns.append((L('split'), self._vault_split, 'danger'))

            bw = max(50, (CW - 40 - 12 * (len(btns) - 1)) / len(btns))
            x = 20
            for label, call, kind in btns:
                self.button(c, (x, CH - 250), (bw, 46),
                            label, call, kind=kind, text_scale=0.7)
                x += bw + 12

            # Chart
            self.label(c, (CW / 2, CH - 285), L('history'),
                       scale=0.7, color=self.pal['dim'], h='center')

            chart_y = max(20, CH - 400)
            chart_h = max(30, min(100, CH - 310))
            chart_x = 30
            chart_w = CW - 60

            def chart_cb(news):
                if not self._alive(tok):
                    return
                if not c.exists():
                    return
                if not isinstance(news, list) or not news:
                    self.label(c, (CW / 2, chart_y + chart_h / 2), L('no_data'),
                               scale=0.7, color=self.pal['dim'], h='center')
                    return
                n = min(len(news), 8)
                if n <= 0:
                    return
                items = news[:n]
                bw_ = max(4, (chart_w - (n - 1) * 6) / n)
                max_val = 1
                for it in items:
                    try:
                        val = abs(int(it.get('val', 0) or 1))
                        if val > max_val:
                            max_val = val
                    except Exception:
                        pass

                for i, it in enumerate(items):
                    try:
                        val = abs(int(it.get('val', 0) or 1))
                    except Exception:
                        val = 1
                    bh = max(6, (val / max_val) * (chart_h - 10))
                    bx = chart_x + i * (bw_ + 6)
                    by = chart_y + 5
                    try:
                        bui.imagewidget(
                            parent=c, position=(bx, by),
                            size=(bw_, bh),
                            texture=bui.gettexture('white'),
                            color=self.pal['accent'],
                            opacity=0.8,
                        )
                    except Exception:
                        pass
                    self.label(c, (bx + bw_ / 2, by + bh + 8), fmt(val),
                               scale=0.4, color=self.pal['dim'], h='center')

            Net.fetch(self.api, "ally_vault_news", (None,), cb=chart_cb)

        Net.fetch(self.api, "ally_vault_status", cb=cb)

    def _vault_deposit(self):
        def do_deposit(amount):
            if amount is None:
                return
            if amount < 100:
                AlertDialog(L('fail'), L('min_deposit'), kind='error')
                return

            def cb(r):
                if r == "1":
                    ToastStack.push(L('deposit_ok'), 'success')
                    AlertDialog(L('success'), L('deposit_ok'),
                                kind='success', on_ok=self._reload)
                else:
                    ToastStack.push(L('no_coins'), 'error')
                    AlertDialog(L('fail'),
                                L('no_coins') if r == "coin_not_enough" else L('fail'),
                                kind='error')
            Net.fetch(self.api, "ally_vault_add", (amount,), cb=cb)
        NumberInputDialog(L('enter_amount'), "", do_deposit)

    def _vault_history(self):
        VaultHistoryWindow(self.api)

    def _vault_split(self):
        opts = [
            ("equal_all", L('equal_all')),
            ("equal_ranking", L('equal_top')),
            ("ranking_points", L('by_points')),
        ]

        def picked(typ):
            def cb(r):
                if r == "1":
                    ToastStack.push(L('vault_ok'), 'success')
                    AlertDialog(L('success'), L('vault_ok'),
                                kind='success', on_ok=self._reload)
                else:
                    msg = {"coin_not_enough": L('no_coins'),
                           "no_ranking_info": L('not_ranked')}.get(r, L('fail'))
                    AlertDialog(L('fail'), msg, kind='error')
            Net.fetch(self.api, "ally_vault_clear", (typ,), cb=cb)
        SelectDialog(L('split'), opts, picked)

    # ═══════════════════════ SETTINGS ═══════════════════════

    def _tab_settings(self):
        c, tok = self._content, self._tok
        CW, CH = self._content_w, self._content_h
        if not c or CW <= 0 or CH <= 0:
            return

        self.label(c, (CW / 2, CH - 24), L('settings'),
                   scale=1.0, color=self.pal['gold'], h='center')
        self.divider(c, 20, CH - 40, CW - 40)

        def cb(st):
            if not self._alive(tok) or not isinstance(st, dict):
                return
            if not c.exists():
                return

            def cb_enrol(en):
                if not self._alive(tok) or not isinstance(en, dict):
                    return
                if not c.exists():
                    return
                taghide = st.get('taghide')
                mode_txt = {None: L('direct'), 1: L('reqmode'),
                            -1: L('closed')}.get(en.get('request'), '?')

                rows = [
                    ("[]", L('capacity'), str(st.get('capacity', '?')),
                     L('buy'), self._buy_cap),
                    ("*", L('gkick'), str(st.get('gkick', 1)),
                     L('set'), lambda: self._edit_num('gkick', st.get('gkick', 1))),
                    ("^", L('spynet'), fmt(st.get('spynet', 0)),
                     L('set'), lambda: self._edit_num('spynet', st.get('spynet', 0))),
                    ("#", L('tag'), L('active') if taghide is None else L('inactive'),
                     None, None),
                    ("$", L('price'),
                     fmt(st.get('price')) if st.get('price') else L('not_set'),
                     L('set'), lambda: self._edit_num('price', st.get('price'))),
                    ("__section__", L('enrol')),
                    ("~", L('join_mode'), mode_txt,
                     L('change'), self._change_mode),
                    ("C", L('min_coin'), str(en.get('coin', '-')),
                     L('set'), lambda: self._edit_enrol('coin', en.get('coin'))),
                    ("T", L('top'), str(en.get('top', '-')),
                     L('set'), lambda: self._edit_enrol('top', en.get('top'))),
                    ("S", L('score'), str(en.get('score', '-')),
                     L('set'), lambda: self._edit_enrol('score', en.get('score'))),
                    ("B", L('bot'), L('forced') if en.get('bot') == 1 else L('off'),
                     L('change'), self._toggle_bot),
                ]

                rh = 42
                scroll_h = max(50, CH - 50)
                try:
                    sc = bui.scrollwidget(
                        parent=c, position=(0, 0),
                        size=(CW, scroll_h),
                        color=(0.4, 0.6, 0.3), border_opacity=0.0,
                    )
                    hh = max(rh * len(rows) + 10, scroll_h)
                    cont = bui.containerwidget(parent=sc, size=(max(50, CW - 12), hh), background=False)
                    rw = CW - 12
                    y = hh

                    for row in rows:
                        y -= rh
                        if row[0] == "__section__":
                            self.label(cont, (rw / 2, y + rh / 2), row[1],
                                       scale=0.8, color=self.pal['gold'], h='center')
                            self.divider(cont, 20, y + 10, rw - 40)
                            continue
                        icon, k, v, btn_label, call = row
                        try:
                            bui.imagewidget(
                                parent=cont, position=(0, y + 2),
                                size=(rw, rh - 4),
                                texture=bui.gettexture('white'),
                                color=self.pal['surface'], opacity=0.5,
                            )
                        except Exception:
                            pass
                        self.label(cont, (10, y + rh / 2), f"{icon}  {k}",
                                   scale=0.62, color=self.pal['text'],
                                   maxwidth=rw - 200)
                        self.label(cont, (rw - 130, y + rh / 2), str(v),
                                   scale=0.6, color=self.pal['dim'],
                                   h='right', maxwidth=110)
                        if btn_label:
                            self.button(cont, (rw - 116, y + 8), (100, 26),
                                        btn_label, call, kind='accent',
                                        text_scale=0.55)
                except Exception as e:
                    log(f"Settings scroll: {e}")
            Net.fetch(self.api, "ally_enrol", cb=cb_enrol)
        Net.fetch(self.api, "ally_settings", cb=cb)

    def _edit_num(self, key, cur):
        def cb(val):
            def res(r):
                if isinstance(r, dict) and 'err' in r:
                    ToastStack.push(str(r['err']), 'error')
                else:
                    ToastStack.push(L('saved'), 'success')
                    self._reload()
            Net.fetch(self.api, "ally_save_setting", (key, val), cb=res)
        NumberInputDialog(L(key), cur, cb)

    def _edit_enrol(self, key, cur):
        labels = {'coin': L('min_coin'), 'top': L('top'), 'score': L('score')}
        def cb(val):
            def res(r):
                if isinstance(r, dict) and 'err' in r:
                    ToastStack.push(str(r['err']), 'error')
                else:
                    ToastStack.push(L('saved'), 'success')
                    self._reload()
            Net.fetch(self.api, "ally_set_enrol", (key, val), cb=res)
        NumberInputDialog(labels.get(key, key), cur, cb)

    def _buy_cap(self):
        def cb(r):
            ok = (r == "1")
            ToastStack.push(L('success') if ok else L('fail'),
                            'success' if ok else 'error')
            if ok:
                self._reload()
        Net.fetch(self.api, "ally_capacity", cb=cb)

    def _change_mode(self):
        opts = [(None, L('direct')),
                (1, L('reqmode')),
                (-1, L('closed'))]

        def picked(req):
            def res(r):
                ToastStack.push(L('saved'), 'success')
                self._reload()
            Net.fetch(self.api, "ally_set_enrol", ("request", req), cb=res)
        SelectDialog(L('join_mode'), opts, picked)

    def _toggle_bot(self):
        def res(r):
            ToastStack.push(L('saved'), 'success')
            self._reload()
        Net.fetch(self.api, "ally_set_enrol", ("bot", 1), cb=res)

    # ═══════════════════════ RANKING ═══════════════════════

    def _tab_ranking(self):
        c, tok = self._content, self._tok
        CW, CH = self._content_w, self._content_h
        if not c or CW <= 0 or CH <= 0:
            return

        self.label(c, (CW / 2, CH - 24), L('ranking'),
                   scale=1.0, color=self.pal['gold'], h='center')
        self.divider(c, 20, CH - 40, CW - 40)

        def cb(r):
            if not self._alive(tok) or not isinstance(r, dict):
                return
            if not c.exists():
                return
            if not r.get('rank'):
                self.label(c, (CW / 2, CH / 2), L('not_ranked'),
                           scale=0.9, color=self.pal['dim'], h='center')
                return

            self.make_card(20, CH - 130, CW - 40, 80, r=14, kind='surface_hi')
            self.label(c, (CW / 2, CH - 72), f"#{r.get('rank')}",
                       scale=2.2, color=self.pal['gold'], h='center')
            self.label(c, (CW / 2, CH - 106),
                       f"{float(r.get('score', 0)):.2f} pts",
                       scale=0.72, color=self.pal['success'], h='center')

            mdata = r.get('m_data') or {}
            effective = [m for m in mdata.values() if m.get('c') == 1]
            if not effective:
                return

            top3 = sorted(effective, key=lambda x: -float(x.get('s', 0)))[:3]
            podium_y = max(60, CH - 200)

            medals = [("1", self.pal['gold']),
                      ("2", self.pal['silver']),
                      ("3", self.pal['bronze'])]

            pw = max(50, (CW - 40) / 3)
            for i, m in enumerate(top3):
                px = 20 + i * pw
                try:
                    self.make_card(px + 4, podium_y, pw - 8, 60, r=10, kind='surface')
                    self.label(c, (px + pw / 2, podium_y + 42), medals[i][0],
                               scale=1.2, color=medals[i][1], h='center')
                    self.label(c, (px + pw / 2, podium_y + 22), m.get('n', '?'),
                               scale=0.55, color=self.pal['text'],
                               h='center', maxwidth=pw - 12)
                    self.label(c, (px + pw / 2, podium_y + 8),
                               f"{float(m.get('s', 0)):.1f}",
                               scale=0.5, color=self.pal['success'], h='center')
                except Exception:
                    pass

            remaining = effective[3:] if len(effective) > 3 else []
            if not remaining:
                return

            scroll_h = max(50, podium_y - 8)
            try:
                sc = bui.scrollwidget(
                    parent=c, position=(0, 0),
                    size=(CW, scroll_h),
                    color=(0.4, 0.6, 0.3), border_opacity=0.0,
                )
                rh = 32
                hh = max(rh * len(remaining) + 10, scroll_h)
                cont = bui.containerwidget(parent=sc, size=(max(50, CW - 12), hh), background=False)
                rw = CW - 12
                y = hh
                for m in remaining:
                    y -= rh
                    try:
                        bui.imagewidget(
                            parent=cont, position=(0, y + 2),
                            size=(rw, rh - 4),
                            texture=bui.gettexture('white'),
                            color=self.pal['surface'], opacity=0.5,
                        )
                    except Exception:
                        pass
                    self.label(cont, (10, y + rh / 2),
                               f"#{m.get('r', '?')}", scale=0.55,
                               color=self.pal['dim'])
                    self.label(cont, (60, y + rh / 2), m.get('n', '?'),
                               scale=0.62, color=self.pal['text'],
                               maxwidth=rw - 150)
                    self.label(cont, (rw - 20, y + rh / 2),
                               f"{float(m.get('s', 0)):.1f}",
                               scale=0.6, color=self.pal['success'], h='right')
            except Exception as e:
                log(f"Ranking scroll: {e}")
        Net.fetch(self.api, "ally_ranking", cb=cb)

    # ═══════════════════════ NEWS ═══════════════════════

    def _tab_news(self):
        self._news = []
        self._load_news(None)

    def _load_news(self, offset):
        tok = self._tok
        def cb(page):
            if not self._alive(tok):
                return
            if isinstance(page, list):
                self._news.extend(page)
            self._render_news(tok, isinstance(page, list) and len(page) == 10)
        Net.fetch(self.api, "ally_news", (offset,), cb=cb)

    def _render_news(self, tok, has_more):
        c, CW, CH = self._content, self._content_w, self._content_h
        if not c or CW <= 0 or CH <= 0:
            return
        if not c.exists():
            return
        try:
            for ch in c.get_children():
                ch.delete()
        except Exception:
            pass
        news = self._news
        if not news:
            self.label(c, (CW / 2, CH / 2), L('no_news'),
                       scale=0.9, color=self.pal['dim'], h='center')
            return

        bottom = 40 if has_more else 0
        scroll_h = max(50, CH - bottom)
        try:
            sc = bui.scrollwidget(
                parent=c, position=(0, bottom),
                size=(CW, scroll_h),
                color=(0.4, 0.6, 0.3), border_opacity=0.0,
            )
            rh = 56
            hh = max(rh * len(news) + 10, scroll_h)
            cont = bui.containerwidget(parent=sc, size=(max(50, CW - 12), hh), background=False)
            rw = CW - 12
            y = hh

            for n in news:
                y -= rh
                try:
                    bui.imagewidget(
                        parent=cont, position=(0, y + 2),
                        size=(rw, rh - 4),
                        texture=bui.gettexture('white'),
                        color=self.pal['surface'], opacity=0.5,
                    )
                    bui.imagewidget(
                        parent=cont, position=(4, y + 8),
                        size=(3, rh - 16),
                        texture=bui.gettexture('white'),
                        color=self.pal['accent'],
                    )
                except Exception:
                    pass
                self.label(cont, (16, y + rh - 20), n.get('text', ''),
                           scale=0.6, color=self.pal['text'],
                           maxwidth=rw - 30)
                self.label(cont, (16, y + 12), n.get('time', ''),
                           scale=0.48, color=self.pal['dim'])
        except Exception as e:
            log(f"News scroll: {e}")
            return

        if has_more and news:
            self.button(c, (CW / 2 - 70, 4), (140, 32),
                        L('more'),
                        MyCall(self._load_news, news[-1].get('id')),
                        kind='accent', text_scale=0.6)

    # ═══════════════════════ CHAT ═══════════════════════

    def _tab_chat(self):
        c, tok = self._content, self._tok
        CW, CH = self._content_w, self._content_h
        if not c or CW <= 0 or CH <= 0:
            return

        self.label(c, (CW / 2, CH - 24), L('chat'),
                   scale=1.0, color=self.pal['gold'], h='center')
        self.divider(c, 20, CH - 40, CW - 40)

        self._chat_sig = None
        scroll_h = max(50, CH - 96)
        try:
            self._chat_scroll = bui.scrollwidget(
                parent=c, position=(0, 48),
                size=(CW, scroll_h),
                color=(0.4, 0.6, 0.3), border_opacity=0.0,
            )
            self._chat_cont = bui.containerwidget(
                parent=self._chat_scroll,
                size=(max(50, CW - 12), scroll_h), background=False,
            )
        except Exception as e:
            log(f"Chat init: {e}")
            return

        self._chat_inp = self.field(c, (0, 4), (max(50, CW - 92), 38),
                                    "", max_chars=200, desc=L('msg_hint'))
        self.button(c, (CW - 86, 4), (86, 38),
                    L('send'), MyCall(self._send_chat),
                    kind='accent', text_scale=0.6)

        self._refresh_chat(tok, True)

    def _refresh_chat(self, tok, loop):
        def cb(history):
            if not self._alive(tok) or self.tab != 'chat':
                return
            if isinstance(history, list):
                sig = (len(history), str(history[-1]) if history else "")
                if sig != self._chat_sig:
                    self._chat_sig = sig
                    try:
                        self._render_chat(history[-60:])
                    except Exception as e:
                        log(f"chat render: {e}")
            if loop and self._alive_flag and self.tab == 'chat':
                _later(3.0, MyCall(self._refresh_chat, tok, True))
        Net.fetch(self.api, "ally_chat_history", cb=cb)

    def _render_chat(self, msgs):
        CW, CH = self._content_w, self._content_h
        if not self._chat_cont:
            return
        if not self._chat_cont.exists():
            return
        try:
            for ch in self._chat_cont.get_children():
                ch.delete()
        except Exception:
            pass
        rh = 30
        hh = max(rh * len(msgs) + 10, CH - 96)
        try:
            bui.containerwidget(edit=self._chat_cont, size=(max(50, CW - 12), hh))
        except Exception:
            pass
        y = hh
        for m in msgs:
            y -= rh
            mine = m.get('name') == self.api.user
            col = self.pal['success'] if mine else self.pal['text']
            prefix = ">" if mine else "-"
            self.label(self._chat_cont, (8, y + rh / 2),
                       f"{prefix} {m.get('name')}: {m.get('chat')}",
                       scale=0.6, color=col, maxwidth=CW - 30)
        try:
            bui.scrollwidget(edit=self._chat_scroll, vertical_scroll=0.0)
        except Exception:
            pass

    def _send_chat(self):
        if not self._chat_inp:
            return
        try:
            msg = (bui.textwidget(query=self._chat_inp) or '').strip()
        except Exception:
            return
        if not msg:
            return
        try:
            bui.textwidget(edit=self._chat_inp, text="")
        except Exception:
            pass
        tok = self._tok
        Net.fetch(self.api, "ally_chat_send", (msg,),
                  cb=lambda r: self._refresh_chat(tok, False))

    # ═══════════════════════ CHANNELS ═══════════════════════

    def _tab_channels(self):
        c, CW, CH = self._content, self._content_w, self._content_h
        if not c or CW <= 0 or CH <= 0:
            return

        self.label(c, (CW / 2, CH - 24), L('channels'),
                   scale=1.0, color=self.pal['gold'], h='center')
        self.divider(c, 20, CH - 40, CW - 40)

        self.make_card(40, CH - 200, CW - 80, 140, r=16, kind='surface_hi')
        self.label(c, (CW / 2, CH - 85), "*",
                   scale=3.5, color=self.pal['gold'], h='center')
        self.label(c, (CW / 2, CH - 128), CHANNEL_NAME,
                   scale=1.4, color=self.pal['text'], h='center')
        self.label(c, (CW / 2, CH - 156), CHANNEL_HANDLE,
                   scale=0.75, color=self.pal['dim'], h='center')

        self.button(c, (CW / 2 - 130, CH - 226), (260, 48),
                    L('open'), MyCall(self._open_channel),
                    kind='accent', text_scale=0.85)

    def _open_channel(self):
        try:
            bui.open_url(CHANNEL_URL)
        except Exception as e:
            log(f"open_url: {e}")
            try:
                if bui.clipboard_is_supported():
                    bui.clipboard_set_text(CHANNEL_URL)
                    ToastStack.push(CHANNEL_URL, 'info')
            except Exception:
                pass


# ═══════════════════════════════════════════════════════════════
# MEMBER ACTION WINDOW
# ═══════════════════════════════════════════════════════════════

class MemberActionWindow(Dialog):
    COLORS = [("white", (1, 1, 1)), ("red", (1, 0.3, 0.3)),
              ("blue", (0.3, 0.6, 1)), ("green", (0.3, 1, 0.3)),
              ("yellow", (1, 1, 0.2)), ("orange", (1, 0.6, 0.2))]

    def __init__(self, api, member, on_refresh):
        W, H = 440, 380
        super().__init__(W, H, f"{L('manage')}: {member.get('name', '?')}")
        self.api = api
        self.member = member
        self.on_refresh = on_refresh

        existing_color = (member.get('title') or {}).get('c', 'white')
        if not any(c[0] == existing_color for c in self.COLORS):
            existing_color = "white"
        self.color_choice = existing_color

        self.make_card(12, 74, W - 24, H - 148, r=12, kind='surface')

        self.label(self.root, (28, H - 100), L('title'),
                   scale=0.62, color=self.pal['dim'])
        self.inp_title = self.field(self.root, (100, H - 126),
                                    (W - 130, 38),
                                    (member.get('title') or {}).get('t', ''),
                                    max_chars=20, desc=L('title'))

        self.label(self.root, (28, H - 160), L('color'),
                   scale=0.62, color=self.pal['dim'])
        self._swatches = []
        x = 100
        for cname, crgb in self.COLORS:
            try:
                b = bui.buttonwidget(
                    parent=self.root, position=(x, H - 178), size=(42, 32),
                    label="*" if cname == existing_color else "",
                    color=crgb, textcolor=(0, 0, 0),
                    button_type='square', autoselect=True,
                    text_scale=0.7,
                    on_activate_call=MyCall(self._pick_color, cname),
                    texture=bui.gettexture('buttonSquare'),
                )
                self._swatches.append((b, cname))
            except Exception:
                pass
            x += 48

        self.button(self.root, (28, H - 226), (W - 56, 40),
                    L('apply_title'), MyCall(self._apply_title),
                    kind='success', text_scale=0.7)

        self.button(self.root, (28, H - 274), (W - 56, 40),
                    L('change_role'),
                    MyCall(self._open_role), kind='accent', text_scale=0.7)

        muted = member.get('muted')
        self.button(self.root, (28, 24), (180, 42),
                    L('unmute') if muted else L('mute'),
                    MyCall(self._toggle_mute),
                    kind='success' if muted else 'surface', text_scale=0.65)
        self.button(self.root, (W - 208, 24), (180, 42),
                    L('kick'), MyCall(self._kick),
                    kind='danger', text_scale=0.65)

    def _pick_color(self, name):
        self.color_choice = name
        for b, n in self._swatches:
            try:
                bui.buttonwidget(edit=b, label="*" if n == name else "")
            except Exception:
                pass

    def _done(self, *_):
        self.close()
        try:
            self.on_refresh()
        except Exception:
            pass

    def _apply_title(self):
        if not self.inp_title:
            return
        try:
            title = (bui.textwidget(query=self.inp_title) or '').strip()
        except Exception:
            return
        Net.fetch(self.api, "ally_change_title",
                  (self.member['id'], title, self.color_choice),
                  cb=self._done)

    def _open_role(self):
        opts = [
            (2, L('general')),
            (3, L('spy')),
            (None, L('remove_role')),
        ]

        def picked(role):
            def cb(r):
                if r == "1":
                    ToastStack.push(L('role_changed'), 'success')
                    AlertDialog(L('success'), L('role_changed'),
                                kind='success', on_ok=self._done)
                else:
                    msg = {"too_many": L('role_full'),
                           "no_bot": L('no_bot')}.get(r, L('fail'))
                    AlertDialog(L('fail'), msg, kind='error')
            Net.fetch(self.api, "ally_change_role",
                      (self.member['id'], role), cb=cb)
        SelectDialog(L('select'), opts, picked)

    def _toggle_mute(self):
        typ = "unmute" if self.member.get('muted') else "mute"
        Net.fetch(self.api, "ally_mute",
                  (self.member.get('name'), typ), cb=self._done)

    def _kick(self):
        def do():
            Net.fetch(self.api, "ally_kick",
                      (self.member['id'],), cb=self._done)
        ConfirmDialog(L('kick'),
                      f"{L('kick')}: {self.member.get('name', '?')} ?",
                      do, danger=True)


# ═══════════════════════════════════════════════════════════════
# VAULT WINDOWS
# ═══════════════════════════════════════════════════════════════

class VaultHistoryWindow(Dialog):
    def __init__(self, api):
        W, H = 540, 420
        super().__init__(W, H, L('vault_hist'))
        self.api = api

        self._box = bui.containerwidget(
            parent=self.root, position=(20, 20),
            size=(max(50, W - 40), max(50, H - 98)), background=False,
        )
        self.label(self._box, ((W - 40) / 2, (H - 98) / 2),
                   L('loading') + "...", scale=0.8,
                   color=self.pal['dim'], h='center')

        Net.fetch(api, "ally_vault_news", (None,), cb=self._cb)

    def _cb(self, news):
        if not self.root.exists() or not self._box.exists():
            return
        try:
            for c in self._box.get_children():
                c.delete()
        except Exception:
            pass
        if not isinstance(news, list) or not news:
            self.label(self._box, ((self.W - 40) / 2, (self.H - 98) / 2),
                       L('no_news'), scale=0.8,
                       color=self.pal['dim'], h='center')
            return

        CW = max(50, self.W - 40)
        CH = max(50, self.H - 98)
        try:
            sc = bui.scrollwidget(
                parent=self._box, position=(0, 0),
                size=(CW, CH),
                color=(0.4, 0.6, 0.3), border_opacity=0.0,
            )
            rh = 42
            hh = max(rh * len(news) + 10, CH)
            cont = bui.containerwidget(parent=sc, size=(max(50, CW - 12), hh), background=False)
            rw = CW - 12
            y = hh

            for n in news:
                y -= rh
                try:
                    bui.imagewidget(
                        parent=cont, position=(0, y + 2),
                        size=(rw, rh - 4),
                        texture=bui.gettexture('white'),
                        color=self.pal['surface'], opacity=0.5,
                    )
                except Exception:
                    pass
                self.label(cont, (10, y + rh / 2), n.get('text', ''),
                           scale=0.6, color=self.pal['text'],
                           maxwidth=rw - 120)
                if n.get('is_parent'):
                    self.button(cont, (rw - 100, y + 8), (90, 26),
                                L('shares'),
                                MyCall(self._open_shares, n.get('id')),
                                kind='accent', text_scale=0.5)
        except Exception as e:
            log(f"Vault history: {e}")

    def _open_shares(self, tid):
        VaultSharesWindow(self.api, tid)


class VaultSharesWindow(Dialog):
    def __init__(self, api, tid):
        W, H = 400, 360
        super().__init__(W, H, L('shares'))
        self._box = bui.containerwidget(
            parent=self.root, position=(20, 20),
            size=(max(50, W - 40), max(50, H - 98)), background=False,
        )
        self.label(self._box, ((W - 40) / 2, (H - 98) / 2),
                   L('loading') + "...", scale=0.8,
                   color=self.pal['dim'], h='center')

        def cb(shares):
            if not self.root.exists() or not self._box.exists():
                return
            try:
                for c in self._box.get_children():
                    c.delete()
            except Exception:
                pass
            if not isinstance(shares, list) or not shares:
                self.label(self._box, ((W - 40) / 2, (H - 98) / 2),
                           L('empty'), scale=0.8,
                           color=self.pal['dim'], h='center')
                return

            CW = max(50, W - 40)
            CH = max(50, H - 98)
            try:
                sc = bui.scrollwidget(
                    parent=self._box, position=(0, 0),
                    size=(CW, CH),
                    color=(0.4, 0.6, 0.3), border_opacity=0.0,
                )
                rh = 32
                hh = max(rh * len(shares) + 10, CH)
                cont = bui.containerwidget(parent=sc, size=(max(50, CW - 12), hh), background=False)
                rw = CW - 12
                y = hh
                for s in shares:
                    y -= rh
                    try:
                        bui.imagewidget(
                            parent=cont, position=(0, y + 2),
                            size=(rw, rh - 4),
                            texture=bui.gettexture('white'),
                            color=self.pal['surface'], opacity=0.5,
                        )
                    except Exception:
                        pass
                    self.label(cont, (10, y + rh / 2), s.get('name', '?'),
                               scale=0.6, color=self.pal['text'],
                               maxwidth=rw - 120)
                    self.label(cont, (rw - 10, y + rh / 2), fmt(s.get('val', 0)),
                               scale=0.6, color=self.pal['success'], h='right')
            except Exception as e:
                log(f"Shares scroll: {e}")
        Net.fetch(api, "ally_vault_shares", (tid,), cb=cb)


# ═══════════════════════════════════════════════════════════════
# HUB WINDOW
# ═══════════════════════════════════════════════════════════════

class HubWindow(BaseWindow):
    def __init__(self, api):
        W, H = 680, win_h()
        super().__init__(W, H)
        self.api = api
        self._tab = "join"
        self._order = "rank"
        self._sub = None

        self.make_card(12, H - 76, W - 24, 64, r=16, kind='header')
        self._title = self.label(
            self.root, (32, H - 48), u"\ue010  " + L('hub'),
            scale=1.0, color=self.pal['gold'], maxwidth=400,
        )
        self.label(self.root, (32, H - 66), L('no_ally'),
                   scale=0.5, color=self.pal['dim'])

        self.button(self.root, (W - 206, H - 62), (60, 38), "o",
                    MyCall(self.cycle_theme), kind='surface')
        self.button(self.root, (W - 138, H - 62), (54, 38), L('style'),
                    MyCall(self.cycle_theme), kind='surface', text_scale=0.55)
        self.button(self.root, (W - 76, H - 62), (60, 38), L('logout'),
                    MyCall(self._logout), kind='danger', text_scale=0.55)

        try:
            cb = bui.buttonwidget(
                parent=self.root, position=(16, H - 66), size=(46, 46),
                label=bui.charstr(bui.SpecialChar.CLOSE),
                color=self.pal['danger'], textcolor=(1, 1, 1),
                button_type='square', text_scale=0.9,
                on_activate_call=MyCall(self.close_sound),
                texture=bui.gettexture('buttonSquare'),
            )
            bui.containerwidget(edit=self.root, cancel_button=cb)
        except Exception:
            pass

        # Tab buttons
        ty = H - 76 - 50
        self._create_btn = self.button(
            self.root, (16, ty), ((W - 32) / 2 - 4, 44),
            L('create'), MyCall(self._switch_tab, "create"),
            kind='surface', text_scale=0.85,
        )
        self._join_btn = self.button(
            self.root, (W / 2 + 4, ty), ((W - 32) / 2 - 4, 44),
            L('join'), MyCall(self._switch_tab, "join"),
            kind='accent', text_scale=0.85,
        )

        self._content_y = 16
        self._content_h = ty - 16 - 12
        self._content_x = 16
        self._content_w = W - 32
        self.make_card(12, self._content_y, W - 24, self._content_h,
                       r=14, kind='surface')
        self._new_sub()

        self._switch_tab("join")

    def _on_tick(self, elapsed, pal):
        try:
            if self._title:
                bui.textwidget(edit=self._title, color=pal['gold'])
        except Exception:
            pass

    def _new_sub(self):
        if self._sub is not None:
            try:
                self._sub.delete()
            except Exception:
                pass
        self._sub = bui.containerwidget(
            parent=self.root,
            position=(self._content_x, self._content_y),
            size=(self._content_w, self._content_h),
            background=False,
        )

    def _switch_tab(self, tab):
        self._tab = tab
        c_acc = self.pal['accent']
        c_surf = self.pal['surface_hi']
        try:
            if self._create_btn:
                bui.buttonwidget(edit=self._create_btn,
                                 color=c_acc if tab == "create" else c_surf)
            if self._join_btn:
                bui.buttonwidget(edit=self._join_btn,
                                 color=c_acc if tab == "join" else c_surf)
        except Exception:
            pass
        self._new_sub()
        if tab == "create":
            self._render_create()
        else:
            self._render_join()

    def _render_create(self):
        c = self._sub
        CW, CH = self._content_w, self._content_h
        if not c or CW <= 0 or CH <= 0:
            return

        def cb(st):
            if not self.root.exists() or not self._alive_flag:
                return
            if not c.exists():
                return
            if not isinstance(st, dict) or 'price' not in st:
                if st == "0":
                    AlertDialog(L('error'), L('already_ally'), kind='error')
                else:
                    AlertDialog(L('error'), str(st), kind='error')
                return

            self.make_card(40, CH - 130, CW - 80, 90, r=12, kind='surface_hi')
            self.label(c, (CW / 2, CH - 78), L('cost'),
                       scale=0.7, color=self.pal['dim'], h='center')
            self.label(c, (CW / 2, CH - 108), f"{fmt(st['price'])} {L('coins')}",
                       scale=1.2, color=self.pal['gold'], h='center')

            self.label(c, (CW / 2, CH - 168), L('name_hint'),
                       scale=0.62, color=self.pal['dim'], h='center')
            self.inp_name = self.field(c, (CW / 2 - 150, CH - 216),
                                       (300, 40), "", max_chars=15,
                                       desc=L('name_hint'))

            self.button(c, (CW / 2 - 110, CH - 276), (220, 48),
                        L('create'),
                        MyCall(self._do_create), kind='accent',
                        text_scale=0.85)

        Net.fetch(self.api, "create_status", cb=cb)

    def _do_create(self):
        if not self.inp_name:
            return
        try:
            name = (bui.textwidget(query=self.inp_name) or '').strip()
        except Exception:
            return
        if not name:
            AlertDialog(L('error'), L('name_hint'), kind='error')
            return

        def cb1(r1):
            if r1 == "confirm_needed":
                def cb2(r2):
                    if isinstance(r2, dict) and "url" in r2:
                        self._go_main()
                    elif isinstance(r2, dict) and "err" in r2:
                        AlertDialog(L('error'), str(r2['err']), kind='error')
                    else:
                        AlertDialog(L('error'), L('fail'), kind='error')
                Net.fetch(self.api, "create_ally", (name, 1), cb=cb2)
            elif r1 == "already_in_ally":
                AlertDialog(L('error'), L('already_ally'), kind='error')
            elif isinstance(r1, dict) and "err" in r1:
                AlertDialog(L('error'), str(r1['err']), kind='error')
            else:
                AlertDialog(L('error'), L('fail'), kind='error')
        Net.fetch(self.api, "create_ally", (name, 0), cb=cb1)

    def _render_join(self):
        c = self._sub
        CW, CH = self._content_w, self._content_h
        if not c or CW <= 0 or CH <= 0:
            return

        self.inp_search = self.field(c, (10, CH - 50), (max(50, CW - 130), 40),
                                     "", max_chars=30, desc=L('search_hint'))
        self.button(c, (CW - 116, CH - 50), (106, 40),
                    L('search'), MyCall(self._do_join_search),
                    kind='accent', text_scale=0.65)

        orders = [("rank", L('rank_by')),
                  ("new", L('newest')),
                  ("old", L('oldest')),
                  ("count", L('most'))]
        bw = max(50, (CW - 20 - 3 * 6) / 4)
        for i, (code, label) in enumerate(orders):
            kind = 'accent' if code == self._order else 'surface'
            self.button(c, (10 + i * (bw + 6), CH - 96),
                        (bw, 32), label,
                        MyCall(self._set_order, code),
                        kind=kind, text_scale=0.6)

        self._join_box = bui.containerwidget(
            parent=c, position=(10, 10),
            size=(max(50, CW - 20), max(50, CH - 116)),
            background=False,
        )
        self._do_join_search()

    def _set_order(self, code):
        self._order = code
        self._new_sub()
        self._render_join()

    def _do_join_search(self):
        if not self.inp_search:
            return
        try:
            search = (bui.textwidget(query=self.inp_search) or '').strip()
        except Exception:
            search = ""
        order = self._order
        box = self._join_box
        CW = max(50, self._content_w - 20)
        CH = max(50, self._content_h - 116)

        def cb(allies):
            if self._tab != "join" or not self.root.exists() or order != self._order:
                return
            if not box or not box.exists():
                return
            try:
                for c in box.get_children():
                    c.delete()
            except Exception:
                pass
            if not isinstance(allies, list):
                return
            visible = [a for a in allies if a.get('request') != -1]
            if not visible:
                self.label(box, (CW / 2, CH / 2), L('empty'),
                           scale=0.8, color=self.pal['dim'], h='center')
                return

            try:
                sc = bui.scrollwidget(
                    parent=box, position=(0, 0), size=(CW, CH),
                    color=(0.4, 0.6, 0.3), border_opacity=0.0,
                )
                rh = 42
                hh = max(rh * len(visible) + 10, CH)
                cont = bui.containerwidget(parent=sc, size=(max(50, CW - 12), hh), background=False)
                rw = CW - 12
                y = hh
                for a in visible:
                    y -= rh
                    is_req = a.get('request') == 1
                    try:
                        bui.imagewidget(
                            parent=cont, position=(0, y + 2),
                            size=(rw, rh - 4),
                            texture=bui.gettexture('white'),
                            color=self.pal['surface'], opacity=0.5,
                        )
                    except Exception:
                        pass
                    self.label(cont, (10, y + rh / 2),
                               f"#{a.get('rank') or '-'}",
                               scale=0.55, color=self.pal['gold'],
                               maxwidth=40)
                    self.label(cont, (60, y + rh / 2),
                               a.get('name', '?'), scale=0.7,
                               color=self.pal['text'], maxwidth=rw - 200)
                    self.button(cont, (rw - 128, y + 8), (120, 28),
                                L('request') if is_req else L('join'),
                                MyCall(self._do_join, a),
                                kind='accent' if is_req else 'success',
                                text_scale=0.6)
            except Exception as e:
                log(f"Join search scroll: {e}")
        Net.fetch(self.api, "list_allies", (search, order), cb=cb)

    def _do_join(self, a):
        def cb(r):
            if r == "requested":
                ToastStack.push(L('req_sent'), 'success')
                AlertDialog(L('success'), L('req_sent'), kind='success')
            elif (r in ("./post/Ally", "./post.php?post=Ally")
                  or (isinstance(r, str) and "post=Ally" in r)
                  or r == "already_in_ally"):
                self._go_main(0.9)
            elif r == "request_rejected":
                AlertDialog(L('fail'), L('req_rejected'), kind='error')
            elif r == "request_unseen":
                AlertDialog(L('fail'), L('pending'), kind='error')
            elif r == "already_left":
                AlertDialog(L('fail'), L('left_recent'), kind='error')
            else:
                reason = L('no_req')
                reqs = []
                if a.get('coin'):
                    reqs.append(f"{L('min_coin')}: {a['coin']}")
                if a.get('top'):
                    reqs.append(f"{L('top')}: {a['top']}")
                if a.get('score'):
                    reqs.append(f"{L('score')}: {a['score']}")
                if a.get('bot'):
                    reqs.append(L('bot'))
                if reqs:
                    reason += f"\n\n{L('needed')}:\n- " + "\n- ".join(reqs)
                AlertDialog(L('fail'), reason, kind='error')
        Net.fetch(self.api, "join_ally", (a['id'],), cb=cb)

    def _go_main(self, delay=0.8):
        self.close()
        _later(delay, MyCall(_route))

    def _logout(self):
        self.api.logout()
        self.close()
        _later(0.3, MyCall(LoginWindow, self.api, _route))


# ═══════════════════════════════════════════════════════════════
# ROUTER
# ═══════════════════════════════════════════════════════════════

def _get_api():
    global _api_singleton
    if _api_singleton is None:
        _api_singleton = BslifeAPI()
    return _api_singleton


def _route():
    global _opening, _top_win
    with _router_lock:
        _opening = False
        api = _get_api()
        if _top_win is not None:
            try:
                _top_win.close()
            except Exception:
                pass
            _top_win = None
        _close_all_dialogs()

        def cb(st):
            if st in ("3", "0", "", None):
                api.logout()
                LoginWindow(api, _route)
                return
            if isinstance(st, dict) and "name" in st:
                MainWindow(api)
            elif isinstance(st, dict) and "error" in st:
                AlertDialog(L('error'), str(st['error']), kind='error')
            else:
                HubWindow(api)

        Net.fetch(api, "ally_status", cb=cb)


def open_manager():
    global _opening
    with _router_lock:
        try:
            if _top_win is not None and _top_win.root.exists():
                return
        except Exception:
            pass
        if _opening:
            return
        _opening = True
    api = _get_api()

    def cb(who):
        global _opening
        _opening = False
        if not who:
            LoginWindow(api, _route)
        else:
            _route()
    Net.fetch(api, "whoami", cb=cb)


# ═══════════════════════════════════════════════════════════════
# PARTY HOOK
# ═══════════════════════════════════════════════════════════════

def _add_btn(win):
    try:
        root = win._root_widget
        if hasattr(win, '_W') and hasattr(win, '_H'):
            W, H = win._W, win._H
            pos = (W - 10 - 6 - 40 - 8 - 64 - 8 - 40, H - 10 - 54 + 9)
            size = (40, 36)
        else:
            width = getattr(win, "_width", 600)
            height = getattr(win, "_height", 500)
            sz = width / 15.0
            pos = (width - width / 30.0, height - 135.0)
            size = (sz, sz)

        base = _theme_rgb(_theme_current()[1], time.time() - _FX_T0)
        pal = _palette(base)
        bui.buttonwidget(
            parent=root, size=size, position=pos,
            label=u"\ue010", button_type="square",
            autoselect=False,
            color=pal['accent'], textcolor=(1, 1, 1),
            on_activate_call=MyCall(open_manager),
        )
    except Exception as e:
        log(f"Patch: {e}")


def _patch():
    orig = party.PartyWindow
    if isinstance(orig, type):
        if getattr(orig, '_bslife_v11', False):
            return
        orig_init = orig.__init__

        def patched(self, *a, **k):
            orig_init(self, *a, **k)
            _add_btn(self)
        orig.__init__ = patched
        orig._bslife_v11 = True
    else:
        def wrapper(*a, **k):
            win = orig(*a, **k)
            _add_btn(win)
            return win
        party.PartyWindow = wrapper


# ba_meta export babase.Plugin
class BSLifeAllyMod(babase.Plugin):
    def on_app_running(self):
        log("--- BSLIFE v11.1 STABLE loaded ---")
        _patch()


print("BSLIFE Ally Manager v11.1 STABLE - @Tajerbetbot")