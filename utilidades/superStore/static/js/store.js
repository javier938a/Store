
///importScripts('/static/js/csrf_scrip.js');
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
    $('.vDateField').datepicker({dateFormat: 'yy-mm-dd'});
    $.datepicker.setDefaults({
        showOn: "both",
        buttonImageOnly: true,
        buttonImage: "calendar.gif",
        buttonText: "Calendar"
      });
    $.datepicker.setDefaults( $.datepicker.regional['es'] );
    
    $("#categorias a.nav-link").hover(function(){
        active = $(this).hasClass("active");
        if(active==false){
            $(this).addClass("active");
        }else{
            $(this).removeClass("active");
        }
    });
   

    //listando los departamentos cuando el usuario seleccione un pais
    $("#paises").change(function(){
        $("#departamento").html('');
        $("#municipio").html('');
        const csrftoken = getCookie('csrftoken');
        id_pais = $(this).val();
        //alert(id_pais);
        url = '/superStore/depto/'+id_pais+''
        list_depto = '';
        $.ajax({
            type:'GET',
            url:url,
            data:{
                csrfmiddlewaretoken: csrftoken,
            },
            dataType:'json',
            success:function(data){
                departamentos = JSON.parse(data);//recividos los departamentos ahora es hora de listarlos
                console.log(departamentos);
                for(let depto in departamentos){
                    id = departamentos[depto].pk;
                    dep = departamentos[depto].fields.departamento;
                    iten = '<option value="'+id+'">'+dep+'</option>'
                    list_depto = list_depto+iten;
                }
                $("#departamento").append(list_depto);
            }
        });

    });
    $("#departamento").change(function(){
        $("#municipio").html('');
        const csrftoken = getCookie('csrftoken');
        id_depto = $(this).val();//obteniendo el id del departamento seleccionado
        url = '/superStore/depto/muni/'+id_depto+''
        //alert(url);
        mnp=''
        $.ajax({
            type:'GET',
            url:url,
            data:{
                csrfmiddlewaretoken: csrftoken,
            },
            dataType:'json',
            success:function(data){
                municipios = JSON.parse(data);
                console.log(municipios);
                for(let muni in municipios){
                    id = municipios[muni].pk;
                    munic = municipios[muni].fields.municipio;
                    item = '<option value="'+id+'">'+munic+'</option>';
                    mnp = mnp+item;
                }
                $("#municipio").append(mnp);
            }
        });
    });

    $("#municipio").change(function(){
        $("#barrioBcanton").html('');
        const csrftoken = getCookie('csrftoken');
        id_bc=$(this).val();
        url = 'depto/muni/barcant/'+id_bc+'';
        bacan='';
        $.ajax({
            type:'GET',
            url:url,
            data:{
                csrfmiddlewaretoken: csrftoken,                
            },
            dataType:'json',
            success:function(data){
                barrioBC = JSON.parse(data);
                console.log(barrioBC);
                for(let bc in barrioBC){
                    id = barrioBC[bc].pk;
                    b_c = barrioBC[bc].fields.barrio_canton;
                    iten = '<option value='+id+'>'+b_c+'</option>'
                    bacan = bacan + iten;
                }
                $("#barrioBcanton").append(bacan);
            }
        });
    });
   /* //reciviendo los socket
    var url = 'ws://'+window.location.host+'/ws/notificacion/'+$("#idprov").val()+'/';
    //alert(url);
    var socket = new WebSocket(url);
        socket.onopen = function(e){
            //alert("Conexion establecida!");
        }

        socket.onmessage = function(e){
            sms = JSON.parse(e.data);
            alert(sms.messaje);
        }
        socket.onclose = function(e){
            //alert("Se ha desconectado")
        }*/

        

});