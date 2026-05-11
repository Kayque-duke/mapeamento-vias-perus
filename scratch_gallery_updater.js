const fs = require('fs');

const filePath = 'genio_ruas_perus.html';
let html = fs.readFileSync(filePath, 'utf8');

// 1. Inserir botão "Vincular Pasta" no header
if (!html.includes('id="btn-vincular-pasta"')) {
    html = html.replace(
        '<button id="btn-exportar">',
        `<button id="btn-vincular-pasta" style="color: var(--accent-secondary); border-color: var(--accent-secondary);">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"></path><line x1="12" y1="11" x2="12" y2="17"></line><line x1="9" y1="14" x2="15" y2="14"></line></svg>
        Pasta de Fotos
      </button>
      <button id="btn-exportar">`
    );
}

// 2. Inserir botão "Ver Fotos" na tabela
if (!html.includes('verFotos(')) {
    // Procura o local exato das ações da tabela
    const targetAcoes = `<button onclick="autoFetchCoords(\${street.id})" title="Mapear Automaticamente via Satélite" style="padding:4px; background:transparent; border:none; color:var(--accent-success); cursor:pointer; margin-left:8px;">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><line x1="2" y1="12" x2="22" y2="12"></line><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path></svg>
            </button>`;
            
    const newAcoes = targetAcoes + `
            <button onclick="verFotos('\${street.nome}')" title="Ver Fotos da Rua" style="padding:4px; background:transparent; border:none; color:var(--accent-primary); cursor:pointer; margin-left:8px;">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect><circle cx="8.5" cy="8.5" r="1.5"></circle><polyline points="21 15 16 10 5 21"></polyline></svg>
            </button>`;
            
    html = html.replace(targetAcoes, newAcoes);
}

// 3. Inserir Modal da Galeria
if (!html.includes('id="modal-galeria"')) {
    const modalGaleria = `
  <!-- Modal Galeria de Fotos -->
  <div class="modal" id="modal-galeria">
    <div class="modal-content" style="max-width: 800px; width: 90%;">
      <div class="modal-header">
        <h2 id="galeria-titulo">Fotos da Rua</h2>
        <button class="close-modal" onclick="fecharGaleria()">×</button>
      </div>
      <div class="modal-body" id="galeria-body" style="display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 16px; max-height: 60vh; overflow-y: auto; padding: 16px 0;">
        <!-- Imagens injetadas via JS -->
      </div>
    </div>
  </div>

  <div id="toast-container"></div>`;
    
    html = html.replace('<div id="toast-container"></div>', modalGaleria);
}

// 4. Inserir lógica no fim do script
if (!html.includes('rootDirectoryHandle')) {
    const scriptLogic = `
    // --- FILE SYSTEM ACCESS API ---
    let rootDirectoryHandle = null;

    document.getElementById('btn-vincular-pasta').addEventListener('click', async () => {
      try {
        rootDirectoryHandle = await window.showDirectoryPicker({ mode: 'readwrite' });
        showToast('Pasta raiz vinculada com sucesso!', 'success');
        syncFolders();
      } catch (err) {
        if(err.name !== 'AbortError') {
           showToast('Erro ao acessar pasta: ' + err.message, 'error');
        }
      }
    });

    async function syncFolders() {
      if(!rootDirectoryHandle) return;
      let count = 0;
      for (const street of streets) {
        try {
          await rootDirectoryHandle.getDirectoryHandle(street.nome, { create: true });
          count++;
        } catch(e) {
          console.error('Erro ao criar pasta para', street.nome, e);
        }
      }
      if(count > 0) showToast(\`Pastas sincronizadas para \${count} ruas.\`, 'info');
    }

    window.verFotos = async function(nomeRua) {
      if(!rootDirectoryHandle) {
        showToast('Vincule a "Pasta de Fotos" no topo da tela primeiro.', 'warning');
        return;
      }
      try {
        const dirHandle = await rootDirectoryHandle.getDirectoryHandle(nomeRua, { create: true });
        
        const galeriaBody = document.getElementById('galeria-body');
        galeriaBody.innerHTML = '<div style="text-align:center; width:100%; color:var(--text-secondary);">Buscando fotos...</div>';
        document.getElementById('galeria-titulo').innerText = \`Fotos: \${nomeRua}\`;
        document.getElementById('modal-galeria').classList.add('active');

        const validExtensions = ['.jpg', '.jpeg', '.png', '.webp', '.gif'];
        const images = [];

        for await (const entry of dirHandle.values()) {
          if (entry.kind === 'file') {
            const ext = entry.name.toLowerCase().slice((entry.name.lastIndexOf(".") - 1 >>> 0) + 2);
            if (validExtensions.includes('.' + ext)) {
              const file = await entry.getFile();
              const objectURL = URL.createObjectURL(file);
              images.push({ url: objectURL, name: entry.name });
            }
          }
        }

        if(images.length === 0) {
           galeriaBody.innerHTML = '<div style="text-align:center; width:100%; color:var(--text-secondary);">Nenhuma foto encontrada nesta pasta. <br><br>Abra seu Windows Explorer e coloque fotos na pasta:<br><strong style="color:var(--accent-secondary)">' + nomeRua + '</strong></div>';
        } else {
           galeriaBody.innerHTML = '';
           images.forEach(img => {
             const imgEl = document.createElement('img');
             imgEl.src = img.url;
             imgEl.title = img.name;
             imgEl.style.width = '100%';
             imgEl.style.height = '150px';
             imgEl.style.objectFit = 'cover';
             imgEl.style.borderRadius = '8px';
             imgEl.style.boxShadow = 'var(--shadow-sm)';
             imgEl.style.cursor = 'pointer';
             imgEl.onclick = () => window.open(img.url, '_blank');
             galeriaBody.appendChild(imgEl);
           });
        }
      } catch(e) {
        showToast('Erro ao abrir pasta da rua.', 'error');
        fecharGaleria();
      }
    };

    window.fecharGaleria = function() {
      document.getElementById('modal-galeria').classList.remove('active');
    };
    
    // Auto-criação na função de save do modal
    `;
    
    html = html.replace('// Boot', scriptLogic + '\n    // Boot');
}

// 5. Ajustar Modal Save para criar a pasta automaticamente
if (!html.includes('rootDirectoryHandle.getDirectoryHandle(nome, { create: true })')) {
    html = html.replace(
        'streets.push({',
        `if (rootDirectoryHandle) rootDirectoryHandle.getDirectoryHandle(nome, { create: true }).catch(e=>e);
        streets.push({`
    );
    html = html.replace(
        'streets[index] = { ...streets[index], ...data };',
        `streets[index] = { ...streets[index], ...data };
        if (rootDirectoryHandle) rootDirectoryHandle.getDirectoryHandle(data.nome, { create: true }).catch(e=>e);`
    );
}


fs.writeFileSync(filePath, html, 'utf8');
console.log('Successfully updated HTML file with Gallery features');
