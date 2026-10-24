"""Create one self-contained HTML book (no network, no external assets)."""
from pathlib import Path
import html, json, re, base64
import mistune, yaml

root=Path(__file__).resolve().parents[1]
docs=root/'docs'
nav=yaml.safe_load((root/'mkdocs.yml').read_text(encoding='utf-8'))['nav']

def flatten(items,group=''):
  for x in items:
    for key,v in x.items():
      if isinstance(v,str):yield (group,key,v)
      else:yield from flatten(v,key)
records=list(flatten(nav))
# Resolve local chapter links to the single-file edition's section anchors.
chapter_by_file = {(docs / rec[2]).resolve(): f'chapter-{i+1}' for i,rec in enumerate(records)}
base_css=(root/'site/assets/style.css').read_text(encoding='utf-8')
# The single-file edition intentionally shows all chapters in one continuous view.
extra_css='''
.shell{grid-template-columns:285px minmax(0,1fr)}main{max-width:1110px}.sidebar{scrollbar-width:thin}.article{margin-bottom:26px;scroll-margin-top:90px}.article h1{margin-top:0}.book-heading{padding:40px 8px 18px}.book-heading h1{font-size:32px}.toc{display:none}.intro{text-align:left;font-size:14px;color:var(--muted);max-width:700px}.sidebar a{font-size:13px}.chapter-nav{border-radius:10px;padding:10px 13px;background:var(--soft);margin-bottom:12px}.chapter-nav h2{font-size:13px;margin:0 0 8px}.chapter-nav a{display:block;padding:3px 0;font-size:12px;color:var(--accent)}@media print{.article{page-break-before:always}.book-heading{page-break-after:always}}@media(max-width:850px){.shell{display:block}.book-heading{padding:15px}.article{margin:10px 0 23px}}
'''
class Renderer(mistune.HTMLRenderer):
  def __init__(self):super().__init__(escape=False);self.seq=0
  def heading(self,text,level,**kwargs):
    self.seq+=1;anchor=f'heading-{self.seq}'
    return f'<h{level} id="{anchor}">{text}</h{level}>\n'

def convert_admonitions(s):
  lines=s.splitlines();out=[];i=0
  while i<len(lines):
    m=re.match(r'^!!!\s+(\w+)(?:\s+"([^"]+)")?',lines[i])
    if m:
      out.append('> **'+(m.group(2) or m.group(1))+'**');i+=1
      while i<len(lines) and (lines[i].startswith('    ') or not lines[i].strip()):
        out.append('> '+lines[i][4:] if lines[i].startswith('    ') else '>');i+=1
    else:out.append(lines[i]);i+=1
  return '\n'.join(out)
renderer=Renderer();parse=mistune.create_markdown(renderer=renderer,plugins=['table','strikethrough','task_lists','def_list'])
sections=[];sidebar=[];groups=[];seen=set();search=[]
for i,(group,title,md) in enumerate(records):
  key='chapter-'+str(i+1)
  if group not in seen:
    seen.add(group);sidebar.append('<div class="sidebar-group">'+html.escape(group or '소개')+'</div>')
  sidebar.append(f'<a href="#{key}">{html.escape(title)}</a>')
  content=(docs/md).read_text(encoding='utf-8')
  render=parse(convert_admonitions(content))
  def remap_single_doc_link(match):
    src=match.group(2)
    if src.startswith(('https://','http://','#','mailto:','data:','/')):
      return match.group(0)
    rawpath,sep,fragment=src.partition('#')
    if not rawpath.endswith('.md'):
      return match.group(0)
    path=(docs/Path(md).parent/rawpath).resolve()
    section=chapter_by_file.get(path)
    return match.group(1)+('#'+section if section else src)+match.group(3)
  render=re.sub(r'(<a\s+href=")(.*?)(")',remap_single_doc_link,render)
  # Inline SVGs as data URIs so this single HTML remains completely portable,
  # with working diagrams even from file:// and without JavaScript or Internet.
  def embed_book_diagram(match):
    relative_src=match.group(2)
    resolved=(docs/Path(md).parent/relative_src).resolve()
    if not resolved.is_relative_to(docs.resolve()) or not resolved.is_file():
      raise ValueError(f'Invalid diagram path {md}: {relative_src}')
    encoded=base64.b64encode(resolved.read_bytes()).decode('ascii')
    return match.group(1)+'data:image/svg+xml;base64,'+encoded+match.group(3)
  render=re.sub(r'(<img\s+src=")(.*?\.svg)("[^>]*>)',embed_book_diagram,render)
  render=re.sub(r'<img (?=[^>]*\bsrc=\"data:image/svg\+xml;base64,)', '<img class="book-diagram" ', render)
  sections.append(f'<article class="article" id="{key}"><div class="meta">{html.escape(group or "시작하기")} · {i+1} / {len(records)}</div>{render}</article>')
  search.append({'id':key,'title':title,'group':group,'text':re.sub(r'\s+',' ',re.sub(r'```[\s\S]*?```','',content))[:26000]})
