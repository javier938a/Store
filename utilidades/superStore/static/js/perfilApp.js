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
    $("#id_barrio_canton").html('');//limpiando el barrio y canton que se listan al cargar
    $("#foto").change(function(e){
        var ruta = e.target.files[0];
        imageType = /image.*/;
        if(!ruta.type.match(imageType))
         return;
        
        var reader = new FileReader();
        reader.onload = function(e){
            var resultado = e.target.result;
            $("#fotoPerfil").attr("src",resultado);
        };
        reader.readAsDataURL(ruta);

    });
    $(document).on('change',"#id_pais",function(){
       $("#id_depto").html('');//Limpiando el selec antes para llenarlo con los nuevos departamentos
       $("#id_muni").html('');
       $("#id_barrio_canton").html('');
       //alert($(this).val());
       let idPais=$(this).val();
       const csrftoken = getCookie('csrftoken');
       let datos ={
        csrfmiddlewaretoken: csrftoken,
       }
       $.ajax({
           type:'GET',
           url:'/superStore/deptoAs/'+idPais,
           data:datos,
           typeData:'json',
           success:function(data){
               depart = JSON.parse(data);
               for(let i in depart){
                   id = depart[i].pk;
                   depto = depart[i].fields.departamento;
                   $('#id_depto').append('<option value="'+id+'">'+depto+'</option>');                   
               }
           }

       });
    });
    $(document).on('change',"#id_depto",function(){
        $("#id_muni").html('');
        $("#id_barrio_canton").html('');
        const csrftoken = getCookie('csrftoken');
        idDepto=$(this).val();
        url = '/superStore/deptoAs/muniAs/'+idDepto;
        datos={
            csrfmiddlewaretoken: csrftoken,
        };
        $.ajax({
            url,
            type:'GET',
            data:datos,
            typeData:'json',
            success:function(data){
                console.log(data);
                munic=JSON.parse(data);
                for(let i in munic){
                    id = munic[i].pk;
                    muni = munic[i].fields.municipio;
                    $("#id_muni").append('<option value="'+id+'">'+muni+'</option>');
                }
            }
        });
    });
    $(document).on('change','#id_muni',function(){
        $("#id_barrio_canton").html('');
        let idMuni=$(this).val();
        const csrftoken = getCookie('csrftoken');
        let url='/superStore/deptoAs/muniAs/b_c/'+idMuni;
        datos = {
            csrfmiddlewaretoken: csrftoken,
        }
        $.ajax({
            url:url,
            data:datos,
            typeData:'json',
            success:function(data){
                bacan = JSON.parse(data);
                for(let i in bacan){
                    id = bacan[i].pk;
                    b_c = bacan[i].fields.barrio_canton;
                    $("#id_barrio_canton").append('<option value="'+id+'">'+b_c+'</option>');
                }
            }
        });

    });
});