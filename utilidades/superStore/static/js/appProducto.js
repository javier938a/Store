//creando una funcion que envie una peticion http que retorne todos los comentarios del producto
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
function listar_comentarios(){
    $("#cargar").ready(function(){
        const csrftoken = getCookie('csrftoken');
        var datos = {//
            csrfmiddlewaretoken:csrftoken,
            'producto_id':$("#producto_id").val(),//obteniendo el valor del id del comentario
        }
        dir = $("#cargar").attr("action");//obteniendo la direccion url
        $.ajax({
            url:dir,
            type:$("#cargar").attr('method'),
            data:datos,
            dataType:'json',
            success:function(data){
                var datos = JSON.parse(data);
                alert(datos[0].fields);
            }
        });
    });
    
}
$(document).ready(function(){
    listar_comentarios()

    $(".foto").hover(function(){
        var ubi = $(this).attr("src");
        //alert(ubi);
        $("#foto_producto").attr("src",ubi);
    })
});
