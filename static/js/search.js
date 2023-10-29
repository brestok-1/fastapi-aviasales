const searchForm = document.getElementById('search-form')
searchForm.addEventListener('submit', async (event) => {
    event.preventDefault()
    const departureText = document.getElementById('departure_loc').value.toLocaleLowerCase().trim()
    const destinationText = document.getElementById('destination-loc').value.toLowerCase().trim()
    const departureDate = document.getElementById('datepicker').value
    const passengerStr = document.getElementById('passangercount').textContent.trim()
    const passengerCount = passengerStr.split(' ')[0]
    const passengerClass = document.getElementById('passangerclass').textContent.toLocaleLowerCase().trim()
    const url = `/search/?departure=${encodeURIComponent(departureText)}&destination=${encodeURIComponent(destinationText)}&departure_date=${departureDate}&count=${encodeURIComponent(passengerCount)}&class_type=${encodeURIComponent(passengerClass)}`;
    window.location.href = 'http://' + window.location.host + url;
})
