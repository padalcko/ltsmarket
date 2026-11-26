(() => {
  'use strict';
  const lang = document.documentElement.lang || 'pl';
  const locale = {pl:'pl-PL',ru:'ru-RU',en:'en-GB'}[lang] || 'pl-PL';
  const t = {
    pl:{invalid:'Wprowadź nieujemne, poprawne liczby.',complete:'Wszystkie kroki ukończone.',done:'Ukończono',unreachable:'Próg nieosiągalny przy tej cenie i koszcie zmiennym',noPayback:'Brak dodatnich środków na zwrot',months:'mies.',treatments:'zabiegów/mies.',available:'Dodatnie środki',negative:'Brak dodatnich środków',chart:'Przychód, nadwyżka operacyjna i dostępne środki przy {n} zabiegach dziennie.'},
    ru:{invalid:'Введите корректные неотрицательные числа.',complete:'Все шаги выполнены.',done:'Выполнено',unreachable:'Безубыточность недостижима при этой цене и переменных расходах',noPayback:'Нет положительного остатка для окупаемости',months:'мес.',treatments:'процедур/мес.',available:'Положительный остаток',negative:'Нет положительного остатка',chart:'Выручка, операционный остаток и доступные средства при {n} процедурах в день.'},
    en:{invalid:'Enter valid non-negative numbers.',complete:'All steps completed.',done:'Completed',unreachable:'Break-even is unreachable at this price and variable cost',noPayback:'No positive cash available for payback',months:'months',treatments:'treatments/month',available:'Positive cash',negative:'No positive cash',chart:'Revenue, operating surplus and available cash at {n} treatments per day.'}
  }[lang] || {};
  const money = new Intl.NumberFormat(locale,{style:'currency',currency:'PLN',maximumFractionDigits:0});
  const number = new Intl.NumberFormat(locale,{maximumFractionDigits:1});
  const scenarios = [
    [35000,3000,3000,2000,2000,1500,1500,12000],
    [70000,6000,12000,5000,3000,4000,2000,24000],
    [130000,12000,30000,10000,6000,8000,4000,40000]
  ];
  const defaults = [60000,200,3,22,20,4000,0];
  const fixedDefaults = [2000,2500,600,1000,300,150,500,450];
  const read = (elements) => {
    const values = elements.map(el => Number(el.value));
    return values.every((v,i) => elements[i].value.trim() !== '' && Number.isFinite(v) && v >= 0 && (!elements[i].max || v <= Number(elements[i].max))) ? values : null;
  };
  const checklist = document.querySelector('[data-checklist]');
  if (checklist) {
    const boxes = [...checklist.querySelectorAll('[data-step]')];
    const key = 'ltsmarket-business-startup-checklist-v1';
    try {
      const saved = JSON.parse(localStorage.getItem(key) || '[]');
      if (Array.isArray(saved)) boxes.forEach(box => {box.checked = saved.includes(box.dataset.step);});
    } catch (_) { /* Storage can be unavailable. */ }
    const update = () => {
      const checked = boxes.filter(box => box.checked);
      const percent = Math.round(100 * checked.length / boxes.length);
      checklist.querySelector('[data-check-status]').textContent = checked.length === boxes.length ? t.complete : t.done + ': ' + checked.length + '/' + boxes.length + ' (' + percent + '%)';
      checklist.querySelector('progress').value = checked.length;
      boxes.forEach(box => box.closest('li').classList.toggle('is-done',box.checked));
      try {localStorage.setItem(key,JSON.stringify(checked.map(box => box.dataset.step)));} catch (_) {}
    };
    boxes.forEach(box => box.addEventListener('change',update));
    checklist.querySelector('[data-check-reset]').addEventListener('click',() => {boxes.forEach(box => {box.checked=false;});update();});
    update();
  }
  const costTool = document.querySelector('[data-cost-tool]');
  const profitTool = document.querySelector('[data-profit-tool]');
  let currentCost = 60000;
  const costInputs = costTool ? [...costTool.querySelectorAll('[data-cost]')] : [];
  const renderCost = () => {
    const values=read(costInputs);
    costTool.querySelector('[data-cost-error]').textContent = values ? '' : t.invalid;
    if (!values) return;
    currentCost=values.reduce((a,b)=>a+b,0);
    const equip=values[0], other=currentCost-equip;
    costTool.querySelector('[data-cost-total]').textContent=money.format(currentCost);
    costTool.querySelector('[data-cost-other]').textContent=money.format(other);
    costTool.querySelector('[data-cost-share]').textContent=currentCost ? number.format(100*equip/currentCost)+'%' : '0%';
    costTool.querySelector('[data-cost-equipment]').style.width=currentCost ? 100*equip/currentCost+'%' : '0%';
    costTool.querySelector('[data-cost-rest]').style.width=currentCost ? 100*other/currentCost+'%' : '0%';
  };
  if (costTool) {
    const select = index => {
      costInputs.forEach((input,i) => {input.value=scenarios[index][i];});
      costTool.querySelectorAll('[data-scenario]').forEach(button => button.setAttribute('aria-pressed',String(Number(button.dataset.scenario)===index)));
      renderCost();
    };
    costTool.querySelectorAll('[data-scenario]').forEach(button=>button.addEventListener('click',()=>select(Number(button.dataset.scenario))));
    costInputs.forEach(input=>input.addEventListener('input',renderCost));
    costTool.querySelector('[data-cost-reset]').addEventListener('click',()=>select(0));
    costTool.querySelector('[data-transfer]').addEventListener('click',()=>{
      if (!read(costInputs) || !profitTool) return;
      profitTool.querySelector('[data-profit="0"]').value=currentCost;
      renderProfit();
      profitTool.scrollIntoView({behavior:window.matchMedia('(prefers-reduced-motion: reduce)').matches?'instant':'smooth',block:'start'});
      profitTool.querySelector('[data-profit="0"]').focus({preventScroll:true});
    });
    renderCost();
  }
  const profitInputs=profitTool ? [...profitTool.querySelectorAll('[data-profit]')] : [];
  const fixedInputs=profitTool ? [...profitTool.querySelectorAll('[data-fixed]')] : [];
  const chart=document.querySelector('[data-chart]');
  const setResult=(i,value,negative=false)=>{
    const el=profitTool.querySelector('[data-result="'+i+'"]');
    el.textContent=value;
    el.dataset.negative=String(negative);
  };
  const plot=(v,fixed)=>{
    if (!chart) return;
    const [initial,price,perDay,days,variable,owner,financing]=v;
    const maxX=Math.max(10,Math.ceil(perDay));
    const series={revenue:[],surplus:[],cash:[]};
    for(let x=0;x<=maxX;x++){
      const revenue=x*days*price;
      const surplus=revenue-x*days*variable-fixed;
      series.revenue.push([x,revenue]);
      series.surplus.push([x,surplus]);
      series.cash.push([x,surplus-owner-financing]);
    }
    const all=Object.values(series).flat().map(point=>point[1]);
    const minY=Math.min(0,...all),maxY=Math.max(1,...all),span=maxY-minY;
    const sx=x=>58+552*x/maxX,sy=y=>305-260*(y-minY)/span;
    const grid=chart.querySelector('[data-chart-grid]');
    grid.replaceChildren();
    for(let i=0;i<=4;i++){
      const value=minY+span*i/4;
      const line=document.createElementNS('http://www.w3.org/2000/svg','line');
      line.setAttribute('x1','58');line.setAttribute('x2','610');line.setAttribute('y1',sy(value));line.setAttribute('y2',sy(value));
      line.setAttribute('class',Math.abs(value)<span/8?'guide-zero':'guide-grid-line');
      grid.append(line);
      const label=document.createElementNS('http://www.w3.org/2000/svg','text');
      label.setAttribute('x','52');label.setAttribute('y',sy(value)+4);label.setAttribute('text-anchor','end');
      label.textContent=number.format(Math.round(value));grid.append(label);
    }
    if(minY<0 && maxY>0){
      const zero=document.createElementNS('http://www.w3.org/2000/svg','line');
      zero.setAttribute('x1','58');zero.setAttribute('x2','610');zero.setAttribute('y1',sy(0));zero.setAttribute('y2',sy(0));zero.setAttribute('class','guide-zero');grid.append(zero);
    }
    for(let x=0;x<=maxX;x+=Math.max(1,Math.ceil(maxX/10))){
      const label=document.createElementNS('http://www.w3.org/2000/svg','text');
      label.setAttribute('x',sx(x));label.setAttribute('y','326');label.setAttribute('text-anchor','middle');label.textContent=x;grid.append(label);
    }
    for(const [name,points] of Object.entries(series))
      chart.querySelector('[data-chart-line="'+name+'"]').setAttribute('d',points.map(([x,y],i)=>(i?'L':'M')+sx(x).toFixed(1)+' '+sy(y).toFixed(1)).join(' '));
    chart.querySelector('svg').setAttribute('aria-label',t.chart.replace('{n}',String(perDay)));
    chart.querySelector('[data-chart-desc]').textContent=t.chart.replace('{n}',String(perDay));
  };
  function renderProfit(){
    if(!profitTool)return;
    const v=read(profitInputs),f=read(fixedInputs);
    profitTool.querySelector('[data-profit-error]').textContent=v&&f?'':t.invalid;
    if(!v||!f)return;
    const [initial,price,perDay,days,variable,owner,financing]=v;
    const treatments=perDay*days,revenue=treatments*price,variableExpenses=treatments*variable;
    const fixed=f.reduce((a,b)=>a+b,0),operatingExpenses=fixed+variableExpenses;
    const surplus=revenue-operatingExpenses,cash=surplus-owner-financing,margin=price-variable;
    setResult(0,money.format(revenue));
    setResult(1,money.format(operatingExpenses));
    setResult(2,money.format(surplus),surplus<0);
    setResult(3,money.format(cash),cash<=0);
    profitTool.querySelector('[data-cash-state]').textContent=cash>0?t.available:t.negative;
    setResult(4,margin>0?number.format(Math.ceil(fixed/margin))+' '+t.treatments:t.unreachable,margin<=0);
    setResult(5,margin>0?number.format(Math.ceil((fixed+owner+financing)/margin))+' '+t.treatments:t.unreachable,margin<=0);
    setResult(6,cash>0&&initial>0?number.format(initial/cash)+' '+t.months:t.noPayback,cash<=0);
    plot(v,fixed);
  }
  if(profitTool){
    profitInputs.forEach((input,i)=>{
      input.addEventListener('input',()=>{
        const slider=profitTool.querySelector('[data-range="'+i+'"]');
        if(slider)slider.value=input.value;
        renderProfit();
      });
    });
    profitTool.querySelectorAll('[data-range]').forEach(slider=>slider.addEventListener('input',()=>{
      profitTool.querySelector('[data-profit="'+slider.dataset.range+'"]').value=slider.value;
      renderProfit();
    }));
    fixedInputs.forEach(input=>input.addEventListener('input',renderProfit));
    profitTool.querySelector('[data-profit-reset]').addEventListener('click',()=>{
      profitInputs.forEach((input,i)=>{input.value=defaults[i];});
      fixedInputs.forEach((input,i)=>{input.value=fixedDefaults[i];});
      profitTool.querySelectorAll('[data-range]').forEach(slider=>{slider.value=defaults[Number(slider.dataset.range)];});
      renderProfit();
    });
    renderProfit();
  }
})();
