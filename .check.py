import re, json, xml.etree.ElementTree as ET

base = 'C:/Users/Administrator/Projects/hk-daily-newletter/'
idx = open(base + 'index.html', encoding='utf-8').read()
html = open(base + 'posts/2026-11-26-two-tier-split-traps.html', encoding='utf-8').read()
md = open(base + 'posts/2026-11-26-two-tier-split-traps.md', encoding='utf-8').read()
sm = base + 'sitemap.xml'

slug = '2026-11-26-two-tier-split-traps'
title = '注册3家香港公司拆利润？8.25%的优惠税率，你可能一分都拿不到'

# POSTS 首条
m = re.search(r'const POSTS = \[\s*\{ date: "([^"]+)", title: "([^"]+)", slug: "([^"]+)"', idx)
assert m and m.group(1) == '2026-11-26' and m.group(3) == slug, 'POSTS 首条错误'
print('POSTS 首条 OK:', m.group(1), m.group(3))

# 静态卡片首条
card_pos = idx.find('<div id="posts-list">')
first_card = idx.find('<article class="post-card">', card_pos)
card_snippet = idx[first_card:first_card+300]
assert '2026年11月26日' in card_snippet and slug in card_snippet, '静态卡片首条错误'
print('静态卡片首条 OK')

# sitemap 首条
tree = ET.parse(sm)
locs = [e.text for e in tree.getroot().findall('{*}url/{*}loc')]
assert locs[0].endswith(slug + '.html') and locs[0].endswith('2026-11-26'), 'sitemap 首条错误'
print('sitemap 首条 OK, url 总数:', len(locs))

# JSON-LD
blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S)
for i, b in enumerate(blocks):
    json.loads(b)
print('JSON-LD 通过, 共', len(blocks), '块')

# answer-capsule 在第一个 h2 前
capsule_pos = html.find('answer-capsule')
h2_pos = html.find('<h2>')
assert 0 < capsule_pos < h2_pos, 'answer-capsule 位置错误'
print('answer-capsule 位于 h1 后首个 h2 前 OK')

# 标题无半角双引号
assert '"' not in title, '标题含半角双引号'
print('标题无半角双引号 OK')

# 字数
body = md[md.index('\n\n')+2:]
print('正文汉字数:', len(re.findall(r'[\u4e00-\u9fff]', body)))
meta = re.search(r'<meta name="description" content="([^"]+)"', html).group(1)
print('meta 汉字数:', len(re.findall(r'[\u4e00-\u9fff]', meta)))
og = re.search(r'og:description" content="([^"]+)"', html).group(1)
assert og == meta, 'og:description 与 meta 不同步'
print('meta/og 同步 OK')
cap = re.search(r'<div class="answer-capsule">\s*<p>([^<]+)</p>', html).group(1)
print('胶囊汉字数:', len(re.findall(r'[\u4e00-\u9fff]', cap)))
print('全部校验通过 ✅')
