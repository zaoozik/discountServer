import React from 'react';
import { Link, Redirect } from 'react-router-dom';
import {Alert} from './Tools.jsx';
import ReactDOM from 'react-dom';
import DatePicker from 'react-datepicker';
import moment from "moment";



export class AddBonusModal extends React.Component{
    constructor(props){
        super(props);
        this.state = {
            value: 1,
            active_to: Date.now(),
            active_from: Date.now()

        }
        this.render = this.render.bind(this);
        this.addBonus = this.addBonus.bind(this);
    }

    async addBonus () {
        let data = await fetch("/cards/api/" + this.props.card_code + "/bonus/",
            {
                method: 'put',
                body: JSON.stringify(this.state),
                credentials: 'include',
            } ).then(response =>response.json())
        if (data.status=='success'){
            ReactDOM.render(<Alert isError={false} message={data.message}/>, document.getElementById('alert'));
            this.props.load(this.props.card_code);
        }
        if (data.status=='error'){
            ReactDOM.render(<Alert isError={true} message={data.message}/>, document.getElementById('alert'));
        }

    }

    onValueChange = (e) =>{


        this.setState(
            {
                value: e.target.value
            }
        )

    }


    onDateFromChange = (d) =>{


        this.setState(
            {
                active_from: d
            }
        )

    }

    onDateToChange = (d) =>{


        this.setState(
            {
                active_to: d
            }
        )

    }

    render(){
        return(
            <div className="modal fade" id="AddBonusModal">
                <div className="modal-dialog" role="document">
                    <div className="modal-content">
                        <div className="modal-header">
                            <h5 className="modal-title">Добавить бонусы</h5>
                            <button type="button" class="close"  data-dismiss="modal" aria-label="Close">
                                <span aria-hidden="true">&times;</span>
                            </button>
                        </div>
                        <div className="modal-body">
                            <div key="BonusForm" >
                                <label >Количество*:</label>
                                <input type="number"
                                       name="value"
                                       onChange={this.onValueChange}
                                       value={this.state.value}
                                       required=""
                                       className="form-control
                                                form-control-sm"
                                />
                                <label >Действуют с*:</label>
                                <DatePicker
                                    className="form-control form-control-sm "
                                    dateFormat="YYYY-MM-DD"
                                    locale={'ru-RU'}
                                    placeholderText="Выберите дату"
                                    onChange={this.onDateFromChange}
                                    selected={moment(this.state.active_from)}/>
                                <label >Действуют по*:</label>
                                <DatePicker
                                    className="form-control form-control-sm "
                                                dateFormat="YYYY-MM-DD"
                                                locale={'ru-RU'}
                                    placeholderText="Выберите дату"
                                             onChange={this.onDateToChange}
                                             selected={moment(this.state.active_to)}/>
                               
                            </div>
                        </div>
                        <div className="modal-footer">
                            <button type="button" className="btn btn-primary" data-dismiss="modal" onClick={this.addBonus}>Добавить</button>
                            <button type="button" id="modal_close" className="btn btn-secondary" data-dismiss="modal">Отмена</button>
                        </div>
                    </div>
                </div>

            </div>
        )
    }
}

