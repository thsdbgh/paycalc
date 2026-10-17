// 급여계산소 — 사장님 급여관리 API (Cloudflare Worker + D1)
// /api/* 요청만 이 코드가 처리하고, 나머지는 정적 사이트(docs/)를 그대로 서빙한다.

const FREE_EMPLOYEE_LIMIT = 2;
const SESSION_DAYS = 30;
const PBKDF2_ITER = 20000; // 무료 플랜 CPU 한도를 고려한 값. 사용자별로 저장되어 나중에 올릴 수 있음.
const enc = new TextEncoder();

const json = (data, status = 200, headers = {}) =>
  new Response(JSON.stringify(data), { status, headers: { "content-type": "application/json; charset=utf-8", "cache-control": "no-store", ...headers } });
const err = (status, message) => json({ error: message }, status);

const b64u = (buf) => btoa(String.fromCharCode(...new Uint8Array(buf))).replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, "");
const randToken = (n = 24) => b64u(crypto.getRandomValues(new Uint8Array(n)));
async function sha256(s) { return b64u(await crypto.subtle.digest("SHA-256", enc.encode(s))); }
async function pbkdf2(password, salt, iter) {
  const key = await crypto.subtle.importKey("raw", enc.encode(password), "PBKDF2", false, ["deriveBits"]);
  const bits = await crypto.subtle.deriveBits({ name: "PBKDF2", hash: "SHA-256", salt: enc.encode(salt), iterations: iter }, key, 256);
  return b64u(bits);
}
function safeEq(a, b) {
  if (a.length !== b.length) return false;
  let r = 0; for (let i = 0; i < a.length; i++) r |= a.charCodeAt(i) ^ b.charCodeAt(i);
  return r === 0;
}
function cookie(req, name) {
  const m = (req.headers.get("cookie") || "").match(new RegExp("(?:^|;\\s*)" + name + "=([^;]+)"));
  return m ? m[1] : null;
}
const sessionCookie = (token, maxAge) =>
  `gs=${token}; Path=/; HttpOnly; Secure; SameSite=Lax; Max-Age=${maxAge}`;

const isDate = (s) => typeof s === "string" && /^\d{4}-\d{2}-\d{2}$/.test(s);
const isTime = (s) => s === "" || (typeof s === "string" && /^([01]\d|2[0-3]):[0-5]\d$/.test(s));
const isYm = (s) => typeof s === "string" && /^\d{4}-(0[1-9]|1[0-2])$/.test(s);
const clampInt = (v, lo, hi) => Math.min(hi, Math.max(lo, Math.round(Number(v) || 0)));
const str = (v, max) => String(v == null ? "" : v).trim().slice(0, max);

async function readJson(req) {
  if (!(req.headers.get("content-type") || "").includes("application/json")) throw new Error("json");
  return await req.json();
}

async function currentUser(env, req) {
  const tok = cookie(req, "gs");
  if (!tok) return null;
  const row = await env.DB.prepare(
    "SELECT u.id, u.email, u.plan, u.pro_requested FROM sessions s JOIN users u ON u.id = s.user_id WHERE s.token_hash = ? AND s.expires_at > datetime('now')"
  ).bind(await sha256(tok)).first();
  return row || null;
}

async function rateLimited(env, key, max, windowSec) {
  const now = Math.floor(Date.now() / 1000);
  await env.DB.prepare("DELETE FROM login_attempts WHERE ts < ?").bind(now - 86400).run();
  const c = await env.DB.prepare("SELECT COUNT(*) AS n FROM login_attempts WHERE key = ? AND ts > ?").bind(key, now - windowSec).first();
  if (c.n >= max) return true;
  await env.DB.prepare("INSERT INTO login_attempts (key, ts) VALUES (?, ?)").bind(key, now).run();
  return false;
}

async function startSession(env, userId) {
  const token = randToken(32);
  await env.DB.prepare("INSERT INTO sessions (token_hash, user_id, expires_at) VALUES (?, ?, datetime('now', ?))")
    .bind(await sha256(token), userId, `+${SESSION_DAYS} days`).run();
  return json({ ok: true }, 200, { "set-cookie": sessionCookie(token, SESSION_DAYS * 86400) });
}

