import React from 'react';
import { Link } from 'react-router-dom';
import {Alert} from './Tools.jsx';
import ReactDOM from 'react-dom';





export class CardInfo extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            accumulation:
                "",
            bonus_to_delete:
                "",
            bonuses:
            [],
            discount_history:
            [],
            history:
            [],
            changes_date:
                "",
            code:
                "",
            deleted:
                "",
            discount:
                "",
            fav_date:
                "",
            holder_name:
                "",
            holder_phone:
                "+7",
            id:
                "",
            last_transaction_date:
                "",
            org:
                "",
            reg_date:
                "",
            sex:
                "",
            type:
                ""
        }
        this.saveCard = this.saveCard.bind(this);
    }

    async loadCard(code) {
        this.setState({
            ... await fetch("/cards/api/"+ code + "/",
                {
                    method: 'get',
                    credentials: 'include',
                } ).then(response =>response.json())

        })
    }

    async loadDiscountHistory(code) {
        let data = await fetch("/transactions/api/"+ code + "/discount/",
                {
                    method: 'get',
                    credentials: 'include',
                } ).then(response =>response.json())
        this.setState(
            {
                discount_history: data
            }
        )

    }

    async loadHistory(code) {
        let data = await fetch("/transactions/api/"+ code + "/",
            {
                method: 'post',
                body: JSON.stringify({count: 20}),
                credentials: 'include',
            } ).then(response =>response.json())
        this.setState(
            {
                history: data
            }
        )

    }


    onInputChange = (e) =>{
        let parameter = e.target.name;
        let temp = this.state;
        temp[parameter] = e.target.value;
        console.log(temp);

        this.setState(
            {
                ... temp
            }
        )

    }

    async saveCard () {
        let data = await fetch("/cards/api/" + this.props.match.params.code + "/",
                {
                    method: 'put',
                    body: JSON.stringify(this.state),
                    credentials: 'include',
                } ).then(response =>response.json())
        if (data.status=='success'){
            ReactDOM.render(<Alert isError={false} message={data.message}/>, document.getElementById('alert'));
        }
        if (data.status=='error'){
            ReactDOM.render(<Alert isError={true} message={data.message}/>, document.getElementById('alert'));
        }

    }

    componentWillUnmount(){
        ReactDOM.unmountComponentAtNode(document.getElementById('alert'));
    }

    componentDidMount(){
        this.loadCard(this.props.match.params.code);
        this.loadDiscountHistory(this.props.match.params.code);
        this.loadHistory(this.props.match.params.code);
    }

    render() {
        let sum_negative_style = {color: 'red'};
        let sum_common_style = {color: 'black'};
        let form_control_class = "form-control form-control-sm";

        let bonuses = this.state.bonuses.map(function (item, index,){
            let active_from = new Date(item.active_from);
            let active_to = new Date(item.active_to);

            return (
                    <tr key={'bonus_id_'+item.id}>
                        <td>{item.value}</td>
                        <td>{active_from.toLocaleDateString()}</td>
                        <td>{active_to.toLocaleDateString()}</td>
                    </tr>

            )
        })
        if (bonuses.length == 0){
            bonuses= (
                <tr key={'bonus_empty'}>
                    <td colSpan={3}>Бонусы отсутствуют</td>

                </tr>
            )
        }

        let discount_history = this.state.discount_history.map(function (item, index,){

            return (

                <tr key={'discount_id_'+item.id}>
                    <td style={{color: "blue"}}>{item.bonus_add} %</td>
                    <td>{item.date}</td>
                    <td style={item.sum <0 ? sum_negative_style : sum_common_style}>{item.sum} руб.</td>
                </tr>
            )
        })

        if (discount_history.length == 0){
            discount_history= (
                <tr key={'discount_empty'}>
                    <td colSpan={3}>Пересчеты скидок отсутствуют</td>

                </tr>
            )
        }

        let history = this.state.history.map(function (item, index,){

            return (

                <tr key={'history_id_'+item.id}>
                    <td>{item.date}</td>
                    <td>{item.type}</td>
                    <td style={item.sum <0 ? sum_negative_style : sum_common_style}>{item.sum} руб.</td>
                    <td>{item.bonus_add}</td>
                    <td>{item.bonus_reduce}</td>


                </tr>
            )
        })

        if (history.length == 0){
            history= (
                <tr key={'history_empty'}>
                    <td colSpan={3}>Операции по карте отсутстуют</td>

                </tr>
            )
        }


        return (
            <div className={""}>
            <h3>Карта номер {this.props.match.params.code}
            </h3>
                <ul class="nav nav-tabs" id="card-tab" role="tablist">
                    <li class="nav-item">
                        <a class="nav-link active" id="home-tab"  href="#info" data-toggle="tab" role="tab" aria-controls="home" aria-selected="true" >Информация</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" id="bonus-tab" href="#bonus" data-toggle="tab" role="tab" aria-controls="home" aria-selected="true">Бонусы</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" id="discount-tab" href="#discount" data-toggle="tab" role="tab" aria-controls="home" aria-selected="true">Скидки</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link "  id="history-tab" href="#history" data-toggle="tab" role="tab" aria-controls="home" aria-selected="true">Операции</a>
                    </li>
                </ul>

                <div class="tab-content" id="card-tab-content">
                    <div class="tab-pane fade show active" id="info" role="tabpanel" aria-labelledby="home-tab">
                        {/*CARD INFO STARTS*/}

                        <form>
                            <label>
                                КОД
                            </label>
                            <input
                                type="text"
                                className={form_control_class}
                                name={"code"}
                                value={this.state.code}
                                disabled={true}
                                onChange={this.onInputChange}
                            />
                            <label>
                                Тип
                            </label>
                            <select name={"type"} onChange={this.onInputChange} value={this.state.type} className={form_control_class}>
                                <option value={"bonus"}>Бонусная</option>
                                <option value={"discount"}>Дисконтная</option>
                                <option value={"combo"}>Комбинированная</option>

                            </select>
                            <label >
                                ФИО владельца
                            </label>
                            <input type={"text"}
                                   className={form_control_class}
                                   name={"holder_name"}
                                   value={this.state.holder_name}
                                   onChange={this.onInputChange}
                            />
                            <label >
                            Пол
                            </label>
                            <select name={"sex"} onChange={this.onInputChange} value={this.state.sex} className={form_control_class}>
                                <option value={"m"}>Мужчина</option>
                                <option value={"f"}>Женщина</option>
                            </select>
                            <label >
                            Телефон
                            </label>
                            <input type={"text"}
                            className={form_control_class}
                            name={"holder_phone"}
                            value={this.state.holder_phone}
                                   onChange={this.onInputChange}
                                   defaultValue={"+7"}
                            />
                            <label >
                            Дата регистрации
                            </label>
                            <input disabled={true}
                            className={form_control_class}
                            name={"reg_date"}
                            value={this.state.reg_date}
                                   onChange={this.onInputChange}
                            />
                            <label >
                            Дата последних изменений
                            </label>
                            <input disabled={true}
                            className={form_control_class}
                            name={"changes_date"}
                            value={this.state.changes_date}
                                   onChange={this.onInputChange}/>
                            <label >
                            Дата последней транзакции
                            </label>
                            <input disabled={true}
                            className={form_control_class}
                            name={"last_transaction_date"}
                            value={this.state.last_transaction_date}
                                   onChange={this.onInputChange}
                            />
                        </form>

                        {/*CARD INFO ENDS */}

                    </div>
                    <div class="tab-pane fade" id="bonus" role="tabpanel" aria-labelledby="profile-tab">

                        {/*CARD_BONUS STARTS*/}

                        <div>
                            <label>
                                Всего бонусов
                            </label>
                            <input className={form_control_class} name={"bonus_total"} value={this.state.bonus}/>
                            <label >
                                Накопления по карте
                            </label>
                            <input className={form_control_class} name={"accumulation"} value={this.state.accumulation}/>
                            <table className="table">
                                <thead>
                                <th>Начисление</th>
                                <th>Дата</th>
                                <th>Сгорят</th>
                                </thead>
                                <tbody>
                                    {bonuses}
                                </tbody>
                            </table>

                        </div>

                        {/*CARD_BONUS ENDS*/}

                    </div>
                    <div class="tab-pane fade" id="discount" role="tabpanel" aria-labelledby="contact-tab">

                        {/*CARD DISCOUNT STARTS*/}

                        <div>
                            <label>
                                Процентная скидка
                            </label>
                            <input className={form_control_class} name={"bonus_total"} value={this.state.discount}/>
                            <label >
                                Накопления по карте
                            </label>
                            <input className={form_control_class} name={"accumulation"} value={this.state.accumulation}/>
                            <label >
                                ДО следующей скидки
                            </label>
                            <input className={form_control_class} name={"accumulation"} value={2345}/>
                            <table className="table">
                                <thead>
                                <th>Пересчет</th>
                                <th>Дата</th>
                                <th>Сумма покупки</th>
                                </thead>
                                <tbody>
                                {discount_history}
                                </tbody>
                            </table>

                        </div>

                        {/*CARD DISCOUNT ENDS*/}

                    </div>
                    <div class="tab-pane fade" id="history" role="tabpanel" aria-labelledby="contact-tab">
                        {/* CARD HISTORY START */}

                        <table className="table">
                            <thead>
                            <tr>
                                <th>Дата/время</th>
                                <th>Тип</th>
                                <th>Сумма покупки</th>
                                <th>Начисление бонусов/пересчет скидки</th>
                                <th>Списание бонусов</th>
                            </tr>
                            </thead>
                            <tbody>
                                {history}
                            </tbody>
                        </table>

                        {/* CARD HISTORY ENDS */}
                    </div>
                </div>
                < br />

                <div className={"bottom-buttons"} >
                    <button type="button"
                            className="btn btn-primary"
                            onClick={this.saveCard}><i class="fa fa-floppy-o" aria-hidden="true"></i> Сохранить</button>
                        <Link to={'/cards/'}>
                            <button type="button"
                                className="btn btn-secondary"><i class="fa fa-arrow-left" aria-hidden="true"></i> Назад</button>
                        </Link>
                </div>

            </div>
        )

    }
}


