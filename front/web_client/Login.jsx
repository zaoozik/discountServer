import React from 'react';
import {render} from 'react-dom';
import {login} from './auth';
import { connect } from 'react-redux'
import store from './store';
import {Route, Redirect} from 'react-router';

export const getAuthToken = () => {
    let state = store.getState();
    return state.token;

}




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
    }

    onChangeUsername = (e) => {
        this.setState({username: e.target.value});
    }

    onChangePassword = (e) =>{
        this.setState({password: e.target.value});
    }

    localLogin = () =>{
        if(login(this.state.username, this.state.password)){
            this.props.history.push('/');
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