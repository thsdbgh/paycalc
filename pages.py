# 급여계산소 — 페이지 콘텐츠 정의
MOEL_MW = ("2027년 적용 최저임금 고시 (고용노동부, 2026.8.5)", "https://www.minimumwage.go.kr/")
LAW = lambda name: (f"{name} (국가법령정보센터)", "https://www.law.go.kr/")

RADIO = "(document.querySelector('input[name=\"%s\"]:checked')||{}).value"

PAGES = [
# ------------------------------------------------------------------ 주휴수당
dict(
slug="juhyu", short="주휴수당 계산기", tag="주 15시간 이상이면 받는 유급 휴일 수당",
title="주휴수당 계산기 2026·2027 — 시급·근무시간만 넣으면 바로 계산",
desc="시급과 주 근무시간만 입력하면 주휴수당 지급 대상 여부, 1주·월 주휴수당을 바로 계산합니다. 2027년 최저임금 10,700원 반영.",
h1="주휴수당 계산기",
lead="시급과 1주 소정근로시간을 넣으면 주휴수당 대상 여부와 금액이 바로 나옵니다.",
fields=[
 dict(id="hourly", type="money", label="시급", hint="원", value="10,320", pair=True),
 dict(id="hours", type="number", label="1주 소정근로시간", hint="시간", value="20", step="0.5"),
],
js="""
var h=U.val('hourly'),w=U.val('hours'),r=Calc.juhyu(h,w);
if(!h||!w){U.set('result',U.note('시급과 근무시간을 입력하세요.'));return;}
if(!r.eligible){U.set('result','<p class="big">0원</p>'+U.note('1주 소정근로시간이 15시간 미만이라 주휴수당 지급 대상이 아닙니다.','warn'));return;}
U.set('result','<p class="big">'+U.won(r.weekly)+'<small>/ 1주</small></p>'+
 U.row('1일 주휴시간',U.fmt(r.hours,2)+'시간')+U.row('계산식',U.fmt(r.hours,2)+'시간 × '+U.won(h))+
 U.row('한 달 환산 (× 4.345주)',U.won(r.monthly),true)+
 U.note('그 주의 소정근로일을 모두 출근(개근)해야 받을 수 있습니다.'));
""",
article="""
<h2>주휴수당이란?</h2>
<p>주휴수당은 1주 동안 정해진 근무일을 모두 출근한 근로자에게 주는 <b>유급 휴일 1일분의 임금</b>입니다(근로기준법 제55조, 시행령 제30조).
정규직뿐 아니라 아르바이트·단시간 근로자도 조건을 채우면 받을 수 있고, 5인 미만 사업장에도 똑같이 적용됩니다.</p>
<h2>받을 수 있는 조건 2가지</h2>
<ol><li><b>1주 소정근로시간 15시간 이상</b> — 근로계약서에 정한 근무시간 기준입니다. 4주 평균이 15시간 이상이어야 합니다.</li>
<li><b>그 주의 소정근로일 개근</b> — 결근이 있으면 그 주 주휴수당은 발생하지 않습니다. 지각·조퇴는 결근이 아니어서 주휴수당에 영향이 없습니다.</li></ol>
<h2>계산 방법</h2>
<p class="formula">주휴수당 = (1주 소정근로시간 ÷ 40 × 8) × 시급</p>
<p>1주 40시간 이상 일해도 1일 주휴시간은 최대 8시간입니다. 예를 들어 시급 10,320원으로 주 20시간 일하면 20 ÷ 40 × 8 = 4시간, 주휴수당은 41,280원입니다.</p>
<table class="t"><tr><th>주 근무시간</th><th>1일 주휴시간</th><th>2026 (10,320원)</th><th>2027 (10,700원)</th></tr>
<tr><td>15시간</td><td>3시간</td><td>30,960원</td><td>32,100원</td></tr>
<tr><td>20시간</td><td>4시간</td><td>41,280원</td><td>42,800원</td></tr>
<tr><td>30시간</td><td>6시간</td><td>61,920원</td><td>64,200원</td></tr>
<tr><td>40시간</td><td>8시간</td><td>82,560원</td><td>85,600원</td></tr></table>
<h2>못 받았다면?</h2>
<p>주휴수당 미지급은 임금체불에 해당합니다. 임금채권 소멸시효는 3년이므로 지난 기간도 청구할 수 있습니다. 사업주와 먼저 이야기해 보고, 해결되지 않으면 고용노동부 고객상담센터(☎1350)나 노동포털에서 진정할 수 있습니다.</p>
""",
faq=[
 ("주 15시간 미만이면 주휴수당이 없나요?", "네. 1주 소정근로시간이 15시간 미만인 초단시간 근로자에게는 주휴일과 주휴수당 규정이 적용되지 않습니다."),
 ("5인 미만 사업장도 주휴수당을 줘야 하나요?", "네. 주휴수당은 사업장 규모와 관계없이 1인 이상 모든 사업장에 적용됩니다."),
 ("월급제 직원도 주휴수당을 따로 받나요?", "월 209시간을 기준으로 정한 월급에는 주휴수당이 이미 들어 있으므로 따로 더 주지 않습니다. 시급제일 때 별도로 계산합니다."),
 ("지각이나 조퇴를 하면 주휴수당이 깎이나요?", "지각·조퇴는 결근이 아니므로 주휴수당 발생에 영향이 없습니다. 다만 빠진 시간만큼 임금은 공제될 수 있습니다."),
],
sources=[LAW("근로기준법 제55조, 시행령 제30조"), MOEL_MW],
related=["alba", "minwage", "insurance"], promo=True,
),
# ------------------------------------------------------------------ 알바 월급
dict(
slug="alba", short="알바 월급 계산기", tag="시급 → 주급·월급 (주휴 포함)",
title="알바 월급 계산기 — 시급으로 주급·월급·실수령액 계산 (주휴수당 포함)",
desc="시급과 주 근무시간으로 주휴수당을 포함한 주급·월급을 계산하고, 3.3% 또는 4대보험 공제 후 실수령액까지 확인하세요.",
h1="알바 월급 계산기",
lead="시급과 1주 근무시간을 넣으면 주휴수당을 포함한 월급과 공제 후 실수령액을 계산합니다.",
fields=[
 dict(id="hourly", type="money", label="시급", hint="원", value="10,320", pair=True),
 dict(id="hours", type="number", label="1주 근무시간", hint="시간", value="25", step="0.5"),
 dict(id="ded", type="seg", label="공제 방식", value="none", options=[("none", "공제 없음"), ("33", "3.3%"), ("ins", "4대보험")]),
],
js="""
var h=U.val('hourly'),w=U.val('hours'),d=%s,r=Calc.albaMonthly(h,w);
if(!h||!w){U.set('result',U.note('시급과 근무시간을 입력하세요.'));return;}
var net=r.monthTotal,dn='';
if(d==='33'){var f=Calc.freelancer(r.monthTotal);net=f.net;dn=U.row('3.3%% 공제','−'+U.won(f.total));}
if(d==='ins'){var i=Calc.insurance(r.monthTotal,2026);net=i.afterIns;dn=U.row('4대보험 공제 (2026)','−'+U.won(i.total));}
U.set('result','<p class="big">'+U.won(net)+'<small>월 실수령 (세전 '+U.won(r.monthTotal)+')</small></p>'+
 U.row('주급 (근무분)',U.won(r.weekBase))+U.row('주휴수당 / 주',r.juhyuHours?U.won(r.weekJuhyu):'대상 아님 (주 15시간 미만)')+
 U.row('주급 합계',U.won(r.weekTotal),true)+U.row('월 환산 시간',r.monthHours+'시간')+dn+
 U.note('월 환산 = (주 근무시간 + 주휴시간) × 365 ÷ 7 ÷ 12'));
""" % (RADIO % "ded"),
article="""
<h2>알바 월급은 이렇게 계산합니다</h2>
<p class="formula">월급 = (1주 근무시간 + 1일 주휴시간) × 4.345주 × 시급</p>
<p>한 달은 평균 4.345주(365일 ÷ 7 ÷ 12)입니다. 주 40시간 근무자는 (40 + 8) × 4.345 ≈ <b>209시간</b>으로, 최저임금 월급(2026년 2,156,880원, 2027년 2,236,300원)이 여기서 나옵니다.</p>
<h2>근무시간별 월급 (최저임금 기준)</h2>
<table class="t"><tr><th>주 근무시간</th><th>월 환산시간</th><th>2026 (10,320원)</th><th>2027 (10,700원)</th></tr>
<tr><td>15시간</td><td>78시간</td><td>804,960원</td><td>834,600원</td></tr>
<tr><td>20시간</td><td>104시간</td><td>1,073,280원</td><td>1,112,800원</td></tr>
<tr><td>30시간</td><td>156시간</td><td>1,609,920원</td><td>1,669,200원</td></tr>
<tr><td>40시간</td><td>209시간</td><td>2,156,880원</td><td>2,236,300원</td></tr></table>
<h2>3.3%와 4대보험, 무엇이 맞나요?</h2>
<p>사장님의 지시를 받으며 정해진 시간에 일하는 아르바이트는 원칙적으로 <b>근로자</b>이므로 근로소득으로 신고하고, 월 60시간(주 약 14시간) 이상이면 4대보험 가입 대상입니다.
3.3% 원천징수는 원래 독립적으로 일하는 프리랜서(사업소득자)에게 쓰는 방식입니다. 3.3%로 처리되고 있다면 퇴직금·실업급여 수급에 불리할 수 있으니 확인해 보세요.</p>
<h2>실제 받는 금액이 다른 이유</h2>
<ul><li>결근한 주는 주휴수당이 빠집니다.</li><li>5인 이상 사업장에서 야간(22~06시)·연장(1일 8시간 초과) 근무를 하면 50%가 더 붙습니다.</li>
<li>4대보험 금액은 회사 신고 기준 보수에 따라 조금 달라질 수 있습니다.</li></ul>
""",
faq=[
 ("주 40시간이면 왜 209시간인가요?", "주휴시간 8시간을 더한 48시간에 한 달 평균 주수 4.345를 곱하면 208.6시간이고, 이를 올림해 209시간을 씁니다."),
 ("알바도 4대보험에 가입해야 하나요?", "월 소정근로시간이 60시간 이상이면 원칙적으로 국민연금·건강보험·고용보험 가입 대상입니다. 산재보험은 근무시간과 관계없이 적용됩니다."),
 ("야간 수당은 알바도 받나요?", "상시 근로자 5인 이상 사업장이라면 오후 10시~오전 6시 근무에 대해 시급의 50%를 추가로 받습니다. 5인 미만 사업장은 의무가 아닙니다."),
],
sources=[LAW("근로기준법 제55조·제56조"), MOEL_MW],
related=["juhyu", "insurance", "freelancer"], promo=True,
),
# ------------------------------------------------------------------ 최저임금
dict(
slug="minwage", short="최저임금 계산기", tag="내 월급, 최저임금 위반일까?",
title="최저임금 계산기 2027 — 월급이 최저임금에 미달하는지 확인",
desc="월급과 주 근무시간을 넣으면 시급으로 환산해 2026년(10,320원)·2027년(10,700원) 최저임금 위반 여부와 부족한 금액을 알려 드립니다.",
h1="최저임금 계산기 (위반 확인)",
lead="세전 월급과 1주 소정근로시간을 넣으면 시급으로 환산해 최저임금 미달 여부를 확인합니다.",
fields=[
 dict(id="year", type="seg", label="기준 연도", value="2027", options=[("2026", "2026년 (10,320원)"), ("2027", "2027년 (10,700원)")]),
 dict(id="monthly", type="money", label="세전 월급", hint="최저임금에 들어가는 임금 기준", value="2,200,000", pair=True),
 dict(id="hours", type="number", label="1주 소정근로시간", hint="시간", value="40", step="0.5"),
],
js="""
var y=+%s,m=U.val('monthly'),w=U.val('hours'),r=Calc.minWageCheck(m,w,y);
if(!m||!w){U.set('result',U.note('월급과 근무시간을 입력하세요.'));return;}
U.set('result','<p class="big">시급 '+U.won(r.hourly)+'</p>'+
 (r.ok?U.note(y+'년 최저임금('+U.won(r.minWage)+') 이상입니다.','good'):U.note(y+'년 최저임금('+U.won(r.minWage)+')보다 낮습니다. 월 '+U.won(r.shortfall)+' 부족','warn'))+
 U.row('월 소정근로시간 (주휴 포함)',r.monthHours+'시간')+U.row(y+'년 최저 월급',U.won(r.required),true));
""" % (RADIO % "year"),
article="""
<h2>2026·2027 최저임금</h2>
<table class="t"><tr><th>구분</th><th>2026년</th><th>2027년</th></tr>
<tr><td>시급</td><td>10,320원</td><td>10,700원 (+3.7%)</td></tr>
<tr><td>일급 (8시간)</td><td>82,560원</td><td>85,600원</td></tr>
<tr><td>월급 (209시간)</td><td>2,156,880원</td><td>2,236,300원</td></tr></table>
<p>2027년 최저임금은 2026년 8월 5일 고용노동부가 확정 고시했고, 2027년 1월 1일 근무분부터 업종 구분 없이 모든 사업장에 적용됩니다.</p>
<h2>환산 방법</h2>
<p class="formula">환산 시급 = 월급 ÷ {(1주 소정근로시간 + 주휴시간) × 4.345}</p>
<p>최저임금 위반을 따질 때는 매달 정기적으로 주는 기본급·고정수당을 포함합니다. 2024년부터 정기상여금과 복리후생비(식대 등)는 전액 최저임금 계산에 들어갑니다. 연장·야간·휴일 수당은 빠집니다.</p>
<h2>2026년에 220만 원을 받는다면?</h2>
<p>주 40시간 근무자가 월 220만 원을 받으면 2026년에는 문제가 없지만, 2027년 1월부터는 최저 월급 2,236,300원보다 36,300원 적어 위반이 됩니다. 연말에 근로계약을 다시 확인하세요.</p>
<h2>수습 기간 감액</h2>
<p>1년 이상 계약을 맺은 근로자는 수습 3개월 동안 최저임금의 90%(2027년 9,630원)까지 줄 수 있습니다. 단, 단순노무 업무는 감액할 수 없습니다.</p>
""",
faq=[
 ("최저임금을 안 지키면 어떻게 되나요?", "최저임금법 위반으로 3년 이하의 징역 또는 2천만 원 이하의 벌금 대상이며, 근로자는 차액을 청구할 수 있습니다."),
 ("식대도 최저임금에 포함되나요?", "2024년부터 매달 정기적으로 지급하는 현금성 복리후생비(식대·교통비 등)는 전액 최저임금 산입범위에 포함됩니다."),
 ("2027년 최저임금은 언제부터 적용되나요?", "2027년 1월 1일 근무분부터입니다. 2026년 12월 근무분 임금을 1월에 받더라도 2026년 기준이 적용됩니다."),
],
sources=[MOEL_MW, LAW("최저임금법 제6조")],
related=["alba", "juhyu", "insurance"], promo=False,
),
# ------------------------------------------------------------------ 퇴직금
dict(
slug="severance", short="퇴직금 계산기", tag="1년 이상 일했다면 꼭 확인",
title="퇴직금 계산기 2026 — 퇴직소득세 뺀 세후 퇴직금까지 계산",
desc="입사일, 마지막 근무일, 최근 3개월 급여를 넣으면 평균임금과 예상 퇴직금을 계산합니다. 상여금·연차수당 반영, 아르바이트도 가능.",
h1="퇴직금 계산기",
lead="입사일과 마지막 근무일, 퇴사 전 3개월 동안 받은 세전 급여를 넣어 주세요.",
fields=[
 dict(id="start", type="date", label="입사일", value="2024-03-01", pair=True),
 dict(id="last", type="date", label="마지막 근무일", value="2026-10-31"),
 dict(id="w3", type="money", label="최근 3개월 세전 급여 합계", hint="원", value="7,500,000"),
 dict(id="bonus", type="money", label="최근 1년 상여금", hint="없으면 0", value="0", pair=True),
 dict(id="leave", type="money", label="최근 1년 연차수당", hint="없으면 0", value="0"),
],
js="""
var s=U.str('start'),l=U.str('last');if(!s||!l){U.set('result',U.note('날짜를 입력하세요.'));return;}
var r=Calc.severance(s,l,U.val('w3'),U.val('bonus'),U.val('leave'));
if(r.tenureDays<=0){U.set('result',U.note('마지막 근무일이 입사일보다 늦어야 합니다.','warn'));return;}
U.set('result','<p class="big">'+U.won(r.severance)+'<small>예상 퇴직금 (세전)</small></p>'+
 (r.eligible?'':U.note('재직기간이 1년 미만이라 법정 퇴직금 지급 대상이 아닙니다.','warn'))+
 U.row('재직일수',U.fmt(r.tenureDays,0)+'일')+U.row('평균임금 산정기간',r.periodDays+'일')+
 U.row('1일 평균임금',U.won(r.avgDaily))+U.row('계산식','1일 평균임금 × 30 × 재직일수 ÷ 365')+
 (r.eligible?(function(){var y=Calc.tenureYears(s,l),t=Calc.retirementTax(r.severance,y);
  return U.row('근속연수 (1년 미만 올림)',y+'년')+U.row('퇴직소득세','−'+U.won(t.tax))+U.row('지방소득세','−'+U.won(t.local))+
  U.row('세후 퇴직금 (일시금 수령 시)',U.won(t.net),true)})():'')+
 U.note('IRP 계좌로 받아 연금으로 나눠 받으면 퇴직소득세를 30~40% 줄일 수 있습니다.'));
""",
article="""
<h2>퇴직금 받는 조건</h2>
<ul><li>같은 사업장에서 <b>1년 이상</b> 계속 근무</li><li>4주 평균 <b>1주 15시간 이상</b> 근무</li></ul>
<p>정규직·계약직·아르바이트 모두 해당하며 5인 미만 사업장도 지급 의무가 있습니다(근로자퇴직급여 보장법 제4조).</p>
<h2>계산 방법</h2>
<p class="formula">퇴직금 = 1일 평균임금 × 30일 × (재직일수 ÷ 365)</p>
<p class="formula">1일 평균임금 = (퇴직 전 3개월 임금 총액 + 연간 상여금 × 3/12 + 연차수당 × 3/12) ÷ 퇴직 전 3개월 일수</p>
<p>퇴직일은 <b>마지막 근무일의 다음 날</b>입니다. 예를 들어 10월 31일까지 일했다면 퇴직일은 11월 1일이고, 평균임금 산정기간은 8월 1일~10월 31일(92일)입니다.</p>
<h2>예시</h2>
<p>2024년 3월 1일 입사, 2026년 10월 31일 퇴사, 최근 3개월 급여 합계 750만 원이라면 1일 평균임금은 약 81,522원, 재직일수 975일로 예상 퇴직금은 약 653만 원입니다.</p>
<h2>퇴직소득세는 이렇게 계산합니다</h2>
<ol><li><b>근속연수공제</b>: 5년 이하 연 100만 원, 6~10년 500만 원 + 5년 초과 1년당 200만 원, 11~20년 1,500만 원 + 10년 초과 1년당 250만 원, 20년 초과 4,000만 원 + 1년당 300만 원</li>
<li><b>환산급여</b> = (퇴직금 − 근속연수공제) × 12 ÷ 근속연수</li>
<li><b>환산급여공제</b>: 800만 원 이하 전액, 7,000만 원까지 800만 원 + 초과분 60%, 1억 원까지 4,520만 원 + 55%, 3억 원까지 6,170만 원 + 45%, 그 이상 1억 5,170만 원 + 35%</li>
<li><b>세액</b> = (환산급여 − 환산급여공제)에 기본세율을 적용한 금액 ÷ 12 × 근속연수. 지방소득세는 그 10%입니다.</li></ol>
<p>근속연수는 1년 미만 끝수를 1년으로 올립니다. 예를 들어 근속 20년, 퇴직금 2억 원이면 퇴직소득세는 약 702만 원, 지방소득세를 합치면 약 773만 원입니다.</p>
<h2>주의할 점</h2>
<ul><li>평균임금이 통상임금보다 낮으면 통상임금으로 계산합니다.</li><li>퇴직 후 <b>14일 이내</b>에 지급해야 하며, 늦으면 연 20%의 지연이자가 붙습니다.</li>
<li>육아휴직·산재 휴업 기간 등은 평균임금 산정기간에서 빠지므로 실제 금액이 달라질 수 있습니다.</li></ul>
""",
faq=[
 ("아르바이트도 퇴직금을 받을 수 있나요?", "네. 1년 이상, 4주 평균 주 15시간 이상 일했다면 아르바이트도 퇴직금을 받습니다."),
 ("정확히 1년만 일해도 받나요?", "계속근로기간이 1년(365일) 이상이면 대상입니다. 예를 들어 1월 1일 입사 후 12월 31일까지 일하면 1년을 채운 것으로 봅니다."),
 ("퇴직금은 언제까지 줘야 하나요?", "퇴직일로부터 14일 이내에 지급해야 합니다. 당사자 합의로 기일을 연장할 수 있습니다."),
 ("상여금도 퇴직금 계산에 들어가나요?", "네. 퇴직 전 1년간 받은 상여금의 3/12을 3개월 임금 총액에 더해 평균임금을 계산합니다."),
],
sources=[LAW("근로자퇴직급여 보장법 제8조"), LAW("근로기준법 제2조(평균임금)")],
related=["unemployment", "leave", "insurance"], promo=False,
),
# ------------------------------------------------------------------ 실업급여
dict(
slug="unemployment", short="실업급여 계산기", tag="하루 얼마, 며칠 받을까?",
title="실업급여 계산기 2026 — 구직급여 1일 금액·지급일수·총액 계산",
desc="퇴사 전 3개월 급여, 나이, 고용보험 가입기간으로 2026년 실업급여(구직급여) 1일 금액(상한 68,100원)과 받을 수 있는 일수, 총액을 계산합니다.",
h1="실업급여 계산기",
lead="2026년 이직자 기준입니다. 퇴사 전 3개월 세전 급여와 고용보험 가입기간을 넣어 주세요.",
fields=[
 dict(id="w3", type="money", label="퇴사 전 3개월 세전 급여 합계", hint="원", value="7,500,000", pair=True),
 dict(id="days3", type="number", label="그 3개월의 총 일수", hint="보통 89~92일", value="92", step="1"),
 dict(id="dh", type="number", label="1일 소정근로시간", hint="시간 (최대 8)", value="8", step="0.5", pair=True),
 dict(id="years", type="number", label="고용보험 가입기간", hint="년", value="3", step="0.5"),
 dict(id="age", type="seg", label="퇴사일 기준 나이", value="u", options=[("u", "50세 미만"), ("o", "50세 이상·장애인")]),
],
js="""
var w=U.val('w3'),n=U.val('days3');if(!w||!n){U.set('result',U.note('급여와 일수를 입력하세요.'));return;}
var avg=w/n,r=Calc.unemployment(avg,U.val('dh')||8,%s==='o',U.val('years'));
U.set('result','<p class="big">'+U.won(r.total)+'<small>총 예상 수령액</small></p>'+
 U.row('1일 구직급여',U.won(r.daily)+' ('+r.applied+')',true)+U.row('지급일수',r.days+'일')+U.row('한 달(30일) 기준',U.won(r.monthly30))+
 U.row('1일 평균임금',U.won(avg))+U.row('2026 상한 / 하한',U.won(r.upper)+' / '+U.won(r.lower))+
 U.note('고용보험 가입(피보험단위기간) 180일 이상, 비자발적 퇴사 등 수급 요건을 채워야 합니다.'));
""" % (RADIO % "age"),
article="""
<h2>2026년 실업급여 핵심 숫자</h2>
<table class="t"><tr><th>구분</th><th>금액</th></tr>
<tr><td>1일 상한액</td><td>68,100원 (2026.1.1 이후 이직자)</td></tr>
<tr><td>1일 하한액 (8시간 기준)</td><td>66,048원 (최저임금 10,320원 × 80% × 8시간)</td></tr>
<tr><td>지급률</td><td>퇴사 전 평균임금의 60%</td></tr></table>
<p class="formula">1일 구직급여 = 1일 평균임금 × 60% (하한액 ~ 상한액 사이로 조정)</p>
<p>하한액은 1일 소정근로시간에 비례합니다. 하루 4시간 일했다면 하한액은 33,024원입니다.</p>
<h2>받을 수 있는 일수 (소정급여일수)</h2>
<table class="t"><tr><th>가입기간</th><th>1년 미만</th><th>1~3년</th><th>3~5년</th><th>5~10년</th><th>10년 이상</th></tr>
<tr><td>50세 미만</td><td>120일</td><td>150일</td><td>180일</td><td>210일</td><td>240일</td></tr>
<tr><td>50세 이상·장애인</td><td>120일</td><td>180일</td><td>210일</td><td>240일</td><td>270일</td></tr></table>
<h2>받을 수 있는 조건</h2>
<ul><li>퇴사 전 18개월 동안 고용보험 피보험단위기간이 <b>180일 이상</b></li>
<li>권고사직·계약만료·폐업 등 <b>비자발적 퇴사</b> (자발적 퇴사도 임금체불, 통근 곤란 등 정당한 사유가 있으면 가능)</li>
<li>일할 의사와 능력이 있고 <b>적극적으로 재취업 활동</b>을 할 것</li></ul>
<h2>2027년 개편안 (미확정)</h2>
<p>정부가 2026년 9월 구직급여를 주 6일 기준으로 지급하고 상한액을 하한액에 연동하는 개편안을 발표했습니다. 아직 법 개정 전이므로 이 계산기는 현행 기준을 씁니다. 확정되면 바로 반영합니다.</p>
""",
faq=[
 ("자진 퇴사하면 실업급여를 못 받나요?", "원칙적으로 받을 수 없지만 임금체불, 최저임금 미달, 통근 곤란, 질병 등 고용보험법 시행규칙에 정한 정당한 사유가 있으면 받을 수 있습니다."),
 ("실업급여는 언제 신청하나요?", "퇴사 다음 날부터 12개월 안에 받아야 하므로 퇴사 후 바로 고용24에서 구직 등록을 하고 거주지 고용센터에 신청하는 것이 좋습니다."),
 ("아르바이트도 실업급여를 받을 수 있나요?", "고용보험에 가입해 180일 이상 피보험단위기간을 채웠다면 아르바이트도 받을 수 있습니다."),
],
sources=[LAW("고용보험법 제45조·제46조·별표1"), ("2026년 구직급여 상한액 인상 (고용노동부)", "https://www.moel.go.kr/")],
related=["severance", "insurance", "minwage"], promo=False,
),
# ------------------------------------------------------------------ 연차
dict(
slug="leave", short="연차 계산기", tag="입사일로 내 연차 일수 확인",
title="연차 계산기 — 입사일로 연차휴가 일수 계산 (1년 미만·근속연수별)",
desc="입사일과 기준일을 넣으면 근로기준법에 따른 연차휴가 일수를 계산합니다. 1년 미만 월차, 3년차 이후 가산 연차, 최대 25일까지.",
h1="연차 계산기",
lead="입사일과 확인하고 싶은 날짜를 넣으면 그 시점에 발생한 연차 일수를 알려 드립니다. (상시 5인 이상 사업장 기준)",
fields=[
 dict(id="start", type="date", label="입사일", value="2024-03-01", pair=True),
 dict(id="ref", type="date", label="기준일", value="2026-10-17"),
],
js="""
var s=U.str('start'),f=U.str('ref');if(!s||!f){U.set('result',U.note('날짜를 입력하세요.'));return;}
var r=Calc.annualLeave(s,f);
U.set('result','<p class="big">'+r.days+'일</p>'+
 (r.under1?U.row('근속','1년 미만 · '+r.months+'개월 개근')+U.note('1년 미만은 1개월 개근할 때마다 1일씩, 최대 11일이 생깁니다.')
 :U.row('근속연수',r.years+'년')+U.row('계산','15일 + 가산 '+(r.days-15)+'일')+U.note('직전 1년 출근율 80% 이상일 때 기준입니다.')));
""",
article="""
<h2>연차는 이렇게 생깁니다</h2>
<table class="t"><tr><th>근속</th><th>연차</th></tr>
<tr><td>1년 미만</td><td>1개월 개근마다 1일 (최대 11일)</td></tr>
<tr><td>1~2년</td><td>15일</td></tr><tr><td>3~4년</td><td>16일</td></tr><tr><td>5~6년</td><td>17일</td></tr>
<tr><td>11~12년</td><td>20일</td></tr><tr><td>21년 이상</td><td>25일 (상한)</td></tr></table>
<p class="formula">1년 이상 연차 = 15일 + (근속연수 − 1) ÷ 2 (소수점 버림), 최대 25일</p>
<h2>꼭 알아둘 점</h2>
<ul><li>연차휴가는 <b>상시 근로자 5인 이상</b> 사업장에 적용됩니다.</li>
<li>1년 동안 출근율이 80% 미만이면 그해에는 개근한 달마다 1일씩만 생깁니다.</li>
<li>주 15시간 미만 근로자는 연차가 없고, 단시간 근로자는 근무시간에 비례해 시간 단위로 계산합니다.</li>
<li>쓰지 못한 연차는 사업주가 사용촉진을 하지 않았다면 연차수당으로 받을 수 있습니다.</li></ul>
<h2>회계연도 기준이라면?</h2>
<p>회사가 1월 1일 기준으로 연차를 일괄 부여하더라도, 퇴사할 때는 입사일 기준으로 다시 계산해 더 유리한 쪽으로 정산해야 합니다.</p>
""",
faq=[
 ("1년만 일하고 퇴사하면 연차가 몇 일인가요?", "1년 미만 기간에 생긴 최대 11일에, 1년을 채우고 다음 날까지 근로관계가 있으면 15일이 추가됩니다. 1년 계약직은 판례에 따라 11일만 인정되는 경우가 많습니다."),
 ("5인 미만 사업장도 연차가 있나요?", "아니요. 연차휴가 규정은 상시 근로자 5인 이상 사업장에만 적용됩니다."),
 ("못 쓴 연차는 돈으로 받을 수 있나요?", "사업주가 법에 정한 연차 사용촉진을 하지 않았다면 사용하지 못한 연차는 통상임금 기준 연차수당으로 받을 수 있습니다."),
],
sources=[LAW("근로기준법 제60조")],
related=["severance", "alba", "juhyu"], promo=False,
),
# ------------------------------------------------------------------ 4대보험
dict(
slug="insurance", short="4대보험 계산기", tag="월급에서 떼이는 금액 확인",
title="4대보험 계산기 2026·2027 — 국민연금·건강보험·고용보험 근로자 부담액",
desc="세전 월급을 넣으면 2026·2027년 요율로 국민연금, 건강보험, 장기요양보험, 고용보험 근로자 부담액과 공제 후 금액을 계산합니다.",
h1="4대보험 계산기",
lead="세전 월급(비과세 제외)을 넣으면 근로자 부담 4대보험료를 계산합니다.",
fields=[
 dict(id="year", type="seg", label="기준 연도", value="2026", options=[("2026", "2026년"), ("2027", "2027년")]),
 dict(id="monthly", type="money", label="월 보수 (세전, 비과세 제외)", hint="원", value="2,500,000"),
],
js="""
var y=+%s,m=U.val('monthly');if(!m){U.set('result',U.note('월급을 입력하세요.'));return;}
var r=Calc.insurance(m,y),R=Calc.INS[y];
U.set('result','<p class="big">'+U.won(r.total)+'<small>월 공제 합계</small></p>'+
 U.row('국민연금 ('+(R.np*100).toFixed(2)+'%%)',U.won(r.np))+U.row('건강보험 (3.595%%)',U.won(r.hi))+
 U.row('장기요양 (건보료 × 13.14%%)',U.won(r.ltc))+U.row('고용보험 (0.9%%)',U.won(r.ei))+
 U.row('공제 후 금액 (소득세 별도)',U.won(r.afterIns),true)+
 (y===2027?U.note('2027년 장기요양·고용보험 요율은 아직 확정 전이라 2026년 요율로 계산했습니다.'):''));
""" % (RADIO % "year"),
article="""
<h2>근로자 부담 요율</h2>
<table class="t"><tr><th>항목</th><th>2026년</th><th>2027년</th></tr>
<tr><td>국민연금</td><td>4.75% (전체 9.5%)</td><td>5.0% (전체 10%)</td></tr>
<tr><td>건강보험</td><td>3.595% (전체 7.19%)</td><td>3.595% (동결)</td></tr>
<tr><td>장기요양보험</td><td>건강보험료 × 13.14%</td><td>미확정</td></tr>
<tr><td>고용보험</td><td>0.9%</td><td>미확정 (인상안 논의 중)</td></tr></table>
<p>회사도 같은 금액(고용보험은 규모에 따라 더 많이)을 부담하고, 산재보험은 전액 회사가 냅니다.</p>
<h2>국민연금 기준소득월액</h2>
<p>국민연금은 월 보수에서 1,000원 미만을 버린 <b>기준소득월액</b>에 요율을 곱합니다. 2026년 7월~2027년 6월 기준소득월액은 하한 41만 원, 상한 659만 원입니다. 그래서 월 659만 원을 넘게 벌어도 국민연금은 313,020원(4.75%)까지만 냅니다.</p>
<h2>계산 예시 (월 250만 원, 2026년)</h2>
<ul><li>국민연금: 2,500,000 × 4.75% = 118,750원</li><li>건강보험: 2,500,000 × 3.595% = 89,870원</li>
<li>장기요양: 89,870 × 13.14% = 11,800원</li><li>고용보험: 2,500,000 × 0.9% = 22,500원</li></ul>
<p>각 보험료는 10원 미만을 버립니다. 실제 고지액은 회사가 신고한 보수월액과 연말정산·보수총액 신고에 따라 달라질 수 있습니다.</p>
""",
faq=[
 ("알바도 4대보험을 내야 하나요?", "월 60시간 이상 일하면 국민연금·건강보험·고용보험 가입 대상입니다. 60시간 미만이어도 3개월 이상 일하면 고용보험은 적용될 수 있습니다."),
 ("식대도 4대보험이 붙나요?", "월 20만 원까지 식대는 비과세라 보험료 계산에서 빠집니다. 이 계산기에는 비과세 금액을 뺀 보수를 넣어 주세요."),
 ("국민연금은 몇 살까지 내나요?", "만 18세 이상 60세 미만이 의무 가입 대상입니다. 60세 이후에는 원하면 임의계속가입할 수 있습니다."),
],
sources=[("국민연금 기준소득월액 상·하한액 (보건복지부, 2026.6)", "https://www.nps.or.kr/"), ("2027년 건강보험료율 동결 (2026.9.8 의결)", "https://www.nhis.or.kr/")],
related=["alba", "minwage", "freelancer"], promo=True,
),
# ------------------------------------------------------------------ 3.3%
dict(
slug="freelancer", short="3.3% 세금 계산기", tag="프리랜서 실수령액·역산",
title="3.3% 세금 계산기 — 프리랜서 실수령액·계약금액 역산",
desc="계약금액에서 3.3% 원천징수 후 실수령액을 계산하거나, 받고 싶은 실수령액으로 계약금액을 역산합니다.",
h1="3.3% 세금 계산기",
lead="프리랜서·사업소득 지급액의 3.3% 원천징수(소득세 3% + 지방소득세 0.3%)를 계산합니다.",
fields=[
 dict(id="mode", type="seg", label="계산 방향", value="g", options=[("g", "계약금액 → 실수령액"), ("n", "실수령액 → 계약금액")]),
 dict(id="amt", type="money", label="금액", hint="원", value="1,000,000"),
],
js="""
var mode=%s,a=U.val('amt');if(!a){U.set('result',U.note('금액을 입력하세요.'));return;}
var g=mode==='n'?Calc.freelancerGross(a).gross:a,r=Calc.freelancer(g);
U.set('result','<p class="big">'+U.won(mode==='n'?g:r.net)+'<small>'+(mode==='n'?'필요한 계약금액':'실수령액')+'</small></p>'+
 U.row('계약금액 (세전)',U.won(g))+U.row('소득세 3%%','−'+U.won(r.tax))+U.row('지방소득세 0.3%%','−'+U.won(r.local))+
 U.row('실수령액',U.won(r.net),true));
""" % (RADIO % "mode"),
article="""
<h2>3.3%는 이렇게 나뉩니다</h2>
<p class="formula">원천징수 = 소득세 3% + 지방소득세(소득세의 10%) = 3.3%</p>
<p>각각 10원 미만은 버립니다. 100만 원을 받기로 했다면 소득세 30,000원과 지방소득세 3,000원을 뗀 <b>967,000원</b>이 입금됩니다.</p>
<h2>3.3%는 최종 세금이 아닙니다</h2>
<p>3.3%는 미리 낸 세금(기납부세액)입니다. 다음 해 5월 종합소득세 신고 때 1년 소득과 경비로 실제 세금을 다시 계산해, 더 냈으면 돌려받고 덜 냈으면 추가로 냅니다. 소득이 적은 프리랜서는 상당 부분을 환급받는 경우가 많습니다.</p>
<h2>근로자인데 3.3%를 떼고 있다면</h2>
<p>정해진 시간·장소에서 지시를 받으며 일한다면 실질은 근로자일 수 있습니다. 이 경우 4대보험, 퇴직금, 실업급여, 연차 등 근로자 권리가 인정될 수 있으니 고용노동부(☎1350)에 상담해 보세요.</p>
""",
faq=[
 ("3.3% 뗀 돈은 돌려받을 수 있나요?", "다음 해 5월 종합소득세 신고에서 실제 세금보다 많이 냈다면 차액을 환급받습니다. 홈택스에서 직접 신고할 수 있습니다."),
 ("8.8%는 무엇인가요?", "강연료·원고료 같은 일시적인 기타소득은 필요경비 60%를 뺀 금액에 22%를 적용해 실제로는 지급액의 8.8%를 원천징수합니다."),
],
sources=[LAW("소득세법 제129조(원천징수세율)")],
related=["alba", "insurance", "minwage"], promo=False,
),
]

