import React from 'react';
import { Link } from 'react-router-dom';
import {Alert} from './Tools.jsx';
import ReactDOM from 'react-dom';


class Workplaces extends React.Component{
    constructor(props){
        super(props);
        this.state = {
            workplaces: []
        }
    }

    async loadWorkPlaces(){
        let data = await fetch("/settings/api/workplaces",
            {
                method: 'get',
                credentials: 'include',
            } ).then(response =>response.json())
        this.setState(
            {
                workplaces: data
            }
        )

    }

    componentDidMount(){
        this.loadWorkPlaces();
    }

    render(){
        let online = (
            <span style={{"color": "green"}}>онлайн</span>
        );
        let offline = (
            <span style={{"color": "red"}}>оффлайн</span>
        );
        let workplaces = this.state.workplaces.map(function (item, index) {
            return (
                <div key={"workplace_"+index}>
                    <p><strong>Касса: "{ item.name }"</strong>
                        <button className="btn btn-small btn-outline-danger" >
                            <i className="fa fa-times" aria-hidden="true"></i>
                        </button>
                    </p>
                    <p>Адрес: {item.address}</p>
                    <p>Статус: { item.online ? online: offline}</p>
                    <p>Версия Frontol - { item.frontol_version }</p>
                    <p>Ключ доступа FRONTOL - {item.frontol_key}</p>
                    <p><a href={"/settings/frontol/?KEY=" + item.frontol_key }>
                        <i className="fa fa-download" aria-hidden="true" > </i>
                        Файл настроек FRONTOL
                    </a>
                </p>
                    <hr />
                </div>

            )

        })
        return(
            <div>
                <br />
                <p>Доступно касс для добавления {"3"}</p>
                <hr />
                {workplaces}

                <p>
                    <button className="btn btn-success btn-sm" id="addCashBoxButton" data-toggle="modal" data-target="#CashBoxModal"><i class="fa fa-money" aria-hidden="true"></i> Добавить </button>
                </p>

            </div>
        )

    }
}

