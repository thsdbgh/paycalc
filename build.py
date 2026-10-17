#!/usr/bin/env python3
"""급여계산소 정적 사이트 생성기.

사용법:  python build.py  [--site-url https://도메인] [--adsense ca-pub-XXXX] [--kmong URL] [--email 주소]
결과물:  dist/  (Cloudflare Pages · GitHub Pages · Netlify에 그대로 올리면 됨)
"""
import argparse, html, json, shutil, datetime
from pathlib import Path

ROOT = Path(__file__).parent
SRC, DIST = ROOT / "src", ROOT / "dist"
SITE_NAME = "급여계산소"
# 검색엔진 소유 확인 (지우지 마세요)
VERIFY_META = '<meta name="naver-site-verification" content="713dec460b0c42601ce5efc3b8c1279d006d818d">'
UPDATED = "2026-10-17"

ap = argparse.ArgumentParser()
ap.add_argument("--site-url", default="https://example.com")
ap.add_argument("--adsense", default="")       # ca-pub-XXXXXXXXXXXXXXXX
ap.add_argument("--kmong", default="")         # 크몽 엑셀 판매 링크
ap.add_argument("--email", default="")
ap.add_argument("--contact-url", default="https://github.com/thsdbgh/paycalc/issues")
ap.add_argument("--preview", action="store_true")  # 미리보기용: 광고 자리 표시
args = ap.parse_args()
CONTACT_HREF = f"mailto:{args.email}" if args.email else args.contact_url
CONTACT_TEXT = args.email or "문의 게시판(GitHub Issues)"
BASE = args.site_url.rstrip("/")
BASE_PATH = "/" + BASE.split("://",1)[-1].split("/",1)[1] + "/" if BASE.count("/") > 2 else "/"

from pages import PAGES  # noqa: E402  (콘텐츠는 pages.py)
from guides import GUIDES  # noqa: E402
import subprocess
SAL = json.loads(subprocess.check_output(["node", str(ROOT / "tools" / "precompute.js")]))
TABLE_TILE = dict(slug="salary-table", short="연봉 실수령액표", tag="2천만~1억5천 한눈에")

def field_html(f):
    t = f["type"]
    lab = f'<label for="{f["id"]}">{f["label"]}' + (f' <span class="hint">{f["hint"]}</span>' if f.get("hint") else "") + "</label>"
    if t == "money":
        inp = f'<input id="{f["id"]}" inputmode="numeric" autocomplete="off" data-money value="{f.get("value","")}" placeholder="{f.get("ph","")}">'
    elif t == "number":
        inp = f'<input id="{f["id"]}" type="number" inputmode="decimal" step="{f.get("step","any")}" min="0" value="{f.get("value","")}">'
    elif t in ("date", "month", "text"):
        inp = f'<input id="{f["id"]}" type="{t}" value="{html.escape(str(f.get("value","")))}" autocomplete="off">'
    elif t == "select":
        opts = "".join(f'<option value="{v}"{" selected" if v == f.get("value") else ""}>{l}</option>' for v, l in f["options"])
        inp = f'<select id="{f["id"]}">{opts}</select>'
    elif t == "seg":
        inp = '<div class="seg">' + "".join(
            f'<label><input type="radio" name="{f["id"]}" value="{v}"{" checked" if v == f.get("value") else ""}><span>{l}</span></label>'
            for v, l in f["options"]) + "</div>"
        lab = f'<label>{f["label"]}</label>'
    return f'<div class="field">{lab}{inp}</div>'

def form_html(fields):
    out, i = [], 0
    while i < len(fields):
        f = fields[i]
        if f.get("pair") and i + 1 < len(fields):
            out.append(f'<div class="two">{field_html(f)}{field_html(fields[i+1])}</div>'); i += 2
        else:
            out.append(field_html(f)); i += 1
    return "".join(out)

def ad_slot(name):
    if args.adsense:
        return (f'<div class="ad" aria-label="광고"><ins class="adsbygoogle" style="display:block;width:100%" '
                f'data-ad-client="{args.adsense}" data-ad-format="auto" data-full-width-responsive="true"></ins>'
                f'<script>(adsbygoogle=window.adsbygoogle||[]).push({{}});</script></div>')
    return '<div class="ad" aria-label="광고 자리"></div>' if args.preview else ""