# ====================================================================== 추가 페이지
for _p in PAGES:
    _p.setdefault("group", "worker")

PAGES.insert(0, dict(
slug="salary", short="연봉 실수령액 계산기", tag="세금·4대보험 뗀 진짜 월급", group="worker",
title="연봉 실수령액 계산기 2026 — 국세청 간이세액표 그대로 (부양가족·자녀·식대 반영)",
desc="연봉을 넣으면 국민연금·건강보험·고용보험·근로소득세를 뺀 월 실수령액을 계산합니다. 국세청 근로소득 간이세액표(2026.3 자녀공제 개정)를 그대로 적용하고, 원하는 실수령액으로 연봉을 역산할 수도 있습니다.",
h1="연봉 실수령액 계산기",
lead="국세청 근로소득 간이세액표를 그대로 넣어 회사 급여명세서와 같은 방식으로 계산합니다.",
fields=[
 dict(id="mode", type="seg", label="계산 방향", value="a", options=[("a", "연봉 → 실수령액"), ("n", "실수령액 → 필요 연봉")]),
 dict(id="amt", type="money", label="연봉 (퇴직금 제외)", hint="원 · 역산이면 원하는 월 실수령액", value="40,000,000"),
 dict(id="nontax", type="money", label="월 비과세액", hint="식대 등, 최대 20만 원", value="200,000", pair=True),
 dict(id="year", type="select", label="4대보험 기준", value="2026", options=[("2026", "2026년"), ("2027", "2027년 (국민연금 10%)")]),
 dict(id="family", type="select", label="공제대상가족 수", hint="본인 포함", value="1", options=[(str(i), f"{i}명") for i in range(1, 12)], pair=True),
 dict(id="kids", type="select", label="8~20세 자녀 수", value="0", options=[(str(i), f"{i}명") for i in range(0, 7)]),
],
js="""
var mode=%s,amt=U.val('amt'),nt=U.val('nontax'),y=+U.str('year'),f=+U.str('family'),k=+U.str('kids');
if(!amt){U.set('result',U.note('금액을 입력하세요.'));return;}
if(k>f-1)k=Math.max(0,f-1);
var annual=mode==='n'?Calc.annualForNet(amt,nt,f,k,y):amt,r=Calc.netPay(annual,nt,f,k,y);
U.set('result',(mode==='n'?'<p class="big">연봉 '+U.won(annual)+'<small>이상이면 월 '+U.won(amt)+' 이상</small></p>':
 '<p class="big">'+U.won(r.net)+'<small>월 실수령액</small></p>')+
 U.row('월 급여 (연봉 ÷ 12)',U.won(r.gross))+U.row('비과세 (식대 등)',U.won(r.nontax))+
 U.row('국민연금','−'+U.won(r.np))+U.row('건강보험','−'+U.won(r.hi))+U.row('장기요양보험','−'+U.won(r.ltc))+U.row('고용보험','−'+U.won(r.ei))+
 U.row('근로소득세 (간이세액표)','−'+U.won(r.incomeTax))+U.row('지방소득세','−'+U.won(r.localTax))+
 U.row('공제 합계 ('+(r.rate*100).toFixed(1)+'%%)','−'+U.won(r.deductions),true)+
 U.row('연 실수령액 (× 12)',U.won(r.annualNet),true)+
 U.note('소득세는 매달 미리 떼는 금액이며, 실제 세금은 연말정산에서 확정됩니다.'));
""" % (RADIO % "mode"),
article="""
<h2>실수령액은 이렇게 계산됩니다</h2>
<p class="formula">실수령액 = 월 급여 − 4대보험(근로자 부담) − 근로소득세 − 지방소득세</p>
<ol><li><b>월 급여</b> = 연봉 ÷ 12. 퇴직금이 포함된 연봉이라면 ÷ 13으로 나눈 금액을 넣으세요.</li>
<li><b>4대보험</b>은 비과세(식대 월 20만 원까지)를 뺀 금액에 요율을 곱합니다. 2026년 근로자 부담은 국민연금 4.75%, 건강보험 3.595%, 장기요양 건강보험료의 13.14%, 고용보험 0.9%입니다.</li>
<li><b>근로소득세</b>는 국세청 「근로소득 간이세액표」(소득세법 시행령 별표2)에서 월 과세급여와 공제대상가족 수가 만나는 칸의 금액입니다. 이 계산기는 표의 646개 구간 × 11개 가족 칸을 그대로 담고 있습니다.</li>
<li><b>자녀 공제</b>: 2026년 3월 1일부터 8세 이상 20세 이하 자녀가 1명이면 20,830원, 2명이면 45,830원, 3명 이상이면 45,830원에 2명을 넘는 1명당 33,330원을 세액에서 뺍니다.</li>
<li><b>지방소득세</b>는 근로소득세의 10%입니다.</li></ol>
<h2>공제대상가족 수 세는 법</h2>
<p>본인을 포함해, 연간 소득금액 100만 원 이하(근로소득만 있으면 총급여 500만 원 이하)인 배우자·20세 이하 자녀·60세 이상 부모 등을 셉니다. 맞벌이라면 각자 본인 1명으로 계산하는 경우가 많습니다.</p>
<h2>회사 명세서와 금액이 다르다면</h2>
<ul><li>회사가 근로자 요청으로 간이세액의 80% 또는 120%를 적용하고 있을 수 있습니다.</li>
<li>4대보험은 전년도 보수 기준으로 신고된 금액이라 이번 달 급여와 다를 수 있습니다.</li>
<li>야근·상여금이 있는 달은 과세급여가 늘어 세금이 더 나옵니다.</li></ul>
""",
faq=[
 ("연봉에 퇴직금이 포함돼 있으면요?", "퇴직금 포함 연봉은 연봉을 13으로 나눈 금액이 실제 월급입니다. 이 경우 연봉 칸에 '포함 연봉 ÷ 13 × 12' 금액을 넣으세요."),
 ("간이세액표 80%·120%는 뭔가요?", "근로자는 매달 떼는 소득세를 간이세액의 80%, 100%, 120% 중에서 고를 수 있습니다. 80%면 월급은 늘지만 연말정산에서 더 낼 가능성이 커집니다."),
 ("식대 비과세는 꼭 넣어야 하나요?", "회사가 식대를 비과세로 처리하면 그만큼 세금과 4대보험이 줄어듭니다. 명세서에 '식대'가 따로 있으면 그 금액(최대 월 20만 원)을 넣으세요."),
 ("2027년에는 실수령액이 줄어드나요?", "국민연금 보험료율이 9.5%에서 10%로 올라 근로자 부담이 0.25%포인트 늘어납니다. 연봉 4,000만 원이면 월 약 7,800원 줄어듭니다."),
],
sources=[("소득세법 시행령 [별표2] 근로소득 간이세액표 (국가법령정보센터)", "https://www.law.go.kr/"), ("국세청 근로소득 간이세액표 조회 (홈택스)", "https://www.hometax.go.kr/"), ("2026년 4대보험 요율", "https://www.nps.or.kr/")],
related=["salary-table", "insurance", "severance"], promo=False,
))

