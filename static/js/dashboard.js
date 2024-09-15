$(function() {
    let url = `ws://${window.location.host}/ws/monitoring/`;
    
    let dashboard = new WebSocket(url);

    // Variable global para almacenar la instancia del gráfico
    let salesChartInstance = null;

    dashboard.onopen = function(e) {
        console.log('CONECTADO');
    };

    dashboard.onclose = function(e) {
        console.log('DESCONECTADO');
    };

    dashboard.onmessage = function(event) {
        var data = JSON.parse(event.data);
        console.log(data);

        // Mostrar el producto más vendido
        document.getElementById('mostSoldProductName').textContent = data.most_sold_product.product_name;
        document.getElementById('mostSoldProductQuantity').textContent = data.most_sold_product.total_quantity_sold;

        // Mostrar el delivery con más pedidos
        document.getElementById('topDeliveryName').textContent = data.top_delivery.delivery_name;
        document.getElementById('topDeliveryOrders').textContent = data.top_delivery.total_orders;

        // Mostrar solo las tarjetas de ingresos si es la primera vez
        const revenueContainer = document.getElementById('revenueCards');
        if(revenueContainer.hasChildNodes())revenueContainer.innerHTML = '';  // Limpiar tarjetas anteriores
        data.total_revenue_per_product.forEach(product => {
            const cardHtml = `
                <div class="col-md-4 mb-4">
                    <div class="card">
                        <div class="card-header bg-primary text-white">${product.product_name}</div>
                        <div class="card-body">
                            <h5 class="card-title">Ingresos Totales</h5>
                            <p class="card-text">$${product.total_revenue.toFixed(2)}</p>
                        </div>
                    </div>
                </div>`;
            revenueContainer.insertAdjacentHTML('beforeend', cardHtml);
        });


        // Actualizar los datos del gráfico sin destruirlo
        const productNames = data.total_sales_per_product.map(product => product.product_name);
        const productQuantities = data.total_sales_per_product.map(product => product.total_quantity_sold);

        if (salesChartInstance) {
            // Actualizar los datos del gráfico
            salesChartInstance.data.labels = productNames;
            salesChartInstance.data.datasets[0].data = productQuantities;
            salesChartInstance.update();  // Aplicar los cambios
        } else {
            // Crear una nueva instancia del gráfico si no existe
            const ctx = document.getElementById('salesChart').getContext('2d');
            salesChartInstance = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: productNames,
                    datasets: [{
                        label: 'Total Vendido',
                        data: productQuantities,
                        backgroundColor: [
                            'rgba(255, 99, 132, 0.2)',
                            'rgba(54, 162, 235, 0.2)',
                            'rgba(255, 206, 86, 0.2)',
                            'rgba(75, 192, 192, 0.2)',
                            'rgba(153, 102, 255, 0.2)'
                        ],
                        borderColor: [
                            'rgba(255, 99, 132, 1)',
                            'rgba(54, 162, 235, 1)',
                            'rgba(255, 206, 86, 1)',
                            'rgba(75, 192, 192, 1)',
                            'rgba(153, 102, 255, 1)'
                        ],
                        borderWidth: 1
                    }]
                },
                options: {
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    },
                    plugins: {
                        legend: {
                            display: false
                        }
                    },
                    animation: false
                }
            });
        }
    };

    dashboard.onerror = function(error) {
        console.error(`Error en WebSocket: ${error.message}`);
    };
});
