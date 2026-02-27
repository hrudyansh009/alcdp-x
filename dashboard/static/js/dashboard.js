let topChart = null;
let timelineChart = null;

async function fetchJSON(url) {
  const r = await fetch(url);
  return await r.json();
}

function riskColor(score) {
  if (score >= 60) return "red";
  if (score >= 30) return "yellow";
  return "lime";
}

function buildTopAttackers(events) {
  const map = {};
  for (const e of events) {
    if (!e.ip) continue;
    map[e.ip] = Math.max(map[e.ip] || 0, e.risk_score || 0);
  }
  const rows = Object.entries(map)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 8);

  return {
    labels: rows.map(r => r[0]),
    scores: rows.map(r => r[1]),
  };
}

function buildTimeline(events) {
  const last = events.slice(-30);
  return {
    labels: last.map(e => (e.timestamp || "").split("T")[1]?.split(".")[0] || ""),
    scores: last.map(e => e.risk_score || 0),
  };
}

function renderTables(sessions, incidents) {
  const sBody = document.querySelector("#sessionsTable tbody");
  sBody.innerHTML = "";
  sessions.forEach(s => {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${s.ip}</td>
      <td>${s.event_count}</td>
      <td>${s.max_risk}</td>
      <td>${s.escalation}</td>
    `;
    sBody.appendChild(tr);
  });

  const iBody = document.querySelector("#incidentsTable tbody");
  iBody.innerHTML = "";
  incidents.forEach(i => {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${i.id}</td>
      <td>${i.ip}</td>
      <td>${i.severity}</td>
      <td>${i.events}</td>
      <td>${i.risk}</td>
      <td>${i.status}</td>
    `;
    iBody.appendChild(tr);
  });
}

async function refresh() {
  const events = await fetchJSON("/api/events");
  const sessions = await fetchJSON("/api/sessions");
  const incidents = await fetchJSON("/api/incidents");

  const top = buildTopAttackers(events);
  const tl = buildTimeline(events);

  // Top attackers chart
  if (!topChart) {
    topChart = new Chart(document.getElementById("topAttackersChart"), {
      type: "bar",
      data: {
        labels: top.labels,
        datasets: [{
          label: "Max Risk",
          data: top.scores,
          backgroundColor: top.scores.map(riskColor),
        }]
      },
      options: {
        responsive: true,
        animation: false,
        scales: { y: { beginAtZero: true, max: 100 } }
      }
    });
  } else {
    topChart.data.labels = top.labels;
    topChart.data.datasets[0].data = top.scores;
    topChart.data.datasets[0].backgroundColor = top.scores.map(riskColor);
    topChart.update();
  }

  // Timeline chart
  if (!timelineChart) {
    timelineChart = new Chart(document.getElementById("riskTimelineChart"), {
      type: "line",
      data: {
        labels: tl.labels,
        datasets: [{
          label: "Risk",
          data: tl.scores,
        }]
      },
      options: {
        responsive: true,
        animation: false,
        scales: { y: { beginAtZero: true, max: 100 } }
      }
    });
  } else {
    timelineChart.data.labels = tl.labels;
    timelineChart.data.datasets[0].data = tl.scores;
    timelineChart.update();
  }

  renderTables(sessions, incidents);
}

refresh();
setInterval(refresh, 2000);
