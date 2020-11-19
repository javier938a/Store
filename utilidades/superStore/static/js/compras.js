


$(document).ready(function(){

    var url='ws://'+window.location.host+'/ws/prod_client/';
    var socket = new WebSocket(url);

    socket.onopen=function(e){
        console.log("Te has conectado al socket");
    }

    socket.onmessage=function(e){
        var datos = JSON.parse(e.data);
        let filas='';

        for(let i in datos){
            id=datos[i].pk;
            producto=datos[i].fields.producto;
            cantidad=datos[i].fields.cantidad;
            proveedor=datos[i].fields.proveedor;
            var fila = '<tr id="fila_'+id+'" class="selected">\
                            <th scope="row">'+id+'</th>\
                            <td>'+producto+'</td>\
                            <td>'+cantidad+'</td>\
                            <td>'+proveedor+'</td>\
                        </tr>';
            filas +=fila;
        }
        $("#productos").empty();
        $("#productos").append(filas);


    }

    socket.onclose=function(e){
        console.log("Te has conectado del socket");
    }
    //fin del socke
    

    $('#exampleModal').on('show.bs.modal', function (event) {
        var modal = $(this)
            socket.send(JSON.stringify({//Obteniendo los datos totales
                'tipo_busqueda':'producto',
                'clave_nombre':''
            }));
      });

      $("#txt_clave_prod").keyup(function(e){
            console.log($("#txt_clave_prod").val());
            claveProd=$("#txt_clave_prod").val();
            socket.send(JSON.stringify({
                'tipo_busqueda':'producto',
                'clave_nombre':claveProd
            }));

      });

      $(document).on('click', ".selected", function(){
          var idfila=$(this).attr('id');
          console.log(idfila);
          console.log($("#"+idfila+"").hasClass('fila_seleccionada'))
          if($("#"+idfila+"").hasClass('fila_seleccionada')){
              $("#"+idfila+"").removeClass('fila_seleccionada');
          }else{
              $("#"+idfila+"").addClass('fila_seleccionada');
          }

      })





      
});