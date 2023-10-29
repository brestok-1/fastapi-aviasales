const currentURL = window.location.href;
const indexOfQuestionMark = currentURL.indexOf("?");
const searchParamsString = currentURL.substring(indexOfQuestionMark + 1);
const url = 'http://' + window.location.host + '/search-flights/?' + searchParamsString

fetch(url)
    .then(response => {
        if (response.ok) {
            return response.json()
        } else if (response.status === 401) {
            window.location.href = 'http://' + window.location.host + '/user/login';
        } else if (response.status === 404) {
            return response.json();
        } else {
            alert('Something was wrong...')
        }
    })
    .then(data => {
        if (data && data.message) {
            alert(data.message);
        } else {
            const departureInput = document.getElementById('departure_loc')
            const destinationInput = document.getElementById('destination-loc')
            const datePicker = document.getElementById('datepicker')
            const passengerField = document.getElementById('passengertype')
            const currentUrl = window.location.href.split("?")[1].split("&");

            const queryParams = {};
            currentUrl.forEach(function (param) {
                const paramParts = param.split("=");
                const paramName = decodeURIComponent(paramParts[0]);
                const paramValue = decodeURIComponent(paramParts[1]);
                queryParams[paramName] = paramValue;
            });
            const count = queryParams["count"];
            let countString
            if(count === '1'){
                countString = count + ' passenger'
            } else {
                countString = count + ' passengers'
            }

            let classType = queryParams["class_type"];
            const originalDate = data[0]['flight']['departure_time'];
            const dateObj = new Date(originalDate);
            const day = dateObj.getDate();
            const month = dateObj.getMonth() + 1;
            const year = dateObj.getFullYear();
            const formattedDate = `${day}-${month}-${year}`;
            classType = classType.charAt(0).toUpperCase() + classType.slice(1);
            departureInput.value = data[0]['flight']['departure']['location']
            destinationInput.value = data[0]['flight']['destination']['location']
            datePicker.value = formattedDate
            passengerField.className = 'bg-white border-passanger px-2 rounded-end py-1'

            passengerField.innerHTML = `<div class="py-3 text-black-50" id="passangersdiv" style="display: none" data-search="1">Passengers and type</div>
                                    <div class="text-black" id="passangercount" style="display: block;">
                                        ${countString}
                                    </div>
                                    <div class="text-black-50" id="passangerclass" style="display: block;">
                                        ${classType}
                                    </div>`


            const ticketList = document.getElementById('ticket-list')
            ticketList.innerHTML = ''
            console.log(data)
            data.forEach(flight => {
                    const flightElement = document.createElement('div')
                    flightElement.className = 'ticket row ticket-card mb-4'
                    flightElement.setAttribute("id", "ticket");

                    const ticketCount = flight['tickets_count']
                    const ticketPrice = flight['tickets_price']

                    flightElement.setAttribute("data-price", ticketPrice);
                    flightElement.setAttribute("data-count", ticketCount);

                    const options = {weekday: 'short', day: 'numeric', month: 'short'};
                    const dateDeparture = new Date(flight['flight']['departure_time'])
                    const hoursDeparture = dateDeparture.getHours()
                    const minutesDeparture = dateDeparture.getMinutes()
                    const formattedDepartureDate = new Intl.DateTimeFormat('en-US', options).format(dateDeparture)
                    const timeDeparture = `${hoursDeparture}:${minutesDeparture < 10 ? '0' : ''}${minutesDeparture}`;

                    const dateArrival = new Date(flight['flight']['arrival_time'])
                    const hoursArrival = dateArrival.getHours()
                    const minutesArrival = dateArrival.getMinutes()
                    const formattedArrivalDate = new Intl.DateTimeFormat('en-US', options).format(dateArrival)
                    const timeArrival = `${hoursArrival}:${minutesArrival < 10 ? '0' : ''}${minutesArrival}`;

                    const timeDifference = dateArrival - dateDeparture;
                    const hoursDifference = Math.floor(timeDifference / (1000 * 60 * 60));
                    const minutesDifference = Math.floor((timeDifference % (1000 * 60 * 60)) / (1000 * 60));
                    const flightTime = `${hoursDifference}h ${minutesDifference}m`;

                    const ticketsList = flight['flight']['tickets']
                    let ticketID = 0
                    let ticketCost = 0
                    for (let ticket = 0; ticket < ticketsList.length; ticket++) {
                        if (ticketsList[ticket]['class_type'] === "economy" && ticketsList[ticket]['status'] === 'available') {
                            ticketCost = ticketsList[ticket]['price']
                            ticketID = ticketsList[ticket]['id']
                            break
                        }
                    }
                    if (ticketCost === 0 && ticketID === 0) {
                        return
                    }
                    flightElement.innerHTML = `<div class="col-3 left-line">
                    <div class="ticket-price text-center mt-4 fs-5 fw-semibold">
                        ${ticketCost}$
                    </div>
                    <div class="d-flex my-3 justify-content-center">
                        <button type="button" class="btn btn-warning py-2 w-75 text-white fw-semibold btn-ticket-buy" data-ticket-id="${ticketID}">Buy ticket
                        </button>
                    </div>
                </div>
                <div class="col-9">
                    <div class="airline-title fw-semibold my-3 ms-3">
                        ${flight['flight']['plane']['model']}
                    </div>
                    <div class="row mb-4">
                        <div class="col-2">
                            <div class="ticket-minutes">
                                ${timeDeparture}
                            </div>
                            <div class="ticket-city fw-light">
                                ${flight['flight']['departure']['location']}
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
                                        ${flight['flight']['departure']['title']}
                                    </span>
                                <span class="ticket-plane-color flight-time">
                                        ${flight['flight']['destination']['title']}
                                    </span>
                            </div>
                        </div>
                        <div class="col-2">
                            <div class="ticket-minutes">
                                ${timeArrival}
                            </div>
                            <div class="ticket-city fw-light">
                                ${flight['flight']['destination']['location']}
                            </div>
                            <div class="ticket-date fw-light">
                                ${formattedArrivalDate}
                            </div>
                        </div>
                    </div>
                </div>`
                    ticketList.appendChild(flightElement)
                }
            )
        }
    })
