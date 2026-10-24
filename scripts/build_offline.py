"""Create a bundled offline reader and a single long Markdown edition.
Dependencies: pip install mistune PyYAML (MkDocs is not needed here).
Run from the repository root: python scripts/build_offline.py
"""
from pathlib import Path
from urllib.parse import unquote
import html, json, re
import shutil
import mistune
import yaml

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / 'docs'
SITE = ROOT / 'site'
ASSETS = SITE / 'assets'
ASSETS.mkdir(parents=True, exist_ok=True)
# Copy the pre-rendered diagrams into the offline site. Unlike MkDocs,
# this custom generator does not automatically copy docs/assets/.
for source in (DOCS/'assets').rglob('*.svg'):
    destination=SITE/'assets'/source.relative_to(DOCS/'assets')
    destination.parent.mkdir(parents=True,exist_ok=True)
    shutil.copy2(source,destination)

config = yaml.safe_load((ROOT / 'mkdocs.yml').read_text(encoding='utf-8'))

def flatten_nav(items, group=''):
    records=[]
    for item in items:
        for name, dest in item.items():
            if isinstance(dest, str):
                records.append(dict(group=group, title=name, md=dest, html=dest.removesuffix('.md')+'.html'))
            else:
                records.extend(flatten_nav(dest, name))
    return records

pages = flatten_nav(config['nav'])
missing = [p['md'] for p in pages if not (DOCS/p['md']).is_file()]
assert not missing, f'Missing docs: {missing}'

markdown = mistune.create_markdown(escape=False, plugins=['table','strikethrough','task_lists','def_list'])

# Convert MkDocs admonitions into standard blockquotes in the offline version.
def offline_markdown(raw):
    lines = raw.splitlines()
    out=[]
    i=0
    while i<len(lines):
        line=lines[i]
        m=re.match(r'^!!!\s+(\w+)(?:\s+"([^"]+)")?\s*$',line)
        if m:
            title=m.group(2) or m.group(1)
            out.append(f'> **{title}**')
            i+=1
            while i<len(lines) and (lines[i].startswith('    ') or not lines[i].strip()):
                if lines[i].startswith('    '):
                    out.append('> '+lines[i][4:])
                else:
                    out.append('>')
                i+=1
            continue
        out.append(line)
        i+=1
    return '\n'.join(out)+'\n'

# Name independent anchor slugs: main heading links stay based on sections rather than id.
def heading_ids(src):
    result=[]
    for level,label in re.findall(r'^(#{2,4})\s+(.+)$',src,flags=re.M):
        clean=re.sub(r'[`*\[\]]','',label).strip()
        result.append((len(level),clean))
    return result

class AnchorRenderer(mistune.HTMLRenderer):
    def __init__(self):
        super().__init__(escape=False)
        self.headings=[]
        self.heading_count=0
    def heading(self,text,level,**attrs):
        self.heading_count+=1
        hid=f'section-{self.heading_count}'
        title=re.sub(r'<[^>]*>', '', text)
        self.headings.append((level,title,hid))
        return f'<h{level} id="{hid}">{text}<a class="heading-link" href="#{hid}" aria-label="이 단락 링크">#</a></h{level}>\n'

