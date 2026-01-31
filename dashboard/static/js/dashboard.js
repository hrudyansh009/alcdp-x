const logBox = document.getElementById("logBox");

const ctx = document.getElementById("attackChart").getContext("2d");

const chart = new Chart(ctx, {
    type: "bar",
    data: {
        labels: [],
        datasets: [{
            label: "Attack Events",
            data: [],
        }]
    }
});

async function loadData() {
    const res = await fetch("/api/attacks");
    const data = await res.json();

    let counts = {};
    logBox.textContent = "";

    data.forEach(event => {
        const type = event.eventid || "unknown";
        counts[type] = (counts[type] || 0) + 1;
        logBox.textContent += JSON.stringify(event, null, 2) + "\n\n";
    });

    chart.data.labels = Object.keys(counts);
    chart.data.datasets[0].data = Object.values(counts);
    chart.update();
}

setInterval(loadData, 3000);
loadData();
