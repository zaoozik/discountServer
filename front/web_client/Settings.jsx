import React from 'react';
import { Link } from 'react-router-dom';
import {Alert} from './Tools.jsx';
import ReactDOM from 'react-dom';

var COID = 0;

class Org extends React.Component{
    constructor(props){
        super(props);
        this.state={
            org: {}
        }
    }

    async loadOrg(){
        let data = await fetch("/settings/api/org",
            {
                method: 'get',
                credentials: 'include',
            } ).then(response =>response.json())
        this.setState(
            {
                org: data
            }
        )

    }

    componentDidMount(){
        this.loadOrg();

    }


    render(){

        return(

            <div class="">
                <br />
                    <h5> Организация - {this.state.org.name}</h5>
                    <p>Активность до: {this.state.org.active_to}</p>
                    <hr />
                        <p><a href="/static/documents/vdk_service_install.exe">
                            <i className="fa fa-download" aria-hidden="true"></i> Установщик службы VtiDiscountKeeper</a></p>
                        <hr />
            </div>
            )
    }
}


class COUnitModal extends React.Component{
    constructor(props){
        super(props);
        this.state = {
            address:
                "",

            name:
                "",

        }

        this.saveCOUnit = this.saveCOUnit.bind(this);
    }

    async saveCOUnit(){
        let data = await fetch("/settings/api/counit/",
            {
                method: 'PUT',
                body: JSON.stringify(this.state),
                credentials: 'include',
            } ).then(response =>response.json())

        if (data.status=='success'){
            $('#co_modal_close').click();
            this.props.update();
            ReactDOM.render(<Alert isError={false} message={data.message}/>, document.getElementById('alert'));
        }
        if (data.status=='error'){
            ReactDOM.render(<Alert isError={true} message={data.message}/>, document.getElementById('alert'));
        }

    }

    onInputChange = (e) =>{
        let parameter = e.target.name;
        let temp = this.state;
        temp[parameter] = e.target.value;
        //temp["co_unit_id"] = COID;

        this.setState(
            {
                ... temp
            }
        )

    }

    render(){
        let obj = this;
        return(
            <div className="modal fade" id="COUnitModal">
                <div className="modal-dialog" role="document">
                    <div className="modal-content">
                        <div className="modal-header">
                            <h5 className="modal-title">Торговый объект</h5>
                            <button type="button" class="close"  data-dismiss="modal" aria-label="Close">
                                <span aria-hidden="true">&times;</span>
                            </button>
                        </div>
                        <div className="modal-body">
                            <div key="COUnitForm" >
                                <label >Наименование*:</label>
                                <input type="text"
                                       name="name"
                                       onChange={obj.onInputChange}
                                       value={obj.state.name}
                                       required=""
                                       className="form-control
                                                form-control-sm"
                                />
                                <label >Адрес*:</label>
                                <input type="text"
                                       name="address"
                                       onChange={obj.onInputChange}
                                       value={obj.state.address}
                                       className="form-control form-control-sm" />
                            </div>
                        </div>
                        <div className="modal-footer">
                            <button type="button" className="btn btn-primary" onClick={this.saveCOUnit}>Сохранить</button>
                            <button type="button" id="co_modal_close" className="btn btn-secondary" data-dismiss="modal">Отмена</button>
                        </div>
                    </div>
                </div>
            </div>
        )
    }
}



class WorkplaceModal extends React.Component{
    constructor(props){
        super(props);
        this.state = {
            co_unit_id:
            COID,

            frontol_version:
                "",

            name:
                "",

            serial_number:
                ""

        }

        this.saveWorkplace = this.saveWorkplace.bind(this);
    }

