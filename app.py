<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>ISI Platform — Industrial Safety Intelligence</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
:root{
  --bg:#080a0d;--card:#0d1117;--border:#1e2530;--primary:#e8a020;
  --destructive:#ef4444;--warning:#f59e0b;--safe:#22c55e;
  --muted:#6b7280;--fg:#e2e8f0;--fg2:#94a3b8;
  --red-glow:rgba(239,68,68,0.25);
}
body{background:var(--bg);color:var(--fg);font-family:'Courier New',monospace;min-height:100vh;overflow:hidden}
#app{display:flex;flex-direction:column;height:100vh;position:relative}

/* CRT overlay */
#app::before{content:'';position:fixed;inset:0;z-index:9990;pointer-events:none;
  background:linear-gradient(rgba(18,16,16,0) 50%,rgba(0,0,0,0.08) 50%),
             linear-gradient(90deg,rgba(255,0,0,0.02),rgba(0,255,0,0.01),rgba(0,0,255,0.02));
  background-size:100% 3px,3px 100%}

/* Emergency border */
.emergency-border{position:fixed;inset:0;z-index:9980;pointer-events:none;
  box-shadow:inset 0 0 0 4px var(--destructive),inset 0 0 60px var(--red-glow);
  animation:emergency-pulse 0.8s ease-in-out infinite alternate}
@keyframes emergency-pulse{from{box-shadow:inset 0 0 0 4px var(--destructive),inset 0 0 40px var(--red-glow)}to{box-shadow:inset 0 0 0 6px var(--destructive),inset 0 0 100px var(--red-glow)}}

/* Emergency banner */
#emergency-banner{display:none;background:var(--destructive);color:#fff;padding:10px 20px;
  font-weight:bold;font-size:13px;letter-spacing:3px;text-transform:uppercase;
  justify-content:space-between;align-items:center;z-index:200;
  animation:banner-pulse 0.6s ease-in-out infinite alternate}
#emergency-banner.active{display:flex}
@keyframes banner-pulse{from{background:#dc2626}to{background:#b91c1c}}
#emergency-banner button{background:rgba(255,255,255,0.2);border:1px solid rgba(255,255,255,0.5);
  color:#fff;padding:4px 14px;font-size:11px;letter-spacing:2px;cursor:pointer;font-family:inherit}
#emergency-banner button:hover{background:rgba(255,255,255,0.35)}

/* Layout */
#layout{display:flex;flex:1;overflow:hidden}
#sidebar{width:220px;background:var(--card);border-right:1px solid var(--border);
  display:flex;flex-direction:column;flex-shrink:0}
#sidebar-logo{padding:16px;border-bottom:1px solid var(--border);background:#000;
  display:flex;align-items:center;gap:10px}
#sidebar-logo svg{color:var(--primary);flex-shrink:0}
#sidebar-logo .brand{font-size:13px;font-weight:bold;letter-spacing:1px;line-height:1.2}
#sidebar-logo .sub{font-size:9px;color:var(--muted);letter-spacing:2px}
#sidebar-nav{flex:1;padding:12px 0;overflow-y:auto}
.nav-section{font-size:9px;color:var(--muted);letter-spacing:2px;padding:12px 16px 6px;opacity:0.6}
.nav-item{display:flex;align-items:center;gap:10px;padding:8px 16px;font-size:11px;
  letter-spacing:1.5px;cursor:pointer;border-left:2px solid transparent;
  transition:all 0.15s;color:var(--muted);text-decoration:none}
.nav-item:hover{background:rgba(255,255,255,0.04);color:var(--fg);border-left-color:var(--border)}
.nav-item.active{background:rgba(232,160,32,0.1);color:var(--primary);border-left-color:var(--primary)}
.nav-item .badge{margin-left:auto;background:var(--destructive);color:#fff;font-size:9px;
  padding:1px 5px;font-weight:bold;min-width:18px;text-align:center}
#sidebar-risk{padding:12px 14px;border-top:1px solid var(--border);background:rgba(0,0,0,0.4)}
#sidebar-risk .label{font-size:9px;color:var(--muted);letter-spacing:2px;margin-bottom:6px}
#sidebar-risk .bar-wrap{display:flex;align-items:center;gap:8px}
#sidebar-risk .bar-track{flex:1;height:4px;background:var(--bg);border:1px solid var(--border)}
#sidebar-risk .bar-fill{height:100%;transition:width 1s,background 1s}
#sidebar-foot{padding:10px 14px;border-top:1px solid var(--border);display:flex;
  align-items:center;justify-content:space-between;font-size:10px;color:var(--muted)}
.pulse-dot{width:8px;height:8px;border-radius:50%;background:var(--safe);
  box-shadow:0 0 6px var(--safe);animation:pulse-dot 2s ease-in-out infinite}
@keyframes pulse-dot{0%,100%{opacity:1;transform:scale(1)}50%{opacity:0.6;transform:scale(0.85)}}

/* Main */
#main{flex:1;overflow-y:auto;background:var(--bg)}
.page{display:none;padding:24px;max-width:1400px}
.page.active{display:block}
.page-header{border-bottom:1px solid var(--border);padding-bottom:16px;margin-bottom:20px;
  display:flex;align-items:flex-start;justify-content:space-between;flex-wrap:wrap;gap:12px}
.page-title{font-size:20px;font-weight:bold;letter-spacing:2px;color:var(--primary)}
.page-sub{font-size:10px;color:var(--muted);letter-spacing:3px;margin-top:4px}

/* Cards */
.card{background:var(--card);border:1px solid var(--border)}
.card-header{padding:10px 14px;border-bottom:1px solid var(--border);background:rgba(0,0,0,0.3);
  font-size:10px;letter-spacing:2px;color:var(--muted);display:flex;align-items:center;gap:8px}
.grid-2{display:grid;grid-template-columns:1fr 1fr;gap:12px}
.grid-3{display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px}
.grid-4{display:grid;grid-template-columns:repeat(4,1fr);gap:12px}

/* Stat cards */
.stat-card{padding:16px;display:flex;align-items:center;gap:14px}
.stat-card .icon{font-size:28px;flex-shrink:0}
.stat-card .val{font-size:28px;font-weight:bold}
.stat-card .lbl{font-size:9px;color:var(--muted);letter-spacing:2px;margin-top:2px}

/* Risk gauge */
#gauge-wrap{display:flex;flex-direction:column;align-items:center;justify-content:center;padding:20px 16px}
#gauge-svg{width:180px;height:180px}
#gauge-score{font-size:52px;font-weight:bold;text-anchor:middle;font-family:'Courier New',monospace}
#gauge-level{font-size:11px;text-anchor:middle;letter-spacing:3px;fill:var(--muted)}
.factor-row{display:flex;align-items:center;justify-content:space-between;font-size:11px;
  padding:4px 0;gap:8px}
.factor-bar{flex:1;height:3px;background:var(--bg);border:1px solid var(--border)}
.factor-fill{height:100%;background:var(--primary);transition:width 0.8s}
.factor-pct{width:28px;text-align:right;font-size:10px;color:var(--muted)}

/* Sensors */
.sensor-card{padding:12px 14px;cursor:default;transition:border-color 0.3s}
.sensor-card.status-normal{border-color:var(--border)}
.sensor-card.status-warning{border-color:rgba(245,158,11,0.6);background:rgba(245,158,11,0.05)}
.sensor-card.status-critical{border-color:rgba(239,68,68,0.7);background:rgba(239,68,68,0.07);
  box-shadow:0 0 12px rgba(239,68,68,0.15)}
.sensor-label{font-size:9px;color:var(--muted);letter-spacing:2px;margin-bottom:6px;display:flex;justify-content:space-between}
.sensor-value{font-size:24px;font-weight:bold;line-height:1}
.sensor-unit{font-size:11px;font-weight:normal;color:var(--muted);margin-left:3px}
.sensor-zone{font-size:9px;color:var(--muted);margin-top:5px;letter-spacing:1px}
.sensor-bar{height:3px;background:var(--bg);border:1px solid var(--border);margin-top:8px;overflow:hidden}
.sensor-bar-fill{height:100%;transition:width 1s,background 1s}
.blink-dot{width:6px;height:6px;border-radius:50%;display:inline-block;vertical-align:middle;margin-right:4px}
.blink-dot.critical{background:var(--destructive);animation:blink 0.5s ease-in-out infinite alternate}
.blink-dot.warning{background:var(--warning)}
.blink-dot.normal{background:var(--safe)}
@keyframes blink{from{opacity:1}to{opacity:0.2}}
.trend-up{color:var(--destructive)}
.trend-down{color:var(--safe)}
.trend-stable{color:var(--muted)}

/* Heatmap */
#heatmap-svg{width:100%;border:1px solid var(--border)}
.zone-label{font-size:8px;font-family:'Courier New',monospace;fill:rgba(255,255,255,0.7);
  text-anchor:middle;pointer-events:none}

/* Incidents */
.incident-card{padding:14px;margin-bottom:10px;border:1px solid var(--border);transition:all 0.3s}
.incident-card.severity-critical{background:rgba(239,68,68,0.07);border-color:var(--destructive);
  box-shadow:0 0 16px rgba(239,68,68,0.12)}
.incident-card.severity-high{background:rgba(245,158,11,0.06);border-color:rgba(245,158,11,0.5)}
.incident-card.severity-medium{border-color:rgba(245,158,11,0.3)}
.incident-card.severity-low{opacity:0.75}
.incident-card.status-acknowledged{opacity:0.75;border-color:var(--border)}
.incident-card.status-resolved{opacity:0.4}
.inc-title{font-size:13px;font-weight:bold;margin-bottom:6px}
.inc-meta{font-size:10px;color:var(--muted);display:flex;flex-wrap:wrap;gap:12px}
.inc-meta strong{color:var(--fg)}
.inc-desc{font-size:11px;color:var(--fg2);margin:6px 0 10px}
.inc-actions{display:flex;align-items:center;gap:10px;flex-wrap:wrap}
.inc-ack-info{font-size:10px;color:var(--muted)}
.inc-ack-info strong{color:var(--primary)}

/* Alert card */
.alert-card{padding:12px 14px;margin-bottom:8px;border:1px solid var(--border);
  display:flex;align-items:center;gap:12px}
