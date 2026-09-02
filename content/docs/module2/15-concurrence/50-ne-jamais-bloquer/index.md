---
title: "Ne jamais bloquer"
slug: "ne-jamais-bloquer"
weight: 50
---

# Ne jamais bloquer

<!-- MESURÉ le 2 septembre 2026 dans la page, Pyodide 3.12.7 : threading.Thread
     -> RuntimeError: can't start new thread ; os.fork et multiprocessing ->
     OSError 52 Function not implemented ; MAIS `await asyncio.sleep(0.1)` via
     runPythonAsync fonctionne (737 ms au premier appel, chauffe de la boucle
     comprise). Donc l'exemple asyncio de cette sous-section PEUT être un bloc
     exécutable dans la page, par le shortcode pyodide,, contrairement aux exemples de
     threads de la sous-section 20. À exploiter : ce serait l'exemple Python le
     plus fort de la section, l'étudiant le lance lui-même. Vérifier que le
     shortcode pyodide passe par runPythonAsync (ou l'adapter). -->
