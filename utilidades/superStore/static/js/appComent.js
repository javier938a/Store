$(document).ready(function(){
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
    $("#escribir").submit(function(evt){
        evt.preventDefault();
        var dire = $("#escribir").attr('action');
        var venta = $("#venta").val();
        var puntaje = $("input:radio[name=puntaje]:checked").val();
        var coment = $("#cmt").val();
        const csrftoken = getCookie('csrftoken');
        datos ={
            csrfmiddlewaretoken:csrftoken,
            'venta_id':venta,
            'puntaje':puntaje,
            'coment':coment,
        };
        $.ajax({
            type:'POST',
            url:dire,
            data:datos,
            success:function(data){
                    comentario = "Valoracion "+data.puntaje+"<br>Cliente "+data.cliente+" <p> "+data.coment+"</p>";
            }
        });
        

    });
});