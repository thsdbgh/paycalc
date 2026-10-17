/* 급여계산소 — 사장님 급여관리 앱 */
(function () {
  "use strict";
  var V = document.getElementById("view"), NAV = document.getElementById("nav");
  var S = { me: null, emps: [], ym: thisMonth(), data: null };
  var WD = ["월", "화", "수", "목", "금", "토", "일"];

  function thisMonth() { var d = new Date(); return d.getFullYear() + "-" + String(d.getMonth() + 1).padStart(2, "0"); }
  function addMonth(ym, k) { var y = +ym.slice(0, 4), m = +ym.slice(5, 7) - 1 + k; var d = new Date(Date.UTC(y, m, 1)); return d.toISOString().slice(0, 7); }
  function esc(s) { return String(s == null ? "" : s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function won(n) { return Math.round(n).toLocaleString("ko-KR") + "원"; }
  function toast(msg) { var t = document.getElementById("toast"); t.textContent = msg; t.hidden = false; clearTimeout(toast.t); toast.t = setTimeout(function () { t.hidden = true; }, 2200); }
  function $(sel) { return V.querySelector(sel); }
  // "930" → "09:30", "1530" → "15:30", "9" → "09:00"; 잘못된 값은 빈칸
  function normTime(v) {
    v = String(v || "").trim(); if (!v) return "";
    var m = v.match(/^(\d{1,2})(?::?(\d{2}))?$/); if (!m) return "";
    var h = +m[1], mi = m[2] ? +m[2] : 0;
    if (!m[2] && v.length >= 3) { h = +v.slice(0, v.length - 2); mi = +v.slice(-2); }
    if (h === 24 && mi === 0) h = 0;
    return h < 24 && mi < 60 ? String(h).padStart(2, "0") + ":" + String(mi).padStart(2, "0") : "";
  }
  document.addEventListener("focusout", function (ev) { if (ev.target.classList && ev.target.classList.contains("tm")) { var n = normTime(ev.target.value); if (n !== ev.target.value) { ev.target.value = n; ev.target.dispatchEvent(new Event("input", { bubbles: true })); } } });

  function api(method, path, body) {
    var opt = { method: method, credentials: "same-origin", headers: {} };
    if (body !== undefined) { opt.headers["content-type"] = "application/json"; opt.body = JSON.stringify(body); }
    return fetch("/api" + path, opt).then(function (r) {
      return r.json().catch(function () { return {}; }).then(function (j) {
        if (!r.ok) { var e = new Error(j.error || "오류가 발생했습니다."); e.status = r.status; throw e; }
        return j;
      });
    });
  }

  // ---------------------------------------------------------------- 라우팅
  function route() {
    var h = location.hash.replace(/^#/, "") || "home";
    if (!S.me) return showAuth(h === "signup" ? "signup" : "login");
    NAV.hidden = !S.me;
    var m = h.match(/^emp-(\d+)$/);
    if (m) return showEmployee(+m[1]);
    if (h === "staff") return showStaff();
    if (h === "settings") return showSettings();
    if (h === "login" || h === "signup") { location.hash = "home"; return; }
    return showHome();
  }
  window.addEventListener("hashchange", route);

  function boot() {
    api("GET", "/me").then(function (me) { S.me = me; return loadEmps(); })
      .catch(function () { S.me = null; }).then(route);
  }
  function loadEmps() { return api("GET", "/employees").then(function (j) { S.emps = j.employees; }); }
  function loadMonth() { return api("GET", "/shifts?ym=" + S.ym).then(function (j) { S.data = j; return j; }); }
  function payrollFor(e) {
    var sh = S.data.shifts.filter(function (s) { return s.employeeId === e.id; });
    var ex = S.data.extras.filter(function (x) { return x.employeeId === e.id; })[0];
    return Calc.monthlyPayroll(slipEmp(e, ex), sh, S.ym, !!(S.me.business && S.me.business.size5));
  }

  // ---------------------------------------------------------------- 로그인·가입
  function showAuth(mode) {
    NAV.hidden = true;
    V.innerHTML = '<section class="hero-app"><h1>출퇴근만 적으면<br>월급·명세서가 끝나요</h1>' +
      '<p class="lead">알바 근무시간을 기록하면 주휴수당 주차별 판정, 야간·연장 가산, 4대보험·3.3% 공제, 임금명세서까지 자동으로 계산합니다. 직원에게는 링크로 명세서를 보냅니다.</p>' +
      '<ul class="feat"><li><b>주휴수당 자동 판정</b> — 결근한 주는 빼고, 월을 넘는 주도 정확하게</li><li><b>임금명세서 링크 발송</b> — 5인 미만도 교부 의무, 카톡으로 링크만 보내면 끝</li><li><b>무료</b> — 직원 2명까지 모든 기능 무료</li></ul></section>' +
      '<section class="card auth"><div class="tabs"><button class="btn ' + (mode === "login" ? "primary" : "") + '" data-m="login" type="button">로그인</button><button class="btn ' + (mode === "signup" ? "primary" : "") + '" data-m="signup" type="button">무료로 시작하기</button></div>' +
      '<form class="calc" id="authf"><div class="field"><label for="em">이메일</label><input id="em" type="email" autocomplete="email" required></div>' +
      '<div class="field"><label for="pw">비밀번호 <span class="hint">8자 이상</span></label><input id="pw" type="password" autocomplete="' + (mode === "signup" ? "new-password" : "current-password") + '" minlength="8" required></div>' +
      (mode === "signup" ? '<label style="font-size:14px"><input type="checkbox" id="agree"> <a href="/terms" target="_blank">이용약관</a>과 <a href="/privacy" target="_blank">개인정보처리방침</a>에 동의합니다</label>' : "") +
      '<button class="btn primary" type="submit">' + (mode === "signup" ? "가입하고 시작하기" : "로그인") + '</button><p class="err" id="aerr" hidden></p></form></section>';
    V.querySelectorAll("[data-m]").forEach(function (b) { b.onclick = function () { location.hash = b.dataset.m; showAuth(b.dataset.m); }; });
    $("#authf").onsubmit = function (ev) {
      ev.preventDefault();
      var btn = ev.target.querySelector("button[type=submit]"); btn.disabled = true;
      var body = { email: $("#em").value, password: $("#pw").value, agree: mode === "signup" ? $("#agree").checked : undefined };
      api("POST", mode === "signup" ? "/signup" : "/login", body)
        .then(function () { return api("GET", "/me"); })
        .then(function (me) { S.me = me; return loadEmps(); })
        .then(function () { location.hash = S.emps.length ? "home" : "staff"; route(); })
        .catch(function (e) { var p = $("#aerr"); p.textContent = e.message; p.hidden = false; btn.disabled = false; });
    };
  }

  // ---------------------------------------------------------------- 이번 달 (대시보드)
  function monthBar() {
    return '<div class="monthbar"><button class="btn" type="button" data-mv="-1" aria-label="이전 달">‹</button><b>' +
      S.ym.slice(0, 4) + "년 " + (+S.ym.slice(5, 7)) + '월</b><button class="btn" type="button" data-mv="1" aria-label="다음 달">›</button></div>';
  }
  function bindMonthBar(cb) { V.querySelectorAll("[data-mv]").forEach(function (b) { b.onclick = function () { S.ym = addMonth(S.ym, +b.dataset.mv); cb(); }; }); }

  function showHome() {
    V.innerHTML = '<h1 style="margin-top:20px">' + esc((S.me.business && S.me.business.name) || "우리 매장") + " 급여</h1>" + monthBar() + '<div id="list"><p class="lead">계산 중…</p></div>';
    bindMonthBar(showHome);
    if (!S.emps.length) { $("#list").innerHTML = '<div class="upsell">아직 직원이 없어요. <a href="#staff">직원을 먼저 등록</a>해 주세요.</div>'; return; }
    loadMonth().then(function () {
      var total = 0, html = S.emps.map(function (e) {
        var r = payrollFor(e); total += r.gross;
        return '<a class="emp-card" href="#emp-' + e.id + '"><div><b>' + esc(e.name) + '</b><div class="m">' + r.days + "일 · " + Calc.num(r.hours.toFixed(1)) + "시간 · 주휴 " + r.paidWeeks + '주</div></div><div class="amt">' + won(r.gross) + "</div></a>";
      }).join("");
      $("#list").innerHTML = '<div class="sumbox"><div><b>' + S.emps.length + '명</b><span>직원</span></div><div><b>' + won(total) + '</b><span>지급 총액 (세전)</span></div><div><b>' + (S.me.business && S.me.business.size5 ? "5인 이상" : "5인 미만") + '</b><span>가산수당 기준</span></div></div>' +
        html + '<p class="note">직원을 누르면 근무시간을 입력하고 명세서를 만들 수 있어요.</p>' + upsell();
      bindUpsell();
    }).catch(fail);
  }

  function upsell() {
    if (S.me.plan === "pro") return "";
    return '<div class="upsell no-print"><b>직원이 3명 이상인가요?</b> 프로 플랜(월 9,900원 예정)으로 인원 제한 없이 쓸 수 있어요. ' +
      (S.me.proRequested ? "출시 알림 신청 완료 ✓" : '<button class="btn" type="button" id="proreq">출시 알림 받기</button>') + "</div>";
  }
  function bindUpsell() {
    var b = document.getElementById("proreq");
    if (b) b.onclick = function () { api("POST", "/pro-request", {}).then(function () { S.me.proRequested = true; b.outerHTML = "출시 알림 신청 완료 ✓"; toast("프로 플랜이 열리면 알려드릴게요"); }).catch(fail); };
  }

  // ---------------------------------------------------------------- 직원 1명: 근무 입력 + 명세서
  function showEmployee(id) {
    var e = S.emps.filter(function (x) { return x.id === id; })[0];
    if (!e) { location.hash = "home"; return; }
    V.innerHTML = '<p class="crumb"><a href="#home">이번 달</a> › ' + esc(e.name) + '</p><h1>' + esc(e.name) + '</h1>' + monthBar() + '<div id="emp"><p class="lead">불러오는 중…</p></div>';
    bindMonthBar(function () { showEmployee(id); });
    loadMonth().then(function () { renderEmployee(e); }).catch(fail);
  }

  function renderEmployee(e) {
    var y = +S.ym.slice(0, 4), m = +S.ym.slice(5, 7), last = new Date(Date.UTC(y, m, 0)).getUTCDate();
    var mine = {}; S.data.shifts.forEach(function (s) { if (s.employeeId === e.id) mine[s.date] = s; });
    var ex = S.data.extras.filter(function (x) { return x.employeeId === e.id; })[0] || { extra: 0, nontax: 0 };
    var rows = "";
    for (var d = 1; d <= last; d++) {
      var ds = S.ym + "-" + String(d).padStart(2, "0"), dt = new Date(Date.UTC(y, m - 1, d)), wd = (dt.getUTCDay() + 6) % 7, s = mine[ds] || {};
      rows += '<div class="day' + (wd >= 5 ? " we" : "") + (s.absent ? " absent" : "") + '" data-d="' + ds + '"><div class="dl">' + d + "일<small>" + WD[wd] + "</small></div>" +
        '<input class="st tm" inputmode="numeric" maxlength="5" placeholder="--:--" value="' + (s.start || "") + '" aria-label="' + d + '일 출근"><input class="en tm" inputmode="numeric" maxlength="5" placeholder="--:--" value="' + (s.end || "") + '" aria-label="' + d + '일 퇴근">' +
        '<input type="number" class="br" min="0" step="10" inputmode="numeric" value="' + (s.start ? s.breakMin : "") + '" placeholder="휴게" aria-label="' + d + '일 휴게(분)">' +
        '<label class="ab"><input type="checkbox" class="abs"' + (s.absent ? " checked" : "") + '>결근</label></div>';
    }
    $("#emp").innerHTML = '<div class="sumbox" id="sum"></div>' +
      '<details class="pattern"><summary><b>근무 패턴으로 한 번에 채우기</b></summary><div class="wd">' +
      WD.map(function (w, i) { return '<label><input type="checkbox" value="' + i + '"' + (i < 5 ? " checked" : "") + ">" + w + "</label>"; }).join("") +
      '</div><div class="tt"><input class="tm" id="pst" inputmode="numeric" maxlength="5" value="10:00" aria-label="출근"><input class="tm" id="pen" inputmode="numeric" maxlength="5" value="15:00" aria-label="퇴근"><input type="number" id="pbr" value="30" min="0" step="10" aria-label="휴게(분)"></div>' +
      '<div class="row-actions"><button class="btn" type="button" id="pfill">빈 날에 채우기</button><button class="btn" type="button" id="pclear">이번 달 모두 지우기</button></div></details>' +
      '<div class="dayhead"><span>날짜</span><span>출근</span><span>퇴근</span><span>휴게(분)</span><span></span></div><div class="days" id="days">' + rows + "</div>" +
      '<div class="two"><div class="field"><label for="extra">기타 수당 <span class="hint">이번 달</span></label><input id="extra" inputmode="numeric" value="' + (ex.extra || 0) + '"></div>' +
      '<div class="field"><label for="nontax">식대 등 비과세 <span class="hint">이번 달</span></label><input id="nontax" inputmode="numeric" value="' + (ex.nontax || 0) + '"></div></div>' +
      '<div class="savebar"><button class="btn primary" type="button" id="save">저장</button><button class="btn" type="button" id="slipbtn">명세서 보기</button></div>' +
      '<div id="slipwrap"></div>';

    var dirty = false;
    var collect = function () {
      var arr = [];
      V.querySelectorAll(".day").forEach(function (row) {
        arr.push({ employeeId: e.id, date: row.dataset.d, start: normTime(row.querySelector(".st").value), end: normTime(row.querySelector(".en").value),
                   breakMin: +row.querySelector(".br").value || 0, absent: row.querySelector(".abs").checked });
      });
      return arr;
    };
    var current = function () {
      var others = S.data.shifts.filter(function (s) { return s.employeeId === e.id && s.date.slice(0, 7) !== S.ym; });
      var cur = collect().filter(function (x) { return x.absent || (x.start && x.end); });
      var emp = slipEmp(e, { extra: Calc.num($("#extra").value), nontax: Calc.num($("#nontax").value) });
      return Calc.monthlyPayroll(emp, others.concat(cur), S.ym, !!S.me.business.size5);
    };
    var refresh = function () {
      var r = current();
      $("#sum").innerHTML = '<div><b>' + Calc.num(r.hours.toFixed(1)) + 'h</b><span>' + r.days + '일 근무</span></div><div><b>' + won(r.juhyu) + '</b><span>주휴 ' + r.paidWeeks + '주</span></div><div><b>' + won(r.net) + '</b><span>실지급 (공제 후)</span></div>';
    };
    V.querySelectorAll(".day").forEach(function (row) {
      row.addEventListener("input", function () { dirty = true; row.classList.toggle("absent", row.querySelector(".abs").checked); refresh(); });
      row.querySelector(".st").addEventListener("change", function () { if (!row.querySelector(".br").value) row.querySelector(".br").value = 0; });
    });
    ["#extra", "#nontax"].forEach(function (s) { $(s).addEventListener("input", function () { dirty = true; refresh(); }); });
    $("#pfill").onclick = function () {
      var wds = [].map.call(V.querySelectorAll(".pattern .wd input:checked"), function (x) { return +x.value; });
      var st = normTime($("#pst").value), en = normTime($("#pen").value), br = $("#pbr").value || 0, n = 0;
      V.querySelectorAll(".day").forEach(function (row) {
        var dt = new Date(row.dataset.d + "T00:00:00Z"), wd = (dt.getUTCDay() + 6) % 7;
        if (wds.indexOf(wd) < 0 || row.querySelector(".st").value || row.querySelector(".abs").checked) return;
        row.querySelector(".st").value = st; row.querySelector(".en").value = en; row.querySelector(".br").value = br; n++;
      });
      dirty = true; refresh(); toast(n + "일을 채웠어요. 저장을 눌러 주세요.");
    };
    $("#pclear").onclick = function () {
      V.querySelectorAll(".day").forEach(function (row) { row.querySelector(".st").value = ""; row.querySelector(".en").value = ""; row.querySelector(".br").value = ""; row.querySelector(".abs").checked = false; row.classList.remove("absent"); });
      dirty = true; refresh();
    };
    var save = function () {
      var btn = $("#save"); btn.disabled = true;
      return api("PUT", "/shifts", { items: collect() })
        .then(function () { return api("PUT", "/extras", { employeeId: e.id, ym: S.ym, extra: Calc.num($("#extra").value), nontax: Calc.num($("#nontax").value) }); })
        .then(function () { return loadMonth(); })
        .then(function () { dirty = false; toast("저장했어요"); })
        .catch(fail).then(function () { btn.disabled = false; });
    };
    $("#save").onclick = save;
    $("#slipbtn").onclick = function () {
      (dirty ? save() : Promise.resolve()).then(function () {
        var r = current(), link = location.origin + "/app/s.html?t=" + encodeURIComponent(e.shareToken) + "&ym=" + S.ym;
        $("#slipwrap").innerHTML = '<h2>임금명세서</h2>' + renderSlip(e, S.me.business, S.ym, r) +
          '<p class="note no-print">직원에게 아래 링크를 카카오톡이나 문자로 보내면 명세서를 볼 수 있어요 (전자 교부).</p>' +
          '<div class="linkbox no-print"><input id="lnk" readonly value="' + esc(link) + '"><button class="btn" type="button" id="cp">복사</button></div>' +
          '<div class="row-actions no-print"><button class="btn primary" type="button" onclick="window.print()">인쇄 · PDF 저장</button></div>';
        $("#cp").onclick = function () {
          var inp = $("#lnk");
          (navigator.clipboard ? navigator.clipboard.writeText(inp.value) : Promise.reject()).then(function () { toast("링크를 복사했어요"); },
            function () { inp.select(); toast("링크를 길게 눌러 복사하세요"); });
        };
        $("#slipwrap").scrollIntoView({ behavior: "smooth" });
      });
    };
    window.onbeforeunload = function () { return dirty ? "저장하지 않은 근무기록이 있어요." : undefined; };
    refresh();
  }

  // ---------------------------------------------------------------- 직원 관리
  function empForm(e) {
    e = e || { name: "", birth: "", hourly: 10320, weeklyHours: 20, deduction: "33", family: 1, kids: 0 };
    var opt = function (v, l) { return '<option value="' + v + '"' + (e.deduction === v ? " selected" : "") + ">" + l + "</option>"; };
    return '<form class="calc card" id="ef"><div class="two"><div class="field"><label for="f-name">이름</label><input id="f-name" value="' + esc(e.name) + '" required maxlength="40"></div>' +
      '<div class="field"><label for="f-birth">생년월일 <span class="hint">명세서용</span></label><input id="f-birth" type="date" value="' + esc(e.birth) + '"></div></div>' +
      '<div class="two"><div class="field"><label for="f-hourly">시급</label><input id="f-hourly" inputmode="numeric" value="' + e.hourly + '"></div>' +
      '<div class="field"><label for="f-weekly">주 소정근로시간 <span class="hint">계약서 기준</span></label><input id="f-weekly" type="number" step="0.5" min="0" value="' + e.weeklyHours + '"></div></div>' +
      '<div class="two"><div class="field"><label for="f-ded">공제 방식</label><select id="f-ded">' + opt("none", "공제 없음") + opt("33", "3.3% (사업소득)") + opt("ins", "4대보험 + 근로소득세") + '</select></div>' +
      '<div class="field"><label for="f-fam">공제대상가족 <span class="hint">4대보험만</span></label><input id="f-fam" type="number" min="1" max="20" value="' + e.family + '"></div></div>' +
      '<div class="row-actions"><button class="btn primary" type="submit">' + (e.id ? "수정 저장" : "직원 추가") + "</button>" +
      (e.id ? '<button class="btn" type="button" id="f-del">삭제</button><button class="btn" type="button" id="f-reset">명세서 링크 새로 만들기</button>' : "") + "</div>" +
      '<p class="err" id="ferr" hidden></p></form>';
  }
  function showStaff(editId) {
    var e = editId ? S.emps.filter(function (x) { return x.id === editId; })[0] : null;
    var full = S.me.plan !== "pro" && S.emps.length >= S.me.employeeLimit && !e;
    V.innerHTML = '<h1 style="margin-top:20px">직원</h1>' +
      S.emps.map(function (x) { return '<a class="emp-card" href="#" data-ed="' + x.id + '"><div><b>' + esc(x.name) + '</b><div class="m">시급 ' + won(x.hourly) + " · 주 " + x.weeklyHours + "시간 · " + ({ none: "공제 없음", "33": "3.3%", ins: "4대보험" })[x.deduction] + '</div></div><div class="m">수정 ›</div></a>'; }).join("") +
      "<h2>" + (e ? esc(e.name) + " 수정" : "직원 추가") + "</h2>" +
      (full ? upsell() : empForm(e)) +
      '<p class="note">주 소정근로시간이 15시간 이상이면 주휴수당이, 월 60시간 이상이면 4대보험이 계산됩니다. 최저임금: 2026년 10,320원, 2027년 10,700원.</p>';
    V.querySelectorAll("[data-ed]").forEach(function (a) { a.onclick = function (ev) { ev.preventDefault(); showStaff(+a.dataset.ed); }; });
    bindUpsell();
    var f = $("#ef"); if (!f) return;
    f.onsubmit = function (ev) {
      ev.preventDefault();
      var body = { name: $("#f-name").value, birth: $("#f-birth").value, hourly: Calc.num($("#f-hourly").value), weeklyHours: +$("#f-weekly").value,
                   deduction: $("#f-ded").value, family: +$("#f-fam").value || 1, kids: 0 };
      if (body.hourly && body.hourly < Calc.MIN_WAGE[2026] && !confirmLow()) return;
      (e ? api("PUT", "/employees/" + e.id, body) : api("POST", "/employees", body))
        .then(loadEmps).then(function () { return api("GET", "/me"); }).then(function (me) { S.me = me; toast(e ? "수정했어요" : "직원을 추가했어요"); showStaff(); })
        .catch(function (er) { var p = $("#ferr"); p.textContent = er.message; p.hidden = false; });
    };
    if (e) {
      $("#f-del").onclick = function () {
        if (this.dataset.ok !== "1") { this.dataset.ok = "1"; this.textContent = "한 번 더 누르면 삭제"; return; }
        api("DELETE", "/employees/" + e.id).then(loadEmps).then(function () { return api("GET", "/me"); }).then(function (me) { S.me = me; toast("삭제했어요"); showStaff(); }).catch(fail);
      };
      $("#f-reset").onclick = function () {
        api("POST", "/employees/" + e.id + "/reset-link", {}).then(loadEmps).then(function () { toast("이전 링크는 더 이상 열리지 않아요"); }).catch(fail);
      };
    }
  }
  function confirmLow() { if (confirmLow.ok) { confirmLow.ok = false; return true; } confirmLow.ok = true; toast("시급이 2026년 최저임금(10,320원)보다 낮아요. 맞다면 한 번 더 저장을 누르세요."); return false; }

  // ---------------------------------------------------------------- 설정
  function showSettings() {
    var b = S.me.business || {};
    V.innerHTML = '<h1 style="margin-top:20px">설정</h1><form class="calc card" id="bf">' +
      '<div class="two"><div class="field"><label for="b-name">사업장명</label><input id="b-name" value="' + esc(b.name) + '" maxlength="60"></div>' +
      '<div class="field"><label for="b-ceo">대표자</label><input id="b-ceo" value="' + esc(b.ceo) + '" maxlength="30"></div></div>' +
      '<div class="two"><div class="field"><label for="b-size">상시 근로자 수</label><select id="b-size"><option value="0"' + (b.size5 ? "" : " selected") + '>5인 미만</option><option value="1"' + (b.size5 ? " selected" : "") + '>5인 이상 (가산수당 적용)</option></select></div>' +
      '<div class="field"><label for="b-pay">급여 지급일 <span class="hint">다음 달</span></label><input id="b-pay" type="number" min="1" max="28" value="' + (b.payday || 10) + '"></div></div>' +
      '<button class="btn primary" type="submit">저장</button></form>' +
      '<h2>계정</h2><p>' + esc(S.me.email) + " · " + (S.me.plan === "pro" ? "프로" : "무료 플랜 (직원 " + S.me.employeeLimit + "명까지)") + "</p>" + upsell() +
      '<div class="row-actions"><button class="btn" type="button" id="logout">로그아웃</button><button class="btn" type="button" id="delacc">회원 탈퇴</button></div>' +
      '<p class="note">회원 탈퇴 시 사업장·직원·근무기록이 모두 즉시 삭제됩니다.</p>';
    bindUpsell();
    $("#bf").onsubmit = function (ev) {
      ev.preventDefault();
      var body = { name: $("#b-name").value, ceo: $("#b-ceo").value, size5: $("#b-size").value === "1", payday: +$("#b-pay").value };
      api("PUT", "/business", body).then(function () { return api("GET", "/me"); }).then(function (me) { S.me = me; toast("저장했어요"); }).catch(fail);
    };
    $("#logout").onclick = function () { api("POST", "/logout", {}).then(function () { S.me = null; location.hash = "login"; route(); }); };
    $("#delacc").onclick = function () {
      if (this.dataset.ok !== "1") { this.dataset.ok = "1"; this.textContent = "한 번 더 누르면 모든 데이터 삭제"; return; }
      api("DELETE", "/account").then(function () { S.me = null; location.hash = "signup"; route(); toast("탈퇴했어요. 모든 데이터를 삭제했습니다."); }).catch(fail);
    };
  }

  function fail(e) {
    if (e && e.status === 401) { S.me = null; location.hash = "login"; route(); return; }
    toast((e && e.message) || "오류가 발생했습니다.");
  }
  boot();
})();