.alert-card.sev-critical{border-color:var(--destructive);background:rgba(239,68,68,0.07)}
.alert-card.sev-high{border-color:rgba(245,158,11,0.5);background:rgba(245,158,11,0.05)}
.alert-card.sev-medium{border-color:rgba(245,158,11,0.25)}
.alert-icon{font-size:20px;flex-shrink:0}
.alert-body{flex:1;min-width:0}
.alert-title{font-size:12px;font-weight:bold;margin-bottom:3px}
.alert-meta{font-size:10px;color:var(--muted);display:flex;gap:12px;flex-wrap:wrap}
.alert-badge{font-size:10px;padding:1px 6px;border:1px solid;font-weight:bold;flex-shrink:0}
.alert-badge.critical{color:var(--destructive);border-color:var(--destructive)}
.alert-badge.high{color:var(--warning);border-color:var(--warning)}
.alert-badge.medium{color:var(--warning);border-color:rgba(245,158,11,0.4)}
.alert-badge.low{color:var(--muted);border-color:var(--border)}

/* Ticker */
#ticker{overflow:hidden;border:1px solid rgba(239,68,68,0.5);background:rgba(239,68,68,0.05);
  display:flex;align-items:center;margin-bottom:14px}
#ticker-label{background:var(--destructive);color:#fff;padding:6px 12px;font-size:10px;
  letter-spacing:2px;white-space:nowrap;flex-shrink:0}
#ticker-inner{overflow:hidden;flex:1}
#ticker-text{display:inline-block;white-space:nowrap;padding:6px 0;font-size:11px;
  color:var(--destructive);animation:marquee 20s linear infinite;will-change:transform}
@keyframes marquee{from{transform:translateX(100%)}to{transform:translateX(-100%)}}

/* Workers */
.worker-row{display:flex;align-items:center;gap:0;border-bottom:1px solid var(--border);
  padding:10px 0;font-size:11px}