function employeeOut(e) {
  return { id: e.id, name: e.name, birth: e.birth, hourly: e.hourly, weeklyHours: e.weekly_hours, deduction: e.deduction,
           family: e.family, kids: e.kids, shareToken: e.share_token, active: !!e.active };
}
function validEmployee(b) {
  const name = str(b.name, 40);
  const hourly = clampInt(b.hourly, 0, 1000000);
  const weekly = Math.min(80, Math.max(0, Number(b.weeklyHours) || 0));
  const deduction = ["none", "33", "ins"].includes(b.deduction) ? b.deduction : "none";
  const birth = b.birth && isDate(b.birth) ? b.birth : "";
  if (!name) throw new Error("직원 이름을 입력하세요.");
  if (!hourly) throw new Error("시급을 입력하세요.");
  return { name, hourly, weekly, deduction, birth, family: clampInt(b.family, 1, 20), kids: clampInt(b.kids, 0, 10) };
}
// 귀속월 계산에 필요한 범위: 그 달 첫 주휴 판정 주의 월요일 ~ 말일
function monthRange(ym) {
  const y = +ym.slice(0, 4), m = +ym.slice(5, 7);
  const first = new Date(Date.UTC(y, m - 1, 1));
  const from = new Date(first.getTime() - 6 * 86400000).toISOString().slice(0, 10);
  const to = new Date(Date.UTC(y, m, 0)).toISOString().slice(0, 10);
  return [from, to];
}
const shiftOut = (s) => ({ id: s.id, employeeId: s.employee_id, date: s.date, start: s.start, end: s.end, breakMin: s.break_min, absent: !!s.absent });

