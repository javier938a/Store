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

$(document).ready(function(){

    $("#btn_intervalo").click(function(evt){
        evt.preventDefault();
        $("#fecha_intervalo").css('display', 'block');
        $("#fecha_mes").css('display','none')

    })
    $("#btn_mes").click(function(evt){
        evt.preventDefault();
        $("#fecha_intervalo").css('display', 'none');
        $("#fecha_mes").css('display', 'block');
    });

    /*$("#form-fechas").submit(function(){
        var fecha_inicio=$("#id_fecha_inicio").val();
        var fecha_fin=$("#id_fecha_fin").val();
        var url=$(this).attr('action');
        const csrftoken=getCookie('csrftoken');
        alert(url);

        $.ajax({
            url:url,
            type:'POST',
            data:{
                csrfmiddlewaretoken: csrftoken,
                'fecha_inicio':fecha_inicio,
                'fecha_fin':fecha_fin
            },
            dataType:'json',
            success:function(data){
                console.log(data)
            }

        });
        return false
    })*/
});