export class CardsList extends React.Component{

    constructor(props){
        super(props);
        this.state={
            cardsList: [],
            list_current_position: 0,
            list_count: 30,
            list_total: 0,
            list_end: false
        }

    }



    async loadCardsList() {
        console.log('start load');
        if (this.state.list_end){
            return;
        }
            let data = await fetch("/cards/api/",
                {
                    method: 'post',
                    credentials: 'include',
                    body: JSON.stringify({
                        current: this.state.list_current_position,
                        count: this.state.list_count
                    }),
                } ).then(
                    response =>response.json())
        let total = data.list_total;
            let current = data.list_current_position;
            let count = this.state.list_count;
            let state = this.state.list_end;

            if (total < count) {
                count = total;

            }
            current = current + count;

            if (current > total){
                current = total;
                state = true;
            }
        this.setState(
            {
                cardsList: [...this.state.cardsList, ...data.data],
                list_current_position: current,
                list_total: total,
                list_count: count,
                list_end: state
            }
        )

    }

    handleScroll = () =>{
        console.log("SCROLLED");

        var height = 0;
        $.each($('#tbody').children(), function(index, value){

            height += value.clientHeight;

        });
        //alert(height + ";" + ($('#scrollData').height() -40));
        if (height < ($('#scrollData').height() -40))
        {
            this.loadCardsList();
            //alert(height + ";" + ($('#scrollData').height() -40));
            return;
        }

        if  ($('#tbody').scrollTop() + $('#scrollData').height() -40 == height )
        {

            this.loadCardsList();
            //alert(height + ";" + ($('#scrollData').height() -40));
            return;
        }

    }



