#!/usr/bin/env python3
"""
Simulador Fee-Based · Nobel Capital
Deploy em qualquer plataforma Python (Render, Railway, Fly.io)
"""
import os, json, urllib.request, urllib.error
from http.server import BaseHTTPRequestHandler, HTTPServer

PORT = int(os.environ.get("PORT", 8181))
API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")

HTML = r"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="Fee Nobel">
<meta name="mobile-web-app-capable" content="yes">
<title>Simulador Fee-Based &#183; Nobel Capital</title>
<style>
  *{box-sizing:border-box;margin:0;padding:0}
  body{background:#050508;color:#f0f2ff;font-family:'Space Grotesk','Segoe UI',sans-serif;min-height:100vh;padding:20px 16px;font-size:14px}
  input[type=number]::-webkit-outer-spin-button,
  input[type=number]::-webkit-inner-spin-button{-webkit-appearance:none}
  input[type=number]{-moz-appearance:textfield}
  @keyframes spin{to{transform:rotate(360deg)}}
  .card{background:#0d0d14;border:1px solid rgba(77,159,255,0.15);padding:16px;margin-bottom:12px;position:relative;overflow:hidden}
  .card-line{position:absolute;top:0;left:0;right:0;height:1px;background:linear-gradient(90deg,transparent,#4d9fff,transparent);opacity:0.35}
  .card-title{font-family:monospace;font-size:9px;letter-spacing:0.22em;text-transform:uppercase;color:#4d9fff;margin-bottom:14px;display:flex;align-items:center;gap:8px;font-weight:700}
  .lbl{display:block;font-size:10px;font-weight:700;color:rgba(240,242,255,0.65);letter-spacing:0.06em;margin-bottom:4px}
  .inp-wrap{display:flex;align-items:center;background:#050508;border:1px solid rgba(77,159,255,0.15)}
  .inp-pfx{padding:8px 9px;font-family:monospace;font-size:11px;color:#4d9fff;border-right:1px solid rgba(77,159,255,0.12);min-width:36px;text-align:center}
  .inp{flex:1;background:transparent;border:none;color:#f0f2ff;padding:8px 10px;font-family:inherit;font-size:14px;font-weight:500;outline:none;width:100%}
  .row{display:flex;justify-content:space-between;align-items:center;padding:8px 0;border-bottom:1px solid rgba(240,242,255,0.07)}
  .row-lbl{font-size:12px;color:rgba(240,242,255,0.65);font-weight:600}
  .row-val{font-family:monospace;font-size:12px;font-weight:700}
  .mono{font-family:'Space Mono','Courier New',monospace}
  .grid2{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:8px}
  .grid-main{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:12px}
  .cls-card{background:#12121c;border:1px solid rgba(77,159,255,0.18);padding:9px 9px 7px}
  .cls-head{display:flex;justify-content:space-between;align-items:center;margin-bottom:4px}
  .cls-name{font-size:9px;color:rgba(240,242,255,0.7);font-weight:700}
  .cls-tag{font-family:monospace;font-size:7px;padding:1px 4px;letter-spacing:0.07em}
  .badge-green{background:rgba(61,255,160,0.1);color:#3dffa0}
  .badge-blue{background:rgba(77,159,255,0.1);color:#4d9fff}
  .badge-dim{background:rgba(240,242,255,0.05);color:rgba(240,242,255,0.35)}
  .badge-red{background:rgba(255,77,106,0.1);color:#ff4d6a}
  .ex-card{background:#12121c;border:1px solid rgba(255,77,106,0.12);padding:9px 9px 7px;opacity:0.5}
  .section-sep{font-family:monospace;font-size:8px;color:rgba(77,159,255,0.7);text-transform:uppercase;letter-spacing:0.2em;margin:12px 0 8px;font-weight:700}
  .drop-area{border:1.5px dashed rgba(77,159,255,0.22);background:#12121c;padding:14px 16px;cursor:pointer;display:flex;align-items:center;gap:12px;transition:all 0.2s;margin-bottom:0}
  .drop-area:hover,.drop-area.dragover{border-color:#4d9fff;background:rgba(77,159,255,0.05)}
  .drop-icon{font-size:22px;flex-shrink:0}
  .drop-main{font-size:13px;color:#f0f2ff;font-weight:600}
  .drop-main span{color:#4d9fff}
  .drop-sub{font-family:monospace;font-size:9px;color:rgba(240,242,255,0.4);margin-top:2px}
  .status{padding:9px 12px;font-family:monospace;font-size:10px;letter-spacing:0.06em;margin-top:10px}
  .status-loading{background:rgba(77,159,255,0.07);border:1px solid rgba(77,159,255,0.2);color:#4d9fff}
  .status-success{background:rgba(61,255,160,0.06);border:1px solid rgba(61,255,160,0.2);color:#3dffa0}
  .status-error{background:rgba(255,77,106,0.06);border:1px solid rgba(255,77,106,0.2);color:#ff4d6a}
  .spin{display:inline-block;width:9px;height:9px;border:2px solid rgba(77,159,255,0.3);border-top-color:#4d9fff;border-radius:50%;animation:spin 0.7s linear infinite;margin-right:6px;vertical-align:middle}
  .fname{font-size:9px;color:#4d9fff;margin-left:10px}
  .client-name{font-family:monospace;font-size:10px;color:#4d9fff;margin-bottom:10px}
  .pie-wrap{display:flex;align-items:center;gap:16px}
  .legend-item{display:flex;align-items:center;gap:7px;margin-bottom:7px;font-size:11px}
  .legend-dot{width:8px;height:8px;border-radius:50%;flex-shrink:0}
  .legend-lbl{flex:1;color:rgba(240,242,255,0.65);font-size:10px;font-weight:600}
  .legend-val{font-family:monospace;font-size:10px;font-weight:700}
  .legend-pct{font-family:monospace;font-size:8px;color:rgba(240,242,255,0.4)}
  .result-grid{display:grid;grid-template-columns:1fr auto;gap:12px;align-items:start}
  .result-right{text-align:center;min-width:110px}
  .result-label{font-family:monospace;font-size:8px;letter-spacing:0.18em;text-transform:uppercase;color:rgba(240,242,255,0.45);margin-bottom:6px}
  .result-big{font-size:36px;font-weight:700;letter-spacing:-0.03em;line-height:1}
  .result-sub{font-family:monospace;font-size:9px;color:rgba(240,242,255,0.4);margin-top:5px}
  .be-badge{font-family:monospace;font-size:10px;color:#4d9fff;background:#12121c;border:1px solid rgba(77,159,255,0.18);padding:4px 10px;margin-top:8px;display:inline-block}
  .bar-area{display:flex;gap:8px;height:180px;margin-top:14px;align-items:flex-end}
  .bar-year{flex:1;display:flex;flex-direction:column;align-items:center}
  .bar-outer{width:100%;background:rgba(240,242,255,0.06);border:1px solid rgba(240,242,255,0.12);position:relative;display:flex;flex-direction:column;justify-content:flex-end}
  .bar-inner{width:100%;background:linear-gradient(180deg,#7bbfff,#4d9fff);box-shadow:0 0 8px rgba(77,159,255,0.4);display:flex;align-items:center;justify-content:center}
  .bar-pct{font-family:monospace;font-size:11px;font-weight:700;color:#fff;text-shadow:0 1px 4px rgba(0,0,0,0.8)}
  .bar-amt{font-family:monospace;font-size:8px;color:rgba(240,242,255,0.55);margin-bottom:3px;text-align:center;white-space:nowrap;font-weight:600}
  .bar-lbl{font-family:monospace;font-size:9px;color:rgba(240,242,255,0.7);margin-top:6px;font-weight:700}
  .legend-bar{display:flex;gap:14px;margin-top:8px}
  .legend-bar-item{display:flex;align-items:center;gap:5px;font-size:10px;color:rgba(240,242,255,0.55);font-weight:600}
  .legend-bar-dot{width:7px;height:7px}
  .glow-border{border-color:#3dffa0!important}
  .glow-text{color:#3dffa0!important}
  @media(max-width:480px){
    .grid-main{grid-template-columns:1fr}
    .result-grid{grid-template-columns:1fr}
    .result-right{text-align:left;min-width:unset;margin-top:8px}
  }
</style>
</head>
<body>
<div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:18px">
  <div>
    <div style="font-size:24px;font-weight:700;letter-spacing:-0.02em;background:linear-gradient(135deg,#f0f2ff,#7bbfff);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text">Simulador Fee-Based</div>
    <div class="mono" style="font-size:9px;color:rgba(240,242,255,0.4);letter-spacing:0.18em;text-transform:uppercase;margin-top:4px">Nobel Capital &#183; Advisory</div>
  </div>
  <div class="mono" style="background:#12121c;border:1px solid rgba(77,159,255,0.15);padding:5px 10px;font-size:9px;color:#4d9fff;letter-spacing:0.12em;text-transform:uppercase">v3 &#183; 2026</div>
</div>
<div class="card">
  <div class="card-line"></div>
  <div class="card-title">Upload de Extrato do Cliente</div>
  <div class="drop-area" id="dropZone">
    <span class="drop-icon">&#128196;</span>
    <div>
      <div class="drop-main"><span>Arraste o extrato</span> ou clique para selecionar</div>
      <div class="drop-sub">PDF &#183; XP Performance, extrato de posi&#231;&#227;o, carteira consolidada</div>
    </div>
    <input id="fileInput" type="file" accept="application/pdf" style="display:none">
  </div>
  <div id="statusBox" style="display:none" class="status"></div>
</div>
<div class="grid-main">
  <div class="card">
    <div class="card-line"></div>
    <div class="card-title">Base Eleg&#237;vel por Classe</div>
    <div id="clientName" class="client-name" style="display:none"></div>
    <div class="grid2">
      <div class="cls-card"><div class="cls-head"><span class="cls-name">Renda Fixa</span><span class="cls-tag badge-green">+spread</span></div><div class="inp-wrap" id="wrap-rf"><span class="inp-pfx">R$</span><input type="number" id="inp-rf" class="inp" value="500000" step="10000"></div></div>
      <div class="cls-card"><div class="cls-head"><span class="cls-name">Fundos</span><span class="cls-tag badge-blue">rebate</span></div><div class="inp-wrap" id="wrap-fd"><span class="inp-pfx">R$</span><input type="number" id="inp-fd" class="inp" value="300000" step="10000"></div></div>
      <div class="cls-card"><div class="cls-head"><span class="cls-name">Previd&#234;ncia</span><span class="cls-tag badge-blue">rebate</span></div><div class="inp-wrap" id="wrap-pv"><span class="inp-pfx">R$</span><input type="number" id="inp-pv" class="inp" value="100000" step="10000"></div></div>
      <div class="cls-card"><div class="cls-head"><span class="cls-name">COEs</span><span class="cls-tag badge-dim">sem spread</span></div><div class="inp-wrap" id="wrap-co"><span class="inp-pfx">R$</span><input type="number" id="inp-co" class="inp" value="100000" step="10000"></div></div>
    </div>
    <div class="ex-card"><div class="cls-head"><span class="cls-name">A&#231;&#245;es + FIIs &#8212; exclu&#237;dos</span><span class="cls-tag badge-red">fora</span></div><div class="inp-wrap"><span class="inp-pfx">R$</span><input type="number" id="inp-ex" class="inp" value="0" step="10000"></div></div>
  </div>
  <div class="card">
    <div class="card-line"></div>
    <div class="card-title">Par&#226;metros do Fee</div>
    <div><label class="lbl">Fee Proposto (% a.a.)</label><div class="inp-wrap"><span class="inp-pfx">%</span><input type="number" id="inp-fee" class="inp" value="0.9" step="0.05"></div></div>
    <div class="section-sep">&#8212; ganhos no modelo fee</div>
    <div style="margin-bottom:10px"><label class="lbl">Spread RF vs. Transacional (% a.a.)</label><div class="inp-wrap"><span class="inp-pfx">%</span><input type="number" id="inp-sp" class="inp" value="0.4" step="0.05"></div></div>
    <div style="margin-bottom:10px"><label class="lbl">Rebate Fundos (% a.a.)</label><div class="inp-wrap"><span class="inp-pfx">%</span><input type="number" id="inp-rbF" class="inp" value="0.5" step="0.05"></div></div>
    <div><label class="lbl">Rebate Previd&#234;ncia (% a.a.)</label><div class="inp-wrap"><span class="inp-pfx">%</span><input type="number" id="inp-rbP" class="inp" value="0.3" step="0.05"></div></div>
    <div class="section-sep">&#8212; custo de reaplica&#231;&#227;o trans.</div>
    <div><label class="lbl">ROA Reaplica&#231;&#227;o (% s/ vencimentos)</label><div class="inp-wrap"><span class="inp-pfx">%</span><input type="number" id="inp-roa" class="inp" value="0.5" step="0.05" min="0.35" max="4"></div></div>
  </div>
  <div class="card">
    <div class="card-line"></div>
    <div class="card-title">Composi&#231;&#227;o da Base</div>
    <div style="font-family:monospace;font-size:7px;color:rgba(77,159,255,0.55);letter-spacing:0.2em;text-transform:uppercase;margin-bottom:6px">&#9632; Fee-Based</div>
    <div class="pie-wrap"><canvas id="pieChart" width="110" height="110" style="flex-shrink:0"></canvas><div id="legend" style="flex:1"></div></div>
    <div style="height:1px;background:rgba(240,242,255,0.07);margin:12px 0"></div>
    <div style="font-family:monospace;font-size:7px;color:rgba(255,77,106,0.55);letter-spacing:0.2em;text-transform:uppercase;margin-bottom:6px">&#9632; Custo Transacional</div>
    <div class="pie-wrap"><canvas id="pieChartTrans" width="110" height="110" style="flex-shrink:0"></canvas><div id="legendTrans" style="flex:1"></div></div>
  </div>
  <div class="card">
    <div class="card-line"></div>
    <div class="card-title">Resultado</div>
    <div class="result-grid">
      <div id="resultRows"></div>
      <div class="result-right"><div class="result-label">Custo L&#237;quido</div><div id="resultBig" class="result-big"></div><div id="resultSub" class="result-sub"></div><div id="resultBE" class="be-badge"></div></div>
    </div>
  </div>
  <div class="card" style="grid-column:1 / -1">
    <div class="card-line"></div>
    <div class="card-title">Custo Acumulado 5 Anos</div>
    <div class="bar-area" id="barChart"></div>
    <div class="legend-bar"><div class="legend-bar-item"><div class="legend-bar-dot" style="background:rgba(240,242,255,0.08);border:1px solid rgba(240,242,255,0.15)"></div>Fee bruto</div><div class="legend-bar-item"><div class="legend-bar-dot" style="background:#4d9fff"></div>Custo l&#237;quido</div><div class="legend-bar-item"><div class="legend-bar-dot" style="background:#ff2d50"></div>Custo transacional</div></div>
  </div>
</div>
<script>
const PIE_COLORS=["#4d9fff","#7bbfff","#b8d8ff","#ffffff"],PIE_LABELS=["Renda Fixa","Fundos","Previd\u00eancia","COEs"];
const PIE_COLORS_RED=["#ff2d50","#ff5570","#ff8a9a","#ffb3bb","#ffd6db"];
let rfAno1=0,rfAno2=0;
function fmtR(v){return"R$\u00a0"+Math.abs(Math.round(v)).toLocaleString("pt-BR")}
function fmtP(v){return(v*100).toFixed(3).replace(".",",")+"%"}
function val(id){return parseFloat(document.getElementById(id).value)||0}
function calc(){
  const rf=val("inp-rf"),fd=val("inp-fd"),pv=val("inp-pv"),co=val("inp-co");
  const fee=val("inp-fee"),sp=val("inp-sp"),rbF=val("inp-rbF"),rbP=val("inp-rbP"),roa=val("inp-roa");
  const base=rf+fd+pv+co,fD=fee/100,spD=sp/100,rbFD=rbF/100,rbPD=rbP/100,roaD=roa/100;
  const feeA=base*fD,gSp=rf*spD,gRF=fd*rbFD,gRP=pv*rbPD,gROA=(rfAno1+rfAno2)*roaD;
  const gain=gSp+gRF+gRP+gROA,liq=feeA-gain;
  const liqPct=base>0?liq/base:0;
  const be=liq<=0?"Imediato":gain>0?(liq/gain).toFixed(1).replace(".",",")+"\u00a0anos":"\u2014";
  const vCol=liqPct<=0?"#3dffa0":liqPct<0.004?"#4d9fff":"#ff4d6a";
  return{rf,fd,pv,co,base,feeA,gSp,gRF,gRP,gROA,gain,liq,liqPct,be,vCol,fee:fD};
}
function drawPie(){
  const{rf,fd,pv,co,base}=calc(),vals=[rf,fd,pv,co];
  const c=document.getElementById("pieChart"),ctx=c.getContext("2d");
  const W=c.width,H=c.height,cx=W/2,cy=H/2,r=W/2-5;
  ctx.clearRect(0,0,W,H);let s=-Math.PI/2;
  vals.forEach((v,i)=>{
    if(v<=0||base<=0)return;const sl=(v/base)*2*Math.PI;
    ctx.beginPath();ctx.moveTo(cx,cy);ctx.arc(cx,cy,r,s,s+sl);ctx.closePath();
    ctx.fillStyle=PIE_COLORS[i];ctx.fill();
    if(i===0){ctx.shadowColor="#4d9fff";ctx.shadowBlur=10;ctx.fill();ctx.shadowBlur=0;}
    s+=sl;
  });
  ctx.beginPath();ctx.arc(cx,cy,r*0.52,0,2*Math.PI);ctx.fillStyle="#0d0d14";ctx.fill();
  ctx.fillStyle="#f0f2ff";ctx.font="bold 10px sans-serif";ctx.textAlign="center";ctx.textBaseline="middle";
  if(base>0){const lbl=base>=1e6?(base/1e6).toFixed(1).replace(".",",")+"M":(base/1e3).toFixed(0)+"k";ctx.fillText("R$"+lbl,cx,cy);}
  const leg=document.getElementById("legend");leg.innerHTML="";
  vals.forEach((v,i)=>{
    if(v<=0)return;const div=document.createElement("div");div.className="legend-item";
    div.innerHTML=`<div class="legend-dot" style="background:${PIE_COLORS[i]};${i===0?"box-shadow:0 0 5px rgba(77,159,255,0.6)":""}"></div><span class="legend-lbl">${PIE_LABELS[i]}</span><span class="legend-val">${fmtR(v)}</span><span class="legend-pct">${base>0?((v/base)*100).toFixed(1).replace(".",",")+"%":""}</span>`;
    leg.appendChild(div);
  });
}
function drawPieTrans(){
  const{gSp,gRF,gRP,gROA,base,rf}=calc();
  const spD=val("inp-sp")/100;
  const hasMatur=rfAno1>0||rfAno2>0;
  let vals,lbls,cols;
  if(hasMatur){
    const rfRest=Math.max(0,rf-rfAno1-rfAno2);
    const gSp1=rfAno1*spD,gSp2=rfAno2*spD,gSpR=rfRest*spD;
    vals=[gROA,gSp1,gSp2,gSpR,gRF,gRP];
    lbls=["ROA Vencimentos","Spread Ano 1","Spread Ano 2","Spread Longo","Rebate Fundos","Rebate Prev."];
    cols=["#ff8c00","#ff2d50","#ff5570","#ff8a9a","#ffc5cc","#ffd6db"];
  }else{
    vals=[gROA,gSp,gRF,gRP];
    lbls=["ROA Vencimentos","Spread RF","Rebate Fundos","Rebate Prev."];
    cols=["#ff8c00","#ff4d6a","#ff8096","#ffb3bb"];
  }
  const total=vals.reduce((s,v)=>s+v,0);
  const c=document.getElementById("pieChartTrans"),ctx=c.getContext("2d");
  const W=c.width,H=c.height,cx=W/2,cy=H/2,r=W/2-5;
  ctx.clearRect(0,0,W,H);
  if(total<=0||base<=0){
    ctx.beginPath();ctx.arc(cx,cy,r,0,2*Math.PI);ctx.fillStyle="rgba(255,77,106,0.08)";ctx.fill();
    ctx.beginPath();ctx.arc(cx,cy,r*0.52,0,2*Math.PI);ctx.fillStyle="#0d0d14";ctx.fill();
    ctx.fillStyle="rgba(240,242,255,0.3)";ctx.font="bold 9px sans-serif";ctx.textAlign="center";ctx.textBaseline="middle";
    ctx.fillText("—",cx,cy);
    document.getElementById("legendTrans").innerHTML="";return;
  }
  let s=-Math.PI/2;
  vals.forEach((v,i)=>{
    if(v<=0)return;const sl=(v/total)*2*Math.PI;
    ctx.beginPath();ctx.moveTo(cx,cy);ctx.arc(cx,cy,r,s,s+sl);ctx.closePath();
    ctx.fillStyle=cols[i];ctx.fill();
    if(i===0){ctx.shadowColor="#ff4d6a";ctx.shadowBlur=10;ctx.fill();ctx.shadowBlur=0;}
    s+=sl;
  });
  ctx.beginPath();ctx.arc(cx,cy,r*0.52,0,2*Math.PI);ctx.fillStyle="#0d0d14";ctx.fill();
  ctx.fillStyle="#ff4d6a";ctx.font="bold 10px sans-serif";ctx.textAlign="center";ctx.textBaseline="middle";
  const pctTxt=base>0?((total/base)*100).toFixed(2).replace(".",",")+"%":"—";
  ctx.fillText(pctTxt,cx,cy-6);
  ctx.fillStyle="rgba(240,242,255,0.3)";ctx.font="7px monospace";
  ctx.fillText("a.a.",cx,cy+7);
  const leg=document.getElementById("legendTrans");leg.innerHTML="";
  vals.forEach((v,i)=>{
    if(v<=0)return;const div=document.createElement("div");div.className="legend-item";
    div.innerHTML=`<div class="legend-dot" style="background:${cols[i]};${i===0?"box-shadow:0 0 5px rgba(255,77,106,0.5)":""}"></div><span class="legend-lbl">${lbls[i]}</span><span class="legend-val" style="color:${cols[i]}">${fmtR(v)}</span><span class="legend-pct">${base>0?((v/base)*100).toFixed(1).replace(".",",")+"%":""}</span>`;
    leg.appendChild(div);
  });
}
function drawResult(){
  const{base,feeA,gSp,gRF,gRP,gROA,gain,liq,liqPct,be,vCol}=calc();
  const rows=[["Base Total",fmtR(base),"#f0f2ff"],["Fee Bruto/ano",fmtR(feeA)+"/ano","#4d9fff"],["Spread RF","+"+fmtR(gSp),"#3dffa0"],["Rebate Fundos","+"+fmtR(gRF),"#3dffa0"],["Rebate Prev.","+"+fmtR(gRP),"#3dffa0"],...(gROA>0?[["ROA Vencimentos","+"+fmtR(gROA),"#ff8c00"]]:[]),(["Total Compensado","+"+fmtR(gain),"#3dffa0"])];
  document.getElementById("resultRows").innerHTML=rows.map(([l,v,c])=>`<div class="row"><span class="row-lbl">${l}</span><span class="row-val" style="color:${c}">${v}</span></div>`).join("");
  document.getElementById("resultBig").textContent=fmtP(liqPct);
  document.getElementById("resultBig").style.color=vCol;
  document.getElementById("resultSub").textContent=liqPct<=0?"positivo p/ cliente":"% a.a. real";
  document.getElementById("resultBE").textContent="BE: "+be;
}
function drawBars(){
  const{base,liqPct,fee,gain,gROA,gSp,gRF,gRP}=calc();
  const annualGain=gSp+gRF+gRP;
  const roaD=val("inp-roa")/100;
  const container=document.getElementById("barChart");
  container.innerHTML="";
  const minBH=45,maxBH=140,minInner=20;
  for(let y=1;y<=5;y++){
    const feeT=base>0?base*fee*y:0;
    // Net cost: annual recurring × y, minus one-time ROA savings (capped: y1=rfAno1, y2+=both)
    const roaCum=y>=2?(rfAno1+rfAno2)*roaD:rfAno1*roaD;
    const annualLiqPct=base>0?(base*fee-annualGain)/base:0;
    const liqT=base>0?Math.max(0,base*annualLiqPct*y-roaCum):0;
    const transT=base>0?annualGain*y+roaCum:0;
    const ratio=feeT>0?liqT/feeT:0;
    const transRatio=feeT>0?transT/feeT:0;
    const bH=minBH+(maxBH-minBH)*((y-1)/4);
    const lH=Math.max(minInner,ratio*bH);
    const tH=Math.max(minInner,Math.min(transRatio*bH,bH));
    const pct=base>0?(ratio*100).toFixed(1).replace(".",",")+"%":"—";
    const tPct=base>0?(transRatio*100).toFixed(1).replace(".",",")+"%":"—";
    const amt=base>0?fmtR(feeT):"—";
    const tAmt=base>0?fmtR(transT):"—";
    const col=document.createElement("div");
    col.className="bar-year";
    col.innerHTML=
      `<div style="display:flex;gap:3px;align-items:flex-end;width:100%">`+
        `<div style="flex:1;display:flex;flex-direction:column;align-items:center">`+
          `<div class="bar-amt">${amt}</div>`+
          `<div class="bar-outer" style="width:100%;height:${bH}px">`+
            `<div class="bar-inner" style="height:${lH}px"><span class="bar-pct">${pct}</span></div>`+
          `</div>`+
        `</div>`+
        `<div style="flex:1;display:flex;flex-direction:column;align-items:center">`+
          `<div class="bar-amt" style="color:rgba(255,77,106,0.7)">${tAmt}</div>`+
          `<div class="bar-outer" style="width:100%;height:${bH}px;border-color:rgba(255,77,106,0.25);background:rgba(255,77,106,0.04)">`+
            `<div style="width:100%;height:${tH}px;background:linear-gradient(180deg,#ff7a8a,#ff2d50);box-shadow:0 0 8px rgba(255,77,106,0.35);display:flex;align-items:center;justify-content:center">`+
              `<span class="bar-pct">${tPct}</span>`+
            `</div>`+
          `</div>`+
        `</div>`+
      `</div>`+
      `<div class="bar-lbl">Ano ${y}</div>`;
    container.appendChild(col);
  }
}
function update(){drawPie();drawPieTrans();drawResult();drawBars();}
document.querySelectorAll("input[type=number]").forEach(el=>el.addEventListener("input",update));
const dropZone=document.getElementById("dropZone"),fileInput=document.getElementById("fileInput");
dropZone.addEventListener("click",()=>fileInput.click());
dropZone.addEventListener("dragover",e=>{e.preventDefault();dropZone.classList.add("dragover");});
dropZone.addEventListener("dragleave",()=>dropZone.classList.remove("dragover"));
dropZone.addEventListener("drop",e=>{e.preventDefault();dropZone.classList.remove("dragover");processPDF(e.dataTransfer.files[0]);});
fileInput.addEventListener("change",e=>processPDF(e.target.files[0]));
function setStatus(type,msg,fname){
  const box=document.getElementById("statusBox");box.className="status status-"+type;box.style.display="block";
  let html="";if(type==="loading")html+='<span class="spin"></span>';
  html+=msg;if(fname)html+=`<span class="fname">&#128206; ${fname}</span>`;box.innerHTML=html;
}
function triggerGlow(){
  ["wrap-rf","wrap-fd","wrap-pv","wrap-co"].forEach(id=>document.getElementById(id).classList.add("glow-border"));
  ["inp-rf","inp-fd","inp-pv","inp-co"].forEach(id=>document.getElementById(id).classList.add("glow-text"));
  setTimeout(()=>{
    ["wrap-rf","wrap-fd","wrap-pv","wrap-co"].forEach(id=>document.getElementById(id).classList.remove("glow-border"));
    ["inp-rf","inp-fd","inp-pv","inp-co"].forEach(id=>document.getElementById(id).classList.remove("glow-text"));
  },4000);
}
async function processPDF(file){
  if(!file)return;
  if(file.type!=="application/pdf"){setStatus("error","&#9888; Envie um arquivo PDF.");return;}
  rfAno1=0;rfAno2=0;
  setStatus("loading","Lendo PDF...",file.name);
  const b64=await new Promise((res,rej)=>{const r=new FileReader();r.onload=()=>res(r.result.split(",")[1]);r.onerror=()=>rej(new Error("Falha na leitura"));r.readAsDataURL(file);});
  setStatus("loading","Extraindo posições com IA...",file.name);
  try{
    const resp=await fetch("/proxy",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({
      model:"claude-sonnet-4-6",max_tokens:1024,
      tools:[{name:"parse_portfolio",description:"Extrai os dados financeiros do extrato do cliente",input_schema:{type:"object",properties:{nome:{type:["string","null"],description:"Nome do cliente"},rf:{type:"number",description:"Renda Fixa: CDB, LCI, LCA, LCD, CRI, CRA, Debêntures, NTN-B, Tesouro Direto, LFT, LTN, compromissadas"},fundos:{type:"number",description:"Fundos de Investimento: FIC, FIM, FIRF, Fundo Mútuo, e qualquer produto com 'Fundo' no nome exceto previdência (VGBL/PGBL). Incluir mesmo que apareçam sob estratégia Renda Variável Brasil ou Multimercado. NÃO incluir ações individuais, FIIs, ETFs, BDRs."},prev:{type:"number",description:"Previdência: VGBL, PGBL"},coe:{type:"number",description:"COE"},excluidos:{type:"number",description:"Excluídos da base fee: SOMENTE ações individuais (ex: PETR4, BBAS3, VALE3), FIIs (ex: HGLG11, KNRI11), ETFs e BDRs. NÃO incluir fundos de investimento com 'Fundo' no nome."},rf_ano1:{type:"number",description:"Valor de RF com vencimento nos próximos 12 meses"},rf_ano2:{type:"number",description:"Valor de RF com vencimento entre 12 e 24 meses"}},required:["nome","rf","fundos","prev","coe","excluidos","rf_ano1","rf_ano2"]}}],
      tool_choice:{type:"tool",name:"parse_portfolio"},
      messages:[{role:"user",content:[{type:"document",source:{type:"base64",media_type:"application/pdf",data:b64}},{type:"text",text:"Extraia os dados financeiros do extrato usando a ferramenta parse_portfolio. Use ponto como separador decimal. Valores não identificados = 0."}]}]
    })});
    const res=await resp.json();
    if(!resp.ok)throw new Error("["+resp.status+"] "+(res.error?.message||JSON.stringify(res.error||res)));
    const toolBlock=res.content?.find(b=>b.type==="tool_use"&&b.name==="parse_portfolio");
    if(!toolBlock)throw new Error("Sem dados na resposta: "+JSON.stringify(res.content?.map(b=>b.type)));
    let data=toolBlock.input;
    if(data.erro){setStatus("error","&#9888; "+data.erro);return;}
    if(data.rf!=null)document.getElementById("inp-rf").value=data.rf||0;
    if(data.fundos!=null)document.getElementById("inp-fd").value=data.fundos||0;
    if(data.prev!=null)document.getElementById("inp-pv").value=data.prev||0;
    if(data.coe!=null)document.getElementById("inp-co").value=data.coe||0;
    if(data.excluidos!=null)document.getElementById("inp-ex").value=data.excluidos||0;
    rfAno1=(data.rf_ano1!=null)?data.rf_ano1||0:0;
    rfAno2=(data.rf_ano2!=null)?data.rf_ano2||0:0;
    if(data.nome){const cn=document.getElementById("clientName");cn.textContent="\u25b8 "+data.nome.toUpperCase();cn.style.display="block";}
    update();triggerGlow();
    const tot=(data.rf||0)+(data.fundos||0)+(data.prev||0)+(data.coe||0)+(data.excluidos||0);
    setStatus("success","&#10003; "+(data.nome?data.nome+" \u00b7 ":"")+"Total "+fmtR(tot),file.name);
  }catch(e){setStatus("error","&#9888; "+e.message);}
}
update();
</script>
</body>
</html>"""

class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args): pass

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(HTML.encode("utf-8"))

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_POST(self):
        if self.path == "/proxy":
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length)
            req = urllib.request.Request(
                "https://api.anthropic.com/v1/messages",
                data=body,
                headers={
                    "Content-Type": "application/json",
                    "x-api-key": API_KEY,
                    "anthropic-version": "2023-06-01",
                    "anthropic-beta": "pdfs-2024-09-25",
                },
                method="POST",
            )
            try:
                with urllib.request.urlopen(req) as r:
                    resp = r.read()
                    self.send_response(200)
                    self.send_header("Content-Type", "application/json")
                    self.send_header("Access-Control-Allow-Origin", "*")
                    self.end_headers()
                    self.wfile.write(resp)
            except urllib.error.HTTPError as e:
                resp = e.read()
                self.send_response(e.code)
                self.send_header("Content-Type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(resp)
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode())
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == "__main__":
    with HTTPServer(("0.0.0.0", PORT), Handler) as httpd:
        print(f"Rodando na porta {PORT}")
        httpd.serve_forever()
