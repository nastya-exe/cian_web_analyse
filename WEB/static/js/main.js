document.addEventListener('DOMContentLoaded', () => {

    // Основной график
    const ctxMain = document.getElementById('myChart').getContext('2d');
    const labelsRange = window.hist_info.map(item => item[0]);
    const dataQuants = window.hist_info.map(item => item[1]);
    new Chart(ctxMain, {
        type: 'bar',
        data: {
            labels: labelsRange,
            datasets: [{
                label: 'Цена, тыс ₽',
                data: dataQuants,
//                салатовый зеленый
                backgroundColor: '#8DC63F'
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { display: false },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return context.parsed.y;
                        }
                    }
                }
            },
            scales: { y: { beginAtZero: true } }
        }
    });

    // График для дорогих станций
    const ctxExp = document.getElementById('expensiveChart').getContext('2d');
    const labelsMax = window.metro_max.map(item => item[0]);
    const dataMax = window.metro_max.map(item => item[1]);

    new Chart(ctxExp, {
        type: 'bar',
        data: {
            labels: labelsMax,
            datasets: [{
                label: 'Цена ₽/м²',
                data: dataMax,
                backgroundColor: '#F2542D'
            }]
        },
        options: {
            responsive: true,
            plugins: { legend: { display: false } },
            scales: {
                y: {
                    beginAtZero: false,
                    ticks: {
                        callback: function(value) { return value.toLocaleString() + ' ₽'; }
                    }
                }
            }
        }
    });

    // График для дешёвых станций
    const ctxCheap = document.getElementById('cheapChart').getContext('2d');
    const labelsMin = window.metro_min.map(item => item[0]);
    const dataMin = window.metro_min.map(item => item[1]);
    new Chart(ctxCheap, {
        type: 'bar',
        data: {
            labels: labelsMin,
            datasets: [{
                label: 'Цена ₽/м²',
                data: dataMin,
                backgroundColor: '#8DC63F'
            }]
        },
        options: {
            responsive: true,
            plugins: { legend: { display: false } },
            scales: {
                y: {
                    beginAtZero: false,
                    ticks: {
                        callback: function(value) { return value.toLocaleString() + ' ₽'; }
                    }
                }
            }
        }
    });

    // Круговая диаграмма (соотношение типов помещений)
    const pieCtx = document.getElementById('pieChart').getContext('2d');
    const labelType = window.type_premises.map(item => item[0]);
    const dataQuant = window.type_premises.map(item => item[1]);

    const pieChart = new Chart(pieCtx, {
        type: 'pie',
        data: {
            labels: labelType,
            datasets: [{
                data: dataQuant,
                backgroundColor: ['#FF8C42', '#00B4D8', '#90BE6D', '#F9C74F']
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { position: 'bottom' },
                title: { display: true, text: 'Соотношение типов помещений' }
            }
        }
    });


});