def promo():
    if not args.kmong:
        return ""
    return ('<div class="promo"><p><b>사장님이라면</b> — 출퇴근만 적으면 주휴수당·임금명세서까지 자동으로 만드는 엑셀</p>'
            f'<a href="{html.escape(args.kmong)}" target="_blank" rel="noopener sponsored">엑셀 보기</a></div>')

def head(title, desc, canonical, extra_ld=None):
    ads = (f'<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={args.adsense}" '
           'crossorigin="anonymous"></script>') if args.adsense else ""
    ld = [{"@context": "https://schema.org", "@type": "WebSite", "name": SITE_NAME, "url": BASE + "/"}]
    if extra_ld:
        ld += extra_ld
    return f"""<!doctype html><html lang="ko"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="website"><meta property="og:site_name" content="{SITE_NAME}">
<meta property="og:title" content="{html.escape(title)}"><meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{canonical}"><meta property="og:locale" content="ko_KR">
<meta property="og:image" content="{BASE}/og.png"><meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#1f3a5f">
{VERIFY_META}
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='14' fill='%231f3a5f'/%3E%3Ctext x='32' y='44' font-size='34' text-anchor='middle' fill='%23f2c94c' font-family='sans-serif' font-weight='700'%3E%E2%82%A9%3C/text%3E%3C/svg%3E">
<link rel="stylesheet" href="style.css">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
{ads}</head><body>
<header class="top"><div class="wrap"><a class="logo" href="index.html"><i>₩</i>{SITE_NAME}</a>
<nav class="mini"><a href="salary.html">실수령액</a><a href="juhyu.html">주휴수당</a><a href="payslip.html">명세서</a><a href="guides.html">가이드</a></nav></div></header>
<main class="wrap">"""

def foot(extra_js=""):
    links = " ".join(f'<a href="{p["slug"]}.html">{p["short"]}</a>' for p in PAGES)
    return f"""</main><footer><div class="wrap">
<p>{links}</p>
<p><a href="about.html">사이트 소개</a><a href="privacy.html">개인정보처리방침</a><a href="{CONTACT_HREF}" rel="noopener">문의</a></p>
<p>모든 계산은 브라우저 안에서만 이루어지며 입력값은 서버로 전송·저장되지 않습니다. 계산 결과는 참고용이며 법률·세무 자문을 대신하지 않습니다.
정확한 판단은 고용노동부 고객상담센터(☎1350), 국민연금공단·건강보험공단, 노무사·세무사에게 확인하세요.</p>
<p>© {datetime.date.today().year} {SITE_NAME} · 기준 갱신일 {UPDATED}</p></div></footer>
{extra_js}<script src="calc.js"></script><script src="app.js"></script>"""

def build_page(p):
    canonical = f"{BASE}/{p['slug']}"
    faq_ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in p["faq"]]}
    app_ld = {"@context": "https://schema.org", "@type": "WebApplication", "name": p["h1"], "url": canonical,
              "applicationCategory": "FinanceApplication", "operatingSystem": "All", "inLanguage": "ko",
              "offers": {"@type": "Offer", "price": "0", "priceCurrency": "KRW"}}
    bc_ld = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": SITE_NAME, "item": BASE + "/"},
        {"@type": "ListItem", "position": 2, "name": p["short"], "item": canonical}]}
    faq = "".join(f"<details><summary>{html.escape(q)}</summary><p>{html.escape(a)}</p></details>" for q, a in p["faq"])
    related = "".join(f'<a class="tile" href="{r["slug"]}.html"><b>{r["short"]}</b><span>{r["tag"]}</span></a>'
                      for r in PAGES + [TABLE_TILE] if r["slug"] in p["related"])
    srcs = "".join(f'<li><a href="{u}" rel="nofollow noopener" target="_blank">{html.escape(t)}</a></li>' for t, u in p["sources"])
    body = f"""<p class="crumb"><a href="index.html">홈</a> › {p['short']}</p>
<h1>{p['h1']}</h1><p class="lead">{p['lead']}</p>
<section class="card"><form class="calc" novalidate>{form_html(p['fields'])}</form>
<div class="result" id="result" aria-live="polite"></div>
<div class="actions"><button class="btn" type="button" data-copy>결과 복사</button></div></section>
{ad_slot('top')}
<article>{p['article']}</article>
{promo() if p.get('promo') else ''}
<h2>자주 묻는 질문</h2>{faq}
{ad_slot('bottom')}
<h2>함께 쓰면 좋은 계산기</h2><div class="grid">{related}</div>
<h2>참고 기준</h2><ul class="src">{srcs}</ul>
<p class="src">최종 확인: {UPDATED}. 법령·고시가 바뀌면 결과가 달라질 수 있습니다.</p>"""
    script = f"<script>{p.get('pre_js','')}bindCalc(function(){{{p['js']}}});</script>"
    needs_tax = p["slug"] in ("salary", "payslip")
    return head(p["title"], p["desc"], canonical, [faq_ld, app_ld, bc_ld]) + body + \
        foot('<script src="ganyi.js"></script>' if needs_tax else "") + script + "</body></html>"

