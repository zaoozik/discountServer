import React from "react";
import { Link } from 'react-router-dom'

export class Queues extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            tasks: []

        }


    }

    async loadTasks() {
        let data = await fetch("/queue/api/",
            {
                method: 'get',
                credentials: 'include',
            } ).then(
            response =>response.json())

        this.setState(
            {
                tasks: data
            }
        )
    }

    componentDidMount(){
        this.loadTasks();
    }


    render() {
        let tasks = this.state.tasks.map(function (item, index,){
            let queue_date = new Date(item.queue_date);
            let execution_date = new Date(item.execution_date);

            let type;
            if (item.operation == 'bonus') {
                type = (<span style={{color: 'red'}}>Начисление бонусов</span>);
            }



            return (
                <tr key={'trans_id_'+item.id}>
                    <td>{execution_date.toLocaleString()}</td>
                    <td>{queue_date.toLocaleString()}</td>
                    <td>{type}</td>
                    <td><Link to={"/card/"+item.card.code + "/"}>{item.card.code}</Link></td>
                    <td>{(item.transaction.sum) + " руб."}</td>
                    <td>{item.transaction.shop}</td>
                    <td>{item.transaction.workplace}</td>
                    <td>{item.transaction.doc_number}</td>
                    <td>{item.transaction.session}</td>
                </tr>

            )
        })
        if (tasks.length == 0){
            tasks= (
                <tr>
                    <td colSpan={3}>Задания отсутствуют</td>

                </tr>
            )
        }

        return(
            <div>
                <br />
                <h3>Текущие задания</h3>
                <br />


                <div id={"data"}>
                    <table className={"table table-striped"} id={'scrollData'}  style={{'font-size': '11pt'}}>
                        <thead>
                        <tr>
                            <th>Будет выполнено</th>
                            <th>Время создания</th>
                            <th>Тип</th>
                            <th>Карта</th>
                            <th>Сумма покупки</th>
                            <th>Номер магазина</th>
                            <th>Рабочее место</th>
                            <th>Номер документа</th>
                            <th>Смена</th>
                        </tr>
                        </thead>

                        <tbody
                            id={'tbody'}>
                        {tasks}
                        </tbody>
                    </table>
                </div>


            </div>
        )

    }


}