export class CardInfo extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            administrator:
            false,
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
                "n",
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
                "m",
            type:
                "bonus"
        }
        this.saveCard = this.saveCard.bind(this);
        this.render  =this.render.bind(this);
        this.deleteBonus=this.deleteBonus.bind(this);

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

    async deleteBonus(e) {
        if (confirm('Вы действительно хотите удалить бонусы?')) {

            let data = await fetch("/cards/api/" + this.props.match.params.code + "/bonus/",
                {
                    method: 'delete',
                    credentials: 'include',
                    body: JSON.stringify({id: e.target.value})
                }).then(response => response.json())

            if (data.status == 'success') {
                ReactDOM.render(<Alert isError={false} message={data.message}/>, document.getElementById('alert'));
                this.loadCard(this.props.match.params.code);
            }
            if (data.status == 'error') {
                ReactDOM.render(<Alert isError={true} message={data.message}/>, document.getElementById('alert'));
            }
        }

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
            this.props.history.push("/card/"+this.state.code + "/");
        }
        if (data.status=='error'){
            ReactDOM.render(<Alert isError={true} message={data.message}/>, document.getElementById('alert'));
        }

    }



    componentWillUnmount(){
        ReactDOM.unmountComponentAtNode(document.getElementById('alert'));
    }

    componentDidMount(){
        if (this.props.match.params.code!='new') {
            this.loadCard(this.props.match.params.code);
            this.loadDiscountHistory(this.props.match.params.code);
            this.loadHistory(this.props.match.params.code);
        }
    }

    render() {
        let sum_negative_style = {color: 'red'};
        let sum_common_style = {color: 'black'};
        let form_control_class = "form-control form-control-sm";
        let obj = this;
        let bonuses = this.state.bonuses.map(function (item, index,){
            let active_from = new Date(item.active_from);
            let active_to = new Date(item.active_to);

            return (
                    <tr key={'bonus_id_'+item.id}>
                        <td>{item.value}</td>
                        <td>{active_from.toLocaleDateString()}</td>
                        <td>{active_to.toLocaleDateString()}</td>
                        <td><button value={item.id} class="btn btn-small btn-outline-danger fa fa-times" onClick={obj.deleteBonus}></button></td>
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
            let date = new Date(item.date);
            return (


                <tr key={'discount_id_'+item.id}>
                    <td style={{color: "blue"}}>{item.bonus_add} %</td>
                    <td>{date.toLocaleString()}</td>
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
            let isNone = (item) =>{
                if ((item) == 0 || item =='0'){
                    return '-'
                }
                else
                {
                    return item
                }
            }

            let isNoneRub = (item) =>{
                if ((item) == 0 || item =='0'){
                    return '-'
                }
                else
                {
                    return item + " руб."
                }
            }

            let date = new Date(item.date);
            let type;
            if (item.type == 'bonus_reduce') {
                type = (<span style={{color: 'red'}}>Списание бонусов</span>);
            }
            else if (item.type == 'bonus_add') {
                type = (<span style={{color: 'green'}}>Начисление бонусов</span>);
            }
            else if (item.type == 'sell') {
                type = (<span style={{color: 'blue'}}>Продажа</span>);
            }
            else if (item.type == 'discount_recount') {
                type = (<span style={{color: 'orange'}}>Пересчет скидки</span>);
            }
            else if (item.type == 'refund') {
                type = (<span style={{color: 'red'}}>Возврат</span>);
            }
            else if (item.type == 'bonus_refund') {
                type = (<span style={{color: 'red'}}>Отмена бонусов</span>);
            }

            return (

                <tr key={'history_id_'+item.id}>
                    <td>{date.toLocaleString()}</td>
                    <td>{type}</td>
                    <td style={item.sum <0 ? sum_negative_style : sum_common_style}>{isNoneRub(item.sum)}</td>
                    <td>{isNone(item.bonus_add) + (item.type == 'discount_recount'? "%" : "")}</td>
                    <td>{isNone(item.bonus_reduce)}</td>


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

        let viewAddBonusButton=() =>{
            return(
                <tr >
                    <td colspan="4">
                        <button className="btn btn-success btn-sm" id="addCashBoxButton" data-toggle="modal" data-target="#AddBonusModal">Добавить</button>
                    </td>
                </tr>

            )
        }

        return (
            <div className={""}>
                <br />
            <h3> {this.props.match.params.code == 'new'? "Новая карта" : "Карта "+this.props.match.params.code}
            </h3>
                <br />
                <ul class="nav nav-tabs" id="card-tab" role="tablist">
                    <li class="nav-item">
                        <a class="nav-link active" id="home-tab"  href="#info" data-toggle="tab" role="tab" aria-controls="home" aria-selected="true" >Информация</a>
                    </li>
                    <li class={"nav-item "}>
                        <a  class={"nav-link " + (this.state.type=='discount'? 'disabled': '')} id="bonus-tab" href="#bonus" data-toggle="tab" role="tab" aria-controls="home" aria-selected="true">Бонусы</a>
                    </li>
                    <li  class="nav-item">
                        <a class={"nav-link " + (this.state.type=='bonus'? 'disabled': '')} id="discount-tab" href="#discount" data-toggle="tab" role="tab" aria-controls="home" aria-selected="true">Скидки</a>
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
                                disabled={this.props.match.params.code=='new'? false: true }
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
                    <div   class="tab-pane fade" id="bonus" role="tabpanel" aria-labelledby="profile-tab">

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
                                    {this.state.administrator ? viewAddBonusButton(): ""}
                                </tbody>
                            </table>

                            <AddBonusModal load={this.loadCard.bind(this)} card_code={this.props.match.params.code} />

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
            list_end: false,
            selected: [],
            filters: {
                showDeleted: false,
                card_type: "",
                order: "",
                sort: "code",
                search: ""

            }
        }

        this.targetSelection = this.targetSelection.bind(this);
        this.restoreSelected = this.restoreSelected.bind(this);
        this.deleteSelected = this.deleteSelected.bind(this);
        this.setFilters = this.setFilters.bind(this);
        this.showDeleted = this.showDeleted.bind(this);
        this.resetCardList = this.resetCardList.bind(this);

    }

    resetCardList(){
        this.setState({
            cardsList: [],
            list_current_position: 0,
            list_count: 30,
            list_total: 0,
            list_end: false,
            selected: [],
            filters: {
                showDeleted: false,
                card_type: "",
                order: "",
                sort: "code",
                search: ""

            }
        })
        this.updateCardsList();
    }

    setFilters(e){
        let filters = this.state.filters;
        filters[e.target.name] = e.target.value;
        this.setState(
            {
                selected: [],
                filters: filters
            })

        this.updateCardsList();

    }
    showDeleted(e){
        let filters = this.state.filters;
        filters[e.target.name] = e.target.checked;
        this.setState(
            {
                filters: filters,
                selected: []
            }
        )
        this.updateCardsList();

    }

    targetSelection(e){
        let selected = this.state.selected;
        if (e.target.checked){
            selected.push(e.target.id);
            this.setState(
                {
                    selected: selected
                }
            )}
            else{
                let pos = selected.indexOf(e.target.id);
                if ( ~pos ) selected.splice(pos, 1);
            this.setState(
                {
                    selected: selected
                }
            )

            }
    }

    async deleteSelected(){
        if (confirm('Удалить выбранные карты?')) {
            let data = await fetch("/cards/api/",
                {
                    method: 'delete',
                    credentials: 'include',
                    body: JSON.stringify(this.state.selected),
                }).then(
                response => response.json())
            this.resetCardList();
        }
    }

   async restoreSelected(){
        let data = await fetch("/cards/api/",
            {
                method: 'restore',
                credentials: 'include',
                body: JSON.stringify(this.state.selected),
            } ).then(
            response =>response.json())
       this.resetCardList();
    }


    async updateCardsList() {

        this.setState({
            list_current_position: 0,
            list_count: 30,
            list_total: 0,
            list_end: false,
            selected: [],
        })


        let data = await fetch("/cards/api/",
            {
                method: 'post',
                credentials: 'include',
                body: JSON.stringify({
                    current: 0,
                    count: 30,
                    filter: this.state.filters
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
                cardsList: [...data.data],
                list_current_position: current,
                list_total: total,
                list_count: count,
                list_end: state
            }
        )

    }

    async loadCardsList() {
        if (this.state.list_end){
            return;
        }
            let data = await fetch("/cards/api/",
                {
                    method: 'post',
                    credentials: 'include',
                    body: JSON.stringify({
                        current: this.state.list_current_position,
                        count: this.state.list_count,
                        filter: this.state.filters
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
        let deleted = {color: "red", "text-decoration" :"line-through"}
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

                <tr key={'id_'+item.code} className={item.deleted=='y'? "scroll-table-row-deleted": ""}>
                    <td>
                        <input type={'checkbox'}
                               id={item.id} onChange={obj.targetSelection} />
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
                <br />
                <h3>Карты системы</h3>
                <CardsToolBox obj={this} />


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
                    <Link to={'/card/new/'}>
                    <button className={"btn btn-success btn-sm"}
                            id="addCardButton">
                        <i className={"fa fa-credit-card"} aria-hidden="true"></i> Добавить
                    </button>
                    </Link>
                    <span> </span>
                    <button className={"btn btn-danger btn-sm"}
                            disabled={this.props.obj.state.selected.length > 0? false: true}
                            onClick={this.props.obj.deleteSelected}>
                            <i className="fa fa-trash-o" aria-hidden="true"></i> Удалить
                    </button>
                    <span> </span>
                    <button className="btn btn-warning btn-sm"
                            disabled={this.props.obj.state.selected.length > 0? false: true}
                            onClick={this.props.obj.restoreSelected}>
                            <i className="fa fa-recycle" aria-hidden="true"></i> Восстановить
                    </button>
                </div>
                <div className="col-5">
                     <input type="text" name="search"
                            value={this.props.obj.state.filters.search}
                            onChange={this.props.obj.setFilters}
                            className={css_form_control_sm}
                            placeholder="Код карты или ФИО владельца" />
                </div>
            </div>
            <div className="form-group row">
                <div className="col-5 ">
                    <button className="btn btn-success btn-sm"
                            id="massAddCardButton"
                            data-toggle="modal"
                            disabled={true}>
                            <i className="fa fa-users" aria-hidden="true"></i> Массовое добавление
                    </button>
                </div>
                <div className="col-5">
                    <div className="d-inline-block">
                        <small>Сортировать по</small>
                        <select id="sort" name={'sort'} onChange={this.props.obj.setFilters}
                                value={this.props.obj.state.filters.sort}
                            className={css_form_control_sm +"d-inline-block"}>
                                <option value="code">КОД</option>
                                <option value="holder_name">ФИО</option>
                                <option value="accumulation"> Накопления</option>
                        </select>
                    </div>
                    <span> </span>
                    <div className="d-inline-block">
                        <button
                                role="button"
                                name="order"
                                value={'-'}
                                className={"btn btn-outline-primary btn-sm fa fa-sort-amount-desc " + (this.props.obj.state.filters.order == '-' ? "active": "")}
                                onClick={this.props.obj.setFilters}>

                        </button>
                    </div>
                    <span> </span>
                    <div className="d-inline-block">
                            <button
                                    role="button"
                                    name="order"
                                    value={''}
                                    className={"btn btn-outline-primary btn-sm fa fa-sort-amount-asc "  + (this.props.obj.state.filters.order == '' ? "active": "")}
                                    onClick={this.props.obj.setFilters}>
                            </button>
                    </div>
                    <br />
                    <small>Тип карты</small>
                    <select id="type" name={'card_type'} onChange={this.props.obj.setFilters}
                            value={this.props.obj.state.filters.card_type}
                            className="form-control form-control-sm">
                            <option value="">Все</option>
                            <option value="bonus">Бонусная</option>
                            <option value="discount">Дисконтная</option>
                            <option value="combo">Комбо</option>
                    </select>
                    <label className="form-check-label form-control-sm">
                        <input className={css_form_control_sm + "form-check-input"}
                               type="checkbox"
                               checked={this.props.obj.state.filters.showDeleted}
                               onChange={this.props.obj.showDeleted}
                               name="showDeleted" /> Показать удаленные
                    </label>
                </div>

            </div>
            <hr />
        </div>
        )
    }
}

export default CardsList;