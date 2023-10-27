fetch('/latest-flights')
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
        if (data.length !== 0) {
            console.log(data)
            const listFlights = document.getElementById('list-flights')
            data.forEach(flight => {
                    const flightElement = document.createElement('div')
                    flightElement.className = 'row ticket-card mb-4'

                    const options = {weekday: 'short', day: 'numeric', month: 'short'};
                    const dateDeparture = new Date(flight['departure_time'])
                    const hoursDeparture = dateDeparture.getHours()
                    const minutesDeparture = dateDeparture.getMinutes()
                    const formattedDepartureDate = new Intl.DateTimeFormat('en-US', options).format(dateDeparture)
                    const timeDeparture = `${hoursDeparture}:${minutesDeparture < 10 ? '0' : ''}${minutesDeparture}`;

                    const dateArrival = new Date(flight['arrival_time'])
                    const hoursArrival = dateArrival.getHours()
                    const minutesArrival = dateArrival.getMinutes()
                    const formattedArrivalDate = new Intl.DateTimeFormat('en-US', options).format(dateArrival)
                    const timeArrival = `${hoursArrival}:${minutesArrival < 10 ? '0' : ''}${minutesArrival}`;

                    const timeDifference = dateArrival - dateDeparture;
                    const hoursDifference = Math.floor(timeDifference / (1000 * 60 * 60));
                    const minutesDifference = Math.floor((timeDifference % (1000 * 60 * 60)) / (1000 * 60));
                    const flightTime = `${hoursDifference}h ${minutesDifference}m`;

                    const ticketsList = flight['tickets']
                    let ticketCost = 0
                    for (let ticket = 0; ticket < ticketsList.length; ticket++) {
                        if (ticketsList[ticket]['class_type'] === "economy"){
                            ticketCost = ticketsList[ticket]['price']
                            break
                        }
                    }
                    flightElement.innerHTML = `<div class="col-3 left-line">
                    <div class="ticket-price text-center mt-4 fs-5 fw-semibold">
                        ${ticketCost}$
                    </div>
                    <div class="d-flex my-3 justify-content-center">
                        <button type="submit" class="btn btn-warning py-2 w-75 text-white fw-semibold">Buy ticket
                        </button>
                    </div>
                </div>
                <div class="col-9">
                    <div class="airline-title fw-semibold my-3 ms-3">
                        ${flight['plane']['model']}
                    </div>
                    <div class="row mb-4">
                        <div class="col-2">
                            <div class="ticket-minutes">
                                ${timeDeparture}
                            </div>
                            <div class="ticket-city fw-light">
                                ${flight['departure']['location']}
                            </div>
                            <div class="ticket-date fw-light">
                                ${formattedDepartureDate}
                            </div>
                        </div>
                        <div class="col-8">
                            <div class="ticket-plane-color d-flex justify-content-between my-2">
                                <i class="fa-solid fa-plane-departure"></i>
                                <span class="flight-time">
                                        Flight time: ${flightTime}
                                    </span>
                                <i class="fa-solid fa-plane-arrival"></i>
                            </div>
                            <div class="horizontal-ticket-line"></div>
                            <div class="airport-name d-flex justify-content-between mt-2">
                                    <span class="ticket-plane-color flight-time">
                                        ${flight['departure']['title']}
                                    </span>
                                <span class="ticket-plane-color flight-time">
                                        ${flight['destination']['title']}
                                    </span>
                            </div>
                        </div>
                        <div class="col-2">
                            <div class="ticket-minutes">
                                ${timeArrival}
                            </div>
                            <div class="ticket-city fw-light">
                                ${flight['destination']['location']}
                            </div>
                            <div class="ticket-date fw-light">
                                ${formattedArrivalDate}
                            </div>
                        </div>
                    </div>
                </div>`
                    listFlights.appendChild(flightElement)
                }
            )
        }
    })