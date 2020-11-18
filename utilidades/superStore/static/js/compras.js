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

class FilaCompra extends React.Component{
    constructor(props){
        super(props);
        this.state={precio:'', cantidad:'', total:''};
        this.handleChange=this.handleChange.bind(this);
    }

    handleChange(e){
        if(e.target.name==="cantidad"){
            this.setState({cantidad:e.target.value});
        }else if(e.target.name==="precio"){
            this.setState({precio:e.target.value});
        }
        
    }

    render(){
        const idprod=this.props.id;
        const producto=this.props.producto;
        const proveedor=this.props.proveedor;

        const cantidad = this.state.cantidad;
        const precio = this.state.precio;

        const total= cantidad!=''&& precio!='' ? parseFloat(cantidad)*parseFloat(precio):0.0;
    
        console.log(total);

        return(
            <tr>
                <td>{idprod}</td>
                <td>{producto}</td>
                <td>{proveedor}</td>
                <td><input type="text" value={this.state.cantidad} name="cantidad" onChange={this.handleChange} /></td>
                <td>$<input type="text" value={this.state.precio} name="precio" onChange={this.handleChange}/></td>
                <td>${total.toString()}</td>
            </tr>
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
            <td>{dato}</td>
        )
    }
}

class Fila extends React.Component{
    constructor(props){
        super(props);
        this.handleClickSelected=this.handleClickSelected.bind(this);
        this.handleClickAdd=this.handleClickAdd.bind(this);
        this.state={selected:'selected', fila_selected:''};
    }

    handleClickSelected(e){
        console.log(this.state.fila_selected);
        this.setState(fila=>({fila_selected:fila.fila_selected===''?'fila_seleccionada':''}));
    }

    handleClickAdd(e){
        const id=this.props.id;
        const producto=this.props.producto;
        const proveedor=this.props.proveedor;

        ReactDOM.render(
            <FilaCompra id={id} producto={producto} proveedor={proveedor}/>,
            document.getElementById('lista_compras')
        )
    }

    render(){
        const id=this.props.id;
        const producto=this.props.producto;
        const cantidad=this.props.cantidad;
        const proveedor=this.props.proveedor
        const classSelected=this.state.selected+' '+this.state.fila_selected;
        return(
            <tr className={classSelected}  onClick={this.handleClickSelected}>
                <Celda dato={id}/>
                <Celda dato={producto}/>
                <Celda dato={cantidad}/>
                <Celda dato={proveedor}/>
                <td><button type="button" onClick={this.handleClickAdd}>agregar</button></td>
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
                <Fila id={element.pk} producto={element.fields.producto} cantidad={element.fields.cantidad} proveedor={element.fields.proveedor} />
        );
        
        return(
                <table className="table table-dark">
                    <thead>
                        <th scope="col">ID</th>
                        <th scope="col">Producto</th>
                        <th scope="col">Cantidad Actual</th>
                        <th scope="col">Proveedor</th>
                    </thead>
                    <tbody>
                        {listaProdMap} 
                    </tbody>
                </table>
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
            this.state={clave_nombre:''}
        }
        handleChange(clave){
            //alert(clave);
            this.setState({clave_nombre:clave})
            socket.send(JSON.stringify({
                'tipo_busqueda':'producto',
                'clave_nombre':clave
            }));
            
        }
        handleSubmit(e){
            e.preventDefault();
            socket.send(JSON.stringify({
                'tipo_busqueda':'producto',
                'clave_nombre':this.state.clave_nombre
            }));
        }
        render(){
            return (<div>
                        <form onSubmit={this.handleSubmit}>
                            <EntradaInput handleChange={this.handleChange} />
                            <div className="form-group" >
                                <button type="submit" className="btn btn-primary">Buscar</button>
                                <a className="btn btn-secondary" href="/superStore/producto/guardar_producto" target="_blank">Nuevo Producto</a>
                                <a className="btn btn-secondary" href="/superStore/registrar_prove" target="_blank">Nuevo Proveedor</a>
                            </div>
                        </form>
                    </div>);
        }
    
    }

    $('#exampleModal').on('show.bs.modal', function (event) {
        var modal = $(this)
            socket.send(JSON.stringify({
                'tipo_busqueda':'producto',
                'clave_nombre':''
            }));

            ReactDOM.render(
                <FormBusqueda/>,
                document.getElementById('buscar')
            )
      });




      
});