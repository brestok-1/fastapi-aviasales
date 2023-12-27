const cartModal = document.getElementById('cart-modal');
cartModal.addEventListener('shown.bs.modal', function (event) {
    fetch('/purchase-history')
        .then(response => {
            if (response.ok) {
                return response.json()
            } else if (response.status === 401) {
                window.location.href = 'http://' + window.location.host + '/user/login';
            } else {
                alert('Something was wrong...')
            }
        })
        .then(data => {
            console.log(data)
            const tbody = document.getElementById('tableticketbody');
            tbody.innerHTML = ''
            data.forEach(purchase => {
                const options = {weekday: 'short', day: 'numeric', month: 'short'};
                const dateDeparture = new Date(purchase['departure_time'])
                const hoursDeparture = dateDeparture.getHours()
                const minutesDeparture = dateDeparture.getMinutes()
                const formattedDepartureDate = new Intl.DateTimeFormat('en-US', options).format(dateDeparture)
                const timeDeparture = `${hoursDeparture}:${minutesDeparture < 10 ? '0' : ''}${minutesDeparture}`;

                const dateArrival = new Date(purchase['arrival_time'])
                const hoursArrival = dateArrival.getHours()
                const minutesArrival = dateArrival.getMinutes()
                const formattedArrivalDate = new Intl.DateTimeFormat('en-US', options).format(dateArrival)
                const timeArrival = `${hoursArrival}:${minutesArrival < 10 ? '0' : ''}${minutesArrival}`;

                const tr = document.createElement('tr')
                tr.innerHTML = `
                        <th class='fw-normal'>${purchase['flight_id']}</th>
                        <td>${purchase['price']}$</td>
                        <td>${purchase['departure']} <i class="fa-solid fa-arrow-right"></i> ${purchase['destination']}</td>
                        <td>${purchase['class_type']}</td>
                        <td>${timeDeparture}, ${formattedDepartureDate}</td>
                        <td>${timeArrival}, ${formattedArrivalDate}</td>
               
                        `
                tbody.appendChild(tr)
            });
        })
        .catch(error => {
            console.error('Error during request:', error);
        });
});
