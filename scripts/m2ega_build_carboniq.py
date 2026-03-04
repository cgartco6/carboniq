# MEGA_BUILD_CARBONIQ.py
import os, json, shutil, zipfile
from fpdf import FPDF
import matplotlib.pyplot as plt

BASE_DIR = "CarbonIQ"

# ======== 1️⃣ CREATE FOLDERS ========
folders = [
    "css","js","assets/logos","assets/images","demo","white-label","investor","scripts"
]
for f in folders:
    os.makedirs(os.path.join(BASE_DIR,f), exist_ok=True)

# ======== 2️⃣ CREATE DASHBOARD METRICS JSON ========
metrics = {
    "fuel_savings":[120,135,150,160,155,170,180],
    "carbon_credits":[5,6,7,6.5,7.2,8,8.5],
    "fleet_efficiency":[78,80,82,81,83,85,86]
}
with open(os.path.join(BASE_DIR,"assets/dashboard_metrics.json"),"w") as f:
    json.dump(metrics,f)
print("Dashboard metrics JSON created")

# ======== 3️⃣ CREATE CSS FILE ========
css_content = """
/* Basic CSS embedded earlier, can be expanded */
body { font-family: 'Inter', sans-serif; background:#F5F5F5; color:#111;}
header{background:#0B6623;color:white;padding:6rem 2rem;text-align:center;}
button{background:#F4C430;border:none;padding:1rem 2rem;border-radius:.5rem;cursor:pointer;}
"""
with open(os.path.join(BASE_DIR,"css/style.css"),"w") as f:
    f.write(css_content)
print("CSS created")

# ======== 4️⃣ CREATE JS FILES ========
js_dashboard = """
const ctx = document.getElementById('dashboardChart').getContext('2d');
let chart;
async function fetchMetrics(){const res=await fetch('assets/dashboard_metrics.json');return await res.json();}
async function initChart(){const metrics=await fetchMetrics();chart=new Chart(ctx,{type:'line',data:{labels:['Jan','Feb','Mar','Apr','May','Jun','Jul'],datasets:[{label:'Fuel Savings',data:metrics.fuel_savings,borderColor:'#0B6623',backgroundColor:'rgba(11,102,35,0.2)',fill:true}]},options:{responsive:true,plugins:{legend:{display:true}}}});}
async function updateChart(tab){const metrics=await fetchMetrics();if(tab==='fuel'){chart.data.datasets[0].label='Fuel Savings';chart.data.datasets[0].data=metrics.fuel_savings;chart.data.datasets[0].borderColor='#0B6623';chart.data.datasets[0].backgroundColor='rgba(11,102,35,0.2)';}else if(tab==='carbon'){chart.data.datasets[0].label='Carbon Credits';chart.data.datasets[0].data=metrics.carbon_credits;chart.data.datasets[0].borderColor='#F4C430';chart.data.datasets[0].backgroundColor='rgba(244,196,48,0.2)';}else if(tab==='fleet'){chart.data.datasets[0].label='Fleet Efficiency';chart.data.datasets[0].data=metrics.fleet_efficiency;chart.data.datasets[0].borderColor='#C7CCD1';chart.data.datasets[0].backgroundColor='rgba(199,204,209,0.2)';}chart.update();}
document.querySelectorAll('.tab').forEach(tab=>{tab.addEventListener('click',()=>{document.querySelectorAll('.tab').forEach(t=>t.classList.remove('active'));tab.classList.add('active');updateChart(tab.dataset.tab);});});
initChart();
"""
with open(os.path.join(BASE_DIR,"js/dashboard.js"),"w") as f:
    f.write(js_dashboard)
print("Dashboard JS created")