.worker-row:last-child{border-bottom:none}
.worker-col{flex:1;padding:0 8px}
.worker-col.narrow{flex:0 0 90px}
.worker-col.actions{flex:0 0 100px;text-align:right}
.tag{display:inline-block;padding:1px 7px;border:1px solid;font-size:9px;letter-spacing:1px;font-weight:bold}
.tag.on-duty{color:var(--safe);border-color:rgba(34,197,94,0.4)}
.tag.off-duty{color:var(--muted);border-color:var(--border)}
.tag.evacuated{color:var(--destructive);border-color:var(--destructive)}
.tag.compliant{color:var(--safe);border-color:rgba(34,197,94,0.3)}
.tag.violation{color:var(--destructive);border-color:rgba(239,68,68,0.5)}
.tag.unknown{color:var(--muted);border-color:var(--border)}
.tag.day{color:#facc15;border-color:rgba(250,204,21,0.3)}
.tag.night{color:#60a5fa;border-color:rgba(96,165,250,0.3)}
.tag.morning{color:#fb923c;border-color:rgba(251,146,60,0.3)}
.tag.hot-work{color:var(--destructive);border-color:rgba(239,68,68,0.4)}
.tag.confined-space{color:var(--warning);border-color:rgba(245,158,11,0.4)}
.tag.electrical{color:#60a5fa;border-color:rgba(96,165,250,0.4)}
.tag.height-work{color:#a78bfa;border-color:rgba(167,139,250,0.4)}
.tag.chemical{color:#f472b6;border-color:rgba(244,114,182,0.4)}

/* Buttons */
.btn{display:inline-flex;align-items:center;gap:6px;padding:6px 14px;border:1px solid;
  font-family:inherit;font-size:10px;letter-spacing:2px;cursor:pointer;
  text-transform:uppercase;transition:all 0.15s;background:transparent}
.btn-primary{border-color:var(--primary);color:var(--primary)}
.btn-primary:hover{background:rgba(232,160,32,0.15)}
.btn-danger{border-color:var(--destructive);color:var(--destructive)}
.btn-danger:hover{background:rgba(239,68,68,0.15)}
.btn-sm{padding:3px 10px;font-size:9px}
.btn-muted{border-color:var(--border);color:var(--muted)}
.btn-muted:hover{background:rgba(255,255,255,0.05);color:var(--fg)}
.btn-success{border-color:var(--safe);color:var(--safe)}
.btn-success:hover{background:rgba(34,197,94,0.1)}
.btn-off{border-color:var(--border);color:var(--muted)}
.btn-off:hover{background:rgba(255,255,255,0.05)}

/* Modal */
.modal-overlay{position:fixed;inset:0;background:rgba(0,0,0,0.75);z-index:500;
  display:none;align-items:center;justify-content:center;padding:20px}
.modal-overlay.open{display:flex}
.modal{background:var(--card);border:1px solid var(--border);width:100%;max-width:460px;padding:24px}
.modal-title{font-size:13px;font-weight:bold;letter-spacing:2px;color:var(--primary);
  padding-bottom:14px;border-bottom:1px solid var(--border);margin-bottom:16px}
.form-label{font-size:9px;letter-spacing:2px;color:var(--muted);display:block;margin-bottom:6px}
.form-input,.form-textarea{width:100%;background:var(--bg);border:1px solid var(--border);
  color:var(--fg);font-family:inherit;font-size:12px;padding:8px 10px;outline:none;
  transition:border-color 0.2s}
.form-input:focus,.form-textarea:focus{border-color:var(--primary)}
.form-textarea{resize:vertical;min-height:80px}
.form-group{margin-bottom:14px}
.modal-actions{display:flex;gap:10px;margin-top:18px}

/* Permits */
.permit-card{padding:14px;margin-bottom:10px}
.permit-header{display:flex;align-items:center;justify-content:space-between;margin-bottom:8px}
.permit-title{font-size:12px;font-weight:bold}
.permit-meta{font-size:10px;color:var(--muted);display:grid;grid-template-columns:1fr 1fr;gap:4px 16px;margin-top:6px}
.permit-meta span strong{color:var(--fg)}
.risk-flag{display:inline-block;padding:1px 8px;font-size:9px;letter-spacing:2px;font-weight:bold;
  background:rgba(239,68,68,0.15);border:1px solid rgba(239,68,68,0.5);color:var(--destructive)}

/* Filters */
.filter-bar{display:flex;gap:6px;flex-wrap:wrap;margin-bottom:14px;align-items:center}
.filter-btn{padding:4px 12px;border:1px solid var(--border);background:transparent;
  color:var(--muted);font-family:inherit;font-size:10px;letter-spacing:1px;cursor:pointer;transition:all 0.15s}
.filter-btn.active{background:var(--primary);border-color:var(--primary);color:#000;font-weight:bold}
.filter-label{font-size:10px;color:var(--muted);letter-spacing:2px}
select.form-select{background:var(--card);border:1px solid var(--border);color:var(--fg);
  font-family:inherit;font-size:11px;padding:4px 10px;outline:none;cursor:pointer}

/* Risk history sparkline */
#sparkline{width:100%;height:60px}

/* Charts */
.bar-chart{display:flex;flex-direction:column;gap:6px}
.bar-row{display:flex;align-items:center;gap:8px;font-size:10px}
.bar-row .bar-label{width:110px;color:var(--muted);text-align:right;flex-shrink:0;font-size:9px;letter-spacing:1px}
.bar-row .bar-track{flex:1;height:12px;background:var(--bg);border:1px solid var(--border);overflow:hidden}
.bar-row .bar-val{width:20px;color:var(--fg2)}
.bar-row .bar-fill{height:100%;background:var(--primary);transition:width 0.8s}

/* Scrollbars */
*::-webkit-scrollbar{width:4px;height:4px}
*::-webkit-scrollbar-track{background:transparent}
*::-webkit-scrollbar-thumb{background:var(--border);border-radius:2px}
*::-webkit-scrollbar-thumb:hover{background:var(--muted)}

/* Utils */
.c-primary{color:var(--primary)}
.c-destructive{color:var(--destructive)}
.c-warning{color:var(--warning)}
.c-safe{color:var(--safe)}
.c-muted{color:var(--muted)}
.fw-bold{font-weight:bold}
.mb-12{margin-bottom:12px}
.mb-16{margin-bottom:16px}
.mb-20{margin-bottom:20px}
.mt-8{margin-top:8px}
.flex{display:flex}.gap-8{gap:8px}.gap-12{gap:12px}.items-center{align-items:center}
.justify-between{justify-content:space-between}.flex-1{flex:1}.text-right{text-align:right}
.w-full{width:100%}

/* Dashboard layout */
#dash-layout{display:grid;grid-template-columns:1fr 2fr 1.2fr;grid-template-rows:auto auto;gap:12px}
#dash-gauge{grid-row:1/3}
#dash-sensors{grid-column:2/3}
#dash-heatmap{grid-column:2/3}
#dash-incidents{grid-column:3/4;grid-row:1/3;overflow-y:auto;max-height:580px}
@media(max-width:1100px){#dash-layout{grid-template-columns:1fr 1fr}#dash-gauge{grid-row:1}#dash-incidents{grid-column:1/3;grid-row:4;max-height:400px}}

/* Responsive */
@media(max-width:700px){#sidebar{display:none}#dash-layout{grid-template-columns:1fr}}

/* Chart mini sparkline */
.sparkline-path{fill:none;stroke-width:2;stroke-linecap:round;stroke-linejoin:round}
.sparkline-area{stroke:none;opacity:0.15}
</style>
</head>
<body>
<div id="app">

<!-- Emergency Banner -->
<div id="emergency-banner">
  <div style="display:flex;align-items:center;gap:12px">
    <span style="font-size:18px;animation:blink 0.4s step-end infinite alternate">&#9888;</span>
    <span>&#9608; PLANT EMERGENCY &#9608; — COMPOUND RISK LEVEL: CRITICAL — INITIATE EVACUATION PROTOCOL</span>
  </div>
  <button onclick="resolveEmergency()">RESOLVE EMERGENCY</button>
</div>

<!-- Emergency border overlay -->
<div id="emergency-overlay" class="emergency-border" style="display:none"></div>

<!-- Layout -->
<div id="layout">
  <!-- Sidebar -->
  <aside id="sidebar">
    <div id="sidebar-logo">
      <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="color:var(--primary)"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
      <div><div class="brand">I.S.I. Platform</div><div class="sub">Safety Intelligence</div></div>
    </div>
    <nav id="sidebar-nav">
      <div class="nav-section">Operations</div>
      <a class="nav-item active" data-page="dashboard" href="#dashboard">
        <span>&#9632;</span> DASHBOARD
      </a>
      <a class="nav-item" data-page="alerts" href="#alerts">
        <span>&#9670;</span> ALERTS <span class="badge" id="nav-alert-count">0</span>
      </a>
      <a class="nav-item" data-page="incidents" href="#incidents">
        <span>&#9650;</span> INCIDENTS
      </a>
      <div class="nav-section">Monitoring</div>
      <a class="nav-item" data-page="sensors" href="#sensors">
        <span>&#9642;</span> SENSORS
      </a>
      <a class="nav-item" data-page="permits" href="#permits">
        <span>&#9644;</span> PERMITS
      </a>
      <div class="nav-section">Personnel</div>
      <a class="nav-item" data-page="workers" href="#workers">
        <span>&#9673;</span> WORKERS
      </a>
    </nav>
    <div id="sidebar-risk">
      <div class="label">COMPOUND RISK INDEX</div>
      <div class="bar-wrap">
        <div class="bar-track" style="flex:1"><div class="bar-fill" id="sidebar-risk-bar" style="width:0%"></div></div>
        <span id="sidebar-risk-val" style="font-size:11px;font-weight:bold;width:24px;text-align:right">0</span>
      </div>
    </div>
    <div id="sidebar-foot">
      <span style="font-size:10px;letter-spacing:2px">SYS.ONLINE</span>
      <div class="pulse-dot"></div>
    </div>
  </aside>

  <!-- Main -->
  <main id="main">

    <!-- DASHBOARD -->
    <div id="page-dashboard" class="page active">
      <div class="page-header">
        <div><div class="page-title">Command Center</div><div class="page-sub">Global Safety Overview</div></div>
        <div id="dash-clock" style="font-size:12px;color:var(--muted);text-align:right;letter-spacing:1px"></div>
      </div>
      <div id="dash-layout">
        <!-- Gauge -->
        <div id="dash-gauge" class="card">
          <div class="card-header">&#9670; Compound Risk Index</div>
          <div id="gauge-wrap">
            <svg id="gauge-svg" viewBox="0 0 200 200">
              <circle cx="100" cy="100" r="80" fill="none" stroke="var(--border)" stroke-width="10"/>
              <circle id="gauge-circle" cx="100" cy="100" r="80" fill="none" stroke="var(--primary)"
                stroke-width="14" stroke-linecap="round"
                stroke-dasharray="502.65" stroke-dashoffset="502.65"
                transform="rotate(-90 100 100)" style="transition:all 1s ease-out"/>
              <text id="gauge-score" x="100" y="108" fill="var(--primary)" font-size="46" font-weight="bold"
                text-anchor="middle" font-family="Courier New,monospace">0</text>
              <text id="gauge-level" x="100" y="130" fill="var(--muted)" font-size="11"
                text-anchor="middle" font-family="Courier New,monospace" letter-spacing="3">LOW</text>
            </svg>
            <div id="gauge-factors" style="width:100%;padding:0 8px"></div>
            <div class="card-header" style="width:100%;margin-top:10px">&#9642; Risk History</div>
            <svg id="sparkline" viewBox="0 0 300 60" preserveAspectRatio="none"></svg>
          </div>
        </div>

        <!-- Sensor Strip -->
        <div id="dash-sensors" class="card">
          <div class="card-header">&#9642; Live Sensor Readings</div>
          <div id="sensor-strip" style="display:grid;grid-template-columns:repeat(6,1fr);gap:1px;background:var(--border)"></div>
        </div>

        <!-- Heatmap -->
        <div id="dash-heatmap" class="card">
          <div class="card-header">&#9632; Facility Topography
            <span style="margin-left:auto;display:flex;gap:10px;font-size:9px">
              <span style="color:var(--safe)">&#9632; Safe</span>
              <span style="color:var(--warning)">&#9632; High Risk</span>
              <span style="color:var(--destructive)">&#9632; Critical</span>
            </span>
          </div>
          <svg id="heatmap-svg" viewBox="0 0 500 280" style="background:rgba(0,0,0,0.3)"></svg>
        </div>

        <!-- Incident Feed -->
        <div id="dash-incidents" class="card">
          <div class="card-header">
            &#9650; Active Incident Log
            <span class="badge" id="dash-inc-count" style="margin-left:auto;background:var(--destructive);color:#fff;font-size:9px;padding:1px 5px">0</span>
          </div>
          <div id="dash-inc-list" style="padding:10px"></div>
        </div>
      </div>

      <!-- Permits Row -->
      <div class="card mb-12" style="margin-top:12px">
        <div class="card-header">&#9644; Active Work Permits — <span id="dash-permit-count">0</span> ACTIVE</div>
        <div id="dash-permit-strip" style="display:grid;grid-template-columns:repeat(3,1fr);gap:1px;background:var(--border)"></div>
      </div>
    </div>

    <!-- ALERTS -->
    <div id="page-alerts" class="page">
      <div class="page-header">
        <div>
          <div class="page-title" style="display:flex;align-items:center;gap:10px">
            <span id="alerts-radio" style="font-size:20px">&#9670;</span> Live Alert Feed
          </div>
          <div class="page-sub">Real-Time Safety Signal Monitor</div>
        </div>
        <div style="display:flex;gap:10px">
          <div class="card" style="padding:8px 14px;font-size:11px">
            <span id="alerts-critical-count" class="c-destructive fw-bold">0</span> <span class="c-muted">CRITICAL</span>
          </div>
          <div class="card" style="padding:8px 14px;font-size:11px">
            <span id="alerts-active-count" class="fw-bold">0</span> <span class="c-muted">ACTIVE</span>
          </div>
        </div>
      </div>
      <div id="ticker" style="display:none">
        <div id="ticker-label">&#9650; CRITICAL</div>
        <div id="ticker-inner"><span id="ticker-text"></span></div>
      </div>
      <div id="alerts-list"></div>
    </div>

    <!-- INCIDENTS -->
    <div id="page-incidents" class="page">
      <div class="page-header">
        <div><div class="page-title">Incident Log</div><div class="page-sub">Comprehensive Alert History</div></div>
        <div class="filter-bar" style="margin-bottom:0">
          <span class="filter-label">FILTER:</span>
          <button class="filter-btn active" onclick="filterIncidents('all',this)">ALL</button>
          <button class="filter-btn" onclick="filterIncidents('active',this)">ACTIVE</button>
          <button class="filter-btn" onclick="filterIncidents('acknowledged',this)">ACK</button>
          <button class="filter-btn" onclick="filterIncidents('resolved',this)">RESOLVED</button>
        </div>
      </div>
      <!-- Stats -->
      <div class="grid-4 mb-16">
        <div class="card stat-card">
          <div class="icon c-primary">&#9650;</div>
          <div><div class="val" id="inc-stat-total">0</div><div class="lbl">TOTAL</div></div>
        </div>
        <div class="card stat-card">
          <div class="icon c-destructive">&#9632;</div>
          <div><div class="val c-destructive" id="inc-stat-active">0</div><div class="lbl">ACTIVE</div></div>
        </div>
        <div class="card stat-card">
          <div class="icon c-warning">&#9670;</div>
          <div><div class="val c-warning" id="inc-stat-ack">0</div><div class="lbl">ACKNOWLEDGED</div></div>
        </div>
        <div class="card stat-card">
          <div class="icon c-safe">&#10003;</div>
          <div><div class="val c-safe" id="inc-stat-res">0</div><div class="lbl">RESOLVED</div></div>
        </div>
      </div>
      <!-- Bar charts row -->
      <div class="grid-2 mb-16">
        <div class="card" style="padding:14px">
          <div class="card-header" style="margin:-14px -14px 12px;padding:10px 14px">By Severity</div>
          <div id="inc-chart-severity" class="bar-chart"></div>
        </div>
        <div class="card" style="padding:14px">
          <div class="card-header" style="margin:-14px -14px 12px;padding:10px 14px">By Type</div>
          <div id="inc-chart-type" class="bar-chart"></div>
        </div>
      </div>
      <div id="incidents-list"></div>
    </div>

    <!-- SENSORS -->
    <div id="page-sensors" class="page">
      <div class="page-header">
        <div><div class="page-title">Sensor Monitor</div><div class="page-sub">IoT Device Status &amp; Readings</div></div>
        <div style="display:flex;gap:8px">
          <div class="card" style="padding:6px 12px;font-size:10px"><span id="s-stat-total" class="fw-bold">0</span> <span class="c-muted">TOTAL</span></div>
          <div class="card" style="padding:6px 12px;font-size:10px"><span id="s-stat-normal" class="c-safe fw-bold">0</span> <span class="c-muted">NORMAL</span></div>
          <div class="card" style="padding:6px 12px;font-size:10px"><span id="s-stat-warn" class="c-warning fw-bold">0</span> <span class="c-muted">WARNING</span></div>
          <div class="card" style="padding:6px 12px;font-size:10px"><span id="s-stat-crit" class="c-destructive fw-bold">0</span> <span class="c-muted">CRITICAL</span></div>
        </div>
      </div>
      <div id="sensors-grid" style="display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:12px"></div>
    </div>

    <!-- PERMITS -->
    <div id="page-permits" class="page">
      <div class="page-header">
        <div><div class="page-title">Work Permits</div><div class="page-sub">Digital Permit Intelligence</div></div>
        <div class="filter-bar" style="margin-bottom:0">
          <button class="filter-btn active" onclick="filterPermits('all',this)">ALL</button>
          <button class="filter-btn" onclick="filterPermits('active',this)">ACTIVE</button>
          <button class="filter-btn" onclick="filterPermits('expired',this)">EXPIRED</button>
        </div>
      </div>
      <div id="permits-list" style="display:grid;grid-template-columns:repeat(auto-fill,minmax(340px,1fr));gap:12px"></div>
    </div>

    <!-- WORKERS -->
    <div id="page-workers" class="page">
      <div class="page-header">
        <div><div class="page-title">Worker Tracking</div><div class="page-sub">Personnel Status &amp; Safety Compliance</div></div>
        <div class="card" style="padding:8px 14px;font-size:11px">
          <span id="workers-on-site" class="fw-bold c-primary">0</span> <span class="c-muted">WORKERS ON SITE</span>
        </div>
      </div>
      <div class="grid-4 mb-16">
        <div class="card stat-card"><div class="icon">&#9673;</div><div><div class="val" id="w-stat-total">0</div><div class="lbl">REGISTERED</div></div></div>
        <div class="card stat-card"><div class="icon c-safe">&#10003;</div><div><div class="val c-safe" id="w-stat-on">0</div><div class="lbl">ON DUTY</div></div></div>
        <div class="card stat-card"><div class="icon c-muted">&#9711;</div><div><div class="val c-muted" id="w-stat-off">0</div><div class="lbl">OFF DUTY</div></div></div>
        <div class="card stat-card"><div class="icon c-destructive">&#9650;</div><div><div class="val c-destructive" id="w-stat-ppe">0</div><div class="lbl">PPE VIOLATIONS</div></div></div>
      </div>
      <div class="grid-2 mb-16">
        <div class="card" style="padding:14px">
          <div style="font-size:10px;color:var(--muted);letter-spacing:2px;margin-bottom:12px">Workers by Zone (On Duty)</div>
          <div id="workers-zone-chart" class="bar-chart"></div>
        </div>
        <div class="card" style="padding:14px">
          <div style="font-size:10px;color:var(--muted);letter-spacing:2px;margin-bottom:12px">Filter Personnel</div>
          <div class="filter-bar mb-12">
            <button class="filter-btn active" onclick="filterWorkers('all',this)">ALL</button>
            <button class="filter-btn" onclick="filterWorkers('on_duty',this)">ON DUTY</button>
            <button class="filter-btn" onclick="filterWorkers('off_duty',this)">OFF DUTY</button>
          </div>
          <div style="font-size:10px;color:var(--muted);letter-spacing:2px;margin-bottom:6px">Zone Filter</div>
          <select class="form-select w-full" id="worker-zone-filter" onchange="renderWorkers()">
            <option value="all">ALL ZONES</option>
          </select>
        </div>
      </div>
      <div class="card">
        <div class="card-header">&#9673; Personnel Registry — <span id="workers-count">0</span> Records</div>
        <div style="padding:0 14px">
          <div class="worker-row" style="border-bottom:1px solid var(--border);font-size:9px;color:var(--muted);letter-spacing:2px">
            <div class="worker-col narrow">ID</div>
            <div class="worker-col">NAME / ROLE</div>
            <div class="worker-col">ZONE</div>
            <div class="worker-col narrow">SHIFT</div>
            <div class="worker-col narrow">STATUS</div>
            <div class="worker-col narrow">PPE</div>
            <div class="worker-col actions">ACTIONS</div>
          </div>
          <div id="workers-list"></div>
        </div>
      </div>
    </div>

  </main>
</div>

<!-- Acknowledge Modal -->
<div class="modal-overlay" id="ack-modal">
  <div class="modal">
    <div class="modal-title">Acknowledge Incident</div>
    <div id="ack-incident-info" style="background:var(--bg);padding:10px;margin-bottom:16px;font-size:11px;color:var(--muted);border-left:3px solid var(--primary)"></div>
    <div class="form-group">
      <label class="form-label">Safety Officer Name *</label>
      <input class="form-input" id="ack-name" type="text" placeholder="Enter your full name">
    </div>
    <div class="form-group">
      <label class="form-label">Remarks / Action Taken *</label>
      <textarea class="form-textarea" id="ack-note" placeholder="Describe the action taken or observation..."></textarea>
    </div>
    <div class="modal-actions">
      <button class="btn btn-primary" onclick="submitAck()" style="flex:1">CONFIRM ACKNOWLEDGE</button>
      <button class="btn btn-muted" onclick="closeModal('ack-modal')">CANCEL</button>
    </div>
  </div>
</div>

<!-- Check-In Modal -->
<div class="modal-overlay" id="checkin-modal">
  <div class="modal">
    <div class="modal-title">Worker Check-In</div>
    <div id="checkin-worker-info" style="background:var(--bg);padding:10px;margin-bottom:16px;font-size:11px;color:var(--muted);border-left:3px solid var(--primary)"></div>
    <div class="form-group">
      <label class="form-label">Assign to Zone</label>
      <select class="form-select w-full" id="checkin-zone" style="padding:8px 10px;font-size:12px"></select>
    </div>
    <div class="modal-actions">
      <button class="btn btn-success" onclick="confirmCheckIn()" style="flex:1">CONFIRM CHECK-IN</button>
      <button class="btn btn-muted" onclick="closeModal('checkin-modal')">CANCEL</button>
    </div>
  </div>
</div>

</div>

<script>
// ============================================================
// DATA DEFINITIONS
// ============================================================

const ZONES = [
  'Coke Oven Battery','Gas Processing Unit','Chemical Storage',
  'Boiler Room','Control Room','Assembly Bay',
  'Maintenance Workshop','Loading Dock','Cooling Towers'
];

const HEATMAP_ZONES = [
  {id:1,name:'Coke Oven Battery',x:5,y:5,w:24,h:30},
  {id:2,name:'Gas Processing',x:32,y:5,w:24,h:30},
  {id:3,name:'Chemical Storage',x:60,y:5,w:28,h:20},
  {id:4,name:'Boiler Room',x:5,y:40,w:20,h:24},
  {id:5,name:'Control Room',x:30,y:40,w:20,h:24},
  {id:6,name:'Assembly Bay',x:54,y:30,w:20,h:28},
  {id:7,name:'Maint. Workshop',x:5,y:70,w:28,h:24},
  {id:8,name:'Loading Dock',x:38,y:70,w:24,h:24},
  {id:9,name:'Cooling Towers',x:68,y:62,w:26,h:30}
];

// ============================================================
// STATE
// ============================================================

const state = {
  riskScore: 0,
  riskLevel: 'low',
  riskHistory: Array(30).fill(0),
  isEmergency: false,
  incidentFilter: 'all',
  permitFilter: 'all',
  workerFilter: 'all',
  pendingAckId: null,
  pendingCheckInId: null,

  sensors: [
    {id:1,name:'H2S Detector A1',type:'GAS',zone:'Coke Oven Battery',value:18.4,unit:'ppm',threshold:10,min:0,max:30,status:'critical',trend:'rising'},
    {id:2,name:'CO Monitor B2',type:'GAS',zone:'Gas Processing Unit',value:42.1,unit:'ppm',threshold:50,min:0,max:80,status:'warning',trend:'rising'},
    {id:3,name:'Temp Sensor C3',type:'TEMP',zone:'Boiler Room',value:312.5,unit:'°C',threshold:280,min:200,max:400,status:'critical',trend:'rising'},
    {id:4,name:'Pressure Gauge D4',type:'PRES',zone:'Gas Processing Unit',value:8.2,unit:'bar',threshold:9,min:0,max:15,status:'warning',trend:'stable'},
    {id:5,name:'O2 Monitor E5',type:'O2',zone:'Coke Oven Battery',value:17.1,unit:'%',threshold:18,min:14,max:22,status:'warning',trend:'falling',inverted:true},
    {id:6,name:'Vibration F6',type:'VIB',zone:'Boiler Room',value:12.3,unit:'mm/s',threshold:15,min:0,max:25,status:'normal',trend:'stable'},
    {id:7,name:'H2 Sensor G7',type:'GAS',zone:'Chemical Storage',value:4.8,unit:'%LEL',threshold:10,min:0,max:20,status:'normal',trend:'stable'},
    {id:8,name:'Temp Sensor H8',type:'TEMP',zone:'Assembly Bay',value:38.2,unit:'°C',threshold:60,min:20,max:80,status:'normal',trend:'stable'},
    {id:9,name:'CO2 Monitor I9',type:'GAS',zone:'Maint. Workshop',value:890,unit:'ppm',threshold:1000,min:400,max:1500,status:'normal',trend:'stable'},
    {id:10,name:'Pressure J10',type:'PRES',zone:'Boiler Room',value:14.7,unit:'bar',threshold:12,min:0,max:20,status:'critical',trend:'rising'},
    {id:11,name:'Humidity K11',type:'HUM',zone:'Control Room',value:68.5,unit:'%RH',threshold:80,min:30,max:100,status:'normal',trend:'stable'},
    {id:12,name:'Vibration L12',type:'VIB',zone:'Cooling Towers',value:7.4,unit:'mm/s',threshold:8,min:0,max:15,status:'warning',trend:'rising'}
  ],

  incidents: [
    {id:1,title:'Critical H2S Leak Detected',desc:'Hydrogen sulfide at Coke Oven Battery A1 has exceeded critical threshold of 10 ppm. Immediate evacuation protocol required.',severity:'critical',status:'active',zone:'Coke Oven Battery',type:'gas_leak',riskScore:85,triggeredAt:Date.now()-12*60000,acknowledgedAt:null,acknowledgedBy:null,acknowledgeNote:null},
    {id:2,title:'Boiler Pressure Anomaly',desc:'Pressure gauge J10 reading 14.7 bar, exceeding safe limit of 12 bar. Compound risk with elevated temperature.',severity:'critical',status:'active',zone:'Boiler Room',type:'pressure_anomaly',riskScore:78,triggeredAt:Date.now()-8*60000,acknowledgedAt:null,acknowledgedBy:null,acknowledgeNote:null},
    {id:3,title:'High Temperature Alert',desc:'Temperature sensor C3 recording 312.5°C in Boiler Room, 11.6% above critical threshold.',severity:'high',status:'acknowledged',zone:'Boiler Room',type:'temperature_spike',riskScore:62,triggeredAt:Date.now()-120*60000,acknowledgedAt:Date.now()-90*60000,acknowledgedBy:'Rajesh Kumar',acknowledgeNote:'Cooling cycle initiated. Monitoring for next 30 minutes.'},
    {id:4,title:'Compound Risk: Hot Work + Gas',desc:'Simultaneous hot work permit active in Coke Oven Battery while H2S levels are elevated. High ignition risk.',severity:'critical',status:'active',zone:'Coke Oven Battery',type:'compound_risk',riskScore:92,triggeredAt:Date.now()-5*60000,acknowledgedAt:null,acknowledgedBy:null,acknowledgeNote:null},
    {id:5,title:'O2 Below Safe Threshold',desc:'Oxygen levels dropping to 17.1% in Coke Oven Battery, approaching confined space danger zone.',severity:'high',status:'active',zone:'Coke Oven Battery',type:'gas_leak',riskScore:71,triggeredAt:Date.now()-18*60000,acknowledgedAt:null,acknowledgedBy:null,acknowledgeNote:null},
    {id:6,title:'Cooling Tower Vibration',desc:'Vibration sensor L12 approaching warning threshold. Possible bearing wear or imbalance in fan assembly.',severity:'medium',status:'acknowledged',zone:'Cooling Towers',type:'equipment_failure',riskScore:35,triggeredAt:Date.now()-240*60000,acknowledgedAt:Date.now()-180*60000,acknowledgedBy:'Priya Sharma',acknowledgeNote:'Maintenance team dispatched. Inspection scheduled.'},
    {id:7,title:'CO Concentration Warning',desc:'Carbon monoxide at 42.1 ppm trending upward — 84% of critical threshold. Ventilation check required.',severity:'medium',status:'active',zone:'Gas Processing Unit',type:'gas_leak',riskScore:45,triggeredAt:Date.now()-25*60000,acknowledgedAt:null,acknowledgedBy:null,acknowledgeNote:null},
    {id:8,title:'Permit Violation: Expired Order',desc:'Chemical handling permit in Chemical Storage zone has exceeded authorized timeframe.',severity:'medium',status:'resolved',zone:'Chemical Storage',type:'permit_violation',riskScore:28,triggeredAt:Date.now()-360*60000,acknowledgedAt:Date.now()-300*60000,acknowledgedBy:'Vikram Nair',acknowledgeNote:'Permit renewed. Work resumed under new authorization.'}
  ],

  permits: [
    {id:1,type:'hot_work',zone:'Coke Oven Battery',issuedTo:'Arjun Mehta',issuedAt:Date.now()-120*60000,expiresAt:Date.now()+240*60000,status:'active',desc:'Welding on coke oven door frame. Gas monitoring mandatory.',riskFlag:true},
    {id:2,type:'confined_space',zone:'Gas Processing Unit',issuedTo:'Suresh Iyer',issuedAt:Date.now()-60*60000,expiresAt:Date.now()+360*60000,status:'active',desc:'Inspection of gas separator vessel. Atmosphere monitoring mandatory.',riskFlag:true},
    {id:3,type:'electrical',zone:'Control Room',issuedTo:'Deepak Rao',issuedAt:Date.now()-30*60000,expiresAt:Date.now()+480*60000,status:'active',desc:'Replacement of faulty PLC module in main safety control panel.',riskFlag:false},
    {id:4,type:'chemical_handling',zone:'Chemical Storage',issuedTo:'Anita Verma',issuedAt:Date.now()-180*60000,expiresAt:Date.now()+60*60000,status:'active',desc:'Transfer of chlorine compounds. Full PPE mandatory.',riskFlag:true},
    {id:5,type:'height_work',zone:'Cooling Towers',issuedTo:'Manoj Singh',issuedAt:Date.now()-240*60000,expiresAt:Date.now()+120*60000,status:'active',desc:'Inspection of fan blades at 25m elevation. Safety harness required.',riskFlag:false},
    {id:6,type:'confined_space',zone:'Coke Oven Battery',issuedTo:'Ramesh Pillai',issuedAt:Date.now()-480*60000,expiresAt:Date.now()-60*60000,status:'expired',desc:'Cleaning of coke oven battery chamber. Operations completed.',riskFlag:true}
  ],

  workers: [
    {id:1,name:'Arjun Mehta',emp:'EMP-0012',role:'Welding Technician',zone:'Coke Oven Battery',shift:'day',status:'on_duty',ppe:'compliant',checkInAt:Date.now()-120*60000},
    {id:2,name:'Suresh Iyer',emp:'EMP-0034',role:'Gas Safety Officer',zone:'Gas Processing Unit',shift:'day',status:'on_duty',ppe:'compliant',checkInAt:Date.now()-60*60000},
    {id:3,name:'Priya Sharma',emp:'EMP-0056',role:'Safety Engineer',zone:'Control Room',shift:'day',status:'on_duty',ppe:'compliant',checkInAt:Date.now()-180*60000},
    {id:4,name:'Deepak Rao',emp:'EMP-0078',role:'Electrical Engineer',zone:'Control Room',shift:'day',status:'on_duty',ppe:'violation',checkInAt:Date.now()-30*60000},
    {id:5,name:'Anita Verma',emp:'EMP-0091',role:'Chemical Handler',zone:'Chemical Storage',shift:'day',status:'on_duty',ppe:'compliant',checkInAt:Date.now()-180*60000},
    {id:6,name:'Manoj Singh',emp:'EMP-0102',role:'Maintenance Technician',zone:'Cooling Towers',shift:'day',status:'on_duty',ppe:'unknown',checkInAt:Date.now()-240*60000},
    {id:7,name:'Ramesh Pillai',emp:'EMP-0115',role:'Process Operator',zone:'Off-Site',shift:'night',status:'off_duty',ppe:'unknown',checkInAt:null},
    {id:8,name:'Vikram Nair',emp:'EMP-0134',role:'HSE Manager',zone:'Boiler Room',shift:'day',status:'on_duty',ppe:'compliant',checkInAt:Date.now()-300*60000},
    {id:9,name:'Kavitha Reddy',emp:'EMP-0149',role:'Instrument Technician',zone:'Off-Site',shift:'morning',status:'off_duty',ppe:'unknown',checkInAt:null},
    {id:10,name:'Sanjay Kumar',emp:'EMP-0162',role:'Boiler Operator',zone:'Boiler Room',shift:'day',status:'on_duty',ppe:'violation',checkInAt:Date.now()-120*60000},
    {id:11,name:'Lalitha Menon',emp:'EMP-0175',role:'Safety Officer',zone:'Assembly Bay',shift:'day',status:'on_duty',ppe:'compliant',checkInAt:Date.now()-60*60000},
    {id:12,name:'Raghav Joshi',emp:'EMP-0189',role:'Crane Operator',zone:'Off-Site',shift:'night',status:'off_duty',ppe:'unknown',checkInAt:null},
    {id:13,name:'Fatima Sheikh',emp:'EMP-0201',role:'Lab Technician',zone:'Maint. Workshop',shift:'morning',status:'on_duty',ppe:'compliant',checkInAt:Date.now()-60*60000},
    {id:14,name:'Dinesh Patel',emp:'EMP-0215',role:'Fire & Safety Officer',zone:'Gas Processing Unit',shift:'day',status:'on_duty',ppe:'compliant',checkInAt:Date.now()-120*60000},
    {id:15,name:'Sunita Biswas',emp:'EMP-0228',role:'Environmental Officer',zone:'Off-Site',shift:'day',status:'off_duty',ppe:'unknown',checkInAt:null}
  ]
};

// ============================================================
// AUDIO (Emergency Alarm)
// ============================================================

let alarmCtx = null, alarmOsc = null, alarmGain = null, alarmInterval = null;

function startAlarm() {
  try {
    alarmCtx = new (window.AudioContext || window.webkitAudioContext)();
    alarmOsc = alarmCtx.createOscillator();
    alarmGain = alarmCtx.createGain();
    alarmOsc.connect(alarmGain);
    alarmGain.connect(alarmCtx.destination);
    alarmOsc.frequency.setValueAtTime(880, alarmCtx.currentTime);
    alarmOsc.type = 'square';
    alarmGain.gain.setValueAtTime(0.1, alarmCtx.currentTime);
    alarmOsc.start();
    let on = true;
    alarmInterval = setInterval(() => {
      if (!alarmGain) return;
      on = !on;
      alarmGain.gain.setValueAtTime(on ? 0.1 : 0, alarmCtx.currentTime);
    }, 500);
  } catch(e) {}
}

function stopAlarm() {
  try {
    clearInterval(alarmInterval);
    if (alarmOsc) { alarmOsc.stop(); alarmOsc = null; }
    if (alarmCtx) { alarmCtx.close(); alarmCtx = null; }
    alarmGain = null;
  } catch(e) {}
}

// ============================================================
// ROUTING
// ============================================================

function navigate(pageId) {
  document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
  document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
  const page = document.getElementById('page-' + pageId);
  if (page) page.classList.add('active');
  const nav = document.querySelector('[data-page="' + pageId + '"]');
  if (nav) nav.classList.add('active');
  renderPage(pageId);
}

document.querySelectorAll('.nav-item').forEach(item => {
  item.addEventListener('click', (e) => {
    e.preventDefault();
    navigate(item.dataset.page);
  });
});

function renderPage(pageId) {
  switch(pageId) {
    case 'dashboard': renderDashboard(); break;
    case 'alerts': renderAlerts(); break;
    case 'incidents': renderIncidents(); break;
    case 'sensors': renderSensors(); break;
    case 'permits': renderPermits(); break;
    case 'workers': renderWorkers(); break;
  }
}

// ============================================================
// RISK ENGINE
// ============================================================

function computeRisk() {
  const critical = state.sensors.filter(s => s.status === 'critical');
  const warning  = state.sensors.filter(s => s.status === 'warning');
  const activeInc = state.incidents.filter(i => i.status === 'active');
  const critInc  = activeInc.filter(i => i.severity === 'critical');
  const riskPermits = state.permits.filter(p => p.status === 'active' && p.riskFlag);

  let score = 0;
  const factors = [];

  if (critical.length) {
    const c = Math.min(critical.length * 15, 40);
    score += c;
    factors.push({name:'Critical Sensors', contribution:c});
  }
  if (warning.length) {
    const c = Math.min(warning.length * 5, 20);
    score += c;
    factors.push({name:'Warning Sensors', contribution:c});
  }
  if (critInc.length) {
    const c = Math.min(critInc.length * 20, 40);
    score += c;
    factors.push({name:'Critical Incidents', contribution:c});
  }
  if (riskPermits.length) {
    const c = Math.min(riskPermits.length * 5, 15);
    score += c;
    factors.push({name:'Risk Permits Active', contribution:c});
  }
  if (!factors.length) factors.push({name:'No Active Threats', contribution:0});

  score = Math.min(score, 100);
  const level = score <= 25 ? 'low' : score <= 50 ? 'moderate' : score <= 75 ? 'high' : 'critical';

  state.riskScore = score;
  state.riskLevel = level;
  state.riskHistory.push(score);
  if (state.riskHistory.length > 30) state.riskHistory.shift();

  const wasEmergency = state.isEmergency;
  state.isEmergency = score >= 100;
  if (state.isEmergency && !wasEmergency) startAlarm();
  if (!state.isEmergency && wasEmergency) stopAlarm();

  return { score, level, factors };
}

// ============================================================
// SIMULATION ENGINE
// ============================================================

function simulateSensors() {
  state.sensors.forEach(s => {
    const drift = (Math.random() - 0.45) * (s.max - s.min) * 0.025;
    s.value = Math.max(s.min, Math.min(s.max, s.value + drift));
    s.value = Math.round(s.value * 10) / 10;
    const pct = s.inverted
      ? (s.threshold - s.value) / (s.threshold - s.min)
      : s.value / s.threshold;
    s.status = s.inverted
      ? (s.value <= s.threshold * 0.9 ? 'critical' : s.value <= s.threshold ? 'warning' : 'normal')
      : (pct >= 1 ? 'critical' : pct >= 0.8 ? 'warning' : 'normal');
    s.trend = drift > 0.1 ? 'rising' : drift < -0.1 ? 'falling' : 'stable';
  });
}

// ============================================================
// RENDER UTILITIES
// ============================================================

const fmt = {
  timeAgo(ts) {
    const d = (Date.now() - ts) / 1000;
    if (d < 60) return Math.floor(d) + 's ago';
    if (d < 3600) return Math.floor(d/60) + 'm ago';
    return Math.floor(d/3600) + 'h ago';
  },
  time(ts) {
    const d = new Date(ts);
    return d.toTimeString().slice(0,8) + ' ' + d.toDateString().slice(4,10);
  },
  duration(ms) {
    const h = Math.floor(ms/3600000), m = Math.floor((ms%3600000)/60000);
    return h > 0 ? h+'h '+m+'m' : m+'m';
  }
};

function severityColor(s) {
  return s==='critical'?'var(--destructive)':s==='high'?'var(--warning)':s==='medium'?'var(--warning)':'var(--muted)';
}
function statusBadge(s) {
  const cfg = {active:'c-destructive',acknowledged:'c-warning',resolved:'c-safe',expired:'c-muted'};
  return `<span class="${cfg[s]||'c-muted'}" style="font-weight:bold;font-size:10px;letter-spacing:1px">${s.toUpperCase()}</span>`;
}
function typeLabel(t) { return (t||'').replace(/_/g,' ').toUpperCase(); }
function permitTypeClass(t) {
  const m={hot_work:'hot-work',confined_space:'confined-space',electrical:'electrical',height_work:'height-work',chemical_handling:'chemical'};
  return m[t]||'';
}

// ============================================================
// EMERGENCY UI
// ============================================================

function updateEmergencyUI() {
  const banner = document.getElementById('emergency-banner');
  const overlay = document.getElementById('emergency-overlay');
  if (state.isEmergency) {
    banner.classList.add('active');
    overlay.style.display = 'block';
  } else {
    banner.classList.remove('active');
    overlay.style.display = 'none';
  }
}

function resolveEmergency() {
  state.isEmergency = false;
  stopAlarm();
  updateEmergencyUI();
  // Force sensors back toward normal
  state.sensors.forEach(s => {
    if (s.status === 'critical') s.value = s.threshold * 0.85;
  });
}

// ============================================================
// DASHBOARD
// ============================================================

function renderDashboard() {
  const { score, level, factors } = computeRisk();
  updateEmergencyUI();

  // Clock
  const now = new Date();
  document.getElementById('dash-clock').innerHTML =
    `SYSTEM TIME<br><span style="color:var(--primary);font-size:14px">${now.toISOString().replace('T',' ').slice(0,19)} IST</span>`;

  // Gauge
  const circ = 2 * Math.PI * 80;
  const offset = circ - (score / 100) * circ;
  const gc = document.getElementById('gauge-circle');
  const gcolor = score >= 100 ? 'var(--destructive)' : score >= 75 ? 'var(--destructive)' : score >= 50 ? 'var(--warning)' : score >= 25 ? 'var(--primary)' : 'var(--safe)';
  gc.setAttribute('stroke-dashoffset', offset);
  gc.style.stroke = gcolor;
  document.getElementById('gauge-score').textContent = score;
  document.getElementById('gauge-score').setAttribute('fill', gcolor);
  document.getElementById('gauge-level').textContent = level.toUpperCase();

  // Factors
  document.getElementById('gauge-factors').innerHTML = factors.map(f => `
    <div class="factor-row">
      <span style="font-size:10px;color:var(--muted);flex:1;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">${f.name}</span>
      <div class="factor-bar" style="width:60px;margin:0 6px"><div class="factor-fill" style="width:${f.contribution}%;background:${gcolor}"></div></div>
      <span class="factor-pct">${f.contribution}%</span>
    </div>`).join('');

  // Sparkline
  renderSparkline();

  // Sidebar risk
  document.getElementById('sidebar-risk-bar').style.width = score + '%';
  document.getElementById('sidebar-risk-bar').style.background = gcolor;
  document.getElementById('sidebar-risk-val').textContent = score;
  document.getElementById('sidebar-risk-val').style.color = gcolor;

  // Sensor strip (top 6 critical/warning first)
  const sorted = [...state.sensors].sort((a,b)=>{
    const o={critical:0,warning:1,normal:2};return(o[a.status]||2)-(o[b.status]||2);
  });
  document.getElementById('sensor-strip').innerHTML = sorted.slice(0,6).map(s => {
    const pct = Math.min(100, (s.inverted ? (s.threshold-s.min)/(s.threshold-s.value)*50 : s.value/s.threshold*100));
    const bc = s.status==='critical'?'var(--destructive)':s.status==='warning'?'var(--warning)':'var(--safe)';
    const tc = s.status==='critical'?'c-destructive':s.status==='warning'?'c-warning':'c-safe';
    return `<div style="background:var(--card);padding:12px 10px;${s.status==='critical'?'box-shadow:inset 0 0 0 1px var(--destructive)':''}">
      <div class="sensor-label"><span>${s.type}</span><span class="${tc}" style="font-size:9px">${s.status.toUpperCase()}</span></div>
      <div style="font-size:20px;font-weight:bold;color:${bc}">${s.value}<span style="font-size:9px;color:var(--muted)"> ${s.unit}</span></div>
      <div style="font-size:9px;color:var(--muted);margin:4px 0">${s.name}</div>
      <div class="sensor-bar"><div class="sensor-bar-fill" style="width:${pct}%;background:${bc}"></div></div>
    </div>`;
  }).join('');

  // Heatmap
  renderHeatmap();

  // Incident feed
  const active = state.incidents.filter(i => i.status !== 'resolved').slice(0,5);
  document.getElementById('dash-inc-count').textContent = state.incidents.filter(i=>i.status==='active').length;
  document.getElementById('dash-inc-list').innerHTML = active.length ? active.map(i => `
    <div style="padding:10px;margin-bottom:8px;border:1px solid ${i.severity==='critical'?'var(--destructive)':i.status==='acknowledged'?'var(--border)':'rgba(245,158,11,0.4)'};
    background:${i.severity==='critical'&&i.status==='active'?'rgba(239,68,68,0.06)':'transparent'};${i.status!=='active'?'opacity:0.7':''}">
      <div style="display:flex;align-items:start;justify-content:space-between;gap:8px">
        <div>
          <div style="font-size:11px;font-weight:bold;color:${i.severity==='critical'?'var(--destructive)':i.severity==='high'?'var(--warning)':'var(--fg)'};margin-bottom:4px">${i.title}</div>
          <div style="font-size:10px;color:var(--muted)">ZONE: <strong style="color:var(--fg)">${i.zone}</strong> &nbsp; ${fmt.timeAgo(i.triggeredAt)}</div>
        </div>
        ${i.status==='active'?`<button class="btn btn-sm btn-primary" onclick="openAck(${i.id})">ACK</button>`:''}
      </div>
    </div>`).join('') : '<div style="padding:20px;text-align:center;font-size:11px;color:var(--muted)">ALL CLEAR</div>';

  // Permit strip
  const activePermits = state.permits.filter(p => p.status === 'active');
  document.getElementById('dash-permit-count').textContent = activePermits.length;
  document.getElementById('dash-permit-strip').innerHTML = activePermits.slice(0,6).map(p => {
    const mins = Math.floor((p.expiresAt - Date.now()) / 60000);
    return `<div style="background:var(--card);padding:12px 10px;${p.riskFlag?'border-left:2px solid var(--destructive)':''}">
      <div style="font-size:9px;color:var(--muted);margin-bottom:4px">
        ${p.riskFlag?'<span class="c-destructive">&#9650; RISK FLAGGED</span>':''}
      </div>
      <div class="tag ${permitTypeClass(p.type)}" style="font-size:9px;margin-bottom:6px">${typeLabel(p.type)}</div>
      <div style="font-size:11px;font-weight:bold;margin-bottom:2px">${p.issuedTo}</div>
      <div style="font-size:10px;color:var(--muted)">${p.zone}</div>
      <div style="font-size:10px;color:${mins<30?'var(--destructive)':'var(--muted)'};margin-top:4px">Exp: ${mins}m</div>
    </div>`;
  }).join('');
}

function renderSparkline() {
  const h = state.riskHistory;
  const max = Math.max(...h, 1);
  const W = 300, H = 60;
  const pts = h.map((v, i) => [
    i * W / (h.length - 1),
    H - (v / max) * (H - 8) - 4
  ]);
  const path = pts.map((p, i) => (i === 0 ? 'M' : 'L') + p[0].toFixed(1) + ' ' + p[1].toFixed(1)).join(' ');
  const area = path + ` L${W} ${H} L0 ${H} Z`;
  const col = state.riskScore >= 75 ? '#ef4444' : state.riskScore >= 50 ? '#f59e0b' : '#e8a020';
  document.getElementById('sparkline').innerHTML = `
    <defs><linearGradient id="sg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="5%" stop-color="${col}" stop-opacity="0.4"/>
      <stop offset="95%" stop-color="${col}" stop-opacity="0"/>
    </linearGradient></defs>
    <path d="${area}" fill="url(#sg)"/>
    <path d="${path}" class="sparkline-path" stroke="${col}"/>`;
}

function renderHeatmap() {
  const svg = document.getElementById('heatmap-svg');
  const W = 500, H = 280;
  const zoneRisk = {};
  state.sensors.forEach(s => {
    const z = s.zone;
    const pts = s.status === 'critical' ? 3 : s.status === 'warning' ? 1 : 0;
    zoneRisk[z] = (zoneRisk[z] || 0) + pts;
  });
  state.incidents.filter(i => i.status === 'active').forEach(i => {
    zoneRisk[i.zone] = (zoneRisk[i.zone] || 0) + (i.severity === 'critical' ? 5 : 2);
  });

  const riskColor = (score) => {
    if (score === 0) return 'rgba(34,197,94,0.2)';
    if (score <= 2) return 'rgba(245,158,11,0.25)';
    if (score <= 5) return 'rgba(249,115,22,0.35)';
    return 'rgba(239,68,68,0.45)';
  };
  const riskStroke = (score) => {
    if (score === 0) return 'rgba(34,197,94,0.6)';
    if (score <= 2) return 'rgba(245,158,11,0.7)';
    if (score <= 5) return 'rgba(249,115,22,0.8)';
    return 'rgba(239,68,68,0.9)';
  };

  svg.innerHTML = HEATMAP_ZONES.map(z => {
    const score = zoneRisk[z.name] || 0;
    const x = z.x/100*W, y = z.y/100*H, w = z.w/100*W, h = z.h/100*H;
    const glow = score >= 6 ? `filter:drop-shadow(0 0 6px rgba(239,68,68,0.6))` : '';
    return `<rect x="${x}" y="${y}" width="${w}" height="${h}"
        fill="${riskColor(score)}" stroke="${riskStroke(score)}" stroke-width="1.5"
        rx="2" style="${glow};cursor:pointer" onclick="alert('${z.name}\\nRisk Score: ${score}\\nSensor Alerts: ${state.sensors.filter(s=>s.zone===z.name&&s.status!=='normal').length}')"/>
      <text x="${x+w/2}" y="${y+h/2-5}" class="zone-label">${z.name}</text>
      <text x="${x+w/2}" y="${y+h/2+10}" class="zone-label" style="font-size:10px;fill:${riskStroke(score)}">${score>0?'RISK:'+score:''}</text>`;
  }).join('');
}

// ============================================================
// ALERTS
// ============================================================

function renderAlerts() {
  const allAlerts = [];
  state.incidents.filter(i => i.status !== 'resolved').forEach(i => {
    allAlerts.push({id:i.id,title:i.title,severity:i.severity,zone:i.zone,type:i.type,
      ts:i.triggeredAt,status:i.status,desc:i.desc,isIncident:true});
  });
  state.sensors.filter(s => s.status !== 'normal').forEach(s => {
    allAlerts.push({id:'s'+s.id,title:s.name+' — '+s.status.toUpperCase(),
      severity:s.status==='critical'?'critical':'medium',zone:s.zone,type:s.type,
      ts:Date.now(),status:'active',desc:`Reading ${s.value}${s.unit} — ${s.status==='critical'?'exceeds':'approaching'} threshold of ${s.threshold}${s.unit}`,isIncident:false});
  });
  allAlerts.sort((a,b) => {
    const o={critical:0,high:1,medium:2,low:3};
    return (o[a.severity]||4)-(o[b.severity]||4);
  });

  const critical = allAlerts.filter(a => a.severity === 'critical');
  document.getElementById('alerts-critical-count').textContent = critical.length;
  document.getElementById('alerts-active-count').textContent = allAlerts.length;
  document.getElementById('nav-alert-count').textContent = allAlerts.length;

  // Ticker
  const ticker = document.getElementById('ticker');
  if (critical.length) {
    ticker.style.display = 'flex';
    document.getElementById('ticker-text').textContent =
      critical.map(a => '  ⬤  ' + a.title + ' — ' + a.zone).join('   ·   ');
  } else {
    ticker.style.display = 'none';
  }

  // Radio pulse
  const radio = document.getElementById('alerts-radio');
  if (critical.length) radio.style.animation = 'blink 0.5s step-end infinite alternate';
  else radio.style.animation = '';

  document.getElementById('alerts-list').innerHTML = allAlerts.length
    ? allAlerts.map(a => `
    <div class="alert-card sev-${a.severity}">
      <div class="alert-icon" style="color:${severityColor(a.severity)}">${
        a.type==='gas_leak'||a.type==='GAS'?'&#9786;':a.type==='temperature_spike'||a.type==='TEMP'?'&#9651;':a.type==='pressure_anomaly'||a.type==='PRES'?'&#9670;':'&#9650;'
      }</div>
      <div class="alert-body">
        <div class="alert-title" style="color:${severityColor(a.severity)}">${a.title}</div>
        <div style="font-size:11px;color:var(--fg2);margin:3px 0 5px">${a.desc||''}</div>
        <div class="alert-meta">
          <span>ZONE: <strong style="color:var(--fg)">${a.zone}</strong></span>
          <span>${fmt.timeAgo(a.ts)}</span>
          <span>${statusBadge(a.status)}</span>
        </div>
      </div>
      <div style="display:flex;flex-direction:column;align-items:flex-end;gap:6px">
        <span class="alert-badge ${a.severity}">${a.severity.toUpperCase()}</span>
        ${a.isIncident && a.status==='active' ? `<button class="btn btn-sm btn-primary" onclick="openAck(${a.id})">ACK</button>` : ''}
      </div>
    </div>`).join('')
    : '<div style="padding:60px;text-align:center;color:var(--muted)">&#10003; ALL CLEAR — No active alerts</div>';
}

// ============================================================
// INCIDENTS
// ============================================================

function filterIncidents(f, btn) {
  state.incidentFilter = f;
  document.querySelectorAll('#page-incidents .filter-btn').forEach(b => b.classList.remove('active'));
  if (btn) btn.classList.add('active');
  renderIncidents();
}

function renderIncidents() {
  const all = state.incidents;
  const filtered = state.incidentFilter === 'all' ? all : all.filter(i => i.status === state.incidentFilter);

  document.getElementById('inc-stat-total').textContent = all.length;
  document.getElementById('inc-stat-active').textContent = all.filter(i=>i.status==='active').length;
  document.getElementById('inc-stat-ack').textContent = all.filter(i=>i.status==='acknowledged').length;
  document.getElementById('inc-stat-res').textContent = all.filter(i=>i.status==='resolved').length;

  // Charts
  const sevs = ['critical','high','medium','low'];
  const maxSev = Math.max(...sevs.map(s => all.filter(i=>i.severity===s).length), 1);
  document.getElementById('inc-chart-severity').innerHTML = sevs.map(s => {
    const n = all.filter(i=>i.severity===s).length;
    return `<div class="bar-row"><span class="bar-label">${s.toUpperCase()}</span>
      <div class="bar-track"><div class="bar-fill" style="width:${n/maxSev*100}%;background:${severityColor(s)}"></div></div>
      <span class="bar-val">${n}</span></div>`;
  }).join('');

  const types = ['gas_leak','temperature_spike','pressure_anomaly','compound_risk','permit_violation','equipment_failure'];
  const maxT = Math.max(...types.map(t => all.filter(i=>i.type===t).length), 1);
  document.getElementById('inc-chart-type').innerHTML = types.map(t => {
    const n = all.filter(i=>i.type===t).length;
    return `<div class="bar-row"><span class="bar-label" style="width:130px">${t.replace(/_/g,' ')}</span>
      <div class="bar-track"><div class="bar-fill" style="width:${n/maxT*100}%"></div></div>
      <span class="bar-val">${n}</span></div>`;
  }).join('');

  document.getElementById('incidents-list').innerHTML = filtered.map(i => `
    <div class="incident-card severity-${i.severity} status-${i.status}">
      <div style="display:flex;align-items:start;justify-content:space-between;gap:12px;flex-wrap:wrap">
        <div style="flex:1;min-width:200px">
          <div class="inc-title" style="color:${i.severity==='critical'&&i.status==='active'?'var(--destructive)':'var(--fg)'}">${i.title}
            <span style="font-size:10px;color:var(--muted);margin-left:6px">#${i.id}</span></div>
          <div class="inc-desc">${i.desc}</div>
          <div class="inc-meta">
            <span>ZONE: <strong>${i.zone}</strong></span>
            <span>SEV: <strong style="color:${severityColor(i.severity)}">${i.severity.toUpperCase()}</strong></span>
            <span>TYPE: <strong>${typeLabel(i.type)}</strong></span>
            <span>${fmt.time(i.triggeredAt)}</span>
            ${i.riskScore ? `<span>RISK: <strong style="color:${severityColor(i.severity)}">${i.riskScore}</strong></span>` : ''}
          </div>
        </div>
        <div style="text-align:right;flex-shrink:0">
          ${statusBadge(i.status)}
          ${i.status==='active'?`<br><br><button class="btn btn-primary btn-sm" onclick="openAck(${i.id})">ACKNOWLEDGE</button>`:''}
        </div>
      </div>
      ${i.acknowledgedBy?`<div class="inc-ack-info" style="margin-top:10px;padding-top:10px;border-top:1px solid var(--border)">
        <strong>Acknowledged by:</strong> ${i.acknowledgedBy} &nbsp; | &nbsp;
        <strong>At:</strong> ${fmt.time(i.acknowledgedAt)} &nbsp; | &nbsp;
        <span>${i.acknowledgeNote}</span>
      </div>`:''}
    </div>`).join('');
}

// ============================================================
// SENSORS
// ============================================================

function renderSensors() {
  const s = state.sensors;
  document.getElementById('s-stat-total').textContent = s.length;
  document.getElementById('s-stat-normal').textContent = s.filter(x=>x.status==='normal').length;
  document.getElementById('s-stat-warn').textContent = s.filter(x=>x.status==='warning').length;
  document.getElementById('s-stat-crit').textContent = s.filter(x=>x.status==='critical').length;

  document.getElementById('sensors-grid').innerHTML = [...s].sort((a,b)=>{
    const o={critical:0,warning:1,normal:2};return(o[a.status]||2)-(o[b.status]||2);
  }).map(s => {
    const pct = Math.min(100, s.inverted
      ? Math.max(0, (s.threshold - s.value) / (s.threshold - s.min) * 100)
      : s.value / s.threshold * 100);
    const bc = s.status==='critical'?'var(--destructive)':s.status==='warning'?'var(--warning)':'var(--safe)';
    const tc = s.status==='critical'?'c-destructive':s.status==='warning'?'c-warning':'c-safe';
    const trendIcon = s.trend==='rising'?'▲':s.trend==='falling'?'▼':'—';
    const trendClass = s.trend==='rising'?'trend-up':s.trend==='falling'?'trend-down':'trend-stable';
    return `<div class="card sensor-card status-${s.status}">
      <div class="sensor-label">
        <span><span class="blink-dot ${s.status}"></span>${s.type}</span>
        <span class="${tc}" style="font-size:9px;font-weight:bold">${s.status.toUpperCase()}</span>
      </div>
      <div style="font-size:11px;color:var(--muted);margin-bottom:4px">${s.name}</div>
      <div style="display:flex;align-items:baseline;gap:6px">
        <span class="sensor-value ${tc}">${s.value}</span>
        <span style="font-size:12px;color:var(--muted)">${s.unit}</span>
        <span class="${trendClass}" style="font-size:13px;margin-left:auto">${trendIcon}</span>
      </div>
      <div style="font-size:10px;color:var(--muted);margin-top:6px">Threshold: ${s.threshold}${s.unit}</div>
      <div class="sensor-bar mt-8"><div class="sensor-bar-fill" style="width:${pct}%;background:${bc}"></div></div>
      <div style="display:flex;justify-content:space-between;font-size:9px;color:var(--muted);margin-top:3px">
        <span>${s.min}${s.unit}</span><span>${s.threshold}${s.unit} limit</span><span>${s.max}${s.unit}</span>
      </div>
      <div class="sensor-zone">&#9642; ${s.zone}</div>
    </div>`;
  }).join('');
}

// ============================================================
// PERMITS
// ============================================================

function filterPermits(f, btn) {
  state.permitFilter = f;
  document.querySelectorAll('#page-permits .filter-btn').forEach(b => b.classList.remove('active'));
  if (btn) btn.classList.add('active');
  renderPermits();
}

function renderPermits() {
  const filtered = state.permitFilter === 'all' ? state.permits
    : state.permits.filter(p => p.status === state.permitFilter);

  document.getElementById('permits-list').innerHTML = filtered.map(p => {
    const minLeft = Math.floor((p.expiresAt - Date.now()) / 60000);
    const expiring = p.status === 'active' && minLeft < 60 && minLeft > 0;
    const expired = p.status === 'expired' || minLeft <= 0;
    return `<div class="card permit-card" style="${expired?'opacity:0.55':''}${expiring?'border-color:rgba(245,158,11,0.6)':''}">
      <div class="permit-header">
        <div>
          <span class="tag ${permitTypeClass(p.type)}">${typeLabel(p.type)}</span>
          ${p.riskFlag?'<span class="risk-flag" style="margin-left:8px">&#9650; RISK FLAGGED</span>':''}
        </div>
        ${statusBadge(p.status)}
      </div>
      <div class="permit-title">${p.issuedTo}</div>
      <div style="font-size:11px;color:var(--fg2);margin:6px 0">${p.desc}</div>
      <div class="permit-meta">
        <span>ZONE: <strong>${p.zone}</strong></span>
        <span>ISSUED: <strong>${fmt.time(p.issuedAt)}</strong></span>
        <span>EXPIRES: <strong style="color:${expiring?'var(--warning)':expired?'var(--destructive)':'var(--fg)'}">${fmt.time(p.expiresAt)}</strong></span>
        <span>TIME LEFT: <strong style="color:${expiring?'var(--warning)':expired?'var(--destructive)':'var(--fg)'}">${expired?'EXPIRED':minLeft+'m'}</strong></span>
      </div>
    </div>`;
  }).join('');
}

// ============================================================
// WORKERS
// ============================================================

function filterWorkers(f, btn) {
  state.workerFilter = f;
  document.querySelectorAll('#page-workers .filter-btn').forEach(b => b.classList.remove('active'));
  if (btn) btn.classList.add('active');
  renderWorkers();
}

function renderWorkers() {
  const onDuty = state.workers.filter(w => w.status === 'on_duty');
  const offDuty = state.workers.filter(w => w.status === 'off_duty');
  const ppeViol = state.workers.filter(w => w.ppe === 'violation');

  document.getElementById('workers-on-site').textContent = onDuty.length;
  document.getElementById('w-stat-total').textContent = state.workers.length;
  document.getElementById('w-stat-on').textContent = onDuty.length;
  document.getElementById('w-stat-off').textContent = offDuty.length;
  document.getElementById('w-stat-ppe').textContent = ppeViol.length;

  // Zone chart
  const zoneMap = {};
  onDuty.forEach(w => { zoneMap[w.zone] = (zoneMap[w.zone]||0) + 1; });
  const zoneEntries = Object.entries(zoneMap).sort((a,b)=>b[1]-a[1]);
  const maxZ = Math.max(...zoneEntries.map(e=>e[1]), 1);
  document.getElementById('workers-zone-chart').innerHTML = zoneEntries.map(([zone, count]) =>
    `<div class="bar-row"><span class="bar-label">${zone.length>16?zone.slice(0,14)+'..':zone}</span>
    <div class="bar-track"><div class="bar-fill" style="width:${count/maxZ*100}%"></div></div>
    <span class="bar-val">${count}</span></div>`
  ).join('');

  // Zone filter
  const zf = document.getElementById('worker-zone-filter');
  const curZone = zf.value;
  const allZones = [...new Set(state.workers.map(w => w.zone))].sort();
  zf.innerHTML = '<option value="all">ALL ZONES</option>' +
    allZones.map(z => `<option value="${z}" ${curZone===z?'selected':''}>${z}</option>`).join('');

  // List
  let filtered = state.workers;
  if (state.workerFilter !== 'all') filtered = filtered.filter(w => w.status === state.workerFilter);
  const zoneVal = document.getElementById('worker-zone-filter').value;
  if (zoneVal !== 'all') filtered = filtered.filter(w => w.zone === zoneVal);

  document.getElementById('workers-count').textContent = filtered.length;
  document.getElementById('workers-list').innerHTML = filtered.map(w => `
    <div class="worker-row">
      <div class="worker-col narrow" style="font-size:10px;color:var(--muted)">${w.emp}</div>
      <div class="worker-col">
        <div style="font-weight:bold;font-size:12px">${w.name}</div>
        <div style="font-size:10px;color:var(--muted)">${w.role}</div>
      </div>
      <div class="worker-col" style="font-size:11px">
        <div>&#9642; ${w.zone}</div>
        ${w.status==='on_duty'&&w.checkInAt?`<div style="font-size:10px;color:var(--muted)">In: ${fmt.timeAgo(w.checkInAt)}</div>`:''}
      </div>
      <div class="worker-col narrow"><span class="tag ${w.shift}">${w.shift.toUpperCase()}</span></div>
      <div class="worker-col narrow">
        <span class="tag ${w.status.replace('_','-')}">${w.status.replace('_',' ').toUpperCase()}</span>
        ${w.status==='on_duty'?`<span style="display:inline-block;width:6px;height:6px;border-radius:50%;background:var(--safe);box-shadow:0 0 4px var(--safe);vertical-align:middle;margin-left:4px;animation:pulse-dot 2s infinite"></span>`:''}
      </div>
      <div class="worker-col narrow">
        <span class="tag ${w.ppe}">${w.ppe.toUpperCase()}</span>
        ${w.status==='on_duty'?`<button class="btn btn-sm btn-muted" style="margin-top:3px;font-size:8px;padding:1px 4px" onclick="togglePpe(${w.id})">✎</button>`:''}
      </div>
      <div class="worker-col actions">
        ${w.status==='off_duty'
          ? `<button class="btn btn-sm btn-success" onclick="openCheckIn(${w.id})">CHECK IN</button>`
          : w.status==='on_duty'
          ? `<button class="btn btn-sm btn-off" onclick="checkOut(${w.id})">OUT</button>`
          : ''}
      </div>
    </div>`).join('');
}

// ============================================================
// WORKER ACTIONS
// ============================================================

function openCheckIn(workerId) {
  state.pendingCheckInId = workerId;
  const w = state.workers.find(x => x.id === workerId);
  document.getElementById('checkin-worker-info').textContent = `${w.name} — ${w.emp} (${w.role})`;
  const sel = document.getElementById('checkin-zone');
  sel.innerHTML = ZONES.map(z => `<option value="${z}">${z}</option>`).join('');
  document.getElementById('checkin-modal').classList.add('open');
}

function confirmCheckIn() {
  const w = state.workers.find(x => x.id === state.pendingCheckInId);
  if (!w) return;
  w.status = 'on_duty';
  w.zone = document.getElementById('checkin-zone').value;
  w.checkInAt = Date.now();
  w.ppe = 'unknown';
  closeModal('checkin-modal');
  renderWorkers();
}

function checkOut(workerId) {
  const w = state.workers.find(x => x.id === workerId);
  if (!w) return;
  w.status = 'off_duty';
  w.zone = 'Off-Site';
  w.checkInAt = null;
  renderWorkers();
}

function togglePpe(workerId) {
  const w = state.workers.find(x => x.id === workerId);
  if (!w) return;
  const cycle = {compliant:'violation',violation:'unknown',unknown:'compliant'};
  w.ppe = cycle[w.ppe] || 'unknown';
  renderWorkers();
}

// ============================================================
// ACKNOWLEDGE MODAL
// ============================================================

function openAck(incidentId) {
  state.pendingAckId = incidentId;
  const inc = state.incidents.find(i => i.id === incidentId);
  document.getElementById('ack-incident-info').textContent =
    `[${inc.severity.toUpperCase()}] ${inc.title} — Zone: ${inc.zone}`;
  document.getElementById('ack-name').value = '';
  document.getElementById('ack-note').value = '';
  document.getElementById('ack-modal').classList.add('open');
}

function submitAck() {
  const name = document.getElementById('ack-name').value.trim();
  const note = document.getElementById('ack-note').value.trim();
  if (!name || !note) { alert('Please fill in both fields'); return; }
  const inc = state.incidents.find(i => i.id === state.pendingAckId);
  if (inc) {
    inc.status = 'acknowledged';
    inc.acknowledgedBy = name;
    inc.acknowledgeNote = note;
    inc.acknowledgedAt = Date.now();
  }
  closeModal('ack-modal');
  renderPage(getActivePage());
}

function closeModal(id) {
  document.getElementById(id).classList.remove('open');
}

function getActivePage() {
  const active = document.querySelector('.page.active');
  return active ? active.id.replace('page-','') : 'dashboard';
}

// ============================================================
// CLOCK
// ============================================================

function updateClock() {
  const el = document.getElementById('dash-clock');
  if (el) {
    const now = new Date();
    el.innerHTML = `SYSTEM TIME<br><span style="color:var(--primary);font-size:14px">${now.toISOString().slice(0,19).replace('T',' ')} UTC</span>`;
  }
}

// ============================================================
// MAIN LOOP
// ============================================================

let tickCount = 0;

function tick() {
  tickCount++;
  simulateSensors();
  computeRisk();
  updateEmergencyUI();

  // Update sidebar risk bar always
  const score = state.riskScore;
  const gcolor = score>=75?'var(--destructive)':score>=50?'var(--warning)':score>=25?'var(--primary)':'var(--safe)';
  document.getElementById('sidebar-risk-bar').style.width = score + '%';
  document.getElementById('sidebar-risk-bar').style.background = gcolor;
  document.getElementById('sidebar-risk-val').textContent = score;
  document.getElementById('sidebar-risk-val').style.color = gcolor;

  // Update alert badge
  const alertCount = state.incidents.filter(i=>i.status!=='resolved').length +
    state.sensors.filter(s=>s.status!=='normal').length;
  document.getElementById('nav-alert-count').textContent = alertCount;

  // Re-render active page
  const page = getActivePage();
  renderPage(page);
  updateClock();
}

// Boot
computeRisk();
renderDashboard();
tick();
setInterval(tick, 4000);
setInterval(updateClock, 1000);

// Close modal on overlay click
document.querySelectorAll('.modal-overlay').forEach(o => {
  o.addEventListener('click', (e) => { if (e.target === o) o.classList.remove('open'); });
});
</script>
</body>
</html>
