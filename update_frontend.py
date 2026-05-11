import os
import re

file_path = "mapeamentovias2.html"

# Detect encoding
encoding = 'utf-8'
try:
    with open(file_path, "r", encoding="utf-8") as f:
        f.read()
except UnicodeDecodeError:
    encoding = 'utf-16'

with open(file_path, "r", encoding=encoding) as f:
    content = f.read()

# 1. Add API_URL at the top of the script
if "const API_URL =" not in content:
    content = content.replace(
        "let map;",
        "const API_URL = 'http://localhost:8000/api';\n    let map;"
    )

# 2. Empty out the huge initial variables
content = re.sub(
    r'let streets = \[.*?\];',
    'let streets = [];',
    content,
    flags=re.DOTALL
)

content = re.sub(
    r'const initialData = \[.*?\];',
    'const initialData = [];',
    content,
    flags=re.DOTALL
)

content = re.sub(
    r'let userPins = \[.*?\];',
    'let userPins = [];',
    content,
    flags=re.DOTALL
)

# 3. Rewrite loadData
new_load_data = """    async function loadData() {
      try {
        const res = await fetch(API_URL + '/ruas');
        if (res.ok) {
          streets = await res.json();
        } else {
          console.error("Erro ao carregar ruas", await res.text());
        }
      } catch (e) {
        console.error("Falha na API:", e);
      }
      renderTable();
      renderMapLayers();
      updateBadge();
    }"""
content = re.sub(r'function loadData\(\) \{.*?\n    \}', new_load_data, content, flags=re.DOTALL)

# 4. Rewrite saveData to just a dummy or remove its inner logic
# Since some sync logic uses it, we'll keep it as a UI notification
new_save_data = """    function saveData(showNotification = true) {
      if(showNotification) showToast('Atualizando dados no servidor...', 'info');
    }"""
content = re.sub(r'function saveData\(.*?\) \{.*?\n    \}', new_save_data, content, flags=re.DOTALL, count=1)

# 5. Fix btn-modal-save click listener
# It currently pushes to `streets` and calls `saveData()`. We'll change it to use fetch.
# Because the script is complex, I will use a targeted replace for the inner part of btn-modal-save.
# Wait, replacing the exact listener might be tricky with regex. 
# Let's replace the whole btn-modal-save listener.
new_btn_modal_save = """    document.getElementById('btn-modal-save').addEventListener('click', async () => {
      const nome = document.getElementById('rua-nome').value.trim();
      const fieldNome = document.getElementById('field-nome');
      if(!nome) {
        fieldNome.classList.add('error');
        document.getElementById('rua-nome').focus();
        return showToast('Nome da rua é obrigatório!', 'error');
      }
      fieldNome.classList.remove('error');

      const cleanCoords = drawPoints.length > 1 
        ? drawPoints.map(p => ({ lat: p.lat, lng: p.lng })) 
        : [];

      const data = {
        nome: nome,
        bairro: document.getElementById('rua-bairro').value.trim(),
        tipo: document.getElementById('rua-tipo').value,
        pavimento: document.getElementById('rua-pavimento').value,
        inicio: document.getElementById('rua-inicio-desc').value.trim(),
        fim: document.getElementById('rua-fim-desc').value.trim(),
        largura: document.getElementById('rua-largura').value ? parseFloat(document.getElementById('rua-largura').value) : null,
        comprimento_manual: document.getElementById('rua-comprimento-manual').value ? parseFloat(document.getElementById('rua-comprimento-manual').value) : null,
        obs: document.getElementById('rua-obs').value.trim()
      };

      try {
        if(editingId) {
          const index = streets.findIndex(s => s.id === editingId);
          if(isDrawing && cleanCoords.length > 1) {
              data.coords = cleanCoords;
          } else {
              data.coords = streets[index].coords; // mantém a antiga
          }
          
          const res = await fetch(API_URL + '/ruas/' + editingId, {
            method: 'PUT',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(data)
          });
          
          if(res.ok) {
            streets[index] = await res.json();
            showToast(`Rua "${nome}" atualizada com sucesso!`, 'success');
          }
        } else {
          data.coords = cleanCoords;
          const res = await fetch(API_URL + '/ruas', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(data)
          });
          
          if(res.ok) {
            streets.push(await res.json());
            showToast(`Rua "${nome}" cadastrada com sucesso!`, 'success');
          }
        }
      } catch(e) {
        showToast('Erro ao comunicar com o servidor.', 'error');
        console.error(e);
      }

      renderTable();
      renderMapLayers();
      updateBadge();
      
      modal.classList.remove('active');
      cancelDrawing();
      if (typeof isSmartRouteMode !== 'undefined' && isSmartRouteMode) exitSmartRouteMode();
      if (typeof clearSmartRouteTemp !== 'undefined') clearSmartRouteTemp();
    });"""