    componentDidMount(){
        this.loadCardsList();
        document.getElementById('tbody').addEventListener('scroll', this.handleScroll);

    }

    render(){
        let temp = this.state.cardsList;
        var obj=this;
        let cards = temp.map(function (item, index,){
                let type;
                if (item.type == 'bonus'){
                    type="Бонусная";
                }
            if (item.type == 'discount'){
                type="Дисконтная";
            }
            if (item.type == 'combo'){
                type="Комбинированная";
            }
            return (

                <tr key={'id_'+item.code}>
                    <td>
                        <input type={'checkbox'}
                               id={item.code} />
                    </td>
                    <td>{item.code}</td>
                    <td>{type}</td>
                    <td>{item.accumulation}</td>
                    <td>{item.holder_name}</td>
                    <td>
                        <Link to={"/card/"+item.code + '/'} >
                        <button
                                type="button"
                                value={item.code}
                                className="fa fa-eye"
                                aria-hidden="true"
                                title="Просмотр"></button>
                        </Link>

                    </td>
                </tr>
            )
        })

        return (
            <div>
                <CardsToolBox />

                {/* COUNTER PANEL*/}

                <div class="form-group row pull-right">
                    <small id="total">{this.state.list_current_position + ' из '+ this.state.list_total}</small>
                </div>

                <div id={"data"}>
                <table className={"scroll-table"} id={'scrollData'}>
                    <thead>
                        <tr>
                            <th></th>
                            <th>КОД</th>
                            <th>ТИП</th>
                            <th>НАКОПЛЕНИЯ</th>
                            <th>ФИО</th>
                            <th></th>
                        </tr>
                    </thead>

                    <tbody
                        id={'tbody'}
                        style={{height: '485px'}}>
                    {cards}
                    </tbody>
                </table>
                </div>


            </div>

    );

    }
}

