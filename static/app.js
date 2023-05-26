function odswiezDane() {
    $.ajax({
        url: '/sensor_data_json',
        type: 'GET',
        dataType: 'json',
        success: function (data) {
            $('#czas').text(data.hour);
            $('#dzien').text(data.dataa);
            $('#slon').text(data.sensor + ' %');
            $('#gleba').text(data.soil_hum_level);
            $('#temperatura').text(data.temperature + ' °C');
            $('#wilg_pow').text(data.humidity + ' %');
        },
        complete: function () {
            // Odśwież dane co 1 sekund
            setTimeout(odswiezDane, 1000);
        }
    });
}

let light_state = 'off';

function light_change() {

    let button = document.getElementById('button-light');
    let buttonText = document.getElementById('napis');
    let buttonImage = document.getElementById('obrazek');

    if (light_state === 'off') {
        light_state = 'on';
        buttonText.textContent = 'WYŁĄCZ';
        buttonImage.src = '../static/idea2.png';
    } else {
        light_state = 'off';
        buttonText.textContent = 'WŁĄCZ';
        buttonImage.src = '../static/idea1.png';
    }

    button.classList.toggle('pressed');

    $.ajax({
        url: '/light_change',
        type: 'POST',
        data: {
            state: light_state
        },
        success: function (data) {
            console.log('Zmieniono stan diody.');
        },
        error: function (xhr, status, error) {
            console.error('Wystąpił błąd podczas zmiany stanu diody:', error);
        }
    });
}

function watering() {
    $.ajax({
        url: '/watering',
        type: 'POST',
        success: function (data) {
            console.log('Podlano.');
            $('#water_time').text(data.hour);
            $('#water_date').text(data.dataa);
        },
        error: function (xhr, status, error) {
            console.error('Wystąpił błąd podczas podlewania:', error);
        }
    });
}

// Rozpocznij odświeżanie danych po załadowaniu strony
$(document).ready(function () {
    odswiezDane();
});