content = re.sub(r"document\.getElementById\('btn-modal-save'\)\.addEventListener\('click', \(\) => \{.*?updateBadge\(\);\n    \}\);", new_btn_modal_save, content, flags=re.DOTALL)

# 6. Rewrite window.deleteStreet
new_delete_street = """    window.deleteStreet = async function(id) {
      const street = streets.find(s => s.id === id);
      if(!street) return;
      if(!confirm(`Tem certeza que deseja excluir a rua ${street.nome}?`)) return;
      
      try {
        const res = await fetch(API_URL + '/ruas/' + id, { method: 'DELETE' });
        if(res.ok) {
          streets = streets.filter(s => s.id !== id);
          if(mapLayers[id]) {
            map.removeLayer(mapLayers[id]);
            delete mapLayers[id];
          }
          renderTable();
          renderMapLayers();
          updateBadge();
          showToast(`Rua "${street.nome}" excluída.`, 'warning');
        }
      } catch(e) {
        showToast('Erro ao excluir do servidor.', 'error');
      }
    };"""

content = re.sub(r'window\.deleteStreet = function\(id\) \{.*?\n    \};', new_delete_street, content, flags=re.DOTALL)

# 7. Rewrite autoFetchCoords save logic
# Just replace `saveData(false);` with a PUT request.
content = content.replace(
"""street.coords = way.geometry.map(pt => ({ lat: pt.lat, lng: pt.lon }));
            saveData(false);""",
"""street.coords = way.geometry.map(pt => ({ lat: pt.lat, lng: pt.lon }));
            fetch(API_URL + '/ruas/' + id, {method: 'PUT', headers: {'Content-Type':'application/json'}, body: JSON.stringify(street)}).catch(e=>e);"""
)

content = content.replace(
"""street.coords = coords;
                      saveData(false);""",
"""street.coords = coords;
                      fetch(API_URL + '/ruas/' + id, {method: 'PUT', headers: {'Content-Type':'application/json'}, body: JSON.stringify(street)}).catch(e=>e);"""
)


# --- NOW PINOS ---

# 8. loadPins
new_load_pins = """    async function loadPins() {
      try {
        const res = await fetch(API_URL + '/pinos');
        if(res.ok) {
          userPins = await res.json();
        }
      } catch(e) {
        console.error("Falha ao carregar pinos da API:", e);
      }
      renderPins();
    }"""
content = re.sub(r'function loadPins\(\) \{.*?\n    \}', new_load_pins, content, flags=re.DOTALL)

# 9. savePins dummy
new_save_pins = """    function savePins() {
      // handled via api now
    }"""
content = re.sub(r'function savePins\(\) \{.*?\n    \}', new_save_pins, content, flags=re.DOTALL)

# 10. submit pin
# Find btn-save-pin
new_save_pin = """    document.getElementById('btn-save-pin').addEventListener('click', async () => {
      const name = document.getElementById('pin-name-input').value.trim();
      if (!name) return showToast('Digite um nome para o pino.', 'error');

      const data = {
        name: name,
        color: selectedPinColor,
        lat: pendingPinLatLng.lat,
        lng: pendingPinLatLng.lng
      };

      try {
        const res = await fetch(API_URL + '/pinos', {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify(data)
        });
        if(res.ok) {
          userPins.push(await res.json());
          renderPins();
          document.getElementById('pin-name-modal').classList.remove('active');
          cancelPinMode();
          showToast(`Pino "${name}" criado com sucesso!`, 'success');
        }
      } catch(e) {
         showToast('Erro ao criar pino no servidor.', 'error');
      }
    });"""
content = re.sub(r"document\.getElementById\('btn-save-pin'\)\.addEventListener\('click', \(\) => \{.*?\n    \}\);", new_save_pin, content, flags=re.DOTALL)

# 11. delete pin
new_delete_pin = """    window.deletePin = async function(index) {
      const pin = userPins[index];
      if(!pin) return;
      if(!confirm(`Deseja excluir o pino "${pin.name}"?`)) return;
      try {
        const res = await fetch(API_URL + '/pinos/' + pin.id, {method: 'DELETE'});
        if(res.ok) {
          userPins.splice(index, 1);
          renderPins();
          showToast('Pino excluído.', 'warning');
        }
      } catch(e) {
        showToast('Erro ao excluir pino.', 'error');
      }
    };"""
content = re.sub(r'window\.deletePin = function\(index\) \{.*?\n    \};', new_delete_pin, content, flags=re.DOTALL)

with open("mapeamentovias_prod.html", "w", encoding=encoding) as f:
    f.write(content)

print("Created mapeamentovias_prod.html successfully.")
