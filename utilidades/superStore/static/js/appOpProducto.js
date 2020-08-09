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
    //alert("Hola mundo");
    //cargando todas las categorias
    $("#id_sub_categoria1").html('');//borrando para que no se pongan al final de las que ya esten
    const csrftoken = getCookie('csrftoken');
    $.ajax({
        type:'POST',
        url:'/superStore/list_cate/',
        data:{
            csrfmiddlewaretoken:csrftoken,
        },
        success:function(data){
            categorias = JSON.parse(data);
            console.log(categorias);
            for(let cate in categorias){
                //console.log(cate);
                var cc = '<option value="'+categorias[cate].pk+'">'+categorias[cate].fields.categoria+'</option>';
                console.log(cc);
                $("#id_categoria1").append(cc);
            }
        }
    });
    //Fin de la carga de categorias de nivel 1
    $("#id_categoria1").change(function(){
        $("#id_sub_categoria1").html('');
        //alert("select val "+$(this).val());
        //alert($("#id_categoria2").val());
        var idcategoria = $(this).val();
        const csrftoken = getCookie('csrftoken');
        var url='/superStore/list_cate/lis_sub_cate1/'+idcategoria;
        console.log(url);
        date = { 
            csrfmiddlewaretoken:csrftoken,
         };
        $.ajax({
            type:'GET',
            url:url,
            //data:date,
            success:function(data){
                console.log(data);
                subcate1 = JSON.parse(data)
                for(let i in subcate1){
                    pk = subcate1[i].pk;
                    subcate = subcate1[i].fields.sub_categoria;
                    var cc = '<option value="'+pk+'">'+subcate+'</option>';
                    console.log(cc);
                    $("#id_sub_categoria1").append(cc);
                }
            }
        });
    });

});