(function(root){
 'use strict';
 const titleKey=t=>String(t||'').normalize('NFKC').toLowerCase().replace(/[^\p{L}\p{N}]/gu,'');
 function identifiers(p){const out=['title:'+titleKey(p.title)];const doi=String(p.doi||'').replace(/^https?:\/\/(?:dx\.)?doi\.org\//i,'').replace(/^doi:\s*/i,'').trim().toLowerCase();if(doi)out.push('doi:'+doi);const arxiv=String(p.url||'').match(/arxiv\.org\/(?:abs|html|pdf)\/([\d.]+)(?:v\d+)?/i);if(arxiv)out.push('arxiv:'+arxiv[1]);for(const a of p.identityAliases||[])if(typeof a==='string')out.push(a);return [...new Set(out.filter(x=>!x.endsWith(':')))];}
 const paperKey=p=>identifiers(p).find(x=>x.startsWith('doi:'))||identifiers(p).find(x=>x.startsWith('arxiv:'))||identifiers(p)[0];
 const samePaper=(a,b)=>identifiers(a).some(id=>identifiers(b).includes(id));
 function effectiveSettings(config,date){const eligible=(config.requests||[]).filter(r=>r.scope==='once'?r.effectiveDate===date:r.effectiveDate<=date);eligible.sort((a,b)=>b.effectiveDate.localeCompare(a.effectiveDate)||b.savedAt.localeCompare(a.savedAt)||b.requestNumber-a.requestNumber);return eligible[0]||config.defaults;}
 function requestBody(settings){return '由网站提交的检索设置。仅仓库所有者提交有效。\n\n<!-- daily-search-settings:v1 -->\n```json\n'+JSON.stringify(settings,null,2)+'\n```';}
 const readingStatus=f=>['unread','read','cite','irrelevant'].includes(f.status)?f.status:(f.read?'read':'unread');
 function rotation(plan,date,kind){const day=s=>Date.parse(s+'T00:00:00Z');const n=Math.floor((day(date)-day(plan.rotations.startDate))/86400000);return n<0?null:plan.rotations[kind][n%plan.rotations[kind].length];}
 function mergeFavorites(current,incoming){const next=[...current];for(const f of incoming)if(!next.some(x=>samePaper(x.paper,f.paper)))next.push(f);return next;}
 const api={titleKey,identifiers,paperKey,samePaper,effectiveSettings,requestBody,readingStatus,rotation,mergeFavorites};if(typeof module!=='undefined'&&module.exports)module.exports=api;root.ResearchCore=api;
})(typeof globalThis!=='undefined'?globalThis:this);