    async saveWorkplace(){
        this.setState(
            {
                co_unit_id: COID
            }
        );
        let data = await fetch("/settings/api/workplaces/",
            {
                method: 'PUT',
                body: JSON.stringify(this.state),
                credentials: 'include',
            } ).then(response =>response.json())

        if (data.status=='success'){
            $('#modal_close').click();
            this.props.update();
            ReactDOM.render(<Alert isError={false} message={data.message}/>, document.getElementById('alert'));
        }
        if (data.status=='error'){
            ReactDOM.render(<Alert isError={true} message={data.message}/>, document.getElementById('alert'));
        }

    }

    onInputChange = (e) =>{
        let parameter = e.target.name;
        let temp = this.state;
        temp[parameter] = e.target.value;
        temp["co_unit_id"] = COID;

        this.setState(
            {
                ... temp
            }
        )

    }

    render(){
        let obj = this;
        return(
            <div className="modal fade" id="CashBoxModal">
                <div className="modal-dialog" role="document">
                    <div className="modal-content">
                        <div className="modal-header">
                            <h5 className="modal-title">Касса</h5>
                            <button type="button" class="close"  data-dismiss="modal" aria-label="Close">
                                <span aria-hidden="true">&times;</span>
                            </button>
                        </div>
                        <div className="modal-body">
                            <div key="CashBoxForm" >
                                    <label >Наименование*:</label>
                                        <input type="text"
                                               name="name"
                                               onChange={obj.onInputChange}
                                               value={obj.state.name}
                                               required=""
                                               className="form-control
                                                form-control-sm"
                                        />
                                    <label >Номер кассы*:</label>
                                        <input type="number"
                                               name="serial_number"
                                               onChange={obj.onInputChange}
                                               value={obj.state.serial_number}
                                               min="0"
                                               className="form-control form-control-sm"
                                               required="" />
                                    <label>Версия Frontol*:</label>
                                                <input type="text"
                                                       name="frontol_version"
                                                       onChange={obj.onInputChange}
                                                       value={obj.state.frontol_version}
                                                       required=""
                                                       className="form-control form-control-sm" />
                            </div>
                        </div>
                        <div className="modal-footer">
                            <button type="button" className="btn btn-primary" onClick={this.saveWorkplace}>Сохранить</button>
                            <button type="button" id="modal_close" className="btn btn-secondary" data-dismiss="modal">Отмена</button>
                        </div>
                    </div>
                </div>
            </div>
        )
    }
}

