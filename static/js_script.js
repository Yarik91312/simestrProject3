const routes = [
    { path: '/weather_pg', handler: weatherHandler },

function RequestToServer(form, url) {
    const formData = new FormData(form);
    console.log('Я RequestToServer');
    formData.append('key1', 'value1');

    return new Promise((resolve, reject) => {
        fetch(url, {
            method: "POST",
            body: formData,

        })
        .then(response => response.json())
        .then(data => {
            resolve(data);
        });
    });
}
function handleRoutes() {
    const currentPath = window.location.pathname;
    console.log('Я  handleRoutes');
    const routeData = routes.find(route => route.path === currentPath);
    routeData.handler();
};

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