def build_index():
    tile = lambda p: f'<a class="tile" href="{p["slug"]}.html"><b>{p["short"]}</b><span>{p["tag"]}</span></a>'
    tiles = "".join(tile(p) for p in PAGES if p["group"] == "worker") + tile(TABLE_TILE)
    boss = "".join(tile(p) for p in PAGES if p["group"] == "boss") + \
        "".join(tile(p) for p in PAGES if p["slug"] in ("juhyu", "minwage"))
    body = f"""<h1 style="margin-top:24px">월급·알바비·퇴직금, 바로 계산하세요</h1>
<p class="lead">2026년·2027년 최저임금과 4대보험 요율을 반영한 무료 급여 계산기 모음입니다. 회원가입 없이, 입력하는 즉시 결과가 나옵니다.</p>
<h2>근로자·알바</h2><div class="grid">{tiles}</div>
<h2>사장님</h2><div class="grid">{boss}</div>
<h2>가이드</h2><div class="grid">{"".join(f'<a class="tile" href="{g["slug"]}.html"><b>{html.escape(g["title"])}</b></a>' for g in GUIDES)}</div>
{ad_slot('home')}
{promo()}
<article>
<h2>2027년에 달라지는 것</h2>
<ul>
<li><b>최저임금 10,700원</b> — 2026년 10,320원에서 380원(3.7%) 올라, 주 40시간 기준 월 2,236,300원(209시간)입니다. 2027년 1월 1일 근무분부터 적용됩니다.</li>
<li><b>국민연금 보험료율 10%</b> — 연금개혁에 따라 해마다 0.5%포인트씩 올라 근로자 부담분은 5.0%가 됩니다.</li>
<li><b>건강보험료율 7.19% 동결</b> — 2026년 9월 건강보험정책심의위원회에서 동결이 결정됐습니다.</li>
<li><b>실업급여 개편 논의</b> — 정부가 주 6일 지급 기준 등 개편안을 발표했지만 아직 확정되지 않았습니다. 확정되면 실업급여 계산기에 반영합니다.</li>
</ul>
<h2>이 사이트의 계산 원칙</h2>
<p>모든 계산식은 근로기준법·최저임금법·고용보험법과 고용노동부·국민연금공단·국민건강보험공단의 공개 기준을 따릅니다. 각 계산기 페이지 아래에 계산식과 근거를 그대로 적어 두었으니 직접 검산해 보세요.</p>
</article>"""
    return head(f"{SITE_NAME} — 주휴수당·알바 월급·퇴직금·실업급여 계산기 (2027 최저임금 반영)",
                "주휴수당, 알바 월급, 최저임금, 퇴직금, 실업급여, 연차, 4대보험, 3.3% 세금을 한곳에서 무료로 계산하세요. 2026·2027 기준 반영.",
                BASE + "/") + body + foot() + "</body></html>"

def simple_page(slug, title, inner):
    return head(f"{title} | {SITE_NAME}", f"{SITE_NAME} {title}", f"{BASE}/{slug}") + \
        f'<p class="crumb"><a href="index.html">홈</a> › {title}</p><h1>{title}</h1><article>{inner}</article>' + foot() + "</body></html>"

