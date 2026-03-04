# scripts/generate_investor_pdf.py
import json
import matplotlib.pyplot as plt
from fpdf import FPDF

with open('assets/dashboard_metrics.json') as f:
    metrics = json.load(f)

# Generate chart images
plt.plot(metrics['fuel_savings'], marker='o', color='green')
plt.title('Fuel Savings (Litres)')
plt.savefig('assets/fuel_chart.png')
plt.clf()

plt.plot(metrics['carbon_credits'], marker='o', color='gold')
plt.title('Carbon Credits (Tonnes)')
plt.savefig('assets/carbon_chart.png')
plt.clf()

plt.plot(metrics['fleet_efficiency'], marker='o', color='gray')
plt.title('Fleet Efficiency (%)')
plt.savefig('assets/fleet_chart.png')

# Create PDF
pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", 'B', 24)
pdf.cell(0,10,"CarbonIQ Investor Deck",0,1,'C')
pdf.ln(10)

pdf.set_font("Arial", '', 14)
pdf.multi_cell(0,7,"Features: Fuel optimization, Carbon intelligence, Fleet management, Compliance automation.",0,1)
pdf.ln(5)

pdf.image('assets/fuel_chart.png', w=180)
pdf.ln(5)
pdf.image('assets/carbon_chart.png', w=180)
pdf.ln(5)
pdf.image('assets/fleet_chart.png', w=180)

pdf.output('investor/CarbonIQ_Investor_Deck.pdf')
print("Investor PDF generated")