style = r'''/* Offline reader: 100% local, system fonts */
:root{--bg:#f7f9fc;--surface:#fff;--text:#17263a;--muted:#617188;--border:#dce3ef;--accent:#2869af;--soft:#e9f2fc;--code:#f1f5fa;--shadow:0 10px 25px rgba(30,49,77,.06)}
*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:var(--bg);font-family:ui-sans-serif,system-ui,-apple-system,"Segoe UI","Malgun Gothic",sans-serif;color:var(--text);line-height:1.83;font-size:15px}
a{color:var(--accent);text-decoration:none}a:hover{text-decoration:underline}header{position:sticky;top:0;z-index:30;height:60px;border-bottom:1px solid var(--border);background:var(--surface);display:flex;align-items:center;gap:20px;padding:0 24px;box-shadow:0 2px 8px rgba(30,49,77,.03)}header .logo{font-weight:750;color:var(--text);font-size:16px;white-space:nowrap}.brand-dot{width:12px;height:12px;border-radius:4px;background:var(--accent);display:inline-block;margin-right:9px}header .note{color:var(--muted);font-size:12px}#search{width:min(440px,43vw);padding:9px 14px;border:1px solid var(--border);border-radius:9px;background:var(--bg);font:inherit;font-size:13px;margin-left:auto;outline-color:var(--accent)}
.search-results{position:fixed;right:24px;top:56px;width:min(450px,calc(100vw - 48px));background:var(--surface);border:1px solid var(--border);border-radius:13px;box-shadow:0 16px 40px rgba(29,45,63,.18);display:none;z-index:100;max-height:70vh;overflow:auto}.search-results a{display:block;padding:11px 16px;border-bottom:1px solid var(--border);color:var(--text)}.search-results a:hover{background:var(--soft);text-decoration:none}.search-results small{display:block;color:var(--muted);line-height:1.4}
.shell{display:grid;grid-template-columns:270px minmax(0,1fr) 200px;max-width:1600px;margin:auto;min-height:calc(100vh - 60px)}aside.sidebar{padding:24px 12px 26px 20px;border-right:1px solid var(--border);height:calc(100vh - 60px);overflow:auto;position:sticky;top:60px}.sidebar-group{font-size:11px;font-weight:800;letter-spacing:.02em;color:var(--muted);margin:19px 12px 6px}.sidebar a{display:block;padding:7px 11px;color:#435470;font-size:13px;line-height:1.5;border-radius:7px;margin-bottom:3px}.sidebar a:hover,.sidebar a.active{background:var(--soft);color:#174b85;text-decoration:none;font-weight:650}
main{min-width:0;padding:40px clamp(24px,4vw,72px) 64px;max-width:1050px;width:100%;margin:auto}.article{background:var(--surface);padding:clamp(24px,4vw,60px);border:1px solid var(--border);border-radius:13px;box-shadow:var(--shadow)}.article h1{font-size:clamp(26px,3vw,34px);line-height:1.3;letter-spacing:-.035em;margin:0 0 28px}.article h2{font-size:23px;margin:50px 0 18px;line-height:1.45;padding-bottom:8px;border-bottom:1px solid var(--border)}.article h3{font-size:18px;margin:28px 0 12px;line-height:1.45}.article h4{font-size:16px;margin:23px 0 10px}.article p{margin:13px 0}.article strong{font-weight:750}.article li{margin:6px 0}.article ul,.article ol{padding-left:24px}.article blockquote{border-left:4px solid #67a2dd;background:var(--soft);border-radius:0 8px 8px 0;padding:12px 18px;margin:22px 0}.article blockquote p{margin:0 0 6px}.article code{background:var(--code);border-radius:4px;padding:2px 5px;font-size:.88em;word-wrap:break-word}.article pre{background:#182438;color:#e5eef9;border-radius:10px;padding:19px 21px;overflow:auto;font-size:13px;line-height:1.6}.article pre code{background:transparent;color:inherit;padding:0;word-wrap:normal}.article table{width:100%;border-collapse:collapse;font-size:13.5px;display:block;overflow-x:auto;margin:22px 0}.article th,.article td{border-bottom:1px solid var(--border);padding:9px 12px;text-align:left;vertical-align:top;min-width:80px}.article th{background:var(--soft);font-weight:700}.article img{max-width:100%}.article img.book-diagram{display:block;width:auto;max-width:100%;height:auto;margin:22px auto;padding:14px;background:#f9fbff;border:1px solid var(--border);border-radius:12px}.article hr{border:0;border-top:1px solid var(--border);margin:32px 0}.heading-link{font-weight:400;color:#8eabc5;margin-left:10px;font-size:.65em;visibility:hidden}.article h1:hover .heading-link,.article h2:hover .heading-link,.article h3:hover .heading-link{visibility:visible}
.toc{padding:32px 13px;border-left:1px solid var(--border);position:sticky;top:60px;height:calc(100vh - 60px);overflow:auto}.toc-title{font-size:12px;font-weight:800;margin-bottom:12px;color:var(--muted)}.toc a{font-size:12px;line-height:1.5;color:var(--muted);display:block;margin:8px 0;padding:3px 0}.toc a.level3{padding-left:12px}.toc a.level4{padding-left:22px}.toc a:hover{color:var(--accent)}.bottom-nav{display:flex;justify-content:space-between;gap:20px;margin:24px 0}.bottom-nav a{border:1px solid var(--border);background:var(--surface);padding:12px 16px;border-radius:10px;flex:1}.bottom-nav a:last-child{text-align:right}.meta{color:var(--muted);font-size:12px;margin-bottom:14px}.mobile-toggle{display:none}.reading{position:fixed;z-index:40;top:59px;left:0;height:2px;background:var(--accent);width:0;pointer-events:none}
@media(max-width:1250px){.shell{grid-template-columns:250px minmax(0,1fr)}.toc{display:none}}@media(max-width:850px){header{padding:0 14px;gap:8px}header .logo{font-size:13px}header .note{display:none}#search{width:40vw}.mobile-toggle{display:block;border:1px solid var(--border);background:var(--surface);border-radius:7px;padding:4px 8px;cursor:pointer}.shell{display:block}.sidebar{position:fixed!important;z-index:20;left:0;top:60px;background:var(--surface);width:280px;transform:translateX(-100%);transition:.2s;box-shadow:var(--shadow)}body.nav-open .sidebar{transform:translateX(0)}main{padding:15px 12px 40px}.article{padding:23px 19px;border-radius:9px}.article h2{font-size:20px}.bottom-nav{margin:14px 0}}@media print{header,.sidebar,.toc,.bottom-nav,.reading{display:none!important}.shell{display:block}main{max-width:none;padding:0}.article{border:0;box-shadow:none}body{background:white;color:black}.article pre{white-space:pre-wrap}}
'''
(ASSETS/'style.css').write_text(style,encoding='utf-8')