ABOUT = f"""<p>{SITE_NAME}는 아르바이트생, 직장인, 소상공인 사장님이 급여와 관련된 숫자를 빠르고 정확하게 확인할 수 있도록 만든 무료 계산기 모음입니다.</p>
<p>주휴수당·최저임금·퇴직금·실업급여처럼 자주 헷갈리는 계산을 법령과 공공기관 기준에 맞춰 정리했고, 각 페이지에 계산식과 근거를 공개합니다.
기준이 바뀌면(최저임금 고시, 보험료율 변경 등) 확인되는 대로 갱신합니다.</p>
<p>계산은 모두 이용자의 브라우저 안에서만 이루어지며, 입력한 금액이나 날짜는 어디에도 전송·저장되지 않습니다.</p>
<p>오류 제보나 계산기 추가 요청은 <a href="{CONTACT_HREF}" rel="noopener">{CONTACT_TEXT}</a>로 보내 주세요.</p>"""

PRIVACY = f"""<p>{SITE_NAME}(이하 '사이트')는 이용자의 개인정보를 중요하게 생각하며, 「개인정보 보호법」을 지킵니다.</p>
<h2>1. 수집하는 개인정보</h2><p>사이트는 회원가입이 없으며 이름·연락처 등 개인정보를 직접 수집하지 않습니다. 계산기에 입력한 값은 이용자의 브라우저에서만 처리되고 서버로 전송되지 않습니다.</p>
<h2>2. 쿠키와 광고</h2><p>사이트는 Google AdSense 광고를 게재할 수 있습니다. Google을 비롯한 제3자 광고 사업자는 쿠키를 사용해 이용자의 이전 방문 기록을 바탕으로 광고를 게재할 수 있습니다.
Google의 광고 쿠키 사용에 대해서는 <a href="https://policies.google.com/technologies/ads" target="_blank" rel="noopener">Google 광고 정책</a>에서 확인할 수 있으며,
<a href="https://adssettings.google.com" target="_blank" rel="noopener">광고 설정</a>에서 맞춤 광고를 끌 수 있습니다. 브라우저 설정에서 쿠키 저장을 거부할 수도 있습니다.</p>
<h2>3. 방문 통계</h2><p>서비스 개선을 위해 페이지 방문 수 등 개인을 식별할 수 없는 통계 정보를 이용할 수 있습니다.</p>
<h2>4. 문의</h2><p>개인정보 관련 문의: <a href="{CONTACT_HREF}" rel="noopener">{CONTACT_TEXT}</a></p>
<h2>5. 시행일</h2><p>이 방침은 {UPDATED}부터 적용됩니다.</p>"""

def man(a):  # 만원 → "4,000만원" / "1억 2,000만원"
    if a >= 10000:
        e, r = divmod(a, 10000)
        return f"{e}억" + (f" {r:,}만원" if r else "원")
    return f"{a:,}만원"

def w(n):
    return f"{int(round(n)):,}원"

