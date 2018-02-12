import React from 'react';
import {render} from 'react-dom';
import {login} from './auth';
import ReactDOM from "react-dom";
import {Alert} from "./Tools.jsx";






class Login extends React.Component{

    constructor(props){
        super(props);
        this.state=
            {
                username: null,
                password: null
            }
            ;
        this.onChangeUsername = this.onChangeUsername.bind(this);
        this.onChangePassword = this.onChangePassword.bind(this);
        this.localLogin = this.localLogin.bind(this);
    }

    onChangeUsername = (e) => {
        this.setState({username: e.target.value});
    }

    onChangePassword = (e) =>{
        this.setState({password: e.target.value});
    }

    async localLogin(){
            var obj = this;
            let data = await fetch("/login/",
                {
                    method: 'post',
                    body: JSON.stringify({username: obj.state.username, password: obj.state.password}),
                    credentials: 'include',
                } ).then(response =>response.json())


        if (data.result == 'success'){
            this.props.history.push('/');
        }
        else if (data.result == 'error'){
            ReactDOM.render(<Alert isError={true} message={data.message}/>, document.getElementById('alert'));
        }

    }

    render(){
        return(
                <div className="containter h-100">
                <br />
                    <br />
                    <br />
                <div className="row h-100 justify-content-center align-items-center">
                    <div className="card col-sm-4">

                        <div className="form-signin">
                            <h2 className="form-signin-heading">Авторизация</h2>
                            <label for="user">Логин</label>
                            <input type="text" className="form-control" name={"username"} onChange={this.onChangeUsername}  />

                                <label for="password">Пароль</label>
                                <input type ='password' className="form-control" name={"password"} onChange={this.onChangePassword}  />
                                    <br />
                                        <button className="btn btn-lg btn-primary btn-block" onClick={this.localLogin}>Войти</button>
                                        <br />
                        </div>
                    </div>
                </div>
            </div>)
    }
}

export default Login