PAGES.append(dict(
slug="labor-cost", short="사장님 인건비 계산기", tag="직원 1명 뽑으면 실제로 드는 돈", group="boss",
title="인건비 계산기 2026 — 직원 1명 채용 시 사업주 부담 4대보험·퇴직금 포함 총비용",
desc="직원 월급을 넣으면 사업주가 부담하는 국민연금·건강보험·고용보험·산재보험과 퇴직금 적립액까지 더한 실제 인건비를 계산합니다. 알바 시급 계산도 가능.",
h1="사장님 인건비 계산기",
lead="직원에게 주는 월급 말고, 사장님 통장에서 실제로 나가는 돈을 계산합니다.",
fields=[
 dict(id="mode", type="seg", label="급여 형태", value="m", options=[("m", "월급제"), ("h", "시급제 (알바)")]),
 dict(id="pay", type="money", label="월급 또는 시급", hint="원 (비과세 제외)", value="2,500,000", pair=True),
 dict(id="hours", type="number", label="주 근무시간", hint="시급제만", value="20", step="0.5"),
 dict(id="ia", type="number", label="산재보험 요율", hint="% · 업종별 (2026 평균 1.47)", value="1.47", step="0.01"),
 dict(id="year", type="seg", label="기준 연도", value="2026", options=[("2026", "2026년"), ("2027", "2027년")]),
],
js="""
var mode=%s,y=+%s,p=U.val('pay'),w=U.val('hours'),ia=U.val('ia')/100;
if(!p){U.set('result',U.note('금액을 입력하세요.'));return;}
var monthly=p,extra='';
if(mode==='h'){var a=Calc.albaMonthly(p,w);monthly=a.monthTotal;extra=U.row('월 급여 (주휴 포함 '+a.monthHours+'시간)',U.won(monthly));}
var e=Calc.employerCost(monthly,y,ia),insOn=mode==='m'||w*4.345>=60;
if(!insOn){e.total-=e.np+e.hi+e.ltc+e.ei;e.np=e.hi=e.ltc=e.ei=0;e.insTotal=e.ia;}
if(mode==='h'&&w<15){e.total-=e.severance;e.severance=0;}
U.set('result','<p class="big">'+U.won(e.total)+'<small>월 실제 인건비</small></p>'+extra+
 U.row('국민연금 (사업주)',U.won(e.np))+U.row('건강보험 (사업주)',U.won(e.hi))+U.row('장기요양 (사업주)',U.won(e.ltc))+
 U.row('고용보험 (사업주, 1.15%%)',U.won(e.ei))+U.row('산재보험 (전액 사업주)',U.won(e.ia))+
 U.row('퇴직금 적립 (월급 ÷ 12)',U.won(e.severance))+U.row('연간 총 인건비',U.won(e.total*12),true)+
 (insOn?'':U.note('월 60시간 미만이라 국민연금·건강·고용보험은 제외했습니다(산재는 항상 적용).'))+
 (mode==='h'&&w<15?U.note('주 15시간 미만은 퇴직금·주휴수당 대상이 아닙니다.'):''));
""" % (RADIO % "mode", RADIO % "year"),
article="""
<h2>월급 250만 원 직원, 실제 비용은?</h2>
<p>2026년 기준으로 월급 250만 원 직원 1명에게 사업주가 추가로 부담하는 금액은 4대보험 약 29만 원(산재 평균요율 적용)과 퇴직금 적립 약 21만 원입니다. 월 총비용은 약 299만 원으로, <b>월급의 약 1.2배</b>입니다.</p>
<h2>사업주 부담 요율 (2026년)</h2>
<table class="t"><tr><th>항목</th><th>사업주 부담</th></tr>
<tr><td>국민연금</td><td>4.75% (근로자와 같음)</td></tr>
<tr><td>건강보험</td><td>3.595% + 장기요양(건보료의 13.14%)</td></tr>
<tr><td>고용보험</td><td>실업급여 0.9% + 고용안정·직업능력개발 0.25% (150인 미만)</td></tr>
<tr><td>산재보험</td><td>업종별 요율 전액 (2026년 평균 1.47%)</td></tr>
<tr><td>퇴직금</td><td>1년 이상 근무 시 연 1개월분 (월 환산 1/12)</td></tr></table>
<h2>두루누리 지원으로 줄일 수 있어요</h2>
<p>근로자 10명 미만 사업장에서 보수가 낮은 신규 가입 근로자는 국민연금·고용보험료의 일부를 지원받을 수 있습니다(두루누리 사회보험료 지원사업). 보수 기준과 지원율은 해마다 바뀌므로 신청 전에 두루누리 누리집에서 확인하세요.</p>
<h2>알바를 쓸 때 꼭 챙길 것</h2>
<ul><li>주 15시간 이상이면 주휴수당과(1년 이상 시) 퇴직금이 생깁니다.</li><li>월 60시간 이상이면 4대보험 가입 대상입니다.</li><li>임금명세서는 5인 미만 사업장도 매번 교부해야 합니다.</li></ul>
""",
faq=[
 ("산재보험 요율은 어디서 확인하나요?", "근로복지공단 고용·산재보험 토탈서비스에서 사업장의 업종 요율을 확인할 수 있습니다. 출퇴근재해 요율이 포함된 금액입니다."),
 ("퇴직금 적립은 꼭 해야 하나요?", "적립 자체는 의무가 아니지만 1년 이상 근무한 직원이 퇴사하면 한꺼번에 지급해야 하므로 매달 1/12씩 따로 모아 두는 것이 안전합니다."),
 ("4대보험을 안 들면 안 되나요?", "가입 대상인 직원을 신고하지 않으면 최대 3년치 보험료를 소급해 내고 과태료도 부과될 수 있습니다."),
],
sources=[("2026년 산재보험료율 1.47% 동결 (고용노동부 고시)", "https://www.moel.go.kr/"), ("두루누리 사회보험료 지원", "https://insurancesupport.or.kr/")],
related=["payslip", "juhyu", "insurance"], promo=True,
))

