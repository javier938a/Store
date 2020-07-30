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
    $(".aniadir_favorito").submit(function(){
        boton = $("button",this)
        //alert("Holqqq");
        const csrftoken=getCookie('csrftoken');
        datos = {
            csrfmiddlewaretoken:csrftoken,
            'cliente_id':$("#cliente_id").val(),
        };
        //alert(datos.cliente_id);
        $.ajax({
            url:$(this).attr("action"),
            type:'GET',
            data:datos,
            dataType:'json',
            success:function(data){
                if(data.res==true){
                    //alert(boton.hasClass('btn-success'));
                    if(boton.hasClass('btn-primary')==true){//verificando si el boton tiene btn-succes
                        boton.addClass('btn-success');
                        boton.removeClass('btn-primary');                           
                    }                    
                }else{
                    if(boton.hasClass('btn-success')){//verificando si el boton esta en primary color
                        boton.addClass('btn-primary');
                        boton.removeClass('btn-success');                        
                    }
                }
            },
        });
        return false;
    });
});