def salary_page(i):
    rows = SAL["rows"]; r = rows[i]; a = r["a"]; b = r["base"]; mw = SAL["minWage"]
    slug = f"salary-{a}"; canonical = f"{BASE}/{slug}"
    name = f"연봉 {man(a)}"
    title = f"{name} 실수령액 — 월 {b['net']:,}원 (2026년 세금·4대보험 공제 후)"
    desc = (f"{name}의 2026년 월 실수령액은 {b['net']:,}원입니다(비과세 식대 20만 원, 부양가족 1인 기준). "
            f"국민연금·건강보험·고용보험·소득세 공제 내역과 가족 수별 실수령액, 2027년 변화를 확인하세요.")
    prev_ = rows[i - 1] if i > 0 else None; next_ = rows[i + 1] if i + 1 < len(rows) else None
    diff_no = r["noNontax"] - b["net"]
    ratio = r["hourly"] / mw["2026"]
    f = r["fam"]
    def nb(x, label):
        return f'<a class="tile" href="salary-{x["a"]}.html"><b>{label} {man(x["a"])}</b><span>월 {x["base"]["net"]:,}원</span></a>' if x else ""
    near = [x for x in rows if abs(x["a"] - a) in (500, 1000)]
    faq = [
        (f"{name}이면 한 달에 얼마 받나요?", f"2026년 기준 세전 월급은 {b['gross']:,}원이고, 4대보험과 소득세 {b['deductions']:,}원을 뺀 실수령액은 {b['net']:,}원입니다(부양가족 1인, 비과세 식대 20만 원)."),
        (f"식대 비과세가 없으면 실수령액이 달라지나요?", f"식대 비과세가 없으면 과세급여가 20만 원 늘어 세금과 보험료가 더 붙고, 실수령액은 월 {r['noNontax']:,}원으로 {abs(diff_no):,}원 줄어듭니다."),
        (f"부양가족이 있으면 얼마나 늘어나나요?", f"공제대상가족 4명(8~20세 자녀 2명 포함)이면 소득세가 줄어 월 실수령액이 {f['4c2']:,}원으로 1인 대비 {f['4c2'] - f['1']:,}원 많습니다."),
    ]
    faq_ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": t}} for q, t in faq]}
    bc_ld = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": SITE_NAME, "item": BASE + "/"},
        {"@type": "ListItem", "position": 2, "name": "연봉 실수령액표", "item": f"{BASE}/salary-table"},
        {"@type": "ListItem", "position": 3, "name": name, "item": canonical}]}
    body = f"""<p class="crumb"><a href="index.html">홈</a> › <a href="salary-table.html">연봉 실수령액표</a> › {name}</p>
<h1>{name} 실수령액 (2026년)</h1>
<p class="lead">비과세 식대 월 20만 원, 공제대상가족 1명(본인) 기준입니다. 조건을 바꾸려면 <a href="salary.html">실수령액 계산기</a>를 쓰세요.</p>
<section class="card"><div class="result" style="margin-top:0">
<p class="big">{w(b['net'])}<small>월 실수령액</small></p>
<div class="r"><span>월 급여 (세전)</span><b>{w(b['gross'])}</b></div>
<div class="r"><span>국민연금 4.75%</span><b>−{w(b['np'])}</b></div>
<div class="r"><span>건강보험 3.595%</span><b>−{w(b['hi'])}</b></div>
<div class="r"><span>장기요양보험</span><b>−{w(b['ltc'])}</b></div>
<div class="r"><span>고용보험 0.9%</span><b>−{w(b['ei'])}</b></div>
<div class="r"><span>근로소득세 (간이세액표)</span><b>−{w(b['incomeTax'])}</b></div>
<div class="r"><span>지방소득세</span><b>−{w(b['localTax'])}</b></div>
<div class="r strong"><span>공제 합계 ({b['rate']*100:.1f}%)</span><b>−{w(b['deductions'])}</b></div>
<div class="r strong"><span>연 실수령액</span><b>{w(b['annualNet'])}</b></div>
</div></section>
{ad_slot('top')}
<article>
<h2>가족 수에 따라 달라지는 실수령액</h2>
<div style="overflow-x:auto"><table class="t"><tr><th>공제대상가족</th><th>월 실수령액</th><th>1인 대비</th></tr>
<tr><td>1명 (본인)</td><td>{w(f['1'])}</td><td>–</td></tr>
<tr><td>2명 (배우자 등)</td><td>{w(f['2'])}</td><td>+{f['2']-f['1']:,}원</td></tr>
<tr><td>3명 (자녀 1명 포함)</td><td>{w(f['3c1'])}</td><td>+{f['3c1']-f['1']:,}원</td></tr>
<tr><td>4명 (자녀 2명 포함)</td><td>{w(f['4c2'])}</td><td>+{f['4c2']-f['1']:,}원</td></tr></table></div>
<p>자녀는 8세 이상 20세 이하 기준이며, 2026년 3월부터 바뀐 자녀 공제액(1명 20,830원, 2명 45,830원)을 반영했습니다.</p>
<h2>{name}, 이렇게 볼 수 있어요</h2>
<ul><li>월 209시간 기준 <b>시급으로 환산하면 약 {r['hourly']:,}원</b>으로, 2026년 최저임금(10,320원)의 {ratio:.1f}배입니다.</li>
<li>월급에서 떼이는 돈은 {w(b['deductions'])}로 세전 월급의 <b>{b['rate']*100:.1f}%</b>입니다. 이 중 4대보험이 {w(b['np']+b['hi']+b['ltc']+b['ei'])}, 세금이 {w(b['incomeTax']+b['localTax'])}입니다.</li>
<li>식대 비과세가 없으면 월 실수령액은 {w(r['noNontax'])}입니다.</li>
<li>2027년에는 국민연금 보험료율이 10%로 올라 같은 연봉이라도 월 실수령액이 약 {w(r['y2027'])}({r['y2027']-b['net']:+,}원)이 됩니다.</li></ul>
<h2>계산 기준</h2>
<p>월 급여는 연봉 ÷ 12이며, 4대보험은 비과세를 뺀 금액에 2026년 요율을, 소득세는 국세청 근로소득 간이세액표(소득세법 시행령 별표2)를 적용했습니다. 매달 떼는 소득세는 미리 내는 세금이라 연말정산에서 공제 항목에 따라 돌려받거나 더 낼 수 있습니다.</p>
</article>
{promo() if a <= 4000 else ''}
<h2>자주 묻는 질문</h2>{"".join(f"<details><summary>{html.escape(q)}</summary><p>{html.escape(t)}</p></details>" for q, t in faq)}
{ad_slot('bottom')}
<h2>비슷한 연봉</h2><div class="grid">{nb(prev_, "이전")}{nb(next_, "다음")}{"".join(nb(x, "연봉") for x in near)}</div>
<p class="src">최종 확인: {UPDATED}. 실제 공제액은 회사의 4대보험 신고 보수와 원천징수 비율(80·100·120%)에 따라 조금 달라질 수 있습니다.</p>"""
    return slug, head(title, desc, canonical, [faq_ld, bc_ld]) + body + foot() + "</body></html>"

