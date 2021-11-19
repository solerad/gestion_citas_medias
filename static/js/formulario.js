function validar_login() {
    var username = document.formRegistro.lname;
    var password = document.formRegistro.password;
   var username_len = username.value.length;
    if (username_len == 0 || username_len < 8) {
      alert("Debes ingresar un username con min. 8 caracteres");
      passid.focus();
      return false; //Para la parte dos, que los datos se conserven
    }
  
  var formato_email = /^\w+([\.-]?\w+)@\w+([\.-]?\w+)(\.\w{2,3})+$/;
    if (!email.value.match(formato_email)) {
      alert("Debes ingresar un email electronico valido!");
      email.focus();
      return false; //Para la parte dos, que los datos se conserven
    }
  }
  
  function  mostrarPassword(){
    var tipo = document.getElementById("contraseña");
    if(tipo.type == "password"){
        tipo.type = "text";
      }else{
          tipo.type = "password";
        }
    }
  
  
  
  function  ocultarPassword(){
    var tipo = document.getElementById("contraseña");
    if(tipo.type == "password"){
        tipo.type = "password";
      }
  }

  function validar_registro() {
    var username = document.formRegistro.lname;
    var email = document.formRegistro.correo;
    var password = document.formRegistro.password;
   var username_len = username.value.length;
    if (username_len == 0 || username_len < 8) {
      alert("Debes ingresar un username con min. 8 caracteres");
      passid.focus();
      return false; //Para la parte dos, que los datos se conserven
    }
  
  var formato_email = /^\w+([\.-]?\w+)@\w+([\.-]?\w+)(\.\w{2,3})+$/;
    if (!email.value.match(formato_email)) {
      alert("Debes ingresar un email electronico valido!");
      email.focus();
      return false; //Para la parte dos, que los datos se conserven
    }
  }