PAGES.append(dict(
slug="payslip", short="임금명세서 만들기", tag="무료 · 법정 기재사항 자동", group="boss",
title="임금명세서 양식 자동 작성 — 무료 급여명세서 만들기 (5인 미만 필수)",
desc="시급·근무시간만 넣으면 근로기준법 시행령 제27조의2 필수 기재사항을 모두 갖춘 임금명세서가 완성됩니다. 주휴수당·4대보험·3.3% 자동 계산, 바로 인쇄·PDF 저장.",
h1="임금명세서 만들기",
lead="빈칸을 채우면 아래에 법정 임금명세서가 완성됩니다. 사업장 정보는 이 브라우저에 기억됩니다.",
fields=[
 dict(id="biz", type="text", label="사업장명", value="하늘카페", pair=True),
 dict(id="ceo", type="text", label="대표자", value="홍길동"),
 dict(id="name", type="text", label="직원 성명", value="김하늘", pair=True),
 dict(id="birth", type="date", label="생년월일", value="2001-03-14"),
 dict(id="ym", type="month", label="귀속 월", value="2026-10", pair=True),
 dict(id="payday", type="date", label="지급일", value="2026-11-10"),
 dict(id="hourly", type="money", label="시급", hint="원", value="10,500", pair=True),
 dict(id="worked", type="number", label="이번 달 실근무시간", hint="휴게 제외", value="85", step="0.5"),
 dict(id="weekly", type="number", label="주 소정근로시간", hint="주휴 계산용", value="20", step="0.5", pair=True),
 dict(id="weeks", type="number", label="주휴 지급 주수", hint="결근 없는 주", value="4", step="1"),
 dict(id="ot", type="number", label="연장근로시간", hint="1일 8h 초과", value="0", step="0.5", pair=True),
 dict(id="night", type="number", label="야간근로시간", hint="22~06시", value="0", step="0.5"),
 dict(id="etc", type="money", label="기타 수당", hint="원", value="0", pair=True),
 dict(id="meal", type="money", label="식대 (비과세)", hint="원", value="0"),
 dict(id="size", type="seg", label="사업장 규모", value="u5", options=[("u5", "5인 미만"), ("o5", "5인 이상")]),
 dict(id="ded", type="seg", label="공제 방식", value="33", options=[("none", "공제 없음"), ("33", "3.3%"), ("ins", "4대보험+소득세")]),
],
js="""
var g=function(id){return U.str(id)},h=U.val('hourly'),wk=U.val('worked'),jw=Calc.juhyuHours(U.val('weekly')),wks=U.val('weeks'),
ot=U.val('ot'),nt=U.val('night'),etc=U.val('etc'),meal=U.val('meal'),o5=%s==='o5',ded=%s;
try{localStorage.setItem('ps_biz',JSON.stringify({biz:g('biz'),ceo:g('ceo')}))}catch(_){}
var base=Math.round(wk*h),ju=Math.round(jw*h*wks),otp=o5?Math.round(ot*h*0.5):0,ntp=o5?Math.round(nt*h*0.5):0;
var total=base+ju+otp+ntp+etc+meal,taxable=total-meal,yr=+(g('ym').slice(0,4)||2026),D=[];
if(ded==='33'){var f=Calc.freelancer(taxable);D=[['소득세 (3%%)',f.tax],['지방소득세',f.local]];}
if(ded==='ins'){var i=Calc.insurance(taxable,yr>=2027?2027:2026),t=Calc.incomeTax(taxable,1,0);
 D=[['국민연금',i.np],['건강보험',i.hi],['장기요양보험',i.ltc],['고용보험',i.ei],['근로소득세',t.tax],['지방소득세',t.local]];}
var dsum=D.reduce(function(s,x){return s+x[1]},0),E=function(s){return String(s).replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})};
var ym=g('ym').split('-'),rows=[['기본급',base,U.fmt(wk)+'시간 × '+U.won(h)],['주휴수당',ju,jw?U.fmt(jw,2)+'시간 × '+U.won(h)+' × '+wks+'주':'해당 없음 (주 15시간 미만)']];
if(o5)rows.push(['연장근로 가산수당',otp,U.fmt(ot)+'시간 × '+U.won(h)+' × 0.5'],['야간근로 가산수당',ntp,U.fmt(nt)+'시간 × '+U.won(h)+' × 0.5']);
if(etc)rows.push(['기타 수당',etc,'']);if(meal)rows.push(['식대 (비과세)',meal,'']);
var tr=function(a){return '<tr><td>'+a[0]+'</td><td class="n">'+U.won(a[1])+'</td><td>'+(a[2]||'')+'</td></tr>'},tr2=function(a){return '<tr><td>'+a[0]+'</td><td class="n">'+U.won(a[1])+'</td></tr>'};
U.set('result','<div class="slip" id="slip"><h3>임금명세서</h3><p class="sub">'+(ym[0]||'')+'년 '+(+ym[1]||'')+'월분</p>'+
 '<table class="t"><tr><th>성명</th><td>'+E(g('name'))+'</td><th>생년월일</th><td>'+E(g('birth'))+'</td></tr><tr><th>사업장</th><td>'+E(g('biz'))+'</td><th>지급일</th><td>'+E(g('payday'))+'</td></tr></table>'+
 '<table class="t"><tr><th>지급 항목</th><th>금액</th><th>계산 방법</th></tr>'+rows.map(tr).join('')+'<tr class="sum"><td>지급 총액</td><td class="n">'+U.won(total)+'</td><td></td></tr></table>'+
 '<table class="t"><tr><th>공제 항목</th><th>금액</th></tr>'+(D.length?D.map(tr2).join(''):'<tr><td>공제 없음</td><td class="n">0원</td></tr>')+'<tr class="sum"><td>공제 총액</td><td class="n">'+U.won(dsum)+'</td></tr></table>'+
 '<p class="pay">실 지급액 <b>'+U.won(total-dsum)+'</b></p>'+
 '<p class="hrs">총 근로시간 '+U.fmt(wk)+'시간'+(o5?' · 연장 '+U.fmt(ot)+'시간 · 야간 '+U.fmt(nt)+'시간':'')+'</p>'+
 '<p class="sign">'+E(g('biz'))+' 대표 '+E(g('ceo'))+' (인)</p></div>'+
 '<div class="actions"><button class="btn primary" type="button" onclick="window.print()">인쇄 · PDF 저장</button></div>'+
 U.note('공제 방식이 4대보험이면 공제대상가족 1명 기준 간이세액을 적용했습니다.'));
""" % (RADIO % "size", RADIO % "ded"),
pre_js="try{var s=JSON.parse(localStorage.getItem('ps_biz')||'null');if(s){if(s.biz)document.getElementById('biz').value=s.biz;if(s.ceo)document.getElementById('ceo').value=s.ceo;}}catch(_){}",
article="""
<h2>임금명세서, 꼭 줘야 하나요?</h2>
<p>네. 2021년 11월 19일부터 <b>근로자를 1명이라도 고용한 모든 사업장</b>은 임금을 줄 때마다 임금명세서를 교부해야 합니다(근로기준법 제48조 제2항). 주지 않으면 1차 30만 원, 기재사항을 빠뜨리거나 사실과 다르게 쓰면 1차 20만 원의 과태료가 부과됩니다.</p>
<h2>반드시 들어가야 하는 항목 (시행령 제27조의2)</h2>
<ol><li>근로자 성명, 생년월일 등 근로자를 특정할 수 있는 정보</li><li>임금 지급일</li><li>임금 총액</li>
<li>기본급, 각종 수당, 상여금, 성과금 등 항목별 금액</li><li>항목별 금액이 출근일수·시간에 따라 달라지면 그 계산 방법</li>
<li>연장·야간·휴일근로 시간 수 (상시 4인 이하 사업장은 생략 가능)</li><li>공제 항목별 금액과 공제 총액</li></ol>
<p>이 도구는 위 항목을 모두 자동으로 채웁니다.</p>
<h2>어떻게 전달하나요?</h2>
<p>종이로 주거나, 이메일·카카오톡·문자 등 전자문서로 보내도 됩니다. <b>인쇄 · PDF 저장</b> 버튼을 누르고 인쇄 대상에서 'PDF로 저장'을 고르면 파일로 저장해 보낼 수 있습니다.</p>
<h2>직원이 여러 명이고 매달 쓴다면</h2>
<p>근무기록만 입력하면 주휴수당 주차별 판정, 급여대장, 직원별 임금명세서까지 한 번에 만드는 엑셀 템플릿도 있습니다.</p>
""",
faq=[
 ("입력한 직원 정보가 어딘가에 저장되나요?", "아니요. 계산과 명세서 작성은 모두 이 브라우저 안에서만 이루어집니다. 사업장명과 대표자만 다음 방문 때 편하도록 이 기기의 브라우저에 기억합니다."),
 ("임금명세서는 보관해야 하나요?", "임금명세서 자체는 보관 의무가 없지만, 그 바탕이 되는 임금대장은 3년간 보관해야 합니다."),
 ("일용직에게도 줘야 하나요?", "네. 일용근로자도 임금을 지급할 때 임금명세서를 교부해야 합니다. 다만 30일 미만 일용근로자는 생년월일 대신 다른 정보로 특정할 수 있습니다."),
],
sources=[LAW("근로기준법 제48조, 시행령 제27조의2"), ("임금명세서 작성 안내 (고용노동부)", "https://www.moel.go.kr/")],
related=["labor-cost", "juhyu", "alba"], promo=True,
))