def salary_table():
    rows = SAL["rows"]
    trs = "".join(f'<tr><td><a href="salary-{r["a"]}.html">{man(r["a"])}</a></td><td>{r["base"]["gross"]:,}</td>'
                  f'<td>{r["base"]["deductions"]:,}</td><td><b>{r["base"]["net"]:,}</b></td><td>{r["fam"]["4c2"]:,}</td></tr>' for r in rows)
    body = f"""<p class="crumb"><a href="index.html">홈</a> › 연봉 실수령액표</p>
<h1>2026 연봉 실수령액표</h1>
<p class="lead">연봉 2,000만 원부터 1억 5,000만 원까지 월 실수령액입니다. 비과세 식대 20만 원 기준이며, 연봉을 누르면 공제 내역을 자세히 볼 수 있습니다.</p>
<div style="overflow-x:auto"><table class="t"><tr><th>연봉</th><th>세전 월급</th><th>공제 합계</th><th>실수령 (1인)</th><th>4인·자녀2</th></tr>{trs}</table></div>
{ad_slot('mid')}
<article><h2>표 보는 법</h2>
<p>'실수령 (1인)'은 공제대상가족이 본인 1명일 때, '4인·자녀2'는 본인·배우자·8~20세 자녀 2명일 때입니다. 4대보험은 2026년 요율, 소득세는 국세청 근로소득 간이세액표를 그대로 적용했습니다.
가족 수나 비과세 금액이 다르면 <a href="salary.html">연봉 실수령액 계산기</a>에서 직접 계산해 보세요.</p></article>"""
    title = "2026 연봉 실수령액표 — 연봉 2천만~1억5천 월 실수령액 한눈에"
    desc = "2026년 연봉별 월 실수령액 표입니다. 4대보험(국민연금 4.75%)과 국세청 간이세액표를 적용한 연봉 2,000만~1억 5,000만 원 실수령액을 한눈에 비교하세요."
    return head(title, desc, f"{BASE}/salary-table") + body + foot() + "</body></html>"

def guide_page(g):
    canonical = f"{BASE}/{g['slug']}"
    art = {"@context": "https://schema.org", "@type": "Article", "headline": g["title"], "description": g["desc"],
           "datePublished": g["date"], "dateModified": UPDATED, "inLanguage": "ko",
           "author": {"@type": "Organization", "name": SITE_NAME}, "publisher": {"@type": "Organization", "name": SITE_NAME},
           "mainEntityOfPage": canonical}
    faq_ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in g["faq"]]}
    allp = PAGES + [TABLE_TILE]
    tools = "".join(f'<a class="tile" href="{r["slug"]}.html"><b>{r["short"]}</b><span>{r["tag"]}</span></a>' for r in allp if r["slug"] in g["tools"])
    others = "".join(f'<li><a href="{o["slug"]}.html">{html.escape(o["title"])}</a></li>' for o in GUIDES if o is not g)
    faq = "".join(f"<details><summary>{html.escape(q)}</summary><p>{html.escape(a)}</p></details>" for q, a in g["faq"])
    body = f"""<p class="crumb"><a href="index.html">홈</a> › <a href="guides.html">가이드</a></p>
<h1>{html.escape(g['title'])}</h1><p class="src">{SITE_NAME} · {g['date']} 작성 · {UPDATED} 확인</p>
<article>{g['body']}</article>{ad_slot('mid')}{promo()}
<h2>자주 묻는 질문</h2>{faq}
<h2>바로 계산해 보기</h2><div class="grid">{tools}</div>
<h2>다른 가이드</h2><ul>{others}</ul>
<p class="src">이 글은 일반적인 정보이며 개별 사안에 대한 법률·세무 자문이 아닙니다.</p>"""
    return head(g["title"], g["desc"], canonical, [art, faq_ld]) + body + foot() + "</body></html>"

