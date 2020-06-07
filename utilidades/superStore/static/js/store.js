function validar_formulario(){
    jQuery.validator.messages.required ='Este campo es obligatorio.';
    jQuery.validator.messages.email = 'Este correo no es correcto.'
    var validado = $("#form").valid();
    $("#enviar").click(function(e){
        e.preventDefault();
        if(validado ==true){
            if($("#contra").val()==$("#confir_contra").val()){
                $.post(reg_usu,{
                    "txtnombre":$("#nombres").val(),
                    "txtapellido":$("#apellido").val(),
                    "txtusuario":$("#usuario").val(),
                    "txtcorreo":$("#correo").val(),
                    "txtcontra":$("#contra").val()

                }, function(data){
                    console.log("Prosesamiento finalizado", data);
                });
            }else{
                alert("Las contraseñas ingresadas son incorrectas!")
            }
        }
    });
}
$(document).ready(function(){
    validar_formulario();
})