search_js='''
const searchIndex = INDEX_HERE;
const input=document.getElementById('search'), results=document.getElementById('search-results');
input.addEventListener('input',()=>{const q=input.value.trim().toLowerCase();if(q.length<2){results.style.display='none';return;}
 const terms=q.split(/\\s+/);const hits=searchIndex.map(e=>({e,score:terms.reduce((n,t)=>n+(e.title.toLowerCase().includes(t)?8:0)+(e.text.toLowerCase().includes(t)?1:0),0)})).filter(x=>x.score>=terms.length).sort((a,b)=>b.score-a.score).slice(0,14);
 results.innerHTML=hits.map(({e})=>{const a=document.createElement('a');a.href='#'+e.id;a.textContent=e.title;a.addEventListener('click',()=>results.style.display='none');return a.outerHTML;}).join('')||'<div style="padding:16px">검색 결과가 없습니다.</div>';results.style.display='block';});
input.addEventListener('keydown',e=>{if(e.key==='Escape')results.style.display='none';});
const b=document.querySelector('.mobile-toggle');b.addEventListener('click',()=>document.body.classList.toggle('nav-open'));
document.querySelectorAll('.sidebar a').forEach(a=>a.addEventListener('click',()=>document.body.classList.remove('nav-open')));
window.addEventListener('scroll',()=>{const d=document.documentElement;document.querySelector('.reading').style.width=(100*d.scrollTop/Math.max(1,d.scrollHeight-d.clientHeight))+'%';},{passive:true});
'''.replace('INDEX_HERE',json.dumps(search,ensure_ascii=False))

output=f'''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Unity 개발자를 위한 GitHub 실무 교과서</title><style>{base_css}\n{extra_css}</style></head><body><div class="reading"></div><header><button class="mobile-toggle" aria-label="목차 열기">☰</button><a class="logo" href="#top"><span class="brand-dot"></span>Unity × GitHub 실무 교과서</a><span class="note">단일 HTML 전자책 · 인터넷 없이 열기</span><input id="search" autocomplete="off" placeholder="책 전체 검색 (2글자 이상)" aria-label="교재 검색"></header><div class="search-results" id="search-results"></div><div class="shell"><aside class="sidebar">{''.join(sidebar)}</aside><main><div class="book-heading" id="top"><h1>Unity 개발자를 위한 GitHub 실무 교과서</h1><p class="intro">Git·GitHub·Unity 버전 관리·팀 협업·Issues·Projects·Actions·자동 테스트·빌드·문서·AI 협업을 소규모 게임 개발의 소프트웨어공학 흐름으로 연결합니다. 2026년 10월 24일 보강 원고. 본문 목차를 선택하거나 Ctrl+F로 검색하세요.</p><div class="chapter-nav"><h2>읽는 방법</h2><a href="#chapter-1">책 소개부터 읽기 →</a><a href="#chapter-2">01. Git 기본 원리부터 읽기 →</a><a href="javascript:window.print()">브라우저에서 인쇄 / PDF로 저장</a></div></div>{''.join(sections)}<p class="meta">끝 · GitHub·Unity 공식 최신 문서 및 사용 중인 환경에서 세부 기능을 재확인하세요.</p></main></div><script>{search_js}</script></body></html>'''
output=output.replace('href="javascript:window.print()"','href="#top" onclick="window.print();return false"')
out=root/'single-book.html'
out.write_text(output,encoding='utf-8')
print(out, len(output), 'characters')
