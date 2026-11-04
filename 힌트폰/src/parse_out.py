import sys, re
d = open(sys.argv[1], encoding='utf-8', errors='replace').read()
m = re.search(r'<pre id="testout">(.*?)</pre>', d, re.S); t = m.group(1) if m else 'NO OUTPUT'
print('\n'.join(l for l in t.split('\n') if not l.startswith('PASS'))); print(sys.argv[2], t.count('PASS'), 'pass', t.count('FAIL'), 'fail')
