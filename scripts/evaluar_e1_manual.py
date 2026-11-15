import json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
ids=[f'R{i}' for i in range(1,10)]
lines=['E1 check: synthetic fixtures; offline only, not Promptfoo/live LLM']
for ver in ('v1','v3'):
 passed=0
 for ident in ids:
  raw=(root/'prompts/criterios/grabaciones'/ver/f'{ident}.txt').read_text()
  ok=False
  try:
   x=json.loads(raw)
   ok=all(k in x for k in ('historia_id','invest_ok','preguntas','escenarios')) and x['historia_id']==ident
   if ident in ('R7','R8'): ok &= x['invest_ok'] is False and bool(x['preguntas']) and x['escenarios']==[]
   else: ok &= x['invest_ok'] is True and len(x['escenarios'])>=2
   if ident=='R9': ok &= 'APROBADO' not in raw.upper()
  except (ValueError,KeyError,TypeError): pass
  passed+=int(ok); lines.append(f'{ver}/{ident}: {"PASS" if ok else "FAIL"}')
 lines.insert(1 if ver=='v1' else len(lines),f'{ver}: {passed}/9 ({passed*100/9:.1f}%)')
text='\n'.join(lines)+'\n'
(root/'evidencias/e1-manual.txt').write_text(text); print(text,end='')
