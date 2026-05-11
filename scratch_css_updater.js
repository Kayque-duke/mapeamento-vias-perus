const fs = require('fs');
const path = require('path');

const filePath = path.resolve('genio_ruas_perus.html');
let content = fs.readFileSync(filePath, 'utf8');

const newCss = `    :root {
      /* Deep Dark Premium Palette */
      --bg-primary: #05050A;
      --bg-secondary: #0A0B10;
      --bg-tertiary: #12141D;
      --bg-card: #161925;

      /* Gradients & Accents */
      --accent-primary: #4F46E5; /* Indigo */
      --accent-secondary: #06B6D4; /* Cyan */
      --accent-glow: rgba(79, 70, 229, 0.4);
      --accent-success: #10B981;
      --accent-warning: #F59E0B;
      --accent-danger: #EF4444;

      /* Typography */
      --text-primary: #F8FAFC;
      --text-secondary: #94A3B8;
      --text-muted: #475569;

      /* Borders & Glass */
      --border-subtle: rgba(255, 255, 255, 0.04);
      --border-medium: rgba(255, 255, 255, 0.08);
      --border-focus: rgba(79, 70, 229, 0.5);

      --glass-bg: rgba(10, 11, 16, 0.7);
      --glass-border: rgba(255, 255, 255, 0.08);
      --glass-blur: blur(24px);
      
      /* Shadows */
      --shadow-sm: 0 2px 4px rgba(0,0,0,0.4);
      --shadow-md: 0 8px 16px rgba(0,0,0,0.6);
      --shadow-glow: 0 0 20px var(--accent-glow);
    }

    * { box-sizing: border-box; margin: 0; padding: 0; }

    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: var(--bg-primary); }
    ::-webkit-scrollbar-thumb { background: var(--bg-tertiary); border-radius: 3px; border: 1px solid var(--bg-primary); }
    ::-webkit-scrollbar-thumb:hover { background: var(--text-muted); }

    body {
      font-family: 'Inter', sans-serif;
      background-color: var(--bg-primary);
      color: var(--text-primary);
      height: 100vh;
      display: flex;
      flex-direction: column;
      overflow: hidden;
      -webkit-font-smoothing: antialiased;
    }

    /* HEADER */
    header {
      background: var(--glass-bg);
      backdrop-filter: var(--glass-blur);
      -webkit-backdrop-filter: var(--glass-blur);
      border-bottom: 1px solid var(--glass-border);
      padding: 16px 32px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      z-index: 1000;
      box-shadow: 0 4px 30px rgba(0, 0, 0, 0.5);
    }

    .brand { display: flex; align-items: center; gap: 16px; }

    .brand h1 {
      font-family: 'Outfit', sans-serif;
      font-size: 26px;
      font-weight: 800;
      letter-spacing: -0.5px;
      background: linear-gradient(135deg, var(--accent-secondary) 0%, var(--accent-primary) 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      filter: drop-shadow(0 2px 10px rgba(6, 182, 212, 0.2));
    }

    .badge {
      background: rgba(6, 182, 212, 0.1);
      padding: 6px 12px;
      border-radius: 20px;
      font-size: 12px;
      font-weight: 600;
      color: var(--accent-secondary);
      border: 1px solid rgba(6, 182, 212, 0.2);
      letter-spacing: 0.5px;
      box-shadow: inset 0 0 10px rgba(6, 182, 212, 0.05);
    }

    .actions { display: flex; gap: 16px; }

    button {
      background: var(--bg-tertiary);
      color: var(--text-primary);
      border: 1px solid var(--border-medium);
      padding: 10px 20px;
      border-radius: 10px;
      font-family: 'Inter', sans-serif;
      font-weight: 600;
      font-size: 13px;
      cursor: pointer;
      transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
      display: flex;
      align-items: center;
      gap: 8px;
      box-shadow: var(--shadow-sm);
    }

    button:hover {
      background: var(--bg-card);
      border-color: var(--accent-secondary);
      transform: translateY(-1px);
      box-shadow: 0 4px 12px rgba(0,0,0,0.5), 0 0 15px rgba(6, 182, 212, 0.15);
    }

    button:active {
      transform: translateY(1px) scale(0.98);
    }

    button.primary {
      background: linear-gradient(135deg, var(--accent-primary) 0%, #312E81 100%);
      border: 1px solid rgba(255,255,255,0.1);
      box-shadow: 0 4px 15px rgba(79, 70, 229, 0.3);
    }

    button.primary:hover {
      background: linear-gradient(135deg, #6366F1 0%, var(--accent-primary) 100%);
      box-shadow: 0 6px 20px rgba(79, 70, 229, 0.5);
      border-color: rgba(255,255,255,0.2);
    }

    /* MAIN CONTENT */
    main { display: flex; flex: 1; overflow: hidden; }

    /* MAP CONTAINER */
    #map-container {
      flex: 1.2;
      position: relative;
      border-right: 1px solid var(--border-subtle);
      box-shadow: 5px 0 30px rgba(0,0,0,0.5);
      z-index: 2;
    }

    #map { width: 100%; height: 100%; background-color: var(--bg-secondary); }

    /* Customizing Leaflet UI */
    .leaflet-control-zoom a {
      background-color: var(--glass-bg) !important;
      color: var(--text-primary) !important;
      border: 1px solid var(--glass-border) !important;
      backdrop-filter: var(--glass-blur);
    }
    .leaflet-control-zoom a:hover {
      background-color: var(--bg-card) !important;
      color: var(--accent-secondary) !important;
    }
    .leaflet-popup-content-wrapper, .leaflet-tooltip {
      background: var(--glass-bg) !important;
      backdrop-filter: var(--glass-blur) !important;
      border: 1px solid var(--glass-border) !important;
      color: var(--text-primary) !important;
      box-shadow: var(--shadow-md) !important;
      border-radius: 12px !important;
    }
    .leaflet-popup-tip { background: var(--glass-bg) !important; border: 1px solid var(--glass-border) !important; }

    /* DRAWING CONTROLS OVERLAY */
    .drawing-overlay {
      position: absolute;
      top: 24px;
      left: 50%;
      transform: translateX(-50%) scale(0.95);
      opacity: 0;
      z-index: 1000;
      background: rgba(10, 11, 16, 0.85);
      backdrop-filter: blur(20px);
      padding: 14px 24px;
      border-radius: 100px;
      border: 1px solid var(--accent-secondary);
      display: none;
      align-items: center;
      gap: 16px;
      box-shadow: 0 0 30px rgba(6, 182, 212, 0.2);
      transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
    }

    .drawing-overlay.active {
      display: flex;
      opacity: 1;
      transform: translateX(-50%) scale(1);
    }

    .drawing-step { font-size: 14px; font-weight: 500; letter-spacing: 0.3px; }
    .drawing-step.highlight { color: var(--text-primary); }
    .drawing-step.highlight strong { color: var(--accent-secondary); font-weight: 700; }

    /* TABLE CONTAINER */
    #table-container {
      flex: 1;
      display: flex;
      flex-direction: column;
      background: var(--bg-secondary);
      overflow: hidden;
      z-index: 1;
    }

    .table-header {
      padding: 24px 32px;
      border-bottom: 1px solid var(--border-subtle);
      display: flex;
      justify-content: space-between;
      align-items: center;
      background: linear-gradient(to bottom, var(--bg-tertiary), var(--bg-secondary));
    }

    .search-box input {
      background: var(--bg-card);
      border: 1px solid var(--border-medium);
      color: var(--text-primary);
      padding: 12px 16px;
      border-radius: 8px;
      width: 300px;
      font-family: 'Inter', sans-serif;
      font-size: 14px;
      transition: all 0.3s;
      box-shadow: inset 0 2px 4px rgba(0,0,0,0.2);
    }

    .search-box input:focus {
      outline: none;
      border-color: var(--accent-primary);
      box-shadow: inset 0 2px 4px rgba(0,0,0,0.2), 0 0 0 3px rgba(79, 70, 229, 0.2);
    }

    .table-wrapper { flex: 1; overflow-y: auto; padding: 0 16px 16px 16px; }

    table { width: 100%; border-collapse: separate; border-spacing: 0 8px; text-align: left; }

    th {
      position: sticky;
      top: 0;
      background: var(--bg-secondary);
      padding: 16px 20px;
      font-size: 11px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.1em;
      color: var(--text-secondary);
      z-index: 10;
    }
    th::after {
      content: '';
      position: absolute;
      bottom: 0; left: 0; right: 0;
      height: 1px;
      background: var(--border-medium);
    }

    td {
      padding: 16px 20px;
      font-size: 13px;
      color: var(--text-primary);
      background: var(--bg-tertiary);
      cursor: pointer;
      transition: all 0.2s ease;
      border-top: 1px solid var(--border-subtle);
      border-bottom: 1px solid var(--border-subtle);
    }

    td:first-child { border-left: 1px solid var(--border-subtle); border-top-left-radius: 8px; border-bottom-left-radius: 8px; }
    td:last-child { border-right: 1px solid var(--border-subtle); border-top-right-radius: 8px; border-bottom-right-radius: 8px; }

    tr { transition: transform 0.2s ease; }

    tr:hover { transform: translateX(4px); }
    
    tr:hover td {
      background: var(--bg-card);
      border-color: var(--border-medium);
    }

    tr.selected td {
      background: rgba(79, 70, 229, 0.1);
      border-color: var(--accent-primary);
    }

    .coord-cell {
      font-family: 'JetBrains Mono', monospace;
      font-size: 11px;
      color: var(--accent-secondary);
      background: rgba(6, 182, 212, 0.1);
      padding: 2px 6px;
      border-radius: 4px;
      display: inline-block;
      margin-top: 4px;
    }

    .editable { position: relative; font-weight: 600; color: #fff; }
    .editable:hover::after {
      content: '✎';
      position: absolute;
      right: 12px;
      color: var(--accent-secondary);
      font-size: 14px;
    }

    .empty-state {
      padding: 60px;
      text-align: center;
      color: var(--text-muted);
      font-size: 15px;
      background: transparent !important;
      border: none !important;
    }

    /* ANIMATIONS */
    @keyframes fadeSlideIn {
      from { opacity: 0; transform: translateY(15px); }
      to { opacity: 1; transform: translateY(0); }
    }

    @keyframes modalIn {
      from { opacity: 0; transform: scale(0.95) translateY(20px); }
      to { opacity: 1; transform: scale(1) translateY(0); }
    }

    /* MODAL */
    .modal-backdrop {
      position: fixed;
      top: 0; left: 0; right: 0; bottom: 0;
      background: rgba(0,0,0,0.8);
      backdrop-filter: blur(8px);
      z-index: 2000;
      display: none;
      align-items: center;
      justify-content: center;
      opacity: 0;
      transition: opacity 0.3s ease;
    }

    .modal-backdrop.active { display: flex; opacity: 1; }

    .modal {
      background: var(--bg-secondary);
      border: 1px solid var(--glass-border);
      border-radius: 16px;
      width: 440px;
      padding: 32px;
      box-shadow: 0 20px 50px rgba(0,0,0,0.9), 0 0 0 1px rgba(255,255,255,0.05);
      animation: modalIn 0.4s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }

    .modal h2 {
      font-family: 'Outfit', sans-serif;
      font-size: 24px;
      margin-bottom: 24px;
      color: var(--text-primary);
      letter-spacing: -0.5px;
    }

    .form-group { margin-bottom: 20px; }

    .form-group label {
      display: block;
      font-size: 13px;
      color: var(--text-secondary);
      margin-bottom: 8px;
      font-weight: 600;
      letter-spacing: 0.3px;
    }

    .form-group input, .form-group select {
      width: 100%;
      background: var(--bg-tertiary);
      border: 1px solid var(--border-medium);
      color: var(--text-primary);
      padding: 12px 16px;
      border-radius: 8px;
      font-family: 'Inter', sans-serif;
      font-size: 14px;
      transition: all 0.2s;
    }

    .form-group input:focus, .form-group select:focus {
      outline: none;
      border-color: var(--accent-primary);
      box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.2);
    }

    .modal-actions {
      display: flex;
      justify-content: flex-end;
      gap: 12px;
      margin-top: 32px;
    }

    /* TOAST */
    #toast-container {
      position: fixed;
      bottom: 32px;
      right: 32px;
      z-index: 3000;
      display: flex;
      flex-direction: column;
      gap: 12px;
    }

    .toast {
      background: rgba(22, 25, 37, 0.9);
      backdrop-filter: blur(12px);
      border-left: 4px solid var(--accent-primary);
      color: var(--text-primary);
      padding: 16px 24px;
      border-radius: 8px;
      font-size: 14px;
      font-weight: 500;
      box-shadow: 0 10px 30px rgba(0,0,0,0.5), 0 0 0 1px rgba(255,255,255,0.05);
      animation: slideIn 0.4s cubic-bezier(0.16, 1, 0.3, 1) forwards;
      display: flex;
      align-items: center;
      gap: 12px;
    }

    .toast::before {
      content: '';
      display: block;
      width: 8px; height: 8px;
      border-radius: 50%;
      background: var(--accent-primary);
    }

    .toast.success { border-left-color: var(--accent-success); }
    .toast.success::before { background: var(--accent-success); }
    
    .toast.error { border-left-color: var(--accent-danger); }
    .toast.error::before { background: var(--accent-danger); }

    .toast.warning { border-left-color: var(--accent-warning); }
    .toast.warning::before { background: var(--accent-warning); }

    @keyframes slideIn {
      from { transform: translateX(120%); opacity: 0; }
      to { transform: translateX(0); opacity: 1; }
    }

    @keyframes slideOut {
      from { transform: translateX(0); opacity: 1; }
      to { transform: translateX(120%); opacity: 0; }
    }`;