# ======== 5️⃣ CREATE INDEX.HTML ========
index_html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>CarbonIQ SaaS Demo</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="css/style.css">
</head>
<body>
<header><h1>CarbonIQ</h1><p>Fuel Intelligence. Carbon Value. Verified.</p><button>Request Demo</button></header>
<section><h2>Features</h2><div class="features"><div class="feature-card"><h3>Fuel Optimization</h3><p>AI analytics for every engine type.</p></div><div class="feature-card"><h3>Carbon Intelligence</h3><p>Automatic carbon credit calculations.</p></div><div class="feature-card"><h3>Fleet Management</h3><p>Integrate OBD-II, SCADA, industrial systems.</p></div><div class="feature-card"><h3>Compliance Automation</h3><p>Regulatory packs & tender readiness.</p></div></div></section>
<section><h2>Testimonials</h2><div class="testimonials"><div class="testimonial">“CarbonIQ cut our fuel costs dramatically.” – Logistics Director</div><div class="testimonial">“Carbon reporting saves weeks of work.” – ESG Manager</div><div class="testimonial">“Industrial SCADA integration was effortless.” – Mining Ops</div></div></section>
<section><h2>Pricing</h2><div class="pricing-cards"><div class="card"><h3>Core</h3><p>SMEs / Individual</p><button>Select</button></div><div class="card"><h3>Fleet</h3><p>Logistics / Delivery</p><button>Select</button></div><div class="card"><h3>Industrial</h3><p>Mining / Heavy Industry</p><button>Select</button></div><div class="card"><h3>Government</h3><p>Public Sector</p><button>Select</button></div></div></section>
<section><h2>AI Dashboard</h2><div class="dashboard"><div class="tabs"><div class="tab active" data-tab="fuel">Fuel Savings</div><div class="tab" data-tab="carbon">Carbon Credits</div><div class="tab" data-tab="fleet">Fleet Efficiency</div></div><canvas id="dashboardChart"></canvas></div></section>
<footer><p>© 2026 CarbonIQ. All rights reserved.</p><div class="partner-logos"><img src="assets/logos/logo.png" alt="Partner Logo"></div></footer>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script src="js/dashboard.js"></script>
</body>
</html>
"""
with open(os.path.join(BASE_DIR,"index.html"),"w") as f:
    f.write(index_html)
print("index.html created")

# ======== 6️⃣ CREATE ONE-CLICK INSTALLER ========
installer_sh = "#!/bin/bash\necho 'Launching CarbonIQ Demo...'\nxdg-open index.html || open index.html"
with open(os.path.join(BASE_DIR,"demo/ONE_CLICK_INSTALL.sh"),"w") as f:
    f.write(installer_sh)
print("Installer created")

# ======== 7️⃣ GENERATE DASHBOARD CHART IMAGES & PDF ========
# Fuel
plt.plot(metrics['fuel_savings'], marker='o', color='green')
plt.title('Fuel Savings (Litres)')
plt.savefig(os.path.join(BASE_DIR,'assets/fuel_chart.png'))
plt.clf()
# Carbon
plt.plot(metrics['carbon_credits'], marker='o', color='gold')
plt.title('Carbon Credits (Tonnes)')
plt.savefig(os.path.join(BASE_DIR,'assets/carbon_chart.png'))
plt.clf()
# Fleet
plt.plot(metrics['fleet_efficiency'], marker='o', color='gray')
plt.title('Fleet Efficiency (%)')
plt.savefig(os.path.join(BASE_DIR,'assets/fleet_chart.png'))

# PDF
pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial",'B',24)
pdf.cell(0,10,"CarbonIQ Investor Deck",0,1,'C')
pdf.ln(10)
pdf.set_font("Arial",'',14)
pdf.multi_cell(0,7,"Features: Fuel optimization, Carbon intelligence, Fleet management, Compliance automation.",0,1)
pdf.ln(5)
pdf.image(os.path.join(BASE_DIR,'assets/fuel_chart.png'),w=180)
pdf.ln(5)
pdf.image(os.path.join(BASE_DIR,'assets/carbon_chart.png'),w=180)
pdf.ln(5)
pdf.image(os.path.join(BASE_DIR,'assets/fleet_chart.png'),w=180)
pdf.output(os.path.join(BASE_DIR,'investor/CarbonIQ_Investor_Deck.pdf'))
print("Investor PDF generated")

# ======== 8️⃣ GENERATE 5 WHITE-LABEL VERSIONS ========
for i in range(1,6):
    dest = os.path.join(BASE_DIR,f'white-label/partner{i}.html')
    shutil.copy(os.path.join(BASE_DIR,"index.html"), dest)
    with open(dest,'r') as f:
        html = f.read()
    html = html.replace("CarbonIQ",f"Partner{i}")
    with open(dest,'w') as f:
        f.write(html)
print("5 white-label HTML files generated")

# ======== 9️⃣ CREATE ZIP ========
zipf = zipfile.ZipFile("CarbonIQ_Demo.zip","w", zipfile.ZIP_DEFLATED)
for root, dirs, files in os.walk(BASE_DIR):
    for file in files:
        zipf.write(os.path.join(root,file), os.path.relpath(os.path.join(root,file), BASE_DIR))
zipf.close()
print("CarbonIQ_Demo.zip created successfully!")
