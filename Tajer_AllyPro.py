# ba_meta require api 9
# BSLIFE Ally Manager — VALHALLA FULL EDITION
# Made with Tajer and Windows
# api 9
# mod is Free

from __future__ import annotations

import babase
import bauiv1 as bui
import bascenev1 as bs
from bauiv1lib import party

import urllib.request
import urllib.error
import http.cookiejar
import ssl
import json
import os
import threading
import time

# ═══════════════════════════════════════════════════════════════
# 🛠️ SETTINGS & COLORS (Valhalla Theme)
# ═══════════════════════════════════════════════════════════════

WIN_W = 780
WIN_H = 520
TAB_H = 45
TAB_GAP = 8
TAB_START_Y = 400

BASE_URL = "https://bslife.ir"
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".bslife_ally")
os.makedirs(DATA_DIR, exist_ok=True)
SESSION_FILE = os.path.join(DATA_DIR, "session.json")
LOG_FILE = os.path.join(DATA_DIR, "bslife_debug.log")

# 🎨 Valhalla Gold/Dark Palette
COL_BG          = (0.04, 0.03, 0.02)  # سنگ سیاه
COL_SIDEBAR_BG  = (0.08, 0.06, 0.04)  # پنل تاریک
COL_CONTENT_BG  = (0.08, 0.06, 0.04)  # پنل تاریک
COL_PANEL       = (0.10, 0.08, 0.05)  # پنل دکمه
COL_ACCENT      = (0.85, 0.65, 0.15)  # طلایی اصلی
COL_ACCENT2     = (0.40, 0.25, 0.05)  # طلایی تیره
COL_GOLD        = (1.00, 0.85, 0.35)  # طلایی درخشان (متن)
COL_TEXT        = (0.95, 0.90, 0.80)  # متن کرم
COL_DIM         = (0.60, 0.55, 0.50)  # متن خاکستری
COL_GREEN       = (0.20, 0.70, 0.30)  # سبز
COL_RED         = (0.70, 0.15, 0.10)  # قرمز

MyCall = getattr(bui, 'CallPartial', bui.Call)

def safe_containerwidget(**kwargs):
    try: return bui.containerwidget(**kwargs)
    except TypeError:
        kwargs.pop('scale_origin_stack_position', None)
        kwargs.pop('stack_offset', None)
        return bui.containerwidget(**kwargs)

def _safe_timer(delay, call):
    try: return bs.AppTimer(delay, call)
    except Exception:
        try: return bui.apptimer(delay, call)
        except Exception: pass

# ═══════════════════════════════════════════════════════════════
# 🌐 LANGUAGE
# ═══════════════════════════════════════════════════════════════

def get_is_persian():
    try:
        lang = bui.app.lang.language
        return lang == "Persian" or lang == "fa" or lang == "Farsi"
    except Exception:
        return False

IS_FA = get_is_persian()

T = {
    "login": {"fa": "ورود", "en": "Login"},
    "logout": {"fa": "خروج", "en": "Logout"},
    "cancel": {"fa": "انصراف", "en": "Cancel"},
    "overview": {"fa": "مرور کلی", "en": "Overview"},
    "members": {"fa": "اعضا", "en": "Members"},
    "requests": {"fa": "درخواست‌ها", "en": "Requests"},
    "vault": {"fa": "خزانه", "en": "Vault"},
    "settings": {"fa": "تنظیمات", "en": "Settings"},
    "ranking": {"fa": "رنکینگ", "en": "Ranking"},
    "chat": {"fa": "چت", "en": "Chat"},
    "news": {"fa": "اخبار", "en": "News"},
    "channels": {"fa": "کانال‌ها", "en": "Channels"},
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
    "split": {"fa": "تقسیم خزانه", "en": "Split Vault"},
    "capacity": {"fa": "ظرفیت", "en": "Capacity"},
    "buy_1": {"fa": "خرید +۱", "en": "Buy +1"},
    "new": {"fa": "جدید", "en": "New"},
    "accepted": {"fa": "تایید شده", "en": "Accepted"},
    "rejected": {"fa": "رد شده", "en": "Rejected"},
    "yes": {"fa": "قبول", "en": "YES"},
    "no": {"fa": "رد", "en": "NO"},
    "ready": {"fa": "آماده", "en": "Ready"},
    "loading": {"fa": "در حال لود...", "en": "Loading..."},
    "session_expired": {"fa": "سشن منقضی شده", "en": "Session expired"},
    "not_ranked": {"fa": "هنوز رتبه‌بندی نشده", "en": "Not ranked yet"},
    "alliance_name": {"fa": "نام اتحاد", "en": "Alliance Name"},
    "your_role": {"fa": "نقش شما", "en": "Your Role"},
    "members_count": {"fa": "تعداد اعضا", "en": "Members Count"},
    "coins": {"fa": "سکه", "en": "Coins"},
    "message": {"fa": "پیام...", "en": "Message..."},
    "send": {"fa": "ارسال", "en": "Send"},
    "error_fill": {"fa": "لطفا هر دو فیلد را پر کنید!", "en": "Please fill both fields!"},
    "logging_in": {"fa": "در حال ورود...", "en": "Logging in..."},
    "success_loading": {"fa": "موفق! در حال لود...", "en": "Success! Loading..."},
    "error": {"fa": "خطا", "en": "Error"},
    "hub_title": {"fa": "مرکز اتحادها", "en": "Alliance Hub"},
    "not_in_ally": {"fa": "شما عضو هیچ اتحادی نیستید.", "en": "You are not in an alliance."},
    "create_ally": {"fa": "ساخت اتحاد", "en": "Create Ally"},
    "join_ally": {"fa": "پیوستن به اتحاد", "en": "Join Ally"},
    "search": {"fa": "جستجو...", "en": "Search..."},
    "cost": {"fa": "هزینه", "en": "Cost"},
    "join": {"fa": "پیوستن", "en": "Join"},
    "user": {"fa": "کاربر", "en": "User"},
    "no_ally": {"fa": "بدون اتحاد", "en": "No Ally"},
    "dismiss": {"fa": "بستن", "en": "Dismiss"},
    "request_sent":      {"fa": "درخواست ارسال شد", "en": "Request sent"},
    "join_success":      {"fa": "ورود به اتحاد موفق", "en": "Joined successfully"},
    "join_fail":         {"fa": "شما شرایط لازم برای ورود را ندارید", "en": "You don't meet the requirements"},
    "ok":                {"fa": "باشه", "en": "OK"},
    "request_btn":       {"fa": "درخواست", "en": "Request"},
    "join_btn":          {"fa": "عضویت", "en": "Join"},
    "confirm":           {"fa": "تایید", "en": "Confirm"},
    "success":           {"fa": "موفق", "en": "Success"},
    "fail":              {"fa": "ناموفق", "en": "Failed"},
    "enter_amount":      {"fa": "مقدار را وارد کنید", "en": "Enter amount"},
    "equal_all":         {"fa": "مساوی بین همه", "en": "Equal: All"},
    "equal_ranking":     {"fa": "مساوی بین ۲۰ برتر", "en": "Equal: Top 20"},
    "ranking_points":    {"fa": "متناسب با امتیاز", "en": "By points"},
    "remove_role":       {"fa": "حذف نقش", "en": "Remove role"},
    "transparency":      {"fa": "شفافیت", "en": "Transparency"},
    "create_fail":       {"fa": "خطا در ساخت اتحاد", "en": "Create failed"},
    "already_in_ally":   {"fa": "شما در اتحاد دیگری هستید", "en": "Already in another ally"},
    "not_enough_coins":  {"fa": "سکه کافی نیست", "en": "Not enough coins"},
    "select_type":       {"fa": "نوع را انتخاب کنید", "en": "Select type"},
    "select_role":       {"fa": "نقش را انتخاب کنید", "en": "Select role"},
    "vault_split_ok":    {"fa": "خزانه تقسیم شد", "en": "Vault split successful"},
    "deposit_ok":        {"fa": "واریز موفق", "en": "Deposit successful"},
    "role_changed":      {"fa": "نقش تغییر کرد", "en": "Role changed"},
    "leave_ally":        {"fa": "خروج از اتحاد", "en": "Leave Ally"},
    "leave_confirm":     {"fa": "آیا مطمئنید می‌خواهید از اتحاد خارج شوید؟", "en": "Are you sure you want to leave the ally?"},
    "vault_news":        {"fa": "تاریخچه خزانه", "en": "Vault History"},
    "vault_shares":      {"fa": "لیست سهام", "en": "Vault Shares"},
    "history":           {"fa": "تاریخچه", "en": "History"},
    "more":              {"fa": "بیشتر", "en": "More"},
    "no_news":           {"fa": "خبری وجود ندارد", "en": "No news available"},
    "gkick":             {"fa": "حذف مجاز جنرال", "en": "General Kick Limit"},
    "spynet":            {"fa": "بودجه Spynet", "en": "Spynet Budget"},
    "tag_status":        {"fa": "وضعیت تگ", "en": "Tag Status"},
    "tag_active":        {"fa": "فعال", "en": "Active"},
    "tag_inactive":      {"fa": "غیرفعال", "en": "Inactive"},
    "sale_price":        {"fa": "فروش اتحاد", "en": "Ally Sale Price"},
    "enrol_settings":    {"fa": "تنظیمات عضوگیری", "en": "Enrolment Settings"},
    "mode_direct":       {"fa": "مستقیم", "en": "Direct"},
    "mode_request":      {"fa": "درخواستی", "en": "Request"},
    "mode_closed":       {"fa": "بسته", "en": "Closed"},
    "min_coin":          {"fa": "حداقل سکه", "en": "Min Coins"},
    "req_top":           {"fa": "رتبه تاپ", "en": "Required Top"},
    "min_score":         {"fa": "حداقل امتیاز", "en": "Min Score"},
    "req_bot":           {"fa": "اجبار به بات", "en": "Require Bot"},
    "saved":             {"fa": "ذخیره شد", "en": "Saved"},
    "order_rank":        {"fa": "رتبه", "en": "Rank"},
    "order_new":         {"fa": "جدیدترین", "en": "Newest"},
    "order_old":         {"fa": "قدیمی‌ترین", "en": "Oldest"},
    "order_count":       {"fa": "بیشترین عضو", "en": "Most Members"},
}

