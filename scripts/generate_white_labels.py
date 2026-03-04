# scripts/generate_white_labels.py
import shutil, os

for i in range(1,6):
    src = "index.html"
    dest = f"white-label/partner{i}.html"
    shutil.copy(src,dest)
    # Optional: swap logos or colors dynamically
    with open(dest,'r') as f:
        html = f.read()
    html = html.replace("CarbonIQ","Partner"+str(i))
    with open(dest,'w') as f:
        f.write(html)
print("5 white-label versions generated")