PAGES.insert(4, dict(
slug="overtime", short="연장·야간·휴일수당 계산기", tag="5인 이상 사업장 가산수당", group="worker",
title="연장·야간·휴일근로수당 계산기 — 1.5배·2배 가산 자동 계산",
desc="시급과 연장·야간·휴일 근무시간을 넣으면 근로기준법 제56조에 따른 가산수당을 계산합니다. 휴일 8시간 초과 2배, 야간 50% 중복 가산까지 반영.",
h1="연장·야간·휴일수당 계산기",
lead="상시 근로자 5인 이상 사업장 기준입니다. 이번 달(또는 이번 주) 해당 시간을 넣어 주세요.",
fields=[
 dict(id="hourly", type="money", label="시급 (통상시급)", hint="원", value="10,320"),
 dict(id="ot", type="number", label="연장근로", hint="1일 8h·1주 40h 초과", value="6", step="0.5", pair=True),
 dict(id="night", type="number", label="야간근로", hint="22시~06시", value="4", step="0.5"),
 dict(id="h8", type="number", label="휴일근로 8시간 이내", hint="시간", value="8", step="0.5", pair=True),
 dict(id="hx", type="number", label="휴일근로 8시간 초과", hint="시간", value="0", step="0.5"),
],
js="""
var h=U.val('hourly');if(!h){U.set('result',U.note('시급을 입력하세요.'));return;}
var r=Calc.overtimePay(h,U.val('ot'),U.val('night'),U.val('h8'),U.val('hx'));
U.set('result','<p class="big">'+U.won(r.total)+'<small>추가로 받을 금액</small></p>'+
 U.row('연장·휴일 근무시간 임금 (1배)',U.won(r.base))+U.row('연장 가산 (50%%)',U.won(r.otP))+U.row('야간 가산 (50%%)',U.won(r.nightP))+
 U.row('휴일 가산 (8h 이내 50%%, 초과 100%%)',U.won(r.holP))+U.row('가산수당 합계',U.won(r.premium),true)+
 U.note('야간에 연장근로를 했다면 같은 시간을 연장과 야간 양쪽에 모두 넣으세요. 가산이 겹쳐 적용됩니다.'));
""",
article="""
<h2>가산 기준 (근로기준법 제56조)</h2>
<table class="t"><tr><th>구분</th><th>기준</th><th>받는 금액</th></tr>
<tr><td>연장근로</td><td>1일 8시간 또는 1주 40시간 초과</td><td>통상임금의 1.5배</td></tr>
<tr><td>야간근로</td><td>오후 10시 ~ 오전 6시</td><td>통상임금의 0.5배 추가</td></tr>
<tr><td>휴일근로</td><td>8시간 이내</td><td>1.5배</td></tr>
<tr><td>휴일근로</td><td>8시간 초과분</td><td>2배</td></tr></table>
<h2>겹치면 더해집니다</h2>
<p>야간에 연장근로를 하면 연장 50%와 야간 50%가 함께 붙어 그 시간은 통상시급의 2배가 됩니다. 휴일에 8시간을 넘겨 밤까지 일하면 휴일 초과 100%에 야간 50%가 더해져 2.5배입니다.</p>
<h2>예시 (시급 10,320원)</h2>
<ul><li>평일 2시간 연장: 10,320 × 1.5 × 2 = 30,960원</li><li>밤 10시~12시 근무(연장 아님): 가산분 10,320 × 0.5 × 2 = 10,320원</li>
<li>일요일 10시간 근무: 8시간 × 1.5배 + 2시간 × 2배 = 165,120원</li></ul>
<h2>5인 미만 사업장은?</h2>
<p>상시 근로자 4인 이하 사업장은 가산수당 지급 의무가 없습니다. 일한 시간만큼 기본 시급(1배)은 당연히 받아야 하고, 근로계약서에서 가산을 약속했다면 그대로 받을 수 있습니다.</p>
""",
faq=[
 ("알바도 야간수당을 받나요?", "상시 근로자 5인 이상 사업장이라면 아르바이트도 오후 10시~오전 6시 근무에 대해 50%를 더 받습니다."),
 ("통상시급은 어떻게 구하나요?", "시급제는 계약 시급이 통상시급입니다. 월급제는 기본급과 고정수당 합계를 월 소정근로시간(주 40시간이면 209시간)으로 나눕니다."),
 ("주 52시간을 넘기면 어떻게 되나요?", "연장근로는 1주 12시간까지만 가능합니다. 넘기면 사업주가 처벌 대상이 되지만, 이미 일한 시간에 대한 가산수당은 받을 수 있습니다."),
],
sources=[LAW("근로기준법 제56조")],
related=["alba", "juhyu", "minwage"], promo=False,
))

