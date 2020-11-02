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
    //aplicando mascaras a los campos
    $('input[name="codigo_factura"]').mask("0000");
    $('input[name="nit"]').mask("0000-000000-000-0");

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
    titulo_modal=''
    mod=$('#list_prod').on('show.bs.modal', function(event){
        var button = $(event.relatedTarget);
        var recipient = button.data('whatever');
        var modal=$(this);
        modal.find('.modal-title').text('Productos')
        url=$("#prodajax").attr('action');
        var csrftoken=getCookie('csrftoken');
        //alert(csrftoken);
        
        clave=$('#txt_clave_prod').val();
        socket.send(JSON.stringify({
            'tipo_busqueda':'producto',
            'clave_nombre':clave,
        }));
        titulo_modal= modal.find('.modal-title').text();//Se utilizara para saber si estoy agregando un producto o cliente

    });
    


    mod_cliente=$('#list_client').on('show.bs.modal', function (event) {
        var button = $(event.relatedTarget) // Button that triggered the modal
        var recipient = button.data('whatever') // Extract info from data-* attributes
        // If necessary, you could initiate an AJAX request here (and then do the updating in a callback).
        // Update the modal's content. We'll use jQuery here, but you could use a data binding library or other methods instead.
        var modal = $(this)
        modal.find('.modal-title').text('Clientes')
        clave=$('#txt_clave_cliente').val();
        socket.send(JSON.stringify({
            'tipo_busqueda':'cliente',
            'clave_nombre':clave,
        }));
        titulo_modal=modal.find('.modal-title').text();
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
    var fila_clientes=[]
    //resaltando filas
    $(document).on("click", ".selected", function(){
        idFila=$(this).attr('id');
        if($('#'+idFila+'').hasClass('fila_selecionada')){
            $('#'+idFila+'').removeClass('fila_selecionada');
        }else{
            $('#'+idFila+'').addClass('fila_selecionada');
            if(titulo_modal=='Productos'){
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
            }else if(titulo_modal=='Clientes'){
                if(fila_clientes.length>0){
                    fila_clientes.splice(0, fila_clientes.length);
                }
                $(this).find("td").each(function(index){
                    fila_clientes.push($(this).html());
                });
            }

        }
    });

    $("#btn_select_cliente").on('click', function(evt){
        mod_cliente.modal('toggle');
        $("#txt_clave_cliente").val('');
        idCliente = fila_clientes[0]; 
        usuario=fila_clientes[1];
        nombres=fila_clientes[2];
        //alert(idCliente);
        //alert(nombres);
        $("#id_cliente").val(idCliente);
        $("#txt_cliente").val(nombres);
    });

    $("#txt_cantidad").keypress(function(event){
        if(event.which>=48 && event.which<58){

        }else{
            event.preventDefault();
        }
    });

    $("#agregar").on('click', function(evt){
        //alert($("#recipient-name").val());
        //alert("Holaaa")
        cantidad=parseInt($("#txt_cantidad").val());
        var prod_venta=new Array();
        $("#table_body").find('tr').each(function(index){//validando que no se repita un producto al agregarlo con el escanner
            fila=[]
            $(this).find('td').each(function(index){
                fila.push($(this).html());
            });
            prod_venta.push(fila)
        });
        console.log(prod_venta);
        existe=false
        prod_venta.forEach(function(element){
            if(element[0]==fila_content[0]){
                existe=true;
            }
        });
        if(existe==false){
            if(fila_content.length>0){             
                mod.modal('toggle');
                $("#txt_clave_prod").val('');
                //alert(fila_content[2]);
                if(fila_content[2]>0){
                    fila_venta='<tr class="selected">\
                                    <td>'+fila_content[0]+'</td>\
                                    <td>'+fila_content[1]+'</td>\
                                    <td id="stock_'+fila_content[0]+'">'+fila_content[2]+'</td>\
                                    <td><input id="prod_'+fila_content[0]+'" style="width:15vh;" class="cantidad_producto" type="text" value="'+1+'" ></td>\
                                    <td id="precio_'+fila_content[0]+'">'+fila_content[4]+'</td>\
                                    <td id="total_'+fila_content[0]+'">'+fila_content[4]+'</td>\
                                    <td><button class="borrar_venta btn btn-primary">Eliminar</button></td>\
                                </tr>'
                    $("#table_body").append(fila_venta);                   
                }else{
                    alert("Ya no hay "+fila_content[1]+' en existencia en el inventario');
                }
            }else{
                alert("Debe de seleccionar un producto en la lista..")
            }
        }else{
            alert("Ya existe existe este producto en la lista,\npor favor si desea agregar otro, solo modificar la cantidad");
        }
    });
    //Eliminando una venta de la tabla
    $(document).on("click",".borrar_venta", function(evt){
        evt.preventDefault();
        $(this).closest('tr').remove();
    });
    //esta funcion escucha el eventon de modificar la cantidad de producto, al teclear los numeros se actualiza el total de compra
    $(document).on('keyup',".cantidad_producto", function(evt){
        console.log(evt.keyCode);
        if((evt.keyCode>=48 && evt.keyCode<58) || (evt.keyCode>=96 && evt.keyCode<=105)){
            //alert(evt.keyCode);
            //alert($(this).attr("id"));
                idStock=$(this).attr("id").replace('prod_','#stock_')//obteniendo el id del producto y modificandolo para obtener el id del stock
                stock=$(idStock).html();
                cantidad=$("#"+$(this).attr("id")+"").val();//utilizando el id para obtener el valor del imput
                //alert('cantidad: '+cantidad+' stock: '+stock)
                if(parseInt(cantidad)<=parseInt(stock)){
                    idprecio = $(this).attr("id").replace('prod_','#precio_');
                    precio=$(idprecio).html();
                    total = parseFloat(cantidad)*parseFloat(precio.replace('$',''));
                    ///alert('cantidad: '+cantidad+' precio:'+precio+' total: '+total);
                    console.log('cantidad: '+cantidad+' precio:'+precio+' total: '+total);
                    idtotal=$(this).attr("id").replace("prod_",'#total_');
        
                    //limpiando el total actual para poner el nuevo total
                    $(idtotal).html('');
                    $(idtotal).html('$'+total); 
                }else{
                    $("#"+$(this).attr("id")+"").val('');
                    alert("La cantida ingresada supera el Stock del inventario favor ingresar una cantidad menor o igual al stock");
                }              

        }else if(evt.keyCode==8){
            //alert(evt.keyCode);
            //alert($(this).attr("id"));
            cantidad=$("#"+$(this).attr("id")+"").val();//utilizando el id para obtener el valor del imput
            if(cantidad==''){
                cantidad='0';
            }
            idprecio = $(this).attr("id").replace('prod_','#precio_');
            precio=$(idprecio).html();
            total = parseFloat(cantidad)*parseFloat(precio.replace('$',''));
            ///alert('cantidad: '+cantidad+' precio:'+precio+' total: '+total);
            console.log('cantidad: '+cantidad+' precio:'+precio+' total: '+total);
            idtotal=$(this).attr("id").replace("prod_",'#total_');

            //limpiando el total actual para poner el nuevo total
            $(idtotal).html('');
            $(idtotal).html('$'+total);

        }else if(evt.keyCode==130){
            return false;
        }
    });


    

    $("#clientajax").submit(function(evt){
        evt.preventDefault()
        socket.send(JSON.stringify({
            'tipo_busqueda':'cliente',
            'clave_nombre':$('#txt_clave_cliente').val(),
        }));
    });
    //al presionar el boton de nueva venta se es necesario crear una factura en blanco para obtener el id de la factura
    var id_factura=0
    $("#nueva_venta").on('click', function(evt){
        $("#code_barra").prop('disabled', false);//habilitando el campo del codigo de barra.
        $("#code_barra").focus();//colocando el foco o cursor automaticamente en el imput de codigo de barra
        $("#nueva_venta").prop('disabled',true);
        $("#btn_listprod").prop('disabled',false);
        $("#btn_listclient").prop('disabled', false);
        $("#btn_efectuar_venta").prop('disabled', false);
        $("#btn_cancelar").prop('disabled', false);
        $("#btn_limpiar_tabla_ventas").prop('disabled', false);
        //activando campos
        $("#txt_cliente").prop('disabled', false);
        $("#txt_direccion").prop('disabled',false);
        $("#txt_nit").prop('disabled',false)
        $("#txt_numero_fact").prop('disabled',false);

        var csrftoken=getCookie('csrftoken');
        url='/superStore/newfact';
        data={
            csrfmiddlewaretoken:csrftoken
        }
        $.ajax({
            type:'POST',
            url:url,
            data:data,
            dataType:'json',
            success:function(data){
                //fact=JSON.parse(data);
                id_factura=data[0].idfactura;
                $("#id_factura").val(id_factura);
                console.log(data[0].idfactura);
            }           
            
        });
    });


    $("#formRegVenta").submit(function(evt){
        evt.preventDefault();
        var ventas_prod=new Array()
        //Aqui se enviara todos los datos de la venta para poder imprimir factura..
        cliente_factura=$("#txt_cliente").val();
        codigo_factura=$("#txt_numero_fact").val();
        direccion_factura=$("#txt_direccion").val();
        nit_factura=$("#txt_nit").val();
        campo_vacio=false;//verificara si se ha ingresado un campo del total vacio.
        $("#table_ventas #table_body").find('tr').each(function(index){
            id_cliente=$('#id_cliente').val();
            id_prod=$(this).find('td').eq(0).html();
            producto=$(this).find('td').eq(1).html();
            stock=$(this).find('td').eq(2).html();
            cantidad=$(this).find('td').eq(3).find("input").val();//obteniendo el valor del input
            if(cantidad.length==0){//si se ingreso un espacio vacio entonces existe un campo vacio
                campo_vacio=true;
            }
            precio=$(this).find('td').eq(4).html();
            total=$(this).find('td').eq(5).html();
            id_factura=$('#id_factura').val();
            fila_prod = {'idCliente':id_cliente,'idProducto':id_prod,'producto':producto, 'cantidad':cantidad,'stock':stock, 'precio':precio, 'total':total, 'idFactura':id_factura};
            ventas_prod.push(fila_prod);
        })
        if(campo_vacio==false){
            if(ventas_prod.length>0){//verificando que hay al menos un producto agregado a la tabla de ventas para efectuar la venta
                ventas_json=JSON.stringify(ventas_prod);
                var csrftoken=getCookie('csrftoken');
                datos = {
                    csrfmiddlewaretoken:csrftoken,
                    'venta':ventas_json,
                    'idfactura':id_factura,
                    'codigo_factura':codigo_factura,
                    'cliente_factura':cliente_factura,
                    'direccion_factura':direccion_factura,
                    'nit_factura':nit_factura,
                };
                url='/superStore/efectuar_venta';
                $.ajax({
                    type:'POST',
                    url:url,
                    data:datos,
                    success:function(data){
                        console.log(data);
                        if(data.resultado==true){
                            //limpiando campos de la anterior venta
                            $("#txt_numero_fact").val('');
                            $("#txt_cliente").val('');
                            $("#txt_direccion").val('');
                            $("#txt_nit").val('');
                            $("#id_factura").val('');
                            $("#id_cliente").val('');
                            $("#table_body").empty();
                            //desactivando los botones y dejando activo solo el boton de nueva venta
                            $("#nueva_venta").prop('disabled',false);//activando los botones 
                            $("#btn_listprod").prop('disabled',true);
                            $("#btn_listclient").prop('disabled', true);
                            $("#btn_efectuar_venta").prop('disabled', true);
                            $("#btn_cancelar").prop('disabled', true);
                            $("#btn_limpiar_tabla_ventas").prop('disabled', true)
            
                            //desactivando campos
                            $("#txt_cliente").prop('disabled', true);
                            $("#txt_direccion").prop('disabled',true);
                            $("#txt_nit").prop('disabled',true)
                            $("#txt_numero_fact").prop('disabled',true);
                            $("#code_barra").prop('disabled',true);
                            alert("Venta efectuada exisotamente..");
                        }
                    }
        
                });
            }else{
                alert("Debe al menos agregar una producto para efectuar una venta..");
            }
        }else{
            alert("Ha dejando un campo de cantidad vacio en alguna de las ventas\n favor ingresar la cantidad a llevar para calcular el total...")
        }
    });

    var close_venta=$('#cancelar_venta').on('show.bs.modal', function(event){
        var button = $(event.relatedTarget);
        var modal=$(this);
    });
    var delete_ventas_agregadas = $("#deleteVentasTodas").on('show.bs.modal', function(event){
        var button=$(event.relatedTarget);
        var modal=$(this);
    });

    $("#btn_eliminar_todas_ventas").on('click', function(evt){
        delete_ventas_agregadas.modal('toggle');
        $("#table_body").empty();
        
    });




    $("#btn_cancelar_venta").on('click', function(evt){
        $("#table_body").empty();//limpiando la tabla
        $("#id_cliente").val('');//borrando los id del los hidden y los demas campos de textos
        $("#txt_cliente").val('')
        $("#txt_direccion").val('');
        $("#txt_nit").val('')
        $("#txt_numero_fact").val('');
        $("#code_barra").val('');
        idfactura=$("#id_factura").val();
        url='/superStore/eliminar_factura';
        var csrftoken=getCookie('csrftoken');
        $.ajax({
            type:'POST',
            url:url,
            data:{
                csrfmiddlewaretoken:csrftoken,
                'idfactura':idfactura
            },
            dataType:'json',
            success:function(data){
               
                if(data.res==true){
                    //alert("Cancelado correctamente.")
                    close_venta.modal('toggle');
                }
                $("#id_factura").val('')//limpiando el hidden contenedor de la factura
                $("#nueva_venta").prop('disabled',false);//activando los botones 
                $("#btn_listprod").prop('disabled',true);
                $("#btn_listclient").prop('disabled', true);
                $("#btn_efectuar_venta").prop('disabled', true);
                $("#btn_cancelar").prop('disabled', true);
                $("#btn_limpiar_tabla_ventas").prop('disabled', true);

                //desactivando campos
                $("#txt_cliente").prop('disabled', true);
                $("#txt_direccion").prop('disabled',true);
                $("#txt_nit").prop('disabled',true)
                $("#txt_numero_fact").prop('disabled',true); 
                $("#code_barra").prop('disabled',true);
            }
        })

    })
    $("#frm_buscar_code_barra").submit(function(evt){
        evt.preventDefault();
        codigo_barra=$("#code_barra").val();
        url='/superStore/buscar_codigo_barra';
        var csrftoken=getCookie('csrftoken');
        data={
            'codigo_barra':codigo_barra, 
            csrfmiddlewaretoken:csrftoken,
        };
        $.ajax({
            type:'POST',
            url:url,
            data:data,
            dataType:'json',
            success:function(data){
                producto_json=JSON.parse(data);
                if(producto_json.length==1){
                    for(let i in producto_json){
                        idproducto=producto_json[i].pk;
                        producto=producto_json[i].fields.producto;
                        stock=producto_json[i].fields.cantidad;
                        cantidad=1;
                        precio_venta=producto_json[i].fields.precio_venta;
                        precio_total=parseFloat(cantidad)*parseFloat(precio_venta);
                        if(parseInt(stock)>0){//se verifica si hay al menos 1 producto en existencia
                           
                            var prod_venta=new Array();
                            $("#table_body").find('tr').each(function(index){//validando que no se repita un producto al agregarlo con el escanner
                                fila=[]
                                $(this).find('td').each(function(index){
                                    fila.push($(this).html());
                                });
                                prod_venta.push(fila)
                            });
                            console.log(prod_venta);
                            existe=false
                            prod_venta.forEach(function(element){
                                if(element[0]==idproducto){
                                    existe=true;
                                }
                            });
                            if(existe==false){
                               
                                fila_venta='<tr class="selected">\
                                                <td>'+idproducto+'</td>\
                                                <td>'+producto+'</td>\
                                                <td id="stock_'+idproducto+'">'+stock+'</td>\
                                                <td><input id="prod_'+idproducto+'" style="width:15vh;" class="cantidad_producto" type="text" value="'+1+'" ></td>\
                                                <td id="precio_'+idproducto+'">'+precio_venta+'</td>\
                                                <td id="total_'+idproducto+'">'+precio_total+'</td>\
                                                <td><button class="borrar_venta btn btn-primary">Eliminar</button></td>\
                                            </tr>'
                                $("#table_body").append(fila_venta); 
                                $("#code_barra").val('');
                                $("#code_barra").focus();
                            }else{
                                alert("El producto que intenta ingresar por el escanner ya esta ingresado\n favor modificar solo la cantidad a vender.. ");
                                $("#code_barra").val('');
                                $("#code_barra").focus();
                            }


                        }else{
                            alert("No hay "+producto+" en existencia en el inventario o no esta registrado el codigo de barra ingresado en ningun producto.");
                        } 
                    }
                }else{
                    alert("El codigo de barra que se ingresó no esta registrado en ningun producto del inventario!");
                    $("#code_barra").val('');
                    $("#code_barra").focus();
                }


            }
        });

    })
});