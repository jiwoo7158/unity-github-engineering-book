(function(){
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
})();