async function api(req, env, url) {
  const p = url.pathname.replace(/\/+$/, "");
  const m = req.method;
  const ip = req.headers.get("cf-connecting-ip") || "0";

  if (p === "/api/health") return json({ ok: true, time: new Date().toISOString() });
  if (p === "/api/selftest") {
    const t0 = Date.now(); await pbkdf2("selftest-password", "salt-salt-salt", PBKDF2_ITER); const t1 = Date.now();
    const c = await env.DB.prepare("SELECT COUNT(*) AS n FROM users").first();
    return json({ pbkdf2Ms: t1 - t0, iter: PBKDF2_ITER, db: c.n >= 0 });
  }

  // ---- 공개: 직원용 명세서 보기 ----
  let mm = p.match(/^\/api\/share\/([A-Za-z0-9_-]{20,64})$/);
  if (mm && m === "GET") {
    const ym = url.searchParams.get("ym");
    if (!isYm(ym)) return err(400, "월을 확인하세요.");
    const e = await env.DB.prepare("SELECT * FROM employees WHERE share_token = ? AND active = 1").bind(mm[1]).first();
    if (!e) return err(404, "명세서를 찾을 수 없습니다. 링크를 다시 확인하세요.");
    const biz = await env.DB.prepare("SELECT name, ceo, size5, payday FROM businesses WHERE user_id = ?").bind(e.user_id).first();
    const [from, to] = monthRange(ym);
    const rs = await env.DB.prepare("SELECT * FROM shifts WHERE employee_id = ? AND date BETWEEN ? AND ? ORDER BY date").bind(e.id, from, to).all();
    const ex = await env.DB.prepare("SELECT extra, nontax FROM monthly_extras WHERE employee_id = ? AND ym = ?").bind(e.id, ym).first();
    const emp = employeeOut(e); delete emp.shareToken;
    return json({ employee: emp, business: biz || {}, shifts: rs.results.map(shiftOut), extras: ex || { extra: 0, nontax: 0 } });
  }

  // ---- 회원 ----
  if (p === "/api/signup" && m === "POST") {
    const b = await readJson(req);
    const email = str(b.email, 120).toLowerCase(), pw = String(b.password || "");
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) return err(400, "이메일 형식을 확인하세요.");
    if (pw.length < 8) return err(400, "비밀번호는 8자 이상으로 정해 주세요.");
    if (!b.agree) return err(400, "이용약관과 개인정보처리방침에 동의해 주세요.");
    if (await rateLimited(env, "signup:" + ip, 10, 3600)) return err(429, "잠시 후 다시 시도하세요.");
    const exists = await env.DB.prepare("SELECT id FROM users WHERE email = ?").bind(email).first();
    if (exists) return err(409, "이미 가입된 이메일입니다. 로그인해 주세요.");
    const salt = randToken(16), hash = await pbkdf2(pw, salt, PBKDF2_ITER);
    const r = await env.DB.prepare("INSERT INTO users (email, pw_hash, pw_salt, pw_iter) VALUES (?, ?, ?, ?)").bind(email, hash, salt, PBKDF2_ITER).run();
    const uid = r.meta.last_row_id;
    await env.DB.prepare("INSERT INTO businesses (user_id) VALUES (?)").bind(uid).run();
    return startSession(env, uid);
  }
  if (p === "/api/login" && m === "POST") {
    const b = await readJson(req);
    const email = str(b.email, 120).toLowerCase(), pw = String(b.password || "");
    if (await rateLimited(env, "login:" + email, 8, 900) || await rateLimited(env, "loginip:" + ip, 30, 900))
      return err(429, "로그인 시도가 많습니다. 15분 뒤 다시 시도하세요.");
    const u = await env.DB.prepare("SELECT * FROM users WHERE email = ?").bind(email).first();
    if (!u || !safeEq(await pbkdf2(pw, u.pw_salt, u.pw_iter), u.pw_hash)) return err(401, "이메일 또는 비밀번호가 맞지 않습니다.");
    return startSession(env, u.id);
  }
  if (p === "/api/logout" && m === "POST") {
    const tok = cookie(req, "gs");
    if (tok) await env.DB.prepare("DELETE FROM sessions WHERE token_hash = ?").bind(await sha256(tok)).run();
    return json({ ok: true }, 200, { "set-cookie": sessionCookie("", 0) });
  }

  const user = await currentUser(env, req);
  if (!user) return err(401, "로그인이 필요합니다.");
  if (m !== "GET" && !(req.headers.get("content-type") || "").includes("application/json") && m !== "DELETE")
    return err(415, "잘못된 요청입니다.");

  if (p === "/api/me" && m === "GET") {
    const biz = await env.DB.prepare("SELECT name, ceo, size5, payday FROM businesses WHERE user_id = ?").bind(user.id).first();
    const cnt = await env.DB.prepare("SELECT COUNT(*) AS n FROM employees WHERE user_id = ? AND active = 1").bind(user.id).first();
    return json({ email: user.email, plan: user.plan, proRequested: !!user.pro_requested, business: biz,
                  employeeCount: cnt.n, employeeLimit: user.plan === "pro" ? null : FREE_EMPLOYEE_LIMIT });
  }
  if (p === "/api/business" && m === "PUT") {
    const b = await readJson(req);
    await env.DB.prepare("UPDATE businesses SET name = ?, ceo = ?, size5 = ?, payday = ? WHERE user_id = ?")
      .bind(str(b.name, 60), str(b.ceo, 30), b.size5 ? 1 : 0, clampInt(b.payday, 1, 31), user.id).run();
    return json({ ok: true });
  }
  if (p === "/api/pro-request" && m === "POST") {
    await env.DB.prepare("UPDATE users SET pro_requested = 1 WHERE id = ?").bind(user.id).run();
    return json({ ok: true });
  }
  if (p === "/api/account" && m === "DELETE") {
    await env.DB.prepare("DELETE FROM users WHERE id = ?").bind(user.id).run();
    return json({ ok: true }, 200, { "set-cookie": sessionCookie("", 0) });
  }

  // ---- 직원 ----
  if (p === "/api/employees" && m === "GET") {
    const rs = await env.DB.prepare("SELECT * FROM employees WHERE user_id = ? AND active = 1 ORDER BY id").bind(user.id).all();
    return json({ employees: rs.results.map(employeeOut) });
  }
  if (p === "/api/employees" && m === "POST") {
    let v; try { v = validEmployee(await readJson(req)); } catch (e) { return err(400, e.message); }
    if (user.plan !== "pro") {
      const cnt = await env.DB.prepare("SELECT COUNT(*) AS n FROM employees WHERE user_id = ? AND active = 1").bind(user.id).first();
      if (cnt.n >= FREE_EMPLOYEE_LIMIT) return err(402, `무료 플랜은 직원 ${FREE_EMPLOYEE_LIMIT}명까지 등록할 수 있습니다.`);
    }
    const r = await env.DB.prepare("INSERT INTO employees (user_id, name, birth, hourly, weekly_hours, deduction, family, kids, share_token) VALUES (?,?,?,?,?,?,?,?,?)")
      .bind(user.id, v.name, v.birth, v.hourly, v.weekly, v.deduction, v.family, v.kids, randToken(24)).run();
    return json({ id: r.meta.last_row_id });
  }
  mm = p.match(/^\/api\/employees\/(\d+)$/);
  if (mm) {
    const id = +mm[1];
    const own = await env.DB.prepare("SELECT id FROM employees WHERE id = ? AND user_id = ?").bind(id, user.id).first();
    if (!own) return err(404, "직원을 찾을 수 없습니다.");
    if (m === "PUT") {
      let v; try { v = validEmployee(await readJson(req)); } catch (e) { return err(400, e.message); }
      await env.DB.prepare("UPDATE employees SET name=?, birth=?, hourly=?, weekly_hours=?, deduction=?, family=?, kids=? WHERE id = ?")
        .bind(v.name, v.birth, v.hourly, v.weekly, v.deduction, v.family, v.kids, id).run();
      return json({ ok: true });
    }
    if (m === "DELETE") {
      await env.DB.prepare("UPDATE employees SET active = 0, share_token = ? WHERE id = ?").bind("x" + randToken(24), id).run();
      return json({ ok: true });
    }
  }
  mm = p.match(/^\/api\/employees\/(\d+)\/reset-link$/);
  if (mm && m === "POST") {
    const r = await env.DB.prepare("UPDATE employees SET share_token = ? WHERE id = ? AND user_id = ?").bind(randToken(24), +mm[1], user.id).run();
    return r.meta.changes ? json({ ok: true }) : err(404, "직원을 찾을 수 없습니다.");
  }

  // ---- 근무기록 ----
  if (p === "/api/shifts" && m === "GET") {
    const ym = url.searchParams.get("ym");
    if (!isYm(ym)) return err(400, "월을 확인하세요.");
    const [from, to] = monthRange(ym);
    const rs = await env.DB.prepare("SELECT * FROM shifts WHERE user_id = ? AND date BETWEEN ? AND ? ORDER BY date").bind(user.id, from, to).all();
    const ex = await env.DB.prepare("SELECT x.* FROM monthly_extras x JOIN employees e ON e.id = x.employee_id WHERE e.user_id = ? AND x.ym = ?").bind(user.id, ym).all();
    return json({ shifts: rs.results.map(shiftOut), extras: ex.results.map((x) => ({ employeeId: x.employee_id, extra: x.extra, nontax: x.nontax })) });
  }
  if (p === "/api/shifts" && m === "PUT") {
    // 여러 건 저장(덮어쓰기). 빈 시간 + 결근 아님 = 삭제
    const b = await readJson(req);
    const items = Array.isArray(b.items) ? b.items.slice(0, 400) : [];
    const empIds = [...new Set(items.map((x) => +x.employeeId))];
    for (const eid of empIds) {
      const own = await env.DB.prepare("SELECT id FROM employees WHERE id = ? AND user_id = ? AND active = 1").bind(eid, user.id).first();
      if (!own) return err(404, "직원을 찾을 수 없습니다.");
    }
    const stmts = [];
    for (const x of items) {
      if (!isDate(x.date) || !isTime(x.start || "") || !isTime(x.end || "")) return err(400, "날짜나 시간 형식을 확인하세요.");
      const absent = x.absent ? 1 : 0;
      if (!absent && (!x.start || !x.end)) {
        stmts.push(env.DB.prepare("DELETE FROM shifts WHERE employee_id = ? AND date = ?").bind(+x.employeeId, x.date));
      } else {
        stmts.push(env.DB.prepare(
          "INSERT INTO shifts (user_id, employee_id, date, start, end, break_min, absent) VALUES (?,?,?,?,?,?,?) " +
          "ON CONFLICT(employee_id, date) DO UPDATE SET start = excluded.start, end = excluded.end, break_min = excluded.break_min, absent = excluded.absent"
        ).bind(user.id, +x.employeeId, x.date, absent ? "" : x.start, absent ? "" : x.end, absent ? 0 : clampInt(x.breakMin, 0, 600), absent));
      }
    }
    if (stmts.length) await env.DB.batch(stmts);
    return json({ ok: true, saved: stmts.length });
  }
  if (p === "/api/extras" && m === "PUT") {
    const b = await readJson(req);
    if (!isYm(b.ym)) return err(400, "월을 확인하세요.");
    const own = await env.DB.prepare("SELECT id FROM employees WHERE id = ? AND user_id = ?").bind(+b.employeeId, user.id).first();
    if (!own) return err(404, "직원을 찾을 수 없습니다.");
    await env.DB.prepare("INSERT INTO monthly_extras (employee_id, ym, extra, nontax) VALUES (?,?,?,?) ON CONFLICT(employee_id, ym) DO UPDATE SET extra = excluded.extra, nontax = excluded.nontax")
      .bind(+b.employeeId, b.ym, clampInt(b.extra, 0, 1e9), clampInt(b.nontax, 0, 1e9)).run();
    return json({ ok: true });
  }

  return err(404, "없는 기능입니다.");
}

export default {
  async fetch(req, env) {
    const url = new URL(req.url);
    if (url.pathname.startsWith("/api/")) {
      if (!env.DB) return err(503, "데이터베이스 연결이 준비되지 않았습니다.");
      try {
        return await api(req, env, url);
      } catch (e) {
        if (e && e.message === "json") return err(415, "잘못된 요청입니다.");
        console.error(e);
        return err(500, "일시적인 오류입니다. 잠시 후 다시 시도하세요.");
      }
    }
    return env.ASSETS.fetch(req);
  },
};
