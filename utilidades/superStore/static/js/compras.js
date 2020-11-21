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
                            <td scope="row">'+id+'</td>\
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
    

    var modal_prod=$('#exampleModal').on('show.bs.modal', function (event) {
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
      
      var datos_filas=[]

      $(document).on('click', ".selected", function(){
          var idfila=$(this).attr('id');
          console.log(idfila);
          console.log($("#"+idfila+"").hasClass('fila_seleccionada'))
          if($("#"+idfila+"").hasClass('fila_seleccionada')){
              $("#"+idfila+"").removeClass('fila_seleccionada');
              datos_filas.splice(0, datos_filas.length);
          }else{
              if(datos_filas.length>0){
                  datos_filas.splice(0, datos_filas.length);
              }
              $("#"+idfila+"").addClass('fila_seleccionada');
              $("#"+idfila+"").find('td').each(function(index){
                datos_filas.push($(this).html())
              });
              console.log(datos_filas);
          }
          

      })

      $("#btn_agregar_prod").click(function(evt){
          console.log(datos_filas.length);
          if(datos_filas.length==4){
            let fila_compra='<tr id="fila_'+datos_filas[0]+'">\
                                <td>'+datos_filas[0]+'</td>\
                                <td>'+datos_filas[1]+'</td>\
                                <td>'+datos_filas[2]+'</td>\
                                <td>'+datos_filas[3]+'</td>\
                                <td><input id="input_'+datos_filas[0]+'" class="cantidad_producto" style="width:15vh;" type="text" value="0" placeholder="cantidad" /></td>\
                                <td>$<input id="input2_'+datos_filas[0]+'" pattern="^[0-9]+(.[0-9]+)?$"  class="precio_producto" style="width:15vh;" type="text" value="0.0" placeholder="precio" /></td>\
                                <td id="total_'+datos_filas[0]+'">$0.0</td>\
                                <td><button class="btn btn-primary eliminar_fila">Eliminar</button></td>\
                            </tr>';
            $("#lista_compras").append(fila_compra);
            modal_prod.modal('toggle');
          }else{
              alert("No ha seleccionado ningun producto para agregar");
          }

        
      });
      //validando que solo pueda ingresar numeros del 0 a 9

      $(document).on('input', '.cantidad_producto', function(){
            this.value=this.value.replace(/[^0-9]/g, '').replace(/,/g, '.');
      });
      
      $(document).on('keyup', '.cantidad_producto', function(evt){
            var idinput=$(this).attr("id")
            var idinput2=$(this).attr("id").replace('input_','input2_');
            var idtotal=idinput.replace('input_', '#total_');
  
            var precio=$('#'+idinput2+'').val();
            var cantidad=$('#'+idinput+'').val();
            
            var total = precio!=''&& cantidad!=''?parseFloat(precio)*parseFloat(cantidad):0.0;
            var totalrounded=Math.round(total*1000)/1000;
            console.log(total);
  
            $(idtotal).html('$'+totalrounded.toString());
            var suma_total=0.0;
            //haciendo una suma total de los totales
            $("#lista_compras").find('tr').each(function(index){
                  var totalStr=$(this).find('td').eq(6).html(); 
                  totalFl = parseFloat(totalStr.replace('$',''));
                  suma_total+=totalFl;
            });

            var sumatotalRedodeo=Math.round(suma_total*1000)/1000;

            $("#suma_total").html('$'+sumatotalRedodeo.toString());
                 
      });

      $("#btn_eliminar_compras").click(function(evt){
        $("#lista_compras").empty();
        $("#suma_total").html("$0");
      });
      //validado que el campo acepte solo numeros y punto decimal
      $(document).on('input', '.precio_producto', function(){
            this.value=this.value.replace(/[^0-9,.]/g, '').replace(/,/g, '.');
      });

      $(document).on('keyup', '.precio_producto', function(evt){
          console.log("codigos: "+evt.keyCode);
            var idinput2=$(this).attr("id");
            var idinput=idinput2.replace('input2_', 'input_');
            var idtotal=idinput.replace('input_', 'total_');
            
            var cantidad=$('#'+idinput+'').val();
            var precio=$('#'+idinput2+'').val();
            
            var total=cantidad!='' && precio!=''? parseFloat(precio)*parseFloat(cantidad):0.0;
            var totalrounded=Math.round(total*1000)/1000;//redondeando el total a 3 decimales
            
            console.log(total);
            $("#"+idtotal+"").html('$'+totalrounded);
    
            var suma_total=0.0;
            $("#lista_compras").find('tr').each(function(index){
                var totalStr=$(this).find('td').eq(6).html();

                var totalFl= parseFloat(totalStr.replace('$',''));
   
                suma_total+=totalFl;
    
                
            });
            var sumatotalRedodeo=Math.round(suma_total*1000)/1000;

            $("#suma_total").html('$'+sumatotalRedodeo.toString());//redondeando el valor a 3 decimales.
            
      });

      $(document).on('click','.eliminar_fila', function(evt){
        var totalFila=parseFloat($(this).parent().parent().find('td').eq(6).html().replace('$',''));
        var sumaTotal= parseFloat($("#suma_total").html().replace('$',''));
        var nuevoTotal=sumaTotal-totalFila;
        var nuevoTotalRedondeado=Math.round(nuevoTotal*1000)/1000;
        $("#suma_total").html('$'+nuevoTotalRedondeado.toString());
        console.log($(this).closest('tr'));
        $(this).closest('tr').remove();



      });


      $("#btn_efectuar_compras").click(function(e){
        e.preventDefault();
        var lista_compras=new Array();
        $("#lista_compras").find('tr').each(function(index){
            
            var id=$(this).find('td').eq(0).html();
            var producto=$(this).find('td').eq(1).html();
            var cantidad=$(this).find('td').eq(4).find('input').val();
            var precio_compra=$(this).find('td').eq(5).find('input').val();
            var precio_total=$(this).find('td').eq(6).html().replace('$','');
            var fila={'id':id, 'producto':producto, 'cantidad':cantidad, 'precio_compra':precio_compra, 'precio_total':precio_total}
            lista_compras.push(fila);
            
        });
        var url='/superStore/guardar_compras';
        const csrftoken = getCookie('csrftoken');
        lista_compras_json=JSON.stringify(lista_compras);
        var datos={
            csrfmiddlewaretoken:csrftoken,
            'compras':lista_compras_json
        };

        $.ajax({
            type:'POST',
            url:url,
            data:datos,
            dataType:'json',
            success:function(data){
                if(data.res==true){
                    $("#lista_compras").empty();
                    alert("Compra efectuada exitosamente..");
                }
            }

        })
        console.log(lista_compras_json);
      });

});