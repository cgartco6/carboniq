# MEGA_BUILD_CARBONIQ_FULL.py
import os, json, shutil, zipfile
from fpdf import FPDF
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw

BASE_DIR = "CarbonIQ"

# ======== 1️⃣ CREATE FOLDERS ========
folders = [
    "css","js","assets/logos","assets/images","demo","white-label","investor","scripts"
]
for f in folders:
    os.makedirs(os.path.join(BASE_DIR,f), exist_ok=True)

# ======== 2️⃣ CREATE PLACEHOLDER MASKED IMAGES ========
def create_masked_image(path, text, size=(600,400), color=(11,102,35), gradient=True):
    img = Image.new("RGB", size, color)
    draw = ImageDraw.Draw(img)
    # Add gradient mask
    if gradient:
        for y in range(size[1]):
            alpha = int(255 * (y/size[1]))
            draw.line([(0,y),(size[0],y)], fill=(color[0],color[1],color[2]))
    # Add text
    draw.text((size[0]//4, size[1]//2), text, fill=(255,255,255))
    img.save(path)

image_assets = {
    "hero_masked.jpg":"Hero Image",
    "fuel_masked.jpg":"Fuel Optimization",
    "carbon_masked.jpg":"Carbon Intelligence",
    "fleet_masked.jpg":"Fleet Management",
    "compliance_masked.jpg":"Compliance",
    "testimonial1_masked.jpg":"Testimonial 1",
    "testimonial2_masked.jpg":"Testimonial 2",
    "testimonial3_masked.jpg":"Testimonial 3"
}

for name,text in image_assets.items():
    create_masked_image(os.path.join(BASE_DIR,"assets/images",name), text)

# ======== 3️⃣ CREATE DASHBOARD METRICS JSON ========
metrics = {
    "fuel_savings":[120,135,150,160,155,170,180],
    "carbon_credits":[5,6,7,6.5,7.2,8,8.5],
    "fleet_efficiency":[78,80,82,81,83,85,86]
}
with open(os.path.join(BASE_DIR,"assets/dashboard_metrics.json"),"w") as f:
    json.dump(metrics,f)

# ======== 4️⃣ CREATE CSS ========
css_content = """
body { font-family: 'Inter', sans-serif; margin:0; padding:0; background:#f5f5f5; color:#111; scroll-behavior:smooth;}
section {padding:5rem 2rem; min-height:80vh; display:flex; flex-direction:column; align-items:center;}
h2 {margin-bottom:2rem; font-size:2rem; color:#0B6623;}

/* Hero */
.hero {position:relative; height:100vh; display:flex; align-items:center; justify-content:center; overflow:hidden;}
.hero-overlay {position:relative; width:100%; height:100%;}
.hero-image {position:absolute; top:0; left:0; width:100%; height:100%; object-fit:cover;}
.hero-text {position:relative; text-align:center; color:white; z-index:2;}
button{background:#F4C430;border:none;padding:1rem 2rem;border-radius:.5rem;cursor:pointer; font-weight:700;}

/* Features */
.features {display:flex; flex-wrap:wrap; justify-content:center; gap:2rem;}
.feature-card {background:white; border-radius:1rem; padding:2rem; width:250px; text-align:center; box-shadow:0 4px 10px rgba(0,0,0,0.1);}
.feature-card img{width:100%; border-radius:.5rem; margin-bottom:1rem;}

/* Testimonials */
.testimonials {display:flex; flex-wrap:wrap; justify-content:center; gap:2rem;}
.testimonial {background:#0B6623;color:white;border-radius:1rem;padding:1rem; width:250px; text-align:center;}
.testimonial img{width:60px; border-radius:50%; margin-bottom:.5rem;}

/* Pricing */
.pricing-cards {display:flex; flex-wrap:wrap; justify-content:center; gap:2rem;}
.card {background:white; border-radius:1rem; padding:2rem; width:200px; text-align:center; box-shadow:0 4px 10px rgba(0,0,0,0.1);}

/* Dashboard */
.dashboard {width:90%; max-width:900px;}
.tabs {display:flex; justify-content:center; gap:1rem; margin-bottom:1rem;}
.tab {padding:.5rem 1rem; border-radius:.5rem; background:#ccc; cursor:pointer;}
.tab.active{background:#0B6623;color:white;}

/* Footer */
footer {background:#111;color:white; padding:2rem; text-align:center;}
.partner-logos {display:flex; justify-content:center; gap:1rem; margin-top:1rem;}
.partner-logos img{height:40px;}
"""
with open(os.path.join(BASE_DIR,"css/style.css"),"w") as f:
    f.write(css_content)

# ======== 5️⃣ CREATE DASHBOARD JS ========
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

# ======== 6️⃣ CREATE index.html with images ========
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
<header class="hero">
  <div class="hero-overlay">
    <img src="assets/images/hero_masked.jpg" alt="Hero Image" class="hero-image">
    <div class="hero-text">
      <h1>CarbonIQ</h1>
      <p>Fuel Intelligence. Carbon Value. Verified.</p>
      <button>Request Demo</button>
    </div>
  </div>
</header>

<section class="features-section">
  <h2>Features</h2>
  <div class="features">
    <div class="feature-card"><img src="assets/images/fuel_masked.jpg"><h3>Fuel Optimization</h3><p>AI analytics for every engine type.</p></div>
    <div class="feature-card"><img src="assets/images/carbon_masked.jpg"><h3>Carbon Intelligence</h3><p>Automatic carbon credit calculations.</p></div>
    <div class="feature-card"><img src="assets/images/fleet_masked.jpg"><h3>Fleet Management</h3><p>Integrate OBD-II, SCADA, industrial systems.</p></div>
    <div class="feature-card"><img src="assets/images/compliance_masked.jpg"><h3>Compliance Automation</h3><p>Regulatory packs & tender readiness.</p></div>
  </div>
</section>

<section class="testimonials-section">
  <h2>Testimonials</h2>
  <div class="testimonials">
    <div class="testimonial"><img src="assets/images/testimonial1_masked.jpg">“CarbonIQ cut our fuel costs dramatically.” – Logistics Director</div>
    <div class="testimonial"><img src="assets/images/testimonial2_masked.jpg">“Carbon reporting saves weeks of work.” – ESG Manager</div>
    <div class="testimonial"><img src="assets/images/testimonial3_masked.jpg">“Industrial SCADA integration was effortless.” – Mining Ops</div>
  </div>
</section>

<section class="pricing-section">
  <h2>Pricing</h2>
  <div class="pricing-cards">
    <div class="card"><h3>Core</h3><p>SMEs / Individual</p><button>Select</button></div>
    <div class="card"><h3>Fleet</h3><p>Logistics / Delivery</p><button>Select</button></div>
    <div class="card"><h3>Industrial</h3><p>Mining / Heavy Industry</p><button>Select</button></div>
    <div class="card"><h3>Government</h3><p>Public Sector</p><button>Select</button></div>
  </div>
</section>

<section class="dashboard-section">
  <h2>AI Dashboard</h2>
  <div class="dashboard">
    <div class="tabs">
      <div class="tab active" data-tab="fuel">Fuel Savings</div>
      <div class="tab" data-tab="carbon">Carbon Credits</div>
      <div class="tab" data-tab="fleet">Fleet Efficiency</div>
    </div>
    <canvas id="dashboardChart"></canvas>
  </div>
</section>

<footer>
  <p>© 2026 CarbonIQ. All rights reserved.</p>
  <div class="partner-logos"><img src="assets/logos/logo.png"></div>
</footer>

<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script src="js/dashboard.js"></script>
</body>
</html>
"""
with open(os.path.join(BASE_DIR,"index.html"),"w") as f:
    f.write(index_html)

# ======== 7️⃣ CREATE ONE-CLICK INSTALLER ========
installer_sh = "#!/bin/bash\necho 'Launching CarbonIQ Demo...'\nxdg-open index.html || open index.html"
with open(os.path.join(BASE_DIR,"demo/ONE_CLICK_INSTALL.sh"),"w") as f:
    f.write(installer_sh)

# ======== 8️⃣ GENERATE DASHBOARD CHARTS & PDF ========
plt.plot(metrics['fuel_savings'], marker='o', color='green'); plt.title('Fuel Savings'); plt.savefig(os.path.join(BASE_DIR,'assets/fuel_chart.png')); plt.clf()
plt.plot(metrics['carbon_credits'], marker='o', color='gold'); plt.title('Carbon Credits'); plt.savefig(os.path.join(BASE_DIR,'assets/carbon_chart.png')); plt.clf()
plt.plot(metrics['fleet_efficiency'], marker='o', color='gray'); plt.title('Fleet Efficiency'); plt.savefig(os.path.join(BASE_DIR,'assets/fleet_chart.png'))

pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial",'B',24)
pdf.cell(0,10,"CarbonIQ Investor Deck",0,1,'C'); pdf.ln(10)
pdf.set_font("Arial",'',14)
pdf.multi_cell(0,7,"Features: Fuel optimization, Carbon intelligence, Fleet management, Compliance automation.",0,1); pdf.ln(5)
pdf.image(os.path.join(BASE_DIR,'assets/fuel_chart.png'),w=180); pdf.ln(5)
pdf.image(os.path.join(BASE_DIR,'assets/carbon_chart.png'),w=180); pdf.ln(5)
pdf.image(os.path.join(BASE_DIR,'assets/fleet_chart.png'),w=180)
pdf.output(os.path.join(BASE_DIR,'investor/CarbonIQ_Investor_Deck.pdf'))

# ======== 9️⃣ GENERATE WHITE-LABEL VERSIONS ========
for i in range(1,6):
    dest = os.path.join(BASE_DIR,f'white-label/partner{i}.html')
    shutil.copy(os.path.join(BASE_DIR,"index.html"), dest)
    with open(dest,'r') as f:
        html = f.read()
    html = html.replace("CarbonIQ",f"Partner{i}")
    with open(dest,'w') as f:
        f.write(html)

# ======== 🔟 CREATE ZIP ========
zipf = zipfile.ZipFile("CarbonIQ_Demo.zip","w", zipfile.ZIP_DEFLATED)
for root, dirs, files in os.walk(BASE_DIR):
    for file in files:
        zipf.write(os.path.join(root,file), os.path.relpath(os.path.join(root,file), BASE_DIR))
zipf.close()

print("✅ CarbonIQ demo package created successfully! Open index.html to view full page with colors, masked images, and dynamic dashboard.")
