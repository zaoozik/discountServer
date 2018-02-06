import React from 'react';
import ReactDOM from 'react-dom';

export class Alert extends React.Component{

    closeThis(){
        ReactDOM.unmountComponentAtNode(document.getElementById('alert'));
    }

   render(){
       console.log(alertCss, header);
       let header;
       let alertCss;
       if (this.props.isError){
            header='Ошибка!';
            alertCss = 'alert alert-danger';
       }  else {
           header='Успешно!';
           alertCss = 'alert alert-success';
       }
       return(
           <div className={alertCss} role="alert">
               <h4 className="alert-heading">{header}</h4>
               <p>{this.props.message}</p>
               <hr />
               <button onClick={this.closeThis}><i className="fa fa-times"></i></button>
           </div>
       )
   }
}