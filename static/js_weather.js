const routes = [
    { path: '/weather_pg', handler: weatherHandler },


function weatherHandler() {
    const Form = document.querySelector('#wth-form');
    const res = document.getElementById('result');

    const urlWeather = '/weather';
    console.log('Я loginHandler');
    Form.addEventListener('submit', (event) => {
        event.preventDefault();
        RequestToServer(event.target, urlWeather)
        .then(response => {
            res.innerHTML = `<p>Тeмпература: ${response["Тeмпература"]}°</p> <p>Вологість: ${response["Вологість"]} %</p> <p> Швидкість вітру: ${response["Швидкість вітру:"]} км/год</p>`;
        });
    });
};

document.addEventListener("DOMContentLoaded", function() {
    handleRoutes();
});
