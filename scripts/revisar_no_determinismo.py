import json
from pathlib import Path
p=Path('evidencias/no-determinismo'); summary=json.loads((p/'resumen.json').read_text())
for case in summary['casos']:
 files=[p/f'{case}-intento-{i}.txt' for i in range(1,4)]
 vals=[json.loads(x.read_text()) for x in files]
 assert all(v['historia_id']==case for v in vals)
 assert len({v['invest_ok'] for v in vals})==1
 assert len({json.dumps(v,sort_keys=True) for v in vals})==3
 print(f'{case}: 3 respuestas parseables; decisión INVEST estable; redacción/escenarios varían')
