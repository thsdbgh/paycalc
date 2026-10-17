// 연봉별 페이지용 수치를 calc.js로 계산해 JSON으로 출력 (빌드 시 build.py가 읽음)
const C = require("../src/calc.js");
const NONTAX = 200000;
const amounts = [];
for (let a = 2000; a <= 10000; a += 100) amounts.push(a);
for (let a = 11000; a <= 15000; a += 1000) amounts.push(a);
const out = amounts.map((a) => {
  const won = a * 10000;
  const base = C.netPay(won, NONTAX, 1, 0, 2026);
  return {
    a, base,
    noNontax: C.netPay(won, 0, 1, 0, 2026).net,
    fam: {
      "1": base.net,
      "2": C.netPay(won, NONTAX, 2, 0, 2026).net,
      "3c1": C.netPay(won, NONTAX, 3, 1, 2026).net,
      "4c2": C.netPay(won, NONTAX, 4, 2, 2026).net,
    },
    y2027: C.netPay(won, NONTAX, 1, 0, 2027).net,
    hourly: Math.round(won / 12 / 209),
  };
});
process.stdout.write(JSON.stringify({ nontax: NONTAX, minWage: C.MIN_WAGE, rows: out }));