js = r'''(function(){
 const input=document.querySelector('#search');const results=document.querySelector('#search-results');
 const list=window.BOOK_SEARCH||[];
 const escape=s=>s.replace(/[&<>\"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
 function search(q){if(!results)return; q=q.trim().toLocaleLowerCase();if(q.length<2){results.style.display='none';return;}
 const words=q.split(/\s+/);const matches=list.map(p=>({p,score:words.reduce((n,w)=>n+(p.title.toLocaleLowerCase().includes(w)?8:0)+(p.group.toLocaleLowerCase().includes(w)?2:0)+(p.text.toLocaleLowerCase().includes(w)?1:0),0)})).filter(x=>x.score>=words.length).sort((a,b)=>b.score-a.score).slice(0,12);
 results.innerHTML=matches.length?matches.map(x=>`<a href="${window.SITE_ROOT}${x.p.html}"><b>${escape(x.p.title)}</b><small>${escape(x.p.group)}</small></a>`).join(''):'<div style="padding:16px;color:#667">검색 결과가 없습니다.</div>';results.style.display='block';}
 if(input){input.addEventListener('input',e=>search(e.target.value));input.addEventListener('keydown',e=>{if(e.key==='Escape'){results.style.display='none';input.blur();}});}
 document.addEventListener('click',e=>{if(results&&!results.contains(e.target)&&e.target!==input)results.style.display='none';});
 const btn=document.querySelector('.mobile-toggle');if(btn)btn.addEventListener('click',()=>document.body.classList.toggle('nav-open'));
 const bar=document.querySelector('.reading');if(bar)window.addEventListener('scroll',()=>{const d=document.documentElement;bar.style.width=(100* d.scrollTop/Math.max(1,d.scrollHeight-d.clientHeight))+'%';},{passive:true});
})();'''
(ASSETS/'search.js').write_text(js,encoding='utf-8')

search_records=[]
long_parts=['# Unity 개발자를 위한 GitHub 실무 교과서 — 통합 Markdown판\n', '> MkDocs 원고 12개 기본 장·3개 보강 장과 부록을 하나의 파일로 모은 읽기·인쇄용 파일.\n']
for p in pages:
    source=(DOCS/p['md']).read_text(encoding='utf-8')
    cleaned=offline_markdown(source)
    first_h1=re.search(r'^#\s+(.+)$',source,re.M)
    title=first_h1.group(1) if first_h1 else p['title']
    text=re.sub(r'```[\s\S]*?```','',source)
    text=re.sub(r'[#>*`\[\]()|\-]',' ',text)
    search_records.append(dict(title=title,group=p['group'] or '시작하기',html=p['html'],text=re.sub(r'\s+',' ',text)[:26000]))
    # The consolidated Markdown lives at the repository root; resolve image
    # paths against each source chapter so diagram links work from BOOK.md.
    def remap_book_image(match):
        path=match.group(2)
        if path.startswith(('https://','http://','data:','/')):
            return match.group(0)
        resolved=(DOCS/Path(p['md']).parent/unquote(path)).resolve()
        if not resolved.is_relative_to(ROOT) or not resolved.exists():
            raise ValueError(f'Book image reference missing: {p["md"]}: {path}')
        return match.group(1)+resolved.relative_to(ROOT).as_posix()+match.group(3)
    book_source=re.sub(r'(!\[[^\]]*\]\()([^\)]+)(\))',remap_book_image,source)
    # In the consolidated book, links originating in docs/ must be resolved
    # against that chapter and then expressed relative to repository root.
    def remap_book_md_link(match):
        href=match.group(2)
        if href.startswith(('https://','http://','#','mailto:','data:','/')):
            return match.group(0)
        path,sep,fragment=href.partition('#')
        if not path.endswith('.md'):
            return match.group(0)
        target=(DOCS/Path(p['md']).parent/unquote(path)).resolve()
        if not target.is_relative_to(DOCS.resolve()) or not target.is_file():
            raise ValueError(f'Book link missing: {p["md"]}: {href}')
        return match.group(1)+target.relative_to(ROOT).as_posix()+(sep+fragment if sep else '')+match.group(3)
    book_source=re.sub(r'(?<!!)(\[[^\]]+\]\()([^\)]+)(\))',remap_book_md_link,book_source)
    long_parts.append('\n---\n\n'+book_source+'\n')
