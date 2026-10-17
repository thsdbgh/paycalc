/* 급여계산소 — 공통 UI 도우미 */
(function () {
  "use strict";
  var won = function (n) { return Math.round(n).toLocaleString("ko-KR") + "원"; };
  var fmt = function (n, dgt) { return Number(n).toLocaleString("ko-KR", { maximumFractionDigits: dgt == null ? 1 : dgt }); };
  window.U = { won: won, fmt: fmt,
    val: function (id) { var el = document.getElementById(id); return el ? Calc.num(el.value) : 0; },
    str: function (id) { var el = document.getElementById(id); return el ? el.value : ""; },
    set: function (id, html) { var el = document.getElementById(id); if (el) el.innerHTML = html; },
    row: function (label, value, strong) {
      return '<div class="r' + (strong ? " strong" : "") + '"><span>' + label + "</span><b>" + value + "</b></div>";
    },
    note: function (text, kind) { return '<p class="note ' + (kind || "") + '">' + text + "</p>"; }
  };

  // 금액 입력칸 천 단위 콤마
  document.addEventListener("input", function (e) {
    var el = e.target;
    if (!el.matches || !el.matches("input[data-money]")) return;
    var raw = el.value.replace(/[^0-9]/g, "");
    var pos = el.value.length - el.selectionStart;
    el.value = raw ? Number(raw).toLocaleString("ko-KR") : "";
    try { var p = Math.max(0, el.value.length - pos); el.setSelectionRange(p, p); } catch (_) {}
  }, true);

  // 페이지 계산 함수 연결: 입력이 바뀔 때마다 다시 계산
  window.bindCalc = function (fn) {
    var form = document.querySelector("form.calc");
    if (!form) return;
    var run = function () { try { fn(); } catch (err) { U.set("result", U.note("입력값을 확인해 주세요.", "warn")); } };
    form.addEventListener("input", run);
    form.addEventListener("change", run);
    form.addEventListener("submit", function (e) { e.preventDefault(); run(); });
    run();
  };

  // 결과 복사 (공유용)
  document.addEventListener("click", function (e) {
    var b = e.target.closest && e.target.closest("[data-copy]");
    if (!b) return;
    var text = (document.getElementById("result") || {}).innerText || "";
    var done = function () { b.textContent = "복사됨 ✓"; setTimeout(function () { b.textContent = "결과 복사"; }, 1500); };
    if (navigator.clipboard) navigator.clipboard.writeText(text + "\n" + location.href).then(done, done); else done();
  });
})();