PAGES.insert(9, dict(
slug="daily-tax", short="일용직 세금 계산기", tag="일당 15만 원 넘으면 떼는 세금", group="worker",
title="일용직 세금 계산기 — 일당 실수령액 (일용근로소득 2.7%)",
desc="일당과 근무일수를 넣으면 일용근로소득세와 지방소득세, 실수령액을 계산합니다. 일 15만 원 비과세, 55% 세액공제, 1,000원 미만 소액부징수 반영.",
h1="일용직 세금 계산기",
lead="건설 현장, 행사 스태프, 단기 알바처럼 일당으로 받는 일용근로소득의 원천징수액을 계산합니다.",
fields=[
 dict(id="wage", type="money", label="일당 (세전)", hint="원", value="200,000", pair=True),
 dict(id="days", type="number", label="근무일수", hint="일", value="10", step="1"),
],
js="""
var w=U.val('wage'),d=U.val('days')||1;if(!w){U.set('result',U.note('일당을 입력하세요.'));return;}
var r=Calc.dailyWorkerTax(w,d);
U.set('result','<p class="big">'+U.won(r.perDayNet)+'<small>하루 실수령액</small></p>'+
 U.row('소득세 / 일',U.won(r.tax))+U.row('지방소득세 / 일',U.won(r.local))+
 U.row(d+'일 세금 합계',U.won(r.totalTax))+U.row(d+'일 실수령 합계',U.won(r.totalNet),true)+
 (r.tax===0&&w>150000?U.note('하루 소득세가 1,000원 미만이라 떼지 않습니다(소액부징수).'):'')+
 U.note('고용보험(0.9%)에 가입된 일용직이라면 별도로 공제될 수 있습니다.'));
""",
article="""
<h2>계산 방법</h2>
<p class="formula">소득세 = (일당 − 150,000원) × 6% × (1 − 55%)</p>
<p>일당에서 하루 15만 원을 근로소득공제로 빼고, 6% 세율을 적용한 뒤 55%를 세액공제합니다. 결국 15만 원을 넘는 금액의 <b>2.7%</b>가 소득세이고, 지방소득세는 그 10%입니다.</p>
<h2>일당별 세금</h2>
<table class="t"><tr><th>일당</th><th>소득세</th><th>지방소득세</th><th>실수령액</th></tr>
<tr><td>150,000원</td><td>0원</td><td>0원</td><td>150,000원</td></tr>
<tr><td>180,000원</td><td>0원 (소액부징수)</td><td>0원</td><td>180,000원</td></tr>
<tr><td>200,000원</td><td>1,350원</td><td>130원</td><td>198,520원</td></tr>
<tr><td>250,000원</td><td>2,700원</td><td>270원</td><td>247,030원</td></tr>
<tr><td>300,000원</td><td>4,050원</td><td>400원</td><td>295,550원</td></tr></table>
<h2>소액부징수란?</h2>
<p>하루 원천징수할 소득세가 1,000원 미만이면 떼지 않습니다. 일당 187,037원까지는 세금이 0원입니다.</p>
<h2>같은 곳에서 오래 일하면?</h2>
<p>같은 사업장에서 3개월 이상(건설공사는 1년 이상) 계속 일하면 일용근로자가 아니라 일반 근로자로 보아 근로소득 간이세액표로 원천징수합니다.</p>
""",
faq=[
 ("일용직도 연말정산을 하나요?", "일용근로소득은 원천징수로 납세 의무가 끝나는 분리과세 소득이라 연말정산이나 종합소득세 신고에 합산하지 않습니다."),
 ("3.3%를 떼는 경우와 무엇이 다른가요?", "3.3%는 사업소득(프리랜서) 원천징수입니다. 일용근로자는 근로자이므로 원래 일용근로소득 방식(15만 원 공제 후 2.7%)으로 떼야 합니다."),
],
sources=[LAW("소득세법 제14조·제47조·제59조, 제86조(소액부징수)")],
related=["freelancer", "alba", "overtime"], promo=False,
))

