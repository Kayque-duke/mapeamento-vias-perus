const fs = require('fs');

const filePath = 'genio_ruas_perus.html';
let html = fs.readFileSync(filePath, 'utf8');

const cssAdditions = `
    /* 🚀 FASE 2: THE JAW-DROPPING UPGRADES */
    
    /* 1. Tech-Noir Map Filter */
    .leaflet-layer,
    .leaflet-control-zoom-in,
    .leaflet-control-zoom-out,
    .leaflet-control-attribution {
      filter: invert(100%) hue-rotate(180deg) brightness(95%) contrast(90%);
    }

    /* 2. Sticky Glass Header in Table */
    .table-wrapper {
      max-height: calc(100vh - 280px);
      overflow-y: auto;
      padding-right: 4px;
    }
    
    /* Scrollbar minimalista para a tabela */
    .table-wrapper::-webkit-scrollbar { width: 6px; }
    .table-wrapper::-webkit-scrollbar-track { background: transparent; }
    .table-wrapper::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.1); border-radius: 10px; }
    .table-wrapper::-webkit-scrollbar-thumb:hover { background: rgba(255,255,255,0.2); }

    #streets-table th {
      position: sticky;
      top: 0;
      background: rgba(15, 17, 23, 0.85) !important;
      backdrop-filter: blur(12px);
      -webkit-backdrop-filter: blur(12px);
      z-index: 10;
      box-shadow: 0 4px 15px rgba(0,0,0,0.5);
    }

    /* 3. Holographic Aura / Glow */
    @keyframes pulseGlow {
      0% { box-shadow: 0 0 0 0 rgba(34, 211, 238, 0.4); }
      70% { box-shadow: 0 0 0 10px rgba(34, 211, 238, 0); }
      100% { box-shadow: 0 0 0 0 rgba(34, 211, 238, 0); }
    }
    
    .btn-aura {
      animation: pulseGlow 2s infinite;
      border-radius: 50%;
    }
    
    .btn-aura:hover {
      animation: none;
      transform: scale(1.1);
      color: #fff !important;
      background: var(--accent-success) !important;
    }

    /* 4. HUD Stats Panel */
    .hud-panel {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 16px;
      margin-bottom: 16px;
      padding: 0 16px;
    }
    
    .hud-card {
      background: var(--glass-bg);
      backdrop-filter: var(--glass-blur);
      border: 1px solid var(--glass-border);
      border-radius: 12px;
      padding: 16px;
      display: flex;
      flex-direction: column;
      position: relative;
      overflow: hidden;
      box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    .hud-card::before {
      content: '';
      position: absolute;
      top: -50%; left: -50%;
      width: 200%; height: 200%;
      background: conic-gradient(from 0deg, transparent 0%, rgba(34, 211, 238, 0.1) 30%, transparent 60%);
      animation: rotateGlow 8s linear infinite;
      z-index: 0;
      pointer-events: none;
    }
    
    @keyframes rotateGlow {
      100% { transform: rotate(360deg); }
    }
    
    .hud-value {
      font-family: 'Outfit', sans-serif;
      font-size: 28px;
      font-weight: 800;
      color: var(--accent-secondary);
      z-index: 1;
      display: flex;
      align-items: baseline;
      gap: 4px;
      text-shadow: 0 0 20px rgba(34, 211, 238, 0.4);
    }
    
    .hud-label {
      font-size: 11px;
      text-transform: uppercase;
      letter-spacing: 1px;
      color: var(--text-muted);
      z-index: 1;
      margin-top: 4px;
      font-weight: 600;
    }

    /* Ajuste para fazer os cards de linha parecerem flutuar */
    #streets-table td {
      border-bottom: 1px solid rgba(255,255,255,0.03);
    }
    #streets-table tr:hover {
      background: rgba(255, 255, 255, 0.03);
      box-shadow: inset 0 0 0 1px rgba(255, 255, 255, 0.05);
    }
`;

if (!html.includes('Tech-Noir Map Filter')) {
    html = html.replace('</style>', cssAdditions + '\n  </style>');
}

const hudHTML = `
      <!-- JAW-DROPPING HUD PANEL -->
      <div class="hud-panel">
        <div class="hud-card">
          <div class="hud-value" id="hud-ruas">0</div>
          <div class="hud-label">Vias Mapeadas</div>
        </div>
        <div class="hud-card">
          <div class="hud-value"><span id="hud-km">0.00</span><span style="font-size:14px;color:var(--text-secondary)">km</span></div>
          <div class="hud-label">Extensão Total</div>
        </div>
        <div class="hud-card">
          <div class="hud-value"><span id="hud-largura">0.0</span><span style="font-size:14px;color:var(--text-secondary)">m</span></div>
          <div class="hud-label">Largura Média</div>
        </div>
      </div>
`;

if (!html.includes('id="hud-ruas"')) {
    html = html.replace('<div class="table-header">', hudHTML + '\n      <div class="table-header">');
}

const jsAdditions = `
    // --- HUD LOGIC ---
    function animateValue(obj, start, end, duration, isFloat = false) {
      let startTimestamp = null;
      const step = (timestamp) => {
        if (!startTimestamp) startTimestamp = timestamp;
        const progress = Math.min((timestamp - startTimestamp) / duration, 1);
        const current = progress * (end - start) + start;
        obj.innerHTML = isFloat ? current.toFixed(2) : Math.floor(current);
        if (progress < 1) {
          window.requestAnimationFrame(step);
        }
      };
      window.requestAnimationFrame(step);
    }

    function updateHUD() {
      const elRuas = document.getElementById('hud-ruas');
      const elKm = document.getElementById('hud-km');
      const elLargura = document.getElementById('hud-largura');
      
      const prevRuas = parseFloat(elRuas.innerText) || 0;
      const prevKm = parseFloat(elKm.innerText) || 0;
      const prevLargura = parseFloat(elLargura.innerText) || 0;

      const totalRuas = streets.length;
      let totalMeters = 0;
      let sumLargura = 0;
      let countLargura = 0;

      streets.forEach(s => {
        if (s.coords && s.coords.length > 1) {
          totalMeters += calculateLength(s.coords);
        }
        if (s.largura) {
          sumLargura += parseFloat(s.largura);
          countLargura++;
        }
      });

      const totalKm = totalMeters / 1000;
      const mediaLargura = countLargura > 0 ? sumLargura / countLargura : 0;

      animateValue(elRuas, prevRuas, totalRuas, 1000);
      animateValue(elKm, prevKm, totalKm, 1000, true);
      animateValue(elLargura, prevLargura, mediaLargura, 1000, true);
    }
`;

if (!html.includes('updateHUD()')) {
    html = html.replace('// --- FILE SYSTEM ACCESS API ---', jsAdditions + '\n\n    // --- FILE SYSTEM ACCESS API ---');
    // Adicionar chamada updateHUD no final de renderTable
    html = html.replace("tbody.appendChild(tr);\n      });", "tbody.appendChild(tr);\n      });\n\n      updateHUD();");
}

// Add btn-aura class to satellite button
if (!html.includes('btn-aura')) {
    html = html.replace(
        'title="Mapear Automaticamente via Satélite" style="padding:4px; background:transparent;',
        'title="Mapear Automaticamente via Satélite" class="btn-aura" style="padding:4px; background:transparent;'
    );
}

fs.writeFileSync(filePath, html, 'utf8');
console.log('Successfully applied JAW-DROPPING Phase 2 enhancements.');
