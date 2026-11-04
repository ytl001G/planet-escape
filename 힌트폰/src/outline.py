import sys,re,collections
h=open(sys.argv[1],encoding='utf-8').read(); h=h[h.find('page-body'):]
for m in re.finditer(r'<h([23])[^>]*>(.*?)</h\1>|<summary>(.*?)</summary>',h,re.S):
    if m.group(2) is not None: print('#'*int(m.group(1)), re.sub('<[^>]+>','',m.group(2)).strip())
    else:
        s=h[m.end():]; s=s[:s.find('</details>')]
        c=collections.Counter(re.findall(r'highlight-(\w+)"',s))
        print('   >', re.sub('<[^>]+>','',m.group(3)).strip()[:45], dict(sorted(c.items())))
