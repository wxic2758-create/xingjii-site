document.addEventListener('DOMContentLoaded',()=>{
 const b=document.querySelector('.menu-btn'),l=document.querySelector('.nav-links');
 if(b)b.addEventListener('click',()=>{const o=l.classList.toggle('open');b.setAttribute('aria-expanded',o)});
 // 语言提示条：仅提示，不强制跳转
 const bar=document.querySelector('.langbar'),isZh=document.documentElement.lang.startsWith('zh');
 if(bar&&!localStorage.getItem('langHint')&&(navigator.language||'').startsWith('zh')!==isZh){bar.classList.add('show');
  bar.querySelector('button').onclick=()=>{bar.remove();localStorage.setItem('langHint','1')}}
});