PAGES.insert(7, dict(
slug="parental-leave", short="육아휴직 급여 계산기", tag="월별 지급액·6+6·한부모", group="worker",
title="육아휴직 급여 계산기 2026 — 월 250만 원 상한, 6+6 부모육아휴직제 반영",
desc="통상임금과 휴직 개월수를 넣으면 2025년 개편 기준(1~3개월 250만, 4~6개월 200만, 7개월~ 160만 상한)으로 월별 육아휴직 급여와 총액을 계산합니다. 6+6 부모육아휴직제·한부모 특례 포함.",
h1="육아휴직 급여 계산기",
lead="월 통상임금과 휴직 기간을 넣으면 달마다 받는 금액과 합계를 계산합니다. 2025년 1월 1일 이후 시작한 육아휴직 기준입니다.",
fields=[
 dict(id="wage", type="money", label="월 통상임금", hint="원 (기본급+고정수당)", value="3,500,000", pair=True),
 dict(id="months", type="select", label="휴직 기간", value="12", options=[(str(i), f"{i}개월") for i in range(1, 19)]),
 dict(id="mode", type="seg", label="유형", value="normal", options=[("normal", "일반"), ("both", "6+6 부모 함께"), ("single", "한부모")]),
],
js="""
var w=U.val('wage'),m=+U.str('months'),mode=%s;if(!w){U.set('result',U.note('통상임금을 입력하세요.'));return;}
var r=Calc.parentalLeave(w,m,mode),rows=r.rows.map(function(x){return '<tr><td>'+x.month+'개월차</td><td>'+(x.rate*100)+'%%</td><td>'+U.won(x.cap)+'</td><td><b>'+U.won(x.amount)+'</b></td></tr>'}).join('');
U.set('result','<p class="big">'+U.won(r.total)+'<small>'+m+'개월 합계</small></p>'+
 '<div style="overflow-x:auto"><table class="t"><tr><th>기간</th><th>지급률</th><th>상한</th><th>받는 금액</th></tr>'+rows+'</table></div>'+
 (m>12?U.note('12개월을 넘는 휴직은 부모가 각각 3개월 이상 쓰거나 한부모·장애아 부모일 때 가능합니다(최대 18개월).'):'')+
 (mode==='both'?U.note('6+6은 자녀 생후 18개월 이내에 부모가 모두 육아휴직을 쓸 때 각자에게 적용됩니다.'):''));
""" % (RADIO % "mode"),
article="""
<h2>2025년부터 바뀐 육아휴직 급여</h2>
<table class="t"><tr><th>기간</th><th>지급률</th><th>월 상한</th></tr>
<tr><td>1~3개월</td><td>통상임금 100%</td><td>250만 원</td></tr>
<tr><td>4~6개월</td><td>통상임금 100%</td><td>200만 원</td></tr>
<tr><td>7개월 이후</td><td>통상임금 80%</td><td>160만 원</td></tr></table>
<p>하한액은 월 70만 원입니다. 예전처럼 급여 일부를 복직 6개월 뒤에 주던 '사후지급금'은 없어져, 휴직 기간 중 전액을 받습니다. 1년을 쓰면 최대 2,310만 원입니다.</p>
<h2>6+6 부모육아휴직제</h2>
<p>자녀가 생후 18개월 이내일 때 부모가 모두 육아휴직을 쓰면, 각자 첫 6개월 동안 통상임금 100%를 받고 상한이 달마다 올라갑니다.</p>
<table class="t"><tr><th>개월</th><th>1</th><th>2</th><th>3</th><th>4</th><th>5</th><th>6</th></tr>
<tr><td>월 상한</td><td>250만</td><td>250만</td><td>300만</td><td>350만</td><td>400만</td><td>450만</td></tr></table>
<p>부부가 함께 1년씩 쓰면 각자 최대 2,960만 원, 합계 5,920만 원입니다.</p>
<h2>한부모 근로자</h2>
<p>한부모는 첫 3개월 상한이 300만 원입니다. 이후 기간은 일반 기준과 같습니다.</p>
<h2>통상임금이란?</h2>
<p>매달 정기적으로 같은 금액을 받는 기본급과 고정수당을 합친 금액입니다. 연장근로수당이나 성과급처럼 달마다 달라지는 돈은 빠집니다. 정확한 금액은 회사 급여 담당자에게 확인하세요.</p>
""",
faq=[
 ("육아휴직 급여는 어디서 신청하나요?", "휴직을 시작하고 1개월이 지난 뒤부터 매달, 고용24(work24.go.kr)나 거주지 고용센터에서 신청합니다. 휴직이 끝난 뒤 12개월 안에 신청해야 합니다."),
 ("받을 수 있는 조건은?", "육아휴직 시작 전 고용보험 피보험단위기간이 180일 이상이어야 하고, 만 8세 이하 또는 초등학교 2학년 이하 자녀를 키워야 합니다."),
 ("휴직 중 회사에서 돈을 받으면 깎이나요?", "회사에서 받는 금액과 육아휴직 급여를 합쳐 통상임금을 넘으면 넘는 만큼 육아휴직 급여가 줄어듭니다."),
],
sources=[("육아휴직 급여 월 최대 250만 원 인상 (복지로)", "https://blog.bokjiro.go.kr/1673"), LAW("고용보험법 시행령 제95조")],
related=["salary", "unemployment", "severance"], promo=False,
))

