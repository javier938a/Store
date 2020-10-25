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
    
    url='ws://'+window.location.host+'/ws/productos/';
    socket = new WebSocket(url);
    socket.onopen=function(e){
        console.log('Conectado..');
    }
    socket.onclose=function(e){
        console.log('Desconectado');
    }
    socket.onmessage=function(e){
        productos=JSON.parse(e.data);
        filas_todas='<tr>'
        fila=''
        for(let i in productos){
            id = productos[i].pk;
            producto = productos[i].fields.producto;
            cantidad = productos[i].fields.cantidad;
            precio_unitario = productos[i].fields.precio_unitario;
            precio_venta=productos[i].fields.precio_venta;
            fila += '<tr id="fila_'+id+'" class="selected">\
                        <th scope="row">'+id+'</th>\
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
            'clave_nombre':clave,
        }));
    });

    $("#save").on('click', function(evt){
        //alert($("#recipient-name").val());
        //alert("Holaaa")
        mod.modal('toggle');
        $("#txt_clave_prod").val('');

    })

    $('#txt_clave_prod').keydown(function(event){
        console.log(event.keyCode);
        if((event.keyCode>64 && event.keyCode<91) || (event.which>48 && event.which<58)){
            clave=$('#txt_clave_prod').val();
            console.log(clave);
            socket.send(JSON.stringify({
                'clave_nombre':clave,
            }));
        }else if(event.keyCode==13){
            clave=$('#txt_clave_prod').val();
            socket.send(JSON.stringify({
                'clave_nombre':clave,
            }));
        }else if(event.keyCode==8){
            clave=$('#txt_clave_prod').val();
            socket.send(JSON.stringify({
                'clave_nombre':clave,
            }));    
        }
    });
    $("#prodajax").on('submit',function(e){
        e.preventDefault();
        clave=$('#txt_clave_prod').val();
        console.log(clave);
        socket.send(JSON.stringify({
            'clave_nombre':clave,
        }));
    });
    //resaltando filas
    $(document).on("click", ".selected", function(){
        idFila=$(this).attr('id');
        if($('#'+idFila+'').hasClass('fila_selecionada')){
            $('#'+idFila+'').removeClass('fila_selecionada');
        }else{
            $('#'+idFila+'').addClass('fila_selecionada');
        }
    });


    function fila_select(){
        fila=$("#fila_"+id);
        if(fila.hasclass("fila_selecionada")){
            fila.removeClass('fila_selecionada');
        }else{
            fila.addClass('fila_selecionada');
        }
    }

});