class Workplaces extends React.Component{
    constructor(props){
        super(props);
        this.state = {
            workplaces: []
        }

        this.deleteWorkPlace = this.deleteWorkPlace.bind(this);
        this.deleteCOUnit = this.deleteCOUnit.bind(this);
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

    async deleteWorkPlace(e){
        if (confirm('Вы действительно хотите удалить кассу?')) {
            let data = await fetch("/settings/api/workplaces",
                {
                    method: 'delete',
                    credentials: 'include',
                    body: e.target.value
                }).then(response => response.json())

            if (data.status == 'success') {
                this.loadWorkPlaces();
                ReactDOM.render(<Alert isError={false} message={data.message}/>, document.getElementById('alert'));
            }
            if (data.status == 'error') {
                ReactDOM.render(<Alert isError={true} message={data.message}/>, document.getElementById('alert'));
            }


        }
    }

    async deleteCOUnit(e){
        if (confirm('Вы действительно хотите удалить торговый объект?')) {
            let data = await fetch("/settings/api/counit",
                {
                    method: 'delete',
                    credentials: 'include',
                    body: e.target.value
                }).then(response => response.json())

            if (data.status == 'success') {
                this.loadWorkPlaces();
                ReactDOM.render(<Alert isError={false} message={data.message}/>, document.getElementById('alert'));
            }
            if (data.status == 'error') {
                ReactDOM.render(<Alert isError={true} message={data.message}/>, document.getElementById('alert'));
            }


        }
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
        let obj = this;

        let workplaces = this.state.workplaces.map(function (item, index) {
            let setCOId = (e) =>{
                COID = e.target.value;
            }
            return (
                <li className={"list-group-item"} key={"workplace_"+index} style={{marginBottom: '1rem'}}>
                    <button type="button" className="close fa fa-trash" aria-label="Close" value={item.id} onClick={obj.deleteCOUnit}>

                    </button>

                    <p><strong>{ item.name +"  "}</strong>
                    </p>
                    <p className={"font-italic"}>Адрес: {item.address}</p>
                    <a data-toggle="collapse" href={"#co_"+item.id} role="button" aria-expanded="false" aria-controls="collapseExample"><i class="fa fa-sort-desc fa-2x" aria-hidden="true"></i></a>
                    <div className={"containter collapse"} id={"co_"+item.id}>
                        <div className={"row"}>
                            {(item.cashboxes.length)==0 ? <div className={"text-muted col"}> <p>кассы отсутствуют </p> </div> : ""}
                            {item.cashboxes.map(function(item, index){
                                return(
                                <div className={"card"} style={{marginLeft: '1rem', marginBottom: '1rem'}}>
                                    <div className={"card-body"}>
                                        <button type="button" className="close fa fa-trash" aria-label="Close" value={item.id} onClick={obj.deleteWorkPlace}>

                                        </button>
                                        <h6 className={"card-title"}><i class="fa fa-money" aria-hidden="true"></i> {item.name}</h6>
                                        <p>
                                            Номер кассы: {item.serial_number}<br />
                                            Статус: { item.online ? online: offline}<br/>
                                            Версия Frontol - { item.frontol_version }<br/>
                                            Ключ доступа FRONTOL: <br /> {item.frontol_key}
                                        </p>
                                        <div className={"card-footer"}><a href={"/settings/frontol/?KEY=" + item.frontol_key }>
                                            <i className="fa fa-download" aria-hidden="true" > </i>
                                            Файл настроек FRONTOL5
                                        </a>
                                        </div>
                                    </div>
                                </div>
                                )
                            })}


                        </div>

                        <button
                            value={item.id}
                            className="btn btn-success btn-sm"
                            id="addCashBoxButton"
                            data-toggle="modal"
                            onClick={setCOId}
                            data-target="#CashBoxModal"><i class="fa fa-plus" aria-hidden="true"></i> Новая касса </button>
                    </div>

                </li>

            )

        })
        return(
            <div>
                <hr />
                <h5>Торговые объекты</h5>
                <hr />
                <ul class="list-group">
                {workplaces}
                </ul>
                <br />
                <p>
                    <button className="btn btn-success btn-sm" id="addCOUnitButton" data-toggle="modal" data-target="#COUnitModal"><i class="fa fa-money" aria-hidden="true"></i> Добавить торговый объект </button>
                </p>

                <WorkplaceModal update={this.loadWorkPlaces.bind(this)}/>
                <COUnitModal update={this.loadWorkPlaces.bind(this)}/>

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

        let parameters = JSON.parse(data.parameters);
        if (! parameters.bonus_mechanism){
            parameters['bonus_mechanism'] = 'bonus_percent';
        }
        if (! parameters.round){
            parameters['round'] = 'math';
        }

        this.setState({
            id: data.id,
            algorithm: data.algorithm,
            rules: rules,
            parameters: parameters,
            time_delay: data.time_delay

        })


    }


    onAlgorithmChange = (e) =>{
        this.setState(
            {
                algorithm: e.target.value,
                parameters: {bonus_mechanism: 'bonus_percent',
                                round: 'math'},
                rules: []
            }
        )
    }

    onBonusMechChange = (e) =>{
        console.log('changing mechanism');
        console.log(e.target.value);
        let params = this.state.parameters;
        params['bonus_mechanism'] = e.target.value;
        this.setState(
            {
                parameters: params
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

        this.setState(
            {
                parameters: temp
            }
        )

    }


    onTimeDelayChange = (e) =>{
        this.setState(
            {
                time_delay: e.target.value
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
        let bonus_cost_meh;
        let bonus_percent_meh;



        if (this.state.algorithm == "bonus"){
            alg_bonus = true;
        }
        if (this.state.algorithm == "discount"){
            alg_discount = true;
        }
        if (this.state.algorithm == "combo"){
            alg_combo = true;
        }

        if (this.state.parameters.bonus_mechanism == 'bonus_cost'){
            bonus_cost_meh = true;
            bonus_percent_meh = false;
            //console.log('bonus_cost');
        }

        else if (this.state.parameters.bonus_mechanism == 'bonus_percent'){
            bonus_percent_meh = true;
            bonus_cost_meh = false;
            //console.log('bonus_percent');
        }
        else{
            bonus_percent_meh = true;
            bonus_cost_meh = false;
        }

        let bonus_parameters = (obj) =>{

            let bonus_percent = () =>{
                return(
                    <div>
                        <label>Сколько процентов от суммы покупки зачисляются в виде бонусов:</label>
                        <input type ="number"
                               onChange={this.onInputChange}
                               value={this.state.parameters.bonus_percent}
                               className={css_form_control_sm}
                               name={"bonus_percent"}/>
                    </div>
                )
            };


            let bonus_cost = () => {
                return(
                    <div>
                    <label>Стоимость 1 бонуса:</label>
                    <input
                    type = "number"
                    onChange = {this.onInputChange}
                    value = {this.state.parameters.bonus_cost}
                    className = {css_form_control_sm}
                    name = {"bonus_cost"} />
                    </div>)
            }

            return(
                <div>
                    <h5>Правила начисления бонусов:</h5>
                    < hr />
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

                    < br/>
                    <h6>Механизм начисления бонусов:</h6>
                    <div className="form-group ">
                        <div className={" form-inline"}>
                            <input checked={bonus_percent_meh} onChange={this.onBonusMechChange} type={"radio"}  value={'bonus_percent'} name={'bonus_mech'} id={'bonus_percent'} />
                            <label className="form-check-label" >Процент от суммы покупки</label>
                        </div>
                        <div className={" form-inline"}>
                            <input checked={bonus_cost_meh} type={"radio"} onChange={this.onBonusMechChange} value={'bonus_cost'}  name={'bonus_mech'} id={'bonus_cost'}/>
                            <label className="form-check-label" >Стоимость бонуса</label>
                        </div>
                    </div>

                    {(bonus_percent_meh)? bonus_percent(): null}
                    {(bonus_cost_meh)? bonus_cost(): null}



                    <label>Режим округления:</label>
                    <select name="round" id="id_round" value={this.state.parameters.round ? this.state.parameters.round: 'math'} onChange={this.onInputChange} className="form-control ">
                        <option value="math">Математическое округление</option>

                        <option value="up">В большую сторону</option>

                        <option value="down">В меньшую сторону</option>

                        <option value="None">Без округления</option>

                    </select>

                    <label>Задержка перед начислением бонуса, дни:</label>
                    <input type ="number"
                           onChange={this.onTimeDelayChange}
                           value={this.state.time_delay}
                           className={css_form_control_sm}
                           name={"assume_delta"}/>

                    <label>Срок действия бонусов, месяцы:</label>
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
                    <h5>Правила начисления скидок:</h5>
                    < hr />
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

                    <br />

                <div id="discount-rules-controls" className={'bottom-buttons'}>
                    <button type="button" className="btn btn-default" onClick={obj.addDiscountRule} >+</button>
                    <button type="button" className="btn btn-default" onClick={obj.remDiscountRule} >-</button>
                </div>
                </div>
            )
        };



        return (
            <div className={""}>
                <br/>
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

                            {(alg_bonus || alg_combo)? bonus_parameters(this): null}
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
                        <Org />
                        {/* ORG SETTINGS END */}
                    </div>



                </div>

            </div>
        )

    }
}

