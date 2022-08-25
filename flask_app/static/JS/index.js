var formLogin = document.getElementById('formLogin');


// vamos a escuchar cuando se realiza el evento  ON SUBMIT

formLogin.onsubmit = function (event) {
    event.preventDefault(); // prevenimos el comportamiento de el formulario 

    // creamos  una variable con todos los datos del formulario 
    var  formulario = new FormData(formLogin);


    fetch("/login", {method:'POST', body:formulario})
    .then(response => response.json())
    .then(data => {
        console.log(data);

        if (data.message == "correcto") {
            window.location.href = "/dashboard";
        }

        var mensajeAlerta = document.getElementById('mensajeAlerta');
        mensajeAlerta.innerText = data.message;
        mensajeAlerta.classList.add('alert')
        mensajeAlerta.classList.add('alert-danger');

    });
}