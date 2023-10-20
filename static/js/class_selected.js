const passengerType = document.getElementById('passengertype');
const dropdownContainer = document.getElementById('dropdown-container');
const passangerDiv = document.getElementById('passangersdiv')
let doesntClick = true
let passangerCount = document.getElementById('passangercount')
let passangerClass = document.getElementById('passangerclass')

const passengerTypeComputedStyle = window.getComputedStyle(passengerType);
const passengerTypeWidth = parseInt(passengerTypeComputedStyle.width);

dropdownContainer.style.width = passengerTypeWidth + 'px';
passengerType.addEventListener('click', () => {
    if (dropdownContainer.style.display === 'none' || dropdownContainer.style.display === '') {
        if (doesntClick) {
            passangerDiv.style.display = 'none'
            passangerCount.style.display = 'block'
            passangerClass.style.display = 'block'
            passengerType.classList = 'bg-white border-passanger px-2 rounded-end py-1'
            doesntClick = false
        }
        dropdownContainer.style.display = 'block';
    } else {
        dropdownContainer.style.display = 'none';
    }
});

function updatePassengerCount(operator) {
    const counterValue = document.querySelector('.counter-value');
    let count = parseInt(counterValue.textContent);

    if (operator === '-' && count > 1) {
        count--;
    } else if (operator === '+') {
        count++;
    }
    if (count === 1) {
        passangerCount.textContent = count + ' passenger'
    } else {
        passangerCount.textContent = count + ' passengers'
    }
    counterValue.textContent = count;
}

function updateServiceClass(serviceClass) {
    passangerClass.textContent = serviceClass
}