export class Settings extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            id: '',
            algorithm: '',
            parameters: {},
            rules: [],
            time_delay: 0,
            rules_count: 0,

        }

        this.saveSettings = this.saveSettings.bind(this);
        this.loadSettings = this.loadSettings.bind(this);

    }

    async loadSettings() {
        let data = await fetch("/settings/api/",
            {
                method: 'get',
                credentials: 'include',
            } ).then(response =>response.json())

        let rules;
        try{
            rules = data.rules;
        }
        catch (err) {
            rules = []
        }
        console.log(rules);

        this.setState({
            id: data.id,
            algorithm: data.algorithm,
            rules: rules,
            parameters: data.parameters ? JSON.parse(data.parameters): {},
            time_delay: data.time_delay

        })
    }


    onAlgorithmChange = (e) =>{
        this.setState(
            {
                algorithm: e.target.value,
                parameters: {},
                rules: []
            }
        )
    }


    onRuleChangeDiscount = (e) =>{
        let rules = this.state.rules;
        rules[e.target.name][0] = e.target.value;
        this.setState(
            {
                rules: rules,
            }
        )

    }


    onRuleChangeAccum = (e) =>{
        let rules = this.state.rules;
        rules[e.target.name][1] = e.target.value;
        this.setState(
            {
                rules: rules,
            }
        )

    }



    onInputChange = (e) =>{
        let parameter = e.target.name;
        let temp = this.state.parameters;
        temp[parameter] = e.target.value;
        console.log(temp);

        this.setState(
            {
                parameters: temp
            }
        )

    }

    addDiscountRule =(dis, val) =>{
        //console.log('hello');
        let rules = this.state.rules;
        rules.push([null, null]);
        this.setState({
            rules: rules
        });
    }

    remDiscountRule =() =>{
        console.log('hello');
        let rules = this.state.rules;
        rules.pop();
        this.setState({
            rules: rules
        });
    }


    async saveSettings () {
        let data = await fetch("/settings/api/",
            {
                method: 'PUT',
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
    }

    componentDidMount(){
        this.loadSettings();


    }


    render() {

        let css_form_control_sm = "form-control form-control-sm ";

        let alg_discount = false;
        let alg_bonus = false;
        let alg_combo = false;


        if (this.state.algorithm == "bonus"){
            alg_bonus = true;
        }
        if (this.state.algorithm == "discount"){
            alg_discount = true;
        }
        if (this.state.algorithm == "combo"){
            alg_combo = true;
        }

        let bonus_parameters = () =>{
            return(
                <div>
                    <label>Минимальная сумма покупки для зачисления бонусов:</label>
                    <input
                        type = "number"
                        onChange = {this.onInputChange}
                        value = {this.state.parameters.min_transaction}
                        className = {css_form_control_sm}
                        name = {"min_transaction"}
                    />

                    <label>Сколько процентов от суммы покупки можно оплатить бонусами:</label>
                    <input type ="number"
                           onChange={this.onInputChange}
                           value={this.state.parameters.max_bonus_percentage}
                           className={css_form_control_sm}
                           name={"max_bonus_percentage"}/>

                    <h6>Начисление бонусов</h6>
                    <div className={" form-inline"}>
                        <input defaultChecked={true} type={"radio"} className={""} name={'bonus_accum_type'} />
                        <label className="form-check-label" >Процент от суммы покупки</label>
                    </div>
                    <div className={" form-inline"}>
                        <input type={"radio"} className={""} name={'bonus_accum_type'} />
                        <label className="form-check-label" >Комбинированный</label>
                    </div>

                    <label>Стоимость 1 бонуса:</label>
                    <input type ="number"
                           onChange={this.onInputChange}
                           value={this.state.parameters.bonus_cost}
                           className={css_form_control_sm}
                           name={"bonus_cost"}/>

                    <label>Сколько процентов от суммы покупки зачисляются в виде бонусов:</label>
                    <input type ="number"
                           onChange={this.onInputChange}
                           value={this.state.parameters.bonus_percent}
                           className={css_form_control_sm}
                           name={"bonus_percent"}/>

                    <label>Режим округления:</label>
                    <select className={css_form_control_sm}>
                    </select>

                    <label>Задержка перед начислением бонуса, часы:</label>
                    <input type ="number"
                           onChange={this.onInputChange}
                           value={this.state.parameters.assume_delta}
                           className={css_form_control_sm}
                           name={"assume_delta"}/>

                    <label>Срок действия бонусов, дни:</label>
                    <input type ="number"
                           onChange={this.onInputChange}
                           value={this.state.parameters.bonus_lifetime}
                           className={css_form_control_sm}
                           name={"bonus_lifetime"}/>
                    <hr />
                </div>

            )
        }

        let discount_data=null;

        if (this.state.rules.length >0 ) {
            console.log('rules started');
            let obj = this;
            discount_data = this.state.rules.map(function (item, index) {
                console.log(obj.state.rules[index]);
                return (
                        <div key={"discount_rule_"+index} className="form-row rule">
                            <div className={'col-1'}>
                                <label>{index+1 + "."}</label>
                            </div>
                            <div className="col-3 ">

                                <input type="number"
                                       name={index}
                                       onChange={obj.onRuleChangeDiscount}
                                       min="0" value={obj.state.rules[index][0]} className="form-control form-control-sm discount"
                                       placeholder="Процент скидки"
                                />
                            </div>
                            <div className="col-3 ">

                                <input type="number"
                                       name={index}
                                       onChange={obj.onRuleChangeAccum}
                                       min="0" value={obj.state.rules[index][1]} className="form-control form-control-sm accum"
                                       placeholder="Необходимые накопления"

                                />
                            </div>
                        </div>

                )

            })
        }

        let discount_parameters = () => {
            let obj = this;
            return(
                <div>
                    <div className="form-row rule">

                            <div className={"col-1"}>
                                <label className="form-control-sm"></label>
                            </div>
                            <div className={"col-3"}>
                                <label className="form-control-sm">Процент скидки</label>
                            </div>
                            <div className={"col-3"}>
                                <label className="form-control-sm">Необходимые накопления</label>
                            </div>
                    </div>
                    <div  id={'discount-rules'}>
                            {discount_data}
                    </div>

                <div id="discount-rules-controls" className={'bottom-buttons'}>
                    <button type="button" className="btn btn-default" onClick={obj.addDiscountRule} >+</button>
                    <button type="button" className="btn btn-default" onClick={obj.remDiscountRule} >-</button>
                </div>
                </div>
            )
        };



        return (
            <div className={""}>
                <h3>Настройки</h3>
                <ul className="nav nav-tabs" id="myTab" role="tablist">
                    <li className="nav-item">
                        <a className="nav-link active" id="discount-tab" data-toggle="tab" href="#discount" role="tab" aria-controls="discount" aria-selected="true">Дисконтная система</a>
                    </li>
                    <li className="nav-item">
                        <a className="nav-link" id="workplace-tab" data-toggle="tab" href="#workplace" role="tab" aria-controls="workplace" aria-selected="false">Кассы</a>
                    </li>
                    <li className="nav-item">
                        <a className="nav-link" id="org-tab" data-toggle="tab" href="#org" role="tab" aria-controls="org" aria-selected="false">Организация</a>
                    </li>
                </ul>

                <div className="tab-content" id="settingsContent">


                    <div className="tab-pane fade show active" id="discount" role="tabpanel" aria-labelledby="discount-tab">
                        {/* DISCOUNT SETTINGS START */}

                        <div>
                            <hr />
                            <h5>Выбор режима работы</h5>
                            < hr />
                        <div className="form-group ">

                            <div className={"form-inline"}>

                                <input onChange={this.onAlgorithmChange}  checked={alg_bonus} id="alg_bonus" type={"radio"} value={'bonus'} className={""} name={'algorithm'} />
                                <label className="form-check-label" >Бонусы</label>
                            </div>
                            <div className={" form-inline"}>

                                <input onChange={this.onAlgorithmChange} id="alg_discount" checked={alg_discount} type={"radio"} value={'discount'} className={""} name={'algorithm'} />
                                <label className="form-check-label" >Накопительная скидка</label>
                            </div>
                            <div className={" form-inline"}>

                                <input onChange={this.onAlgorithmChange} id="alg_combo" checked={alg_combo} type={"radio"} value={'combo'} className={""} name={'algorithm'} />
                                <label className="form-check-label" >Комбинированный</label>
                            </div>


                        </div>
                                <hr />
                            <h5>Параметры режима</h5>
                            {(alg_bonus || alg_combo)? bonus_parameters(): null}
                            {(alg_discount || alg_combo)? discount_parameters(): null}



                                    <p className="text-center">

                                    <br />
                                    <button type="button" onClick={this.saveSettings} className="btn btn-lg">Сохранить</button>
                                </p>

                        </div>


                        {/* DISCOUNT SETTINGS ENDS */}
                    </div>

                    <div className="tab-pane fade" id="workplace" role="tabpanel" aria-labelledby="workplace-tab">
                        {/* WORKPLACE SETTINGS START */}
                            <Workplaces/>
                        {/* WORKPLACE SETTINGS ENDS */}
                    </div>

                    <div className="tab-pane fade" id="org" role="tabpanel" aria-labelledby="org-tab">
                        {/* ORG SETTINGS START */}
                        {/* ORG SETTINGS END */}
                    </div>



                </div>

            </div>
        )

    }
}

