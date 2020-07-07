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
    $(".foto").hover(function(){
        var ubi = $(this).attr("src");
        //alert(ubi);
        $("#foto_producto").attr("src",ubi);
    })
    //formulario de comentario
    $("#comentar").submit(function(evt){//Enviando el formulario
        const csrftoken = getCookie('csrftoken');
        //alert($("#cmt").val());
        evt.preventDefault();
        datos={
            csrfmiddlewaretoken:csrftoken,
            'producto_id':$("#prod_id").val(),
            'coment':$("#cmt").val(),
            'puntaje':$("input:radio[name=puntaje]:checked").val()
        };
        $.ajax({
            type:'POST',
            url:$("#comentar").attr("action"),
            data:datos,
            dataType:"json",
            success:function(data){
                if(data.res==true){
                    location.reload();//recarga la pagina para mostrar los comentarios
                    $("#cmt").val('');//limpia el contenido del textview
                }else{
                    alert("Hubo un error favor recarge o contacte con el desarrollador!!")
                }
            }
        });     
    });
    //Elimina el comentario
    $(".del_coment").click(function(evt){
        evt.preventDefault();
        var conf = confirm("¿Esta seguro que desea eliminar el comentario?");
        if(conf==true){
            url = $(this).attr('href');//obtiene el valor de href que es el url de cada comentario
            btn = $(this).attr('id');//obtiene el valor del id del boton eliminar que "c + cid" que es el id de cada comentario
            id_p = btn.substring(1,btn.length);//con substring eliminamos un "c" ya que en los p esta como "cid"
            $.ajax({
                url:url,
                type:'GET',
                dataType:'json',
                success:function(data){
                    if(data.res==true){//si se elimina el elemento 
                        $("#"+id_p).remove();//eliminamos el parrafo o el comentario de la lista en la pagina
   
                    }
                    
                }
            });
        }

    });
});
