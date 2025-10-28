document.addEventListener('DOMContentLoaded', () => {

    // 🔹 Основной график
    const ctxMain = document.getElementById('myChart').getContext('2d');
    new Chart(ctxMain, {
        type: 'bar',
        data: {
            labels: ['Янв','Фев','Мар'],
            datasets: [{
                label: 'Цена, тыс ₽',
                data: [120,150,100],
                backgroundColor: '#4CAF50'
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { display: false },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return context.parsed.y + ' ₽';
                        }
                    }
                }
            },
            scales: { y: { beginAtZero: true } }
        }
    });

    // 🔹 График для дорогих станций
    const ctxExp = document.getElementById('expensiveChart').getContext('2d');
    new Chart(ctxExp, {
        type: 'bar',
        data: {
            labels: ['Парк Культуры','Арбатская','Киевская','Маяковская','Охотный ряд'],
            datasets: [{
                label: 'Цена ₽/м²',
                data: [290000,280000,270000,260000,255000],
                backgroundColor: '#d62828'
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

    // 🔹 График для дешёвых станций
    const ctxCheap = document.getElementById('cheapChart').getContext('2d');
    new Chart(ctxCheap, {
        type: 'bar',
        data: {
            labels: ['Котельники','Жулебино','Новокосино','Бунинская аллея','Щёлковская'],
            datasets: [{
                label: 'Цена ₽/м²',
                data: [85000,90000,92000,95000,97000],
                backgroundColor: '#2a9d8f'
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

    // 🔹 Затычка тепловой карты
const heatCtx = document.getElementById('heatmapChart').getContext('2d');
const heatmapChart = new Chart(heatCtx, {
    type: 'bar',
    data: {
        labels: ['Площадь <30м²', '30-50м²', '50-70м²', '70-90м²', '>90м²'],
        datasets: [
            { label: 'Студии', data: [5, 10, 7, 3, 2], backgroundColor: '#ff9999' },
            { label: 'Квартиры', data: [2, 7, 10, 5, 3], backgroundColor: '#66b3ff' },
            { label: 'Апартаменты', data: [1, 3, 4, 2, 1], backgroundColor: '#99ff99' }
        ]
    },
    options: {
        responsive: true,
        plugins: {
            legend: { position: 'top' },
            title: { display: true, text: 'Тепловая карта (затычка)' }
        },
        scales: {
            y: { beginAtZero: true }
        }
    }
});

// 🔹 Круговая диаграмма (соотношение типов квартир)
const pieCtx = document.getElementById('pieChart').getContext('2d');
const pieChart = new Chart(pieCtx, {
    type: 'pie',
    data: {
        labels: ['Студии', 'Квартиры', 'Апартаменты'],
        datasets: [{
            data: [15, 30, 5],
            backgroundColor: ['#ff9999','#66b3ff','#99ff99']
        }]
    },
    options: {
        responsive: true,
        plugins: {
            legend: { position: 'bottom' },
            title: { display: true, text: 'Соотношение типов квартир (затычка)' }
        }
    }
});

});