(ROOT/'BOOK.md').write_text('\n'.join(long_parts),encoding='utf-8')

(ASSETS/'index-data.js').write_text('window.BOOK_SEARCH='+json.dumps(search_records,ensure_ascii=False)+';',encoding='utf-8')

# The Markdown online links to other .md docs can be translated to html if present.
for idx,p in enumerate(pages):
    raw=offline_markdown((DOCS/p['md']).read_text(encoding='utf-8'))
    renderer=AnchorRenderer()
    parser=mistune.create_markdown(renderer=renderer,plugins=['table','strikethrough','task_lists','def_list'])
    content=parser(raw)
    content=re.sub(r'<img (?=[^>]*\bsrc=\"[^\"]+\.svg\")', '<img class=\"book-diagram\" ', content)
    from_root='../' * p['html'].count('/')
    # replace only relative .md links referenced in article
    def linkreplace(match):
        url=match.group(1)
        if url.startswith(('https://','http://','#','mailto:')):return match.group(0)
        return 'href="'+url.replace('.md','.html')+'"'
    content=re.sub(r'href="([^"]+)"',linkreplace,content)
    groups=[]
    previous=None
    for other in pages:
        if other['group']!=previous:
            groups.append(f'<div class="sidebar-group">{html.escape(other["group"] or "소개")}</div>')
            previous=other['group']
        active=' active' if other is p else ''
        groups.append(f'<a class="{active}" href="{from_root}{other["html"]}">{html.escape(other["title"])}</a>')
    toc=[]
    for level,header,hid in renderer.headings:
        if level>=2:
            toc.append(f'<a class="level{level}" href="#{hid}">{html.escape(re.sub(r"<[^>]+>","",header))}</a>')
    before=pages[idx-1] if idx else None
    after=pages[idx+1] if idx+1<len(pages) else None
    navlinks=(f'<a href="{from_root}{before["html"]}">← {html.escape(before["title"])}</a>' if before else '<span></span>')+(f'<a href="{from_root}{after["html"]}">{html.escape(after["title"])} →</a>' if after else '<span></span>')
    page=f'''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="light"><title>{html.escape(title)} · Unity GitHub 실무 교과서</title><link rel="stylesheet" href="{from_root}assets/style.css"></head><body>
    <div class="reading"></div><header><button class="mobile-toggle" aria-label="목차 열기">☰</button><a class="logo" href="{from_root}index.html"><span class="brand-dot"></span>Unity × GitHub 실무 교과서</a><span class="note">소규모 게임 개발 · 소프트웨어공학</span><input id="search" autocomplete="off" placeholder="전체 교재 검색 (2글자 이상)" aria-label="책 검색"></header>
    <div class="search-results" id="search-results"></div><div class="shell"><aside class="sidebar">{''.join(groups)}</aside><main><div class="meta">{html.escape(p['group'] or '시작하기')} · 2026년 10월 24일 보강</div><article class="article">{content}</article><nav class="bottom-nav">{navlinks}</nav></main><aside class="toc"><div class="toc-title">이 페이지에서</div>{''.join(toc)}</aside></div>
    <script>window.SITE_ROOT={json.dumps(from_root)};</script><script src="{from_root}assets/index-data.js"></script><script src="{from_root}assets/search.js"></script></body></html>'''
    dest=SITE/p['html']
    dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(page,encoding='utf-8')

print('Generated:',len(pages),'HTML chapters /',len((ROOT/'BOOK.md').read_text(encoding='utf-8')),'characters consolidated Markdown')
