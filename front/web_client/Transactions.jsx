import React from "react";
import ReactDOM from "react-dom";
import { Link } from 'react-router-dom'

export class Transactions extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            transactions: [],
            list_current_position: 0,
            list_count: 30,
            list_total: 0,
            list_end: false

        }


    }

    async loadTransactions() {
        let data = await fetch("/transactions/api/",
            {
                method: 'get',
                credentials: 'include',
            } ).then(
            response =>response.json())

        this.setState(
            {
                transactions: data
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
        this.loadTransactions();
        document.getElementById('tbody').addEventListener('scroll', this.handleScroll);
    }


    render() {
        let transactions = this.state.transactions.map(function (item, index,){
            let date = new Date(item.date);

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


            return (
                <tr key={'trans_id_'+item.id}>
                    <td>{date.toLocaleString()}</td>
                    <td>{type}</td>
                    <td><Link to={"/card/"+item.card.code + "/"}>{item.card.code}</Link></td>
                    <td>{isNoneRub(item.sum)}</td>
                    <td>{item.bonus_before}</td>
                    <td>{isNone(item.bonus_add)}</td>
                    <td>{isNoneRub(item.bonus_reduce)}</td>
                    <td>{item.shop}</td>
                    <td>{item.workplace}</td>
                    <td>{item.doc_number}</td>
                    <td>{item.session}</td>
                    <td>{item.doc_close_user}</td>
                </tr>

            )
        })
        if (transactions.length == 0){
            transactions= (
                <tr key={'history_empty'}>
                    <td colSpan={3}>Операции отсутствуют</td>

                </tr>
            )
        }

        return(
            <div>
                <br />
                <h3>История операций</h3>
                <hr />
                    <div class="form-group row">
                        <div class="col-3">
                            <label for = "dateFrom">Начало периода</label>
                            <input class="form-control form-control-sm" type="text" id="dateFrom" />
                                <label for = "dateTo">Конец периода</label>
                                <input class="form-control form-control-sm" type="text" id="dateTo" />
                                    <label for = "type">Тип операции</label>
                                    <select class="form-control form-control-sm" name="type" id="type">
                                        <option value="">Любой</option>
                                        <option value="sell">Продажа</option>
                                        <option value="refund">Возврат</option>
                                        <option value="bonus_add">Начисление бонусов</option>
                                        <option value="bonus_reduce">Списание бонусов</option>
                                        <option value="discount_recount">Пересчет скидки</option>
                                    </select>
                        </div>

                        <div class="col-3">
                            <label for = "card">Номер карты</label>
                            <input class="form-control form-control-sm" type="text" id="card"/>
                                <label for = "workplace">Рабочее место</label>
                                <input class="form-control form-control-sm" type="text" id="workplace" />
                                    <label for = "session">Номер смены</label>
                                    <input class="form-control form-control-sm" type="text" id="session" />
                        </div>
                        <div class="col-3">
                            <label for = "doc_close_user">Пользователь</label>
                            <input class="form-control form-control-sm" type="text" id="doc_close_user"/>
                                <label for = "doc_number">Номер документа</label>
                                <input class="form-control form-control-sm" type="text" id="doc_number" />
                                    <label for = "shop">Номер магазина</label>
                                    <input class="form-control form-control-sm" type="text" id="shop" />

                        </div>
                        <div class="col-3" style={{display: "inline"}}>
                            <button onclick="dataUpdate();" class="btn btn-default btn-sm"><i class="fa fa-filter" aria-hidden="true"></i> Фильтр </button>
                            <span> </span>
                            <button class="btn btn-default btn-sm" onclick="clearFilter();"><i class="fa fa-repeat" aria-hidden="true"></i> Сбросить </button>
                        </div>
                    </div>


                    <hr />
                            <div class="form-group row pull-right">
                                <small id="total">{this.state.list_current_position + ' из '+ this.state.list_total}</small>
                            </div>



                            <div id={"data"}>
                <table className={"scroll-table-trans"} id={'scrollData'}>
                    <thead>
                    <tr>
                        <th>Дата/время</th>
                        <th>Тип</th>
                        <th>Карта</th>
                        <th>Сумма покупки</th>
                        <th>Бонусов до операции</th>
                        <th>Начисление бонусов</th>
                        <th>Списание бонусов</th>
                        <th>Номер магазина</th>
                        <th>Рабочее место</th>
                        <th>Номер документа</th>
                        <th>Номер смены</th>
                        <th>Пользователь</th>

                    </tr>
                    </thead>

                    <tbody
                        id={'tbody'}
                        style={{height: '485px'}}>
                    {transactions}
                    </tbody>
                </table>
            </div>


        </div>
        )

    }


}