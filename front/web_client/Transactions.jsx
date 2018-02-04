import React from "react";
import ReactDOM from "react-dom";

export class Transactions extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            transactions: []

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

    componentDidMount(){
        this.loadTransactions();
    }


    render() {
        let transactions = this.state.transactions.map(function (item, index,){
            let date = new Date(item.date);

            return (
                <tr key={'trans_id_'+item.id}>
                    <td>{date.toLocaleString()}</td>
                    <td>{item.type}</td>
                    <td>{item.card}</td>
                    <td>{item.sum}</td>
                    <td>{item.bonus_before}</td>
                    <td>{item.bonus_add}</td>
                    <td>{item.bonus_reduce}</td>
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
                <tr key={'bonus_empty'}>
                    <td colSpan={3}>Бонусы отсутствуют</td>

                </tr>
            )
        }

        return(
            <div>

            {/* COUNTER PANEL*/}

            {/*<div class="form-group row pull-right">*/}
                {/*<small id="total">{this.state.list_current_position + ' из '+ this.state.list_total}</small>*/}
            {/*</div>*/}

            <div id={"data"}>
                <table className={"table table-striped table-sm"} id={'scrollData'}>
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