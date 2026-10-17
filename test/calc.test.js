const assert = require("assert");
const C = require("../src/calc.js");
let n = 0;
function t(name, fn) { fn(); n++; console.log("ok -", name); }

t("주휴: 40h × 10,320 = 82,560/주", () => assert.strictEqual(C.juhyu(10320, 40).weekly, 82560));
t("주휴: 20h → 4시간", () => assert.strictEqual(C.juhyu(10500, 20).weekly, 42000));
t("주휴: 14.9h 비대상", () => assert.strictEqual(C.juhyu(10320, 14.9).eligible, false));
t("주휴: 50h도 최대 8시간", () => assert.strictEqual(C.juhyu(10000, 50).hours, 8));
t("월급: 40h 2026 = 209h, 2,156,880", () => {
  const r = C.albaMonthly(10320, 40); assert.strictEqual(r.monthHours, 209); assert.strictEqual(r.monthTotal, 2156880);
});
t("월급: 40h 2027 = 2,236,300", () => assert.strictEqual(C.albaMonthly(10700, 40).monthTotal, 2236300));
t("최저임금: 220만원/40h 2027 미달", () => {
  const r = C.minWageCheck(2200000, 40, 2027); assert.strictEqual(r.ok, false); assert.strictEqual(r.shortfall, 36300);
});
t("최저임금: 2,156,880/40h 2026 정상", () => assert.strictEqual(C.minWageCheck(2156880, 40, 2026).ok, true));
t("3.3%: 100만원 → 967,000", () => assert.strictEqual(C.freelancer(1000000).net, 967000));
t("3.3% 역산: 967,000 → 1,000,000", () => assert.strictEqual(C.freelancerGross(967000).gross, 1000000));
t("4대보험: 1,919,520 (엑셀과 동일)", () => {
  const r = C.insurance(1919520, 2026);
  assert.deepStrictEqual([r.np, r.hi, r.ltc, r.ei], [91150, 69000, 9060, 17270]);
});
t("4대보험: 국민연금 상한 659만", () => assert.strictEqual(C.insurance(10000000, 2026).np, floor10(6590000 * 0.0475)));
function floor10(x) { return Math.floor(x / 10) * 10; }
t("퇴직금: 1년 미만 비대상", () => assert.strictEqual(C.severance("2026-01-01", "2026-12-30", 9000000, 0, 0).eligible, false));
t("퇴직금: 정확히 1년 대상", () => assert.strictEqual(C.severance("2025-01-01", "2025-12-31", 9000000, 0, 0).eligible, true));
t("퇴직금: 월 300만 × 2년 ≈ 600만 전후", () => {
  // 2024-01-01 입사, 2025-12-31 마지막 근무 → 재직 731일, 최근 3개월(10/1~12/31) 92일
  const r = C.severance("2024-01-01", "2025-12-31", 9000000, 0, 0);
  assert.strictEqual(r.tenureDays, 731); assert.strictEqual(r.periodDays, 92);
  assert.strictEqual(r.severance, Math.floor(9000000 / 92 * 30 * 731 / 365));
});
t("실업급여: 하한 66,048 (8h)", () => assert.strictEqual(C.unemployment(80000, 8, false, 2).daily, 66048));
t("실업급여: 상한 68,100", () => assert.strictEqual(C.unemployment(200000, 8, false, 2).daily, 68100));
t("실업급여: 50세 이상 10년 → 270일", () => assert.strictEqual(C.unemployment(100000, 8, true, 12).days, 270));
t("실업급여: 4h 근무 하한 33,024", () => assert.strictEqual(C.unemployment(40000, 4, false, 0.5).lower, 33024));
t("연차: 6개월 → 6일", () => assert.strictEqual(C.annualLeave("2026-01-15", "2026-07-15").days, 6));
t("연차: 1년 → 15일", () => assert.strictEqual(C.annualLeave("2025-03-01", "2026-03-01").days, 15));
t("연차: 3년 → 16일", () => assert.strictEqual(C.annualLeave("2023-03-01", "2026-03-01").days, 16));
t("연차: 21년 → 25일 상한", () => assert.strictEqual(C.annualLeave("2005-01-01", "2026-06-01").days, 25));
t("연차: 11개월 → 11일 상한", () => assert.strictEqual(C.annualLeave("2025-04-01", "2026-03-31").days, 11));

// ---- 간이세액표 (공식 값 대조) ----
const IT = (m, n, c) => C.incomeTax(m, n, c).tax;
t("간이세액: 300만 1인 74,350", () => assert.strictEqual(IT(3000000, 1), 74350));
t("간이세액: 350만 가족 1~6 (국세청 예시 행)", () =>
  assert.deepStrictEqual([1,2,3,4,5,6].map(n => IT(3510000, n)), [127220,102220,62460,49340,37630,32380]));
t("간이세액: 350만 4인·자녀 2명 = 3,510 (2026.3 개정 예시)", () => assert.strictEqual(IT(3500000, 4, 2), 3510));
t("간이세액: 106만 미만 0원, 106만 1,040원", () => { assert.strictEqual(IT(1059000, 1), 0); assert.strictEqual(IT(1060000, 1), 1040); });
t("간이세액: 1,000만 1인 1,507,400", () => assert.strictEqual(IT(10000000, 1), 1507400));
t("간이세액: 1,000만 초과 연속성", () => { const a = IT(9999000, 1), b = IT(10000000, 1), c = IT(10010000, 1);
  assert.ok(a <= b && b < c && c - b < 30000); });
