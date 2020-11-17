    //Conectando al socket

class EntradaInput extends React.Component{
    constructor(props){
        super(props);
        this.handleChange=this.handleChange.bind(this);
    }
    
    handleChange(e){
        this.props.handleChange(e.target.value);
    }
    
    render(){
        return(
            <div className="form-group" >
                <input className="form-control" type="text" onChange={this.handleChange} />
            </div>
        )
    }
        
}

class Celda extends React.Component{
    constructor(props){
        super(props);
    }
    render(){
        const dato=this.props.dato;
        return(
            <td>dato</td>
        )
    }
}

class Fila extends React.Component{
    constructor(props){
        super(props);
    }

    render(){
        const datos = this.props.datos;
        return(
            <tr>
                {listVal}
            </tr>
        )
    }
}

class Tabla extends React.Component{
    constructor(props){
        super(props);
        this.handleClickfila=this.handleClickfila.bind(this);
    }

    handleClickfila(e){

    }

    render(){
        const listaProd=this.props.listaProd;
        //console.log(listaProd);
        const listaProdMap = listaProd.map((element)=>//recorriendo el ojeto json pasado
            <tr className='selected' onClick={this.handleClickfila}>
                <td>{element.pk}</td>
                <td>{element.fields.producto}</td>
                <td>{element.fields.cantidad}</td>  
            </tr>
        );
        
        return(
            <div>
                <table className="table table-dark">
                    <thead>
                        <th scope="col">ID</th>
                        <th scope="col">Producto</th>
                        <th scope="col">Cantidad Actual</th>
                    </thead>
                    <tbody>
                        {listaProdMap} 
                    </tbody>
                </table>
            </div>
        )
    }
}

$(document).ready(function(){
    

    var url='ws://'+window.location.host+'/ws/prod_client/';
    var socket = new WebSocket(url);

    socket.onopen=function(e){
        console.log("Te has conectado al socket");
    }

    socket.onmessage=function(e){
        var datos = JSON.parse(e.data);
        //console.log(datos);
        ReactDOM.render(
            <Tabla listaProd={datos}/>,
            document.getElementById('tabla-prod')
        )
        //datos=JSON.parse(e.data);
        //console.log(datos);
    }

    socket.onclose=function(e){
        console.log("Te has conectado del socket");
    }
    //fin del sockt
    
    class FormBusqueda extends React.Component{
        constructor(props){
            super(props);
            this.handleChange=this.handleChange.bind(this);
            this.handleSubmit=this.handleSubmit.bind(this);
        }
        handleChange(clave){
            //alert(clave);
            socket.send(JSON.stringify({
                'tipo_busqueda':'producto',
                'clave_nombre':clave
            }));
            
        }
        handleSubmit(e){
            e.preventDefault();
        }
        render(){
            return (<div>
                        <form onSubmit={this.handleSubmit}>
                            <EntradaInput handleChange={this.handleChange} />
                            <div className="form-group" >
                                <button className="btn btn-primary">Buscar</button>
                            </div>
                            
                        </form>
                    </div>);
        }
    
    }

    $('#exampleModal').on('show.bs.modal', function (event) {
        var modal = $(this)
            ReactDOM.render(
                <FormBusqueda/>,
                document.getElementById('buscar')
            )
      });




      
});