def guides_index():
    items = "".join(f'<a class="tile" href="{g["slug"]}.html"><b>{html.escape(g["title"])}</b><span>{html.escape(g["desc"][:60])}…</span></a>' for g in GUIDES)
    body = f"""<p class="crumb"><a href="index.html">홈</a> › 가이드</p><h1>급여·노무 가이드</h1>
<p class="lead">사장님과 근로자가 자주 헷갈리는 급여 규칙을 법령 근거와 함께 정리했습니다.</p><div class="grid">{items}</div>"""
    return head(f"급여·노무 가이드 | {SITE_NAME}", "최저임금, 주휴수당, 임금명세서, 4대보험, 실수령액에 대한 실무 가이드 모음.", f"{BASE}/guides") + body + foot() + "</body></html>"

NOT_FOUND = """<p class="crumb"><a href="index.html">홈</a></p><h1>페이지를 찾을 수 없어요</h1>
<p class="lead">주소가 바뀌었거나 없는 페이지입니다. 아래에서 필요한 계산기를 찾아보세요.</p>"""

def main():
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir()
    for f in ("style.css", "calc.js", "app.js", "ganyi.js"):
        shutil.copy(SRC / f, DIST / f)
    (DIST / "index.html").write_text(build_index(), encoding="utf-8")
    for p in PAGES:
        (DIST / f"{p['slug']}.html").write_text(build_page(p), encoding="utf-8")
    sal_urls = []
    for i in range(len(SAL["rows"])):
        slug, page = salary_page(i)
        (DIST / f"{slug}.html").write_text(page, encoding="utf-8"); sal_urls.append(f"{BASE}/{slug}")
    (DIST / "salary-table.html").write_text(salary_table(), encoding="utf-8")
    for g in GUIDES:
        (DIST / f"{g['slug']}.html").write_text(guide_page(g), encoding="utf-8")
    (DIST / "guides.html").write_text(guides_index(), encoding="utf-8")
    tiles = "".join(f'<a class="tile" href="{p["slug"]}.html"><b>{p["short"]}</b><span>{p["tag"]}</span></a>' for p in PAGES)
    (DIST / "404.html").write_text(head(f"페이지 없음 | {SITE_NAME}", "페이지를 찾을 수 없습니다.", BASE + "/").replace("<head>", "<head><base href=\"" + BASE_PATH + "\">", 1)
        + NOT_FOUND + f'<div class="grid">{tiles}</div>' + foot() + "</body></html>", encoding="utf-8")
    shutil.copy(SRC / "og.png", DIST / "og.png")
    (DIST / "about.html").write_text(simple_page("about", "사이트 소개", ABOUT), encoding="utf-8")
    (DIST / "privacy.html").write_text(simple_page("privacy", "개인정보처리방침", PRIVACY), encoding="utf-8")
    urls = [BASE + "/"] + [f"{BASE}/{p['slug']}" for p in PAGES] + [f"{BASE}/salary-table", f"{BASE}/guides"] + [f"{BASE}/{g['slug']}" for g in GUIDES] + sal_urls + [f"{BASE}/about", f"{BASE}/privacy"]
    (DIST / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
        + "".join(f"<url><loc>{u}</loc><lastmod>{UPDATED}</lastmod></url>" for u in urls) + "</urlset>\n", encoding="utf-8")
    (DIST / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n", encoding="utf-8")
    if args.adsense:
        pub = args.adsense.replace("ca-", "")
        (DIST / "ads.txt").write_text(f"google.com, {pub}, DIRECT, f08c47fec0942fa0\n", encoding="utf-8")
    print(f"built {len(urls)} pages → {DIST}")

main()