t("간이세액: 1,400만 경계 연속", () => { const a = IT(14000000, 1), b = IT(14000010, 1); assert.ok(Math.abs(b - a) < 100); });
t("자녀공제: 1명 20,830 / 3명 79,160", () => { assert.strictEqual(C.childDeduction(1), 20830); assert.strictEqual(C.childDeduction(3), 79160); });
t("자녀공제는 0 아래로 내려가지 않음", () => assert.strictEqual(IT(2000000, 1, 3), 0));
t("가족 12명: 11명 기준 외삽", () => assert.ok(IT(9000000, 12) <= IT(9000000, 11)));
t("실수령: 연봉 4,000만 (식대 20만, 1인) 구성 합 일치", () => {
  const r = C.netPay(40000000, 200000, 1, 0, 2026);
  assert.strictEqual(r.gross, 3333333); assert.strictEqual(r.taxable, 3133333);
  assert.strictEqual(r.net, r.gross - r.np - r.hi - r.ltc - r.ei - r.incomeTax - r.localTax);
  assert.strictEqual(r.incomeTax, IT(3133333, 1));
});
t("역산: 월 300만 실수령 → 연봉 탐색값의 실수령 ≥ 300만", () => {
  const a = C.annualForNet(3000000, 200000, 1, 0, 2026);
  assert.ok(C.netPay(a, 200000, 1, 0, 2026).net >= 3000000);
  assert.ok(C.netPay(a - 10000, 200000, 1, 0, 2026).net < 3000000);
});
t("인건비: 월 250만 사업주 총비용 > 급여", () => { const e = C.employerCost(2500000, 2026); assert.ok(e.total > 2500000 && e.severance === 208333); });
t("가산수당: 시급 1만, 연장 2h → 30,000 (1.5배)", () => assert.strictEqual(C.overtimePay(10000, 2, 0, 0, 0).total, 30000));
t("가산수당: 휴일 10h → 8h×1.5 + 2h×2 = 160,000", () => assert.strictEqual(C.overtimePay(10000, 0, 0, 8, 2).total, 160000));
t("가산수당: 야간 4h 가산분만 20,000", () => assert.strictEqual(C.overtimePay(10000, 0, 4, 0, 0).total, 20000));
t("일용직: 일급 20만 → 소득세 1,350", () => assert.strictEqual(C.dailyWorkerTax(200000).tax, 1350));
t("일용직: 일급 187,000 → 999원 소액부징수 0", () => assert.strictEqual(C.dailyWorkerTax(187000).tax, 0));
t("일용직: 15만 이하 0원", () => assert.strictEqual(C.dailyWorkerTax(150000).tax, 0));
t("퇴직소득세: 20년 2억 → 7,025,000 + 지방 702,500", () => { const r = C.retirementTax(200000000, 20);
  assert.strictEqual(r.tax, 7025000); assert.strictEqual(r.local, 702500); assert.strictEqual(r.serviceDeduction, 40000000); });
t("퇴직소득세: 근속공제가 더 크면 0원", () => assert.strictEqual(C.retirementTax(3000000, 5).tax, 0));
t("근속연수: 2년 8개월 → 3년 (끝수 올림)", () => assert.strictEqual(C.tenureYears("2024-03-01", "2026-10-31"), 3));
t("근속연수: 정확히 2년 → 2년", () => assert.strictEqual(C.tenureYears("2024-11-01", "2026-10-31"), 2));
t("육아휴직: 일반 12개월 상한 → 2,310만", () => assert.strictEqual(C.parentalLeave(5000000, 12, "normal").total, 23100000));
t("육아휴직: 6+6 6개월 통상 500만 → 2,000만", () => assert.strictEqual(C.parentalLeave(5000000, 6, "both").total, 20000000));
t("육아휴직: 하한 70만", () => assert.strictEqual(C.parentalLeave(500000, 1, "normal").rows[0].amount, 700000));
t("육아휴직: 7개월차 80%", () => assert.strictEqual(C.parentalLeave(1500000, 7, "normal").rows[6].amount, 1200000));
t("육아휴직: 한부모 1개월 300만", () => assert.strictEqual(C.parentalLeave(4000000, 1, "single").rows[0].amount, 3000000));
t("대출: 1억 5% 30년 원리금균등 월 536,822", () => assert.strictEqual(C.loanSchedule(100000000, 5, 360, "ann").first, 536822));
t("대출: 원금균등 첫 달 = 원금/n + 이자", () => assert.strictEqual(C.loanSchedule(12000000, 6, 12, "prin").first, 1060000));
t("대출: 만기일시 총이자 = 원금×연이율", () => assert.strictEqual(C.loanSchedule(10000000, 6, 12, "bullet").totalInterest, 600000));
t("대출: 잔액 0으로 끝남", () => assert.strictEqual(C.loanSchedule(100000000, 4.2, 120, "ann").rows[119].balance, 0));
console.log(`\n${n} tests passed`);
