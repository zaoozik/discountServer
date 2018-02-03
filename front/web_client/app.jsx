import React from 'react';
import {render} from 'react-dom';
import Login from './Login.jsx';
import Main from './routes.jsx'


import { BrowserRouter, Switch, Route} from 'react-router-dom'



 const App = () => (
    <div>
        <Switch>
            <Route exact path={'/login'} component ={Login} />
            <Route path={'/'} component = {Main} />
        </Switch>
    </div>
)

render((
    <BrowserRouter>
        <App />
    </BrowserRouter>
), document.getElementById('main'));

    //render((<SideMenu/>, document.getElementById('side-menu'));
    //render (<CardsList />, document.getElementById('cardsList'));
    //render (<Login />, document.getElementById('login'));
