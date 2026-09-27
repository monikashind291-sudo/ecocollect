// EcoCollect - Charts Initialization using Chart.js

function renderEcoCharts(categoryData, statusData) {
    // 1. Waste Category Distribution Chart (Doughnut)
    const categoryCtx = document.getElementById("categoryChart");
    if (categoryCtx && categoryData) {
        const labels = Object.keys(categoryData);
        const dataValues = Object.values(categoryData);

        const colorMap = {
            "Plastic": "#0ea5e9",
            "Paper": "#3b82f6",
            "Glass": "#10b981",
            "Metal": "#f59e0b",
            "E-Waste": "#8b5cf6",
            "Organic Waste": "#16a34a",
            "Other": "#94a3b8"
        };

        const bgColors = labels.map(l => colorMap[l] || "#059669");

        new Chart(categoryCtx, {
            type: "doughnut",
            data: {
                labels: labels,
                datasets: [{
                    data: dataValues,
                    backgroundColor: bgColors,
                    borderWidth: 2,
                    borderColor: "#ffffff"
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: "bottom",
                        labels: {
                            boxWidth: 14,
                            font: { family: "'Plus Jakarta Sans', sans-serif", size: 12 }
                        }
                    }
                },
                cutout: "68%"
            }
        });
    }

    // 2. Request Status Breakdown Chart (Bar)
    const statusCtx = document.getElementById("statusChart");
    if (statusCtx && statusData) {
        const statusLabels = Object.keys(statusData);
        const statusCounts = Object.values(statusData);

        const statusColorMap = {
            "Pending": "#f59e0b",
            "Scheduled": "#3b82f6",
            "Picked Up": "#8b5cf6",
            "Completed": "#10b981",
            "Cancelled": "#ef4444"
        };

        const barColors = statusLabels.map(s => statusColorMap[s] || "#059669");

        new Chart(statusCtx, {
            type: "bar",
            data: {
                labels: statusLabels,
                datasets: [{
                    label: "Number of Requests",
                    data: statusCounts,
                    backgroundColor: barColors,
                    borderRadius: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: { stepSize: 1 }
                    },
                    x: {
                        grid: { display: false }
                    }
                }
            }
        });
    }
}
