import React from 'react';
import ReactDOM from 'react-dom';

export class Alert extends React.Component{

    closeThis(){
        ReactDOM.unmountComponentAtNode(document.getElementById('alert'));
    }

   render(){
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
               <button type="button" class="close" aria-label="Close" onClick={this.closeThis}>
                   <span aria-hidden="true">&times;</span>
               </button>
               <h4 className="alert-heading">{header}</h4>
               <p>{this.props.message}</p>

           </div>
       )
   }
}