class CardsToolBox extends React.Component{
    render(){
        let css_form_control_sm = "form-control form-control-sm ";

        return(
        <div id = "tools">
            <hr />
            <div className={"form-group row"}>
                <div className={"col-5 "}>
                    <button className={"btn btn-success btn-sm"}
                            id="addCardButton"
                            data-toggle="modal"
                            data-target="#CardModal">
                        <i className={"fa fa-credit-card"} aria-hidden="true"></i> Добавить
                    </button>
                    <button className={"btn btn-danger btn-sm"}
                            onclick="deleteCard();">
                            <i className="fa fa-trash-o" aria-hidden="true"></i> Удалить
                    </button>
                    <button className="btn btn-warning btn-sm"
                            onclick="restoreCard();">
                            <i className="fa fa-recycle" aria-hidden="true"></i> Восстановить
                    </button>
                </div>
                <div className="col-5">
                     <input type="text" id="search" className={css_form_control_sm} placeholder="Код карты или ФИО владельца" />
                </div>
                <div className="col-2">
                    <button className="btn btn-primary btn-sm"
                            onclick="dataUpdate();">
                        <i className="fa fa-filter" aria-hidden="true"></i> Применить
                    </button>
                </div>
            </div>
            <div className="form-group row">
                <div className="col-5 ">
                    <button className="btn btn-success btn-sm"
                            id="massAddCardButton"
                            data-toggle="modal"
                            data-target="#MassCardModal">
                            <i className="fa fa-users" aria-hidden="true"></i> Массовое добавление
                    </button>
                </div>
                <div className="col-5">
                    <div className="d-inline-block">
                        <small>Сортировать по</small>
                        <select id="sort"
                            className={css_form_control_sm +"d-inline-block"}>
                                <option value="code">КОД</option>
                                <option value="holder_name">ФИО</option>
                                <option value="accumulation"> Накопления</option>
                        </select>
                    </div>
                    <div className="d-inline-block">
                        <button id="order-desc"
                                className="btn btn-outline-primary btn-sm active"
                                onclick="setSortOrder('-');">
                                <i className="fa fa-sort-amount-desc" aria-hidden="true"></i>
                        </button>
                    </div>
                    <div className="d-inline-block">
                            <button id="order-asc"
                                    className="btn btn-outline-primary btn-sm "
                                    onclick="setSortOrder('');">
                                    <i className="fa fa-sort-amount-asc" aria-hidden="true"></i>
                            </button>
                    </div>
                    <br />
                    <small>Тип карты</small>
                    <select id="type"
                            className="form-control form-control-sm">
                            <option value="">Все</option>
                            <option value="bonus">Бонусная</option>
                            <option value="discount">Дисконтная</option>
                            <option value="combo">Комбо</option>
                    </select>
                    <label className="form-check-label form-control-sm">
                        <input className={css_form_control_sm + "form-check-input"}
                               type="checkbox"
                               id="showDeleted" /> Показать удаленные
                    </label>
                </div>
                <div className="col-2">
                    <button className="btn btn-primary btn-sm"
                            onclick="clearFilter();">
                            <i className="fa fa-repeat" aria-hidden="true"></i> Сбросить
                    </button>
                </div>
            </div>
            <div className="form-group row pull-right">
                <small id="total"></small>
            </div>
            <hr />
        </div>
        )
    }
}

export default CardsList;