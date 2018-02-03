import React from 'react';
import {Route, Switch} from 'react-router';
import { Link } from 'react-router-dom'

import {CardsList} from './Cards.jsx';
import {CardInfo} from './Cards.jsx';
import {Settings} from './Settings.jsx'
import SideMenu from "./SideMenu.jsx";

export const Home = () =>(

        <div class="jumbotron">
            <h1 class="display-3">Дисконтная система "ВТИ-ДИСКОНТ"</h1>
            <br />
                <h3 class="display-5">Быстрый старт:</h3>
                <ul>
                    <li class="lead">
                        <Link to="/cards/">Заведите карты</Link>
                    </li>
                    <li class="lead">
                        <Link to="/settings/">Настройте режим работы дисконтной системы</Link>
                    </li>
                    <li class="lead">
                        <a  href="/settings/">Добавьте кассы</a>
                    </li>
                    <li class="lead">
                        <a  href="/settings/">Настройте рабочие места с помощью файла настроек</a>
                    </li>
                    <li class="lead">
                        <a  href="/settings/">Установите службу VtiDiscountKeeper для бесперебойной работы</a>
                    </li>
                    <li class="lead">
                        <a  href="/transactions/">Контролируйте продажи</a>
                    </li>
                </ul>
        </div>

)

const Inbox =  () =>{
            <div>
                <h2>Inbox</h2>
            </div>
}

export const Main =() =>(
    <main>
        <SideMenu />
        <div className="container-fluid custom" id="content">
            <Switch>
                <Route exact path={'/'} component ={Home} />
                <Route path='/card/:code' component={CardInfo}/>
                <Route exact path={'/cards'} component={CardsList} />
                <Route exact path={'/settings'} component={Settings} />


            </Switch>
        </div>
    </main>
)

export default Main