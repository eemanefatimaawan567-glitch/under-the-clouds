/* Daily Blind Days calendar. Uses only locally bundled verified date records. */
(()=>{
 'use strict';
 let records=[], selected=null;
 const MONTH_EN=['January','February','March','April','May','June','July','August','September','October','November','December'];
 const MONTH_UR=['جنوری','فروری','مارچ','اپریل','مئی','جون','جولائی','اگست','ستمبر','اکتوبر','نومبر','دسمبر'];
 const isUr=()=>document.documentElement.lang==='ur';
 const dateText=s=>{const [y,m,d]=s.split('-').map(Number);return isUr()?`${d} ${MONTH_UR[m-1]} ${y}`:`${d} ${MONTH_EN[m-1]} ${y}`};
 const enStatus={optical_usable:'Optical usable (at least 80% clear)',optical_obstructed:'Optical obstructed (under 80% clear)',no_observation:'No Sentinel-2 observation'};
 const urStatus={optical_usable:'آپٹیکل قابلِ استعمال (کم از کم ۸۰ فیصد صاف)',optical_obstructed:'آپٹیکل متاثرہ (۸۰ فیصد سے کم صاف)',no_observation:'سینٹینل ۲ کا مشاہدہ دستیاب نہیں'};
 function show(date){
  selected=date;
  const item=records.find(x=>x.date===date); if(!item)return;
  document.querySelectorAll('.cal-day').forEach(b=>{const active=b.dataset.date===date;b.classList.toggle('is-selected',active);b.setAttribute('aria-pressed',String(active));});
  const percentage=item.clear_fraction==null?null:(100*item.clear_fraction).toFixed(1)+'%';
  const nisar=item.nisar_pass?(isUr()?' · نثار کا معلوم تحقیقی پاس':' · Known NISAR study pass'):'';
  const coverage=percentage===null?'':(isUr()?` · اندازاً صاف رقبہ: ${percentage}`:` · Estimated clear fraction: ${percentage}`);
  document.getElementById('dailyDateInfo').replaceChildren();
  const title=document.createElement('strong');title.textContent=dateText(date);
  const line=document.createElement('span');line.textContent=(isUr()?urStatus:enStatus)[item.optical_status]+coverage+nisar;
  document.getElementById('dailyDateInfo').append(title,line);
 }
 function draw(){
  const grid=document.getElementById('dailyCalendarGrid');if(!grid)return;
  grid.replaceChildren();
  const months=new Map();
  records.forEach(r=>{const month=r.date.slice(0,7);if(!months.has(month))months.set(month,[]);months.get(month).push(r)});
  for(const [month,days] of months){
   const [year,m]=month.split('-').map(Number);
   const panel=document.createElement('section');panel.className='cal-month';
   const heading=document.createElement('h4');heading.textContent=(isUr()?MONTH_UR:MONTH_EN)[m-1]+' '+year;panel.appendChild(heading);
   const dates=document.createElement('div');dates.className='cal-month-days';
   (isUr()?['ا','پ','م','ب','ج','ہ','ا']:['S','M','T','W','T','F','S']).forEach(label=>{const s=document.createElement('span');s.className='cal-dow';s.textContent=label;dates.appendChild(s)});
   const offset=new Date(Date.UTC(year,m-1,1)).getUTCDay();
   for(let i=0;i<offset;i++){const blank=document.createElement('span');blank.className='cal-empty';dates.appendChild(blank)}
   // Days in range only, with spacers for preceding dates within first month.
   const byDay=new Map(days.map(r=>[Number(r.date.slice(-2)),r]));
   const lastDay=new Date(Date.UTC(year,m,0)).getUTCDate();
   for(let d=1;d<=lastDay;d++){
    const r=byDay.get(d);if(!r){const blank=document.createElement('span');blank.className='cal-empty';dates.appendChild(blank);continue;}
    const btn=document.createElement('button');btn.type='button';btn.className='cal-day'+(r.nisar_pass?' is-nisar':'');btn.dataset.date=r.date;btn.dataset.status=r.optical_status;btn.textContent=String(d);btn.setAttribute('aria-label',dateText(r.date)+' — '+(isUr()?urStatus:enStatus)[r.optical_status]+(r.nisar_pass?' — NISAR':''));
    btn.addEventListener('click',()=>show(r.date));dates.appendChild(btn);
   }
   panel.appendChild(dates);grid.appendChild(panel);
  }
  if(selected)show(selected);
 }
 fetch('data/calendar.json').then(r=>{if(!r.ok)throw Error('Missing calendar');return r.json()}).then(data=>{
  if(!Array.isArray(data)||data.length!==150)throw Error('Unexpected record count');
  const counts={optical_usable:0,optical_obstructed:0,no_observation:0};
  data.forEach(item=>{if(!(item.optical_status in counts))throw Error('Invalid status');counts[item.optical_status]++});
  if(counts.optical_usable!==56||counts.optical_obstructed!==12||counts.no_observation!==82)throw Error('Counts mismatch');
  records=data;draw();
  new MutationObserver(()=>draw()).observe(document.documentElement,{attributes:true,attributeFilter:['lang']});
 }).catch(err=>{
  const grid=document.getElementById('dailyCalendarGrid');if(grid)grid.textContent='Daily calendar data unavailable. Summary metrics above remain available.';
  console.warn('Blind Days calendar:',err.message);
 });
})();