def L(key):
    lang = "fa" if IS_FA else "en"
    return T.get(key, {}).get(lang, key)

# ═══════════════════════════════════════════════════════════════
# 📝 LOGGING & UTILS
# ═══════════════════════════════════════════════════════════════

def log(msg):
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {msg}\n")
    except Exception: pass

def fmt(n):
    try: return f"{int(n):,}"
    except Exception: return str(n)

def role_name(rid):
    return L({1: "leader", 2: "general", 3: "spy"}.get(rid, "member"))

def role_color(rid):
    return {1: COL_GOLD, 2: COL_ACCENT, 3: (0.5, 0.2, 0.7)}.get(rid, COL_DIM)

# ═══════════════════════════════════════════════════════════════
# 🌐 API CLIENT
# ═══════════════════════════════════════════════════════════════

class BslifeAPI:
    def __init__(self):
        self.jar = http.cookiejar.CookieJar()
        try: ctx = ssl.create_default_context()
        except Exception:
            try: ctx = ssl._create_unverified_context()
            except Exception: ctx = None

        handlers = [urllib.request.HTTPCookieProcessor(self.jar)]
        try: handlers.append(urllib.request.HTTPSHandler(context=ctx))
        except Exception: pass

        self.opener = urllib.request.build_opener(*handlers)
        self.headers = {"User-Agent": "BombSquad/1.7.x (Valhalla UI)",
                        "Accept": "application/json", "Content-Type": "application/json"}
        self.user = None
        self.ally = None
        self.roleid = None
        self.memberid = None
        self._load_cookies()

    def _load_cookies(self):
        if not os.path.exists(SESSION_FILE): return
        try:
            with open(SESSION_FILE, "r", encoding="utf-8") as f: data = json.load(f)
            for k, v in data.get("cookies", {}).items():
                c = http.cookiejar.Cookie(
                    version=0, name=k, value=v, port=None, port_specified=False,
                    domain="bslife.ir", domain_specified=True, domain_initial_dot=False,
                    path="/", path_specified=True, secure=True,
                    expires=None, discard=True, comment=None, comment_url=None,
                    rest={"HttpOnly": None}, rfc2109=False
                )
                self.jar.set_cookie(c)
            self.user = data.get("user")
            log(f"Loaded session for: {self.user}")
        except Exception as e: 
            log(f"Load cookies failed: {e}")

    def _save_cookies(self):
        data = {"cookies": {c.name: c.value for c in self.jar}, "user": self.user}
        try:
            with open(SESSION_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e: 
            log(f"Save cookies failed: {e}")

    def post(self, path, payload):
        url = BASE_URL + path
        try:
            data = json.dumps(payload).encode("utf-8")
            cookies = self.jar._cookies
            cookie_str = "".join(f"{n}={cookies[d][p][n].value}; " for d in cookies for p in cookies[d] for n in cookies[d][p])
            headers = self.headers.copy()
            if cookie_str: headers["Cookie"] = cookie_str
            req = urllib.request.Request(url, data=data, headers=headers, method="POST")
            with self.opener.open(req, timeout=20) as resp:
                result = resp.read().decode("utf-8", errors="replace").strip()
                self._save_cookies()
                return result
        except urllib.error.HTTPError as e:
            return f"__HTTPERROR__:{e.code}"
        except Exception as e:
            return f"__ERROR__:{e}"

    def post_json(self, path, payload):
        t = self.post(path, payload)
        if t in ("3", "", "-1"): return t
        if t.startswith("__"): return {"error": t}
        try: return json.loads(t)
        except Exception: return t

    def login(self, name, otp):
        r = self.post("/Head.php", {"fu": "login", "n": name, "p": otp})
        if r == "1":
            self.user = name
            self._save_cookies()
            return True, L("success_loading")
        return False, {"0": "Wrong Username/OTP", "ban": "Blocked", "banned": "Banned", "-1": "Server Error"}.get(r, "Unknown Error")

    def whoami(self):
        r = self.post("/Head.php", {"fu": "load"})
        if r in ("3", ""):
            log("Session expired, trying to recover with tk_user...")
            r = self.post("/Head.php", {"fu": "load"})
        return None if r in ("3", "") else r

    def logout(self):
        try: self.post("/Head.php", {"fu": "account_logout"})
        except Exception: pass
        self.jar.clear()
        if os.path.exists(SESSION_FILE): os.remove(SESSION_FILE)
        self.user = None
        self.ally = None
        self.roleid = None
        self.memberid = None

    def ally_status(self): return self.post_json("/post/Ally.php", {"fu": "status"})
    def ally_members(self): return self.post_json("/post/Ally.php", {"fu": "members"})
    def ally_leave(self): return self.post("/post/Ally.php", {"fu": "leave_ally"})
    def ally_requests(self, rtype="new"): return self.post_json("/post/Ally.php", {"fu": "get_requests", "type": rtype, "offset": None})
    def ally_handle_request(self, req_id, mode): return self.post("/post/Ally.php", {"fu": "handle_request", "request": req_id, "mode": mode})
    def ally_change_role(self, member_id, roleid): return self.post("/post/Ally.php", {"fu": "change_role", "id": member_id, "roleid": roleid})
    def ally_change_title(self, member_id, title, color): return self.post("/post/Ally.php", {"fu": "change_title", "id": member_id, "title": title, "color": color})
    def ally_mute(self, target, typ): return self.post("/post/Ally.php", {"fu": "mute_unmute", "target": target, "type": typ})
    def ally_kick(self, member_id): return self.post("/post/Ally.php", {"fu": "delete_member", "id": member_id})
    def ally_settings(self): return self.post_json("/post/Ally.php", {"fu": "settings"})
    def ally_save_setting(self, key, val): return self.post_json("/post/Ally.php", {"fu": "settings", "key": key, "val": val})
    def ally_capacity(self): return self.post("/post/Ally.php", {"fu": "capacity"})
    def ally_chat_history(self, offset=None): return self.post_json("/post/Ally.php", {"fu": "chat_history", "offset": offset})
    def ally_chat_send(self, text): return self.post("/post/Ally.php", {"fu": "chat_send", "chat": text})
    def ally_ranking(self, date=None): return self.post_json("/post/Ally.php", {"fu": "ranking_info", "date": date})
    def ally_vault_status(self): return self.post_json("/post/Ally.php", {"fu": "vault_status"})
    def ally_vault_add(self, amount): return self.post("/post/Ally.php", {"fu": "vault_add", "amount": amount})
    def ally_vault_clear(self, typ): return self.post("/post/Ally.php", {"fu": "vault_clear", "type": typ})
    def ally_vault_news(self, offset=None): return self.post_json("/post/Ally.php", {"fu": "vault_news", "offset": offset})
    def ally_vault_shares(self, trans_id): return self.post_json("/post/Ally.php", {"fu": "vault_shares", "id": trans_id})
    def ally_enrol(self): return self.post_json("/post/Ally.php", {"fu": "enrol_settings"})
    def ally_set_enrol(self, key, val): return self.post_json("/post/Ally.php", {"fu": "enrol_settings", "key": key, "val": val})
    def ally_news(self, offset=None): return self.post_json("/post/Ally.php", {"fu": "news", "offset": offset})
    def create_status(self): return self.post_json("/post/AllyCreate.php", {"fu": "status"})
    def create_ally(self, name, confirm=0): return self.post_json("/post/AllyCreate.php", {"fu": "create", "name": name, "confirm": confirm})
    def list_allies(self, search="", order="rank"): return self.post_json("/post/AllyList.php", {"fu": "get_allys", "offset": None, "order": order, "search": search, "filter": "[]"})
    def join_ally(self, ally_id): return self.post("/post/AllyList.php", {"fu": "join_ally", "ally": ally_id})

class Network:
    @classmethod
    def fetch(cls, api, method_name, args=(), callback=None):
        def worker():
            try: result = getattr(api, method_name)(*args)
            except Exception as e: result = {"error": str(e)}
            if callback:
                try: bui.pushcall(MyCall(callback, result), from_other_thread=True)
                except Exception as e: log(f"Pushcall error: {e}")
        threading.Thread(target=worker, daemon=True).start()

# ═══════════════════════════════════════════════════════════════
# 🎨 VALHALLA UI HELPERS
# ═══════════════════════════════════════════════════════════════

class AH:
    @staticmethod
    def uis():
        s = bui.app.ui_v1.uiscale
        return 1.7 if s is babase.UIScale.SMALL else 1.3 if s is babase.UIScale.MEDIUM else 1.0

    @staticmethod
    def draw_panel(parent, x, y, w, h, bg=COL_PANEL, border=COL_ACCENT2):
        """Draws a floating Valhalla panel (Shadow + Glow + Border + Fill)"""
        try:
            # Shadow (Black, offset by 4)
            bui.imagewidget(parent=parent, position=(x-4, y-4), size=(w+8, h+8), 
                            texture=bui.gettexture('softRect'), color=(0,0,0), opacity=0.8)
            # Glow (Gold, slightly larger)
            bui.imagewidget(parent=parent, position=(x-1, y-1), size=(w+2, h+2), 
                            texture=bui.gettexture('softRect'), color=border, opacity=0.7)
            # Solid Border
            bui.imagewidget(parent=parent, position=(x, y), size=(w, h), 
                            texture=bui.gettexture('softRect'), color=border)
            # Inner Fill
            bui.imagewidget(parent=parent, position=(x+2, y+2), size=(w-4, h-4), 
                            texture=bui.gettexture('softRect'), color=bg)
        except Exception: pass

    @staticmethod
    def window(source=None, size=(WIN_W, WIN_H), track_bg=None):
        w = safe_containerwidget(
            parent=bui.get_special_widget("overlay_stack"), size=size,
            transition="in_scale", scale=AH.uis(), color=COL_BG,
            stack_offset=(0, 0),
            scale_origin_stack_position=source.get_screen_space_center() if source else None
        )
        # Massive outer frame
        try:
            bui.imagewidget(parent=w, position=(-10,-10), size=(size[0]+20, size[1]+20), 
                            texture=bui.gettexture('softRect'), color=COL_ACCENT2, opacity=0.6)
            bui.imagewidget(parent=w, position=(0,0), size=size, texture=bui.gettexture('softRect'), color=COL_BG)
            bui.imagewidget(parent=w, position=(6,6), size=(size[0]-12, size[1]-12), texture=bui.gettexture('softRect'), color=COL_ACCENT2)
            bui.imagewidget(parent=w, position=(9,9), size=(size[0]-18, size[1]-18), texture=bui.gettexture('softRect'), color=COL_BG)
        except Exception: pass
        return w

    @staticmethod
    def close_window(win):
        try: bui.getsound("swish").play()
        except Exception: pass
        try:
            bui.containerwidget(edit=win, transition="out_scale")
            _safe_timer(0.2, win.delete)
        except Exception: pass

    @staticmethod
    def close_btn(parent, pos, win):
        return AH.button(parent, pos, (50, 50), "X", COL_RED, MyCall(AH.close_window, win), textcolor=(1,1,1), text_scale=1.0)

    @staticmethod
    def text(parent, pos, text, scale=0.7, color=COL_TEXT, h="left", maxwidth=None, v="center"):
        kw = dict(parent=parent, position=pos, text=str(text) if text is not None else "", scale=scale, color=color, h_align=h, v_align=v, shadow=1.2)
        if maxwidth: kw["maxwidth"] = maxwidth
        return bui.textwidget(**kw)

    @staticmethod
    def button(parent, pos, size, label, color, on_click, textcolor=COL_TEXT, autoselect=True, text_scale=None):
        # Draw custom panel for button background
        bg_col = COL_PANEL
        b_col = color if color != COL_ACCENT else COL_ACCENT2
        AH.draw_panel(parent, pos[0], pos[1], size[0], size[1], bg=bg_col, border=b_col)
        
        # Invisible button on top
        kw = dict(parent=parent, position=pos, size=size, label=label, color=(1,1,1,0), textcolor=textcolor, button_type='square',
                  autoselect=autoselect, enable_sound=True, on_activate_call=on_click, texture=bui.gettexture('buttonSquare'))
        if text_scale: kw["text_scale"] = text_scale
        
        b = bui.buttonwidget(**kw)
        try: bui.buttonwidget(edit=b, color=(0,0,0,0), texture=bui.gettexture('transparent'))
        except: pass
        return b

# ═══════════════════════════════════════════════════════════════
# 💬 POPUPS
# ═══════════════════════════════════════════════════════════════

class Popup:
    def __init__(self, title, text, on_ok=None, kind="info"):
        self._on_ok = on_ok
        self.w = safe_containerwidget(
            parent=bui.get_special_widget("overlay_stack"), size=(400, 220), transition="in_scale", scale=AH.uis(), color=COL_BG
        )
        AH.draw_panel(self.w, 0, 0, 400, 220, bg=COL_PANEL, border=COL_ACCENT2)
        
        border = COL_GREEN if kind == "success" else COL_RED if kind == "error" else COL_GOLD
        AH.text(self.w, (200, 170), str(title), scale=1.0, color=border, h="center", maxwidth=360)
        AH.text(self.w, (200, 100), str(text), scale=0.7, color=COL_TEXT, h="center", maxwidth=360)
        AH.button(self.w, (140, 30), (120, 40), L("ok"), border, MyCall(self._close), textcolor=(1, 1, 1), text_scale=0.8)

    def _close(self):
        AH.close_window(self.w)
        if self._on_ok: _safe_timer(0.25, MyCall(self._on_ok))

class NumberInputPopup:
    def __init__(self, title, initial_val, on_submit):
        self._on_submit = on_submit
        self.w = safe_containerwidget(
            parent=bui.get_special_widget("overlay_stack"), size=(400, 220), transition="in_scale", scale=AH.uis(), color=COL_BG
        )
        AH.draw_panel(self.w, 0, 0, 400, 220, bg=COL_PANEL, border=COL_ACCENT2)
        
        AH.text(self.w, (200, 170), title, scale=0.9, color=COL_GOLD, h="center", maxwidth=360)
        # Input field inside a small panel
        AH.draw_panel(self.w, 80, 90, 240, 40, bg=COL_BG, border=COL_ACCENT)
        self.inp = bui.textwidget(parent=self.w, position=(80, 90), size=(240, 40), editable=True, text=str(initial_val or ""), h_align="center", v_align="center", color=COL_TEXT)
        
        AH.button(self.w, (60, 30), (130, 40), L("confirm"), COL_GREEN, MyCall(self._confirm), textcolor=(1, 1, 1), text_scale=0.7)
        AH.button(self.w, (210, 30), (130, 40), L("cancel"), COL_RED, MyCall(AH.close_window, self.w), textcolor=(1, 1, 1), text_scale=0.7)

    def _confirm(self):
        txt = bui.textwidget(query=self.inp).strip()
        if txt == "": val = None
        else:
            try: val = int(txt)
            except Exception: return
        AH.close_window(self.w)
        _safe_timer(0.2, MyCall(self._on_submit, val))

# ═══════════════════════════════════════════════════════════════
# 👤 MEMBER ACTION WINDOW
# ═══════════════════════════════════════════════════════════════

class MemberActionWindow:
    def __init__(self, api, member, on_refresh):
        self.api = api
        self.member = member
        self.on_refresh = on_refresh

        self.w = AH.window(size=(360, 380))
        AH.close_btn(self.w, (300, 320), self.w)

        name = member.get("name", "?")
        AH.text(self.w, (180, 335), f"{L('manage')}: {name}", scale=0.9, color=COL_GOLD, h="center")

        AH.text(self.w, (30, 300), f"{L('title')}:", scale=0.7, color=COL_TEXT)
        self.inp_title = bui.textwidget(parent=self.w, position=(100, 295), size=(220, 30), editable=True, text=(member.get("title") or {}).get("t", ""), color=COL_TEXT)

        colors = [("white", (1, 1, 1)), ("red", (1, 0.3, 0.3)), ("blue", (0.3, 0.6, 1)), ("green", (0.3, 1, 0.3)), ("yellow", (1, 1, 0.2)), ("orange", (1, 0.6, 0.2))]
        self.color_choice = {"name": "white"}
        x = 30
        AH.text(self.w, (30, 260), f"{L('color')}:", scale=0.7, color=COL_TEXT)
        for cname, crgb in colors:
            def mk(n=cname): return lambda: self.color_choice.update({"name": n})
            AH.draw_panel(self.w, x, 230, 36, 24, bg=crgb, border=COL_ACCENT)
            bui.buttonwidget(parent=self.w, position=(x, 230), size=(36, 24), label="", color=(1,1,1,0), button_type="square", on_activate_call=mk(), texture=bui.gettexture('transparent'))
            x += 45

        AH.button(self.w, (90, 180), (180, 35), L("apply_title"), COL_ACCENT, MyCall(self._apply_title), textcolor=(1, 1, 1), text_scale=0.7)
        AH.text(self.w, (30, 145), f"{L('role')}:", scale=0.7, color=COL_TEXT)
        AH.button(self.w, (100, 135), (220, 35), L("change_role"), COL_ACCENT2, MyCall(self._open_role_menu), text_scale=0.7)

        mute_label = L("unmute") if member.get("muted") else L("mute")
        mute_color = COL_GREEN if member.get("muted") else COL_GOLD
        AH.button(self.w, (30, 80), (140, 35), mute_label, mute_color, MyCall(self._toggle_mute), textcolor=(1, 1, 1), text_scale=0.7)
        AH.button(self.w, (190, 80), (140, 35), L("kick"), COL_RED, MyCall(self._kick), textcolor=(1, 1, 1), text_scale=0.7)

    def _apply_title(self):
        title = bui.textwidget(query=self.inp_title).strip()
        def cb(r):
            AH.close_window(self.w)
            self.on_refresh()
        Network.fetch(self.api, "ally_change_title", (self.member["id"], title, self.color_choice["name"]), callback=cb)

    def _open_role_menu(self):
        w = safe_containerwidget(parent=bui.get_special_widget("overlay_stack"), size=(360, 300), transition="in_scale", scale=AH.uis(), color=COL_BG)
        AH.draw_panel(w, 0, 0, 360, 300, bg=COL_PANEL, border=COL_ACCENT2)
        AH.text(w, (180, 260), L("select_role"), scale=0.9, color=COL_GOLD, h="center")

        options = [(2, L("general")), (3, L("spy")), (None, L("remove_role"))]
        selected = {"role": "__not_set__"}
        buttons = []
        y = 200
        for roleid, label in options:
            def mk_click(r=roleid):
                def click():
                    selected["role"] = r
                    for b, rr in buttons:
                        try: bui.buttonwidget(edit=b, color=COL_ACCENT if rr == r else COL_PANEL)
                        except Exception: pass
                return click
            b = AH.button(w, (40, y), (280, 38), label, COL_PANEL, MyCall(mk_click()), text_scale=0.7)
            buttons.append((b, roleid))
            y -= 50

        def confirm():
            if selected["role"] == "__not_set__": return
            AH.close_window(w)
            def cb(r):
                if r == "1": Popup(L("success"), L("role_changed"), kind="success", on_ok=self._after_change)
                else: Popup(L("fail"), {"too_many": "ظرفیت نقش پر است", "no_bot": "اکانت به بات متصل نیست"}.get(r, L("fail")), kind="error")
            Network.fetch(self.api, "ally_change_role", (self.member["id"], selected["role"]), callback=cb)

        def _after_change():
            try: AH.close_window(self.w)
            except Exception: pass
            self.on_refresh()

        AH.button(w, (40, 25), (130, 38), L("confirm"), COL_GREEN, MyCall(confirm), textcolor=(1, 1, 1), text_scale=0.7)
        AH.button(w, (190, 25), (130, 38), L("cancel"), COL_RED, MyCall(AH.close_window, w), textcolor=(1, 1, 1), text_scale=0.7)

    def _toggle_mute(self):
        typ = "unmute" if self.member.get("muted") else "mute"
        def cb(r):
            AH.close_window(self.w)
            self.on_refresh()
        Network.fetch(self.api, "ally_mute", (self.member.get("name"), typ), callback=cb)

    def _kick(self):
        def cb(r):
            AH.close_window(self.w)
            self.on_refresh()
        Network.fetch(self.api, "ally_kick", (self.member["id"],), callback=cb)

# ═══════════════════════════════════════════════════════════════
# 🔐 LOGIN WINDOW
# ═══════════════════════════════════════════════════════════════

class LoginWindow:
    def __init__(self, api, on_success):
        self.api = api
        self.on_success = on_success
        self._loading = None
        self._angle = 0
        self._check_login = False

        self.w = AH.window(size=(600, 420))
        AH.text(self.w, (300, 370), u"⚔ VALHALLA LOGIN", scale=1.3, color=COL_GOLD, h="center")
        AH.text(self.w, (300, 340), "BSLIFE Alliance Manager", scale=0.6, color=COL_DIM, h="center")
        AH.close_btn(self.w, (530, 355), self.w)

        AH.draw_panel(self.w, 60, 140, 480, 160, bg=COL_PANEL, border=COL_ACCENT2)
        
        AH.text(self.w, (90, 260), L("user") + ":", scale=0.7, color=COL_GOLD)
        self.inp_user = bui.textwidget(parent=self.w, position=(180, 250), size=(320, 30), editable=True, text="", color=COL_TEXT, h_align="left", max_chars=30)

        AH.text(self.w, (90, 200), "OTP:", scale=0.7, color=COL_GOLD)
        self.inp_otp = bui.textwidget(parent=self.w, position=(180, 190), size=(320, 30), editable=True, text="", color=COL_TEXT, h_align="left", max_chars=8)

        self.status = AH.text(self.w, (300, 100), "", scale=0.6, color=COL_DIM, h="center")

        AH.button(self.w, (180, 30), (240, 45), L("login"), COL_ACCENT, MyCall(self.do_login), textcolor=(1, 1, 1), text_scale=0.9)

    def do_login(self):
        if self._loading is not None: return
        name = bui.textwidget(query=self.inp_user).strip()
        otp = bui.textwidget(query=self.inp_otp).strip()
        if not name or not otp:
            self.set_status(L("error_fill"), COL_RED)
            return
        self.set_status(L("logging_in"), COL_GOLD)
        
        def worker():
            ok, msg = self.api.login(name, otp)
            bui.pushcall(MyCall(self._login_done, ok, msg), from_other_thread=True)
        threading.Thread(target=worker, daemon=True).start()

    def set_status(self, text, color=COL_DIM):
        try: bui.textwidget(edit=self.status, text=text, color=color)
        except Exception: pass

    def _login_done(self, ok, msg):
        if ok:
            self.set_status(L("success_loading"), COL_GREEN)
            _safe_timer(0.5, MyCall(self._go_next))
        else:
            self.set_status(f"{L('error')}: {msg}", COL_RED)

    def _go_next(self):
        AH.close_window(self.w)
        global _main_win
        _main_win = None
        _safe_timer(0.3, MyCall(self.on_success))

# ═══════════════════════════════════════════════════════════════
# 🏰 ALLY MAIN WINDOW (Exact Image Match)
# ═══════════════════════════════════════════════════════════════

class AllyMainWindow:
    TABS = ["overview", "members", "requests", "vault", "settings", "ranking", "news", "chat", "channels"]
    ICONS = {"overview": "🛡", "members": "👥", "requests": "✉", "vault": "💰", "settings": "⚙", "ranking": "🏆", "news": "📜", "chat": "💬", "channels": "⚡"}

    def __init__(self, api):
        self.api = api
        self.current_tab = "channels"
        self.tab_buttons = {}
        self.chat_poll_timer = None
        self._closing = False
        self._req_filter = "new"

        self.w = AH.window(size=(800, 550))

        # ─── HEADER (Image Match) ───
        AH.close_btn(self.w, (20, 470), self.w) # Big X on left
        self.head_text = AH.text(self.w, (400, 500), "Valhalla (Member)", scale=1.3, color=COL_GOLD, h="center")
        self.head_sub = AH.text(self.w, (400, 475), f"{L('user')}: ...", scale=0.7, color=(0.4, 0.7, 1.0), h="center")
        
        # Style / Logout buttons
        AH.button(self.w, (590, 480), (90, 40), "Style", COL_ACCENT2, MyCall(self._cycle_style), text_scale=0.7)
        AH.button(self.w, (690, 480), (90, 40), L("logout"), COL_RED, MyCall(self._do_logout), textcolor=(1,1,1), text_scale=0.7)

        # ─── SIDEBAR ───
        AH.draw_panel(self.w, 20, 40, 180, 400, bg=COL_SIDEBAR_BG, border=COL_ACCENT2)
        self._render_sidebar()

        # ─── CONTENT ───
        AH.draw_panel(self.w, 210, 40, 570, 400, bg=COL_CONTENT_BG, border=COL_ACCENT2)
        self.content_root = bui.containerwidget(parent=self.w, position=(220, 50), size=(550, 380), background=False)
        
        # ─── FOOTER ───
        AH.text(self.w, (400, 20), "Theme: Gold Rush", scale=0.7, color=COL_GOLD, h="center")

        self.refresh()

    def _cycle_style(self):
        Popup("Style", "Themes are locked to Gold Rush for Valhalla.", kind="info")

    def _create_content_area(self):
        if self.content_root is not None:
            try: self.content_root.delete()
            except Exception: pass
        self.content_root = bui.containerwidget(parent=self.w, position=(220, 50), size=(550, 380), background=False)

    def _do_logout(self):
        self._closing = True
        self.api.logout()
        AH.close_window(self.w)
        global _main_win
        _main_win = None
        LoginWindow(self.api, _route_after_login)

    def _render_sidebar(self):
        for btn in self.tab_buttons.values():
            try: btn.delete()
            except Exception: pass
        self.tab_buttons = {}

        tabs_to_show = []
        for k in self.TABS:
            if k in ("requests", "settings") and self.api.roleid not in (1, 2):
                continue
            tabs_to_show.append(k)

        y = 390
        for key in tabs_to_show:
            icon = self.ICONS.get(key, "•")
            label = f"{icon}   {L(key)}"
            color = COL_ACCENT if key == self.current_tab else COL_PANEL
            btn = AH.button(self.w, (30, y), (160, 45), label, color, MyCall(self.switch_tab, key), text_scale=0.8)
            self.tab_buttons[key] = btn
            y -= 50

    def switch_tab(self, key):
        if self._closing: return
        self.current_tab = key
        self._render_sidebar()
        if key != "chat": self.chat_poll_timer = None
        self._create_content_area()
        self._render_current()

    def refresh(self):
        Network.fetch(self.api, "ally_status", callback=self._on_status)

    def _on_status(self, st):
        if not self.w.exists(): return
        if st in ("3", "0", "", None):
            self._do_logout()
            return
        if not isinstance(st, dict):
            AH.close_window(self.w)
            global _main_win
            _main_win = None
            HubWindow(self.api)
            return

        self.api.ally = st.get("name")
        self.api.roleid = st.get("roleid")
        self.api.memberid = st.get("memberid")
        
        name = st.get("name") or L("no_ally")
        role = role_name(st.get("roleid"))
        try:
            bui.textwidget(edit=self.head_text, text=f"{name} ({role})")
            bui.textwidget(edit=self.head_sub, text=f"{L('user')}: {self.api.user or '?'}")
        except Exception: pass

        self._render_sidebar()
        self._create_content_area()
        self._render_current()

    def _render_current(self):
        if self._closing: return
        handler = getattr(self, "_tab_" + self.current_tab, None)
        if handler:
            try: handler()
            except Exception as e: log(f"Render EXCEPTION {self.current_tab}: {e}")

    # ─── TABS ───
    def _tab_overview(self):
        def cb(st):
            if not self.w.exists() or not isinstance(st, dict): return
            try:
                AH.text(self.content_root, (275, 320), L("overview"), scale=1.0, color=COL_GOLD, h="center")
                y = 260
                AH.text(self.content_root, (40, y), f"{L('alliance_name')}:", scale=0.7, color=COL_TEXT); AH.text(self.content_root, (200, y), st.get("name"), scale=0.7, color=COL_GOLD); y -= 45
                AH.text(self.content_root, (40, y), f"{L('your_role')}:", scale=0.7, color=COL_TEXT); AH.text(self.content_root, (200, y), role_name(st.get("roleid")), scale=0.7, color=role_color(st.get("roleid"))); y -= 45
                AH.text(self.content_root, (40, y), f"{L('members_count')}:", scale=0.7, color=COL_TEXT); AH.text(self.content_root, (200, y), str(st.get("count", "?")), scale=0.7, color=COL_TEXT)
                
                if self.api.roleid != 1:
                    AH.button(self.content_root, (175, 40), (200, 45), L("leave_ally"), COL_RED, MyCall(self._confirm_leave), textcolor=(1, 1, 1), text_scale=0.7)
            except ReferenceError: pass
        Network.fetch(self.api, "ally_status", callback=cb)

    def _confirm_leave(self):
        w = safe_containerwidget(parent=bui.get_special_widget("overlay_stack"), size=(400, 200), transition="in_scale", scale=AH.uis(), color=COL_BG)
        AH.draw_panel(w, 0, 0, 400, 200, bg=COL_PANEL, border=COL_ACCENT2)
        AH.text(w, (200, 150), L("leave_ally"), scale=1.0, color=COL_RED, h="center")
        AH.text(w, (200, 100), L("leave_confirm"), scale=0.7, color=COL_TEXT, h="center", maxwidth=360)
        
        def do_leave():
            AH.close_window(w)
            def cb(r):
                if r == "1":
                    AH.close_window(self.w)
                    global _main_win
                    _main_win = None
                    _safe_timer(0.5, MyCall(_route_after_login))
            Network.fetch(self.api, "ally_leave", callback=cb)

        AH.button(w, (60, 30), (130, 40), L("yes"), COL_GREEN, MyCall(do_leave), textcolor=(1, 1, 1), text_scale=0.7)
        AH.button(w, (210, 30), (130, 40), L("no"), COL_PANEL, MyCall(AH.close_window, w), textcolor=(1, 1, 1), text_scale=0.7)

    def _tab_members(self):
        def cb(members):
            if not self.w.exists(): return
            if not isinstance(members, list):
                if members in ("3", "", "-1"): self._on_status("3")
                return
            try:
                scroll = bui.scrollwidget(parent=self.content_root, position=(20, 10), size=(510, 340), color=COL_BG, highlight=False)
                container = bui.containerwidget(parent=scroll, size=(500, 36 * len(members) + 10), background=False)
                y = 36 * len(members)
                for m in members:
                    y -= 36
                    is_me = m.get("id") == self.api.memberid
                    bg = COL_ACCENT2 if is_me else COL_PANEL
                    bui.buttonwidget(parent=container, position=(0, y), size=(500, 32), label="", color=bg, enable_sound=False, texture=bui.gettexture('white'))
                    AH.text(container, (15, y + 16), role_name(m.get("roleid")), scale=0.6, color=role_color(m.get("roleid")))
                    AH.text(container, (120, y + 16), m.get("name", "?"), scale=0.6, color=COL_TEXT)
                    if self.api.roleid in (1, 2) and not is_me:
                        AH.button(container, (430, y + 4), (60, 24), "...", COL_ACCENT, MyCall(self._open_member_window, m), autoselect=False, text_scale=0.6, textcolor=(1, 1, 1))
            except Exception as e: log(f"UI Error: {e}")
        Network.fetch(self.api, "ally_members", callback=cb)

    def _open_member_window(self, m): MemberActionWindow(self.api, m, self._tab_members)

    def _tab_requests(self):
        x = 20
        for key in ["new", "accepted", "rejected"]:
            color = COL_ACCENT if key == self._req_filter else COL_PANEL
            AH.button(self.content_root, (x, 320), (150, 35), L(key), color, MyCall(self._set_req_filter, key), textcolor=(1, 1, 1), text_scale=0.7)
            x += 165

        def cb(reqs):
            if not self.w.exists() or not isinstance(reqs, list): return
            try:
                scroll = bui.scrollwidget(parent=self.content_root, position=(20, 10), size=(510, 290), color=COL_BG, highlight=False)
                container = bui.containerwidget(parent=scroll, size=(500, 40 * len(reqs) + 10), background=False)
                y = 40 * len(reqs)
                for r in reqs:
                    y -= 40
                    bui.buttonwidget(parent=container, position=(0, y), size=(500, 36), label="", color=COL_PANEL, enable_sound=False, texture=bui.gettexture('white'))
                    AH.text(container, (15, y + 18), r.get("name", "?"), scale=0.6, color=COL_TEXT)
                    if self._req_filter == "new":
                        AH.button(container, (360, y + 6), (60, 24), L("yes"), COL_GREEN, MyCall(self._handle_req, r, "accept"), textcolor=(1, 1, 1), text_scale=0.5)
                        AH.button(container, (430, y + 6), (60, 24), L("no"), COL_RED, MyCall(self._handle_req, r, "reject"), textcolor=(1, 1, 1), text_scale=0.5)
            except Exception as e: log(f"UI Error: {e}")
        Network.fetch(self.api, "ally_requests", (self._req_filter,), callback=cb)

    def _set_req_filter(self, key):
        self._req_filter = key
        self._create_content_area()
        self._tab_requests()

    def _handle_req(self, r, mode):
        Network.fetch(self.api, "ally_handle_request", (r.get("id"), mode), callback=lambda res: self._tab_requests())

    def _tab_vault(self):
        def cb(v):
            if not self.w.exists() or not isinstance(v, dict): return
            try:
                AH.text(self.content_root, (275, 300), f"{fmt(v.get('coin', 0))} {L('coins')}", scale=1.6, color=COL_GOLD, h="center")
                AH.button(self.content_root, (40, 200), (140, 45), L("deposit"), COL_ACCENT, MyCall(self._open_deposit), textcolor=(1, 1, 1), text_scale=0.7)
                AH.button(self.content_root, (205, 200), (140, 45), L("history"), COL_PANEL, MyCall(self._open_vault_history), text_scale=0.7)
                if self.api.roleid in (1, 2):
                    AH.button(self.content_root, (370, 200), (140, 45), L("split"), COL_ACCENT2, MyCall(self._open_split), textcolor=(1, 1, 1), text_scale=0.7)
            except ReferenceError: pass
        Network.fetch(self.api, "ally_vault_status", callback=cb)

    def _open_vault_history(self):
        w = safe_containerwidget(parent=bui.get_special_widget("overlay_stack"), size=(500, 380), transition="in_scale", scale=AH.uis(), color=COL_BG)
        AH.draw_panel(w, 0, 0, 500, 380, bg=COL_PANEL, border=COL_ACCENT2)
        AH.close_btn(w, (440, 330), w)
        AH.text(w, (250, 340), L("vault_news"), scale=1.0, color=COL_GOLD, h="center")

        scroll = bui.scrollwidget(parent=w, position=(20, 20), size=(460, 300), color=COL_BG, highlight=False)
        container = bui.containerwidget(parent=scroll, size=(450, 300), background=False)

        def cb(news):
            if not isinstance(news, list): return
            y = len(news) * 36
            for n in news:
                y -= 36
                bui.buttonwidget(parent=container, position=(0, y), size=(450, 32), label="", color=COL_PANEL, enable_sound=False, texture=bui.gettexture('white'))
                AH.text(container, (10, y + 16), n.get("text", ""), scale=0.6, maxwidth=320, color=COL_TEXT)
                if n.get("is_parent"):
                    AH.button(container, (350, y + 4), (90, 24), L("vault_shares"), COL_ACCENT, MyCall(self._open_vault_shares, n.get("id")), textcolor=(1,1,1), text_scale=0.5)
        Network.fetch(self.api, "ally_vault_news", (None,), callback=cb)

    def _open_vault_shares(self, trans_id):
        w = safe_containerwidget(parent=bui.get_special_widget("overlay_stack"), size=(360, 300), transition="in_scale", scale=AH.uis(), color=COL_BG)
        AH.draw_panel(w, 0, 0, 360, 300, bg=COL_PANEL, border=COL_ACCENT2)
        AH.close_btn(w, (300, 250), w)
        AH.text(w, (180, 260), L("vault_shares"), scale=1.0, color=COL_GOLD, h="center")

        scroll = bui.scrollwidget(parent=w, position=(15, 20), size=(330, 230), color=COL_BG, highlight=False)
        container = bui.containerwidget(parent=scroll, size=(320, 230), background=False)

        def cb(shares):
            if not isinstance(shares, list): return
            y = len(shares) * 32
            for s in shares:
                y -= 32
                AH.text(container, (10, y + 16), s.get("name", "?"), scale=0.6, color=COL_TEXT)
                AH.text(container, (250, y + 16), fmt(s.get("val", 0)), scale=0.6, color=COL_GREEN, h="right")
        Network.fetch(self.api, "ally_vault_shares", (trans_id,), callback=cb)

    def _open_deposit(self):
        def do_deposit(amount):
            if amount is None or amount < 100: return
            def cb(r):
                if r == "1": Popup(L("success"), L("deposit_ok"), kind="success", on_ok=self._tab_vault)
                else: Popup(L("fail"), L("not_enough_coins") if r == "coin_not_enough" else L("fail"), kind="error")
            Network.fetch(self.api, "ally_vault_add", (amount,), callback=cb)
        NumberInputPopup(L("enter_amount"), "", do_deposit)

    def _open_split(self):
        w = safe_containerwidget(parent=bui.get_special_widget("overlay_stack"), size=(400, 300), transition="in_scale", scale=AH.uis(), color=COL_BG)
        AH.draw_panel(w, 0, 0, 400, 300, bg=COL_PANEL, border=COL_ACCENT2)
        AH.text(w, (200, 260), L("split"), scale=1.0, color=COL_GOLD, h="center")
        AH.text(w, (200, 230), L("select_type"), scale=0.6, color=COL_DIM, h="center")

        types = [("equal_all", L("equal_all")), ("equal_ranking", L("equal_ranking")), ("ranking_points", L("ranking_points"))]
        selected = {"type": "__not_set__"}
        buttons = []
        y = 180
        for typ, label in types:
            def mk_click(t=typ):
                def click():
                    selected["type"] = t
                    for b, tt in buttons:
                        try: bui.buttonwidget(edit=b, color=COL_ACCENT if tt == t else COL_PANEL)
                        except Exception: pass
                return click
            b = AH.button(w, (40, y), (320, 38), label, COL_PANEL, MyCall(mk_click()), text_scale=0.7)
            buttons.append((b, typ))
            y -= 50

        def confirm():
            if selected["type"] == "__not_set__": return
            AH.close_window(w)
            def cb(r):
                if r == "1": Popup(L("success"), L("vault_split_ok"), kind="success", on_ok=self._tab_vault)
                else: Popup(L("fail"), {"coin_not_enough": L("not_enough_coins"), "no_ranking_info": "اطلاعات رنکینگ موجود نیست"}.get(r, L("fail")), kind="error")
            Network.fetch(self.api, "ally_vault_clear", (selected["type"],), callback=cb)

        AH.button(w, (60, 20), (130, 38), L("confirm"), COL_GREEN, MyCall(confirm), textcolor=(1, 1, 1), text_scale=0.7)
        AH.button(w, (210, 20), (130, 38), L("cancel"), COL_RED, MyCall(AH.close_window, w), textcolor=(1, 1, 1), text_scale=0.7)

    def _tab_settings(self):
        def cb_settings(st):
            def cb_enrol(en):
                if not self.w.exists(): return
                try:
                    scroll = bui.scrollwidget(parent=self.content_root, position=(20, 10), size=(510, 340), color=COL_BG, highlight=False)
                    container = bui.containerwidget(parent=scroll, size=(500, 480), background=False)
                    y = 450
                    
                    AH.text(container, (20, y), f"{L('capacity')}: {st.get('capacity', '?')}", scale=0.7, color=COL_TEXT)
                    AH.button(container, (360, y-8), (110, 30), L("buy_1"), COL_ACCENT, MyCall(self._buy_capacity), textcolor=(1,1,1), text_scale=0.6)
                    y -= 45
                    
                    AH.text(container, (20, y), f"{L('gkick')}: {st.get('gkick', 1)}", scale=0.7, color=COL_TEXT)
                    AH.button(container, (360, y-8), (110, 30), "Set", COL_PANEL, MyCall(self._set_gkick, st.get('gkick', 1)), text_scale=0.6)
                    y -= 45
                    
                    AH.text(container, (20, y), f"{L('spynet')}: {fmt(st.get('spynet', 0))}", scale=0.7, color=COL_TEXT)
                    AH.button(container, (360, y-8), (110, 30), "Set", COL_PANEL, MyCall(self._set_spynet, st.get('spynet', 0)), text_scale=0.6)
                    y -= 45
                    
                    tag_txt = L("tag_active") if st.get("taghide") is None else L("tag_inactive")
                    AH.text(container, (20, y), f"{L('tag_status')}: {tag_txt}", scale=0.7, color=COL_GREEN if st.get("taghide") is None else COL_RED)
                    y -= 45
                    
                    price_txt = fmt(st.get('price')) if st.get('price') else "Not set"
                    AH.text(container, (20, y), f"{L('sale_price')}: {price_txt}", scale=0.7, color=COL_TEXT)
                    AH.button(container, (360, y-8), (110, 30), "Set", COL_PANEL, MyCall(self._set_price, st.get('price')), text_scale=0.6)
                    y -= 55
                    
                    AH.text(container, (250, y), L("enrol_settings"), scale=0.9, color=COL_GOLD, h="center")
                    y -= 45
                    
                    req_mode = en.get("request")
                    mode_txt = {None: L("mode_direct"), 1: L("mode_request"), -1: L("mode_closed")}.get(req_mode, "?")
                    AH.text(container, (20, y), f"Mode: {mode_txt}", scale=0.7, color=COL_TEXT)
                    AH.button(container, (360, y-8), (110, 30), "Change", COL_ACCENT, MyCall(self._change_join_mode), textcolor=(1,1,1), text_scale=0.6)
                    y -= 45
                    
                    AH.text(container, (20, y), f"{L('min_coin')}: {en.get('coin', '-')}", scale=0.7, color=COL_TEXT)
                    AH.button(container, (360, y-8), (110, 30), "Set", COL_PANEL, MyCall(self._set_enrol, "coin", en.get("coin")), text_scale=0.6)
                    y -= 45
                    
                    AH.text(container, (20, y), f"{L('req_top')}: {en.get('top', '-')}", scale=0.7, color=COL_TEXT)
                    AH.button(container, (360, y-8), (110, 30), "Set", COL_PANEL, MyCall(self._set_enrol, "top", en.get("top")), text_scale=0.6)
                    y -= 45
                    
                    AH.text(container, (20, y), f"{L('min_score')}: {en.get('score', '-')}", scale=0.7, color=COL_TEXT)
                    AH.button(container, (360, y-8), (110, 30), "Set", COL_PANEL, MyCall(self._set_enrol, "score", en.get("score")), text_scale=0.6)
                    y -= 45
                    
                    bot_txt = "اجباری" if en.get("bot") == 1 else "خاموش"
                    AH.text(container, (20, y), f"اتصال به ربات تلگرام: {bot_txt}", scale=0.7, color=COL_TEXT)
                    AH.button(container, (360, y-8), (110, 30), "Toggle", COL_PANEL, MyCall(self._toggle_enrol_bot, en.get("bot")), text_scale=0.6)
                    
                except Exception as e:
                    log(f"Settings render error: {e}")
            Network.fetch(self.api, "ally_enrol", callback=cb_enrol)
        Network.fetch(self.api, "ally_settings", callback=cb_settings)

    def _save_setting(self, key, val, refresh_fn):
        def cb(r):
            if isinstance(r, dict) and "err" in r: Popup(L("fail"), str(r["err"]), kind="error")
            else: Popup(L("success"), L("saved"), kind="success", on_ok=refresh_fn)
        Network.fetch(self.api, "ally_save_setting", (key, val), callback=cb)

    def _set_gkick(self, current): NumberInputPopup(L("gkick"), current, lambda v: self._save_setting("gkick", v, self._tab_settings))
    def _set_spynet(self, current): NumberInputPopup(L("spynet"), current, lambda v: self._save_setting("spynet", v, self._tab_settings))
    def _set_price(self, current): NumberInputPopup(L("sale_price"), current, lambda v: self._save_setting("price", v, self._tab_settings))
    def _buy_capacity(self): Network.fetch(self.api, "ally_capacity", callback=lambda r: Popup(L("success") if r=="1" else L("fail"), "", on_ok=self._tab_settings))

    def _change_join_mode(self):
        def cb(req):
            if req == "__not_set__": return
            def res_cb(r):
                mode_msg = L("mode_direct") if req is None else L("mode_request") if req == 1 else L("mode_closed")
                Popup(L("success"), f"حالت ورود: {mode_msg}", kind="success", on_ok=self._tab_settings)
            Network.fetch(self.api, "ally_set_enrol", ("request", req), callback=res_cb)
        
        w = safe_containerwidget(parent=bui.get_special_widget("overlay_stack"), size=(320, 260), transition="in_scale", scale=AH.uis(), color=COL_BG)
        AH.draw_panel(w, 0, 0, 320, 260, bg=COL_PANEL, border=COL_ACCENT2)
        AH.text(w, (160, 220), "Select Mode", scale=0.9, color=COL_GOLD, h="center")
        
        AH.button(w, (60, 160), (200, 35), L("mode_direct"), COL_PANEL, lambda: (AH.close_window(w), cb(None)), text_scale=0.7)
        AH.button(w, (60, 110), (200, 35), L("mode_request"), COL_PANEL, lambda: (AH.close_window(w), cb(1)), text_scale=0.7)
        AH.button(w, (60, 60), (200, 35), L("mode_closed"), COL_PANEL, lambda: (AH.close_window(w), cb(-1)), text_scale=0.7)
        AH.button(w, (110, 15), (100, 35), L("cancel"), COL_RED, MyCall(AH.close_window, w), text_scale=0.6)

    def _set_enrol(self, key, current):
        def cb(val):
            def res_cb(r):
                if isinstance(r, dict) and "err" in r:
                    Popup(L("fail"), str(r["err"]), kind="error")
                else:
                    Popup(L("success"), L("saved"), kind="success", on_ok=self._tab_settings)
            Network.fetch(self.api, "ally_set_enrol", (key, val), callback=res_cb)
        NumberInputPopup(key.capitalize(), current, cb)

    def _toggle_enrol_bot(self, current):
        val = None if current == 1 else 1
        def res_cb(r):
            state_msg = "اجباری" if val == 1 else "خاموش"
            Popup(L("success"), f"اتصال به ربات: {state_msg}", kind="success", on_ok=self._tab_settings)
        Network.fetch(self.api, "ally_set_enrol", ("bot", val), callback=res_cb)

    def _tab_ranking(self):
        def cb(r):
            if not self.w.exists() or not isinstance(r, dict): return
            try:
                AH.text(self.content_root, (275, 320), L("ranking"), scale=1.0, color=COL_GOLD, h="center")
                if not r.get("rank"):
                    AH.text(self.content_root, (275, 200), L("not_ranked"), scale=0.9, color=COL_DIM, h="center")
                    return
                AH.text(self.content_root, (275, 280), f"#{r.get('rank')} | {float(r.get('score', 0)):.2f} pts", scale=1.0, color=COL_GREEN, h="center")
                mdata = r.get("m_data") or {}
                effective = [m for m in mdata.values() if m.get("c") == 1]
                scroll = bui.scrollwidget(parent=self.content_root, position=(20, 10), size=(510, 250), color=COL_BG, highlight=False)
                container = bui.containerwidget(parent=scroll, size=(500, 32 * len(effective) + 10), background=False)
                y = 32 * len(effective)
                for m in effective:
                    y -= 32
                    AH.text(container, (15, y + 16), f"#{m.get('r', '?')} {m.get('n', '?')}", scale=0.6, color=COL_TEXT)
                    AH.text(container, (400, y + 16), f"{float(m.get('s', 0)):.1f}", scale=0.6, color=COL_GREEN)
            except Exception as e: log(f"UI Error: {e}")
        Network.fetch(self.api, "ally_ranking", callback=cb)

    def _tab_news(self):
        self.news_offset = None
        def cb(news):
            if not self.w.exists(): return
            try:
                if not isinstance(news, list) or len(news) == 0:
                    AH.text(self.content_root, (275, 200), L("no_news"), scale=0.9, color=COL_DIM, h="center")
                    return
                scroll = bui.scrollwidget(parent=self.content_root, position=(20, 50), size=(510, 300), color=COL_BG, highlight=False)
                container = bui.containerwidget(parent=scroll, size=(500, 50 * len(news) + 10), background=False)
                y = 50 * len(news)
                for n in news:
                    y -= 50
                    bui.buttonwidget(parent=container, position=(0, y), size=(500, 46), label="", color=COL_PANEL, enable_sound=False, texture=bui.gettexture('white'))
                    AH.text(container, (10, y + 25), n.get("text", ""), scale=0.6, maxwidth=480, color=COL_TEXT)
                    AH.text(container, (10, y + 8), n.get("time", ""), scale=0.5, color=COL_DIM)
                
                if len(news) == 10:
                    AH.button(self.content_root, (225, 10), (100, 35), L("more"), COL_ACCENT, MyCall(self._load_more_news, news[-1]["id"]), textcolor=(1,1,1), text_scale=0.6)
            except Exception as e: log(f"UI Error: {e}")
        Network.fetch(self.api, "ally_news", (self.news_offset,), callback=cb)

    def _load_more_news(self, offset):
        def cb(news):
            if not self.w.exists(): return
            try:
                if not isinstance(news, list) or len(news) == 0: return
                scroll = bui.scrollwidget(parent=self.content_root, position=(20, 50), size=(510, 300), color=COL_BG, highlight=False)
                container = bui.containerwidget(parent=scroll, size=(500, 50 * len(news) + 10), background=False)
                y = 50 * len(news)
                for n in news:
                    y -= 50
                    bui.buttonwidget(parent=container, position=(0, y), size=(500, 46), label="", color=COL_PANEL, enable_sound=False, texture=bui.gettexture('white'))
                    AH.text(container, (10, y + 25), n.get("text", ""), scale=0.6, maxwidth=480, color=COL_TEXT)
                    AH.text(container, (10, y + 8), n.get("time", ""), scale=0.5, color=COL_DIM)
                
                if len(news) == 10:
                    AH.button(self.content_root, (225, 10), (100, 35), L("more"), COL_ACCENT, MyCall(self._load_more_news, news[-1]["id"]), textcolor=(1,1,1), text_scale=0.6)
            except Exception as e: log(f"UI Error: {e}")
        Network.fetch(self.api, "ally_news", (offset,), callback=cb)

    def _tab_chat(self):
        self.chat_scroll = bui.scrollwidget(parent=self.content_root, position=(20, 60), size=(510, 290), color=COL_BG, highlight=False)
        self.chat_container = bui.containerwidget(parent=self.chat_scroll, size=(500, 290), background=False)
        self.chat_inp = bui.textwidget(parent=self.content_root, position=(20, 15), size=(380, 35), editable=True, description=L("message"), max_chars=200, color=COL_TEXT)
        AH.button(self.content_root, (410, 15), (120, 35), L("send"), COL_ACCENT, MyCall(self._send_chat), textcolor=(1, 1, 1), text_scale=0.7)
        self._refresh_chat()

    def _refresh_chat(self):
        def cb(history):
            if not isinstance(history, list) or self._closing or self.current_tab != "chat" or not self.w.exists(): return
            try:
                for c in self.chat_container.get_children(): c.delete()
                bui.containerwidget(edit=self.chat_container, size=(500, 32 * max(1, len(history)) + 10))
                y = 32 * max(1, len(history))
                for m in history[-50:]:
                    y -= 32
                    AH.text(self.chat_container, (10, y + 16), f"{m.get('name')}: {m.get('chat')}", scale=0.6, maxwidth=480, color=COL_TEXT)
                bui.scrollwidget(edit=self.chat_scroll, vertical_scroll=0.0)
            except Exception: pass
            if self.current_tab == "chat" and not self._closing:
                self.chat_poll_timer = _safe_timer(3.0, MyCall(self._refresh_chat))
        Network.fetch(self.api, "ally_chat_history", callback=cb)

    def _send_chat(self):
        try: msg = bui.textwidget(query=self.chat_inp).strip()
        except Exception: return
        if not msg: return
        bui.textwidget(edit=self.chat_inp, text="")
        Network.fetch(self.api, "ally_chat_send", (msg,), callback=lambda r: self._refresh_chat())

    # ═══════════════════════ CHANNELS (EXACT IMAGE MATCH) ═══════════════════════
    
    def _tab_channels(self):
        # Title
        AH.text(self.content_root, (275, 330), "Channels :", scale=1.4, color=COL_GOLD, h="center")
        
        # ─── BsRush Button ───
        def open_bsrush():
            try: bui.open_url("https://t.me/bsrush_mod")
            except: pass

        y1 = 210
        AH.draw_panel(self.content_root, 20, y1, 510, 80, bg=COL_BG, border=COL_GOLD)
        AH.text(self.content_root, (275, y1+40), "⚡  BsRush", scale=1.4, color=COL_GOLD, h="center")
        
        b1 = bui.buttonwidget(parent=self.content_root, position=(20, y1), size=(510, 80), label="", color=(1,1,1,0), on_activate_call=open_bsrush)
        bui.buttonwidget(edit=b1, color=(0,0,0,0), texture=bui.gettexture('transparent'))
            
        # ─── Tajer Button ───
        def open_tajer():
            try: bui.open_url("https://t.me/Tajerbetbot")
            except: pass

        y2 = 100
        AH.draw_panel(self.content_root, 20, y2, 510, 80, bg=COL_BG, border=COL_ACCENT2)
        AH.text(self.content_root, (275, y2+40), "Tajer", scale=1.4, color=COL_TEXT, h="center")
        
        b2 = bui.buttonwidget(parent=self.content_root, position=(20, y2), size=(510, 80), label="", color=(1,1,1,0), on_activate_call=open_tajer)
        bui.buttonwidget(edit=b2, color=(0,0,0,0), texture=bui.gettexture('transparent'))

# ═══════════════════════════════════════════════════════════════
# 🏛️ HUB WINDOW
# ═══════════════════════════════════════════════════════════════

class HubWindow:
    def __init__(self, api):
        self.api = api
        self.w = AH.window(size=(700, 480))
        AH.close_btn(self.w, (630, 420), self.w)
        
        AH.button(self.w, (500, 420), (100, 40), L("logout"), COL_RED, MyCall(self._do_logout), textcolor=(1, 1, 1), text_scale=0.6)
        
        AH.text(self.w, (350, 430), L("hub_title"), scale=1.2, color=COL_GOLD, h="center")
        AH.text(self.w, (350, 400), L("not_in_ally"), scale=0.7, color=COL_DIM, h="center")

        self.content = bui.containerwidget(parent=self.w, position=(20, 20), size=(660, 350), background=False)
        AH.button(self.content, (40, 300), (280, 40), L("create_ally"), COL_ACCENT, MyCall(self._tab_create), textcolor=(1, 1, 1), text_scale=0.8)
        AH.button(self.content, (340, 300), (280, 40), L("join_ally"), COL_ACCENT2, MyCall(self._tab_join), textcolor=(1, 1, 1), text_scale=0.8)

        self.sub = bui.containerwidget(parent=self.content, position=(0, 0), size=(660, 280), background=False)
        self._tab_join()
        
    def _do_logout(self):
        self.api.logout()
        AH.close_window(self.w)
        global _main_win
        _main_win = None
        LoginWindow(self.api, _route_after_login)

    def _clear_sub(self):
        try: self.sub.delete()
        except Exception: pass
        self.sub = bui.containerwidget(parent=self.content, position=(0, 0), size=(660, 280), background=False)

    def _tab_create(self):
        self._clear_sub()
        def cb_status(st):
            if not isinstance(st, dict) or "price" not in st:
                if st == "0": Popup(L("error"), L("already_in_ally"), kind="error")
                else: Popup(L("error"), str(st), kind="error")
                return
            AH.text(self.sub, (330, 220), f"{L('cost')}: {fmt(st['price'])} {L('coins')}", scale=0.9, color=COL_GOLD, h="center")
            self.inp_name = bui.textwidget(parent=self.sub, position=(200, 120), size=(260, 40), editable=True, text="", color=COL_TEXT, h_align="center", max_chars=15)
            AH.button(self.sub, (240, 40), (180, 45), L("create_ally"), COL_ACCENT, MyCall(self._do_create), textcolor=(1, 1, 1), text_scale=0.8)
        Network.fetch(self.api, "create_status", callback=cb_status)

    def _do_create(self):
        name = bui.textwidget(query=self.inp_name).strip()
        if not name: Popup(L("error"), "نام را وارد کنید", kind="error"); return

        def cb(r1):
            if r1 == "confirm_needed":
                def cb2(r2):
                    if isinstance(r2, dict) and "url" in r2: self._go_to_main()
                    elif isinstance(r2, dict) and "err" in r2: Popup(L("error"), str(r2["err"]), kind="error")
                    else: Popup(L("error"), L("create_fail"), kind="error")
                Network.fetch(self.api, "create_ally", (name, 1), callback=cb2)
            elif r1 == "already_in_ally": Popup(L("error"), L("already_in_ally"), kind="error")
            elif isinstance(r1, dict) and "err" in r1: Popup(L("error"), str(r1["err"]), kind="error")
            else: Popup(L("error"), L("create_fail"), kind="error")
        Network.fetch(self.api, "create_ally", (name, 0), callback=cb)

    def _tab_join(self):
        self._clear_sub()
        self.order_type = "rank"
        
        self.inp_search = bui.textwidget(parent=self.sub, position=(80, 220), size=(380, 35), editable=True, text="", color=COL_TEXT, h_align="left", description=L("search"))
        AH.button(self.sub, (480, 220), (120, 35), L("search"), COL_ACCENT, MyCall(self._do_join_search), textcolor=(1, 1, 1), text_scale=0.7)
        
        orders = [("rank", L("order_rank")), ("new", L("order_new")), ("old", L("order_old")), ("count", L("order_count"))]
        x_pos = 80
        self.filter_btns = {}
        for code, name in orders:
            btn = AH.button(self.sub, (x_pos, 160), (140, 35), name, COL_ACCENT if code=="rank" else COL_PANEL, MyCall(self._set_order, code), textcolor=(1,1,1) if code=="rank" else COL_TEXT, text_scale=0.6)
            self.filter_btns[code] = btn
            x_pos += 150

        self.join_scroll = bui.scrollwidget(parent=self.sub, position=(80, 20), size=(520, 120), color=COL_BG, highlight=False)
        self._do_join_search()

    def _set_order(self, code):
        self.order_type = code
        for k, btn in self.filter_btns.items():
            try: bui.buttonwidget(edit=btn, color=COL_ACCENT if k == code else COL_PANEL, textcolor=(1,1,1) if k == code else COL_TEXT)
            except Exception: pass
        self._do_join_search()

    def _do_join_search(self):
        search = bui.textwidget(query=self.inp_search).strip()
        def cb(allies):
            try:
                for c in self.join_scroll.get_children(): c.delete()
            except Exception: pass
            if not isinstance(allies, list): return

            visible = []
            for a in allies:
                req_type = a.get("request")
                if req_type == -1: continue
                visible.append(a)

            row_h = 40
            container = bui.containerwidget(parent=self.join_scroll, size=(520, max(1, len(visible)) * row_h + 10), background=False)
            y = len(visible) * row_h
            for a in visible:
                y -= row_h
                req_type = a.get("request")
                btn_label = L("request_btn") if req_type == 1 else L("join_btn")
                btn_color = COL_ACCENT if req_type == 1 else COL_GREEN

                bui.buttonwidget(parent=container, position=(0, y), size=(500, 36), label="", color=COL_PANEL, enable_sound=False, texture=bui.gettexture('white'))
                AH.text(container, (10, y + 18), f"#{a.get('rank') or '-'} {a.get('name')}", scale=0.7, maxwidth=300, color=COL_TEXT)
                AH.button(container, (380, y + 6), (110, 24), btn_label, btn_color, MyCall(self._do_join, a), textcolor=(1, 1, 1), text_scale=0.6)
        Network.fetch(self.api, "list_allies", (search, self.order_type), callback=cb)

    def _do_join(self, a):
        req_type = a.get("request")
        
        def cb(r):
            if r == "requested":
                Popup(L("success"), L("request_sent"), kind="success", on_ok=self._close_all)
            
            elif r in ("./post/Ally", "./post.php?post=Ally") or (isinstance(r, str) and "post=Ally" in r) or r == "already_in_ally":
                AH.close_window(self.w)
                global _main_win
                _main_win = None
                _safe_timer(1.0, MyCall(_route_after_login))
                
            elif r == "request_rejected": 
                Popup(L("fail"), "درخواست شما قبلا رد شده است.", kind="error")
            elif r == "request_unseen": 
                Popup(L("fail"), "درخواست شما در انتظار بررسی است.", kind="error")
            elif r == "already_left": 
                Popup(L("fail"), "شما اخیرا از این اتحاد خارج شده اید. 24 ساعت صبر کنید.", kind="error")
            else:
                reason = "شما شرایط لازم برای ورود را ندارید."
                reqs = []
                if a.get("coin"): reqs.append(f"حداقل سکه: {a['coin']}")
                if a.get("top"): reqs.append(f"رتبه تاپ: {a['top']}")
                if a.get("score"): reqs.append(f"امتیاز: {a['score']}")
                if a.get("bot"): reqs.append("اتصال به ربات تلگرام")
                
                if reqs: 
                    reason += "\n\nشرایط مورد نیاز:\n- " + "\n- ".join(reqs)
                
                Popup(L("fail"), reason, kind="error")
                
        Network.fetch(self.api, "join_ally", (a["id"],), callback=cb)

    def _close_all(self):
        AH.close_window(self.w)
        global _main_win
        _main_win = None

    def _go_to_main(self):
        AH.close_window(self.w)
        global _main_win
        _main_win = None
        _safe_timer(0.8, MyCall(_route_after_login))

# ═══════════════════════════════════════════════════════════════
# ROUTER
# ═══════════════════════════════════════════════════════════════

_api = None
_main_win = None
_is_opening = False

def _ensure_api():
    global _api
    if _api is None:
        _api = BslifeAPI()
    return _api

def open_ally_manager():
    global _main_win, _is_opening
    if _is_opening or _main_win is not None: return
    _is_opening = True

    api = _ensure_api()
    def check(who):
        global _is_opening
        _is_opening = False
        if not who:
            LoginWindow(api, _route_after_login)
        else:
            _route_after_login()
    Network.fetch(api, "whoami", callback=check)

def _route_after_login():
    global _main_win, _is_opening
    _is_opening = False
    api = _ensure_api()
    
    if _main_win is not None:
        try: _main_win.w.delete()
        except: pass
        _main_win = None

    def check_status(st):
        if st in ("3", "0", "", None):
            api.logout()
            LoginWindow(api, _route_after_login)
            return
        if isinstance(st, dict) and "name" in st:
            _main_win = AllyMainWindow(api)
        else:
            _main_win = HubWindow(api)
    Network.fetch(api, "ally_status", callback=check_status)

def _patch_party_window():
    original_init = party.PartyWindow.__init__

    def patched(self, *a, **k):
        original_init(self, *a, **k)
        try:
            width = getattr(self, "_width", 600)
            height = getattr(self, "_height", 500)
            btn_size = width / 15.0
            btn_x = width - width / 30.0
            bui.buttonwidget(
                parent=self._root_widget, size=(btn_size, btn_size), position=(btn_x, height - 135.0),
                label="⚔", button_type="square", autoselect=False, color=COL_GOLD, textcolor=(0,0,0),
                on_activate_call=MyCall(open_ally_manager), texture=bui.gettexture('buttonSquare')
            )
        except Exception as e:
            log(f"Patch error: {e}")

    party.PartyWindow.__init__ = patched

# ba_meta export babase.Plugin
class BSLifeAllyMod(babase.Plugin):
    def on_app_running(self):
        log("--- Valhalla Edition Loaded ---")
        _patch_party_window()

print("Loaded BSLIFE Ally Manager Valhalla")