content = content.replace(/<style>[\s\S]*?<\/style>/, '<style>\n' + newCss + '\n  </style>');
content = content.replace(/filtered\.forEach\(street => \{/, 'filtered.forEach((street, index) => {');
content = content.replace(/const tr = document\.createElement\('tr'\);\s*tr\.id = `row-\$\{street\.id\}`;/, 
  "const tr = document.createElement('tr');\n        tr.id = `row-${street.id}`;\n        tr.style.animation = `fadeSlideIn 0.4s ease forwards ${index * 0.05}s`;\n        tr.style.opacity = '0';");
content = content.replace(/instruction\.innerText = "Clique no mapa para marcar o INÍCIO da via";/, 
  'instruction.innerHTML = "Clique no mapa para marcar o <strong>INÍCIO</strong> da via";');
content = content.replace(/instruction\.innerText = "Clique para marcar o FIM da via \\(ou pontos intermediários\\)";/, 
  'instruction.innerHTML = "Clique para marcar o <strong>FIM</strong> da via (ou pontos intermediários)";');
content = content.replace(/instruction\.innerText = `Marcando INÍCIO para: \$\{street\.nome\}`;/, 
  'instruction.innerHTML = `Marcando <strong>INÍCIO</strong> para: <span style="color:var(--accent-primary)">${street.nome}</span>`;');

fs.writeFileSync(filePath, content);
console.log('Successfully updated HTML file');
