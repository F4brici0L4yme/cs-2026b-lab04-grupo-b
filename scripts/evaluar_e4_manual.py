import ast,json,pathlib,subprocess,tempfile
root=pathlib.Path(__file__).resolve().parents[1]; base=root/'prompts/pruebas_eta'; cases=json.loads((base/'casos.json').read_text()); results={}
for ver in ('v1','v2','v3'):
 checks={'json':0,'id':0,'three_asserts':0,'pytest_pass':0}
 for c in cases:
  raw=(base/'grabaciones'/ver/(c['id']+'.txt')).read_text()
  try: x=json.loads(raw); checks['json']+=1
  except ValueError: continue
  if x.get('caso_id')==c['id']: checks['id']+=1
  try:
   tree=ast.parse(x.get('pruebas','')); count=sum(isinstance(n,ast.Assert) for n in ast.walk(tree))
   if count>=3: checks['three_asserts']+=1
   safe=all(not isinstance(n,(ast.Import,ast.ImportFrom,ast.Global,ast.Nonlocal)) for n in ast.walk(tree))
   if count>=3 and safe:
    source=c['codigo']+'\n'+x['pruebas']
    with tempfile.NamedTemporaryFile('w',suffix='.py',delete=False) as f: f.write(source); name=f.name
    r=subprocess.run(['python3','-m','pytest','-q',name],capture_output=True,text=True)
    pathlib.Path(name).unlink(missing_ok=True)
    checks['pytest_pass']+=int(r.returncode==0)
  except (SyntaxError,ValueError): pass
 results[ver]={k:{'pass':v,'total':8,'pct':round(v*12.5,1)} for k,v in checks.items()}
out={'source':'simulated fixtures, deterministic offline checks; not live model output','results':results}
(base.parent.parent/'evidencias/e4-manual.json').write_text(json.dumps(out,indent=2)+'\n'); print(json.dumps(out,indent=2))
