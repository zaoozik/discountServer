import React from 'react';
import { Link } from 'react-router-dom'

class SideMenu extends React.Component {
  render() {
    return (
       <div className="nav-side-menu">
    <div className="brand">
        <img height='32' width='298' src="/static/images/logo.png"/>
    </div>
    <div className="brand">

            <a  className="nav-item" style={{marginRight: "10px"}}>"first_name  last_name"</a>
            <a href = "/logout/" className="logout">Выйти</a>

    </div>
    <i className="fa fa-bars fa-2x toggle-btn" data-toggle="collapse" data-target="#menu-content"></i>

        <div className="menu-list">

            <ul id="menu-content" className="menu-content collapse out">
                <Link to='/'>
                    <li>
                      <i className="fa fa-lg fa-home" aria-hidden="true"></i> Главная
                    </li>
                </Link>

                <Link to="/cards">
                    <li>
                        <i className="fa fa-credit-card fa-lg" aria-hidden="true"></i> Карты
                    </li>
                </Link>

                <Link to="/transactions">
                    <li>
                        <i className="fa fa-history fa-lg" aria-hidden="true"></i> История операций
                    </li>
                </Link>

                <Link to="/queue">
                    <li>
                        <i className="fa fa-tasks fa-lg" aria-hidden="true"></i> Задания
                    </li>
                </Link>

                <Link to="/service">
                    <li>
                        <i className="fa fa-database fa-lg" aria-hidden="true"></i> Сервисные операции
                    </li>
                </Link>

                <Link to="/settings">
                    <li>
                        <i className="fa fa-cogs fa-lg" aria-hidden="true"></i> Настройки

                    </li>
                 </Link>

                 <AdminButton />

            </ul>
     </div>

</div>
    );
  }

}


class AdminButton extends React.Component{

    render()
        {
            return (
            <Link to="/admin">
                    <li>
                        <i className="fa fa-dashboard fa-lg"></i> Администрирование
                    </li>
            </Link>
                );
        }

}


export default SideMenu;