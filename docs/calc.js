/* 급여계산소 — 계산 로직 (순수 함수, 브라우저·Node 공용) */
(function (root) {
  "use strict";

  // ---- 기준값 (출처는 각 페이지 하단에 표기) ----
  var MIN_WAGE = { 2026: 10320, 2027: 10700 };
  var INS = {
    2026: { np: 0.0475, hi: 0.03595, ltcRatio: 0.9448 / 7.19, ei: 0.009, npMin: 410000, npMax: 6590000 },
    // 2027: 국민연금 10%(연금개혁 단계 인상), 건강보험 7.19% 동결 확정. 장기요양·고용보험은 미확정 → 2026값 임시
    2027: { np: 0.05, hi: 0.03595, ltcRatio: 0.9448 / 7.19, ei: 0.009, npMin: 410000, npMax: 6590000 }
  };
  var UI_2026 = { rate: 0.6, upper: 68100, minWage: 10320, lowerRatio: 0.8 };
  var UI_DAYS = {
    under50: [120, 150, 180, 210, 240],
    over50: [120, 180, 210, 240, 270]
  };
  var WEEKS_PER_MONTH = 365 / 7 / 12; // 4.345...

  function floor10(x) { return Math.floor(x / 10) * 10; }
  function round(x) { return Math.round(x); }
  function num(x) { var n = Number(String(x == null ? "" : x).replace(/[^0-9.\-]/g, "")); return isFinite(n) ? n : 0; }

  // 1일 주휴시간 (주 15시간 미만이면 0)
  function juhyuHours(weeklyHours) {
    if (weeklyHours < 15) return 0;
    return Math.min(weeklyHours, 40) / 40 * 8;
  }

  // 주휴수당 (1주)
  function juhyu(hourly, weeklyHours) {
    var h = juhyuHours(weeklyHours);
    return { eligible: h > 0, hours: h, weekly: round(h * hourly), monthly: round(h * hourly * WEEKS_PER_MONTH) };
  }

  // 알바 월급 (주휴 포함, 월 환산)
  function albaMonthly(hourly, weeklyHours) {
    var jh = juhyuHours(weeklyHours);
    var weekPay = hourly * weeklyHours;
    var jPay = hourly * jh;
    var monthHours = Math.round((weeklyHours + jh) * WEEKS_PER_MONTH);
    return {
      weekBase: round(weekPay), weekJuhyu: round(jPay), weekTotal: round(weekPay + jPay),
      monthHours: monthHours, monthTotal: round(monthHours * hourly),
      juhyuHours: jh
    };
  }

  // 최저임금 점검: 월급 + 주 소정근로시간 → 환산 시급
  function minWageCheck(monthly, weeklyHours, year) {
    var jh = juhyuHours(weeklyHours);
    var monthHours = Math.round((weeklyHours + jh) * WEEKS_PER_MONTH);
    var hourlyEq = monthHours > 0 ? monthly / monthHours : 0;
    var mw = MIN_WAGE[year];
    return { monthHours: monthHours, hourly: Math.floor(hourlyEq), minWage: mw, ok: hourlyEq >= mw,
             shortfall: Math.max(0, round(mw * monthHours - monthly)), required: round(mw * monthHours) };
  }

  // 4대보험 근로자 부담분 (월)
  function insurance(monthly, year) {
    var r = INS[year] || INS[2026];
    var npBase = Math.min(Math.max(Math.floor(monthly / 1000) * 1000, r.npMin), r.npMax);
    var np = floor10(npBase * r.np);
    var hi = floor10(monthly * r.hi);
    var ltc = floor10(hi * r.ltcRatio);
    var ei = floor10(monthly * r.ei);
    var total = np + hi + ltc + ei;
    return { np: np, hi: hi, ltc: ltc, ei: ei, total: total, afterIns: monthly - total, npBase: npBase };
  }

  // 3.3% 원천징수
  function freelancer(gross) {
    var tax = floor10(gross * 0.03);
    var local = floor10(tax * 0.1);
    return { tax: tax, local: local, total: tax + local, net: gross - tax - local };
  }
  // 실수령액 → 계약금액 역산 (실수령액이 목표 이상이 되는 금액)
  function freelancerGross(net) {
    var g = Math.round(net / 0.967);
    while (freelancer(g).net < net) g++;
    return { gross: g, detail: freelancer(g) };
  }

  // 날짜 유틸 (YYYY-MM-DD → UTC Date)
  function d(s) { var p = String(s).split("-"); return new Date(Date.UTC(+p[0], +p[1] - 1, +p[2])); }
  function days(a, b) { return Math.round((b - a) / 86400000); }
  function addMonths(dt, m) {
    var y = dt.getUTCFullYear(), mo = dt.getUTCMonth() + m, day = dt.getUTCDate();
    var last = new Date(Date.UTC(y, mo + 1, 0)).getUTCDate();
    return new Date(Date.UTC(y, mo, Math.min(day, last)));
  }

  // 퇴직금: 입사일, 마지막 근무일, 최근 3개월 임금총액, 연간 상여금, 연차수당
  function severance(startStr, lastDayStr, wages3m, annualBonus, annualLeavePay) {
    var start = d(startStr);
    var retire = new Date(d(lastDayStr).getTime() + 86400000); // 퇴직일 = 마지막 근무일 다음 날
    var tenure = days(start, retire);
    var from = addMonths(retire, -3);
    var period = days(from, retire);
    var total3 = wages3m + annualBonus * 3 / 12 + annualLeavePay * 3 / 12;
    var avgDaily = period > 0 ? total3 / period : 0;
    var pay = avgDaily * 30 * tenure / 365;
    return { eligible: tenure >= 365, tenureDays: tenure, periodDays: period,
             avgDaily: Math.round(avgDaily * 100) / 100, severance: Math.floor(pay) };
  }

  // 실업급여 (2026년 이직자 기준)
  function unemployment(avgDailyWage, dailyHours, over50, insuredYears) {
    var c = UI_2026;
    var h = Math.min(Math.max(dailyHours, 1), 8);
    var lower = Math.floor(c.minWage * c.lowerRatio * h);
    var raw = Math.floor(avgDailyWage * c.rate);
    var daily = Math.min(Math.max(raw, lower), c.upper);
    if (lower > c.upper) daily = lower; // 하한이 상한보다 크면 하한 적용
    var idx = insuredYears < 1 ? 0 : insuredYears < 3 ? 1 : insuredYears < 5 ? 2 : insuredYears < 10 ? 3 : 4;
    var dDays = (over50 ? UI_DAYS.over50 : UI_DAYS.under50)[idx];
    return { daily: daily, raw: raw, lower: lower, upper: c.upper, days: dDays, total: daily * dDays,
             monthly30: daily * 30, applied: raw > c.upper ? "상한액" : raw < lower ? "하한액" : "평균임금 60%" };
  }

  // 연차 (5인 이상 사업장): 입사일, 기준일
  function annualLeave(startStr, refStr) {
    var start = d(startStr), ref = d(refStr);
    if (ref < start) return { years: 0, months: 0, days: 0, under1: true };
    var years = 0;
    while (addMonths(start, 12 * (years + 1)) <= ref) years++;
    if (years < 1) {
      var months = 0;
      while (addMonths(start, months + 1) <= ref) months++;
      return { years: 0, months: months, days: Math.min(months, 11), under1: true };
    }
    var dd = Math.min(15 + Math.floor((years - 1) / 2), 25);
    return { years: years, months: 0, days: dd, under1: false };
  }

  // ---- 근로소득세 (간이세액표) ----
  function ganyi() {
    if (typeof GANYI !== "undefined") return GANYI;
    if (typeof require !== "undefined") return require("./ganyi.js");
    throw new Error("간이세액표 데이터 없음");
  }
  // 2026.3.1 이후: 8세 이상 20세 이하 자녀 공제
  function childDeduction(c) {
    if (c <= 0) return 0;
    if (c === 1) return 20830;
    return 45830 + Math.max(0, c - 2) * 33330;
  }
  // 월 과세급여(원), 공제대상가족 수(본인 포함), 8~20세 자녀 수 → 월 소득세
  function incomeTax(monthlyTaxable, family, children) {
    var G = ganyi(), n = Math.max(1, Math.floor(family || 1)), k = monthlyTaxable / 1000, base;
    var col = function (row, m) {
      if (m <= 11) return row[1 + m] * 10;
      var a = row[12] * 10, b = row[11] * 10;
      return Math.max(0, a - (b - a) * (m - 11));
    };
    if (k < 770) base = 0;
    else if (k < 10000) {
      var R = G.rows, lo = 0, hi = R.length - 1;
      while (lo < hi) { var mid = (lo + hi + 1) >> 1; if (R[mid][0] <= k) lo = mid; else hi = mid - 1; }
      base = col(R[lo], n);
    } else {
      var t = G.t10000, top = n <= 11 ? t[n - 1] : Math.max(0, t[10] - (t[9] - t[10]) * (n - 11));
      var x = monthlyTaxable - 10000000;
      if (x <= 0) base = top;
      else if (k <= 14000) base = top + x * 0.98 * 0.35 + 25000;
      else if (k <= 28000) base = top + 1397000 + (monthlyTaxable - 14000000) * 0.98 * 0.38;
      else if (k <= 30000) base = top + 6610600 + (monthlyTaxable - 28000000) * 0.98 * 0.40;
      else if (k <= 45000) base = top + 7394600 + (monthlyTaxable - 30000000) * 0.40;
      else if (k <= 87000) base = top + 13394600 + (monthlyTaxable - 45000000) * 0.42;
      else base = top + 31034600 + (monthlyTaxable - 87000000) * 0.45;
      base = floor10(base);
    }
    var tax = Math.max(0, base - childDeduction(Math.max(0, Math.floor(children || 0))));
    return { tax: tax, local: floor10(tax * 0.1), base: base };
  }

  // 연봉 실수령액: 연봉(원), 월 비과세(원), 가족 수, 자녀 수, 보험 연도
  function netPay(annual, nontaxMonthly, family, children, year) {
    var gross = Math.floor(annual / 12);
    var nontax = Math.min(Math.max(nontaxMonthly || 0, 0), gross);
    var taxable = gross - nontax;
    var ins = insurance(taxable, year || 2026);
    var it = incomeTax(taxable, family, children);
    var ded = ins.total + it.tax + it.local;
    return { gross: gross, taxable: taxable, nontax: nontax, np: ins.np, hi: ins.hi, ltc: ins.ltc, ei: ins.ei,
             incomeTax: it.tax, localTax: it.local, deductions: ded, net: gross - ded, annualNet: (gross - ded) * 12,
             rate: gross ? ded / gross : 0 };
  }
  // 원하는 월 실수령액 → 필요한 연봉 (만원 단위 탐색)
  function annualForNet(targetNet, nontaxMonthly, family, children, year) {
    var lo = 0, hi = 2000000000;
    while (hi - lo > 10000) { var m = Math.floor((lo + hi) / 2 / 10000) * 10000;
      if (m === lo) break;
      if (netPay(m, nontaxMonthly, family, children, year).net >= targetNet) hi = m; else lo = m; }
    return hi;
  }

  // 사업주 인건비: 월 과세보수, 업종 산재요율, 상시근로자 150인 미만 여부
  function employerCost(monthly, year, accidentRate) {
    var r = INS[year] || INS[2026];
    var npBase = Math.min(Math.max(Math.floor(monthly / 1000) * 1000, r.npMin), r.npMax);
    var np = floor10(npBase * r.np);
    var hi = floor10(monthly * r.hi);
    var ltc = floor10(hi * r.ltcRatio);
    var ei = floor10(monthly * (r.ei + 0.0025)); // 고용안정·직업능력개발 0.25% (150인 미만)
    var ia = floor10(monthly * (accidentRate == null ? 0.0147 : accidentRate));
    var sev = Math.round(monthly / 12);
    var total = monthly + np + hi + ltc + ei + ia + sev;
    return { np: np, hi: hi, ltc: ltc, ei: ei, ia: ia, severance: sev, insTotal: np + hi + ltc + ei + ia, total: total };
  }

  // 연장·야간·휴일 가산수당 (5인 이상): 가산분과 1배분을 분리
  function overtimePay(hourly, ot, night, hol8, holOver) {
    var basePart = hourly * (ot + hol8 + holOver);            // 1배분 (연장·휴일 근로 자체의 임금)
    var prem = hourly * (ot * 0.5 + night * 0.5 + hol8 * 0.5 + holOver * 1.0);
    return { base: Math.round(basePart), premium: Math.round(prem), total: Math.round(basePart + prem),
             otP: Math.round(hourly * ot * 0.5), nightP: Math.round(hourly * night * 0.5),
             holP: Math.round(hourly * (hol8 * 0.5 + holOver)) };
  }

  // 일용근로소득 원천징수: (일급 − 15만) × 6% × (1 − 55%) , 1,000원 미만 소액부징수
  function dailyWorkerTax(dailyWage, days) {
    var per = Math.max(0, dailyWage - 150000) * 0.06 * 0.45;
    per = Math.floor(per);
    if (per < 1000) per = 0;
    per = floor10(per);
    var local = floor10(per * 0.1);
    var d = Math.max(1, Math.floor(days || 1));
    return { tax: per, local: local, perDayNet: dailyWage - per - local, totalTax: (per + local) * d, totalNet: (dailyWage - per - local) * d };
  }

  var api = { MIN_WAGE: MIN_WAGE, INS: INS, UI_2026: UI_2026, UI_DAYS: UI_DAYS, num: num,
    overtimePay: overtimePay, dailyWorkerTax: dailyWorkerTax,
    incomeTax: incomeTax, childDeduction: childDeduction, netPay: netPay, annualForNet: annualForNet, employerCost: employerCost,
    juhyuHours: juhyuHours, juhyu: juhyu, albaMonthly: albaMonthly, minWageCheck: minWageCheck,
    insurance: insurance, freelancer: freelancer, freelancerGross: freelancerGross,
    severance: severance, unemployment: unemployment, annualLeave: annualLeave };
  if (typeof module !== "undefined" && module.exports) module.exports = api; else root.Calc = api;
})(this);