PAGES.append(dict(
slug="loan", short="대출 이자 계산기", tag="원리금균등·원금균등·만기일시", group="worker",
title="대출 이자 계산기 — 원리금균등·원금균등·만기일시 월 상환액과 상환표",
desc="대출금, 금리, 기간을 넣으면 원리금균등·원금균등·만기일시 상환 방식별 월 상환액, 총이자, 회차별 상환표를 계산합니다.",
h1="대출 이자 계산기",
lead="대출 금액과 연 금리, 기간을 넣으면 매달 갚을 돈과 총이자를 계산합니다.",
fields=[
 dict(id="p", type="money", label="대출 금액", hint="원", value="100,000,000"),
 dict(id="rate", type="number", label="연 금리", hint="%", value="4.5", step="0.01", pair=True),
 dict(id="months", type="number", label="대출 기간", hint="개월", value="360", step="1"),
 dict(id="type", type="seg", label="상환 방식", value="ann", options=[("ann", "원리금균등"), ("prin", "원금균등"), ("bullet", "만기일시")]),
],
js="""
var p=U.val('p'),r=U.val('rate'),n=U.val('months'),ty=%s;if(!p||!n){U.set('result',U.note('금액과 기간을 입력하세요.'));return;}
if(n>600){U.set('result',U.note('기간은 600개월(50년) 이하로 입력하세요.','warn'));return;}
var s=Calc.loanSchedule(p,r,n,ty),R=s.rows,show=R.length<=24?R:R.slice(0,12).concat([null]).concat(R.slice(-6));
var tr=show.map(function(x){return x?'<tr><td>'+x.i+'</td><td>'+U.won(x.payment)+'</td><td>'+U.won(x.principal)+'</td><td>'+U.won(x.interest)+'</td><td>'+U.won(x.balance)+'</td></tr>':'<tr><td colspan="5">…</td></tr>'}).join('');
U.set('result','<p class="big">'+U.won(s.first)+'<small>첫 달 상환액</small></p>'+
 U.row('총이자',U.won(s.totalInterest))+U.row('총 상환액',U.won(s.totalPayment),true)+
 (ty==='prin'?U.row('마지막 달 상환액',U.won(R[R.length-1].payment)):'')+
 '<div style="overflow-x:auto"><table class="t"><tr><th>회차</th><th>상환액</th><th>원금</th><th>이자</th><th>잔액</th></tr>'+tr+'</table></div>');
""" % (RADIO % "type"),
article="""
<h2>상환 방식 비교</h2>
<table class="t"><tr><th>방식</th><th>매달 내는 돈</th><th>총이자</th></tr>
<tr><td>원리금균등</td><td>매달 같음</td><td>중간</td></tr>
<tr><td>원금균등</td><td>처음 많고 점점 줄어듦</td><td>가장 적음</td></tr>
<tr><td>만기일시</td><td>이자만 내다 마지막에 원금 전액</td><td>가장 많음</td></tr></table>
<h2>계산 방법</h2>
<p class="formula">원리금균등 월 상환액 = 대출금 × 월이율 ÷ (1 − (1 + 월이율)<sup>−개월수</sup>)</p>
<p>월이율은 연 금리 ÷ 12입니다. 1억 원을 연 5%, 30년(360개월) 원리금균등으로 빌리면 매달 536,822원을 내고, 총이자는 약 9,326만 원입니다.</p>
<h2>이자를 줄이는 방법</h2>
<ul><li>같은 조건이면 원금균등이 총이자가 가장 적습니다. 대신 초기 부담이 큽니다.</li>
<li>중도상환수수료가 없거나 면제 기간이 지났다면 일부 상환으로 이자를 줄일 수 있습니다.</li>
<li>금리가 0.1%포인트만 달라도 장기 대출에서는 총이자가 수백만 원 차이 날 수 있습니다.</li></ul>
<p class="src">실제 상환액은 은행의 일할 계산 방식, 거치기간, 금리 변동에 따라 조금 다를 수 있습니다.</p>
""",
faq=[
 ("원리금균등과 원금균등 중 무엇이 유리한가요?", "총이자는 원금균등이 적고, 매달 부담을 일정하게 하고 싶다면 원리금균등이 편합니다."),
 ("거치기간이 있으면요?", "거치기간 동안에는 이자만 내고, 그 뒤 남은 기간에 원금을 나눠 갚습니다. 이 계산기는 거치기간이 없는 경우를 계산합니다."),
],
sources=[("금융감독원 금융상품 통합비교공시 (금융상품한눈에)", "https://finlife.fss.or.kr/")],
related=["salary", "salary-table", "severance"], promo=False,
))
