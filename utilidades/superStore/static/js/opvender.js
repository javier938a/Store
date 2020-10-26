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
$(document).ready(function (){
    
    url='ws://'+window.location.host+'/ws/prod_client/';
    socket = new WebSocket(url);
    socket.onopen=function(e){
        console.log('Conectado..');
    }
    socket.onclose=function(e){
        console.log('Desconectado');
    }
    socket.onmessage=function(e){
        prod_clien=JSON.parse(e.data);
        filas_todas='<tr>'
        fila=''
        if(prod_clien[0]!=undefined){
            if(prod_clien[0].model=="superStore.tbl_producto"){
                for(let i in prod_clien){
                    id = prod_clien[i].pk;
                    producto = prod_clien[i].fields.producto;
                    cantidad = prod_clien[i].fields.cantidad;
                    precio_unitario = prod_clien[i].fields.precio_unitario;
                    precio_venta=prod_clien[i].fields.precio_venta;
                    fila += '<tr id="fila_'+id+'" class="selected">\
                                <td>'+id+'</td>\
                                <td>'+producto+'</td>\
                                <td>'+cantidad+'</td>\
                                <td>$'+precio_unitario+'</td>\
                                <td>$'+precio_venta+'</td>\
                            </tr>'
                }
                filas_todas+=fila+'</tr>'
                var tabla='\
                            <table id="tabla_producto" class="table">\
                                <thead class="thead-dark">\
                                    <tr>\
                                        <th scope="col">ID</th>\
                                        <th scope="col">Producto</th>\
                                        <th scope="col">Cantidad</th>\
                                        <th scope="col">Precio de compra</th>\
                                        <th scope="col">Precio de venta</th>\
                                    </tr>\
                                </thead>\
                                <tbody>\
                                    '+filas_todas+'\
                                </tbody>\
                            </table>\
                            ';
                $("#content_table").empty();
                $("#content_table").append(tabla);
            }else if(prod_clien[0].model=="superStore.tbl_cliente"){
                console.log(prod_clien);
                for(let i in prod_clien){
                    id=prod_clien[i].pk;
                    username=prod_clien[i].fields.user[0]
                    nombres=prod_clien[i].fields.user[1]
                    apellidos=prod_clien[i].fields.user[2]
                    fila += '<tr id="fila_'+id+'" class="selected">\
                                <td>'+id+'</td>\
                                <td>'+username+'</td>\
                                <td>'+nombres+' '+apellidos+'</td>\
                            </tr>'
                }
                filas_todas+=fila+'</tr>'
                var tabla='\
                            <table id="tabla_clientes" class="table">\
                                <thead class="thead-dark">\
                                    <tr>\
                                        <th scope="col">ID</th>\
                                        <th scope="col">Usuario</th>\
                                        <th scope="col">Nombres</th>\
                                    </tr>\
                                </thead>\
                                <tbody>\
                                    '+filas_todas+'\
                                </tbody>\
                            </table>\
                            ';
                $("#content_clientes").empty();
                $("#content_clientes").append(tabla);
                
            }
        }


    }

    clave=''
    mod=$('#list_prod').on('show.bs.modal', function(event){
        var button = $(event.relatedTarget);
        var recipient = button.data('whatever');
        var modal=$(this);
        url=$("#prodajax").attr('action');
        var csrftoken=getCookie('csrftoken');
        //alert(csrftoken);
        clave=$('#txt_clave_prod').val();
        socket.send(JSON.stringify({
            'tipo_busqueda':'producto',
            'clave_nombre':clave,
        }));
    });
    $('#list_client').on('show.bs.modal', function (event) {
        var button = $(event.relatedTarget) // Button that triggered the modal
        var recipient = button.data('whatever') // Extract info from data-* attributes
        // If necessary, you could initiate an AJAX request here (and then do the updating in a callback).
        // Update the modal's content. We'll use jQuery here, but you could use a data binding library or other methods instead.
        var modal = $(this)
        clave=$('#txt_clave_cliente').val();
        socket.send(JSON.stringify({
            'tipo_busqueda':'cliente',
            'clave_nombre':clave,
        }));
      })

    $('#txt_clave_prod').keydown(function(event){
        console.log(event.keyCode);
        if((event.keyCode>64 && event.keyCode<91) || (event.which>48 && event.which<58)){
            clave=$('#txt_clave_prod').val();
            console.log(clave);
            socket.send(JSON.stringify({
                'tipo_busqueda':'producto',
                'clave_nombre':clave,
            }));
        }else if(event.keyCode==13){
            clave=$('#txt_clave_prod').val();
            socket.send(JSON.stringify({
                'tipo_busqueda':'producto',
                'clave_nombre':clave,
            }));
        }else if(event.keyCode==8){
            clave=$('#txt_clave_prod').val();
            socket.send(JSON.stringify({
                'tipo_busqueda':'producto',
                'clave_nombre':clave,
            }));    
        }
    });

    $("#txt_clave_cliente").keydown(function(event){
        console.log(event.keyCode);
        if((event.keyCode>64 && event.keyCode<91) || (event.which>48 && event.which<58)){
            clave=$('#txt_clave_cliente').val();
            console.log(clave);
            socket.send(JSON.stringify({
                'tipo_busqueda':'cliente',
                'clave_nombre':clave,
            }));
        }else if(event.keyCode==13){
            clave=$('#txt_clave_cliente').val();
            socket.send(JSON.stringify({
                'tipo_busqueda':'cliente',
                'clave_nombre':clave,
            }));
        }else if(event.keyCode==8){
            clave=$('#txt_clave_cliente').val();
            socket.send(JSON.stringify({
                'tipo_busqueda':'cliente',
                'clave_nombre':clave,
            }));    
        }       
    });

    $("#prodajax").on('submit',function(e){
        e.preventDefault();
        clave=$('#txt_clave_prod').val();
        console.log(clave);
        socket.send(JSON.stringify({
            'tipo_busqueda':'producto',
            'clave_nombre':clave,
        }));
    });
    var fila_content = [];
    //resaltando filas
    $(document).on("click", ".selected", function(){
        idFila=$(this).attr('id');
        if($('#'+idFila+'').hasClass('fila_selecionada')){
            $('#'+idFila+'').removeClass('fila_selecionada');
        }else{
            $('#'+idFila+'').addClass('fila_selecionada');
            if(fila_content.length>0){
                    //alert(i);
                fila_content.splice(0, fila_content.length);
            }
            $(this).find("td").each(function(index){//Recorriendo la fila seleccionada
                //$(this).html()
                //console.log($(this).html());
                //alert($(this).html());
                fila_content.push($(this).html());
            });
        }
    });

    $("#agregar").on('click', function(evt){
        //alert($("#recipient-name").val());
        //alert("Holaaa")
        mod.modal('toggle');
        $("#txt_clave_prod").val('');
        cantidad=parseInt($("#txt_cantidad").val());
        total = parseFloat(fila_content[4].replace('$',''))*cantidad;
        
        fila_venta='<tr>\
                        <td>'+fila_content[1]+'</td>\
                        <td>'+cantidad+'</td>\
                        <td>'+fila_content[4]+'</td>\
                        <td>$'+total+'</td>\
                    </tr>'
        $("#table_body").append(fila_venta);

    })

    $("#clientajax").submit(function(evt){
        evt.preventDefault()
        socket.send(JSON.stringify({
            'tipo_busqueda':'cliente',
            'clave_nombre':$('#txt_clave_cliente').val(),
        }));
    });


});