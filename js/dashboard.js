const ctx = document.getElementById('dashboardChart').getContext('2d');
let chart;

async function fetchMetrics() {
  const res = await fetch('assets/dashboard_metrics.json');
  return await res.json();
}

async function initChart() {
  const metrics = await fetchMetrics();
  chart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: ['Jan','Feb','Mar','Apr','May','Jun','Jul'],
      datasets: [{
        label: 'Fuel Savings (Litres)',
        data: metrics.fuel_savings,
        borderColor: '#0B6623',
        backgroundColor: 'rgba(11,102,35,0.2)',
        fill:true
      }]
    },
    options: { responsive:true, plugins:{ legend:{ display:true }} }
  });
}

async function updateChart(tab) {
  const metrics = await fetchMetrics();
  if(tab==='fuel') {
    chart.data.datasets[0].label='Fuel Savings (Litres)';
    chart.data.datasets[0].data=metrics.fuel_savings;
    chart.data.datasets[0].borderColor='#0B6623';
    chart.data.datasets[0].backgroundColor='rgba(11,102,35,0.2)';
  } else if(tab==='carbon') {
    chart.data.datasets[0].label='Carbon Credits (Tonnes)';
    chart.data.datasets[0].data=metrics.carbon_credits;
    chart.data.datasets[0].borderColor='#F4C430';
    chart.data.datasets[0].backgroundColor='rgba(244,196,48,0.2)';
  } else if(tab==='fleet') {
    chart.data.datasets[0].label='Fleet Efficiency (%)';
    chart.data.datasets[0].data=metrics.fleet_efficiency;
    chart.data.datasets[0].borderColor='#C7CCD1';
    chart.data.datasets[0].backgroundColor='rgba(199,204,209,0.2)';
  }
  chart.update();
}

document.querySelectorAll('.tab').forEach(tab=>{
  tab.addEventListener('click',()=>{
    document.querySelectorAll('.tab').forEach(t=>t.classList.remove('active'));
    tab.classList.add('active');
    updateChart(tab.dataset.tab);
  });
});

initChart();
