// 엑셀 템플릿 예시(2026년 10월, 직원 3명)와 같은 결과가 나오는지 검증
const assert = require("assert");
const C = require("../src/calc.js");
function gen() {
  const S = { a: [], b: [], c: [] };
  for (let d = new Date(Date.UTC(2026, 8, 28)); d <= new Date(Date.UTC(2026, 9, 31)); d = new Date(d.getTime() + 864e5)) {
    const ds = d.toISOString().slice(0, 10), wd = (d.getUTCDay() + 6) % 7;
    if (wd <= 3) S.a.push({ date: ds, start: "10:00", end: "15:30", breakMin: 30 });
    if (wd <= 4 && ds !== "2026-10-09") {
      if (ds === "2026-10-14") S.b.push({ date: ds, absent: true });
      else if (ds === "2026-10-22") S.b.push({ date: ds, start: "09:00", end: "20:00", breakMin: 60 });
      else S.b.push({ date: ds, start: "09:00", end: "18:00", breakMin: 60 });
    }
    if (ds >= "2026-10-01" && wd >= 5) S.c.push(ds === "2026-10-17" ? { date: ds, start: "20:00", end: "02:00", breakMin: 0 } : { date: ds, start: "17:00", end: "23:00", breakMin: 0 });
  }
  return S;
}
const S = gen(); let n = 0;
const t = (name, fn) => { fn(); n++; console.log("ok -", name); };
const A = { hourly: 10500, weeklyHours: 20, deduction: "33" }, B = { hourly: 10320, weeklyHours: 40, deduction: "ins" }, Cc = { hourly: 11000, weeklyHours: 12, deduction: "none" };
t("주휴 판정 주: 2026-10 → 4주 (9/28~10/25)", () => assert.deepStrictEqual(C.payrollWeeks("2026-10").map(w => w.start), ["2026-09-28", "2026-10-05", "2026-10-12", "2026-10-19"]));
t("김하늘 (3.3%): 지급 1,060,500 / 실지급 1,025,510", () => { const r = C.monthlyPayroll(A, S.a, "2026-10", false);
  assert.strictEqual(r.gross, 1060500); assert.strictEqual(r.net, 1025510); assert.strictEqual(r.days, 17); });
t("이준호 (4대보험): 지급 1,919,520 / 결근 주 주휴 제외 / 4대보험 엑셀과 동일 + 간이세액", () => { const r = C.monthlyPayroll(B, S.b, "2026-10", false);
  const it = C.incomeTax(1919520, 1, 0);
  assert.strictEqual(r.gross, 1919520); assert.strictEqual(r.paidWeeks, 3); assert.strictEqual(r.ot, 2);
  assert.strictEqual(r.net, 1733040 - it.tax - it.local); });
t("박서연: 12시간 야간, 주휴 없음, 594,000", () => { const r = C.monthlyPayroll(Cc, S.c, "2026-10", false);
  assert.strictEqual(r.night, 12); assert.strictEqual(r.juhyu, 0); assert.strictEqual(r.gross, 594000); });
t("5인 이상: 연장 가산 10,320 / 야간 가산 66,000", () => {
  assert.strictEqual(C.monthlyPayroll(B, S.b, "2026-10", true).otPay, 10320);
  assert.strictEqual(C.monthlyPayroll(Cc, S.c, "2026-10", true).nightPay, 66000); });
t("11월로 넘어간 주(10/26~11/1)는 11월에 지급", () => assert.strictEqual(C.monthlyPayroll(A, S.a, "2026-11", false).juhyu, 42000));
console.log(`\n${n} payroll tests passed`);
