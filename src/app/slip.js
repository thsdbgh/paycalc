/* 임금명세서 렌더러 (사장님 앱·직원 보기 공용) */
(function () {
  "use strict";
  var esc = function (s) { return String(s == null ? "" : s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); };
  var won = function (n) { return Math.round(n).toLocaleString("ko-KR") + "원"; };
  var fmt = function (n) { return Number(n).toLocaleString("ko-KR", { maximumFractionDigits: 2 }); };
  // emp: employeeOut, biz: {name, ceo, size5, payday}, r: Calc.monthlyPayroll 결과
  window.renderSlip = function (emp, biz, ym, r) {
    var y = ym.slice(0, 4), m = +ym.slice(5, 7);
    var pd = new Date(Date.UTC(+y, m, Math.min(biz.payday || 10, 28)));
    var payday = pd.toISOString().slice(0, 10);
    var rows = [["기본급", r.base, fmt(r.hours) + "시간 × " + won(emp.hourly)],
      ["주휴수당", r.juhyu, r.juhyuHours ? fmt(r.juhyuHours) + "시간 × " + won(emp.hourly) + " × " + r.paidWeeks + "주" : "해당 없음 (주 15시간 미만)"]];
    if (biz.size5) rows.push(["연장근로 가산수당", r.otPay, fmt(r.ot) + "시간 × " + won(emp.hourly) + " × 0.5"],
                             ["야간근로 가산수당", r.nightPay, fmt(r.night) + "시간 × " + won(emp.hourly) + " × 0.5"]);
    if (r.extra) rows.push(["기타 수당", r.extra, ""]);
    if (r.nontax) rows.push(["식대 등 비과세", r.nontax, ""]);
    var tr3 = function (a) { return "<tr><td>" + a[0] + '</td><td class="n">' + won(a[1]) + "</td><td>" + esc(a[2]) + "</td></tr>"; };
    var tr2 = function (a) { return "<tr><td>" + a[0] + '</td><td class="n">' + won(a[1]) + "</td></tr>"; };
    return '<div class="slip"><h3>임금명세서</h3><p class="sub">' + y + "년 " + m + "월분</p>" +
      '<table class="t"><tr><th>성명</th><td>' + esc(emp.name) + "</td><th>생년월일</th><td>" + esc(emp.birth || "-") + "</td></tr>" +
      "<tr><th>사업장</th><td>" + esc(biz.name || "-") + "</td><th>지급일</th><td>" + payday + "</td></tr></table>" +
      '<table class="t"><tr><th>지급 항목</th><th>금액</th><th>계산 방법</th></tr>' + rows.map(tr3).join("") +
      '<tr class="sum"><td>지급 총액</td><td class="n">' + won(r.gross) + "</td><td></td></tr></table>" +
      '<table class="t"><tr><th>공제 항목</th><th>금액</th></tr>' +
      (r.deductions.length ? r.deductions.map(tr2).join("") : '<tr><td>공제 없음</td><td class="n">0원</td></tr>') +
      '<tr class="sum"><td>공제 총액</td><td class="n">' + won(r.deductionTotal) + "</td></tr></table>" +
      '<p class="pay">실 지급액 <b>' + won(r.net) + "</b></p>" +
      '<p class="hrs">근로일수 ' + r.days + "일 · 총 근로시간 " + fmt(r.hours) + "시간" + (biz.size5 ? " · 연장 " + fmt(r.ot) + "시간 · 야간 " + fmt(r.night) + "시간" : "") + "</p>" +
      '<p class="sign">' + esc(biz.name || "") + " 대표 " + esc(biz.ceo || "") + " (인)</p></div>";
  };
  window.slipEmp = function (e, extras) {
    return { hourly: e.hourly, weeklyHours: e.weeklyHours, deduction: e.deduction, family: e.family, kids: e.kids,
             extra: (extras && extras.extra) || 0, nontax: (extras && extras.nontax) || 0 };
  };
})();
